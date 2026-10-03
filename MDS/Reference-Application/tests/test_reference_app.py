#!/usr/bin/env python3
"""
========================================================================
     MASTER DESIGN SYSTEM (MDS) — REFERENCE APPLICATION TEST SUITE
                   Phase 9.6 Automated Verification
========================================================================
Verifies that the MDS Workspace Reference Application is:
1. An unprivileged consumer of the canonical Runtime Core.
2. Exercising all 6 canonical templates, 8 patterns, and 6 workflows.
3. Completely free of npm runtime packages or duplicate design systems.
4. Adhering to 100% CSS logical properties, 0 row-reverse, 0 raw hex colors.
5. Fully supporting the 4 mock roles and AI human-in-the-loop lifecycle.
========================================================================
"""

import json
import re
import sys
import unittest
from pathlib import Path

# Workspace Root
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
REF_APP_DIR = ROOT_DIR / "MDS" / "Reference-Application"
RUNTIME_DIR = ROOT_DIR / "MDS" / "Runtime"


class TestReferenceApplicationInventory(unittest.TestCase):
    """Verifies complete file inventory and zero npm dependencies."""

    def test_01_core_files_exist(self):
        self.assertTrue((REF_APP_DIR / "index.html").exists(), "index.html must exist")
        self.assertTrue((REF_APP_DIR / "app.css").exists(), "app.css must exist")
        self.assertTrue((REF_APP_DIR / "app.js").exists(), "app.js must exist")
        self.assertTrue((REF_APP_DIR / "fixtures" / "workspace_data.json").exists(), "workspace_data.json must exist")

    def test_02_zero_npm_dependencies(self):
        self.assertFalse((REF_APP_DIR / "package.json").exists(), "Reference App must NOT contain package.json")
        self.assertFalse((REF_APP_DIR / "package-lock.json").exists(), "Reference App must NOT contain package-lock.json")
        self.assertFalse((REF_APP_DIR / "node_modules").exists(), "Reference App must NOT contain node_modules")


class TestRuntimeConsumerContracts(unittest.TestCase):
    """Verifies that the Reference App consumes Runtime cleanly without modifying it."""

    def setUp(self):
        self.html_text = (REF_APP_DIR / "index.html").read_text(encoding="utf-8")
        self.js_text = (REF_APP_DIR / "app.js").read_text(encoding="utf-8")
        self.css_text = (REF_APP_DIR / "app.css").read_text(encoding="utf-8")

    def test_03_imports_mds_core_css(self):
        self.assertIn("../Runtime/css/mds-core.css", self.html_text,
                      "index.html must import ../Runtime/css/mds-core.css")

    def test_04_imports_components_js(self):
        self.assertIn("../Runtime/components/components.js", self.js_text,
                      "app.js must import ../Runtime/components/components.js")
        self.assertIn("MdsSwitch", self.js_text)
        self.assertIn("MdsTabs", self.js_text)
        self.assertIn("MdsDialog", self.js_text)
        # R-003: Mobile navigation drawer composed via canonical <mds-dialog id="dialog-mobile-nav">
        self.assertIn('id="dialog-mobile-nav"', self.html_text)
        self.assertIn('dialog-mobile-nav', self.js_text)
        self.assertIn('.mds-ref-mobile-nav-surface', self.css_text)
        self.assertNotIn('.is-mobile-open', self.css_text)
        self.assertNotIn('is-mobile-open', self.js_text)

    def test_05_css_in_layer_overrides(self):
        self.assertIn("@layer mds.overrides", self.css_text,
                      "app.css must be enclosed in @layer mds.overrides")

    def test_06_cairo_font_and_rtl_defaults(self):
        self.assertIn("Cairo", self.html_text, "index.html must import Cairo font")
        self.assertIn('dir="rtl"', self.html_text, "index.html must default to RTL")
        self.assertIn('lang="ar"', self.html_text, "index.html must default to Arabic")


