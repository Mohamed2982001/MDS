#!/usr/bin/env python3
"""
Live Browser Integration Tests for Dynamic Accessibility Automation
Phase 9.7.5: Dynamic Accessibility Automation (Layer I)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Executes real axe-core accessibility auditing inside headless Google Chrome / Chromium
against accessible baseline fixtures, deliberately inaccessible fixtures,
and actual locked MDS application surfaces.
"""

import os
import sys
import unittest
from pathlib import Path

# Ensure MDS/10-Testing is on sys.path
TESTING_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TESTING_DIR))

from browser.models import BrowserExecutionStatus, Viewport
from browser.browser_discovery import BrowserDiscovery
from browser.local_server import LocalTestServer
from browser.cdp_driver import CDPBrowserDriver
from browser.session import BrowserSession
from browser.dispatch_integration import BrowserCapabilityDispatcher

from accessibility.accessibility_models import (
    AccessibilityPolicy,
    AccessibilityResult,
    AccessibilityImpact,
)
from accessibility.axe_loader import AxeLoader
from accessibility.axe_runner import AxeRunner
from accessibility.accessibility_dispatch import AccessibilityDispatcher
from accessibility.evidence import AccessibilityEvidenceGenerator
from static.dispatch_adapter import CapabilityDispatcher, ExecutionStatus


