#!/usr/bin/env python3
"""
MDS Design System Selection Engine (DSSE) — Mathematical Core Engine
Implements the locked and approved 5-pillar decoupled mathematical specification:
1. Candidate Suitability / Selection Score (Normalized 0.0% - 100.0%)
2. Hard Constraint Tri-State Eligibility Gate (PASS / FAIL / UNKNOWN)
3. Decision Margin & Deterministic Tie-Break Cascade (<= 1.0%, 1.0% - 3.0%, > 3.0%)
4. Conjunctive Epistemic Confidence Model (C_epistemic = C_req * C_eval * C_evid)
5. Rule-Based Confidence Gating (Family C: HIGH / MEDIUM / LOW) & Governance Triggers
"""

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from tools.dsse.catalog import CandidateCatalog, Candidate

ENGINE_VERSION = "1.0.0"

# Standard Discrete Evidence Taxonomy (Ratified in DSSE-ADR-001)
EVIDENCE_TIERS: Dict[str, float] = {
    "CODE_AUDITED": 1.00,
    "OFFICIAL_DOCS": 0.75,
    "COMMUNITY": 0.50,
    "INFERRED": 0.25,
    "UNKNOWN": 0.00
}

# Standard Semantic Priority Weights (Ratified in DSSE-ADR-001)
PRIORITY_WEIGHTS: Dict[str, float] = {
    "Critical": 1.00,
    "High": 0.75,
    "Medium": 0.50,
    "Low": 0.25,
    "N/A": 0.00
}

ALL_12_DIMENSIONS: List[str] = [f"D{i}" for i in range(1, 13)]


def calculate_c_req(declared_dims: List[str]) -> float:
    """
    Requirements Coverage (C_req) = |{explicitly declared dimensions, including N/A}| / 12
    """
    explicit_count = len([d for d in declared_dims if d in ALL_12_DIMENSIONS])
    return round(explicit_count / 12.0, 4)


def calculate_c_eval(active_dims: List[str], rated_dims: List[str]) -> float:
    """
    Evaluation Coverage (C_eval) = |active dimensions with benchmark ratings| / |active dimensions|
    """
    if not active_dims:
        return 0.0
    evaluated = len([d for d in active_dims if d in rated_dims])
    return round(evaluated / len(active_dims), 4)


def calculate_c_evid(active_dims: List[str], weights: Dict[str, float], evidence_dict: Dict[str, str]) -> float:
    """
    Evidence Quality (C_evid) = Σ (weight * tier) / Σ weight
    """
    total_weight = sum(weights.get(d, 0.0) for d in active_dims)
    if total_weight == 0.0:
        return 0.0
    weighted_sum = sum(
        weights.get(d, 0.0) * EVIDENCE_TIERS.get(evidence_dict.get(d, "UNKNOWN"), 0.0)
        for d in active_dims
    )
    return round(weighted_sum / total_weight, 4)


def calculate_c_epistemic(c_req: float, c_eval: float, c_evid: float) -> float:
    """
    Conjunctive Epistemic Confidence (C_epistemic) = C_req * C_eval * C_evid
    """
    return round(c_req * c_eval * c_evid, 4)


def classify_confidence_tier(c_req: float, c_eval: float, c_evid: float, has_critical_gap: bool = False) -> str:
    """
    Rule-Based Confidence Gating (Family C):
    HIGH: C_req >= 0.85, C_eval == 1.00, C_evid >= 0.75, No critical gap
    MEDIUM: C_req >= 0.60, C_evid >= 0.50, No critical gap
    LOW: Otherwise
    """
    if has_critical_gap:
        return "LOW"
    if c_req >= 0.85 and c_eval == 1.00 and c_evid >= 0.75:
        return "HIGH"
    if c_req >= 0.60 and c_evid >= 0.50:
        return "MEDIUM"
    return "LOW"


def calculate_selection_score(
    active_dims: List[str],
    weights: Dict[str, float],
    scores: Dict[str, float],
    hard_constraint_status: str = "PASS"
) -> float:
    """
    SelectionScore = Σ (s(d) * w(d)) / (10.0 * Σ w(d)) * 100%
    If hard_constraint_status == 'FAIL' -> forced to 0.0% (Disqualified)
    """
    if hard_constraint_status == "FAIL":
        return 0.0
    total_weight = sum(weights.get(d, 0.0) for d in active_dims)
    if total_weight == 0.0:
        return 0.0
    raw_sum = sum(scores.get(d, 0.0) * weights.get(d, 0.0) for d in active_dims)
    max_attainable = 10.0 * total_weight
    return round((raw_sum / max_attainable) * 100.0, 1)


