#!/usr/bin/env python3
"""
MDS Responsive Evidence Generator & Report Formatter
Phase 9.7.6: Responsive Viewport Automation (Layer K)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Generates structured JSON evidence artifacts and human-readable terminal reports
for Phase 9.7.6 Responsive Automation runs.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from .responsive_models import ResponsiveMatrixResult, AssertionClass
except ImportError:
    from responsive_models import ResponsiveMatrixResult, AssertionClass


class ResponsiveEvidenceGenerator:
    """Generates structured evidence and human-readable reports."""

    @classmethod
    def generate_evidence_dict(cls, result: ResponsiveMatrixResult) -> Dict[str, Any]:
        """Produces canonical structured evidence dictionary."""
        return {
            "schema_version": "1.0.0",
            "capability_id": result.capability_id,
            "status": result.status,
            "browser_version": result.browser_version,
            "duration_ms": round(result.duration_ms, 2),
            "accounting": {
                "total_runs": len(result.runs),
                "total_assertions": result.total_assertions,
                "passed_assertions": result.passed_assertions,
                "failed_assertions": result.failed_assertions,
                "hard_failures": result.hard_failures,
            },
            "runs": [r.to_dict() for r in result.runs],
            "error_message": result.error_message,
        }

    @classmethod
    def to_dict(cls, result: ResponsiveMatrixResult) -> Dict[str, Any]:
        """Alias for generate_evidence_dict."""
        return cls.generate_evidence_dict(result)

    @classmethod
    def format_text_report(cls, result: ResponsiveMatrixResult) -> str:
        """Formats a human-readable terminal execution summary."""
        lines = []
        lines.append("=" * 73)
        lines.append("       MDS RESPONSIVE VIEWPORT AUTOMATION EXECUTION REPORT        ")
        lines.append("=" * 73)
        lines.append(f"Capability ID:     {result.capability_id}")
        lines.append(f"Overall Status:    {result.status}")
        lines.append(f"Total Runs:        {len(result.runs)} (Canonical 17-Run Matrix)")
        lines.append(f"Total Assertions:  {result.total_assertions}")
        lines.append(f"  [+] Passed:      {result.passed_assertions}")
        lines.append(f"  [-] Hard Failed: {result.hard_failures}")
        lines.append(f"Duration:          {result.duration_ms:.1f} ms")
        if result.browser_version:
            lines.append(f"Browser:           {result.browser_version}")
        lines.append("-" * 73)

        lines.append("\n--- [CANONICAL 17-RUN MATRIX BREAKDOWN] ---")
        for r in result.runs:
            status_tag = "[PASS]" if r.passed else "[FAIL]"
            cfg = r.config
            lines.append(
                f"{status_tag} {r.run_id:<12} {cfg.screen:<12} "
                f"{cfg.viewport.label:<16} Dir:{cfg.direction:<4} "
                f"Density:{cfg.density:<12} ({r.duration_ms:.1f}ms)"
            )
            # Show any hard failures
            for a in r.hard_failures:
                lines.append(
                    f"       └── [FAIL] {a.assertion_name} ({a.selector}): "
                    f"expected {a.expected}, got {a.actual}"
                )
                if a.diagnostics:
                    lines.append(f"           Details: {a.diagnostics}")

        lines.append("-" * 73)
        if result.status == "PASS":
            lines.append("[SUCCESS] All 17 Canonical Responsive Runs PASSED with 0 hard failures.")
        elif result.status == "DEFERRED":
            lines.append(f"[DEFERRED] Execution deferred: {result.error_message}")
        else:
            lines.append(f"[FAILURE] Responsive Matrix failed with {result.hard_failures} hard failure(s).")
        lines.append("=" * 73)
        return "\n".join(lines)

    @classmethod
    def save_artifact(cls, result: ResponsiveMatrixResult, output_path: Path) -> Path:
        """Serializes evidence dictionary to target JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        data = cls.generate_evidence_dict(result)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return output_path
