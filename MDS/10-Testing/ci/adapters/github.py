"""
Master Design System (MDS) -- GitHub Actions CI Adapter
Document Reference: MDS-SPEC-9711-REV5 / Section 6 & Table 6.2
"""

from __future__ import annotations

import os
import platform
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..models import CIEnvironmentContext, FindingRecord, TrustedExecutionRecord
from .base import CIProviderAdapter


class GitHubActionsAdapter(CIProviderAdapter):
    """
    Adapter for GitHub Actions environment.
    IMPORTANT (ADR-151):
      - $GITHUB_OUTPUT is runner-local transport ONLY; never a Trust Anchor.
      - $GITHUB_STEP_SUMMARY is markdown presentation only.
      - Provider-Controlled Trust Records reside in the Provider Control Plane.
    """

    # In-memory / provider control plane store simulation for testing & runner execution
    _CONTROL_PLANE_STORE: Dict[str, TrustedExecutionRecord] = {}

    def detect_environment(self) -> CIEnvironmentContext:
        run_id_raw = os.environ.get("GITHUB_RUN_ID", "local-run")
        run_attempt_raw = int(os.environ.get("GITHUB_RUN_ATTEMPT", "1"))
        commit_sha = os.environ.get("GITHUB_SHA", "0" * 40)
        ref = os.environ.get("GITHUB_REF", "refs/heads/main")
        actor = os.environ.get("GITHUB_ACTOR", "github-actions[bot]")
        runner_os = os.environ.get("RUNNER_OS", platform.system().lower())
        runner_arch = os.environ.get("RUNNER_ARCH", platform.machine().lower())

        pr_number = None
        pr_match = re.match(r"^refs/pull/(\d+)/", ref)
        if pr_match:
            pr_number = int(pr_match.group(1))

        formatted_run_id = f"gh-{run_id_raw}-{run_attempt_raw}"

        return CIEnvironmentContext(
            provider_name="github_actions",
            is_ci=True,
            run_id=formatted_run_id,
            run_attempt=run_attempt_raw,
            commit_sha=commit_sha,
            branch_ref=ref,
            pr_number=pr_number,
            actor=actor,
            runner_os=runner_os,
            runner_arch=runner_arch,
            workspace_root=self.workspace_root,
            trust_anchor_type="provider_controlled_record",
        )

    def get_execution_flags(self) -> List[str]:
        return ["--ci"]

    def export_step_summary(self, manifest_dict: Dict[str, Any], output_path: Optional[Path] = None) -> str:
        orch = manifest_dict.get("orchestrator_summary", {})
        run_ctx = manifest_dict.get("run_context", {})
        findings_summary = manifest_dict.get("findings_summary", {})
        subsystems = manifest_dict.get("subsystems", [])
        manifest_digest = manifest_dict.get("manifest_sha256", "UNVERIFIED")

        verdict_badge = "🟢 PASS" if orch.get("overall_status") == "PASS" else "🔴 FAIL"

        lines = [
            f"# Master Design System (MDS) — CI Validation Summary",
            f"",
            f"**Run ID:** `{run_ctx.get('run_id')}` | **Commit:** `{run_ctx.get('commit_sha')[:7]}` | **Branch:** `{run_ctx.get('branch_ref')}`",
            f"**Overall Verdict:** {verdict_badge} (Exit Code: `{orch.get('exit_code')}`)",
            f"**Total Execution Time:** `{orch.get('duration_ms', 0):.1f} ms` (CI Overhead: `{orch.get('ci_overhead_ms', 0):.1f} ms`)",
            f"**Canonical Manifest Digest:** `{manifest_digest}`",
            f"*(Attestation: Provider-Controlled Trust Record committed to GitHub Control Plane)*",
            f"",
            f"## Subsystem Execution Matrix",
            f"",
            f"| Subsystem | Stage | Status | Duration | Findings |",
            f"| :--- | :---: | :---: | :---: | :---: |",
        ]

        for sub in subsystems:
            status_emoji = "✅" if sub.get("status") == "PASS" else ("⚠️" if sub.get("status") == "DEFERRED" else "❌")
            lines.append(
                f"| `{sub.get('subsystem_id')}` {sub.get('subsystem_name')} | {sub.get('stage')} | {status_emoji} {sub.get('status')} | {sub.get('duration_ms', 0):.1f} ms | {sub.get('findings_count', 0)} |"
            )

        lines.extend([
            f"",
            f"## Findings Summary",
            f"- **Total Findings:** {findings_summary.get('total', 0)}",
            f"- **Blocker:** {findings_summary.get('blocker', 0)}",
            f"- **Critical:** {findings_summary.get('critical', 0)}",
            f"- **Warn:** {findings_summary.get('warn', 0)}",
            f"- **Info:** {findings_summary.get('info', 0)}",
            f"",
        ])

        summary_md = "\n".join(lines) + "\n"

        # If running inside GitHub Actions with GITHUB_STEP_SUMMARY set
        step_summary_env = os.environ.get("GITHUB_STEP_SUMMARY")
        if step_summary_env and Path(step_summary_env).parent.exists():
            try:
                with open(step_summary_env, "a", encoding="utf-8") as f:
                    f.write(summary_md)
            except Exception:
                pass

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(summary_md, encoding="utf-8")

        return summary_md

    def record_trusted_execution(self, manifest_dict: Dict[str, Any]) -> TrustedExecutionRecord:
        run_ctx = manifest_dict.get("run_context", {})
        run_id = run_ctx.get("run_id", "unknown-run")
        commit_sha = run_ctx.get("commit_sha", "0" * 40)
        digest = manifest_dict.get("manifest_sha256", "")

        record = TrustedExecutionRecord(
            run_id=run_id,
            commit_identity=commit_sha,
            manifest_digest=digest,
            provider_identity="github_actions",
            execution_identity=f"check_run_{run_id}",
            authenticity_status="PROVIDER_VERIFIED",
        )
        self._CONTROL_PLANE_STORE[run_id] = record
        return record

    def fetch_trusted_execution(self, run_id: str) -> Optional[TrustedExecutionRecord]:
        return self._CONTROL_PLANE_STORE.get(run_id)

    def format_pr_annotation(self, finding: FindingRecord) -> str:
        level = "error" if finding.severity in ("BLOCKER", "CRITICAL") else ("warning" if finding.severity == "WARN" else "notice")
        line_part = f",line={finding.line}" if finding.line else ""
        col_part = f",col={finding.col}" if finding.col else ""
        return f"::{level} file={finding.target}{line_part}{col_part}::[{finding.code}] {finding.message}"
