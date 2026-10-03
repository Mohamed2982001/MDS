#!/usr/bin/env python3
"""
Unit Tests for MDS Responsive Viewport Automation Engine
Phase 9.7.6: Responsive Viewport Automation (Layer K)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Validates:
1. Canonical Viewport definitions and constraints (ADR-074)
2. Canonical 17-Run Deterministic Execution Matrix (ADR-071 & ADR-075)
3. Tri-Class Assertion Model (HARD_CONTRACT, OBSERVABLE_BEHAVIOR, INFORMATIONAL_MEASUREMENT)
4. Anti-False-Green Protection (Horizontal blowout, missing controls)
5. Layout reflow settlement timeout bounds (ADR-076)
6. Evidence serialization & test accounting
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

TESTING_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = TESTING_DIR.parent.parent
sys.path.insert(0, str(TESTING_DIR))

from responsive.responsive_models import (
    AssertionClass,
    CanonicalViewportTier,
    ViewportDefinition,
    ResponsiveRunConfig,
    ResponsiveAssertion,
    ResponsiveRunResult,
    ResponsiveMatrixResult,
)
from responsive.viewport_matrix import (
    VP_320,
    VP_768,
    VP_1024,
    VP_1440,
    CANONICAL_VIEWPORTS,
    CANONICAL_MATRIX_RUNS,
    get_canonical_viewports,
    get_canonical_matrix,
    get_run_config_by_id,
)
from responsive.responsive_assertions import ResponsiveAssertionsEvaluator
from responsive.responsive_runner import ResponsiveRunner
from responsive.evidence import ResponsiveEvidenceGenerator
from responsive.responsive_dispatch import ResponsiveDispatcher


class TestResponsiveEngineUnit(unittest.TestCase):
    """Exhaustive unit test suite for the Responsive Engine."""

    # -------------------------------------------------------------------------
    # 1. Canonical Viewports Validation (ADR-074)
    # -------------------------------------------------------------------------
    def test_01_canonical_viewports_integrity(self):
        """Verifies exactly 4 canonical viewports exist with exact dimensions."""
        viewports = get_canonical_viewports()
        self.assertEqual(len(viewports), 4)
        self.assertIn("320", viewports)
        self.assertIn("768", viewports)
        self.assertIn("1024", viewports)
        self.assertIn("1440", viewports)
        self.assertNotIn("1280", viewports, "1280px is strictly forbidden as a canonical breakpoint")

        # Mobile 320
        self.assertEqual(VP_320.width, 320)
        self.assertEqual(VP_320.height, 640)
        self.assertEqual(VP_320.device_scale_factor, 2.0)
        self.assertTrue(VP_320.is_mobile)

        # Tablet 768
        self.assertEqual(VP_768.width, 768)
        self.assertEqual(VP_768.height, 1024)
        self.assertEqual(VP_768.device_scale_factor, 2.0)
        self.assertTrue(VP_768.is_mobile)

        # Desktop 1024
        self.assertEqual(VP_1024.width, 1024)
        self.assertEqual(VP_1024.height, 768)
        self.assertEqual(VP_1024.device_scale_factor, 1.0)
        self.assertFalse(VP_1024.is_mobile)

        # Wide 1440
        self.assertEqual(VP_1440.width, 1440)
        self.assertEqual(VP_1440.height, 900)
        self.assertEqual(VP_1440.device_scale_factor, 1.0)
        self.assertFalse(VP_1440.is_mobile)

    # -------------------------------------------------------------------------
    # 2. Canonical 17-Run Matrix Integrity (ADR-071 & ADR-075)
    # -------------------------------------------------------------------------
    def test_02_canonical_matrix_structure(self):
        """Verifies the canonical matrix defines exactly 17 runs."""
        matrix = get_canonical_matrix()
        self.assertEqual(len(matrix), 17)

        # Unique IDs
        run_ids = [r.run_id for r in matrix]
        self.assertEqual(len(run_ids), len(set(run_ids)), "All run IDs in matrix must be unique")

        # Runs RWD-RUN-001 through RWD-RUN-017
        expected_ids = [f"RWD-RUN-{i:03d}" for i in range(1, 18)]
        self.assertEqual(run_ids, expected_ids)

    def test_03_tier_1_recomposition_sweep(self):
        """Verifies Tier 1 covers 3 archetype screens across 4 viewports (12 runs)."""
        matrix = get_canonical_matrix()
        tier_1 = matrix[:12]
        self.assertEqual(len(tier_1), 12)

        # Screens covered
        screens = {r.screen for r in tier_1}
        self.assertEqual(screens, {"Overview", "Items List", "Item Edit"})

        # Baseline settings: RTL, Light, Comfortable
        for r in tier_1:
            self.assertEqual(r.direction, "rtl")
            self.assertEqual(r.theme, "light")
            self.assertEqual(r.density, "comfortable")

        # Verify Item Edit runs 9-12 use canonical route #/items/edit
        item_edit_runs = [r for r in tier_1 if r.screen == "Item Edit"]
        self.assertEqual(len(item_edit_runs), 4)
        for r in item_edit_runs:
            self.assertEqual(r.route, "#/items/edit", f"Run {r.run_id} must use canonical route #/items/edit")

    def test_04_tier_2_orthogonal_invariants(self):
        """Verifies Tier 2 covers LTR symmetry, compact density, and high contrast (5 runs)."""
        matrix = get_canonical_matrix()
        tier_2 = matrix[12:]
        self.assertEqual(len(tier_2), 5)

        run_13 = get_run_config_by_id("RWD-RUN-013")
        self.assertIsNotNone(run_13)
        self.assertEqual(run_13.direction, "ltr")
        self.assertEqual(run_13.viewport.width, 320)

        run_14 = get_run_config_by_id("RWD-RUN-014")
        self.assertIsNotNone(run_14)
        self.assertEqual(run_14.direction, "ltr")
        self.assertEqual(run_14.viewport.width, 768)

        run_15 = get_run_config_by_id("RWD-RUN-015")
        self.assertIsNotNone(run_15)
        self.assertEqual(run_15.density, "compact")
        self.assertEqual(run_15.viewport.width, 320)

        run_16 = get_run_config_by_id("RWD-RUN-016")
        self.assertIsNotNone(run_16)
        self.assertEqual(run_16.density, "compact")
        self.assertEqual(run_16.viewport.width, 1024)

        run_17 = get_run_config_by_id("RWD-RUN-017")
        self.assertIsNotNone(run_17)
        self.assertEqual(run_17.theme, "high-contrast")
        self.assertEqual(run_17.theme_semantic_label, "High Contrast")
        self.assertEqual(run_17.viewport.width, 320)

    # -------------------------------------------------------------------------
    # 3. Tri-Class Assertion Model Classification (ADR-073)
    # -------------------------------------------------------------------------
    def test_05_assertion_model_classification(self):
        """Verifies the three assertion classes exist with correct semantics."""
        self.assertEqual(AssertionClass.HARD_CONTRACT.value, "HARD_CONTRACT")
        self.assertEqual(AssertionClass.OBSERVABLE_BEHAVIOR.value, "OBSERVABLE_BEHAVIOR")
        self.assertEqual(AssertionClass.INFORMATIONAL_MEASUREMENT.value, "INFORMATIONAL_MEASUREMENT")

    def test_06_hard_contract_failure_impact(self):
        """Verifies that a failure in a HARD_CONTRACT marks the run as FAIL."""
        cfg = get_run_config_by_id("RWD-RUN-001")
        assertions = [
            ResponsiveAssertion(
                run_id=cfg.run_id,
                capability_id="MDS-RWD-003",
                screen=cfg.screen,
                viewport_tier="320px",
                dimension="Navigation",
                assertion_class=AssertionClass.HARD_CONTRACT,
                selector="#btn-mobile-nav",
                assertion_name="Mobile nav toggle visible",
                passed=False,
                expected=True,
                actual=False,
            )
        ]
        result = ResponsiveRunResult(
            run_id=cfg.run_id,
            config=cfg,
            passed=False,
            assertions=assertions,
        )
        self.assertEqual(len(result.hard_failures), 1)
        self.assertFalse(result.passed)

    def test_07_informational_measurement_does_not_fail_run(self):
        """Verifies that an unpassed INFORMATIONAL_MEASUREMENT does NOT trigger a hard failure."""
        cfg = get_run_config_by_id("RWD-RUN-001")
        assertions = [
            ResponsiveAssertion(
                run_id=cfg.run_id,
                capability_id="MDS-RWD-003",
                screen=cfg.screen,
                viewport_tier="320px",
                dimension="Diagnostics",
                assertion_class=AssertionClass.INFORMATIONAL_MEASUREMENT,
                selector="window",
                assertion_name="Diagnostic Style Dump",
                passed=False,
                expected="optimal",
                actual="degraded",
            ),
            ResponsiveAssertion(
                run_id=cfg.run_id,
                capability_id="MDS-RWD-003",
                screen=cfg.screen,
                viewport_tier="320px",
                dimension="Navigation",
                assertion_class=AssertionClass.HARD_CONTRACT,
                selector="#btn-mobile-nav",
                assertion_name="Mobile nav toggle visible",
                passed=True,
                expected=True,
                actual=True,
            ),
        ]
        result = ResponsiveRunResult(
            run_id=cfg.run_id,
            config=cfg,
            passed=True,
            assertions=assertions,
        )
        self.assertEqual(len(result.hard_failures), 0)
        self.assertTrue(result.passed)

    # -------------------------------------------------------------------------
    # 4. Anti-False-Green Protection (ADR-072)
    # -------------------------------------------------------------------------
    def test_08_horizontal_overflow_detection(self):
        """Verifies evaluate_horizontal_overflow fails when scrollWidth > clientWidth."""
        mock_driver = MagicMock()
        # Simulate horizontal blowout: scrollWidth is 360, clientWidth is 320
        mock_driver.evaluate.return_value = {
            "clientWidth": 320,
            "scrollWidth": 360,
            "overflowDiff": 40.0,
            "hasOverflow": True,
            "blowouts": [{"tag": "div", "width": 360}],
        }
        cfg = get_run_config_by_id("RWD-RUN-001")
        assertions = ResponsiveAssertionsEvaluator.evaluate_horizontal_overflow(mock_driver, cfg)
        self.assertEqual(len(assertions), 1)
        a = assertions[0]
        self.assertEqual(a.assertion_class, AssertionClass.HARD_CONTRACT)
        self.assertFalse(a.passed, "Horizontal blowout must trigger assertion failure")
        self.assertIn("blowout detected", a.diagnostics)

    def test_09_mobile_sidebar_hidden_assertion(self):
        """Verifies desktop sidebar must be hidden at 320px."""
        mock_driver = MagicMock()
        # Simulate sidebar remaining visible at 320px (defect)
        mock_driver.evaluate.return_value = {
            "btnExists": True,
            "btnVisible": True,
            "sidebarExists": True,
            "sidebarVisible": True,
            "sidebarWidth": 260,
        }
        cfg = get_run_config_by_id("RWD-RUN-001")
        assertions = ResponsiveAssertionsEvaluator.evaluate_navigation_transformation(mock_driver, cfg)
        # Should have 2 assertions: btn visible, sidebar hidden
        sidebar_assertion = next(a for a in assertions if a.selector == ".mds-ref-sidebar")
        self.assertFalse(sidebar_assertion.passed)
        self.assertEqual(sidebar_assertion.assertion_class, AssertionClass.HARD_CONTRACT)

    def test_10_tablet_rail_width_assertion(self):
        """Verifies tablet sidebar must collapse to 72px icon rail (+/- 8px)."""
        mock_driver = MagicMock()
        mock_driver.evaluate.return_value = {
            "btnExists": True,
            "btnVisible": False,
            "sidebarExists": True,
            "sidebarVisible": True,
            "sidebarWidth": 72,
            "labelsHidden": True,
        }
        cfg = get_run_config_by_id("RWD-RUN-002")
        assertions = ResponsiveAssertionsEvaluator.evaluate_navigation_transformation(mock_driver, cfg)
        rail_assertion = next(a for a in assertions if a.selector == ".mds-ref-sidebar")
        self.assertTrue(rail_assertion.passed)
        self.assertEqual(rail_assertion.assertion_class, AssertionClass.OBSERVABLE_BEHAVIOR)

    def test_11_forbidden_1280_container_detection(self):
        """Verifies container constraint assertion fails if 1280px is used."""
        mock_driver = MagicMock()
        mock_driver.evaluate.return_value = {
            "mainExists": True,
            "mainMaxInlineSize": "1280px",
            "mainWidth": 1024,
        }
        cfg = get_run_config_by_id("RWD-RUN-003")
        assertions = ResponsiveAssertionsEvaluator.evaluate_container_constraints(mock_driver, cfg)
        rule_assertion = next(a for a in assertions if "1280px" in a.assertion_name)
        self.assertFalse(rule_assertion.passed)
        self.assertEqual(rule_assertion.assertion_class, AssertionClass.HARD_CONTRACT)

    # -------------------------------------------------------------------------
    # 5. Settlement Algorithm Timeout Bounds (ADR-076)
    # -------------------------------------------------------------------------
    def test_12_settlement_timeout_bounds(self):
        """Verifies wait_for_layout_settlement respects bounded timeout and does not hang."""
        mock_driver = MagicMock()
        # Simulate driver evaluate always returning unsettled DOM
        mock_driver.evaluate.return_value = {"settled": False, "clientWidth": 0}

        runner = ResponsiveRunner(settlement_timeout_ms=100)
        res = runner.wait_for_layout_settlement(mock_driver, timeout_ms=100)

        self.assertFalse(res["success"])
        self.assertIn("timed out", res["error"])
        self.assertLessEqual(res["duration_ms"], 500)

    # -------------------------------------------------------------------------
    # 6. Evidence Generation & Dispatch Adapter
    # -------------------------------------------------------------------------
    def test_13_evidence_generation(self):
        """Verifies evidence serialization adheres to canonical structure."""
        matrix_res = ResponsiveMatrixResult(
            capability_id="MDS-RWD-003",
            status="PASS",
            runs=[],
            total_assertions=50,
            passed_assertions=50,
            failed_assertions=0,
            hard_failures=0,
            duration_ms=1250.0,
            browser_version="Chrome/153.0.0.0",
        )
        evidence = ResponsiveEvidenceGenerator.generate_evidence_dict(matrix_res)
        self.assertEqual(evidence["capability_id"], "MDS-RWD-003")
        self.assertEqual(evidence["status"], "PASS")
        self.assertEqual(evidence["accounting"]["total_assertions"], 50)
        self.assertEqual(evidence["accounting"]["hard_failures"], 0)

        report_txt = ResponsiveEvidenceGenerator.format_text_report(matrix_res)
        self.assertIn("MDS-RWD-003", report_txt)
        self.assertIn("Overall Status:    PASS", report_txt)

    def test_14_dispatcher_result_translation(self):
        """Verifies ResponsiveDispatcher correctly maps to ExecutionResult and BrowserCapabilityResult."""
        disp = ResponsiveDispatcher(workspace_root=WORKSPACE_ROOT)
        m_res = ResponsiveMatrixResult(
            capability_id="MDS-RWD-003",
            status="PASS",
            runs=[],
            total_assertions=20,
            passed_assertions=20,
            failed_assertions=0,
            hard_failures=0,
            duration_ms=500.0,
        )

        b_res = disp.to_browser_capability_result(m_res)
        self.assertEqual(b_res.capability_id, "MDS-RWD-003")
        self.assertEqual(b_res.status.value, "PASS")

        e_res = disp.to_execution_result(m_res)
        self.assertEqual(e_res.capability_id, "MDS-RWD-003")
        self.assertEqual(e_res.status, "PASS")


if __name__ == "__main__":
    unittest.main()
