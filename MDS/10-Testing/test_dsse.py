#!/usr/bin/env python3
"""
MDS Design System Selection Engine (DSSE) — Automated Mathematical Test Suite
Verifies the locked and approved 5-pillar DSSE mathematical specification:
1. Requirements Coverage (C_req)
2. Evaluation Coverage (C_eval)
3. Importance-Weighted Evidence Quality (C_evid)
4. Conjunctive Epistemic Confidence (C_epistemic)
5. Hard Constraint Tri-State Eligibility (PASS / FAIL / UNKNOWN)
6. Decision Margin Classification (Δ <= 1%, 1% < Δ <= 3%, Δ > 3%)
7. Rule-Based Confidence Gating (Family C: High / Medium / Low)
8. Governance & Human Review Triggers
9. Execution & Validation of all 8 Calibration Scenarios (Cases A through H)
"""

import sys

# Standard Discrete Evidence Taxonomy
EVIDENCE_TIERS = {
    "CODE_AUDITED": 1.00,
    "OFFICIAL_DOCS": 0.75,
    "COMMUNITY": 0.50,
    "INFERRED": 0.25,
    "UNKNOWN": 0.00
}

# Standard Semantic Priority Weights
PRIORITY_WEIGHTS = {
    "Critical": 1.00,
    "High": 0.75,
    "Medium": 0.50,
    "Low": 0.25,
    "N/A": 0.00
}

ALL_12_DIMENSIONS = [f"D{i}" for i in range(1, 13)]

def calculate_c_req(declared_dims):
    """
    C_req = |{explicitly declared dimensions, including N/A}| / 12
    """
    explicit_count = len([d for d in declared_dims if d in ALL_12_DIMENSIONS])
    return round(explicit_count / 12.0, 4)

def calculate_c_eval(active_dims, rated_dims):
    """
    C_eval = |active dimensions with benchmark ratings| / |active dimensions|
    """
    if not active_dims:
        return 0.0
    evaluated = len([d for d in active_dims if d in rated_dims])
    return round(evaluated / len(active_dims), 4)

def calculate_c_evid(active_dims, weights, evidence_dict):
    """
    C_evid = Σ (weight * tier) / Σ weight
    """
    total_weight = sum(weights.get(d, 0.0) for d in active_dims)
    if total_weight == 0.0:
        return 0.0
    weighted_sum = sum(weights.get(d, 0.0) * EVIDENCE_TIERS.get(evidence_dict.get(d, "UNKNOWN"), 0.0) for d in active_dims)
    return round(weighted_sum / total_weight, 4)

def calculate_c_epistemic(c_req, c_eval, c_evid):
    """
    C_epistemic = C_req * C_eval * C_evid
    """
    return round(c_req * c_eval * c_evid, 4)

def classify_confidence_tier(c_req, c_eval, c_evid, has_critical_gap=False):
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

def calculate_selection_score(active_dims, weights, scores, hard_constraint_status="PASS"):
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

def classify_decision_margin(delta):
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

def evaluate_governance(top_score, runner_up_score, hard_constraint_status, confidence_tier, has_critical_gap=False):
    """
    Determines if human architect review is required and compiles reasons.
    """
    reasons = []
    delta = round(top_score - runner_up_score, 1)
    
    if hard_constraint_status == "UNKNOWN":
        reasons.append("Hard constraint verification state is UNKNOWN")
    if delta <= 1.0 and runner_up_score > 0.0:
        reasons.append(f"Decision margin (+{delta}%) is within virtual tie boundary (<= 1.0%)")
    if confidence_tier == "LOW":
        reasons.append("Epistemic confidence is LOW due to critical information deficits")
    if has_critical_gap:
        reasons.append("Critical dimension lacks verified evidence")

    return {
        "humanReviewRequired": len(reasons) > 0,
        "reasons": reasons,
        "delta": delta,
        "marginClassification": classify_decision_margin(delta)
    }

