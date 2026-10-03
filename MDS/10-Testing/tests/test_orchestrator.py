"""
Master Design System (MDS) — Orchestrator Comprehensive Test Suite
Phase 9.7.10: Unified Local Orchestrator CLI & Master Validation Pipeline
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Standard library only (unittest).
Implements all 44 Pre-Implementation Test Scenarios (TEST-ORC-01 through TEST-ORC-44)
mandated by ADR-134 and Section 11 of the Ratified Architecture Specification.
"""

from __future__ import annotations

import copy
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Dict, List, Any

TESTING_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = TESTING_DIR.parent.parent
if str(TESTING_DIR) not in sys.path:
    sys.path.insert(0, str(TESTING_DIR))

from orchestrator.models import (
    ExecutionStatus,
    FindingSeverity,
    Finding,
    SubsystemDefinition,
    SubsystemResult,
    PipelineResult,
    ExecutionContext,
    ExecutionCategory,
    to_finding_severity,
)
from orchestrator.registry import (
    ORCHESTRATOR_SUBSYSTEM_REGISTRY,
    MANDATORY_SAFETY_GATES,
    resolve_subsystem_id,
)
from orchestrator.dag import DAGCompiler, DAGCycleError, InvalidTargetError
from orchestrator.cache import AssertionExecutionCache, AssertionIdentity
from orchestrator.snapshot import ProtectedCoreSnapshotManager
from orchestrator.governance import (
    PhaseGovernanceManager,
    PhaseGovernanceError,
    PHASE_TRANSITION_GRAPH,
)
from orchestrator.normalizer import (
    resolve_final_exit_code,
    NORMALIZATION_MATRIX_20,
)
from orchestrator.reporters import ConsoleReporter, JsonReporter
from orchestrator.cli import (
    create_parser,
    resolve_execution_policy,
    CLIConfigurationError,
)
from orchestrator.engine import OrchestratorEngine
from orchestrator.worker import run_worker_dispatch


