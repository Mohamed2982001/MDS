"""
Master Design System (MDS) -- Local Runner Adapter
Document Reference: MDS-SPEC-9711-REV5 / Section 6 & Table 6.2
"""

from __future__ import annotations

import datetime
import platform
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..models import CIEnvironmentContext, FindingRecord, TrustedExecutionRecord
from .base import CIProviderAdapter


class LocalRunnerAdapter(CIProviderAdapter):
    """
    Adapter for local developer workflows.
    Operates in Integrity-Only Mode (ADR-151).
    """

    def __init__(self, workspace_root: Path, run_id: Optional[str] = None):
        super().__init__(workspace_root)
        self.explicit_run_id = run_id
        self._local_records: Dict[str, TrustedExecutionRecord] = {}

    def detect_environment(self) -> CIEnvironmentContext:
        now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M%S")
        run_id = self.explicit_run_id or f"local-{now_str}-{uuid.uuid4().hex[:6]}"

        return CIEnvironmentContext(
            provider_name="local_runner",
            is_ci=False,
            run_id=run_id,
            run_attempt=1,
            commit_sha="0" * 40,
            branch_ref="refs/heads/local",
            pr_number=None,
            actor="local-developer",
            runner_os=platform.system().lower(),
            runner_arch=platform.machine().lower(),
            workspace_root=self.workspace_root,
            trust_anchor_type="none_integrity_only",
        )

    def get_execution_flags(self) -> List[str]:
        return ["--ci"]

    def export_step_summary(self, manifest_dict: Dict[str, Any], output_path: Optional[Path] = None) -> str:
        orch = manifest_dict.get("orchestrator_summary", {})
        run_ctx = manifest_dict.get("run_context", {})
        lines = [
            f"# Local MDS Validation Summary",
            f"Run ID: {run_ctx.get('run_id')} | Status: {orch.get('overall_status')} | Exit: {orch.get('exit_code')}",
            f"Digest: {manifest_dict.get('manifest_sha256')}",
            f"Mode: Local Integrity-Only Mode",
        ]
        summary_md = "\n".join(lines) + "\n"
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(summary_md, encoding="utf-8")
        return summary_md

    def record_trusted_execution(self, manifest_dict: Dict[str, Any]) -> TrustedExecutionRecord:
        run_ctx = manifest_dict.get("run_context", {})
        run_id = run_ctx.get("run_id", "local-run")
        commit_sha = run_ctx.get("commit_sha", "0" * 40)
        digest = manifest_dict.get("manifest_sha256", "")

        record = TrustedExecutionRecord(
            run_id=run_id,
            commit_identity=commit_sha,
            manifest_digest=digest,
            provider_identity="local_runner",
            execution_identity=f"local_proc_{run_id}",
            authenticity_status="INTEGRITY_ONLY",
        )
        self._local_records[run_id] = record
        return record

    def fetch_trusted_execution(self, run_id: str) -> Optional[TrustedExecutionRecord]:
        return self._local_records.get(run_id)

    def format_pr_annotation(self, finding: FindingRecord) -> str:
        return f"[{finding.severity}] {finding.target}:{finding.line or 1} - [{finding.code}] {finding.message}"
