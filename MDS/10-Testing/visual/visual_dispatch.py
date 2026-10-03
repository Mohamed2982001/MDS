#!/usr/bin/env python3
"""
MDS Visual Capability Dispatcher
Phase 9.7.7: Visual Regression Engine & Snapshot Diffing
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Provides the master execution entrypoint for capability MDS-VIS-001,
orchestrating font verification, live capture, baseline comparison,
and evidence generation.
"""

import sys
import time
from typing import Optional, Dict, Any, List
from pathlib import Path

# Ensure 10-Testing is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from browser.cdp_driver import CDPBrowserDriver
from browser.local_server import LocalTestServer
from browser.models import BrowserCapabilityResult, BrowserExecutionStatus

try:
    from .visual_models import (
        VisualExecutionStatus,
        VisualSweepResult,
        ComparisonResult,
        ComparisonMetrics
    )
    from .baseline_manager import BaselineManager, BaselineIntegrityError, FontArtifactUnavailableError
    from .visual_runner import VisualRunner
    from .visual_comparator import VisualComparator
    from .evidence_generator import VisualEvidenceGenerator
except (ImportError, ValueError):
    from visual.visual_models import (
        VisualExecutionStatus,
        VisualSweepResult,
        ComparisonResult,
        ComparisonMetrics
    )
    from visual.baseline_manager import BaselineManager, BaselineIntegrityError, FontArtifactUnavailableError
    from visual.visual_runner import VisualRunner
    from visual.visual_comparator import VisualComparator
    from visual.evidence_generator import VisualEvidenceGenerator


