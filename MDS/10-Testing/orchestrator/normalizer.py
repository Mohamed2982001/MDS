"""
Master Design System (MDS) — Status/Severity Normalizer & Exit Code Resolution
Phase 9.7.10: Unified Local Orchestrator CLI & Master Validation Pipeline
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

from typing import List, Set, Dict, Tuple, Any
from .models import ExecutionStatus, FindingSeverity, Finding, SubsystemResult


# Complete 20-Combination Normalization Matrix ($5 \times 4 = 20$)
COMBINATION_TABLE: Dict[Tuple[ExecutionStatus, FindingSeverity], Dict[str, Any]] = {
    # 1-4: PASS
    (ExecutionStatus.PASS, FindingSeverity.INFO): {
        "classification": "VALID",
        "standard_exit": 0,
        "strict_exit": 0,
        "strict_env_exit": 0,
        "semantics": "Clean pass with neutral informational telemetry.",
    },
    (ExecutionStatus.PASS, FindingSeverity.WARN): {
        "classification": "VALID",
        "standard_exit": 0,
        "strict_exit": 1,
        "strict_env_exit": 0,
        "semantics": "Nominal pass with advisory warning. Promotes to Exit 1 under --strict.",
    },
    (ExecutionStatus.PASS, FindingSeverity.CRITICAL): {
        "classification": "VALID",
        "standard_exit": 1,
        "strict_exit": 1,
        "strict_env_exit": 1,
        "semantics": "Orthogonal diagnostic failure (test logic passed, but critical anomaly recorded).",
    },
    (ExecutionStatus.PASS, FindingSeverity.BLOCKER): {
        "classification": "VALID",
        "standard_exit": 2,
        "strict_exit": 2,
        "strict_env_exit": 2,
        "semantics": "Fatal system error detected during clean test run (e.g. Trust Anchor corruption).",
    },

    # 5-8: FAIL
    (ExecutionStatus.FAIL, FindingSeverity.INFO): {
        "classification": "VALID",
        "standard_exit": 1,
        "strict_exit": 1,
        "strict_env_exit": 1,
        "semantics": "Assertion logic failed without explicit finding; implicit severity promoted to CRITICAL.",
    },
    (ExecutionStatus.FAIL, FindingSeverity.WARN): {
        "classification": "VALID",
        "standard_exit": 1,
        "strict_exit": 1,
        "strict_env_exit": 1,
        "semantics": "Assertion logic failed while logging advisory warning; test failure dictates Exit 1.",
    },
    (ExecutionStatus.FAIL, FindingSeverity.CRITICAL): {
        "classification": "VALID",
        "standard_exit": 1,
        "strict_exit": 1,
        "strict_env_exit": 1,
        "semantics": "Standard contract failure with critical finding.",
    },
    (ExecutionStatus.FAIL, FindingSeverity.BLOCKER): {
        "classification": "VALID",
        "standard_exit": 2,
        "strict_exit": 2,
        "strict_env_exit": 2,
        "semantics": "Fatal infrastructure failure causing test failure.",
    },

    # 9-12: DEFERRED
    (ExecutionStatus.DEFERRED, FindingSeverity.INFO): {
        "classification": "VALID",
        "standard_exit": 0,
        "strict_exit": 0,
        "strict_env_exit": 1,
        "semantics": "Chrome unavailable. Exit 0 on developer laptop; Exit 1 on strict browser CI runner.",
    },
    (ExecutionStatus.DEFERRED, FindingSeverity.WARN): {
        "classification": "VALID",
        "standard_exit": 0,
        "strict_exit": 1,
        "strict_env_exit": 1,
        "semantics": "Deferred test logged an advisory warning during discovery.",
    },
    (ExecutionStatus.DEFERRED, FindingSeverity.CRITICAL): {
        "classification": "VALID",
        "standard_exit": 1,
        "strict_exit": 1,
        "strict_env_exit": 1,
        "semantics": "Discovery/deferral inspection flagged critical configuration flaw before deferring.",
    },
    (ExecutionStatus.DEFERRED, FindingSeverity.BLOCKER): {
        "classification": "VALID",
        "standard_exit": 2,
        "strict_exit": 2,
        "strict_env_exit": 2,
        "semantics": "Subsystem discovery suffered fatal crash before deferral.",
    },

    # 13-16: SKIPPED
    (ExecutionStatus.SKIPPED, FindingSeverity.INFO): {
        "classification": "VALID",
        "standard_exit": 0,
        "strict_exit": 0,
        "strict_env_exit": 0,
        "semantics": "Stage intentionally excluded by profile scope (e.g. Stage 4 in --fast).",
    },
    (ExecutionStatus.SKIPPED, FindingSeverity.WARN): {
        "classification": "VALID",
        "standard_exit": 0,
        "strict_exit": 1,
        "strict_env_exit": 0,
        "semantics": "Skipped stage with pre-eval advisory.",
    },
    (ExecutionStatus.SKIPPED, FindingSeverity.CRITICAL): {
        "classification": "VALID",
        "standard_exit": 1,
        "strict_exit": 1,
        "strict_env_exit": 1,
        "semantics": "Pre-evaluation inspection flagged critical misconfiguration on skipped stage.",
    },
    (ExecutionStatus.SKIPPED, FindingSeverity.BLOCKER): {
        "classification": "VALID",
        "standard_exit": 2,
        "strict_exit": 2,
        "strict_env_exit": 2,
        "semantics": "Pre-evaluation inspection detected fatal corruption.",
    },

    # 17-20: CACHED
    (ExecutionStatus.CACHED, FindingSeverity.INFO): {
        "classification": "VALID",
        "standard_exit": 0,
        "strict_exit": 0,
        "strict_env_exit": 0,
        "semantics": "Re-certified pass via 5-tuple cache hit.",
    },
    (ExecutionStatus.CACHED, FindingSeverity.WARN): {
        "classification": "VALID",
        "standard_exit": 0,
        "strict_exit": 1,
        "strict_env_exit": 0,
        "semantics": "Cached pass carrying upstream advisory.",
    },
    (ExecutionStatus.CACHED, FindingSeverity.CRITICAL): {
        "classification": "INVALID",
        "standard_exit": 2,
        "strict_exit": 2,
        "strict_env_exit": 2,
        "semantics": "Architectural Invariant Violation: ADR-123 Condition 5 strictly forbids caching when target has CRITICAL findings.",
    },
    (ExecutionStatus.CACHED, FindingSeverity.BLOCKER): {
        "classification": "INVALID",
        "standard_exit": 2,
        "strict_exit": 2,
        "strict_env_exit": 2,
        "semantics": "Architectural Invariant Violation: ADR-123 Condition 5 strictly forbids caching when target has BLOCKER findings.",
    },
}

NORMALIZATION_MATRIX_20 = [
    (
        i + 1,
        k[0],
        k[1],
        v["standard_exit"],
        v["strict_exit"],
        v["strict_env_exit"],
        v["semantics"],
    )
    for i, (k, v) in enumerate(COMBINATION_TABLE.items())
]


def resolve_final_exit_code(
    results: List[SubsystemResult],
    strict: bool = False,
    strict_env: bool = False,
) -> int:
    """
    Canonical 6-step resolution algorithm:
    ResultSet -> Step 0 Invariant Check -> Step 1 Aggregate -> Step 2 Policy -> Final Exit Code
    """
    # Step 0: Invariant Validation (Illegal CACHED States)
    # ADR-123 Condition 5 strictly forbids CACHED when CRITICAL or BLOCKER findings exist on the target
    for r in results:
        if r.status == ExecutionStatus.CACHED:
            for f in r.findings:
                if f.severity in (FindingSeverity.CRITICAL, FindingSeverity.BLOCKER):
                    # Architectural invariant violated: illegal cached state -> BLOCKER / Exit 2
                    return 2

    all_findings: List[Finding] = [f for r in results for f in r.findings]
    all_statuses: Set[ExecutionStatus] = {r.status for r in results}

    # Step 1: Base Severity from explicit diagnostic findings
    max_severity = FindingSeverity.INFO
    if all_findings:
        max_severity = max(f.severity for f in all_findings)

    # Step 2: Status promotion (ExecutionStatus.FAIL implies at least CRITICAL)
    if ExecutionStatus.FAIL in all_statuses:
        if max_severity in (FindingSeverity.INFO, FindingSeverity.WARN):
            max_severity = FindingSeverity.CRITICAL

    # Step 3: Fatal Blocker evaluation
    if max_severity == FindingSeverity.BLOCKER:
        return 2

    # Step 4: Critical Failure evaluation
    if max_severity == FindingSeverity.CRITICAL:
        return 1

    # Step 5: Warning / Advisory evaluation
    if max_severity == FindingSeverity.WARN:
        if strict:
            return 1
        if ExecutionStatus.DEFERRED in all_statuses and strict_env:
            return 1
        return 0

    # Step 6: Clean passes, cached, skipped, or deferred
    if ExecutionStatus.DEFERRED in all_statuses and strict_env:
        return 1

    return 0


def lookup_matrix_combination(
    status: ExecutionStatus,
    severity: FindingSeverity,
    strict: bool = False,
    strict_env: bool = False,
) -> Tuple[str, int]:
    """
    Looks up the classification and expected exit code from the 20-combination matrix.
    Returns:
        (classification, expected_exit_code)
    """
    entry = COMBINATION_TABLE.get((status, severity))
    if not entry:
        raise ValueError(f"Unknown combination: {status}, {severity}")

    classification = entry["classification"]

    if strict and strict_env:
        exit_code = entry["strict_exit"] if entry["strict_exit"] != 0 else entry["strict_env_exit"]
    elif strict:
        exit_code = entry["strict_exit"]
    elif strict_env:
        exit_code = entry["strict_env_exit"]
    else:
        exit_code = entry["standard_exit"]

    return classification, exit_code
