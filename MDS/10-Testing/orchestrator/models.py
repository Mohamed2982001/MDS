"""
Master Design System (MDS) — Orchestrator Data Models & Enums
Phase 9.7.10: Unified Local Orchestrator CLI & Master Validation Pipeline
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Set, Tuple


class ExecutionStatus(str, enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    DEFERRED = "DEFERRED"
    SKIPPED = "SKIPPED"
    CACHED = "CACHED"


class FindingSeverity(str, enum.Enum):
    INFO = "INFO"
    WARN = "WARN"
    CRITICAL = "CRITICAL"
    BLOCKER = "BLOCKER"

    def __ge__(self, other: FindingSeverity) -> bool:
        order = {
            FindingSeverity.INFO: 0,
            FindingSeverity.WARN: 1,
            FindingSeverity.CRITICAL: 2,
            FindingSeverity.BLOCKER: 3,
        }
        return order[self] >= order[other]

    def __gt__(self, other: FindingSeverity) -> bool:
        order = {
            FindingSeverity.INFO: 0,
            FindingSeverity.WARN: 1,
            FindingSeverity.CRITICAL: 2,
            FindingSeverity.BLOCKER: 3,
        }
        return order[self] > order[other]

    def __lt__(self, other: FindingSeverity) -> bool:
        order = {
            FindingSeverity.INFO: 0,
            FindingSeverity.WARN: 1,
            FindingSeverity.CRITICAL: 2,
            FindingSeverity.BLOCKER: 3,
        }
        return order[self] < order[other]

    def __le__(self, other: FindingSeverity) -> bool:
        order = {
            FindingSeverity.INFO: 0,
            FindingSeverity.WARN: 1,
            FindingSeverity.CRITICAL: 2,
            FindingSeverity.BLOCKER: 3,
        }
        return order[self] <= order[other]


def to_finding_severity(val: Any) -> FindingSeverity:
    """Safely normalizes arbitrary subsystem severity representations to canonical FindingSeverity."""
    if isinstance(val, FindingSeverity):
        return val
    s = str(val).upper()
    if hasattr(val, "value"):
        s = str(val.value).upper()
    if "BLOCKER" in s:
        return FindingSeverity.BLOCKER
    if "CRITICAL" in s:
        return FindingSeverity.CRITICAL
    if "MAJOR" in s or "WARN" in s:
        return FindingSeverity.WARN
    if "MINOR" in s or "ADVISORY" in s or "INFO" in s:
        return FindingSeverity.INFO
    return FindingSeverity.INFO


class ExecutionContext(str, enum.Enum):
    STATIC_FILE_SYNTAX = "STATIC_FILE_SYNTAX"
    AST_GRAPH_ANALYSIS = "AST_GRAPH_ANALYSIS"
    RUNTIME_DOM_EVALUATION = "RUNTIME_DOM_EVALUATION"
    HEADLESS_CDP_VIEWPORT = "HEADLESS_CDP_VIEWPORT"


class ExecutionCategory(str, enum.Enum):
    MANDATORY_SAFETY_GATE = "MANDATORY_SAFETY_GATE"
    CORE_SPECIFICATION = "CORE_SPECIFICATION"
    CONTRACT_INVARIANT = "CONTRACT_INVARIANT"
    DYNAMIC_INFRASTRUCTURE = "DYNAMIC_INFRASTRUCTURE"
    DYNAMIC_LIVE = "DYNAMIC_LIVE"


@dataclass
class Finding:
    severity: FindingSeverity
    target: str
    code: str
    message: str
    line: Optional[int] = None
    col: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "severity": self.severity.value,
            "target": self.target,
            "code": self.code,
            "message": self.message,
            "line": self.line,
            "col": self.col,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Finding:
        return cls(
            severity=FindingSeverity(data["severity"]),
            target=data.get("target", ""),
            code=data.get("code", "UNKNOWN"),
            message=data.get("message", ""),
            line=data.get("line"),
            col=data.get("col"),
        )


@dataclass
class SubsystemDefinition:
    subsystem_id: str
    subsystem_name: str
    owning_phase: str
    stage: int
    dependencies: List[str]
    entrypoint: str
    assertion_namespace: str
    result_contract: str
    supported_profiles: List[str]
    execution_category: ExecutionCategory


@dataclass
class SubsystemResult:
    subsystem_id: str
    subsystem_name: str
    status: ExecutionStatus
    duration_ms: float = 0.0
    findings: List[Finding] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    assertions_run: int = 0
    assertions_cached: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "subsystem_id": self.subsystem_id,
            "subsystem_name": self.subsystem_name,
            "status": self.status.value,
            "duration_ms": round(self.duration_ms, 2),
            "findings": [f.to_dict() for f in self.findings],
            "metrics": self.metrics,
            "assertions_run": self.assertions_run,
            "assertions_cached": self.assertions_cached,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SubsystemResult:
        return cls(
            subsystem_id=data["subsystem_id"],
            subsystem_name=data.get("subsystem_name", data["subsystem_id"]),
            status=ExecutionStatus(data["status"]),
            duration_ms=data.get("duration_ms", 0.0),
            findings=[Finding.from_dict(f) for f in data.get("findings", [])],
            metrics=data.get("metrics", {}),
            assertions_run=data.get("assertions_run", 0),
            assertions_cached=data.get("assertions_cached", 0),
        )


@dataclass
class PipelineResult:
    overall_status: ExecutionStatus
    exit_code: int
    duration_ms: float
    profile: str
    subsystem_results: List[SubsystemResult] = field(default_factory=list)
    pre_snapshot: Dict[str, Tuple[int, str]] = field(default_factory=dict)
    post_snapshot: Dict[str, Tuple[int, str]] = field(default_factory=dict)
    protected_core_clean: bool = True
    active_phase: str = "Phase-9.7.10"
    all_findings: List[Finding] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_status": self.overall_status.value,
            "exit_code": self.exit_code,
            "duration_ms": round(self.duration_ms, 2),
            "profile": self.profile,
            "active_phase": self.active_phase,
            "protected_core_clean": self.protected_core_clean,
            "subsystem_results": [r.to_dict() for r in self.subsystem_results],
            "findings": [f.to_dict() for f in self.all_findings],
        }