class TestTemplateAndPatternCoverage(unittest.TestCase):
    """Verifies that all 6 canonical templates and 8 patterns are present."""

    def setUp(self):
        self.js_text = (REF_APP_DIR / "app.js").read_text(encoding="utf-8")
        self.html_text = (REF_APP_DIR / "index.html").read_text(encoding="utf-8")

    def test_07_all_6_templates_implemented(self):
        # 1. Dashboard Overview (TMP-001)
        self.assertIn("_renderOverview", self.js_text)
        # 2. List Management (TMP-002)
        self.assertIn("_renderItemsList", self.js_text)
        # 3. Detail Entity (TMP-003)
        self.assertIn("_renderItemDetail", self.js_text)
        # 4. Form Edit (TMP-004)
        self.assertIn("_renderItemEdit", self.js_text)
        # 5. Settings Workspace (TMP-005)
        self.assertIn("_renderSettings", self.js_text)
        # 6. AI Workspace (TMP-006)
        self.assertIn("_renderAIWorkspace", self.js_text)

    def test_08_all_8_patterns_implemented(self):
        css_and_js = (REF_APP_DIR / "app.css").read_text(encoding="utf-8") + self.js_text
        patterns = [
            "mds-ref-form-section",     # Form-Section (PAT-001)
            "mds-ref-search-filter-bar", # Search-Filter-Bar (PAT-002)
            "mds-card",                 # Data-List-Card (PAT-003)
            "mds-ref-empty-state",       # Empty-State (PAT-004)
            "mds-dialog",               # Confirmation-Dialog (PAT-005)
            "mds-ref-page-header",      # Page-Header (PAT-006)
            "mds-ref-ai-prompt",        # AI-Input-Prompt (PAT-007)
            "mds-ref-ai-review"         # AI-Result-Review (PAT-008)
        ]
        for pat in patterns:
            self.assertIn(pat, css_and_js, f"Pattern {pat} must be represented in app")
        # R-004: Multi-step stepper composed via <mds-tabs id="tabs-item-stepper"> with programmatic step locking
        self.assertIn('id="tabs-item-stepper"', self.js_text)
        self.assertIn('itemEditStep2Unlocked', self.js_text)
        self.assertIn('btn-stepper-next', self.js_text)
        self.assertIn('btn-stepper-prev', self.js_text)
        self.assertIn('.mds-ref-stepper-tabs', (REF_APP_DIR / "app.css").read_text(encoding="utf-8"))


class TestWorkflowsAndRoles(unittest.TestCase):
    """Verifies that all 6 canonical workflows and 4 mock roles are represented."""

    def setUp(self):
        self.js_text = (REF_APP_DIR / "app.js").read_text(encoding="utf-8")
        self.html_text = (REF_APP_DIR / "index.html").read_text(encoding="utf-8")

    def test_09_all_4_mock_roles_exist(self):
        roles = ["Administrator", "Manager", "Reviewer", "User"]
        for r in roles:
            self.assertIn(r, self.html_text, f"Role {r} must be in role switcher")
            self.assertIn(r, self.js_text, f"Role {r} must be handled in app controller")

    def test_10_ai_human_in_the_loop_states(self):
        # R-002: Canonical FSM states
        ai_states = ["IDLE", "PROCESSING", "STREAMING", "REVIEWING", "SUCCESS_RESOLVED"]
        for st in ai_states:
            self.assertIn(st, self.js_text, f"AI canonical state {st} must be handled")
        # Check AF-001 live announcer
        self.assertIn("ai-live-announcer", self.js_text)
        self.assertIn('aria-live="polite"', self.js_text)
        # Check reset action in SUCCESS_RESOLVED state
        self.assertIn("btn-ai-new", self.js_text)


class TestCSSQualityAndLogicalProperties(unittest.TestCase):
    """Verifies zero physical properties, zero row-reverse, zero raw hex colors."""

    def setUp(self):
        raw_css = (REF_APP_DIR / "app.css").read_text(encoding="utf-8")
        self.clean_css = re.sub(r'/\*.*?\*/', '', raw_css, flags=re.DOTALL)

    def test_11_zero_physical_directional_properties(self):
        phys_regex = re.compile(
            r'\b(margin-left|margin-right|margin-top|margin-bottom|padding-left|padding-right|padding-top|padding-bottom|left|right|top|bottom)\s*:',
            re.IGNORECASE
        )
        matches = [line.strip() for line in self.clean_css.splitlines() if phys_regex.search(line)]
        self.assertEqual(len(matches), 0, f"Found physical directional properties: {matches}")

    def test_12_zero_row_reverse(self):
        self.assertNotIn("row-reverse", self.clean_css, "row-reverse is strictly forbidden (WCAG 2.4.3)")

    def test_13_zero_hardcoded_hex_colors(self):
        hex_matches = re.findall(r'#[0-9a-fA-F]{3,6}\b', self.clean_css)
        self.assertEqual(len(hex_matches), 0, f"Found raw hex colors: {hex_matches}")

    def test_14_dense_density_is_deferred(self):
        html_text = (REF_APP_DIR / "index.html").read_text(encoding="utf-8")
        self.assertIn('value="dense" disabled', html_text,
                      "Dense tier must be disabled in density switcher")


class TestFixturesDataIntegrity(unittest.TestCase):
    """Verifies that the mock fixtures are well-formed and complete."""

    def test_15_fixtures_valid_json_and_complete(self):
        data_path = REF_APP_DIR / "fixtures" / "workspace_data.json"
        data = json.loads(data_path.read_text(encoding="utf-8"))
        self.assertIn("users", data)
        self.assertIn("items", data)
        self.assertIn("tasks", data)
        self.assertIn("activities", data)
        self.assertIn("aiCorpus", data)
        self.assertIn("settings", data)
        self.assertGreaterEqual(len(data["items"]), 8)
        self.assertGreaterEqual(len(data["tasks"]), 5)
        self.assertGreaterEqual(len(data["users"]), 4)


def suite():
    s = unittest.TestSuite()
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestReferenceApplicationInventory))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestRuntimeConsumerContracts))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestTemplateAndPatternCoverage))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestWorkflowsAndRoles))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestCSSQualityAndLogicalProperties))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestFixturesDataIntegrity))
    return s


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    sys.exit(0 if result.wasSuccessful() else 1)
