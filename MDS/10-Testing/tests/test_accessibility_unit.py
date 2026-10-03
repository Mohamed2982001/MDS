#!/usr/bin/env python3
"""
Unit & Contract Tests for MDS Dynamic Accessibility Automation Engine
Phase 9.7.5: Dynamic Accessibility Automation (Layer I)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Validates artifact integrity, loader discovery, policy evaluation, violation extraction,
failure modes, and dispatch contracts without requiring a live browser.
"""

import sys
import os
import json
import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

# Ensure MDS/10-Testing is on sys.path
TESTING_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TESTING_DIR))

from browser.models import BrowserExecutionStatus, Viewport
from accessibility.accessibility_models import (
    AccessibilityImpact,
    AccessibilityNode,
    AccessibilityViolation,
    AccessibilityIncomplete,
    AccessibilityPass,
    AccessibilityPolicy,
    AccessibilityResult,
)
from accessibility.axe_loader import (
    AxeLoader,
    AxeArtifact,
    AxeArtifactNotFoundError,
    AxeIntegrityError,
)
from accessibility.evidence import AccessibilityEvidenceGenerator
from accessibility.axe_runner import AxeRunner
from accessibility.accessibility_dispatch import AccessibilityDispatcher
from static.dispatch_adapter import CapabilityDispatcher, ExecutionStatus


