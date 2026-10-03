#!/usr/bin/env python3
"""
DSSE Contract & Schema Validator
Pure Python 3.12 implementation validating Project Profiles, Candidate Catalogs,
and Decision Tuples against formal specifications without external dependencies.
"""

from typing import Any, Dict, List, Tuple

CANONICAL_DIMENSIONS = {
    "D1": "Platform Fit",
    "D2": "Design Language & Aesthetics",
    "D3": "Accessibility & Compliance",
    "D4": "Localization & RTL",
    "D5": "Information Density & Data Ergonomics",
    "D6": "Component Ecosystem Breadth",
    "D7": "Architectural Extensibility",
    "D8": "Responsive Recomposition",
    "D9": "Enterprise Needs",
    "D10": "AI-Native Needs",
    "D11": "Customization Needs",
    "D12": "Developer Ecosystem"
}

ALLOWED_PRIORITIES = {"Critical", "High", "Medium", "Low", "N/A"}
ALLOWED_EVIDENCE_TIERS = {"CODE_AUDITED", "OFFICIAL_DOCS", "COMMUNITY", "INFERRED", "UNKNOWN"}
ALLOWED_HARD_CONSTRAINT_STATES = {"PASS", "FAIL", "UNKNOWN"}
ALLOWED_CONFIDENCE_TIERS = {"HIGH", "MEDIUM", "LOW", "High", "Medium", "Low"}
ALLOWED_MARGIN_CLASSIFICATIONS = {"Virtual Tie", "Tie-Break Zone", "Decisive Lead"}


class DSSEValidationError(Exception):
    """Raised when validation fails against DSSE contract rules."""
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__("; ".join(errors))


def validate_project_profile(data: Any) -> Tuple[bool, List[str]]:
    """
    Validates a ProjectProfile dictionary.
    Returns (is_valid, list_of_errors).
    """
    errors: List[str] = []
    if not isinstance(data, dict):
        return False, ["Root of project profile must be a JSON object"]

    if "projectName" not in data or not isinstance(data["projectName"], str) or not data["projectName"].strip():
        errors.append("Field 'projectName' is required and must be a non-empty string")

    if "dimensions" not in data or not isinstance(data["dimensions"], dict):
        errors.append("Field 'dimensions' is required and must be an object")
    else:
        dims = data["dimensions"]
        for d_id, priority in dims.items():
            if d_id not in CANONICAL_DIMENSIONS:
                errors.append(f"Invalid dimension identifier '{d_id}'. Must be one of {list(CANONICAL_DIMENSIONS.keys())}")
            if priority not in ALLOWED_PRIORITIES:
                errors.append(f"Invalid priority '{priority}' for {d_id}. Must be one of {sorted(ALLOWED_PRIORITIES)}")

    if "hardConstraints" in data:
        hc = data["hardConstraints"]
        if not isinstance(hc, list):
            errors.append("Field 'hardConstraints' must be a list of constraint objects")
        else:
            for i, constraint in enumerate(hc):
                if not isinstance(constraint, dict):
                    errors.append(f"hardConstraints[{i}] must be an object")
                    continue
                if "id" not in constraint or not isinstance(constraint["id"], str):
                    errors.append(f"hardConstraints[{i}] missing required string field 'id'")
                if "description" not in constraint or not isinstance(constraint["description"], str):
                    errors.append(f"hardConstraints[{i}] missing required string field 'description'")

    return len(errors) == 0, errors