class VisualDispatcher:
    """
    Coordinates execution of visual regression checks and integrates
    directly with the MDS Capability Registry and Master Test Harness.
    """

    CAPABILITY_ID = "MDS-VIS-001"

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(__file__).resolve().parent.parent.parent.parent
        self.baseline_manager = BaselineManager(workspace_root=self.workspace_root)
        self.runner = VisualRunner(workspace_root=self.workspace_root)
        self.comparator = VisualComparator()
        self.evidence_gen = VisualEvidenceGenerator(workspace_root=self.workspace_root)

    def run_sweep(
        self,
        capability_id: str = CAPABILITY_ID,
        baseline_ids: Optional[List[str]] = None
    ) -> VisualSweepResult:
        """
        Executes the canonical visual regression sweep across specified baselines
        (defaults to all 12 canonical baselines).
        """
        start_time = time.perf_counter()
        target_ids = baseline_ids or self.baseline_manager.CANONICAL_BASELINE_IDS

        sweep_result = VisualSweepResult(
            capability_id=capability_id,
            total_baselines=len(target_ids)
        )

        # 1. Verify Browser Availability
        if not self.runner.is_browser_available:
            sweep_result.status = VisualExecutionStatus.DEFERRED
            sweep_result.error_message = "No Chromium-compatible browser binary (Chrome/Edge/Chromium) found."
            sweep_result.deferred_baselines = len(target_ids)
            return sweep_result

        # 2. Verify Deterministic Font Artifacts
        is_font_valid, font_msg, font_telemetry = self.baseline_manager.verify_fonts()
        if not is_font_valid:
            sweep_result.status = VisualExecutionStatus.DEFERRED
            sweep_result.error_message = font_msg
            sweep_result.deferred_baselines = len(target_ids)
            return sweep_result

        # 3. Execute Visual Sweeps inside CDP Browser Session
        server = LocalTestServer(serve_dir=self.workspace_root)
        server.start()

        results: List[ComparisonResult] = []
        try:
            with CDPBrowserDriver(browser_info=self.runner.preferred_browser) as driver:
                driver.launch(headless=True)

                for b_id in target_ids:
                    config = self.baseline_manager.get_baseline_config(b_id)
                    if not config:
                        results.append(ComparisonResult(
                            baseline_id=b_id,
                            status=VisualExecutionStatus.ERROR,
                            metrics=ComparisonMetrics(),
                            error_message=f"Configuration missing for baseline {b_id}"
                        ))
                        continue

                    # Check baseline image on disk
                    try:
                        baseline_png = self.baseline_manager.get_baseline_image(b_id)
                    except FileNotFoundError as fnf:
                        results.append(ComparisonResult(
                            baseline_id=b_id,
                            status=VisualExecutionStatus.DEFERRED,
                            metrics=ComparisonMetrics(),
                            error_message=f"BASELINE_MISSING: {fnf}"
                        ))
                        continue
                    except BaselineIntegrityError as bie:
                        results.append(ComparisonResult(
                            baseline_id=b_id,
                            status=VisualExecutionStatus.FAIL,
                            metrics=ComparisonMetrics(),
                            error_message=f"BASELINE_INTEGRITY_FAILED: {bie}"
                        ))
                        continue

                    # Capture live snapshot
                    try:
                        actual_png = self.runner.capture_baseline_snapshot(driver, server, config)
                    except Exception as ce:
                        results.append(ComparisonResult(
                            baseline_id=b_id,
                            status=VisualExecutionStatus.ERROR,
                            metrics=ComparisonMetrics(),
                            error_message=f"CAPTURE_FAILED: {ce}"
                        ))
                        continue

                    # Evaluate comparison
                    diff_output_path = (
                        self.evidence_gen.artifacts_dir / f"{b_id}_diff.png"
                    )
                    eval_result = self.comparator.evaluate(
                        baseline_png=baseline_png,
                        actual_png=actual_png,
                        baseline_id=b_id,
                        output_diff_path=diff_output_path
                    )
                    eval_result.evidence["theme"] = config.theme
                    eval_result.evidence["viewport"] = f"{config.width}x{config.height}"
                    eval_result.evidence["direction"] = config.direction
                    eval_result.evidence["density"] = config.density
                    results.append(eval_result)

        finally:
            server.stop()

        sweep_result.results = results
        sweep_result.passed_baselines = sum(1 for r in results if r.status == VisualExecutionStatus.PASS)
        sweep_result.failed_baselines = sum(1 for r in results if r.status in (VisualExecutionStatus.FAIL, VisualExecutionStatus.ERROR))
        sweep_result.deferred_baselines = sum(1 for r in results if r.status == VisualExecutionStatus.DEFERRED)
        sweep_result.total_duration_ms = (time.perf_counter() - start_time) * 1000.0

        if sweep_result.failed_baselines > 0:
            sweep_result.status = VisualExecutionStatus.FAIL
            sweep_result.error_message = f"{sweep_result.failed_baselines} baselines failed visual comparison."
        elif sweep_result.deferred_baselines > 0:
            sweep_result.status = VisualExecutionStatus.DEFERRED
            sweep_result.error_message = f"{sweep_result.deferred_baselines} baselines deferred."
        else:
            sweep_result.status = VisualExecutionStatus.PASS

        # Persist structured evidence
        self.evidence_gen.save_evidence(sweep_result)
        return sweep_result

    def to_browser_capability_result(self, sweep_res: VisualSweepResult) -> BrowserCapabilityResult:
        """Translates VisualSweepResult into the standard BrowserCapabilityResult."""
        status_map = {
            VisualExecutionStatus.PASS: BrowserExecutionStatus.PASS,
            VisualExecutionStatus.FAIL: BrowserExecutionStatus.FAIL,
            VisualExecutionStatus.DEFERRED: BrowserExecutionStatus.DEFERRED,
            VisualExecutionStatus.ERROR: BrowserExecutionStatus.FAIL
        }
        return BrowserCapabilityResult(
            capability_id=sweep_res.capability_id,
            status=status_map.get(sweep_res.status, BrowserExecutionStatus.FAIL),
            duration_ms=sweep_res.total_duration_ms,
            evidence=sweep_res.to_dict(),
            error_message=sweep_res.error_message
        )

    def to_execution_result(self, sweep_res: VisualSweepResult) -> Any:
        """Translates VisualSweepResult into Master Harness ExecutionResult."""
        try:
            from static.dispatch_adapter import ExecutionResult, ExecutionStatus
        except ImportError:
            from ..static.dispatch_adapter import ExecutionResult, ExecutionStatus

        status_map = {
            VisualExecutionStatus.PASS: ExecutionStatus.PASS,
            VisualExecutionStatus.FAIL: ExecutionStatus.FAIL,
            VisualExecutionStatus.DEFERRED: ExecutionStatus.DEFERRED,
            VisualExecutionStatus.ERROR: ExecutionStatus.FAIL,
        }
        details = (
            f"12-Baseline Visual Sweep: {sweep_res.passed_baselines}/{sweep_res.total_baselines} passed, "
            f"max_diff_ratio={sweep_res.max_diff_ratio:.6f} in {sweep_res.total_duration_ms:.1f}ms"
        )
        if sweep_res.error_message:
            details = f"{details} — {sweep_res.error_message}"

        return ExecutionResult(
            capability_id=sweep_res.capability_id,
            status=status_map.get(sweep_res.status, ExecutionStatus.FAIL),
            details=details,
            duration_ms=sweep_res.total_duration_ms,
        )


def run_visual_capability(session: Optional[Any] = None) -> VisualSweepResult:
    """Standard entrypoint callable by Master Test Harness and Dispatch Adapter."""
    dispatcher = VisualDispatcher()
    return dispatcher.run_sweep()

