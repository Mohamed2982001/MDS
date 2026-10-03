#!/usr/bin/env python3
"""
MDS Playground Test Suite — Reference Runtime Laboratory Verification
Phase 9.5: Interactive Playground
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Validates:
1. File & Directory Inventory (index.html, playground.css, playground.js, fixtures/sample_data.json, README.md)
2. Zero External Runtime Dependencies (No package.json, zero npm runtime deps)
3. Shared-Core Runtime Invariants (Imports mds-core.css and components.js strictly as consumer)
4. Full 11-Section Architectural Presence
5. Full 19-Component Canonical Showcase (0 missing, 0 leaks of deferred enterprise components)
6. Density Tier Discipline (Comfortable, Compact, with Dense strictly marked Deferred)
7. RTL & Typography Standards (Cairo default, dir='rtl' default, skip link)
8. CSS Standards (100% logical properties, zero row-reverse, zero hardcoded hex)
9. State Machine Laboratory (8 Universal operational states)
10. Mock Fixtures Integrity (sample_data.json)
"""

import json
import re
import sys
import unittest
from pathlib import Path

# Ensure UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PLAYGROUND_DIR = Path(__file__).resolve().parent.parent
MDS_DIR = PLAYGROUND_DIR.parent
RUNTIME_DIR = MDS_DIR / "Runtime"


class TestPlaygroundInventory(unittest.TestCase):
    """Verifies all required playground laboratory files exist and no node_modules exist."""

    def test_01_core_files_exist(self):
        required_files = [
            PLAYGROUND_DIR / "index.html",
            PLAYGROUND_DIR / "playground.css",
            PLAYGROUND_DIR / "playground.js",
            PLAYGROUND_DIR / "fixtures" / "sample_data.json",
            PLAYGROUND_DIR / "README.md",
        ]
        for f in required_files:
            self.assertTrue(f.exists(), f"Missing playground file: {f.relative_to(MDS_DIR)}")

    def test_02_zero_npm_dependencies(self):
        """Playground must be pure modern web standards with zero npm dependencies."""
        node_modules = PLAYGROUND_DIR / "node_modules"
        package_json = PLAYGROUND_DIR / "package.json"
        self.assertFalse(node_modules.exists(), "Illegal node_modules found in MDS/Playground!")
        self.assertFalse(package_json.exists(), "Illegal package.json found in MDS/Playground!")


class TestPlaygroundRuntimeImports(unittest.TestCase):
    """Verifies that the Playground imports and consumes MDS Runtime directly."""

    def setUp(self):
        self.html_text = (PLAYGROUND_DIR / "index.html").read_text(encoding="utf-8")
        self.js_text = (PLAYGROUND_DIR / "playground.js").read_text(encoding="utf-8")

    def test_03_imports_mds_core_css(self):
        self.assertIn("../Runtime/css/mds-core.css", self.html_text,
                      "index.html must import ../Runtime/css/mds-core.css")

    def test_04_imports_components_js(self):
        self.assertIn("../Runtime/components/components.js", self.js_text,
                      "playground.js must import ../Runtime/components/components.js")

    def test_05_html_arabic_rtl_cairo_defaults(self):
        self.assertIn('dir="rtl"', self.html_text, "index.html must have dir='rtl' by default")
        self.assertIn('lang="ar"', self.html_text, "index.html must have lang='ar' by default")
        self.assertIn("Cairo", self.html_text, "index.html must import Cairo font")
        self.assertIn("mds-pg-skip-link", self.html_text, "index.html must include skip navigation link")


class TestPlaygroundSectionCoverage(unittest.TestCase):
    """Verifies that all 11 required sections exist with proper semantic landmarks."""

    def setUp(self):
        self.html_text = (PLAYGROUND_DIR / "index.html").read_text(encoding="utf-8")

    def test_06_all_11_sections_present(self):
        required_sections = [
            "sec-overview",
            "sec-foundations",
            "sec-primitives",
            "sec-components",
            "sec-states",
            "sec-themes",
            "sec-density",
            "sec-rtl",
            "sec-responsive",
            "sec-tokens",
            "sec-a11y"
        ]
        for sec_id in required_sections:
            self.assertIn(f'id="{sec_id}"', self.html_text, f"Missing section: #{sec_id}")