def validate_candidate_catalog(data: Any) -> Tuple[bool, List[str]]:
    """
    Validates a CandidateCatalog dictionary.
    Returns (is_valid, list_of_errors).
    """
    errors: List[str] = []
    if not isinstance(data, dict):
        return False, ["Root of candidate catalog must be a JSON object"]

    for req_field in ["schemaVersion", "catalogName", "candidates"]:
        if req_field not in data:
            errors.append(f"Catalog missing required field '{req_field}'")

    if "candidates" in data:
        if not isinstance(data["candidates"], list) or len(data["candidates"]) == 0:
            errors.append("Field 'candidates' must be a non-empty list of candidate objects")
        else:
            for idx, cand in enumerate(data["candidates"]):
                c_prefix = f"candidates[{idx}]"
                if not isinstance(cand, dict):
                    errors.append(f"{c_prefix} must be an object")
                    continue

                for f in ["id", "name", "dimensions"]:
                    if f not in cand:
                        errors.append(f"{c_prefix} missing required field '{f}'")

                if "dimensions" in cand and isinstance(cand["dimensions"], dict):
                    dims = cand["dimensions"]
                    for d_id, rating in dims.items():
                        if d_id not in CANONICAL_DIMENSIONS:
                            errors.append(f"{c_prefix}.dimensions has invalid identifier '{d_id}'")
                        if not isinstance(rating, dict):
                            errors.append(f"{c_prefix}.dimensions['{d_id}'] must be a rating object")
                            continue
                        if "score" not in rating or not isinstance(rating["score"], (int, float)):
                            errors.append(f"{c_prefix}.dimensions['{d_id}'] missing numeric 'score'")
                        else:
                            s = float(rating["score"])
                            if s < 0.0 or s > 10.0:
                                errors.append(f"{c_prefix}.dimensions['{d_id}'].score ({s}) must be between 0.0 and 10.0")

                        if "evidenceTier" not in rating or rating["evidenceTier"] not in ALLOWED_EVIDENCE_TIERS:
                            errors.append(f"{c_prefix}.dimensions['{d_id}'] invalid 'evidenceTier'. Must be one of {sorted(ALLOWED_EVIDENCE_TIERS)}")

                if "hardConstraints" in cand and isinstance(cand["hardConstraints"], dict):
                    for hc_id, val in cand["hardConstraints"].items():
                        if val not in ALLOWED_HARD_CONSTRAINT_STATES:
                            errors.append(f"{c_prefix}.hardConstraints['{hc_id}'] value '{val}' must be one of {sorted(ALLOWED_HARD_CONSTRAINT_STATES)}")

    return len(errors) == 0, errors


def validate_decision_tuple(data: Any) -> Tuple[bool, List[str]]:
    """
    Validates a generated DecisionTuple report against the canonical schema.
    Returns (is_valid, list_of_errors).
    """
    errors: List[str] = []
    if not isinstance(data, dict):
        return False, ["Root of decision report must be a JSON object"]

    if "selectionReport" not in data or not isinstance(data["selectionReport"], dict):
        return False, ["Root must contain 'selectionReport' object"]

    report = data["selectionReport"]
    required_sections = [
        "projectProfile",
        "recommendation",
        "decisionMargin",
        "epistemicConfidence",
        "hardConstraints",
        "ranking",
        "governance"
      ]
    for section in required_sections:
        if section not in report or not isinstance(report[section], (dict, list)):
            errors.append(f"selectionReport missing required section '{section}'")

    # Validate recommendation
    if "recommendation" in report and isinstance(report["recommendation"], dict):
        rec = report["recommendation"]
        for f in ["selectedSystem", "selectionScore", "rank"]:
            if f not in rec:
                errors.append(f"recommendation missing required field '{f}'")

    # Validate margin
    if "decisionMargin" in report and isinstance(report["decisionMargin"], dict):
        dm = report["decisionMargin"]
        if "delta" not in dm or not isinstance(dm["delta"], (int, float)):
            errors.append("decisionMargin missing numeric 'delta'")
        if "classification" not in dm or dm["classification"] not in ALLOWED_MARGIN_CLASSIFICATIONS:
            errors.append(f"decisionMargin classification invalid. Must be one of {sorted(ALLOWED_MARGIN_CLASSIFICATIONS)}")

    # Validate epistemic confidence
    if "epistemicConfidence" in report and isinstance(report["epistemicConfidence"], dict):
        ec = report["epistemicConfidence"]
        if "score" not in ec or not isinstance(ec["score"], (int, float)):
            errors.append("epistemicConfidence missing numeric 'score'")
        if "tier" not in ec or ec["tier"] not in ALLOWED_CONFIDENCE_TIERS:
            errors.append(f"epistemicConfidence tier invalid. Must be one of {sorted(ALLOWED_CONFIDENCE_TIERS)}")

    # Validate governance
    if "governance" in report and isinstance(report["governance"], dict):
        gov = report["governance"]
        if "humanReviewRequired" not in gov or not isinstance(gov["humanReviewRequired"], bool):
            errors.append("governance missing boolean 'humanReviewRequired'")
        if "humanReviewReasons" not in gov or not isinstance(gov["humanReviewReasons"], list):
            errors.append("governance missing list 'humanReviewReasons'")

    return len(errors) == 0, errors