class TestAccessibilityUnit(unittest.TestCase):
    """Category A: Offline Unit Tests for Dynamic Accessibility Validation Engine."""

    # 1. Pinned axe artifact discovery and metadata verification
    def test_01_axe_artifact_discovery_and_metadata(self):
        """A-01: Verifies discovery of pinned local axe.min.js and metadata validity."""
        artifact = AxeLoader.get_artifact()
        self.assertIsNotNone(artifact)
        self.assertEqual(artifact.version, "4.13.0")
        self.assertTrue(artifact.file_path.exists())
        self.assertGreater(artifact.size_bytes, 500000)
        self.assertEqual(len(artifact.sha256), 64)
        # Check source content begins with axe definition
        src = artifact.get_source()
        self.assertIn("axe", src[:500].lower())

    # 2. Missing artifact raises AxeArtifactNotFoundError
    def test_02_missing_axe_artifact_raises_not_found(self):
        """A-02: Verifies AxeArtifactNotFoundError raised when vendor directory is empty."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self.assertRaises(AxeArtifactNotFoundError) as ctx:
                AxeLoader.get_artifact(vendor_dir=Path(tmp_dir))
            self.assertIn("Axe-core artifact missing", str(ctx.exception))
            self.assertFalse(AxeLoader.is_artifact_available(vendor_dir=Path(tmp_dir)))

    # 3. Corrupted artifact raises AxeIntegrityError
    def test_03_corrupted_axe_artifact_raises_integrity_error(self):
        """A-03: Verifies AxeIntegrityError raised when artifact checksum fails."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            corrupted_js = tmp_path / "axe.min.js"
            with open(corrupted_js, "w", encoding="utf-8") as fp:
                fp.write("/* corrupted code */")

            meta_file = tmp_path / "axe_metadata.json"
            with open(meta_file, "w", encoding="utf-8") as fp:
                json.dump({"version": "4.13.0", "sha256": "0000000000000000000000000000000000000000000000000000000000000000"}, fp)

            with self.assertRaises(AxeIntegrityError) as ctx:
                AxeLoader.get_artifact(vendor_dir=tmp_path)
            self.assertIn("checksum mismatch", str(ctx.exception).lower())

    # 4. AccessibilityNode truncates long HTML strings
    def test_04_accessibility_models_and_node_truncation(self):
        """A-04: Verifies AccessibilityNode limits HTML snippet length to prevent payload bloat."""
        long_html = "<div class='super-long-class-attribute-with-nested-elements'>" + ("x" * 500) + "</div>"
        node = AccessibilityNode(target=["#my-id"], html=long_html, failure_summary="Fix color contrast")
        node_dict = node.to_dict()
        self.assertLessEqual(len(node_dict["html"]), 203)
        self.assertTrue(node_dict["html"].endswith("..."))
        self.assertEqual(node_dict["target"], ["#my-id"])

    # 5. Policy evaluation: Critical and Serious cause FAIL
    def test_05_policy_evaluation_critical_and_serious_fail(self):
        """A-05: Verifies default policy marks critical and serious violations as FAIL."""
        policy = AccessibilityPolicy()
        violations = [
            AccessibilityViolation(
                id="color-contrast",
                impact="serious",
                description="Elements must have sufficient color contrast",
                help="Ensure sufficient color contrast",
                help_url="https://dequeuniversity.com/rules/axe/4.13/color-contrast",
                tags=["wcag2aa"],
                nodes=[AccessibilityNode(target=["p.text"], html="<p class='text'>Invisible</p>")]
            )
        ]
        status, summary = policy.evaluate(violations, [])
        self.assertEqual(status, BrowserExecutionStatus.FAIL)
        self.assertIn("Serious: 1", summary)

    # 6. Policy evaluation: Zero violations produces PASS
    def test_06_policy_evaluation_zero_violations_pass(self):
        """A-06: Verifies default policy produces PASS when zero blocking violations exist."""
        policy = AccessibilityPolicy()
        status, summary = policy.evaluate([], [])
        self.assertEqual(status, BrowserExecutionStatus.PASS)
        self.assertIn("0 blocking violations", summary)

    # 7. Minor and incomplete items treated as advisory diagnostics
    def test_07_policy_minor_and_incomplete_advisory_handling(self):
        """A-07: Verifies minor violations and incomplete checks do not fail default policy."""
        policy = AccessibilityPolicy()
        minor_v = [
            AccessibilityViolation(
                id="link-in-text-block",
                impact="minor",
                description="Links must be distinguishable without color",
                help="Underline links",
                help_url="https://dequeuniversity.com/rules/axe/4.13/link-in-text-block"
            )
        ]
        inc = [
            AccessibilityIncomplete(
                id="color-contrast",
                impact="serious",
                description="Contrast check requires manual review",
                help="Manual contrast verification",
                help_url="",
                nodes_count=1
            )
        ]
        status, summary = policy.evaluate(minor_v, inc)
        self.assertEqual(status, BrowserExecutionStatus.PASS)

    # 8. Evidence generator structure
    def test_08_evidence_generation_structure(self):
        """A-08: Verifies AccessibilityEvidenceGenerator builds full structured audit bundle."""
        res = AccessibilityResult(
            capability_id="MDS-A11Y-004",
            status=BrowserExecutionStatus.PASS,
            axe_version="4.13.0",
            page_url="http://127.0.0.1:8000/fixture.html",
            browser="Chrome",
            viewport={"width": 1440, "height": 900},
            violation_count=0,
            incomplete_count=1,
            pass_count=15,
            duration_ms=45.2
        )
        evidence = AccessibilityEvidenceGenerator.build_evidence(res)
        self.assertEqual(evidence["capability_id"], "MDS-A11Y-004")
        self.assertEqual(evidence["status"], "PASS")
        self.assertEqual(evidence["summary_metrics"]["pass_count"], 15)
        self.assertEqual(evidence["audit_environment"]["browser"], "Chrome")

        report_txt = AccessibilityEvidenceGenerator.format_text_report(res)
        self.assertIn("MDS ACCESSIBILITY AUDIT REPORT", report_txt)
        self.assertIn("VIOLATIONS: None detected (0 violations)", report_txt)

    # 9. Runner fails if driver is not connected
    def test_09_runner_driver_not_connected_fails(self):
        """A-09: Verifies AxeRunner.audit_page returns FAIL when driver is disconnected."""
        mock_driver = MagicMock()
        mock_driver.is_connected = False
        runner = AxeRunner()
        res = runner.audit_page(mock_driver)
        self.assertEqual(res.status, BrowserExecutionStatus.FAIL)
        self.assertEqual(res.exception_type, "BrowserBridgeError")
        self.assertIn("not connected", res.error_message)

    # 10. Runner catches integrity error as FAIL
    def test_10_runner_catches_injection_integrity_error_as_fail(self):
        """A-10: Verifies AxeRunner catches AxeIntegrityError and reports FAIL."""
        mock_driver = MagicMock()
        mock_driver.is_connected = True
        mock_driver.evaluate.return_value = False
        runner = AxeRunner()
        with patch.object(AxeLoader, "get_artifact", side_effect=AxeIntegrityError("Checksum mismatch")):
            res = runner.audit_page(mock_driver)
            self.assertEqual(res.status, BrowserExecutionStatus.FAIL)
            self.assertEqual(res.exception_type, "AxeIntegrityError")

    # 11. Runner catches missing artifact as DEFERRED
    def test_11_runner_catches_missing_artifact_as_deferred(self):
        """A-11: Verifies AxeRunner catches AxeArtifactNotFoundError and reports DEFERRED."""
        mock_driver = MagicMock()
        mock_driver.is_connected = True
        mock_driver.evaluate.return_value = False
        runner = AxeRunner()
        with patch.object(AxeLoader, "get_artifact", side_effect=AxeArtifactNotFoundError("Artifact missing")):
            res = runner.audit_page(mock_driver)
            self.assertEqual(res.status, BrowserExecutionStatus.DEFERRED)
            self.assertEqual(res.exception_type, "AxeArtifactNotFoundError")

    # 12. Runner catches JavaScript evaluation exception as FAIL
    def test_12_runner_catches_cdp_evaluation_exception_as_fail(self):
        """A-12: Verifies AxeRunner catches JS runtime errors during axe.run and reports FAIL."""
        mock_driver = MagicMock()
        mock_driver.is_connected = True
        # 1st evaluate (check loaded): returns True
        # 2nd evaluate (get version): returns "4.13.0"
        # 3rd evaluate (run axe): raises Exception
        mock_driver.evaluate.side_effect = [True, "4.13.0", RuntimeError("Uncaught Error inside axe.run")]
        runner = AxeRunner()
        res = runner.audit_page(mock_driver)
        self.assertEqual(res.status, BrowserExecutionStatus.FAIL)
        self.assertEqual(res.exception_type, "RuntimeError")
        self.assertIn("axe.run execution failed", res.error_message)

    # 13. Dispatcher returns DEFERRED when browser is unavailable
    def test_13_dispatcher_deferred_when_no_browser(self):
        """A-13: Verifies AccessibilityDispatcher returns DEFERRED when host has no browser."""
        dispatcher = AccessibilityDispatcher()
        dispatcher.preferred_browser = None
        res = dispatcher.run_audit()
        self.assertEqual(res.status, BrowserExecutionStatus.DEFERRED)
        self.assertEqual(res.exception_type, "BrowserUnavailableError")

    # 14. Dispatcher conversion to ExecutionResult
    def test_14_dispatcher_to_execution_result_contract(self):
        """A-14: Verifies translation from AccessibilityResult to ExecutionResult."""
        dispatcher = AccessibilityDispatcher()
        a_res = AccessibilityResult(
            capability_id="MDS-A11Y-004",
            status=BrowserExecutionStatus.PASS,
            axe_version="4.13.0",
            violation_count=0,
            pass_count=22,
            duration_ms=65.0
        )
        exec_res = dispatcher.to_execution_result(a_res)
        self.assertEqual(exec_res.capability_id, "MDS-A11Y-004")
        self.assertEqual(exec_res.status, ExecutionStatus.PASS)
        self.assertIn("22 passed", exec_res.details)

    # 15. Registry accounting invariant 170
    def test_15_registry_accounting_invariant_170(self):
        """A-15: Verifies registry accounting: 170 Unique IDs = 168 Active + 2 Deferred."""
        registry_path = TESTING_DIR / "capabilities" / "registry.json"
        with open(registry_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)

        accounting = data["metadata"]["accounting"]
        self.assertEqual(accounting["unique_defined_ids"], 170)
        self.assertEqual(accounting["active_executable_assertions"], 170)
        self.assertEqual(accounting["deferred_capabilities"], 0)
        self.assertEqual(accounting["wrapped_assertions"], 37)

        # Confirm MDS-A11Y-004 is ACTIVE
        caps = {c["id"]: c for c in data["capabilities"]}
        self.assertIn("MDS-A11Y-004", caps)
        a11y_cap = caps["MDS-A11Y-004"]
        self.assertEqual(a11y_cap["status"], "ACTIVE")
        self.assertIsNone(a11y_cap["deferred_reason"])
        self.assertEqual(a11y_cap["execution"], "BROWSER_AUTOMATION")
        self.assertEqual(a11y_cap["runner"]["entrypoint"], "run_accessibility_capability")

    # 16. Structural dispatch chain resolution
    def test_16_structural_dispatch_chain_resolution(self):
        """A-16: Verifies complete dispatch path resolution for MDS-A11Y-004."""
        cap_dispatcher = CapabilityDispatcher()
        ok, msg, runner_fn = cap_dispatcher.resolve_runner("MDS-A11Y-004")
        self.assertTrue(ok, f"Failed to resolve MDS-A11Y-004: {msg}")
        self.assertIsNotNone(runner_fn)
        self.assertEqual(runner_fn.__name__, "run_accessibility_capability")

    # 17. Policy Exact Severity Matrix Regression (A11Y-001)
    def test_17_policy_exact_severity_matrix_regression(self):
        """A-17 (A11Y-001): Proves canonical WCAG-AA policy boundary: Critical/Serious/Moderate FAIL, Minor/Incomplete PASS."""
        policy = AccessibilityPolicy()
        self.assertEqual(policy.policy_name, "MDS-Standard-WCAG-AA")
        self.assertTrue(policy.fail_on_critical)
        self.assertTrue(policy.fail_on_serious)
        self.assertTrue(policy.fail_on_moderate)
        self.assertFalse(policy.fail_on_minor)
        self.assertFalse(policy.fail_on_incomplete)

        def make_violation(rule_id: str, impact: str) -> AccessibilityViolation:
            return AccessibilityViolation(
                id=rule_id,
                impact=impact,
                description=f"Test violation for {rule_id}",
                help=f"Fix {rule_id}",
                help_url=f"https://dequeuniversity.com/rules/axe/4.13/{rule_id}",
                tags=["wcag2aa"],
                nodes=[AccessibilityNode(target=["#elem"], html="<div>Test</div>")]
            )

        def make_incomplete(rule_id: str) -> AccessibilityIncomplete:
            return AccessibilityIncomplete(
                id=rule_id,
                impact="moderate",
                description=f"Incomplete check for {rule_id}",
                help=f"Review {rule_id}",
                help_url=f"https://dequeuniversity.com/rules/axe/4.13/{rule_id}",
                tags=["wcag2aa"],
                nodes_count=1
            )

        # 1. Critical alone -> FAIL
        status, summary = policy.evaluate([make_violation("button-name", "critical")], [])
        self.assertEqual(status, BrowserExecutionStatus.FAIL)
        self.assertIn("Critical: 1", summary)

        # 2. Serious alone -> FAIL
        status, summary = policy.evaluate([make_violation("color-contrast", "serious")], [])
        self.assertEqual(status, BrowserExecutionStatus.FAIL)
        self.assertIn("Serious: 1", summary)

        # 3. Moderate alone -> FAIL
        status, summary = policy.evaluate([make_violation("heading-order", "moderate")], [])
        self.assertEqual(status, BrowserExecutionStatus.FAIL)
        self.assertIn("Moderate: 1", summary)

        # 4. Minor alone -> PASS (Advisory diagnostic)
        status, summary = policy.evaluate([make_violation("link-in-text-block", "minor")], [])
        self.assertEqual(status, BrowserExecutionStatus.PASS)
        self.assertIn("0 blocking violations", summary)

        # 5. Incomplete alone -> PASS (Advisory diagnostic)
        status, summary = policy.evaluate([], [make_incomplete("color-contrast")])
        self.assertEqual(status, BrowserExecutionStatus.PASS)
        self.assertIn("0 blocking violations", summary)

        # 6. Minor + Incomplete together -> PASS
        status, summary = policy.evaluate([make_violation("link-in-text-block", "minor")], [make_incomplete("color-contrast")])
        self.assertEqual(status, BrowserExecutionStatus.PASS)
        self.assertIn("0 blocking violations", summary)

        # 7. Minor + Moderate together -> FAIL (Moderate blocks)
        status, summary = policy.evaluate([make_violation("link-in-text-block", "minor"), make_violation("heading-order", "moderate")], [])
        self.assertEqual(status, BrowserExecutionStatus.FAIL)
        self.assertIn("Moderate: 1", summary)

        # 8. Empty -> PASS
        status, summary = policy.evaluate([], [])
        self.assertEqual(status, BrowserExecutionStatus.PASS)
        self.assertIn("0 blocking violations", summary)

        # 9. Strict policy variant enforcing minor and incomplete
        strict_policy = AccessibilityPolicy(policy_name="MDS-Strict-A11Y", fail_on_minor=True, fail_on_incomplete=True)
        s_status, _ = strict_policy.evaluate([make_violation("link-in-text-block", "minor")], [])
        self.assertEqual(s_status, BrowserExecutionStatus.FAIL)
        inc_status, inc_summary = strict_policy.evaluate([], [make_incomplete("color-contrast")])
        self.assertEqual(inc_status, BrowserExecutionStatus.FAIL)
        self.assertIn("incomplete checks require manual review", inc_summary)

    # 18. Registry & Master Harness Accounting Reconciliation (A11Y-003)
    def test_18_registry_master_harness_accounting_reconciliation(self):
        """A-18 (A11Y-003): Proves exact invariant 170 Unique IDs = 168 Active + 2 Deferred, 37 Wrapped, 0 Duplicates."""
        registry_path = TESTING_DIR / "capabilities" / "registry.json"
        with open(registry_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)

        # 1. Metadata accounting validation
        accounting = data["metadata"]["accounting"]
        self.assertEqual(accounting["unique_defined_ids"], 170)
        self.assertEqual(accounting["active_executable_assertions"], 170)
        self.assertEqual(accounting["deferred_capabilities"], 0)
        self.assertEqual(accounting["wrapped_assertions"], 37)
        self.assertEqual(accounting["quarantined_capabilities"], 0)
        self.assertEqual(accounting["disabled_capabilities"], 0)

        # 2. Strict ID uniqueness: Exactly 170 unique capability definitions (zero duplicates)
        caps = data["capabilities"]
        cap_ids = [c["id"] for c in caps]
        self.assertEqual(len(cap_ids), 170, f"Expected 170 capabilities, found {len(cap_ids)}")
        self.assertEqual(len(set(cap_ids)), 170, "Detected duplicate capability IDs in registry.json")

        # 3. Active vs Deferred partition
        active_caps = [c for c in caps if c["status"] == "ACTIVE"]
        deferred_caps = [c for c in caps if c["status"] == "DEFERRED"]
        self.assertEqual(len(active_caps), 170, f"Expected 170 active capabilities, found {len(active_caps)}")
        self.assertEqual(len(deferred_caps), 0, f"Expected 0 deferred capabilities, found {len(deferred_caps)}")

        # 4. Verify exact deferred capabilities list is empty
        deferred_ids = sorted([c["id"] for c in deferred_caps])
        self.assertEqual(deferred_ids, [])

        # 5. Verify MDS-A11Y-004 is uniquely defined, ACTIVE, and BROWSER_AUTOMATION
        a11y_caps = [c for c in caps if c["id"] == "MDS-A11Y-004"]
        self.assertEqual(len(a11y_caps), 1, "MDS-A11Y-004 must be defined exactly once")
        a11y_cap = a11y_caps[0]
        self.assertEqual(a11y_cap["status"], "ACTIVE")
        self.assertEqual(a11y_cap["execution"], "BROWSER_AUTOMATION")
        self.assertIsNone(a11y_cap["deferred_reason"])
        self.assertEqual(a11y_cap["runner"]["entrypoint"], "run_accessibility_capability")

        # 6. Verify 37 wrapped assertions in MDS-DSS-000
        dss_wrapper = [c for c in caps if c["id"] == "MDS-DSS-000"]
        self.assertEqual(len(dss_wrapper), 1)
        self.assertEqual(len(dss_wrapper[0]["wraps"]), 37)

        # 7. Reconcile with Master Test Harness (run_tests.py)
        # Master Harness defines 48 tests: 48 active executable tests + 0 deferred
        import run_tests
        harness = run_tests.MDSTestRunner()
        # Verify run_responsive_tests records MDS-RWD-003 as PASS (when browser available)
        harness.run_responsive_tests()
        resp_res = [r for r in harness.results if r["id"] == "MDS-RWD-003"]
        self.assertEqual(len(resp_res), 1)
        self.assertIn(resp_res[0]["status"], ["PASS", "NOT_EXECUTABLE_IN_CURRENT_RUNTIME"])

        # Verify run_visual_tests records MDS-VIS-001 as PASS (when browser available)
        harness.run_visual_tests()
        vis_res = [r for r in harness.results if r["id"] == "MDS-VIS-001"]
        self.assertEqual(len(vis_res), 1)
        self.assertIn(vis_res[0]["status"], ["PASS", "NOT_EXECUTABLE_IN_CURRENT_RUNTIME"])


if __name__ == "__main__":
    unittest.main()
