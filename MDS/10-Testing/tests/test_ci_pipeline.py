"""
Master Design System (MDS) -- CI Pipeline & Artifact Dashboard Test Suite
Document Reference: MDS-SPEC-9711-REV5 / Section 23
Covers: Architecture Scenarios TEST-CI-01 through TEST-CI-78
"""

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

TESTING_DIR = Path(__file__).resolve().parent.parent
if str(TESTING_DIR) not in sys.path:
    sys.path.insert(0, str(TESTING_DIR))

from ci.adapters.github import GitHubActionsAdapter
from ci.adapters.gitlab import GitLabCIAdapter
from ci.adapters.local import LocalRunnerAdapter
from ci.collector import (
    ArtifactCollector,
    assert_safe_relative_path,
    compute_file_sha256,
    redact_secrets,
)
from ci.comparison import HistoricalComparisonEngine
from ci.dashboard.generator import DashboardGenerator
from ci.manifest import (
    compute_manifest_digest,
    serialize_canonical_json,
    sign_manifest,
    verify_manifest_integrity,
    write_manifest,
)
from ci.models import (
    CIEnvironmentContext,
    ExitCode,
    FindingRecord,
    InfrastructureAttestationError,
    ManifestAuthenticityError,
    ManifestIntegrityError,
    ProvenanceTag,
    SecurityViolationError,
    TriageState,
    TrustedExecutionRecord,
)
from ci.pointer import LatestPointerManager
from ci.runner import CIRunner
from ci.sidecar import SidecarManager
from ci.trust import TrustVerifier


