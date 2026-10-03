"""
Master Design System (MDS) — Console & JSON Telemetry Reporters
Phase 9.7.10: Unified Local Orchestrator CLI & Master Validation Pipeline
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from .models import PipelineResult, SubsystemResult, Finding, FindingSeverity, ExecutionStatus


class ConsoleReporter:
    """Renders executive terminal dashboard with ANSI colors."""

    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    def render(self, result: PipelineResult) -> None:
        term_width = 80
        divider = "=" * term_width
        sub_divider = "-" * term_width

        print("\n" + divider)
        print(f"{self.BOLD}      MASTER DESIGN SYSTEM (MDS) -- UNIFIED LOCAL ORCHESTRATOR{self.RESET}")
        print(divider)
        print(f"Overall Status        : {self._format_status(result.overall_status)} (Exit Code: {result.exit_code})")
        print(f"Execution Profile     : {result.profile.upper()}")
        print(f"Active Phase          : {result.active_phase} (Governed)")
        print(f"Total Pipeline Time   : {result.duration_ms:.1f} ms")
        print(f"Protected Core State  : {self._format_core(result.protected_core_clean)}")
        print(sub_divider)

        # Stage / Subsystem breakdown
        print(f"{self.BOLD}Subsystem Execution Matrix:{self.RESET}")
        for r in result.subsystem_results:
            status_tag = self._format_status_badge(r.status)
            time_tag = f"{r.duration_ms:6.1f} ms"
            findings_str = f"({len(r.findings)} findings)" if r.findings else "(0 findings)"
            cached_str = f" [cached: {r.assertions_cached}]" if r.assertions_cached else ""
            print(f"  {status_tag} {r.subsystem_id:<7} : {r.subsystem_name:<36} {time_tag} {findings_str}{cached_str}")

        print(sub_divider)

        # Findings Summary
        all_findings = result.all_findings
        if all_findings:
            print(f"{self.BOLD}Diagnostic Findings ({len(all_findings)}):{self.RESET}")
            for f in all_findings:
                sev_tag = self._format_severity(f.severity)
                loc_str = f" (line {f.line})" if f.line else ""
                print(f"  - {sev_tag} [{f.code}] on '{f.target}'{loc_str}: {f.message}")
            print(sub_divider)
        else:
            print(f"{self.GREEN}Zero diagnostic findings recorded across all executed subsystems.{self.RESET}")
            print(sub_divider)

        # Final Verdict Box
        if result.exit_code == 0:
            print(f"{self.GREEN}{self.BOLD}> PIPELINE VERDICT: SUCCESS (Exit 0) -- Repository Ready{self.RESET}")
        elif result.exit_code == 1:
            print(f"{self.RED}{self.BOLD}> PIPELINE VERDICT: FAILURE (Exit 1) -- Validation or Policy Violations Detected{self.RESET}")
        else:
            print(f"{self.MAGENTA}{self.BOLD}> PIPELINE VERDICT: BLOCKER (Exit 2) -- Fatal System or Governance Invariant Violation{self.RESET}")
        print(divider + "\n")

    def _format_status(self, status: ExecutionStatus) -> str:
        if status == ExecutionStatus.PASS:
            return f"{self.GREEN}{self.BOLD}PASS (All Invariants Satisfied){self.RESET}"
        if status == ExecutionStatus.DEFERRED:
            return f"{self.YELLOW}{self.BOLD}DEFERRED (Environmental Prerequisites Missing){self.RESET}"
        if status == ExecutionStatus.CACHED:
            return f"{self.CYAN}{self.BOLD}CACHED (Re-certified via Composite Cache){self.RESET}"
        if status == ExecutionStatus.SKIPPED:
            return f"{self.DIM}SKIPPED (Excluded by Profile){self.RESET}"
        return f"{self.RED}{self.BOLD}FAIL (Invariants Violated){self.RESET}"

    def _format_status_badge(self, status: ExecutionStatus) -> str:
        if status == ExecutionStatus.PASS:
            return f"{self.GREEN}[PASS]{self.RESET}"
        if status == ExecutionStatus.DEFERRED:
            return f"{self.YELLOW}[DEFR]{self.RESET}"
        if status == ExecutionStatus.CACHED:
            return f"{self.CYAN}[CACH]{self.RESET}"
        if status == ExecutionStatus.SKIPPED:
            return f"{self.DIM}[SKIP]{self.RESET}"
        return f"{self.RED}[FAIL]{self.RESET}"

    def _format_severity(self, severity: FindingSeverity) -> str:
        if severity == FindingSeverity.BLOCKER:
            return f"{self.MAGENTA}{self.BOLD}[BLOCKER]{self.RESET}"
        if severity == FindingSeverity.CRITICAL:
            return f"{self.RED}{self.BOLD}[CRITICAL]{self.RESET}"
        if severity == FindingSeverity.WARN:
            return f"{self.YELLOW}[WARN]{self.RESET}"
        return f"{self.DIM}[INFO]{self.RESET}"

    def _format_core(self, clean: bool) -> str:
        if clean:
            return f"{self.GREEN}CLEAN (0 mutations detected across 4 protected directories){self.RESET}"
        return f"{self.RED}{self.BOLD}CORRUPTED (Unauthorized mutation detected){self.RESET}"


class JsonReporter:
    """Exports standardized Layer-M JSON telemetry artifact."""

    def __init__(self, workspace_root: Optional[Path] = None):
        if workspace_root is None:
            self.workspace_root = Path(__file__).resolve().parent.parent.parent.parent
        else:
            self.workspace_root = Path(workspace_root).resolve()

        self.output_dir = self.workspace_root / "MDS" / "10-Testing" / "artifacts"
        self.output_file = self.output_dir / "run_all_telemetry.json"

    def build_telemetry(self, result: PipelineResult) -> Dict[str, Any]:
        return {
            "schema_version": "1.0.0",
            "orchestrator_version": "1.0.0",
            "phase": "9.7.10",
            "overall_status": result.overall_status.value,
            "exit_code": result.exit_code,
            "duration_ms": round(result.duration_ms, 2),
            "profile": result.profile,
            "active_phase": result.active_phase,
            "performance_contracts": {
                "global_layer_m": {
                    "contract": "ADR-100",
                    "warm_ms": 500.0,
                    "cold_ms": 1200.0,
                    "status": "Target Met" if result.duration_ms <= 1200.0 else "Exceeded",
                },
                "local_historical_guard": {
                    "contract": "ADR-113",
                    "warm_ms": 100.0,
                    "cold_ms": 300.0,
                },
            },
            "protected_core": {
                "clean": result.protected_core_clean,
                "pre_snapshot_files": len(result.pre_snapshot),
                "post_snapshot_files": len(result.post_snapshot),
            },
            "subsystems": [r.to_dict() for r in result.subsystem_results],
            "findings": [f.to_dict() for f in result.all_findings],
        }

    def export(self, result: PipelineResult) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        telemetry = self.build_telemetry(result)

        with open(self.output_file, "w", encoding="utf-8") as fp:
            json.dump(telemetry, fp, indent=2)

        return self.output_file
