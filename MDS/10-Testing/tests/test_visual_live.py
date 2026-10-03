#!/usr/bin/env python3
"""
MDS Live Visual Regression Sweep Tests
Phase 9.7.7: Visual Regression Engine & Snapshot Diffing
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Executes the full 12-baseline visual regression sweep against the locked
Reference Application using live headless Chrome via CDP.
"""

import unittest
from pathlib import Path
import sys

TESTING_DIR = Path(__file__).resolve().parent.parent
if str(TESTING_DIR) not in sys.path:
    sys.path.insert(0, str(TESTING_DIR))

from browser.browser_discovery import BrowserDiscovery
from visual.baseline_manager import BaselineManager
from visual.visual_dispatch import VisualDispatcher
from visual.visual_models import VisualExecutionStatus
from visual.evidence_generator import VisualEvidenceGenerator


class TestVisualLive(unittest.TestCase):
    """Category B: Real Browser Live Visual Snapshot Auditing Tests on Google Chrome."""

    @classmethod
    def setUpClass(cls):
        cls.preferred_browser = BrowserDiscovery.get_preferred()
        if not cls.preferred_browser or not cls.preferred_browser.is_available:
            raise unittest.SkipTest("Skipping Visual Live: No Chromium browser available on host.")

        cls.mgr = BaselineManager(workspace_root=TESTING_DIR.parent.parent)
        is_font_valid, msg, _ = cls.mgr.verify_fonts()
        if not is_font_valid:
            raise unittest.SkipTest(f"Skipping Visual Live: {msg}")

        cls.dispatcher = VisualDispatcher(workspace_root=TESTING_DIR.parent.parent)

    def test_01_live_12_baseline_visual_sweep(self):
        """
        Executes real browser visual comparison across all 12 canonical baselines
        against the locked Reference Application with pinned Cairo font artifacts.
        """
        result = self.dispatcher.run_sweep(capability_id="MDS-VIS-001")

        # 1. Status and counts
        self.assertEqual(result.status, VisualExecutionStatus.PASS, f"Visual sweep failed: {result.error_message}")
        self.assertEqual(result.total_baselines, 12)
        self.assertEqual(result.passed_baselines, 12)
        self.assertEqual(result.failed_baselines, 0)
        self.assertEqual(result.deferred_baselines, 0)

        # 2. Assert every baseline has 0.0 or <= 0.001 diff ratio
        for r in result.results:
            self.assertEqual(r.status, VisualExecutionStatus.PASS)
            self.assertLessEqual(r.metrics.diff_ratio, 0.001, f"{r.baseline_id} diff ratio exceeded threshold")

        # 3. Evidence file generation
        self.assertIsNotNone(result.evidence_file)
        self.assertTrue(result.evidence_file.exists())

        # 4. Text report formatting
        report = VisualEvidenceGenerator.format_text_report(result)
        self.assertIn("MDS VISUAL REGRESSION & SNAPSHOT DIFFING AUDIT REPORT", report)
        self.assertIn("OVERALL VERDICT: SUCCESS", report)


if __name__ == "__main__":
    unittest.main()