class TestAccessibilityLive(unittest.TestCase):
    """Category B: Real Browser Live Accessibility Auditing Tests on Google Chrome."""

    @classmethod
    def setUpClass(cls):
        cls.preferred_browser = BrowserDiscovery.get_preferred()
        if not cls.preferred_browser or not cls.preferred_browser.is_available:
            raise unittest.SkipTest("Skipping Category B: No Chromium browser available on host.")

        if not AxeLoader.is_artifact_available():
            raise unittest.SkipTest("Skipping Category B: Pinned axe-core artifact not available.")

        # Start shared local HTTP server serving workspace
        cls.workspace_root = TESTING_DIR.parent.parent
        cls.server = LocalTestServer(serve_dir=cls.workspace_root)
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "server") and cls.server:
            cls.server.stop()

    # 1. Real Chrome launch, axe injection, and global confirmation
    def test_01_live_chrome_inject_axe_and_verify_global(self):
        """B-01: Verifies axe-core successfully injects into live Chrome and exposes window.axe."""
        with CDPBrowserDriver(browser_info=self.preferred_browser) as driver:
            driver.launch(headless=True)
            url = self.server.get_url("MDS/10-Testing/accessibility/fixtures/accessible_fixture.html")
            driver.navigate(url)

            runner = AxeRunner()
            version = runner.inject(driver)
            self.assertEqual(version, "4.13.0")

            # Verify global axe object properties
            axe_type = driver.evaluate("typeof window.axe")
            self.assertEqual(axe_type, "object")
            run_fn_type = driver.evaluate("typeof window.axe.run")
            self.assertEqual(run_fn_type, "function")

    # 2. Accessible fixture produces PASS with zero violations
    def test_02_live_accessible_fixture_zero_violations_pass(self):
        """B-02: Verifies accessible baseline fixture achieves PASS with exactly 0 violations."""
        with CDPBrowserDriver(browser_info=self.preferred_browser) as driver:
            driver.launch(headless=True)
            url = self.server.get_url("MDS/10-Testing/accessibility/fixtures/accessible_fixture.html")
            driver.navigate(url)

            runner = AxeRunner()
            result = runner.audit_page(driver, capability_id="MDS-A11Y-004")

            self.assertEqual(result.status, BrowserExecutionStatus.PASS)
            self.assertEqual(result.violation_count, 0)
            self.assertEqual(len(result.violations), 0)
            self.assertGreater(result.pass_count, 10)  # Multiple rules evaluated and passed
            self.assertEqual(result.axe_version, "4.13.0")
            self.assertGreater(result.duration_ms, 0.0)

            # Evidence inspection
            self.assertEqual(result.evidence["status"], "PASS")
            self.assertEqual(result.evidence["summary_metrics"]["violation_count"], 0)

    # 3. Inaccessible fixture produces FAIL with specific detected violations (No False-Green)
    def test_03_live_inaccessible_fixture_detected_violations_fail(self):
        """B-03 (No False-Green): Proves deliberately broken fixture causes FAIL and captures violations."""
        with CDPBrowserDriver(browser_info=self.preferred_browser) as driver:
            driver.launch(headless=True)
            url = self.server.get_url("MDS/10-Testing/accessibility/fixtures/inaccessible_fixture.html")
            driver.navigate(url)

            runner = AxeRunner()
            result = runner.audit_page(driver, capability_id="MDS-A11Y-004")

            self.assertEqual(result.status, BrowserExecutionStatus.FAIL)
            self.assertGreaterEqual(result.violation_count, 3)

            violation_ids = [v["id"] for v in result.violations]
            # Must detect our deliberate violations
            self.assertTrue(
                any(v_id in violation_ids for v_id in ["label", "image-alt", "button-name", "color-contrast", "document-title"]),
                f"Deliberate violations not detected. Found: {violation_ids}"
            )

            # Verify node extraction
            for v in result.violations:
                nodes = v.get("nodes", [])
                self.assertGreater(len(nodes), 0)
                for node in nodes:
                    self.assertIn("target", node)
                    self.assertIn("html", node)
                    self.assertLessEqual(len(node["html"]), 203)

    # 4. Incomplete fixture captures ambiguous evaluation metrics
    def test_04_live_incomplete_fixture_captures_incomplete_metrics(self):
        """B-04: Verifies incomplete items requiring manual review are captured in metrics."""
        with CDPBrowserDriver(browser_info=self.preferred_browser) as driver:
            driver.launch(headless=True)
            url = self.server.get_url("MDS/10-Testing/accessibility/fixtures/incomplete_fixture.html")
            driver.navigate(url)

            runner = AxeRunner()
            result = runner.audit_page(driver, capability_id="MDS-A11Y-004")

            self.assertGreaterEqual(result.incomplete_count, 1)
            incomplete_ids = [inc["id"] for inc in result.incomplete]
            self.assertIn("color-contrast", incomplete_ids)

    # 5. Live audit on locked MDS Reference Application surface
    def test_05_live_reference_app_accessibility_audit(self):
        """B-05 (A11Y-002): Executes dynamic axe audit against actual locked Reference Application surface with deterministic surface evidence."""
        with CDPBrowserDriver(browser_info=self.preferred_browser) as driver:
            driver.launch(headless=True)
            url = self.server.get_url("MDS/Reference-Application/index.html")
            driver.navigate(url)
            driver.wait_for("#ctrl-ref-role", timeout_ms=5000)

            # 1. Deterministic surface identity assertions tying execution directly to Reference Application DOM
            doc_title = driver.evaluate("document.title")
            self.assertIn("MDS Workspace", doc_title)
            self.assertIn("Reference Application", doc_title)

            # 2. Execute live axe-core audit against the Reference Application
            policy = AccessibilityPolicy(policy_name="MDS-Audit-Inspection", fail_on_minor=False)
            runner = AxeRunner(policy=policy)
            result = runner.audit_page(driver, capability_id="MDS-A11Y-004")

            # 3. Deterministic surface & environment assertions
            self.assertIn("MDS/Reference-Application/index.html", result.page_url)
            self.assertEqual(result.axe_version, "4.13.0")
            self.assertIsNotNone(result.browser)
            self.assertIn("Chrome", result.browser)
            self.assertIsNotNone(result.viewport)
            self.assertEqual(result.viewport.get("width"), 1440)
            self.assertEqual(result.viewport.get("height"), 900)
            self.assertGreater(result.duration_ms, 0.0)

            # 4. Deterministic audit rule metrics on real Reference App surface
            self.assertGreaterEqual(result.pass_count, 35)  # Real surface passes >=35 rules
            self.assertGreaterEqual(result.violation_count, 2)
            violation_ids = [v["id"] for v in result.violations]
            self.assertIn("color-contrast", violation_ids)
            self.assertIn("select-name", violation_ids)

            # 5. Incomplete checks verification
            self.assertGreaterEqual(result.incomplete_count, 1)
            incomplete_ids = [inc["id"] for inc in result.incomplete]
            self.assertIn("color-contrast", incomplete_ids)

            # 6. Format and confirm comprehensive text report generation
            report = AccessibilityEvidenceGenerator.format_text_report(result)
            self.assertIn("MDS ACCESSIBILITY AUDIT REPORT", report)
            self.assertIn("axe-core:     v4.13.0", report)
            self.assertIn("Reference-Application/index.html", report)
            self.assertIn("color-contrast", report)
            self.assertIn("select-name", report)

    # 6. Complete End-to-End Dispatch Integration
    def test_06_live_end_to_end_dispatch_promotion_a11y_004(self):
        """B-06: Verifies full dispatch chain: Registry -> Dispatcher -> BrowserBridge -> axe-core -> ExecutionResult."""
        cap_dispatcher = CapabilityDispatcher(workspace_root=self.workspace_root)
        browser_dispatcher = BrowserCapabilityDispatcher(workspace_root=self.workspace_root)

        # 1. Verify capability metadata from registry
        cap_meta = cap_dispatcher.get_capability("MDS-A11Y-004")
        self.assertIsNotNone(cap_meta)
        self.assertEqual(cap_meta["status"], "ACTIVE")
        self.assertEqual(cap_meta["execution"], "BROWSER_AUTOMATION")
        self.assertIsNone(cap_meta["deferred_reason"])

        # 2. Dispatch capability through BrowserCapabilityDispatcher
        browser_res = browser_dispatcher.execute_browser_capability("MDS-A11Y-004")
        self.assertIn(browser_res.status, (BrowserExecutionStatus.PASS, BrowserExecutionStatus.FAIL))
        self.assertEqual(browser_res.capability_id, "MDS-A11Y-004")

        # 3. Translate to Master Harness ExecutionResult
        exec_res = browser_dispatcher.to_execution_result(browser_res)
        self.assertEqual(exec_res.capability_id, "MDS-A11Y-004")
        self.assertIn(exec_res.status, (ExecutionStatus.PASS, ExecutionStatus.FAIL))
        self.assertEqual(browser_res.evidence["audit_environment"]["axe_version"], "4.13.0")
        self.assertTrue(len(exec_res.details) > 0)


if __name__ == "__main__":
    unittest.main()
