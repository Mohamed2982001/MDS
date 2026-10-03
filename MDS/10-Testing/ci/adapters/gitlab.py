"""
Master Design System (MDS) -- GitLab CI Adapter
Document Reference: MDS-SPEC-9711-REV5 / Section 6 & Table 6.2
"""

from __future__ import annotations

import json
import os
import platform
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..models import CIEnvironmentContext, FindingRecord, TrustedExecutionRecord
from .base import CIProviderAdapter


class GitLabCIAdapter(CIProviderAdapter):
    """
    Adapter for GitLab CI environment.
    """

    _CONTROL_PLANE_STORE: Dict[str, TrustedExecutionRecord] = {}

    def detect_environment(self) -> CIEnvironmentContext:
        pipeline_id = os.environ.get("CI_PIPELINE_ID", "pipeline-0")
        job_id = os.environ.get("CI_JOB_ID", "job-0")
        commit_sha = os.environ.get("CI_COMMIT_SHA", "0" * 40)
        ref = os.environ.get("CI_COMMIT_REF_NAME", "main")
        actor = os.environ.get("GITLAB_USER_LOGIN", "gitlab-ci[bot]")
        runner_os = platform.system().lower()
        runner_arch = platform.machine().lower()

        pr_number = None
        mr_iid = os.environ.get("CI_MERGE_REQUEST_IID")
        if mr_iid and mr_iid.isdigit():
            pr_number = int(mr_iid)

        formatted_run_id = f"gl-{pipeline_id}-{job_id}"

        return CIEnvironmentContext(
            provider_name="gitlab_ci",
            is_ci=True,
            run_id=formatted_run_id,
            run_attempt=1,
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
        lines = [
            f"# GitLab CI MDS Validation Report",
            f"Pipeline: {run_ctx.get('run_id')} | Status: {orch.get('overall_status')} | Exit: {orch.get('exit_code')}",
            f"Digest: {manifest_dict.get('manifest_sha256')}",
        ]
        summary_md = "\n".join(lines) + "\n"
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
            provider_identity="gitlab_ci",
            execution_identity=f"job_{run_id}",
            authenticity_status="PROVIDER_VERIFIED",
        )
        self._CONTROL_PLANE_STORE[run_id] = record
        return record

    def fetch_trusted_execution(self, run_id: str) -> Optional[TrustedExecutionRecord]:
        return self._CONTROL_PLANE_STORE.get(run_id)

    def format_pr_annotation(self, finding: FindingRecord) -> str:
        severity_map = {"BLOCKER": "blocker", "CRITICAL": "critical", "WARN": "major", "INFO": "info"}
        gitlab_severity = severity_map.get(finding.severity, "info")
        return json.dumps({
            "description": f"[{finding.code}] {finding.message}",
            "severity": gitlab_severity,
            "location": {
                "path": finding.target,
                "lines": {"begin": finding.line or 1}
            }
        })
