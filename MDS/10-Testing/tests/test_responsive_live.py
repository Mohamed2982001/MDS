#!/usr/bin/env python3
"""
Live Real-Browser Integration Tests for MDS Responsive Viewport Automation Engine
Phase 9.7.6: Responsive Viewport Automation (Layer K)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Executes live tests on Google Chrome (v153+) against the live Reference Application:
1. Canonical Viewport sweeps (320px, 768px, 1024px, 1440px)
2. Canonical 17-Run Deterministic Execution Matrix
3. Bi-directional RTL/LTR symmetry
4. Touch target compliance under Compact density
5. High Contrast theme stability
6. Deliberate failure detection against broken fixture
"""

import sys
import unittest
from pathlib import Path

TESTING_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = TESTING_DIR.parent.parent
sys.path.insert(0, str(TESTING_DIR))

from browser.browser_discovery import BrowserDiscovery
from browser.session import BrowserSession
from responsive.responsive_models import (
    AssertionClass,
    ResponsiveMatrixResult,
    ResponsiveRunResult,
)
from responsive.viewport_matrix import (
    VP_320,
    VP_768,
    VP_1024,
    VP_1440,
    get_run_config_by_id,
    get_canonical_matrix,
)
from responsive.responsive_runner import ResponsiveRunner
from responsive.responsive_dispatch import ResponsiveDispatcher
from responsive.evidence import ResponsiveEvidenceGenerator


