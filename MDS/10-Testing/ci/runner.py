"""
Master Design System (MDS) -- CI Pipeline Execution Bridge & Runner
Document Reference: MDS-SPEC-9711-REV5 / Section 5, 6, 7 & 15
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

TESTING_DIR = Path(__file__).resolve().parent.parent
if str(TESTING_DIR) not in sys.path:
    sys.path.insert(0, str(TESTING_DIR))

try:
    from .adapters import CIProviderAdapter, detect_adapter
    from .collector import ArtifactCollector
    from .comparison import HistoricalComparisonEngine
    from .dashboard import DashboardGenerator
    from .manifest import write_manifest
    from .models import ExitCode, FindingRecord
    from .pointer import LatestPointerManager
    from .sidecar import SidecarManager
    from .trust import TrustVerifier
except ImportError:
    from ci.adapters import CIProviderAdapter, detect_adapter
    from ci.collector import ArtifactCollector
    from ci.comparison import HistoricalComparisonEngine
    from ci.dashboard import DashboardGenerator
    from ci.manifest import write_manifest
    from ci.models import ExitCode, FindingRecord
    from ci.pointer import LatestPointerManager
    from ci.sidecar import SidecarManager
    from ci.trust import TrustVerifier


class CIRunner:
    """
    Drives the complete 4-Stage CI lifecycle (MDS-CI-001):
      Stage 1: Runner Initialization & Adapter Detection
      Stage 2: Authoritative Validation Execution (python MDS/10-Testing/run_all.py --ci)
      Stage 3: Artifact Harvesting, Canonical Manifest & External Digest Sidecar
      Stage 4: Static Dashboard Bundling, Step Summary & Exit Code Propagation
    """

    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        force_provider: str = "",
    ):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.adapter: CIProviderAdapter = detect_adapter(self.workspace_root, force_provider=force_provider)
        self.ci_root = self.workspace_root / "MDS" / "10-Testing" / "artifacts" / "ci"
        self.collector = ArtifactCollector(self.workspace_root, self.ci_root)

        registry_path = self.workspace_root / "MDS" / "10-Testing" / "baselines" / "provenance" / "surface_provenance_registry.json"
        hist_dir = self.workspace_root / "MDS" / "10-Testing" / "baselines" / "historical"
        self.comparison_engine = HistoricalComparisonEngine(registry_path, hist_dir)

    def execute_pipeline(
        self,
        custom_telemetry_path: Optional[Path] = None,
        skip_execution: bool = False,
        simulated_exit_code: Optional[int] = None,
    ) -> Tuple[int, Dict[str, Any], Path]:
        """
        Executes the CI lifecycle and returns (exit_code, manifest_dict, run_dir).
        """
        ci_start_time = time.perf_counter()

        # --- Stage 1: Runner Initialization ---
        env_ctx = self.adapter.detect_environment()

        # --- Stage 2: Authoritative Validation Execution ---
        telemetry_file = custom_telemetry_path or (
            self.workspace_root / "MDS" / "10-Testing" / "artifacts" / "run_all_telemetry.json"
        )
        stdout_text = ""
        stderr_text = ""
        orchestrator_exit_code = ExitCode.SUCCESS.value

        if not skip_execution:
            run_all_script = self.workspace_root / "MDS" / "10-Testing" / "run_all.py"
            cmd = [sys.executable, str(run_all_script), "--ci"]
            proc = subprocess.run(
                cmd,
                cwd=str(self.workspace_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
            )
            stdout_text = proc.stdout
            stderr_text = proc.stderr
            orchestrator_exit_code = proc.returncode
        elif simulated_exit_code is not None:
            orchestrator_exit_code = simulated_exit_code

        # --- Stage 3: Artifact Harvesting & Manifest Assembly ---
        ci_overhead_ms = (time.perf_counter() - ci_start_time) * 1000.0

        manifest_dict, run_dir = self.collector.harvest_execution(
            env_context=env_ctx,
            telemetry_path=telemetry_file,
            stdout_text=stdout_text,
            stderr_text=stderr_text,
            ci_overhead_ms=ci_overhead_ms,
        )

        # Classify raw findings using the 5-step decision algorithm (ADR-152)
        raw_findings = manifest_dict.get("findings", [])
        finding_objs = [
            FindingRecord(
                severity=f.get("severity", "INFO"),
                code=f.get("code", "UNKNOWN"),
                target=f.get("target", ""),
                line=f.get("line"),
                col=f.get("col"),
                message=f.get("message", ""),
            )
            for f in raw_findings
        ]
        classified_findings = self.comparison_engine.classify_all_findings(finding_objs)

        # Update findings in manifest with derived provenance metadata
        manifest_dict["findings"] = [
            {
                "severity": cf.severity,
                "code": cf.code,
                "target": cf.target,
                "line": cf.line,
                "col": cf.col,
                "message": cf.message,
                "provenance": cf.provenance,
                "triage_state": cf.triage_state,
            }
            for cf in classified_findings
        ]

        # Serialize canonical manifest and calculate internal hash (ADR-146)
        manifest_file = run_dir / "ci_artifact_manifest.json"
        write_manifest(manifest_dict, manifest_file)
        manifest_digest = manifest_dict["manifest_sha256"]

        # Generate external digest sidecar (ADR-149)
        sidecar_file = SidecarManager.write_sidecar(manifest_file, manifest_digest)

        # Commit Provider-Controlled Trust Record to CI Provider Control Plane (ADR-151)
        trusted_record = self.adapter.record_trusted_execution(manifest_dict)

        # Verify Full Trust Chain
        TrustVerifier.verify_full_trust_chain(
            manifest_path=manifest_file,
            sidecar_path=sidecar_file,
            trusted_record=trusted_record if env_ctx.is_ci else None,
            is_ci=env_ctx.is_ci,
        )

        # Update latest.json Logical Pointer (ADR-148)
        rel_manifest_path = manifest_file.relative_to(self.ci_root).as_posix()
        LatestPointerManager.write_pointer(
            ci_artifacts_root=self.ci_root,
            run_id=env_ctx.run_id,
            manifest_relative_path=rel_manifest_path,
            manifest_digest=manifest_digest,
        )

        # --- Stage 4: Static Dashboard & Summary Generation ---
        dashboard_dir = run_dir / "dashboard"
        DashboardGenerator.generate_dashboard(manifest_dict, dashboard_dir)

        # Export step summary markdown
        summary_file = run_dir / "step_summary.md"
        self.adapter.export_step_summary(manifest_dict, summary_file)

        # Emit PR annotations
        for cf in classified_findings:
            if cf.severity in ("BLOCKER", "CRITICAL"):
                annotation_str = self.adapter.format_pr_annotation(cf)
                # In GitHub Actions, printing to stdout triggers runner annotation
                if env_ctx.is_ci:
                    print(annotation_str, file=sys.stdout)

        # Final exit code propagation invariant: Orchestrator owns the Exit Code!
        final_exit_code = manifest_dict.get("orchestrator_summary", {}).get("exit_code", orchestrator_exit_code)
        return final_exit_code, manifest_dict, run_dir


def main():
    parser = argparse.ArgumentParser(description="Master Design System -- CI Pipeline Runner")
    parser.add_argument("--workspace", type=str, default=None, help="Path to repository workspace root")
    parser.add_argument("--provider", type=str, default="", help="Force specific CI provider adapter")
    args = parser.parse_args()

    workspace_root = Path(args.workspace) if args.workspace else Path.cwd()
    runner = CIRunner(workspace_root=workspace_root, force_provider=args.provider)
    exit_code, _, _ = runner.execute_pipeline()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