def classify_decision_margin(delta: float) -> str:
    """
    Δ <= 1.0% -> Virtual Tie
    1.0% < Δ <= 3.0% -> Tie-Break Zone
    Δ > 3.0% -> Decisive Lead
    """
    if delta <= 1.0:
        return "Virtual Tie"
    elif delta <= 3.0:
        return "Tie-Break Zone"
    else:
        return "Decisive Lead"


@dataclass
class CandidateEvaluationResult:
    candidate_id: str
    name: str
    selection_score: float
    eligibility_status: str  # PASS / FAIL / UNKNOWN
    disqualification_reason: Optional[str] = None
    scores: Dict[str, float] = field(default_factory=dict)
    evidence: Dict[str, str] = field(default_factory=dict)
    suggested_configuration: Dict[str, str] = field(default_factory=dict)


@dataclass
class EvaluationOutput:
    report: Dict[str, Any]
    human_review_required: bool
    human_review_reasons: List[str]
    winning_candidate: Optional[CandidateEvaluationResult]
    exit_code: int


class DSSEEngine:
    def __init__(self, catalog: CandidateCatalog):
        self.catalog = catalog

    def evaluate(self, project_profile: Dict[str, Any]) -> EvaluationOutput:
        """
        Executes full 5-pillar mathematical evaluation of candidate catalog
        against the provided project profile.
        """
        project_name = project_profile.get("projectName", "Unnamed Project")
        context = project_profile.get("context", "")
        declared_dims = project_profile.get("dimensions", {})
        hard_constraints = project_profile.get("hardConstraints", [])

        # Parse declared dimensions & weights
        declared_dim_keys = list(declared_dims.keys())
        c_req = calculate_c_req(declared_dim_keys)

        weights: Dict[str, float] = {}
        active_dims: List[str] = []
        for d in ALL_12_DIMENSIONS:
            prio = declared_dims.get(d, "N/A" if d in declared_dims else None)
            if prio:
                w = PRIORITY_WEIGHTS.get(prio, 0.0)
                weights[d] = w
                if w > 0.0:
                    active_dims.append(d)

        # Evaluate each candidate in catalog
        results: List[CandidateEvaluationResult] = []
        has_critical_gap = False
        hc_unknown_encountered = False

        for candidate in self.catalog.candidates:
            # 1. Hard Constraints Eligibility Evaluation
            cand_hc_status = "PASS"
            disqual_reason = None

            for hc in hard_constraints:
                hc_id = hc.get("id")
                # Check candidate's rating on this constraint
                c_val = candidate.hard_constraints.get(hc_id, "PASS")
                if c_val == "FAIL":
                    cand_hc_status = "FAIL"
                    disqual_reason = f"Failed hard constraint: {hc.get('description', hc_id)}"
                    break
                elif c_val == "UNKNOWN":
                    cand_hc_status = "UNKNOWN"
                    hc_unknown_encountered = True

            # Extract scores and evidence for active dimensions
            cand_scores: Dict[str, float] = {}
            cand_evidence: Dict[str, str] = {}
            rated_dims: List[str] = []

            for d in active_dims:
                if d in candidate.dimensions:
                    rating = candidate.dimensions[d]
                    cand_scores[d] = rating.score
                    cand_evidence[d] = rating.evidence_tier
                    rated_dims.append(d)
                    # Check for critical dimension missing verified evidence
                    if weights.get(d, 0.0) == 1.00 and EVIDENCE_TIERS.get(rating.evidence_tier, 0.0) < 0.50:
                        has_critical_gap = True
                else:
                    cand_scores[d] = 0.0
                    cand_evidence[d] = "UNKNOWN"
                    if weights.get(d, 0.0) == 1.00:
                        has_critical_gap = True

            # Calculate Selection Score
            score = calculate_selection_score(active_dims, weights, cand_scores, cand_hc_status)

            results.append(CandidateEvaluationResult(
                candidate_id=candidate.id,
                name=candidate.name,
                selection_score=score,
                eligibility_status=cand_hc_status,
                disqualification_reason=disqual_reason,
                scores=cand_scores,
                evidence=cand_evidence,
                suggested_configuration=candidate.suggested_configuration
            ))

        # Sort candidates: Eligible first by score desc, then Disqualified
        eligible = [r for r in results if r.eligibility_status != "FAIL"]
        disqualified = [r for r in results if r.eligibility_status == "FAIL"]
        eligible.sort(key=lambda x: x.selection_score, reverse=True)
        ranked = eligible + disqualified

        top_cand = ranked[0] if ranked else None
        runner_up = ranked[1] if len(ranked) > 1 else None

        top_score = top_cand.selection_score if top_cand else 0.0
        runner_up_score = runner_up.selection_score if (runner_up and runner_up.eligibility_status != "FAIL") else 0.0

        delta = round(top_score - runner_up_score, 1)
        margin_class = classify_decision_margin(delta)

        # Tie-Break Cascade execution if in Tie-Break Zone
        tie_break_triggered = False
        tie_break_log: List[str] = []
        unresolved_tie_break = False

        if margin_class == "Tie-Break Zone" and runner_up and runner_up.eligibility_status != "FAIL":
            tie_break_triggered = True
            tie_break_log.append(f"Candidates '{top_cand.name}' and '{runner_up.name}' entered Tie-Break Zone (+{delta}%).")

            # Step 1: Critical Dimensions Lead
            crit_dims = [d for d in active_dims if weights.get(d, 0.0) == 1.00]
            top_crit = sum(top_cand.scores.get(d, 0.0) for d in crit_dims)
            run_crit = sum(runner_up.scores.get(d, 0.0) for d in crit_dims)
            if top_crit > run_crit:
                tie_break_log.append(f"Step 1 (Critical Dims): '{top_cand.name}' leads ({top_crit:.1f} vs {run_crit:.1f}). Resolved.")
            elif run_crit > top_crit:
                tie_break_log.append(f"Step 1 (Critical Dims): '{runner_up.name}' leads ({run_crit:.1f} vs {top_crit:.1f}). Rank swapped.")
                # Swap rank
                eligible[0], eligible[1] = eligible[1], eligible[0]
                ranked = eligible + disqualified
                top_cand, runner_up = ranked[0], ranked[1]
            else:
                tie_break_log.append(f"Step 1 (Critical Dims): Tied ({top_crit:.1f}). Proceeding to Step 2.")
                # Step 2: Primary Platform Fit (D1)
                top_d1 = top_cand.scores.get("D1", 0.0)
                run_d1 = runner_up.scores.get("D1", 0.0)
                if top_d1 > run_d1:
                    tie_break_log.append(f"Step 2 (Platform Fit D1): '{top_cand.name}' leads ({top_d1} vs {run_d1}). Resolved.")
                elif run_d1 > top_d1:
                    tie_break_log.append(f"Step 2 (Platform Fit D1): '{runner_up.name}' leads ({run_d1} vs {top_d1}). Rank swapped.")
                    eligible[0], eligible[1] = eligible[1], eligible[0]
                    ranked = eligible + disqualified
                    top_cand, runner_up = ranked[0], ranked[1]
                else:
                    tie_break_log.append(f"Step 2 (Platform Fit D1): Tied ({top_d1}). Proceeding to Step 3.")
                    # Step 3: Accessibility & RTL Combined (D3 + D4 unweighted)
                    top_a11y_rtl = top_cand.scores.get("D3", 0.0) + top_cand.scores.get("D4", 0.0)
                    run_a11y_rtl = runner_up.scores.get("D3", 0.0) + runner_up.scores.get("D4", 0.0)
                    if top_a11y_rtl > run_a11y_rtl:
                        tie_break_log.append(f"Step 3 (A11y+RTL): '{top_cand.name}' leads ({top_a11y_rtl:.1f} vs {run_a11y_rtl:.1f}). Resolved.")
                    elif run_a11y_rtl > top_a11y_rtl:
                        tie_break_log.append(f"Step 3 (A11y+RTL): '{runner_up.name}' leads ({run_a11y_rtl:.1f} vs {top_a11y_rtl:.1f}). Rank swapped.")
                        eligible[0], eligible[1] = eligible[1], eligible[0]
                        ranked = eligible + disqualified
                        top_cand, runner_up = ranked[0], ranked[1]
                    else:
                        tie_break_log.append(f"Step 3 (A11y+RTL): Tied ({top_a11y_rtl:.1f}). Proceeding to Step 4.")
                        # Step 4: Developer Ecosystem (D12)
                        top_d12 = top_cand.scores.get("D12", 0.0)
                        run_d12 = runner_up.scores.get("D12", 0.0)
                        if top_d12 > run_d12:
                            tie_break_log.append(f"Step 4 (Developer Ecosystem D12): '{top_cand.name}' leads ({top_d12} vs {run_d12}). Resolved.")
                        elif run_d12 > top_d12:
                            tie_break_log.append(f"Step 4 (Developer Ecosystem D12): '{runner_up.name}' leads ({run_d12} vs {top_d12}). Rank swapped.")
                            eligible[0], eligible[1] = eligible[1], eligible[0]
                            ranked = eligible + disqualified
                            top_cand, runner_up = ranked[0], ranked[1]
                        else:
                            tie_break_log.append("Step 5 (Human Escalation): Cascade unresolved. Mandatory Human Review triggered.")
                            unresolved_tie_break = True

        # Calculate Epistemic Confidence for the top candidate
        rated_dims_top = [d for d in active_dims if d in top_cand.scores and top_cand.evidence.get(d) != "UNKNOWN"] if top_cand else []
        c_eval = calculate_c_eval(active_dims, rated_dims_top)
        c_evid = calculate_c_evid(active_dims, weights, top_cand.evidence) if top_cand else 0.0
        c_epistemic = calculate_c_epistemic(c_req, c_eval, c_evid)
        confidence_tier = classify_confidence_tier(c_req, c_eval, c_evid, has_critical_gap)

        # Governance & Human Review Evaluation
        human_review_reasons: List[str] = []
        if hc_unknown_encountered:
            human_review_reasons.append("Hard constraint verification state is UNKNOWN")
        if margin_class == "Virtual Tie" and runner_up and runner_up.eligibility_status != "FAIL":
            human_review_reasons.append(f"Decision margin (+{delta}%) is within virtual tie boundary (<= 1.0%)")
        if unresolved_tie_break:
            human_review_reasons.append("Deterministic tie-break cascade could not separate top candidates")
        if confidence_tier == "LOW":
            human_review_reasons.append("Epistemic confidence is LOW due to critical information deficits or unverified evidence")
        if has_critical_gap:
            human_review_reasons.append("Critical dimension lacks verified evidence (tier < 0.50 or unrated)")

        human_review_required = len(human_review_reasons) > 0

        # Construct Ranking List for Output
        ranking_output = []
        for i, r in enumerate(ranked):
            item = {
                "rank": i + 1,
                "system": r.name,
                "systemId": r.candidate_id,
                "score": r.selection_score,
                "status": "Eligible" if r.eligibility_status != "FAIL" else f"Disqualified ({r.disqualification_reason})"
            }
            if r.disqualification_reason:
                item["disqualificationReason"] = r.disqualification_reason
            ranking_output.append(item)

        # Build Decision Tuple JSON Structure
        report_data = {
            "selectionReport": {
                "engineVersion": ENGINE_VERSION,
                "projectProfile": {
                    "projectName": project_name,
                    "context": context,
                    "declaredDimensionsCount": len(declared_dim_keys),
                    "activeDimensionsCount": len(active_dims)
                },
                "recommendation": {
                    "selectedSystem": top_cand.name if top_cand else "None",
                    "selectedSystemId": top_cand.candidate_id if top_cand else "none",
                    "selectionScore": top_score,
                    "rank": 1
                },
                "decisionMargin": {
                    "delta": delta,
                    "classification": margin_class,
                    "tieBreakTriggered": tie_break_triggered,
                    "tieBreakLog": tie_break_log
                },
                "epistemicConfidence": {
                    "score": c_epistemic,
                    "tier": confidence_tier,
                    "metrics": {
                        "requirementsCoverage": c_req,
                        "evaluationCoverage": c_eval,
                        "evidenceQuality": c_evid
                    }
                },
                "hardConstraints": {
                    "status": "All Passed" if not hc_unknown_encountered and len(disqualified) == 0 else (
                        "Disqualifications Present" if len(disqualified) > 0 else "Ambiguous"
                    ),
                    "evaluatedCount": len(hard_constraints),
                    "disqualifiedCount": len(disqualified)
                },
                "ranking": ranking_output,
                "governance": {
                    "humanReviewRequired": human_review_required,
                    "humanReviewReasons": human_review_reasons
                },
                "selectedConfiguration": top_cand.suggested_configuration if top_cand else {}
            }
        }

        # Compute Reproducibility Digest (SHA-256 of canonical inputs + engine version)
        canonical_profile = json.dumps(project_profile, sort_keys=True, separators=(',', ':'))
        canonical_catalog = json.dumps(self.catalog.raw_data, sort_keys=True, separators=(',', ':'))
        digest_input = f"{canonical_profile}|{canonical_catalog}|{ENGINE_VERSION}"
        reproducibility_digest = hashlib.sha256(digest_input.encode("utf-8")).hexdigest()
        report_data["selectionReport"]["reproducibilityDigest"] = reproducibility_digest

        # Exit code determination
        exit_code = 1 if human_review_required else 0

        return EvaluationOutput(
            report=report_data,
            human_review_required=human_review_required,
            human_review_reasons=human_review_reasons,
            winning_candidate=top_cand,
            exit_code=exit_code
        )