class TestResponsiveEngineLive(unittest.TestCase):
    """Live browser tests against real Chromium and Reference Application."""

    @classmethod
    def setUpClass(cls):
        cls.browser = BrowserDiscovery.get_preferred()
        if not cls.browser or not cls.browser.is_available:
            raise unittest.SkipTest("No Chromium-compatible browser binary found on host system.")
        cls.workspace_root = WORKSPACE_ROOT
        cls.ref_app_path = "MDS/Reference-Application/index.html"
        cls.broken_fixture_path = "MDS/10-Testing/responsive/fixtures/broken_responsive.html"

    # -------------------------------------------------------------------------
    # 1. Live Single-Run Viewport Verification
    # -------------------------------------------------------------------------
    def test_01_live_mobile_320_overview(self):
        """Live verification of RWD-RUN-001 (Overview @ 320px mobile)."""
        cfg = get_run_config_by_id("RWD-RUN-001")
        self.assertIsNotNone(cfg)

        with BrowserSession(
            serve_dir=self.workspace_root,
            browser_info=self.browser,
            headless=True
        ) as session:
            session.driver.navigate(session.server.get_url(self.ref_app_path))
            session.driver.wait_for("body")

            runner = ResponsiveRunner()
            run_result = runner.execute_run(session.driver, cfg)

            self.assertTrue(run_result.passed, f"Run 001 failed: {run_result.error_message}")
            self.assertEqual(len(run_result.hard_failures), 0)

            # Check individual hard contracts
            btn_assert = next((a for a in run_result.assertions if a.selector == "#btn-mobile-nav"), None)
            self.assertIsNotNone(btn_assert)
            self.assertTrue(btn_assert.passed, "Mobile toggle button must be visible at 320px")

            side_assert = next((a for a in run_result.assertions if a.selector == ".mds-ref-sidebar"), None)
            self.assertIsNotNone(side_assert)
            self.assertTrue(side_assert.passed, "Sidebar must be hidden at 320px")

    def test_02_live_tablet_768_overview(self):
        """Live verification of RWD-RUN-002 (Overview @ 768px tablet)."""
        cfg = get_run_config_by_id("RWD-RUN-002")
        self.assertIsNotNone(cfg)

        with BrowserSession(
            serve_dir=self.workspace_root,
            browser_info=self.browser,
            headless=True
        ) as session:
            session.driver.navigate(session.server.get_url(self.ref_app_path))
            session.driver.wait_for("body")

            runner = ResponsiveRunner()
            run_result = runner.execute_run(session.driver, cfg)

            self.assertTrue(run_result.passed, f"Run 002 failed: {run_result.error_message}")
            self.assertEqual(len(run_result.hard_failures), 0)

            # Check tablet 72px rail
            rail_assert = next((a for a in run_result.assertions if a.selector == ".mds-ref-sidebar"), None)
            self.assertIsNotNone(rail_assert)
            self.assertTrue(rail_assert.passed, "Sidebar must collapse to 72px rail at 768px")

    def test_03_live_desktop_1024_overview(self):
        """Live verification of RWD-RUN-003 (Overview @ 1024px desktop)."""
        cfg = get_run_config_by_id("RWD-RUN-003")
        self.assertIsNotNone(cfg)

        with BrowserSession(
            serve_dir=self.workspace_root,
            browser_info=self.browser,
            headless=True
        ) as session:
            session.driver.navigate(session.server.get_url(self.ref_app_path))
            session.driver.wait_for("body")

            runner = ResponsiveRunner()
            run_result = runner.execute_run(session.driver, cfg)

            self.assertTrue(run_result.passed, f"Run 003 failed: {run_result.error_message}")
            self.assertEqual(len(run_result.hard_failures), 0)

    def test_04_live_wide_1440_overview(self):
        """Live verification of RWD-RUN-004 (Overview @ 1440px wide)."""
        cfg = get_run_config_by_id("RWD-RUN-004")
        self.assertIsNotNone(cfg)

        with BrowserSession(
            serve_dir=self.workspace_root,
            browser_info=self.browser,
            headless=True
        ) as session:
            session.driver.navigate(session.server.get_url(self.ref_app_path))
            session.driver.wait_for("body")

            runner = ResponsiveRunner()
            run_result = runner.execute_run(session.driver, cfg)

            self.assertTrue(run_result.passed, f"Run 004 failed: {run_result.error_message}")
            self.assertEqual(len(run_result.hard_failures), 0)

    # -------------------------------------------------------------------------
    # 2. Live Full 17-Run Matrix Execution
    # -------------------------------------------------------------------------
    def test_05_live_full_17_run_matrix(self):
        """Live execution of the complete Canonical 17-Run Matrix."""
        disp = ResponsiveDispatcher(workspace_root=self.workspace_root)
        matrix_res = disp.run_matrix(target_path=self.ref_app_path)

        self.assertEqual(matrix_res.status, "PASS", f"Matrix failed: {matrix_res.error_message}")
        self.assertEqual(matrix_res.hard_failures, 0, f"Found {matrix_res.hard_failures} hard failure(s)")
        self.assertEqual(len(matrix_res.runs), 17, "Expected exactly 17 completed runs")
        self.assertGreater(matrix_res.total_assertions, 50, "Expected >50 evaluated assertions across 17 runs")

        # Verify evidence artifact was written
        evidence_file = TESTING_DIR / "artifacts" / "responsive_evidence.json"
        self.assertTrue(evidence_file.exists(), "Evidence file must be written to artifacts/responsive_evidence.json")

    # -------------------------------------------------------------------------
    # 3. Deliberate Failure Detection against Broken Fixture
    # -------------------------------------------------------------------------
    def test_06_live_broken_fixture_detects_blowout(self):
        """Verifies that deliberate blowout and small buttons fail the runner."""
        cfg = get_run_config_by_id("RWD-RUN-001")
        self.assertIsNotNone(cfg)

        with BrowserSession(
            serve_dir=self.workspace_root,
            browser_info=self.browser,
            headless=True
        ) as session:
            session.driver.navigate(session.server.get_url(self.broken_fixture_path))
            session.driver.wait_for("body")

            runner = ResponsiveRunner()
            run_result = runner.execute_run(session.driver, cfg)

            # Must fail due to:
            # 1. 1600px blowout
            # 2. Touch targets < 44px
            # 3. 1280px forbidden container
            self.assertFalse(run_result.passed, "Broken fixture must NOT pass responsive evaluation")
            self.assertGreater(len(run_result.hard_failures), 0, "Broken fixture must yield hard failure(s)")

    # -------------------------------------------------------------------------
    # 4. Live End-to-End Pipeline: Registry -> Dispatch -> Real Chrome -> Result
    # -------------------------------------------------------------------------
    def test_07_live_e2e_registry_dispatch_browser_pipeline(self):
        """
        Live verification of the complete architectural pipeline (Finding 3):
        registry.json
          -> CapabilityDispatcher
          -> BrowserCapabilityDispatcher
          -> ResponsiveDispatcher
          -> CDPBrowserDriver
          -> real Chrome
          -> 17-run matrix
          -> structured result
        """
        import json
        from static.dispatch_adapter import CapabilityDispatcher, ExecutionStatus
        from browser.dispatch_integration import BrowserCapabilityDispatcher
        from browser.models import BrowserExecutionStatus

        # 1. Registry Lookup
        registry_file = TESTING_DIR / "capabilities" / "registry.json"
        self.assertTrue(registry_file.exists(), "Registry file must exist")
        with open(registry_file, "r", encoding="utf-8") as f:
            registry_data = json.load(f)

        cap_meta = next((c for c in registry_data["capabilities"] if c["id"] == "MDS-RWD-003"), None)
        self.assertIsNotNone(cap_meta, "MDS-RWD-003 must be registered in registry.json")
        self.assertEqual(cap_meta["status"], "ACTIVE")
        self.assertEqual(cap_meta["execution"], "BROWSER_AUTOMATION")
        self.assertIsNone(cap_meta["deferred_reason"])

        # 2. CapabilityDispatcher Resolution
        cap_dispatcher = CapabilityDispatcher(workspace_root=self.workspace_root)
        resolved_ok, msg, runner_target = cap_dispatcher.resolve_runner("MDS-RWD-003")
        self.assertTrue(resolved_ok, f"CapabilityDispatcher must resolve MDS-RWD-003: {msg}")

        # 3. BrowserCapabilityDispatcher Execution on Real Chrome
        browser_dispatcher = BrowserCapabilityDispatcher(workspace_root=self.workspace_root)
        self.assertTrue(browser_dispatcher.is_browser_available, "Real Chrome browser must be available")

        browser_result = browser_dispatcher.execute_browser_capability("MDS-RWD-003")

        # 4. Assertions Required by Audit Finding 3
        self.assertEqual(browser_result.capability_id, "MDS-RWD-003")
        self.assertEqual(browser_result.status, BrowserExecutionStatus.PASS)
        self.assertGreater(browser_result.duration_ms, 0.0, "Real browser execution duration must be > 0ms")

        # Extract structured evidence
        evidence = browser_result.evidence
        self.assertIsInstance(evidence, dict, "Evidence must be a dictionary")
        accounting = evidence.get("accounting", {})
        runs = evidence.get("runs", [])

        self.assertEqual(len(runs), 17, f"Expected exactly 17 runs, got {len(runs)}")
        self.assertEqual(accounting.get("total_runs"), 17)
        self.assertEqual(accounting.get("hard_failures"), 0, "Hard failures must be 0")
        self.assertEqual(accounting.get("failed_assertions"), 0, "Failed assertions must be 0")
        self.assertEqual(accounting.get("passed_assertions"), accounting.get("total_assertions"))

        # 5. Translation to standard ExecutionResult
        exec_result = browser_dispatcher.to_execution_result(browser_result)
        self.assertEqual(exec_result.capability_id, "MDS-RWD-003")
        self.assertEqual(exec_result.status, ExecutionStatus.PASS)


if __name__ == "__main__":
    unittest.main()

