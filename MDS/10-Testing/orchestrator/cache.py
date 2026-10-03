"""
Master Design System (MDS) — 5-Tuple Assertion De-Duplication Cache
Phase 9.7.10: Unified Local Orchestrator CLI & Master Validation Pipeline
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import hashlib
from typing import Dict, Tuple, Optional, List, Set, Any
from .models import ExecutionStatus, ExecutionContext, FindingSeverity, Finding


class AssertionIdentity:
    """
    5-Tuple Composite Identity:
    K_assertion = (assertion_id, subsystem_id, execution_context, input_fingerprint, validator_version)
    """

    def __init__(
        self,
        assertion_id: str,
        subsystem_id: str,
        execution_context: ExecutionContext,
        input_fingerprint: str,
        validator_version: str,
    ):
        self.assertion_id = assertion_id.strip()
        self.subsystem_id = subsystem_id.strip()
        self.execution_context = execution_context
        self.input_fingerprint = input_fingerprint.strip()
        self.validator_version = validator_version.strip()

    @property
    def key(self) -> Tuple[str, str, str, str, str]:
        return (
            self.assertion_id,
            self.subsystem_id,
            self.execution_context.value,
            self.input_fingerprint,
            self.validator_version,
        )

    def __hash__(self) -> int:
        return hash(self.key)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AssertionIdentity):
            return False
        return self.key == other.key

    def __repr__(self) -> str:
        return (
            f"AssertionIdentity({self.assertion_id}, {self.subsystem_id}, "
            f"{self.execution_context.value}, {self.input_fingerprint[:8]}, {self.validator_version})"
        )


class AssertionCacheRecord:
    def __init__(
        self,
        identity: AssertionIdentity,
        status: ExecutionStatus,
        findings: List[Finding],
    ):
        self.identity = identity
        self.status = status
        self.findings = findings


class AssertionExecutionCache:
    """
    In-memory assertion de-duplication registry for single pipeline execution runs.
    Enforces ADR-123 Conditions 1 through 5.
    """

    def __init__(self):
        self._entries: Dict[Tuple[str, str, str, str, str], AssertionCacheRecord] = {}

    def record_execution(
        self,
        assertion_id: str,
        subsystem_id: str,
        execution_context: ExecutionContext,
        input_fingerprint: str,
        validator_version: str,
        status: ExecutionStatus,
        findings: Optional[List[Finding]] = None,
    ) -> None:
        identity = AssertionIdentity(
            assertion_id=assertion_id,
            subsystem_id=subsystem_id,
            execution_context=execution_context,
            input_fingerprint=input_fingerprint,
            validator_version=validator_version,
        )
        self._entries[identity.key] = AssertionCacheRecord(
            identity=identity,
            status=status,
            findings=findings or [],
        )

    def is_cache_valid(
        self,
        assertion_id: str,
        subsystem_id: str,
        execution_context: ExecutionContext,
        input_fingerprint: str,
        validator_version: str,
    ) -> bool:
        """
        Evaluates whether a downstream assertion can be safely CACHED:
        1. Exact byte-level identity K(A1) == K(A2) exists.
        2. Upstream status == PASS.
        3. Input fingerprint is identical.
        4. Context is identical.
        5. Zero findings with CRITICAL or BLOCKER severity.
        """
        key = (
            assertion_id.strip(),
            subsystem_id.strip(),
            execution_context.value,
            input_fingerprint.strip(),
            validator_version.strip(),
        )

        record = self._entries.get(key)
        if record is None:
            return False

        # Condition 2: Upstream status must be PASS
        if record.status != ExecutionStatus.PASS:
            return False

        # Condition 5: No CRITICAL or BLOCKER findings
        for f in record.findings:
            if f.severity in (FindingSeverity.CRITICAL, FindingSeverity.BLOCKER):
                return False

        return True

    def clear(self) -> None:
        self._entries.clear()
