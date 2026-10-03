"""
Master Design System (MDS) — Master Orchestrator Engine
Phase 9.7.10: Unified Local Orchestrator CLI & Master Validation Pipeline
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any

from .models import (
    ExecutionStatus,
    FindingSeverity,
    to_finding_severity,
    Finding,
    SubsystemDefinition,
    SubsystemResult,
    PipelineResult,
    ExecutionContext,
)
from .registry import ORCHESTRATOR_SUBSYSTEM_REGISTRY, MANDATORY_SAFETY_GATES
from .dag import DAGCompiler
from .cache import AssertionExecutionCache
from .snapshot import ProtectedCoreSnapshotManager
from .governance import PhaseGovernanceManager, PhaseGovernanceError
from .normalizer import resolve_final_exit_code


class OrchestratorEngine:
    """
    Executes and coordinates the four-tier validation estate of the Master Design System.
    Pure orchestrator: delegates to autonomous subsystem entrypoints.
    """

    STAGE_TIMEOUTS = {
        1: 15.0,  # Stage 1: Core Governance & Immutability (15s)
        2: 30.0,  # Stage 2: Tokens & Static Code (30s)
        3: 30.0,  # Stage 3: Components & Contracts (30s)
        4: 90.0,  # Stage 4: Live Browser & Viewports (90s)
    }

    def __init__(self, workspace_root: Optional[Path] = None):
        if workspace_root is None:
            self.workspace_root = Path(__file__).resolve().parent.parent.parent.parent
        else:
            self.workspace_root = Path(workspace_root).resolve()

        self.testing_dir = self.workspace_root / "MDS" / "10-Testing"
        # Ensure testing_dir is in sys.path
        if str(self.testing_dir) not in sys.path:
            sys.path.insert(0, str(self.testing_dir))

        self.dag_compiler = DAGCompiler()
        self.cache = AssertionExecutionCache()
        self.snapshot_manager = ProtectedCoreSnapshotManager(self.workspace_root)
        self.governance_manager = PhaseGovernanceManager(self.workspace_root)

        self.chrome_available: bool = False
        self.chrome_binary: Optional[str] = None
        self.active_phase_id: str = "Phase-9.7.10"
        self.active_prefixes: List[str] = ["Phase-9.7.10"]

    # -------------------------------------------------------------------------
    # Stage 0: Preflight & Environment Discovery
    # -------------------------------------------------------------------------
    def run_stage_0_preflight(self) -> Tuple[bool, List[Finding], Dict[str, Tuple[int, str]]]:
        """
        Executes Stage 0 preflight checks:
        1. Python runtime check (3.12+)
        2. Workspace root resolution
        3. Active phase governance audit
        4. Headless Chrome discovery
        5. Protected Core preflight cryptographic snapshot
        """
        findings: List[Finding] = []

        # 1. Python check
        if sys.version_info < (3, 12):
            findings.append(
                Finding(
                    severity=FindingSeverity.BLOCKER,
                    target="Python",
                    code="PREFLIGHT_PYTHON_VERSION",
                    message=f"Python 3.12+ required; running on {sys.version}",
                )
            )
            return False, findings, {}

        # 2. Workspace root check
        tokens_dir = self.workspace_root / "MDS" / "02-Tokens"
        if not tokens_dir.exists():
            findings.append(
                Finding(
                    severity=FindingSeverity.BLOCKER,
                    target="WorkspaceRoot",
                    code="PREFLIGHT_WORKSPACE_INVALID",
                    message=f"Workspace root does not contain MDS/02-Tokens: {self.workspace_root}",
                )
            )
            return False, findings, {}

        # 3. Active Phase Governance Audit
        ok_gov, gov_findings, gov_data = self.governance_manager.audit_governance()
        if not ok_gov or gov_findings:
            findings.extend(gov_findings)
            return False, findings, {}

        if gov_data:
            self.active_phase_id = gov_data["active_phase_id"]
            self.active_prefixes = gov_data["active_prefixes"]
            self.previous_phase_id = gov_data.get("previous_phase_id", "Phase-9.7.9")

        # 4. Chrome Discovery
        try:
            from browser.browser_discovery import BrowserDiscovery
            b_info = BrowserDiscovery.find_chrome()
            if b_info and b_info.is_available:
                self.chrome_binary = str(b_info.path)
                self.chrome_available = True
            else:
                self.chrome_binary = None
                self.chrome_available = False
        except Exception:
            self.chrome_available = False
            self.chrome_binary = None

        # 5. Protected Core Preflight Snapshot
        pre_snapshot = self.snapshot_manager.capture_snapshot()

        return True, findings, pre_snapshot

    # -------------------------------------------------------------------------
    # Direct Subsystem Execution
    # -------------------------------------------------------------------------
    def execute_subsystem_direct(
        self,
        s_def: SubsystemDefinition,
        strict: bool = False,
        strict_env: bool = False,
    ) -> SubsystemResult:
        """Executes subsystem entrypoint in-process and normalizes result."""
        start_time = time.perf_counter()
        sid = s_def.subsystem_id
        findings: List[Finding] = []
        status = ExecutionStatus.PASS
        metrics: Dict[str, Any] = {}
        assertions_run = 0
        assertions_cached = 0

        try:
            if sid == "SUB-01":
                # Historical Phase Guard
                from historical_guard.engine import HistoricalGuardEngine
                engine = HistoricalGuardEngine(workspace_root=self.workspace_root)
                # Inject active phase prefix dynamically (including transitional predecessor)
                active_and_transition = list(self.active_prefixes)
                if hasattr(self, "previous_phase_id") and self.previous_phase_id and self.previous_phase_id not in active_and_transition:
                    active_and_transition.append(self.previous_phase_id)
                PhaseGovernanceManager.inject_active_prefixes_into_guard(
                    engine, active_and_transition
                )
                h_res = engine.verify_all(strict=strict)
                status = ExecutionStatus(h_res.status)
                for hf in h_res.findings:
                    findings.append(
                        Finding(
                            severity=to_finding_severity(hf.severity),
                            target=hf.target,
                            code=hf.state.value if hasattr(hf.state, "value") else str(hf.state),
                            message=hf.reason,
                        )
                    )
                metrics["total_documents"] = h_res.total_documents
                metrics["duration_ms"] = h_res.duration_ms
                assertions_run = h_res.total_documents

            elif sid == "SUB-02":
                # Governance Invariants Engine
                from governance.engine import GovernanceEngine
                engine = GovernanceEngine(workspace_root=self.workspace_root)
                g_res = engine.audit_all(strict_mode=strict)
                if g_res.exit_code != 0:
                    status = ExecutionStatus.FAIL
                for gf in g_res.findings:
                    findings.append(
                        Finding(
                            severity=to_finding_severity(gf.severity),
                            target=gf.source_file or "governance",
                            code=gf.rule_id,
                            message=f"{gf.title}: {gf.description}",
                            line=gf.line_number,
                        )
                    )
                if g_res.telemetry:
                    metrics["wall_clock_ms"] = g_res.telemetry.wall_clock_ms
                    metrics["files_scanned"] = g_res.telemetry.files_scanned
                    metrics["nodes_count"] = g_res.telemetry.nodes_count
                    assertions_run = g_res.telemetry.nodes_count
                else:
                    assertions_run = len(g_res.findings)

            elif sid == "SUB-03":
                # Capability Registry Validator
                from registry.validator import RegistryValidator
                reg_path = self.workspace_root / "MDS" / "10-Testing" / "capabilities" / "registry.json"
                val = RegistryValidator()
                v_res = val.validate_file(reg_path)
                if not v_res.is_valid:
                    status = ExecutionStatus.FAIL
                    for err in v_res.errors:
                        findings.append(
                            Finding(
                                severity=FindingSeverity.CRITICAL,
                                target="registry.json",
                                code="REGISTRY_VIOLATION",
                                message=str(err),
                            )
                        )
                metrics.update(v_res.accounting)
                assertions_run = v_res.accounting.get("total_capabilities", 0)

            elif sid == "SUB-04":
                # Repository Structure Validator
                from static.repo_validator import RepoValidator
                val = RepoValidator(workspace_root=self.workspace_root)
                r_res = val.validate_all()
                if not r_res.is_valid:
                    status = ExecutionStatus.FAIL
                    for err in r_res.errors:
                        findings.append(
                            Finding(
                                severity=FindingSeverity.CRITICAL,
                                target="repository",
                                code="REPO_VIOLATION",
                                message=str(err),
                            )
                        )
                for warn in r_res.warnings:
                    findings.append(
                        Finding(
                            severity=FindingSeverity.WARN,
                            target="repository",
                            code="REPO_WARNING",
                            message=str(warn),
                        )
                    )
                metrics.update(r_res.metrics)
                assertions_run = len(r_res.checked_rules)

            elif sid == "SUB-05":
                # Token DTCG Parser & Schema Check
                from governance.dtcg_parser import DTCGTokenParser
                token_dir = self.workspace_root / "MDS" / "02-Tokens"
                token_graph = DTCGTokenParser.parse_tokens_directory(token_dir)
                if token_graph.unresolved_aliases or token_graph.cycles or token_graph.max_depth_exceeded:
                    status = ExecutionStatus.FAIL
                    for tok, alias in token_graph.unresolved_aliases:
                        findings.append(
                            Finding(
                                severity=FindingSeverity.CRITICAL,
                                target=tok,
                                code="UNRESOLVED_ALIAS",
                                message=f"Unresolved alias '{alias}' in token '{tok}'",
                            )
                        )
                    for cycle in token_graph.cycles:
                        findings.append(
                            Finding(
                                severity=FindingSeverity.CRITICAL,
                                target=" -> ".join(cycle),
                                code="TOKEN_CYCLE",
                                message=f"Token alias cycle detected: {cycle}",
                            )
                        )
                    for tok, depth in token_graph.max_depth_exceeded:
                        findings.append(
                            Finding(
                                severity=FindingSeverity.CRITICAL,
                                target=tok,
                                code="ALIAS_DEPTH_EXCEEDED",
                                message=f"Max alias depth exceeded: {depth} > 2 for token '{tok}'",
                            )
                        )
                metrics["total_tokens"] = len(token_graph.tokens)
                metrics["files_count"] = len(token_graph.files)
                assertions_run = len(token_graph.tokens)

            elif sid == "SUB-06":
                # Semantic CSS Scanner
                from static.css_scanner import CssAstScanner
                scanner = CssAstScanner(workspace_root=self.workspace_root)
                target_dirs = [
                    self.workspace_root / "MDS" / "Runtime",
                    self.workspace_root / "MDS" / "Playground",
                    self.workspace_root / "MDS" / "Reference-Application",
                ]
                all_results = []
                for d in target_dirs:
                    if d.exists():
                        all_results.extend(scanner.scan_directory(d))
                total_violations = 0
                for r in all_results:
                    if not r.is_valid:
                        total_violations += len(r.violations)
                        status = ExecutionStatus.FAIL
                        for v in r.violations:
                            findings.append(
                                Finding(
                                    severity=FindingSeverity.CRITICAL,
                                    target=str(v.file_path),
                                    code=v.violation_type.value,
                                    message=f"Line {v.line_number}: {v.property_name}: {v.value} -> {v.message}",
                                    line=v.line_number,
                                )
                            )
                assertions_run = len(all_results)
                metrics["total_files_scanned"] = len(all_results)
                metrics["total_violations"] = total_violations

            elif sid == "SUB-07":
                # DSSE Mathematical Harness
                import test_dsse
                import io
                import contextlib
                suite = test_dsse.DSSETestSuite()
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    ret = suite.run_all()
                assertions_run = suite.passed + suite.failed
                if ret != 0 or suite.failed > 0:
                    status = ExecutionStatus.FAIL
                    for name, st, details in suite.tests:
                        if st == "FAIL":
                            findings.append(
                                Finding(
                                    severity=FindingSeverity.CRITICAL,
                                    target=name,
                                    code="DSSE_ASSERTION_FAIL",
                                    message=details or name,
                                )
                            )
                metrics["passed"] = suite.passed
                metrics["failed"] = suite.failed

            elif sid in ("SUB-08", "SUB-09", "SUB-10", "SUB-11"):
                # Component & Primitive Contracts
                import run_tests
                import io
                import contextlib
                runner_inst = run_tests.MDSTestRunner()
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    if sid == "SUB-08":
                        runner_inst.run_primitive_tests()
                    elif sid == "SUB-09":
                        runner_inst.run_component_tests()
                    elif sid == "SUB-10":
                        runner_inst.run_pattern_tests()
                    elif sid == "SUB-11":
                        runner_inst.run_workflow_tests()

                assertions_run = len(runner_inst.results)
                if runner_inst.failed > 0:
                    status = ExecutionStatus.FAIL
                    for r in runner_inst.results:
                        if r["status"] == "FAIL":
                            findings.append(
                                Finding(
                                    severity=FindingSeverity.CRITICAL,
                                    target=r["id"],
                                    code="CONTRACT_INVARIANT_FAILURE",
                                    message=r.get("details") or r["description"],
                                )
                            )
                metrics["passed"] = runner_inst.passed
                metrics["failed"] = runner_inst.failed

            elif sid == "SUB-12":
                # Browser Discovery & Local Server
                if not self.chrome_available:
                    status = ExecutionStatus.DEFERRED
                    findings.append(
                        Finding(
                            severity=FindingSeverity.INFO,
                            target="Chrome",
                            code="BROWSER_UNAVAILABLE",
                            message="Google Chrome/Chromium headless binary not found on host",
                        )
                    )
                else:
                    status = ExecutionStatus.PASS
                    metrics["chrome_binary"] = self.chrome_binary
                    assertions_run = 1

            elif sid in ("SUB-13", "SUB-14", "SUB-15"):
                # Live dynamic browser tests
                if not self.chrome_available:
                    status = ExecutionStatus.DEFERRED
                    findings.append(
                        Finding(
                            severity=FindingSeverity.INFO,
                            target=sid,
                            code="DYNAMIC_TEST_DEFERRED",
                            message=f"Live test {sid} deferred: Headless Chrome unavailable",
                        )
                    )
                else:
                    if sid == "SUB-13":
                        from accessibility.accessibility_dispatch import AccessibilityDispatcher
                        from browser.models import BrowserExecutionStatus
                        disp = AccessibilityDispatcher(workspace_root=self.workspace_root)
                        a_res = disp.run_audit()
                        if a_res.status == BrowserExecutionStatus.FAIL:
                            status = ExecutionStatus.FAIL
                            findings.append(
                                Finding(
                                    severity=FindingSeverity.CRITICAL,
                                    target="SUB-13",
                                    code="A11Y_AUDIT_FAIL",
                                    message=a_res.error_message or f"{a_res.violation_count} axe violations found",
                                )
                            )
                        elif a_res.status == BrowserExecutionStatus.DEFERRED:
                            status = ExecutionStatus.DEFERRED
                        else:
                            status = ExecutionStatus.PASS
                        metrics["violation_count"] = a_res.violation_count
                        metrics["pass_count"] = a_res.pass_count
                        assertions_run = a_res.pass_count + a_res.violation_count

                    elif sid == "SUB-14":
                        from responsive.responsive_dispatch import ResponsiveDispatcher
                        from browser.models import BrowserExecutionStatus
                        disp = ResponsiveDispatcher(workspace_root=self.workspace_root)
                        r_res = disp.run_matrix()
                        if r_res.status == BrowserExecutionStatus.FAIL:
                            status = ExecutionStatus.FAIL
                            findings.append(
                                Finding(
                                    severity=FindingSeverity.CRITICAL,
                                    target="SUB-14",
                                    code="RESPONSIVE_AUDIT_FAIL",
                                    message=r_res.error_message or "Responsive matrix failures detected",
                                )
                            )
                        elif r_res.status == BrowserExecutionStatus.DEFERRED:
                            status = ExecutionStatus.DEFERRED
                        else:
                            status = ExecutionStatus.PASS
                        metrics["viewports_tested"] = len(r_res.runs)
                        assertions_run = len(r_res.runs)

                    elif sid == "SUB-15":
                        from visual.visual_dispatch import VisualDispatcher
                        from visual.visual_models import VisualExecutionStatus
                        disp = VisualDispatcher(workspace_root=self.workspace_root)
                        v_res = disp.run_sweep()
                        if v_res.status == VisualExecutionStatus.FAIL:
                            status = ExecutionStatus.FAIL
                            findings.append(
                                Finding(
                                    severity=FindingSeverity.CRITICAL,
                                    target="SUB-15",
                                    code="VISUAL_DIFF_FAIL",
                                    message=v_res.error_message or f"{v_res.failed_baselines} visual mismatches detected",
                                )
                            )
                        elif v_res.status == VisualExecutionStatus.DEFERRED:
                            status = ExecutionStatus.DEFERRED
                        else:
                            status = ExecutionStatus.PASS
                        metrics["total_baselines"] = v_res.total_baselines
                        metrics["passed_baselines"] = v_res.passed_baselines
                        metrics["failed_baselines"] = v_res.failed_baselines
                        assertions_run = v_res.total_baselines

        except Exception as exc:
            status = ExecutionStatus.FAIL
            findings.append(
                Finding(
                    severity=FindingSeverity.BLOCKER,
                    target=sid,
                    code="SUBSYSTEM_EXECUTION_EXCEPTION",
                    message=f"Subsystem {sid} raised unhandled exception: {exc}",
                )
            )

        duration_ms = (time.perf_counter() - start_time) * 1000
        return SubsystemResult(
            subsystem_id=sid,
            subsystem_name=s_def.subsystem_name,
            status=status,
            duration_ms=duration_ms,
            findings=findings,
            metrics=metrics,
            assertions_run=assertions_run,
            assertions_cached=assertions_cached,
        )

    # -------------------------------------------------------------------------
    # Subprocess Isolation Execution (--isolate)
    # -------------------------------------------------------------------------
    def execute_subsystem_isolated(
        self,
        s_def: SubsystemDefinition,
        strict: bool = False,
        strict_env: bool = False,
    ) -> SubsystemResult:
        """Spawns child worker subprocess and exchanges JSON stream via stdin/stdout."""
        start_time = time.perf_counter()
        sid = s_def.subsystem_id
        timeout_sec = self.STAGE_TIMEOUTS.get(s_def.stage, 30.0)

        payload = {
            "subsystem_id": sid,
            "workspace_root": str(self.workspace_root),
            "strict": strict,
            "strict_env": strict_env,
        }

        cmd = [
            sys.executable,
            "-m",
            "orchestrator.worker",
            "--subsystem",
            sid,
        ]

        try:
            proc = subprocess.run(
                cmd,
                input=json.dumps(payload) + "\n",
                text=True,
                capture_output=True,
                timeout=timeout_sec,
                cwd=str(self.testing_dir),
            )
        except subprocess.TimeoutExpired:
            return SubsystemResult(
                subsystem_id=sid,
                subsystem_name=s_def.subsystem_name,
                status=ExecutionStatus.FAIL,
                duration_ms=timeout_sec * 1000,
                findings=[
                    Finding(
                        severity=FindingSeverity.BLOCKER,
                        target=sid,
                        code="SUBPROCESS_TIMEOUT",
                        message=f"Subsystem {sid} timed out after {timeout_sec}s",
                    )
                ],
            )
        except Exception as exc:
            return SubsystemResult(
                subsystem_id=sid,
                subsystem_name=s_def.subsystem_name,
                status=ExecutionStatus.FAIL,
                duration_ms=(time.perf_counter() - start_time) * 1000,
                findings=[
                    Finding(
                        severity=FindingSeverity.BLOCKER,
                        target=sid,
                        code="SUBPROCESS_SPAWN_ERROR",
                        message=f"Failed to spawn isolated subprocess: {exc}",
                    )
                ],
            )

        # Parse worker JSON from stdout
        raw_stdout = proc.stdout.strip()
        if raw_stdout:
            try:
                data = json.loads(raw_stdout)
                return SubsystemResult.from_dict(data)
            except Exception:
                pass

        # If child exited abnormally without valid JSON
        duration_ms = (time.perf_counter() - start_time) * 1000
        return SubsystemResult(
            subsystem_id=sid,
            subsystem_name=s_def.subsystem_name,
            status=ExecutionStatus.FAIL,
            duration_ms=duration_ms,
            findings=[
                Finding(
                    severity=FindingSeverity.BLOCKER,
                    target=sid,
                    code="SUBPROCESS_CRASH",
                    message=f"Worker process exited with code {proc.returncode}: {proc.stderr[:300]}",
                )
            ],
        )

    # -------------------------------------------------------------------------
    # Master Pipeline Execution
    # -------------------------------------------------------------------------
    def run_pipeline(
        self,
        profile: str = "core",
        subsystem: Optional[str] = None,
        strict: bool = False,
        strict_env: bool = False,
        fail_fast: bool = False,
        isolate: bool = False,
    ) -> PipelineResult:
        """Executes full orchestrated validation pipeline."""
        start_time = time.perf_counter()
        all_results: List[SubsystemResult] = []
        all_findings: List[Finding] = []

        # Stage 0: Preflight
        ok_pre, pre_findings, pre_snapshot = self.run_stage_0_preflight()
        all_findings.extend(pre_findings)

        if not ok_pre:
            duration_ms = (time.perf_counter() - start_time) * 1000
            exit_code = 2
            return PipelineResult(
                overall_status=ExecutionStatus.FAIL,
                exit_code=exit_code,
                duration_ms=duration_ms,
                profile=profile,
                subsystem_results=[],
                pre_snapshot={},
                post_snapshot={},
                protected_core_clean=True,
                active_phase=self.active_phase_id,
                all_findings=all_findings,
            )

        # Compile DAG execution plan
        try:
            plan = self.dag_compiler.compile_profile(profile, target_subsystem=subsystem)
        except Exception as dag_err:
            all_findings.append(
                Finding(
                    severity=FindingSeverity.BLOCKER,
                    target="DAGCompiler",
                    code="DAG_COMPILATION_ERROR",
                    message=str(dag_err),
                )
            )
            duration_ms = (time.perf_counter() - start_time) * 1000
            return PipelineResult(
                overall_status=ExecutionStatus.FAIL,
                exit_code=2,
                duration_ms=duration_ms,
                profile=profile,
                subsystem_results=[],
                pre_snapshot=pre_snapshot,
                post_snapshot={},
                protected_core_clean=True,
                active_phase=self.active_phase_id,
                all_findings=all_findings,
            )

        # Execute scheduled subsystems
        for s_def in plan:
            # Check fail-fast condition
            if fail_fast and any(
                f.severity in (FindingSeverity.CRITICAL, FindingSeverity.BLOCKER)
                for f in all_findings
            ):
                all_results.append(
                    SubsystemResult(
                        subsystem_id=s_def.subsystem_id,
                        subsystem_name=s_def.subsystem_name,
                        status=ExecutionStatus.SKIPPED,
                    )
                )
                continue

            # Determine whether to isolate
            should_isolate = isolate and (s_def.stage == 4 or "dynamic" in s_def.execution_category.value.lower())

            if should_isolate:
                s_res = self.execute_subsystem_isolated(
                    s_def, strict=strict, strict_env=strict_env
                )
            else:
                s_res = self.execute_subsystem_direct(
                    s_def, strict=strict, strict_env=strict_env
                )

            all_results.append(s_res)
            all_findings.extend(s_res.findings)

            # Stage 1 Blocker abort
            if s_def.stage == 1:
                has_blocker = any(
                    f.severity == FindingSeverity.BLOCKER for f in s_res.findings
                )
                if has_blocker:
                    break

        # Postflight Protected Core Snapshot & Delta Audit
        post_snapshot = self.snapshot_manager.capture_snapshot()
        core_clean, core_findings = self.snapshot_manager.compare_snapshots(
            pre_snapshot, post_snapshot
        )
        all_findings.extend(core_findings)

        # Resolve Final Exit Code & Overall Status
        exit_code = resolve_final_exit_code(
            all_results, strict=strict, strict_env=strict_env
        )

        # If core mutated, force Exit 2
        if not core_clean:
            exit_code = 2

        if exit_code == 0:
            overall_status = ExecutionStatus.PASS
            if any(r.status == ExecutionStatus.DEFERRED for r in all_results):
                overall_status = ExecutionStatus.DEFERRED
        else:
            overall_status = ExecutionStatus.FAIL

        duration_ms = (time.perf_counter() - start_time) * 1000
        return PipelineResult(
            overall_status=overall_status,
            exit_code=exit_code,
            duration_ms=duration_ms,
            profile=profile,
            subsystem_results=all_results,
            pre_snapshot=pre_snapshot,
            post_snapshot=post_snapshot,
            protected_core_clean=core_clean,
            active_phase=self.active_phase_id,
            all_findings=all_findings,
        )
