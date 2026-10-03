"""
Master Design System (MDS) — Workspace Phase Governance Contract
Phase 9.7.10: Unified Local Orchestrator CLI & Master Validation Pipeline
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from .models import Finding, FindingSeverity


PHASE_TRANSITION_GRAPH = {
    "Phase-9.7.8": "Phase-9.7.9",
    "Phase-9.7.9": "Phase-9.7.10",
    "Phase-9.7.10": "Phase-9.7.11",
    "Phase-9.7.11": "Phase-9.7.12",
    "Phase-9.7.12": "Phase-10.1",
    "Phase-10.1": "Phase-10.2",
}


class PhaseGovernanceError(RuntimeError):
    """Raised when active phase governance contract is violated."""
    pass


class PhaseGovernanceManager:
    """
    Enforces governance contract on MDS/13-Implementation/ACTIVE_PHASE.json:
    - Schema validation
    - Monotonic sequential progression graph: 9.7.9 -> 9.7.10 -> 9.7.11
    - Previous-phase prerequisite verification
    - Active prefix restriction (no arbitrary prefix injection)
    - Dynamic injection into HistoricalGuardEngine without modifying locked files
    """

    PHASE_ID_PATTERN = re.compile(r"^Phase-(9|10)\.[0-9]+(\.[0-9]+)?$")
    ALLOWED_STATUSES = {"IN_PROGRESS", "SEALED"}
    AUTHORIZED_ARCHITECT = "Lead Architect Mohamed Khalid"

    def __init__(self, workspace_root: Optional[Path] = None):
        if workspace_root is None:
            self.workspace_root = Path(__file__).resolve().parent.parent.parent.parent
        else:
            self.workspace_root = Path(workspace_root).resolve()

        self.active_phase_file = (
            self.workspace_root / "MDS" / "13-Implementation" / "ACTIVE_PHASE.json"
        )
        self.master_registry_file = (
            self.workspace_root
            / "MDS"
            / "10-Testing"
            / "baselines"
            / "historical"
            / "master_historical_registry.json"
        )

    def load_active_phase(self) -> Dict[str, Any]:
        """Loads and parses ACTIVE_PHASE.json, raising PhaseGovernanceError on I/O or JSON failure."""
        if not self.active_phase_file.exists():
            raise PhaseGovernanceError(
                f"Missing required active phase descriptor: {self.active_phase_file}"
            )

        try:
            with open(self.active_phase_file, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            return data
        except Exception as e:
            raise PhaseGovernanceError(f"Failed to read/parse ACTIVE_PHASE.json: {e}")

    def validate_schema(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validates ACTIVE_PHASE.json against the formal JSON schema."""
        required_fields = [
            "schema_version",
            "active_phase_id",
            "active_phase_name",
            "status",
            "active_prefixes",
            "previous_phase_id",
            "authorized_by",
            "authorization_timestamp",
        ]

        for field in required_fields:
            if field not in data:
                return False, f"Missing required field '{field}' in ACTIVE_PHASE.json"

        if data["schema_version"] != "1.0.0":
            return False, f"Unsupported schema_version: {data['schema_version']} (expected 1.0.0)"

        active_id = data["active_phase_id"]
        if not self.PHASE_ID_PATTERN.match(active_id):
            return False, f"Invalid active_phase_id format: '{active_id}'"

        if data["status"] not in self.ALLOWED_STATUSES:
            return False, f"Invalid status: '{data['status']}' (expected IN_PROGRESS or SEALED)"

        prefixes = data["active_prefixes"]
        if not isinstance(prefixes, list) or len(prefixes) != 1:
            return False, f"active_prefixes must be a list containing exactly 1 entry matching active_phase_id"

        if prefixes[0] != active_id:
            return (
                False,
                f"Unauthorized prefix injection: '{prefixes[0]}' does not match active_phase_id '{active_id}'",
            )

        prev_id = data["previous_phase_id"]
        if not self.PHASE_ID_PATTERN.match(prev_id):
            return False, f"Invalid previous_phase_id format: '{prev_id}'"

        if data["authorized_by"] != self.AUTHORIZED_ARCHITECT:
            return (
                False,
                f"Unauthorized phase authorizer: '{data['authorized_by']}' (expected '{self.AUTHORIZED_ARCHITECT}')",
            )

        return True, None

    def verify_sequential_progression(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Verifies that active_phase_id sequentially follows previous_phase_id
        and that previous_phase_id is recognized as locked/ratified.
        """
        active_id = data["active_phase_id"]
        prev_id = data["previous_phase_id"]

        # Validate that active_id is the direct successor of prev_id
        # Allowed transition graph:
        # Phase-9.7.9 -> Phase-9.7.10
        # Phase-9.7.10 -> Phase-9.7.11
        # Phase-9.7.8 -> Phase-9.7.9
        def parse_phase_tuple(pid: str) -> Tuple[int, ...]:
            num_str = pid.replace("Phase-", "")
            return tuple(int(x) for x in num_str.split("."))

        try:
            curr_t = parse_phase_tuple(active_id)
            prev_t = parse_phase_tuple(prev_id)
        except Exception:
            return False, f"Failed to parse phase numbers for '{active_id}' or '{prev_id}'"

        # Check for non-sequential forward jumps (e.g. 9.7.9 to 9.7.11 skipping 9.7.10)
        if curr_t <= prev_t:
            return False, f"Non-forward phase progression: '{active_id}' does not succeed '{prev_id}'"

        # Check known sequential pairings
        valid_transitions = {
            "Phase-9.7.8": "Phase-9.7.9",
            "Phase-9.7.9": "Phase-9.7.10",
            "Phase-9.7.10": "Phase-9.7.11",
            "Phase-9.7.11": "Phase-9.7.12",
            "Phase-9.7.12": "Phase-10.1",
            "Phase-10.1": "Phase-10.2",
        }

        expected_next = valid_transitions.get(prev_id)
        if expected_next and active_id != expected_next:
            return (
                False,
                f"Invalid phase jump: '{active_id}' cannot directly succeed '{prev_id}' (expected '{expected_next}')",
            )

        return True, None

    def audit_governance(self) -> Tuple[bool, List[Finding], Optional[Dict[str, Any]]]:
        """
        Performs full audit of active phase descriptor.
        Returns:
            valid: bool
            findings: List[Finding] (empty if valid, BLOCKER finding if violated)
            data: loaded dictionary if valid
        """
        findings: List[Finding] = []

        try:
            data = self.load_active_phase()
        except PhaseGovernanceError as pge:
            findings.append(
                Finding(
                    severity=FindingSeverity.BLOCKER,
                    target="MDS/13-Implementation/ACTIVE_PHASE.json",
                    code="ORCHESTRATOR_PHASE_GOVERNANCE_VIOLATION",
                    message=str(pge),
                )
            )
            return False, findings, None

        ok_schema, schema_err = self.validate_schema(data)
        if not ok_schema:
            findings.append(
                Finding(
                    severity=FindingSeverity.BLOCKER,
                    target="MDS/13-Implementation/ACTIVE_PHASE.json",
                    code="ORCHESTRATOR_PHASE_SCHEMA_VIOLATION",
                    message=schema_err or "ACTIVE_PHASE.json schema validation failed",
                )
            )
            return False, findings, None

        ok_prog, prog_err = self.verify_sequential_progression(data)
        if not ok_prog:
            findings.append(
                Finding(
                    severity=FindingSeverity.BLOCKER,
                    target="MDS/13-Implementation/ACTIVE_PHASE.json",
                    code="ORCHESTRATOR_PHASE_GOVERNANCE_VIOLATION",
                    message=prog_err or "Invalid phase progression",
                )
            )
            return False, findings, None

        return True, [], data

    def audit_config(self, data: Dict[str, Any]) -> Tuple[bool, List[Finding]]:
        """Audits an in-memory phase configuration against schema and sequential progression."""
        findings: List[Finding] = []
        ok_schema, schema_err = self.validate_schema(data)
        if not ok_schema:
            findings.append(
                Finding(
                    severity=FindingSeverity.BLOCKER,
                    target="ACTIVE_PHASE.json",
                    code="ORCHESTRATOR_PHASE_SCHEMA_VIOLATION",
                    message=schema_err or "ACTIVE_PHASE.json schema validation failed",
                )
            )
            return False, findings

        ok_prog, prog_err = self.verify_sequential_progression(data)
        if not ok_prog:
            findings.append(
                Finding(
                    severity=FindingSeverity.BLOCKER,
                    target="ACTIVE_PHASE.json",
                    code="ORCHESTRATOR_PHASE_GOVERNANCE_VIOLATION",
                    message=prog_err or "Invalid phase progression",
                )
            )
            return False, findings

        return True, []

    @classmethod
    def inject_active_prefixes_into_guard(
        cls, historical_guard_engine: Any, active_prefixes: List[str]
    ) -> None:
        """
        Injects the verified active phase prefixes into HistoricalGuardEngine
        dynamically at runtime without editing locked Phase 9.7.9 files on disk.
        """
        historical_guard_engine.ACTIVE_PHASE_PREFIXES = tuple(active_prefixes)