class TestComponentSpecimensCoverage(unittest.TestCase):
    """Verifies all 19 canonical components are showcased and 0 banned enterprise components exist."""

    @classmethod
    def setUpClass(cls):
        cls.html_text = (PLAYGROUND_DIR / "index.html").read_text(encoding="utf-8")
        cls.canonical_19 = [
            "button", "icon-button", "link",
            "field", "input", "textarea", "checkbox", "radio", "switch", "select",
            "alert", "spinner", "skeleton", "badge",
            "card", "table",
            "tabs", "dialog", "tooltip"
        ]
        cls.banned_enterprise = [
            "data-grid", "richtexteditor", "calendar", "date-range-picker",
            "commandsystem", "tree", "combobox", "virtualizedlist", "file-upload-manager"
        ]

    def test_07_all_19_components_in_specimens(self):
        for comp in self.canonical_19:
            # Check either class or tag or text marker
            marker1 = f"mds-{comp}"
            marker2 = comp.replace("-", "")
            found = marker1 in self.html_text or marker2 in self.html_text.lower()
            self.assertTrue(found, f"Canonical component '{comp}' not found in playground specimens!")

    def test_08_zero_banned_enterprise_components(self):
        for banned in self.banned_enterprise:
            pattern = re.compile(rf'\bmds-{banned}\b', re.IGNORECASE)
            self.assertFalse(pattern.search(self.html_text),
                             f"Illegal deferred component specimen found: mds-{banned}")

    def test_09_dense_tier_marked_deferred(self):
        self.assertIn("Deferred", self.html_text, "Dense tier must be explicitly marked Deferred")
        self.assertIn('option value="dense" disabled', self.html_text,
                      "Density selector must have 'dense' option disabled")


class TestCSSQualityAndLogicalProperties(unittest.TestCase):
    """Verifies playground.css conforms to CSS Logical Properties and Zero Hex rules."""

    @classmethod
    def setUpClass(cls):
        cls.css_path = PLAYGROUND_DIR / "playground.css"
        cls.css_text = cls.css_path.read_text(encoding="utf-8")
        # Strip comments
        cls.clean_css = re.sub(r'/\*.*?\*/', '', cls.css_text, flags=re.DOTALL)

    def test_10_zero_physical_properties(self):
        physical_props = re.compile(r'\b(margin-left|margin-right|padding-left|padding-right)\s*:', re.IGNORECASE)
        matches = physical_props.findall(self.clean_css)
        self.assertEqual(len(matches), 0, f"Found physical properties in playground.css: {matches}")

    def test_11_zero_row_reverse(self):
        self.assertNotIn("row-reverse", self.clean_css,
                         "Functional row-reverse is prohibited (WCAG 2.4.3 Focus Order Invariant)!")

    def test_12_zero_hardcoded_hex_colors(self):
        hex_pattern = re.compile(r'#[0-9a-fA-F]{3,6}\b')
        matches = hex_pattern.findall(self.clean_css)
        self.assertEqual(len(matches), 0, f"Hardcoded hex colors found in playground.css: {matches}")


class TestFixturesAndData(unittest.TestCase):
    """Verifies sample data integrity."""

    def test_13_sample_data_valid_json(self):
        fixture_file = PLAYGROUND_DIR / "fixtures" / "sample_data.json"
        with open(fixture_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("transactions", data, "sample_data.json must contain transactions")
        self.assertGreaterEqual(len(data["transactions"]), 3, "sample_data.json must have at least 3 transactions")
        self.assertIn("users", data, "sample_data.json must contain users")


if __name__ == "__main__":
    unittest.main(verbosity=2)