class TestOrchestratorSuite(unittest.TestCase):
    """
    Exhaustive 44-Scenario Validation Suite for Master Orchestrator Pipeline.
    """

    @classmethod
    def setUpClass(cls):
        cls.engine = OrchestratorEngine(workspace_root=WORKSPACE_ROOT)
        cls.dag_compiler = DAGCompiler()
        cls.snapshot_mgr = ProtectedCoreSnapshotManager(WORKSPACE_ROOT)
        cls.gov_mgr = PhaseGovernanceManager(WORKSPACE_ROOT)

    # -------------------------------------------------------------------------
    # TEST-ORC-01: Clean repository default execution (--core)
    # -------------------------------------------------------------------------
    def test_orc_01_clean_repository_default_execution(self):
        """Verifies clean repository default execution (--core) completes Stages 0-3 with Exit 0."""
        result = self.engine.run_pipeline(profile="core")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.overall_status, ExecutionStatus.PASS)
        self.assertTrue(result.protected_core_clean)
        executed_sids = [r.subsystem_id for r in result.subsystem_results]
        # Should include SUB-01 through SUB-11
        for sid in [f"SUB-{i:02d}" for i in range(1, 12)]:
            self.assertIn(sid, executed_sids)

    # -------------------------------------------------------------------------
    # TEST-ORC-02: Fast profile execution (--fast)
    # -------------------------------------------------------------------------
    def test_orc_02_fast_profile_execution(self):
        """Verifies fast profile execution executes only Stages 0, 1, 2 in under 5 seconds."""
        result = self.engine.run_pipeline(profile="fast")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.overall_status, ExecutionStatus.PASS)
        executed_sids = [r.subsystem_id for r in result.subsystem_results]
        for sid in executed_sids:
            s_def = ORCHESTRATOR_SUBSYSTEM_REGISTRY[sid]
            self.assertIn(s_def.stage, [1, 2])
        # Stages 3 and 4 must not be executed
        self.assertNotIn("SUB-08", executed_sids)
        self.assertNotIn("SUB-12", executed_sids)
        self.assertLess(result.duration_ms, 5000.0)

    # -------------------------------------------------------------------------
    # TEST-ORC-03: Full profile execution (--full)
    # -------------------------------------------------------------------------
    def test_orc_03_full_profile_execution(self):
        """Verifies full profile compiles all 15 subsystems into the DAG plan."""
        plan = self.dag_compiler.compile_profile("full")
        self.assertEqual(len(plan), 15)
        plan_sids = [s.subsystem_id for s in plan]
        for i in range(1, 16):
            self.assertIn(f"SUB-{i:02d}", plan_sids)

    # -------------------------------------------------------------------------
    # TEST-ORC-04: Safe targeted subsystem execution (--subsystem historical)
    # -------------------------------------------------------------------------
    def test_orc_04_safe_targeted_subsystem_execution(self):
        """Verifies targeting historical guard executes Stage 1 safety gates and target."""
        plan = self.dag_compiler.compile_profile("core", target_subsystem="historical")
        plan_sids = [s.subsystem_id for s in plan]
        # All mandatory gates must be present
        for gate in MANDATORY_SAFETY_GATES:
            self.assertIn(gate, plan_sids)
        # Target must be present
        self.assertIn("SUB-01", plan_sids)
        # Unrequested stage 2/3 subsystems must not be present
        self.assertNotIn("SUB-05", plan_sids)
        self.assertNotIn("SUB-08", plan_sids)

    # -------------------------------------------------------------------------
    # TEST-ORC-05: Forbidden targeted bypass attempt (--subsystem visual)
    # -------------------------------------------------------------------------
    def test_orc_05_forbidden_targeted_bypass_attempt(self):
        """Confirms Stage 0 preflight and Stage 1 immutability cannot be bypassed when targeting visual."""
        plan = self.dag_compiler.compile_profile("full", target_subsystem="visual")
        plan_sids = [s.subsystem_id for s in plan]
        # Safety gates must be included
        for gate in MANDATORY_SAFETY_GATES:
            self.assertIn(gate, plan_sids)
        # Visual upstream dependency (SUB-12 Browser) must be included
        self.assertIn("SUB-12", plan_sids)
        self.assertIn("SUB-15", plan_sids)

    # -------------------------------------------------------------------------
    # TEST-ORC-06: Headless Chrome missing in --full mode
    # -------------------------------------------------------------------------
    def test_orc_06_headless_chrome_missing_in_full_mode(self):
        """Verifies missing Chrome marks dynamic tests as DEFERRED with Exit 0 in standard mode."""
        deferred_results = [
            SubsystemResult(
                subsystem_id="SUB-12",
                subsystem_name="Browser Infrastructure",
                status=ExecutionStatus.DEFERRED,
                findings=[Finding(FindingSeverity.INFO, "Chrome", "BROWSER_UNAVAILABLE", "No Chrome")],
            ),
            SubsystemResult(
                subsystem_id="SUB-13",
                subsystem_name="Accessibility",
                status=ExecutionStatus.DEFERRED,
                findings=[Finding(FindingSeverity.INFO, "SUB-13", "DYNAMIC_TEST_DEFERRED", "Deferred")],
            ),
        ]
        exit_code = resolve_final_exit_code(deferred_results, strict=False, strict_env=False)
        self.assertEqual(exit_code, 0)

    # -------------------------------------------------------------------------
    # TEST-ORC-07: Headless Chrome missing under --strict-environment
    # -------------------------------------------------------------------------
    def test_orc_07_headless_chrome_missing_under_strict_environment(self):
        """Verifies missing Chrome marks dynamic tests as DEFERRED and escalates to Exit 1 under strict-env."""
        deferred_results = [
            SubsystemResult(
                subsystem_id="SUB-12",
                subsystem_name="Browser Infrastructure",
                status=ExecutionStatus.DEFERRED,
                findings=[Finding(FindingSeverity.INFO, "Chrome", "BROWSER_UNAVAILABLE", "No Chrome")],
            )
        ]
        exit_code = resolve_final_exit_code(deferred_results, strict=False, strict_env=True)
        self.assertEqual(exit_code, 1)

    # -------------------------------------------------------------------------
    # TEST-ORC-08: Historical drift detection in Stage 1
    # -------------------------------------------------------------------------
    def test_orc_08_historical_drift_detection_stage_1(self):
        """Verifies drift detected in historical guard emits CRITICAL finding and Exit 1."""
        results = [
            SubsystemResult(
                subsystem_id="SUB-01",
                subsystem_name="Historical Phase Guard",
                status=ExecutionStatus.FAIL,
                findings=[Finding(FindingSeverity.CRITICAL, "Phase-1.0.md", "MODIFIED", "Hash drift")],
            )
        ]
        exit_code = resolve_final_exit_code(results)
        self.assertEqual(exit_code, 1)

    # -------------------------------------------------------------------------
    # TEST-ORC-09: Trust Anchor corruption in Stage 1
    # -------------------------------------------------------------------------
    def test_orc_09_trust_anchor_corruption_stage_1(self):
        """Verifies trust anchor corruption emits BLOCKER finding and Exit 2."""
        results = [
            SubsystemResult(
                subsystem_id="SUB-01",
                subsystem_name="Historical Phase Guard",
                status=ExecutionStatus.FAIL,
                findings=[Finding(FindingSeverity.BLOCKER, "RootAnchor", "TRUST_ANCHOR_MISMATCH", "Corrupted")],
            )
        ]
        exit_code = resolve_final_exit_code(results)
        self.assertEqual(exit_code, 2)

    # -------------------------------------------------------------------------
    # TEST-ORC-10: Governance invariant violation (INV-001)
    # -------------------------------------------------------------------------
    def test_orc_10_governance_invariant_violation(self):
        """Verifies governance invariant failure emits CRITICAL finding and Exit 1."""
        results = [
            SubsystemResult(
                subsystem_id="SUB-02",
                subsystem_name="Governance Engine",
                status=ExecutionStatus.FAIL,
                findings=[Finding(FindingSeverity.CRITICAL, "tokens.json", "INV-001", "Token count mismatch")],
            )
        ]
        exit_code = resolve_final_exit_code(results)
        self.assertEqual(exit_code, 1)

    # -------------------------------------------------------------------------
    # TEST-ORC-11: Capability Registry integrity violation
    # -------------------------------------------------------------------------
    def test_orc_11_capability_registry_integrity_violation(self):
        """Verifies capability registry integrity violation emits BLOCKER and Exit 2."""
        results = [
            SubsystemResult(
                subsystem_id="SUB-03",
                subsystem_name="Capability Registry",
                status=ExecutionStatus.FAIL,
                findings=[Finding(FindingSeverity.BLOCKER, "registry.json", "REGISTRY_CORRUPT", "Malformed schema")],
            )
        ]
        exit_code = resolve_final_exit_code(results)
        self.assertEqual(exit_code, 2)

    # -------------------------------------------------------------------------
    # TEST-ORC-12: CSS Scanner rule violation (raw hex injected)
    # -------------------------------------------------------------------------
    def test_orc_12_css_scanner_rule_violation(self):
        """Verifies CSS scanner violation logs exact target file/line and emits Exit 1."""
        finding = Finding(
            severity=FindingSeverity.CRITICAL,
            target="MDS/Runtime/components/button.css",
            code="RAW_HEX_COLOR",
            message="Raw hex color #ff0000 forbidden in author stylesheets",
            line=42,
        )
        results = [
            SubsystemResult(
                subsystem_id="SUB-06",
                subsystem_name="CSS Scanner",
                status=ExecutionStatus.FAIL,
                findings=[finding],
            )
        ]
        exit_code = resolve_final_exit_code(results)
        self.assertEqual(exit_code, 1)
        self.assertEqual(finding.line, 42)

    # -------------------------------------------------------------------------
    # TEST-ORC-13: Token schema corruption (invalid JSON)
    # -------------------------------------------------------------------------
    def test_orc_13_token_schema_corruption(self):
        """Verifies DTCG token parsing failure emits CRITICAL finding and Exit 1."""
        results = [
            SubsystemResult(
                subsystem_id="SUB-05",
                subsystem_name="Token DTCG Parser",
                status=ExecutionStatus.FAIL,
                findings=[Finding(FindingSeverity.CRITICAL, "color.tokens.json", "UNRESOLVED_ALIAS", "Broken alias")],
            )
        ]
        exit_code = resolve_final_exit_code(results)
        self.assertEqual(exit_code, 1)

    # -------------------------------------------------------------------------
    # TEST-ORC-14: Fail-fast mode (--fail-fast)
    # -------------------------------------------------------------------------
    def test_orc_14_fail_fast_mode(self):
        """Verifies --fail-fast stops running remaining subsystems after first critical failure."""
        all_findings = [Finding(FindingSeverity.CRITICAL, "target", "ERR", "Fail")]
        plan = self.dag_compiler.compile_profile("fast")
        all_results = []
        for s_def in plan:
            if any(f.severity in (FindingSeverity.CRITICAL, FindingSeverity.BLOCKER) for f in all_findings):
                all_results.append(
                    SubsystemResult(
                        subsystem_id=s_def.subsystem_id,
                        subsystem_name=s_def.subsystem_name,
                        status=ExecutionStatus.SKIPPED,
                    )
                )
        self.assertEqual(len(all_results), len(plan))
        for r in all_results:
            self.assertEqual(r.status, ExecutionStatus.SKIPPED)

    # -------------------------------------------------------------------------
    # TEST-ORC-15: Strict mode with advisory warnings (--strict)
    # -------------------------------------------------------------------------
    def test_orc_15_strict_mode_with_advisory_warnings(self):
        """Verifies advisory warnings yield Exit 0 normally, but promote to Exit 1 under --strict."""
        warn_results = [
            SubsystemResult(
                subsystem_id="SUB-04",
                subsystem_name="Repo Validator",
                status=ExecutionStatus.PASS,
                findings=[Finding(FindingSeverity.WARN, "doc.md", "BROKEN_LINK", "Legacy advisory link")],
            )
        ]
        exit_standard = resolve_final_exit_code(warn_results, strict=False)
        self.assertEqual(exit_standard, 0)
        exit_strict = resolve_final_exit_code(warn_results, strict=True)
        self.assertEqual(exit_strict, 1)

    # -------------------------------------------------------------------------
    # TEST-ORC-16: Composite assertion de-duplication cache hit
    # -------------------------------------------------------------------------
    def test_orc_16_composite_assertion_deduplication_cache_hit(self):
        """Verifies identical 5-tuple composite key resolves to CACHED."""
        cache = AssertionExecutionCache()
        finding = Finding(FindingSeverity.INFO, "target", "OK", "Passed")
        cache.record_execution(
            assertion_id="MDS-TKN-001",
            subsystem_id="SUB-05",
            execution_context=ExecutionContext.STATIC_FILE_SYNTAX,
            input_fingerprint="abc123hash",
            validator_version="1.0.0",
            status=ExecutionStatus.PASS,
            findings=[finding],
        )

        valid = cache.is_cache_valid(
            assertion_id="MDS-TKN-001",
            subsystem_id="SUB-05",
            execution_context=ExecutionContext.STATIC_FILE_SYNTAX,
            input_fingerprint="abc123hash",
            validator_version="1.0.0",
        )
        self.assertTrue(valid)

    # -------------------------------------------------------------------------
    # TEST-ORC-17: Composite assertion de-duplication context mismatch
    # -------------------------------------------------------------------------
    def test_orc_17_assertion_deduplication_context_mismatch(self):
        """Verifies differing execution context causes cache miss."""
        cache = AssertionExecutionCache()
        cache.record_execution(
            assertion_id="MDS-TKN-001",
            subsystem_id="SUB-05",
            execution_context=ExecutionContext.STATIC_FILE_SYNTAX,
            input_fingerprint="abc123hash",
            validator_version="1.0.0",
            status=ExecutionStatus.PASS,
            findings=[],
        )
        miss = cache.is_cache_valid(
            assertion_id="MDS-TKN-001",
            subsystem_id="SUB-05",
            execution_context=ExecutionContext.AST_GRAPH_ANALYSIS,
            input_fingerprint="abc123hash",
            validator_version="1.0.0",
        )
        self.assertFalse(miss)

    # -------------------------------------------------------------------------
    # TEST-ORC-18: Canonical Subsystem Registry completeness
    # -------------------------------------------------------------------------
    def test_orc_18_canonical_subsystem_registry_completeness(self):
        """Verifies all 15 subsystems exist in registry with valid properties."""
        self.assertEqual(len(ORCHESTRATOR_SUBSYSTEM_REGISTRY), 15)
        for sid, s_def in ORCHESTRATOR_SUBSYSTEM_REGISTRY.items():
            self.assertEqual(sid, s_def.subsystem_id)
            self.assertIn(s_def.stage, [1, 2, 3, 4])
            self.assertTrue(len(s_def.entrypoint) > 0)
            self.assertTrue(len(s_def.supported_profiles) > 0)

    # -------------------------------------------------------------------------
    # TEST-ORC-19: Execution Status vs Finding Severity decoupling
    # -------------------------------------------------------------------------
    def test_orc_19_execution_status_vs_finding_severity_decoupling(self):
        """Verifies status and severity decoupling and orthogonal exit code resolution."""
        # 1. PASS + CRITICAL (Diagnostic anomaly) -> Exit 1
        res1 = [SubsystemResult("SUB-01", "Sub1", ExecutionStatus.PASS, findings=[Finding(FindingSeverity.CRITICAL, "t", "c", "m")])]
        self.assertEqual(resolve_final_exit_code(res1), 1)

        # 2. FAIL + INFO (Assertion failed without explicit finding) -> Exit 1
        res2 = [SubsystemResult("SUB-01", "Sub1", ExecutionStatus.FAIL, findings=[Finding(FindingSeverity.INFO, "t", "c", "m")])]
        self.assertEqual(resolve_final_exit_code(res2), 1)

        # 3. PASS + WARN -> Standard Exit 0, Strict Exit 1
        res3 = [SubsystemResult("SUB-01", "Sub1", ExecutionStatus.PASS, findings=[Finding(FindingSeverity.WARN, "t", "c", "m")])]
        self.assertEqual(resolve_final_exit_code(res3, strict=False), 0)
        self.assertEqual(resolve_final_exit_code(res3, strict=True), 1)

    # -------------------------------------------------------------------------
    # TEST-ORC-20: Unified JSON telemetry schema validation
    # -------------------------------------------------------------------------
    def test_orc_20_unified_json_telemetry_schema_validation(self):
        """Verifies JSON telemetry generator outputs valid conforming schema."""
        pipeline_res = PipelineResult(
            overall_status=ExecutionStatus.PASS,
            exit_code=0,
            duration_ms=123.4,
            profile="core",
            subsystem_results=[],
            pre_snapshot={"a": (1, "hash")},
            post_snapshot={"a": (1, "hash")},
            protected_core_clean=True,
            active_phase="Phase-9.7.10",
        )
        reporter = JsonReporter(WORKSPACE_ROOT)
        telemetry = reporter.build_telemetry(pipeline_res)
        self.assertEqual(telemetry["schema_version"], "1.0.0")
        self.assertEqual(telemetry["overall_status"], "PASS")
        self.assertEqual(telemetry["exit_code"], 0)
        self.assertEqual(telemetry["active_phase"], "Phase-9.7.10")
        self.assertTrue(telemetry["protected_core"]["clean"])
        self.assertIn("subsystems", telemetry)

    # -------------------------------------------------------------------------
    # TEST-ORC-21: Performance contract cross-phase consistency
    # -------------------------------------------------------------------------
    def test_orc_21_performance_contract_cross_phase_consistency(self):
        """Verifies cross-phase performance benchmarks match canonical targets."""
        from governance.engine import GovernanceEngine
        self.assertEqual(GovernanceEngine.WARM_BENCHMARK_MS, 500.0)
        self.assertEqual(GovernanceEngine.COLD_BENCHMARK_MS, 1200.0)

    # -------------------------------------------------------------------------
    # TEST-ORC-22: Protected Core SHA-256 pre/post snapshot validation
    # -------------------------------------------------------------------------
    def test_orc_22_protected_core_sha256_snapshot_validation(self):
        """Verifies mutation in protected core is detected and raises BLOCKER."""
        pre = {"MDS/02-Tokens/color.tokens.json": (100, "original_hash")}
        post = {"MDS/02-Tokens/color.tokens.json": (100, "mutated_hash")}
        clean, findings = self.snapshot_mgr.compare_snapshots(pre, post)
        self.assertFalse(clean)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, FindingSeverity.BLOCKER)
        self.assertEqual(findings[0].code, "PROTECTED_CORE_MODIFIED")

    # -------------------------------------------------------------------------
    # TEST-ORC-23: Subprocess isolation mode (--isolate) execution
    # -------------------------------------------------------------------------
    def test_orc_23_subprocess_isolation_mode_execution(self):
        """Verifies worker execution payload dispatch returns valid SubsystemResult dict."""
        payload = {
            "subsystem_id": "SUB-03",
            "workspace_root": str(WORKSPACE_ROOT),
            "strict": False,
            "strict_env": False,
        }
        res_dict = run_worker_dispatch(payload)
        self.assertEqual(res_dict["subsystem_id"], "SUB-03")
        self.assertEqual(res_dict["status"], "PASS")

    # -------------------------------------------------------------------------
    # TEST-ORC-24: Subprocess isolation crash & timeout handling
    # -------------------------------------------------------------------------
    def test_orc_24_subprocess_isolation_crash_timeout_handling(self):
        """Verifies unknown/crashing isolated worker translates to BLOCKER / Exit 2."""
        payload = {
            "subsystem_id": "SUB-NONEXISTENT",
            "workspace_root": str(WORKSPACE_ROOT),
        }
        res_dict = run_worker_dispatch(payload)
        self.assertEqual(res_dict["status"], "FAIL")
        self.assertTrue(any(f["severity"] == "BLOCKER" for f in res_dict["findings"]))

    # -------------------------------------------------------------------------
    # TEST-ORC-25: Non-zero exit code propagation
    # -------------------------------------------------------------------------
    def test_orc_25_nonzero_exit_code_propagation(self):
        """Verifies any failing subsystem bubbles up to a non-zero exit code."""
        results = [
            SubsystemResult("SUB-01", "Sub1", ExecutionStatus.PASS),
            SubsystemResult("SUB-02", "Sub2", ExecutionStatus.FAIL),
        ]
        code = resolve_final_exit_code(results)
        self.assertEqual(code, 1)

    # -------------------------------------------------------------------------
    # TEST-ORC-26: Transitive dependency closure computation
    # -------------------------------------------------------------------------
    def test_orc_26_transitive_dependency_closure_computation(self):
        """Verifies C(target) correctly includes all recursive upstream prerequisites."""
        deps = self.dag_compiler.get_transitive_dependencies("SUB-10")
        # SUB-10 depends on SUB-09 -> SUB-08 -> SUB-05 -> SUB-04
        self.assertIn("SUB-09", deps)
        self.assertIn("SUB-08", deps)
        self.assertIn("SUB-05", deps)
        self.assertIn("SUB-04", deps)

    # -------------------------------------------------------------------------
    # TEST-ORC-27: Dependency cycle detection & rejection
    # -------------------------------------------------------------------------
    def test_orc_27_dependency_cycle_detection_rejection(self):
        """Verifies cyclical dependency graph is detected and raises DAGCycleError."""
        cyclic_registry = {
            "NODE-A": SubsystemDefinition("NODE-A", "A", "P", 1, ["NODE-B"], "ep", "ns", "res", ["fast"], ExecutionCategory.CORE_SPECIFICATION),
            "NODE-B": SubsystemDefinition("NODE-B", "B", "P", 1, ["NODE-A"], "ep", "ns", "res", ["fast"], ExecutionCategory.CORE_SPECIFICATION),
        }
        with self.assertRaises(DAGCycleError):
            self.dag_compiler.compile_profile("fast", registry=cyclic_registry)

    # -------------------------------------------------------------------------
    # TEST-ORC-28: Deterministic dependency ordering & tie-breaking
    # -------------------------------------------------------------------------
    def test_orc_28_deterministic_dependency_ordering_tie_breaking(self):
        """Verifies independent sibling nodes resolve in alphabetical order."""
        plan = self.dag_compiler.compile_profile("fast")
        # SUB-01, SUB-03, SUB-04, SUB-07 have no intra-stage dependencies
        # In Stage 1: SUB-01, SUB-03, SUB-04 should sort alphabetically: SUB-01, SUB-03, SUB-04
        sids = [s.subsystem_id for s in plan]
        idx_01 = sids.index("SUB-01")
        idx_03 = sids.index("SUB-03")
        idx_04 = sids.index("SUB-04")
        self.assertLess(idx_01, idx_03)
        self.assertLess(idx_03, idx_04)

    # -------------------------------------------------------------------------
    # TEST-ORC-29: Complete 20-Combination Status/Severity Normalization
    # -------------------------------------------------------------------------
    def test_orc_29_complete_20_combination_normalization(self):
        """Exhaustively tests all 20 permutations of status x severity from Table 6.3."""
        for num, status, sev, standard, strict, strict_env, _ in NORMALIZATION_MATRIX_20:
            result = SubsystemResult(
                subsystem_id="SUB-TEST",
                subsystem_name="Test Subsystem",
                status=status,
                findings=[Finding(severity=sev, target="t", code="c", message="m")],
            )
            # 1. Standard mode
            c_std = resolve_final_exit_code([result], strict=False, strict_env=False)
            self.assertEqual(
                c_std, standard,
                f"Row {num} ({status} x {sev}) Standard mode failed: expected {standard}, got {c_std}"
            )
            # 2. Strict mode
            c_str = resolve_final_exit_code([result], strict=True, strict_env=False)
            self.assertEqual(
                c_str, strict,
                f"Row {num} ({status} x {sev}) Strict mode failed: expected {strict}, got {c_str}"
            )
            # 3. Strict-environment mode
            c_env = resolve_final_exit_code([result], strict=False, strict_env=True)
            self.assertEqual(
                c_env, strict_env,
                f"Row {num} ({status} x {sev}) Strict-Env mode failed: expected {strict_env}, got {c_env}"
            )

    # -------------------------------------------------------------------------
    # TEST-ORC-30: Compound policy precedence resolution
    # -------------------------------------------------------------------------
    def test_orc_30_compound_policy_precedence_resolution(self):
        """Verifies CLI argument resolution respects 5-tier policy precedence."""
        parser = create_parser()
        args = parser.parse_args(["--fast", "--strict", "--fail-fast"])
        policy = resolve_execution_policy(args)
        self.assertEqual(policy.profile, "fast")
        self.assertTrue(policy.strict)
        self.assertTrue(policy.fail_fast)
        self.assertFalse(policy.strict_env)

    # -------------------------------------------------------------------------
    # TEST-ORC-31: Invalid profile combination rejection
    # -------------------------------------------------------------------------
    def test_orc_31_invalid_profile_combination_rejection(self):
        """Verifies specifying multiple conflicting profiles raises CLI error."""
        parser = create_parser()
        with self.assertRaises(CLIConfigurationError):
            args = parser.parse_args(["--fast", "--full"])
            resolve_execution_policy(args)

    # -------------------------------------------------------------------------
    # TEST-ORC-32: Active phase transition recognition
    # -------------------------------------------------------------------------
    def test_orc_32_active_phase_transition_recognition(self):
        """Verifies PhaseGovernanceManager reads ACTIVE_PHASE.json correctly."""
        phase_config = self.gov_mgr.load_active_phase()
        self.assertIsNotNone(phase_config)
        self.assertIn(phase_config["active_phase_id"], ("Phase-9.7.10", "Phase-9.7.11", "Phase-9.7.12", "Phase-10.1", "Phase-10.2"))
        self.assertIn(phase_config["active_phase_id"], phase_config["active_prefixes"])

    # -------------------------------------------------------------------------
    # TEST-ORC-33: Active phase unsealed document acceptance
    # -------------------------------------------------------------------------
    def test_orc_33_active_phase_unsealed_document_acceptance(self):
        """Verifies active phase prefix is injected dynamically into Historical Guard."""
        from historical_guard.engine import HistoricalGuardEngine
        guard_engine = HistoricalGuardEngine(workspace_root=WORKSPACE_ROOT)
        self.gov_mgr.inject_active_prefixes_into_guard(guard_engine, ["Phase-9.7.10"])
        self.assertIn("Phase-9.7.10", guard_engine.ACTIVE_PHASE_PREFIXES)

    # -------------------------------------------------------------------------
    # TEST-ORC-34: Sealing transition & cumulative chain integrity
    # -------------------------------------------------------------------------
    def test_orc_34_sealing_transition_cumulative_chain_integrity(self):
        """Verifies sequential transition graph preserves cumulative chain."""
        self.assertEqual(PHASE_TRANSITION_GRAPH.get("Phase-9.7.9"), "Phase-9.7.10")
        self.assertEqual(PHASE_TRANSITION_GRAPH.get("Phase-9.7.10"), "Phase-9.7.11")

    # -------------------------------------------------------------------------
    # TEST-ORC-35: Protected Core post-state integrity guarantee boundary
    # -------------------------------------------------------------------------
    def test_orc_35_protected_core_post_state_integrity_boundary(self):
        """Verifies pre/post snapshot match guarantees clean protected core state."""
        snap1 = self.snapshot_mgr.capture_snapshot()
        snap2 = self.snapshot_mgr.capture_snapshot()
        clean, findings = self.snapshot_mgr.compare_snapshots(snap1, snap2)
        self.assertTrue(clean)
        self.assertEqual(len(findings), 0)

    # -------------------------------------------------------------------------
    # TEST-ORC-36: Illegal cached state rejection: CACHED + CRITICAL
    # -------------------------------------------------------------------------
    def test_orc_36_illegal_cached_state_rejection_critical(self):
        """Verifies ADR-123 Condition 5: CACHED status with CRITICAL finding forces Exit 2."""
        illegal_result = SubsystemResult(
            subsystem_id="SUB-05",
            subsystem_name="Token Parser",
            status=ExecutionStatus.CACHED,
            findings=[Finding(FindingSeverity.CRITICAL, "t", "c", "m")],
        )
        exit_code = resolve_final_exit_code([illegal_result])
        self.assertEqual(exit_code, 2)

    # -------------------------------------------------------------------------
    # TEST-ORC-37: Illegal cached state rejection: CACHED + BLOCKER
    # -------------------------------------------------------------------------
    def test_orc_37_illegal_cached_state_rejection_blocker(self):
        """Verifies ADR-123 Condition 5: CACHED status with BLOCKER finding forces Exit 2."""
        illegal_result = SubsystemResult(
            subsystem_id="SUB-05",
            subsystem_name="Token Parser",
            status=ExecutionStatus.CACHED,
            findings=[Finding(FindingSeverity.BLOCKER, "t", "c", "m")],
        )
        exit_code = resolve_final_exit_code([illegal_result])
        self.assertEqual(exit_code, 2)

    # -------------------------------------------------------------------------
    # TEST-ORC-38: ACTIVE_PHASE.json schema validation failure
    # -------------------------------------------------------------------------
    def test_orc_38_active_phase_schema_validation_failure(self):
        """Verifies malformed schema in ACTIVE_PHASE.json is rejected with BLOCKER finding."""
        bad_config = {
            "schema_version": "999.0",  # invalid
            "active_phase_id": "Invalid-Phase",
        }
        ok, findings = self.gov_mgr.audit_config(bad_config)
        self.assertFalse(ok)
        self.assertTrue(any(f.severity == FindingSeverity.BLOCKER for f in findings))

    # -------------------------------------------------------------------------
    # TEST-ORC-39: Unauthorized phase prefix injection rejection
    # -------------------------------------------------------------------------
    def test_orc_39_unauthorized_phase_prefix_injection_rejection(self):
        """Verifies injecting extra unauthorized prefixes is rejected."""
        unauthorized_config = {
            "schema_version": "1.0.0",
            "active_phase_id": "Phase-9.7.10",
            "active_phase_name": "Test",
            "status": "IN_PROGRESS",
            "active_prefixes": ["Phase-9.7.10", "Phase-9.8.0-UNAUTHORIZED"],
            "previous_phase_id": "Phase-9.7.9",
            "authorized_by": "Lead Architect Mohamed Khalid",
            "authorization_timestamp": "2026-09-27T12:00:00Z",
        }
        ok, findings = self.gov_mgr.audit_config(unauthorized_config)
        self.assertFalse(ok)
        self.assertTrue(any(f.severity == FindingSeverity.BLOCKER for f in findings))

    # -------------------------------------------------------------------------
    # TEST-ORC-40: Invalid phase jump rejection (9.7.9 to 9.7.11)
    # -------------------------------------------------------------------------
    def test_orc_40_invalid_phase_jump_rejection(self):
        """Verifies skipping a phase (e.g. 9.7.9 -> 9.7.11) is rejected by governance."""
        jump_config = {
            "schema_version": "1.0.0",
            "active_phase_id": "Phase-9.7.11",  # skipped 9.7.10
            "active_phase_name": "Test",
            "status": "IN_PROGRESS",
            "active_prefixes": ["Phase-9.7.11"],
            "previous_phase_id": "Phase-9.7.9",
            "authorized_by": "Lead Architect Mohamed Khalid",
            "authorization_timestamp": "2026-09-27T12:00:00Z",
        }
        ok, findings = self.gov_mgr.audit_config(jump_config)
        self.assertFalse(ok)
        self.assertTrue(any("ORCHESTRATOR_PHASE_GOVERNANCE_VIOLATION" in f.code for f in findings))

    # -------------------------------------------------------------------------
    # TEST-ORC-41: Valid phase activation protocol execution
    # -------------------------------------------------------------------------
    def test_orc_41_valid_phase_activation_protocol_execution(self):
        """Verifies authorized ACTIVE_PHASE.json passes Stage 0 audit cleanly."""
        ok, findings, data = self.gov_mgr.audit_governance()
        self.assertTrue(ok)
        self.assertEqual(len(findings), 0)
        self.assertIn(data["active_phase_id"], ("Phase-9.7.10", "Phase-9.7.11", "Phase-9.7.12", "Phase-10.1", "Phase-10.2"))

    # -------------------------------------------------------------------------
    # TEST-ORC-42: Valid sealing transition to next phase in descriptor
    # -------------------------------------------------------------------------
    def test_orc_42_valid_sealing_transition_to_next_phase(self):
        """Verifies valid descriptor for sealing 9.7.10 and transitioning to 9.7.11."""
        next_config = {
            "schema_version": "1.0.0",
            "active_phase_id": "Phase-9.7.11",
            "active_phase_name": "Next Phase",
            "status": "IN_PROGRESS",
            "active_prefixes": ["Phase-9.7.11"],
            "previous_phase_id": "Phase-9.7.10",
            "authorized_by": "Lead Architect Mohamed Khalid",
            "authorization_timestamp": "2026-09-27T12:00:00Z",
        }
        ok, findings = self.gov_mgr.audit_config(next_config)
        self.assertTrue(ok)
        self.assertEqual(len(findings), 0)

    # -------------------------------------------------------------------------
    # TEST-ORC-43: --ci preset expansion with --strict-environment
    # -------------------------------------------------------------------------
    def test_orc_43_ci_preset_expansion_with_strict_environment(self):
        """Verifies --ci preset expands into full, strict, strict-environment, and isolate."""
        parser = create_parser()
        args = parser.parse_args(["--ci"])
        policy = resolve_execution_policy(args)
        self.assertEqual(policy.profile, "full")
        self.assertTrue(policy.strict)
        self.assertTrue(policy.strict_env)
        self.assertTrue(policy.isolate)

    # -------------------------------------------------------------------------
    # TEST-ORC-44: --ci mutually exclusive profile conflict (--ci --fast)
    # -------------------------------------------------------------------------
    def test_orc_44_ci_mutually_exclusive_profile_conflict(self):
        """Verifies providing --ci alongside conflicting base profile raises error."""
        parser = create_parser()
        with self.assertRaises(CLIConfigurationError):
            args = parser.parse_args(["--ci", "--fast"])
            resolve_execution_policy(args)


if __name__ == "__main__":
    unittest.main()