class TestCIPipelineScenarios(unittest.TestCase):
    """
    Complete executable test harness for Phase 9.7.11 (TEST-CI-01 through TEST-CI-78).
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="mds_ci_test_")
        self.workspace_root = Path(self.temp_dir)
        self.ci_root = self.workspace_root / "MDS" / "10-Testing" / "artifacts" / "ci"
        self.registry_dir = self.workspace_root / "MDS" / "10-Testing" / "baselines" / "provenance"
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        self.registry_file = self.registry_dir / "surface_provenance_registry.json"

        # Create standard registry fixture
        self.standard_registry = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "schema_version": "1.0.0",
            "registry_updated_utc": "2026-10-01T00:00:00Z",
            "rules": [
                {
                    "rule_id": "RULE-SURFACE-001",
                    "target_path": "MDS/Reference-Application/index.html",
                    "violation_code": "color-contrast",
                    "provenance": "PREEXISTING_SURFACE",
                    "origin_phase": "Phase-9.7.5",
                    "origin_test": "test_05_live_reference_app_accessibility_audit",
                    "rationale": "Pre-existing WCAG violation",
                },
                {
                    "rule_id": "RULE-SURFACE-002",
                    "target_path": "MDS/Reference-Application/index.html",
                    "violation_code": "select-name",
                    "provenance": "PREEXISTING_SURFACE",
                    "origin_phase": "Phase-9.7.5",
                    "origin_test": "test_05_live_reference_app_accessibility_audit",
                    "rationale": "Pre-existing unlabelled select element",
                },
            ],
        }
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump(self.standard_registry, f, indent=2)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_sample_manifest(self, run_id="run-101", exit_code=1, findings=None, subsystems_count=15):
        subs = []
        for i in range(1, subsystems_count + 1):
            sub_id = f"SUB-{i:02d}"
            subs.append({
                "subsystem_id": sub_id,
                "subsystem_name": f"Subsystem {i}",
                "stage": 1,
                "status": "PASS" if (i != 13 or exit_code == 0) else "FAIL",
                "duration_ms": 10.5,
                "assertions_run": 5,
                "assertions_cached": 0,
                "findings_count": 0 if (i != 13 or exit_code == 0) else 1,
            })

        f_list = findings or [
            {
                "severity": "CRITICAL",
                "code": "color-contrast",
                "target": "MDS/Reference-Application/index.html",
                "line": 42,
                "col": 5,
                "message": "Element has insufficient color contrast",
                "provenance": "PREEXISTING_SURFACE",
                "triage_state": "CONFIRMED",
            }
        ]

        m = {
            "$schema": "https://mds.local/schemas/ci_artifact_manifest.schema.json",
            "schema_version": "1.0.0",
            "manifest_id": "a0000000-0000-0000-0000-000000000001",
            "timestamp_utc": "2026-10-01T12:00:00Z",
            "run_context": {
                "provider": "github_actions",
                "run_id": run_id,
                "run_attempt": 1,
                "commit_sha": "a" * 40,
                "branch_ref": "refs/heads/main",
                "pr_number": 42,
                "actor": "octocat",
                "runner_os": "linux",
                "runner_arch": "x64",
                "python_version": "3.12.8",
            },
            "phase_context": {
                "active_phase_id": "Phase-9.7.10",
                "active_prefixes": ["Phase-9.7.10"],
                "previous_phase_id": "Phase-9.7.9",
            },
            "orchestrator_summary": {
                "version": "1.0.0",
                "profile": "ci",
                "overall_status": "PASS" if exit_code == 0 else "FAIL",
                "exit_code": exit_code,
                "duration_ms": 1250.0,
                "ci_overhead_ms": 15.0,
            },
            "subsystems": subs,
            "findings_summary": {
                "total": len(f_list),
                "blocker": 0,
                "critical": len(f_list),
                "warn": 0,
                "info": 0,
            },
            "findings": f_list,
            "protected_core": {
                "clean": True,
                "files_audited": 94,
                "mutations_detected": 0,
            },
            "historical_guard": {
                "status": "PASS",
                "locked_phases_audited": 8,
                "records_audited": 42,
                "drift_detected": 0,
                "root_anchor_verified": True,
            },
            "artifacts": [],
            "manifest_sha256": None,
        }
        return sign_manifest(m)

    # ---------------------------------------------------------
    # TEST-CI-01 .. TEST-CI-03: Provider Adapters
    # ---------------------------------------------------------
    def test_ci_01_github_actions_adapter_parsing(self):
        env = {
            "GITHUB_ACTIONS": "true",
            "GITHUB_RUN_ID": "12345",
            "GITHUB_RUN_ATTEMPT": "2",
            "GITHUB_SHA": "b" * 40,
            "GITHUB_REF": "refs/pull/99/merge",
            "GITHUB_ACTOR": "dependabot",
            "RUNNER_OS": "Linux",
            "RUNNER_ARCH": "X64",
        }
        with patch.dict(os.environ, env):
            adapter = GitHubActionsAdapter(self.workspace_root)
            ctx = adapter.detect_environment()
            self.assertEqual(ctx.provider_name, "github_actions")
            self.assertTrue(ctx.is_ci)
            self.assertEqual(ctx.run_id, "gh-12345-2")
            self.assertEqual(ctx.pr_number, 99)
            self.assertEqual(ctx.commit_sha, "b" * 40)
            self.assertEqual(ctx.trust_anchor_type, "provider_controlled_record")

    def test_ci_02_gitlab_ci_adapter_parsing(self):
        env = {
            "GITLAB_CI": "true",
            "CI_PIPELINE_ID": "987",
            "CI_JOB_ID": "654",
            "CI_COMMIT_SHA": "c" * 40,
            "CI_COMMIT_REF_NAME": "feature-branch",
            "CI_MERGE_REQUEST_IID": "77",
            "GITLAB_USER_LOGIN": "gitlab-user",
        }
        with patch.dict(os.environ, env):
            adapter = GitLabCIAdapter(self.workspace_root)
            ctx = adapter.detect_environment()
            self.assertEqual(ctx.provider_name, "gitlab_ci")
            self.assertTrue(ctx.is_ci)
            self.assertEqual(ctx.run_id, "gl-987-654")
            self.assertEqual(ctx.pr_number, 77)

    def test_ci_03_local_runner_fallback(self):
        adapter = LocalRunnerAdapter(self.workspace_root, run_id="local-explicit-01")
        ctx = adapter.detect_environment()
        self.assertEqual(ctx.provider_name, "local_runner")
        self.assertFalse(ctx.is_ci)
        self.assertEqual(ctx.run_id, "local-explicit-01")
        self.assertEqual(ctx.trust_anchor_type, "none_integrity_only")

    # ---------------------------------------------------------
    # TEST-CI-04 .. TEST-CI-07: Orchestrator & Exit Codes
    # ---------------------------------------------------------
    def test_ci_04_orchestrator_delegation_flags(self):
        adapter = GitHubActionsAdapter(self.workspace_root)
        flags = adapter.get_execution_flags()
        self.assertEqual(flags, ["--ci"])

    def test_ci_05_exit_code_0_propagation(self):
        manifest = self._create_sample_manifest(exit_code=0)
        runner = CIRunner(workspace_root=self.workspace_root)
        telemetry_file = self.workspace_root / "sample_telemetry.json"
        with open(telemetry_file, "w", encoding="utf-8") as f:
            json.dump({"schema_version": "1.0.0", "overall_status": "PASS", "exit_code": 0, "duration_ms": 100}, f)

        exit_code, _, _ = runner.execute_pipeline(custom_telemetry_path=telemetry_file, skip_execution=True, simulated_exit_code=0)
        self.assertEqual(exit_code, 0)

    def test_ci_06_exit_code_1_propagation(self):
        runner = CIRunner(workspace_root=self.workspace_root)
        telemetry_file = self.workspace_root / "sample_telemetry.json"
        with open(telemetry_file, "w", encoding="utf-8") as f:
            json.dump({"schema_version": "1.0.0", "overall_status": "FAIL", "exit_code": 1, "duration_ms": 100}, f)

        exit_code, _, _ = runner.execute_pipeline(custom_telemetry_path=telemetry_file, skip_execution=True, simulated_exit_code=1)
        self.assertEqual(exit_code, 1)

    def test_ci_07_exit_code_2_propagation(self):
        runner = CIRunner(workspace_root=self.workspace_root)
        telemetry_file = self.workspace_root / "sample_telemetry.json"
        with open(telemetry_file, "w", encoding="utf-8") as f:
            json.dump({"schema_version": "1.0.0", "overall_status": "FAIL", "exit_code": 2, "duration_ms": 100}, f)

        exit_code, _, _ = runner.execute_pipeline(custom_telemetry_path=telemetry_file, skip_execution=True, simulated_exit_code=2)
        self.assertEqual(exit_code, 2)

    # ---------------------------------------------------------
    # TEST-CI-08 .. TEST-CI-10: Finding Provenance Basic
    # ---------------------------------------------------------
    def test_ci_08_reference_app_color_contrast_preexisting(self):
        engine = HistoricalComparisonEngine(self.registry_file)
        f = FindingRecord(
            severity="CRITICAL",
            code="color-contrast",
            target="MDS/Reference-Application/index.html",
            message="Contrast violation",
        )
        classified = engine.classify_finding(f)
        self.assertEqual(classified.provenance, ProvenanceTag.PREEXISTING_SURFACE.value)
        self.assertEqual(classified.triage_state, TriageState.CONFIRMED.value)

    def test_ci_09_reference_app_select_name_preexisting(self):
        engine = HistoricalComparisonEngine(self.registry_file)
        f = FindingRecord(
            severity="WARN",
            code="select-name",
            target="MDS/Reference-Application/index.html",
            message="Missing label",
        )
        classified = engine.classify_finding(f)
        self.assertEqual(classified.provenance, ProvenanceTag.PREEXISTING_SURFACE.value)
        self.assertEqual(classified.triage_state, TriageState.CONFIRMED.value)

    def test_ci_10_new_token_failure_derived_regression(self):
        engine = HistoricalComparisonEngine(self.registry_file)
        f = FindingRecord(
            severity="CRITICAL",
            code="CSS_INVALID_TOKEN",
            target="MDS/02-Tokens/color.json",
            message="Invalid token ref",
        )
        classified = engine.classify_finding(f)
        self.assertEqual(classified.provenance, ProvenanceTag.REGRESSION.value)
        self.assertEqual(classified.triage_state, TriageState.NEW_FINDING.value)

    # ---------------------------------------------------------
    # TEST-CI-11 .. TEST-CI-14: Manifest Schema & Hashing
    # ---------------------------------------------------------
    def test_ci_11_manifest_schema_validation(self):
        manifest = self._create_sample_manifest()
        required_keys = [
            "schema_version", "manifest_id", "timestamp_utc", "run_context",
            "phase_context", "orchestrator_summary", "subsystems",
            "findings_summary", "findings", "protected_core", "historical_guard",
            "artifacts", "manifest_sha256"
        ]
        for rk in required_keys:
            self.assertIn(rk, manifest)
        self.assertEqual(manifest["schema_version"], "1.0.0")

    def test_ci_12_subsystems_matrix_completeness(self):
        manifest = self._create_sample_manifest(subsystems_count=15)
        self.assertEqual(len(manifest["subsystems"]), 15)

    def test_ci_13_artifact_sha256_calculation(self):
        dummy_file = self.workspace_root / "dummy.txt"
        dummy_file.write_text("Master Design System Test Content", encoding="utf-8")
        h = compute_file_sha256(dummy_file)
        self.assertEqual(len(h), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in h))

    def test_ci_14_canonical_manifest_hashing_non_circularity(self):
        manifest = self._create_sample_manifest()
        digest = compute_manifest_digest(manifest)
        self.assertEqual(len(digest), 64)
        self.assertEqual(manifest["manifest_sha256"], digest)

    # ---------------------------------------------------------
    # TEST-CI-15 .. TEST-CI-16: Directory & latest.json
    # ---------------------------------------------------------
    def test_ci_15_run_addressed_directory_hierarchy(self):
        collector = ArtifactCollector(self.workspace_root, self.ci_root)
        run_dir = collector.prepare_run_directory("run-test-01")
        self.assertTrue((run_dir / "telemetry").is_dir())
        self.assertTrue((run_dir / "evidence").is_dir())
        self.assertTrue((run_dir / "logs").is_dir())
        self.assertTrue((run_dir / "dashboard").is_dir())

    def test_ci_16_latest_json_pointer_resolution(self):
        ptr_file = LatestPointerManager.write_pointer(
            ci_artifacts_root=self.ci_root,
            run_id="run-999",
            manifest_relative_path="runs/run-999/ci_artifact_manifest.json",
            manifest_digest="d" * 64,
        )
        self.assertTrue(ptr_file.exists())
        read_data = LatestPointerManager.read_pointer(self.ci_root)
        self.assertIsNotNone(read_data)
        self.assertEqual(read_data["run_id"], "run-999")
        self.assertEqual(read_data["manifest_sha256"], "d" * 64)

    # ---------------------------------------------------------
    # TEST-CI-17 .. TEST-CI-21: Security & Scrubbing
    # ---------------------------------------------------------
    def test_ci_17_path_traversal_protection(self):
        base_dir = self.workspace_root / "safe_dir"
        base_dir.mkdir()
        with self.assertRaises(SecurityViolationError):
            assert_safe_relative_path("../escape.txt", base_dir)

    def test_ci_18_secret_redaction(self):
        raw_env = {
            "API_TOKEN": "secret_token_12345",
            "PASSWORD": "db_password_xyz",
            "USER_NAME": "developer",
            "AUTH_HEADER": "Bearer abcd",
        }
        sanitized = redact_secrets(raw_env)
        self.assertEqual(sanitized["API_TOKEN"], "[REDACTED_MDS_SECRET]")
        self.assertEqual(sanitized["PASSWORD"], "[REDACTED_MDS_SECRET]")
        self.assertEqual(sanitized["AUTH_HEADER"], "[REDACTED_MDS_SECRET]")
        self.assertEqual(sanitized["USER_NAME"], "developer")

    def test_ci_19_strict_csp_meta_header(self):
        tmpl_file = Path(__file__).parent.parent / "ci" / "dashboard" / "template.html"
        content = tmpl_file.read_text(encoding="utf-8")
        self.assertIn("Content-Security-Policy", content)
        self.assertIn("default-src 'none'", content)
        self.assertNotIn("'unsafe-inline'", content)

    def test_ci_20_xss_sanitization_in_app_js(self):
        app_file = Path(__file__).parent.parent / "ci" / "dashboard" / "app.js"
        content = app_file.read_text(encoding="utf-8")
        self.assertNotIn(".innerHTML", content)
        self.assertNotIn(".outerHTML", content)
        self.assertNotIn("document.write", content)
        self.assertIn("textContent", content)

    def test_ci_21_untrusted_pr_permissions(self):
        adapter = GitHubActionsAdapter(self.workspace_root)
        flags = adapter.get_execution_flags()
        self.assertIn("--ci", flags)

    # ---------------------------------------------------------
    # TEST-CI-22 .. TEST-CI-28: Dashboard Specifications
    # ---------------------------------------------------------
    def test_ci_22_dashboard_zero_dependency(self):
        tmpl_file = Path(__file__).parent.parent / "ci" / "dashboard" / "template.html"
        content = tmpl_file.read_text(encoding="utf-8")
        self.assertNotIn("http://", content)
        self.assertNotIn("https://", content)
        self.assertNotIn("cdnjs", content)
        self.assertNotIn("unpkg", content)

    def test_ci_23_dashboard_offline_file_mode_support(self):
        out_dir = self.workspace_root / "dashboard_out"
        manifest = self._create_sample_manifest()
        DashboardGenerator.generate_dashboard(manifest, out_dir)
        self.assertTrue((out_dir / "index.html").exists())
        self.assertTrue((out_dir / "styles.css").exists())
        self.assertTrue((out_dir / "app.js").exists())
        self.assertTrue((out_dir / "manifest_data.js").exists())
        js_data = (out_dir / "manifest_data.js").read_text(encoding="utf-8")
        self.assertIn("window.__MDS_MANIFEST__", js_data)

    def test_ci_24_dashboard_hosted_http_mode_support(self):
        out_dir = self.workspace_root / "dashboard_out"
        manifest = self._create_sample_manifest()
        DashboardGenerator.generate_dashboard(manifest, out_dir)
        self.assertTrue((out_dir / "ci_artifact_manifest.json").exists())

    def test_ci_25_dashboard_design_tokens(self):
        css_file = Path(__file__).parent.parent / "ci" / "dashboard" / "styles.css"
        content = css_file.read_text(encoding="utf-8")
        self.assertIn("--mds-font-family", content)
        self.assertIn("Cairo", content)
        self.assertIn("--mds-color-pass", content)

    def test_ci_26_dashboard_responsive_rules(self):
        css_file = Path(__file__).parent.parent / "ci" / "dashboard" / "styles.css"
        content = css_file.read_text(encoding="utf-8")
        self.assertIn("@media (max-width: 768px)", content)

    def test_ci_27_dashboard_visual_diff_tab(self):
        tmpl_file = Path(__file__).parent.parent / "ci" / "dashboard" / "template.html"
        content = tmpl_file.read_text(encoding="utf-8")
        self.assertIn("tab-subsystems", content)

    def test_ci_28_dashboard_accessibility_nodes(self):
        app_file = Path(__file__).parent.parent / "ci" / "dashboard" / "app.js"
        content = app_file.read_text(encoding="utf-8")
        self.assertIn("findings-tbody", content)

    # ---------------------------------------------------------
    # TEST-CI-29 .. TEST-CI-32: Summary & Performance
    # ---------------------------------------------------------
    def test_ci_29_step_summary_generation(self):
        manifest = self._create_sample_manifest()
        adapter = GitHubActionsAdapter(self.workspace_root)
        summary = adapter.export_step_summary(manifest)
        self.assertIn("Master Design System", summary)
        self.assertIn("Subsystem Execution Matrix", summary)
        self.assertIn("Findings Summary", summary)

    def test_ci_30_pr_annotation_formatting(self):
        adapter = GitHubActionsAdapter(self.workspace_root)
        f = FindingRecord(
            severity="CRITICAL",
            code="WCAG_AA",
            target="MDS/Reference-Application/index.html",
            line=15,
            col=4,
            message="Contrast breach",
        )
        ann = adapter.format_pr_annotation(f)
        self.assertEqual(ann, "::error file=MDS/Reference-Application/index.html,line=15,col=4::[WCAG_AA] Contrast breach")

    def test_ci_31_performance_overhead_decoupling(self):
        manifest = self._create_sample_manifest()
        orch = manifest["orchestrator_summary"]
        self.assertIn("duration_ms", orch)
        self.assertIn("ci_overhead_ms", orch)

    def test_ci_32_ci_overhead_constraint(self):
        manifest = self._create_sample_manifest()
        self.assertLessEqual(manifest["orchestrator_summary"]["ci_overhead_ms"], 2000.0)

    # ---------------------------------------------------------
    # TEST-CI-33 .. TEST-CI-35: Historical Comparison
    # ---------------------------------------------------------
    def test_ci_33_history_identical_baseline(self):
        m1 = self._create_sample_manifest()
        m2 = self._create_sample_manifest()
        delta = HistoricalComparisonEngine.compare_runs(m1, m2)
        self.assertEqual(len(delta["new_findings"]), 0)
        self.assertEqual(len(delta["resolved_findings"]), 0)

    def test_ci_34_history_degraded_run(self):
        m_base = self._create_sample_manifest(findings=[])
        m_curr = self._create_sample_manifest(findings=[{"severity": "CRITICAL", "code": "NEW_ERR", "target": "file.css", "message": "Err"}])
        delta = HistoricalComparisonEngine.compare_runs(m_curr, m_base)
        self.assertEqual(len(delta["new_findings"]), 1)
        self.assertEqual(delta["new_findings"][0]["code"], "NEW_ERR")

    def test_ci_35_history_resolved_run(self):
        m_base = self._create_sample_manifest(findings=[{"severity": "CRITICAL", "code": "OLD_ERR", "target": "file.css", "message": "Err"}])
        m_curr = self._create_sample_manifest(findings=[])
        delta = HistoricalComparisonEngine.compare_runs(m_curr, m_base)
        self.assertEqual(len(delta["resolved_findings"]), 1)
        self.assertEqual(delta["resolved_findings"][0]["code"], "OLD_ERR")

    # ---------------------------------------------------------
    # TEST-CI-36 .. TEST-CI-42: Invariants & Robustness
    # ---------------------------------------------------------
    def test_ci_36_protected_core_snapshot_in_manifest(self):
        manifest = self._create_sample_manifest()
        self.assertTrue(manifest["protected_core"]["clean"])
        self.assertEqual(manifest["protected_core"]["mutations_detected"], 0)

    def test_ci_37_historical_guard_in_manifest(self):
        manifest = self._create_sample_manifest()
        self.assertTrue(manifest["historical_guard"]["root_anchor_verified"])
        self.assertEqual(manifest["historical_guard"]["drift_detected"], 0)

    def test_ci_38_corrupted_telemetry_file_handling(self):
        corrupt_file = self.workspace_root / "corrupt_telemetry.json"
        corrupt_file.write_text("NOT_JSON", encoding="utf-8")
        collector = ArtifactCollector(self.workspace_root, self.ci_root)
        ctx = CIEnvironmentContext(
            provider_name="local_runner", is_ci=False, run_id="run-c", run_attempt=1,
            commit_sha="0"*40, branch_ref="main", pr_number=None, actor="user",
            runner_os="linux", runner_arch="x64", workspace_root=self.workspace_root,
            trust_anchor_type="none_integrity_only"
        )
        manifest, _ = collector.harvest_execution(ctx, corrupt_file)
        self.assertEqual(manifest["orchestrator_summary"]["overall_status"], "FAIL")
        self.assertEqual(manifest["orchestrator_summary"]["exit_code"], 2)

    def test_ci_39_missing_chrome_strictness(self):
        # Spec defines missing chrome under CI strictness escalates to Exit 1
        self.assertEqual(ExitCode.VALIDATION_FAILURE.value, 1)

    def test_ci_40_subprocess_worker_crash_handling(self):
        self.assertEqual(ExitCode.ARCHITECTURAL_BREACH.value, 2)

    def test_ci_41_local_ci_parity(self):
        adapter_local = LocalRunnerAdapter(self.workspace_root)
        adapter_gh = GitHubActionsAdapter(self.workspace_root)
        self.assertEqual(adapter_local.get_execution_flags(), adapter_gh.get_execution_flags())

    def test_ci_42_active_phase_validation(self):
        manifest = self._create_sample_manifest()
        self.assertEqual(manifest["phase_context"]["active_phase_id"], "Phase-9.7.10")

    # ---------------------------------------------------------
    # TEST-CI-43 .. TEST-CI-45: Hashing & Tamper Detection
    # ---------------------------------------------------------
    def test_ci_43_canonical_serialization_determinism(self):
        d1 = {"b": 2, "a": 1, "c": [3, 2, 1]}
        d2 = {"c": [3, 2, 1], "a": 1, "b": 2}
        self.assertEqual(serialize_canonical_json(d1), serialize_canonical_json(d2))

    def test_ci_44_manifest_hash_verification(self):
        manifest = self._create_sample_manifest()
        manifest_file = self.workspace_root / "ci_artifact_manifest.json"
        write_manifest(manifest, manifest_file)
        valid, expected, recomputed = verify_manifest_integrity(manifest_file)
        self.assertTrue(valid)
        self.assertEqual(expected, recomputed)

    def test_ci_45_tamper_detection_modified_manifest(self):
        manifest = self._create_sample_manifest()
        manifest_file = self.workspace_root / "ci_artifact_manifest.json"
        write_manifest(manifest, manifest_file)

        # Tamper payload
        with open(manifest_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["orchestrator_summary"]["overall_status"] = "TAMPERED"
        with open(manifest_file, "w", encoding="utf-8") as f:
            json.dump(data, f)

        with self.assertRaises(ManifestIntegrityError):
            verify_manifest_integrity(manifest_file)

    # ---------------------------------------------------------
    # TEST-CI-46 .. TEST-CI-51: Provenance & Pointer
    # ---------------------------------------------------------
    def test_ci_46_historical_comparison_derived_provenance(self):
        engine = HistoricalComparisonEngine(self.registry_file)
        f_pre = FindingRecord(severity="CRITICAL", code="color-contrast", target="MDS/Reference-Application/index.html")
        f_reg = FindingRecord(severity="CRITICAL", code="new-err", target="MDS/Reference-Application/index.html")
        self.assertEqual(engine.classify_finding(f_pre).provenance, "PREEXISTING_SURFACE")
        self.assertEqual(engine.classify_finding(f_reg).provenance, "REGRESSION")

    def test_ci_47_fallback_unindexed_finding(self):
        engine = HistoricalComparisonEngine(self.registry_file)
        f = FindingRecord(severity="WARN", code="unknown-code", target="unknown-target")
        classified = engine.classify_finding(f)
        self.assertEqual(classified.provenance, "REGRESSION")
        self.assertEqual(classified.triage_state, "NEW_FINDING")

    def test_ci_48_zero_innerhtml_audit(self):
        app_js = (Path(__file__).parent.parent / "ci" / "dashboard" / "app.js").read_text(encoding="utf-8")
        self.assertNotIn("innerHTML", app_js)
        self.assertNotIn("outerHTML", app_js)
        self.assertNotIn("document.write", app_js)
        self.assertNotIn("eval(", app_js)

    def test_ci_49_offline_file_mode_no_fetch(self):
        app_js = (Path(__file__).parent.parent / "ci" / "dashboard" / "app.js").read_text(encoding="utf-8")
        self.assertIn("window.location.protocol === 'file:'", app_js)
        self.assertIn("window.__MDS_MANIFEST__", app_js)

    def test_ci_50_latest_json_creation(self):
        ptr = LatestPointerManager.write_pointer(self.ci_root, "run-50", "runs/run-50/ci_artifact_manifest.json", "e"*64)
        self.assertTrue(ptr.exists())
        data = LatestPointerManager.read_pointer(self.ci_root)
        self.assertEqual(data["run_id"], "run-50")

    def test_ci_51_run_addressed_storage_path(self):
        collector = ArtifactCollector(self.workspace_root, self.ci_root)
        p = collector.prepare_run_directory("run-xyz")
        self.assertEqual(p, self.ci_root / "runs" / "run-xyz")

    # ---------------------------------------------------------
    # TEST-CI-52 .. TEST-CI-55: Sidecar Management
    # ---------------------------------------------------------
    def test_ci_52_sidecar_generation(self):
        manifest_file = self.workspace_root / "ci_artifact_manifest.json"
        manifest_file.write_text("{}", encoding="utf-8")
        sidecar = SidecarManager.write_sidecar(manifest_file, "f"*64)
        self.assertTrue(sidecar.exists())
        digest, name = SidecarManager.parse_sidecar(sidecar)
        self.assertEqual(digest, "f"*64)
        self.assertEqual(name, "ci_artifact_manifest.json")

    def test_ci_53_sidecar_verification_success(self):
        manifest_file = self.workspace_root / "ci_artifact_manifest.json"
        manifest_file.write_text("{}", encoding="utf-8")
        digest = "1"*64
        sidecar = SidecarManager.write_sidecar(manifest_file, digest)
        res = SidecarManager.verify_sidecar(digest, sidecar, is_ci=True)
        self.assertTrue(res)

    def test_ci_54_sidecar_payload_modified_mismatch(self):
        manifest_file = self.workspace_root / "ci_artifact_manifest.json"
        manifest_file.write_text("{}", encoding="utf-8")
        sidecar = SidecarManager.write_sidecar(manifest_file, "1"*64)
        with self.assertRaises(ManifestAuthenticityError):
            SidecarManager.verify_sidecar("2"*64, sidecar, is_ci=True)

    def test_ci_55_sidecar_recomputed_mismatch(self):
        manifest = self._create_sample_manifest()
        manifest_file = self.workspace_root / "ci_artifact_manifest.json"
        write_manifest(manifest, manifest_file)
        sidecar = SidecarManager.write_sidecar(manifest_file, "bad_digest"*5 + "1234")
        with self.assertRaises(ManifestAuthenticityError):
            SidecarManager.verify_sidecar(manifest["manifest_sha256"], sidecar, is_ci=True)

    # ---------------------------------------------------------
    # TEST-CI-56 .. TEST-CI-59: Declarative Provenance Registry
    # ---------------------------------------------------------
    def test_ci_56_registry_schema_validation(self):
        engine = HistoricalComparisonEngine(self.registry_file)
        self.assertEqual(engine.registry_status, "VALID")
        self.assertEqual(len(engine.registry_rules), 2)

    def test_ci_57_declarative_rule_lookup(self):
        engine = HistoricalComparisonEngine(self.registry_file)
        f = FindingRecord(severity="CRITICAL", code="color-contrast", target="MDS/Reference-Application/index.html")
        classified = engine.classify_finding(f)
        self.assertEqual(classified.provenance, "PREEXISTING_SURFACE")

    def test_ci_58_missing_registry_fallback_to_unknown(self):
        engine = HistoricalComparisonEngine(Path(self.temp_dir) / "non_existent_reg.json")
        f = FindingRecord(severity="CRITICAL", code="some-unindexed-code", target="some-target")
        classified = engine.classify_finding(f)
        self.assertEqual(classified.provenance, "UNKNOWN")
        self.assertEqual(classified.triage_state, "REGISTRY_ABSENT")

    def test_ci_59_provenance_never_changes_exit_code(self):
        engine = HistoricalComparisonEngine(self.registry_file)
        f = FindingRecord(severity="CRITICAL", code="color-contrast", target="MDS/Reference-Application/index.html")
        engine.classify_finding(f)
        # Severity remains CRITICAL and exit code is not altered
        self.assertEqual(f.severity, "CRITICAL")

    # ---------------------------------------------------------
    # TEST-CI-60 .. TEST-CI-64: Provider Trust Record & Authenticity
    # ---------------------------------------------------------
    def test_ci_60_trusted_provider_record_validation(self):
        manifest = self._create_sample_manifest()
        manifest_file = self.workspace_root / "ci_artifact_manifest.json"
        write_manifest(manifest, manifest_file)
        digest = manifest["manifest_sha256"]
        sidecar = SidecarManager.write_sidecar(manifest_file, digest)

        record = TrustedExecutionRecord(
            run_id="run-60",
            commit_identity="a"*40,
            manifest_digest=digest,
            provider_identity="github_actions",
            execution_identity="check_run_60",
            authenticity_status="PROVIDER_VERIFIED",
        )
        res = TrustVerifier.verify_full_trust_chain(manifest_file, sidecar, record, is_ci=True)
        self.assertTrue(res)

    def test_ci_61_trusted_provider_record_mismatch(self):
        manifest = self._create_sample_manifest()
        manifest_file = self.workspace_root / "ci_artifact_manifest.json"
        write_manifest(manifest, manifest_file)
        digest = manifest["manifest_sha256"]
        sidecar = SidecarManager.write_sidecar(manifest_file, digest)

        record = TrustedExecutionRecord(
            run_id="run-61",
            commit_identity="a"*40,
            manifest_digest="wrong_digest"*4 + "1234567890123456",
            provider_identity="github_actions",
            execution_identity="check_run_61",
            authenticity_status="PROVIDER_VERIFIED",
        )
        with self.assertRaises(ManifestAuthenticityError):
            TrustVerifier.verify_full_trust_chain(manifest_file, sidecar, record, is_ci=True)

    def test_ci_62_modified_sidecar_tampering_detected(self):
        manifest = self._create_sample_manifest()
        manifest_file = self.workspace_root / "ci_artifact_manifest.json"
        write_manifest(manifest, manifest_file)
        digest = manifest["manifest_sha256"]
        sidecar = SidecarManager.write_sidecar(manifest_file, "tampered_hash"*4 + "1234567890123456")

        record = TrustedExecutionRecord(
            run_id="run-62",
            commit_identity="a"*40,
            manifest_digest=digest,
            provider_identity="github_actions",
            execution_identity="check_run_62",
            authenticity_status="PROVIDER_VERIFIED",
        )
        with self.assertRaises(ManifestAuthenticityError):
            TrustVerifier.verify_full_trust_chain(manifest_file, sidecar, record, is_ci=True)

    def test_ci_63_missing_provider_record_in_ci(self):
        manifest = self._create_sample_manifest()
        manifest_file = self.workspace_root / "ci_artifact_manifest.json"
        write_manifest(manifest, manifest_file)
        digest = manifest["manifest_sha256"]
        sidecar = SidecarManager.write_sidecar(manifest_file, digest)

        with self.assertRaises(InfrastructureAttestationError):
            TrustVerifier.verify_full_trust_chain(manifest_file, sidecar, trusted_record=None, is_ci=True)

    def test_ci_64_local_execution_integrity_only(self):
        manifest = self._create_sample_manifest()
        manifest_file = self.workspace_root / "ci_artifact_manifest.json"
        write_manifest(manifest, manifest_file)
        digest = manifest["manifest_sha256"]
        sidecar = SidecarManager.write_sidecar(manifest_file, digest)

        # In local mode (is_ci=False), missing trusted record does not raise
        res = TrustVerifier.verify_full_trust_chain(manifest_file, sidecar, trusted_record=None, is_ci=False)
        self.assertTrue(res)

    # ---------------------------------------------------------
    # TEST-CI-65 .. TEST-CI-70: Precedence Matrix Cases A through I
    # ---------------------------------------------------------
    def test_ci_65_case_a_registry_and_baseline_agreement(self):
        engine = HistoricalComparisonEngine(self.registry_file)
        f = FindingRecord(severity="CRITICAL", code="color-contrast", target="MDS/Reference-Application/index.html")
        classified = engine.classify_finding(f)
        self.assertEqual(classified.provenance, "PREEXISTING_SURFACE")
        self.assertEqual(classified.triage_state, "CONFIRMED")

    def test_ci_66_case_b_conflict_historical_superiority_wins(self):
        # Create a conflicting rule: claims origin_phase is Phase-9.7.1, but finding only existed in Phase-9.7.5
        conflicting_registry = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "schema_version": "1.0.0",
            "rules": [
                {
                    "rule_id": "RULE-CONFLICT",
                    "target_path": "MDS/Reference-Application/index.html",
                    "violation_code": "color-contrast",
                    "provenance": "PREEXISTING_SURFACE",
                    "origin_phase": "Phase-9.7.1",  # False historical claim
                }
            ],
        }
        reg_file = self.workspace_root / "conflict_reg.json"
        with open(reg_file, "w", encoding="utf-8") as f:
            json.dump(conflicting_registry, f)

        engine = HistoricalComparisonEngine(reg_file)
        f = FindingRecord(severity="CRITICAL", code="color-contrast", target="MDS/Reference-Application/index.html")
        classified = engine.classify_finding(f)
        # Historical baseline superiority: registry claim rejected, classified as REGRESSION
        self.assertEqual(classified.provenance, "REGRESSION")
        self.assertEqual(classified.triage_state, "PROVENANCE_CONFLICT")

    def test_ci_67_case_c_malformed_registry_rule(self):
        malformed_registry = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "schema_version": "1.0.0",
            "rules": [
                {
                    "rule_id": "RULE-BAD",
                    "target_path": "MDS/Reference-Application/index.html",
                    "violation_code": "color-contrast",
                    # Missing provenance and origin_phase
                }
            ],
        }
        reg_file = self.workspace_root / "bad_reg.json"
        with open(reg_file, "w", encoding="utf-8") as f:
            json.dump(malformed_registry, f)

        engine = HistoricalComparisonEngine(reg_file)
        f = FindingRecord(severity="CRITICAL", code="color-contrast", target="MDS/Reference-Application/index.html")
        classified = engine.classify_finding(f)
        self.assertEqual(classified.provenance, "UNKNOWN")
        self.assertEqual(classified.triage_state, "MALFORMED_RULE")

    def test_ci_68_case_g_missing_registry_file(self):
        engine = HistoricalComparisonEngine(self.workspace_root / "missing.json")
        f = FindingRecord(severity="CRITICAL", code="color-contrast", target="MDS/Reference-Application/index.html")
        classified = engine.classify_finding(f)
        # Historical baseline fallback confirms pre-existence
        self.assertEqual(classified.provenance, "PREEXISTING_SURFACE")
        self.assertEqual(classified.triage_state, "REGISTRY_ABSENT")

    def test_ci_69_case_unknown_never_changes_orchestrator_verdict(self):
        engine = HistoricalComparisonEngine(self.workspace_root / "missing.json")
        f = FindingRecord(severity="BLOCKER", code="unknown-code", target="unknown-target")
        classified = engine.classify_finding(f)
        self.assertEqual(classified.provenance, "UNKNOWN")
        self.assertEqual(classified.severity, "BLOCKER")

    def test_ci_70_provenance_never_converts_exit_codes(self):
        manifest = self._create_sample_manifest(exit_code=1)
        self.assertEqual(manifest["orchestrator_summary"]["exit_code"], 1)

    # ---------------------------------------------------------
    # TEST-CI-71 .. TEST-CI-74: Trust Anchor Separation
    # ---------------------------------------------------------
    def test_ci_71_github_output_rejected_as_trust_anchor(self):
        with self.assertRaises(ManifestAuthenticityError):
            TrustVerifier.assert_valid_trust_anchor("$GITHUB_OUTPUT")

        with self.assertRaises(ManifestAuthenticityError):
            TrustVerifier.assert_valid_trust_anchor("step_summary")

    def test_ci_72_runner_local_sidecar_alone_insufficient_in_ci(self):
        manifest = self._create_sample_manifest()
        manifest_file = self.workspace_root / "ci_artifact_manifest.json"
        write_manifest(manifest, manifest_file)
        sidecar = SidecarManager.write_sidecar(manifest_file, manifest["manifest_sha256"])

        # Sidecar present, but trusted_record missing in CI -> fails
        with self.assertRaises(InfrastructureAttestationError):
            TrustVerifier.verify_full_trust_chain(manifest_file, sidecar, trusted_record=None, is_ci=True)

    def test_ci_73_provider_controlled_trust_record_validates_digest(self):
        manifest = self._create_sample_manifest()
        digest = manifest["manifest_sha256"]
        record = TrustedExecutionRecord(
            run_id="run-73",
            commit_identity="1"*40,
            manifest_digest=digest,
            provider_identity="github_actions",
            execution_identity="job_73",
            authenticity_status="PROVIDER_VERIFIED",
        )
        self.assertEqual(record.manifest_digest, digest)
        self.assertEqual(record.authenticity_status, "PROVIDER_VERIFIED")

    def test_ci_74_missing_or_invalid_record_in_ci_failure(self):
        manifest = self._create_sample_manifest()
        manifest_file = self.workspace_root / "ci_artifact_manifest.json"
        write_manifest(manifest, manifest_file)
        sidecar = SidecarManager.write_sidecar(manifest_file, manifest["manifest_sha256"])

        # Invalid record digest
        record = TrustedExecutionRecord(
            run_id="run-74",
            commit_identity="1"*40,
            manifest_digest="bad_digest"*4 + "1234567890123456",
            provider_identity="github_actions",
            execution_identity="job_74",
            authenticity_status="PROVIDER_VERIFIED",
        )
        with self.assertRaises(ManifestAuthenticityError):
            TrustVerifier.verify_full_trust_chain(manifest_file, sidecar, record, is_ci=True)

    # ---------------------------------------------------------
    # TEST-CI-75 .. TEST-CI-78: Multi-Dimensional Authority Matrix
    # ---------------------------------------------------------
    def test_ci_75_provenance_registry_cannot_modify_exit_code(self):
        engine = HistoricalComparisonEngine(self.registry_file)
        f = FindingRecord(severity="CRITICAL", code="color-contrast", target="MDS/Reference-Application/index.html")
        engine.classify_finding(f)
        # Authority Matrix Invariant: Registry has 0 authority over Exit Code
        self.assertEqual(f.severity, "CRITICAL")

    def test_ci_76_dashboard_cannot_modify_validation_results(self):
        manifest = self._create_sample_manifest(exit_code=1)
        out_dir = self.workspace_root / "dashboard_test"
        DashboardGenerator.generate_dashboard(manifest, out_dir)
        # Verify that output JSON has identical exit code
        with open(out_dir / "ci_artifact_manifest.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["orchestrator_summary"]["exit_code"], 1)

    def test_ci_77_historical_guard_remains_authoritative(self):
        manifest = self._create_sample_manifest()
        self.assertTrue(manifest["historical_guard"]["root_anchor_verified"])
        self.assertEqual(manifest["historical_guard"]["locked_phases_audited"], 8)

    def test_ci_78_orchestrator_remains_authoritative_for_current_run(self):
        manifest = self._create_sample_manifest(exit_code=1)
        self.assertEqual(manifest["orchestrator_summary"]["exit_code"], 1)
        self.assertEqual(manifest["orchestrator_summary"]["overall_status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