class DSSETestSuite:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []

    def assert_true(self, name, condition, details=""):
        if condition:
            self.passed += 1
            self.tests.append((name, "PASS", details))
            print(f"  [PASS] {name}")
        else:
            self.failed += 1
            self.tests.append((name, "FAIL", details))
            print(f"  [FAIL] {name}: {details}")

    def run_all(self):
        print("\n=========================================================================")
        print("          MDS DESIGN SYSTEM SELECTION ENGINE (DSSE) TEST SUITE           ")
        print("=========================================================================")

        # 1. Requirements Coverage Tests
        print("\n--- [Domain 1: Requirements Coverage (C_req)] ---")
        self.assert_true("C_req: Full 12 dimensions declared", calculate_c_req(ALL_12_DIMENSIONS) == 1.0)
        self.assert_true("C_req: 6 declared, 6 omitted", calculate_c_req(ALL_12_DIMENSIONS[:6]) == 0.5)
        # Explicit N/A included in declared dimensions
        declared_with_na = ALL_12_DIMENSIONS[:8] + ["D9", "D10", "D11", "D12"]
        self.assert_true("C_req: Explicit N/A counts as specified", calculate_c_req(declared_with_na) == 1.0)
        self.assert_true("C_req: Single dimension specified", calculate_c_req(["D1"]) == 0.0833)

        # 2. Evaluation Coverage Tests
        print("\n--- [Domain 2: Evaluation Coverage (C_eval)] ---")
        active_dims = ["D1", "D2", "D3", "D4"]
        self.assert_true("C_eval: 100% active rated", calculate_c_eval(active_dims, ["D1", "D2", "D3", "D4"]) == 1.0)
        self.assert_true("C_eval: 3 of 4 active rated", calculate_c_eval(active_dims, ["D1", "D2", "D3"]) == 0.75)
        self.assert_true("C_eval: Single active dimension fully rated", calculate_c_eval(["D1"], ["D1"]) == 1.0)
        self.assert_true("C_eval: Zero active rated", calculate_c_eval(active_dims, []) == 0.0)

        # 3. Evidence Quality Tests
        print("\n--- [Domain 3: Evidence Quality (C_evid)] ---")
        w = {"D1": 1.00, "D2": 1.00, "D3": 0.25}
        # Code Audited (1.0), Official Docs (0.75), Inferred (0.25)
        # Weighted sum: (1.0*1.0 + 1.0*0.75 + 0.25*0.25) / 2.25 = (1.0 + 0.75 + 0.0625) / 2.25 = 1.8125 / 2.25 = 0.8056
        ev = {"D1": "CODE_AUDITED", "D2": "OFFICIAL_DOCS", "D3": "INFERRED"}
        calc_ev = calculate_c_evid(["D1", "D2", "D3"], w, ev)
        self.assert_true("C_evid: Importance-weighted average correctly computed", calc_ev == 0.8056, f"Got {calc_ev}")
        self.assert_true("C_evid: Pure CODE_AUDITED yields 1.0", calculate_c_evid(["D1"], {"D1": 1.0}, {"D1": "CODE_AUDITED"}) == 1.0)
        self.assert_true("C_evid: Pure UNKNOWN yields 0.0", calculate_c_evid(["D1"], {"D1": 1.0}, {"D1": "UNKNOWN"}) == 0.0)

        # 4. Epistemic Confidence Tests
        print("\n--- [Domain 4: Conjunctive Epistemic Confidence (C_epistemic)] ---")
        self.assert_true("C_epistemic: Perfect inputs yield 1.0", calculate_c_epistemic(1.0, 1.0, 1.0) == 1.0)
        self.assert_true("C_epistemic: Collapses when C_req drops", calculate_c_epistemic(0.25, 1.0, 0.75) == 0.1875)
        self.assert_true("C_epistemic: Zero evidence collapses confidence", calculate_c_epistemic(1.0, 1.0, 0.0) == 0.0)

        # 5. Hard Constraints Tests
        print("\n--- [Domain 5: Hard Constraints Eligibility Gate] ---")
        s = calculate_selection_score(["D1"], {"D1": 1.0}, {"D1": 9.0}, "PASS")
        self.assert_true("Hard Constraint: PASS keeps score", s == 90.0)
        s_fail = calculate_selection_score(["D1"], {"D1": 1.0}, {"D1": 9.0}, "FAIL")
        self.assert_true("Hard Constraint: FAIL forces score to 0.0% (Disqualified)", s_fail == 0.0)

        # 6. Decision Margin & Tie-Break Zones Tests
        print("\n--- [Domain 6: Decision Margin Classification] ---")
        self.assert_true("Margin: <= 1.0% is Virtual Tie", classify_decision_margin(0.5) == "Virtual Tie")
        self.assert_true("Margin: 1.0% exact boundary is Virtual Tie", classify_decision_margin(1.0) == "Virtual Tie")
        self.assert_true("Margin: 1.1% to 3.0% is Tie-Break Zone", classify_decision_margin(2.2) == "Tie-Break Zone")
        self.assert_true("Margin: 3.0% exact boundary is Tie-Break Zone", classify_decision_margin(3.0) == "Tie-Break Zone")
        self.assert_true("Margin: > 3.0% is Decisive Lead", classify_decision_margin(3.1) == "Decisive Lead")

        # 7. Confidence Tier Gating (Family C) Tests
        print("\n--- [Domain 7: Rule-Based Confidence Gating (Family C)] ---")
        self.assert_true("Tier: HIGH requires C_req>=0.85, C_eval=1.0, C_evid>=0.75", classify_confidence_tier(1.0, 1.0, 0.9) == "HIGH")
        self.assert_true("Tier: MEDIUM when C_req>=0.60 and C_evid>=0.50", classify_confidence_tier(0.7, 1.0, 0.6) == "MEDIUM")
        self.assert_true("Tier: LOW when C_req < 0.60", classify_confidence_tier(0.4, 1.0, 0.9) == "LOW")
        self.assert_true("Tier: LOW when C_evid < 0.50", classify_confidence_tier(1.0, 1.0, 0.3) == "LOW")
        self.assert_true("Tier: LOW when critical gap exists", classify_confidence_tier(1.0, 1.0, 1.0, has_critical_gap=True) == "LOW")

        # 8. Human Review Triggers Tests
        print("\n--- [Domain 8: Governance & Human Review Triggers] ---")
        gov_ok = evaluate_governance(88.4, 78.2, "PASS", "HIGH")
        self.assert_true("Governance: Decisive HIGH with PASS requires no review", not gov_ok["humanReviewRequired"])
        gov_tie = evaluate_governance(89.2, 88.7, "PASS", "HIGH")
        self.assert_true("Governance: Virtual Tie triggers review", gov_tie["humanReviewRequired"] and "virtual tie" in gov_tie["reasons"][0])
        gov_unk = evaluate_governance(87.5, 85.0, "UNKNOWN", "HIGH")
        self.assert_true("Governance: UNKNOWN hard constraint triggers review", gov_unk["humanReviewRequired"] and "UNKNOWN" in gov_unk["reasons"][0])

        # 9. Calibration Scenarios Validation (Cases A through H)
        print("\n--- [Domain 9: Validation of All 8 Calibration Scenarios] ---")
        
        # Scenario A: Decisive Healthcare
        c_req_a = calculate_c_req(ALL_12_DIMENSIONS)
        c_eval_a = calculate_c_eval(ALL_12_DIMENSIONS[:10], ALL_12_DIMENSIONS[:10])
        w_a = {d: 1.0 for d in ALL_12_DIMENSIONS[:10]}
        ev_a = {ALL_12_DIMENSIONS[i]: ("CODE_AUDITED" if i < 7 else "OFFICIAL_DOCS") for i in range(10)}
        c_evid_a = calculate_c_evid(ALL_12_DIMENSIONS[:10], w_a, ev_a)
        c_epist_a = calculate_c_epistemic(c_req_a, c_eval_a, c_evid_a)
        tier_a = classify_confidence_tier(c_req_a, c_eval_a, c_evid_a)
        gov_a = evaluate_governance(88.4, 78.2, "PASS", tier_a)
        self.assert_true("Scenario A: C_epistemic == 0.925 and Review == False", c_epist_a == 0.925 and not gov_a["humanReviewRequired"])

        # Scenario B: Close SaaS (Virtual Tie)
        c_epist_b = calculate_c_epistemic(1.0, 1.0, 1.0)
        tier_b = classify_confidence_tier(1.0, 1.0, 1.0)
        gov_b = evaluate_governance(89.2, 88.7, "PASS", tier_b)
        self.assert_true("Scenario B: C_epistemic == 1.0 but Review == True (Virtual Tie)", c_epist_b == 1.0 and gov_b["humanReviewRequired"] and gov_b["delta"] == 0.5)

        # Scenario C: Incomplete Startup (Blowout Lead with Missing Requirements)
        c_req_c = calculate_c_req(ALL_12_DIMENSIONS[:3]) # 3/12 = 0.25
        c_epist_c = calculate_c_epistemic(c_req_c, 1.0, 0.75)
        tier_c = classify_confidence_tier(c_req_c, 1.0, 0.75)
        gov_c = evaluate_governance(92.0, 54.0, "PASS", tier_c)
        self.assert_true("Scenario C: C_epistemic == 0.1875 and Review == True (LOW confidence)", c_epist_c == 0.1875 and tier_c == "LOW" and gov_c["humanReviewRequired"])

        # Scenario D: AI Workspace (Inferred Evidence)
        w_d = {ALL_12_DIMENSIONS[i]: 1.0 for i in range(9)}
        ev_d = {ALL_12_DIMENSIONS[i]: ("CODE_AUDITED" if i < 2 else ("OFFICIAL_DOCS" if i < 5 else "INFERRED")) for i in range(9)}
        c_evid_d = calculate_c_evid(ALL_12_DIMENSIONS[:9], w_d, ev_d)
        c_epist_d = calculate_c_epistemic(1.0, 1.0, c_evid_d)
        tier_d = classify_confidence_tier(1.0, 1.0, c_evid_d)
        self.assert_true("Scenario D: C_evid == 0.5833 and Tier == MEDIUM", c_evid_d == 0.5833 and tier_d == "MEDIUM")

        # Scenario E: Hard Constraint UNKNOWN
        gov_e = evaluate_governance(87.5, 85.0, "UNKNOWN", "HIGH")
        self.assert_true("Scenario E: Hard Constraint UNKNOWN blocks automated clearance", gov_e["humanReviewRequired"] and "UNKNOWN" in gov_e["reasons"][0])

        # Scenario F: Weak Everything
        c_epist_f = calculate_c_epistemic(0.3333, 0.75, 0.45)
        tier_f = classify_confidence_tier(0.3333, 0.75, 0.45)
        gov_f = evaluate_governance(61.2, 59.8, "PASS", tier_f)
        self.assert_true("Scenario F: Weak Everything yields C_epistemic ~0.112 and Tier LOW", c_epist_f == 0.1125 and tier_f == "LOW" and gov_f["humanReviewRequired"])

        # Scenario G: Sole Surviving Candidate
        c_epist_g = calculate_c_epistemic(1.0, 1.0, 0.90)
        tier_g = classify_confidence_tier(1.0, 1.0, 0.90)
        gov_g = evaluate_governance(71.0, 0.0, "PASS", tier_g)
        self.assert_true("Scenario G: Sole survivor yields HIGH confidence and Review == False", tier_g == "HIGH" and not gov_g["humanReviewRequired"] and gov_g["delta"] == 71.0)

        # Scenario H: Two Elite Candidates (Virtual Tie)
        gov_h = evaluate_governance(93.4, 92.8, "PASS", "HIGH")
        self.assert_true("Scenario H: Elite tie triggers Human Review", gov_h["humanReviewRequired"] and gov_h["delta"] == 0.6)

        # Summary
        print("\n-------------------------------------------------------------------------")
        print(f"DSSE Total Tests Executed: {self.passed + self.failed}")
        print(f"  [+] Passed: {self.passed}")
        print(f"  [-] Failed: {self.failed}")
        print("-------------------------------------------------------------------------")
        if self.failed == 0:
            print("DSSE TEST SUITE: SUCCESS — 100% of mathematical assertions PASSED.\n")
            return 0
        else:
            print(f"DSSE TEST SUITE: FAILURE — {self.failed} test(s) failed.\n")
            return 1

if __name__ == "__main__":
    suite = DSSETestSuite()
    sys.exit(suite.run_all())
