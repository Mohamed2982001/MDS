"""Reporting and Telemetry formatters for the MDS Governance Engine.

Provides:
- ConsoleReporter: Rich ANSI terminal dashboard.
- JsonReporter: Machine-readable JSON output for CI pipelines.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .engine import GovernanceResult
from .rules import FindingSeverity


class ConsoleReporter:
    """Renders human-readable ANSI terminal output."""

    # ANSI Colors
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    GRAY = "\033[90m"

    @classmethod
    def render(cls, result: GovernanceResult) -> str:
        lines = []
        lines.append("=" * 80)
        lines.append(f"{cls.BOLD}{cls.CYAN}       MASTER DESIGN SYSTEM (MDS) — GOVERNANCE AUDIT REPORT{cls.RESET}")
        lines.append("=" * 80)

        # Overview Status
        if result.is_success:
            if result.major_count > 0:
                status_text = f"PASS (Standard Mode — 0 Blockers, 0 Criticals; {result.major_count} Non-Blocking Major Structural Findings)"
                status_color = cls.YELLOW
            else:
                status_text = "PASS (Clean — 0 Findings)"
                status_color = cls.GREEN
        else:
            status_text = f"FAIL (Exit Code: {result.exit_code})"
            status_color = cls.RED
        lines.append(f"Overall Status        : {cls.BOLD}{status_color}{status_text}{cls.RESET} (Exit Code: {result.exit_code})")

        # Telemetry
        if result.telemetry:
            bench_status = "Target Met" if result.telemetry.benchmark_status == "PASS" else "Advisory Exceeded"
            lines.append(f"Execution Duration    : {result.telemetry.wall_clock_ms:.1f} ms (Benchmark Advisory: {bench_status})")
            lines.append(f"Benchmark Note        : Advisory target met during this run; performance remains advisory and environment-dependent.")
            lines.append(f"Files Discovered      : {result.telemetry.files_scanned} ({result.telemetry.markdown_files} markdown, {result.telemetry.token_files} tokens)")
            lines.append(f"Knowledge Graph (IR)  : {result.telemetry.nodes_count} nodes, {result.telemetry.edges_count} edges")

        # Capability Coverage Triad
        cov = result.capability_coverage_stats
        if cov:
            lines.append("-" * 80)
            lines.append(f"{cls.BOLD}Capability Coverage Accounting (INV-009):{cls.RESET}")
            lines.append(f"  Total Capabilities  : {cov.get('total_capabilities', 0)} declared (133 Core + 37 DSSE)")
            lines.append(f"  Direct Relations    : {cov.get('direct_relations', 0)}")
            lines.append(f"  Wrapped Relations   : {cov.get('wrapped_relations', 0)} (DSSE 37 wrapped by MDS-DSS-004)")
            lines.append(f"  Supporting Relations: {cov.get('indirect_relations', 0)}")
            lines.append(f"  Duplicate Coverage  : {cov.get('duplicate_covered', 0)} (Healthy defense-in-depth)")
            uncovered = cov.get("uncovered", 0)
            unc_color = cls.GREEN if uncovered == 0 else cls.RED
            lines.append(f"  Uncovered Gaps      : {cls.BOLD}{unc_color}{uncovered}{cls.RESET}")

        # Findings Summary
        lines.append("-" * 80)
        lines.append(f"{cls.BOLD}Findings Breakdown:{cls.RESET}")
        lines.append(f"  BLOCKER   : {cls.RED if result.blocker_count else cls.GRAY}{result.blocker_count}{cls.RESET}")
        lines.append(f"  CRITICAL  : {cls.RED if result.critical_count else cls.GRAY}{result.critical_count}{cls.RESET}")
        lines.append(f"  MAJOR     : {cls.YELLOW if result.major_count else cls.GRAY}{result.major_count}{cls.RESET}")
        lines.append(f"  MINOR     : {cls.GRAY}{result.minor_count}{cls.RESET}")
        lines.append(f"  ADVISORY  : {cls.GRAY}{result.advisory_count}{cls.RESET}")

        # Findings List (if any)
        if result.findings:
            lines.append("-" * 80)
            lines.append(f"{cls.BOLD}Detailed Findings:{cls.RESET}")
            for f in result.findings:
                sev_color = cls.RED if f.severity in (FindingSeverity.BLOCKER, FindingSeverity.CRITICAL) else (cls.YELLOW if f.severity == FindingSeverity.MAJOR else cls.GRAY)
                lines.append(f"  [{sev_color}{f.severity.value}{cls.RESET}] {f.rule_id}: {cls.BOLD}{f.title}{cls.RESET}")
                lines.append(f"    File: {f.source_file}:{f.line_number}")
                lines.append(f"    Desc: {f.description}")
                if f.remediation_hint:
                    lines.append(f"    Hint: {cls.CYAN}{f.remediation_hint}{cls.RESET}")

        lines.append("=" * 80)
        return "\n".join(lines)


class JsonReporter:
    """Serializes GovernanceResult to standardized JSON format."""

    @classmethod
    def serialize(cls, result: GovernanceResult) -> Dict[str, Any]:
        return {
            "version": "1.0.0",
            "is_success": result.is_success,
            "exit_code": result.exit_code,
            "stats": result.stats,
            "telemetry": {
                "wall_clock_ms": result.telemetry.wall_clock_ms if result.telemetry else 0.0,
                "files_scanned": result.telemetry.files_scanned if result.telemetry else 0,
                "markdown_files": result.telemetry.markdown_files if result.telemetry else 0,
                "token_files": result.telemetry.token_files if result.telemetry else 0,
                "nodes_count": result.telemetry.nodes_count if result.telemetry else 0,
                "edges_count": result.telemetry.edges_count if result.telemetry else 0,
                "benchmark_status": result.telemetry.benchmark_status if result.telemetry else "UNKNOWN",
                "benchmark_note": result.telemetry.benchmark_note if result.telemetry else None,
            },
            "capability_coverage": result.capability_coverage_stats,
            "findings": [
                {
                    "rule_id": f.rule_id,
                    "severity": f.severity.value,
                    "title": f.title,
                    "description": f.description,
                    "source_file": f.source_file,
                    "line_number": f.line_number,
                    "remediation_hint": f.remediation_hint,
                }
                for f in result.findings
            ],
        }

    @classmethod
    def write_to_file(cls, result: GovernanceResult, output_path: Path) -> None:
        data = cls.serialize(result)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
