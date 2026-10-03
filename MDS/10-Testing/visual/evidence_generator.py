#!/usr/bin/env python3
"""
MDS Visual Evidence Generator
Phase 9.7.7: Visual Regression Engine & Snapshot Diffing
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Serializes visual regression results into structured JSON evidence
and human-readable audit text reports.
"""

import json
from typing import Dict, Any, Optional
from pathlib import Path

from .visual_models import VisualSweepResult, ComparisonResult


class VisualEvidenceGenerator:
    """
    Handles persistence and serialization of visual regression telemetry.
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(__file__).resolve().parent.parent.parent.parent
        self.artifacts_dir = self.workspace_root / "MDS" / "10-Testing" / "artifacts" / "visual_diffs"

    def save_evidence(self, sweep_result: VisualSweepResult) -> Path:
        """
        Writes visual_evidence.json into the artifacts directory.
        """
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        evidence_file = self.artifacts_dir / "visual_evidence.json"

        data = sweep_result.to_dict()
        data["metadata"] = {
            "engine": "Pure Python Standard Library (zlib/struct)",
            "color_metric": "Luminance-Weighted RGB Distance (D_lum)",
            "coefficients": "ITU-R BT.601 (0.299, 0.587, 0.114)",
            "font_family": "Cairo (Pinned Local Offline Artifact)",
            "pixel_threshold": 0.05,
            "image_threshold": 0.001,
            "cartesian_space": "528 total = 12 visual baselines + 516 non-baselined combinations"
        }

        evidence_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
        sweep_result.evidence_file = evidence_file
        return evidence_file

    @staticmethod
    def format_text_report(sweep_result: VisualSweepResult) -> str:
        """
        Generates a formatted text summary for console output and test assertions.
        """
        lines = [
            "=" * 73,
            "            MDS VISUAL REGRESSION & SNAPSHOT DIFFING AUDIT REPORT        ",
            "=" * 73,
            f"Capability ID:     {sweep_result.capability_id}",
            f"Status:            {sweep_result.status.value}",
            f"Baselines Audited: {sweep_result.total_baselines}",
            f"  [+] Passed:      {sweep_result.passed_baselines}",
            f"  [-] Failed:      {sweep_result.failed_baselines}",
            f"  [*] Deferred:    {sweep_result.deferred_baselines}",
            f"Total Duration:    {sweep_result.total_duration_ms:.2f} ms",
            "-" * 73,
            "Runs Execution Summary:"
        ]

        for r in sweep_result.results:
            m = r.metrics
            diff_pct = m.diff_ratio * 100.0
            status_tag = f"[{r.status.value}]"
            lines.append(
                f"  {status_tag:<8} {r.baseline_id:<14} {m.dimensions:<10} "
                f"Diff: {diff_pct:.4f}% ({m.mismatched_pixels}/{m.total_pixels} px) "
                f"[{m.duration_ms:.1f}ms]"
            )
            if r.error_message:
                lines.append(f"           └── Error: {r.error_message}")

        lines.append("-" * 73)
        if sweep_result.status.value == "PASS":
            lines.append("OVERALL VERDICT: SUCCESS — 100% of canonical visual baselines PASSED.")
        elif sweep_result.status.value == "DEFERRED":
            lines.append(f"OVERALL VERDICT: DEFERRED — {sweep_result.error_message}")
        else:
            lines.append(f"OVERALL VERDICT: FAILED — {sweep_result.failed_baselines} visual regressions detected.")
        lines.append("=" * 73)

        return "\n".join(lines)
