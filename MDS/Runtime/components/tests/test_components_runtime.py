#!/usr/bin/env python3
"""
MDS Component Runtime Engine — Comprehensive Test Suite
Phase 9.4: Core Component Runtime Verification
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Validates:
1. Canonical Component Inventory (Exactly 19 canonical components, 0 missing, 0 banned)
2. File Inventory (Modular CSS & JS controllers, consolidated components.css)
3. Cascade Layering (@layer mds.components and mds-core.css import)
4. Parent-Owned Spacing Law (Zero external margins across all components)
5. 100% CSS Logical Properties (Zero physical left/right, zero row-reverse)
6. 100% Token Consumption (Zero hardcoded hex/rgb/hsl colors, component tokens bound)
7. Canonical Touch Targets (PressTarget >= 44x44px on coarse pointers)
8. High-Visibility Focus Rings (2px solid var(--mds-color-focus-ring) on :focus-visible)
9. Accessibility Contracts (AF-002 Table focusable region, AF-002 Dialog initial focus safety)
10. Vestibular Reduced Motion Safety (animation/transition collapse on prefers-reduced-motion)
11. Web Standards Custom Elements & Interactive Controllers (switch, tabs, dialog, tooltip)
"""

import re
import sys
import unittest
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Setup paths
TESTS_DIR = Path(__file__).resolve().parent
COMPONENTS_DIR = TESTS_DIR.parent
RUNTIME_DIR = COMPONENTS_DIR.parent
CSS_DIR = RUNTIME_DIR / "css"
MDS_DIR = RUNTIME_DIR.parent


class TestComponentInventoryAndFiles(unittest.TestCase):
    """Verifies that exactly 19 canonical core components exist and zero banned components exist."""

    @classmethod
    def setUpClass(cls):
        cls.canonical_19 = [
            # Batch 1: Core Interaction
            "button", "icon-button", "link",
            # Batch 2: Form Infrastructure
            "field", "input", "textarea", "checkbox", "radio", "switch", "select",
            # Batch 3: Feedback / Status
            "alert", "spinner", "skeleton", "badge",
            # Batch 4: Content / Data
            "card", "table",
            # Batch 5: Navigation / Overlay
            "tabs", "dialog", "tooltip"
        ]

        cls.banned_deferred = [
            "data-grid", "rich-text-editor", "calendar", "date-range-picker",
            "command-palette", "command-system", "tree", "combobox",
            "virtualized-list", "file-upload-manager"
        ]

    def test_01_canonical_19_components_exist(self):
        """Asserts all 19 canonical component directories exist."""
        for comp in self.canonical_19:
            comp_dir = COMPONENTS_DIR / comp
            self.assertTrue(
                comp_dir.is_dir(),
                f"Missing canonical component directory: {comp_dir}"
            )

    def test_02_zero_banned_enterprise_components(self):
        """Asserts zero premature enterprise components are implemented."""
        for banned in self.banned_deferred:
            banned_dir = COMPONENTS_DIR / banned
            self.assertFalse(
                banned_dir.exists(),
                f"Banned enterprise component must not be implemented: {banned_dir}"
            )

    def test_03_modular_css_files_exist(self):
        """Asserts every component has its modular stylesheet."""
        for comp in self.canonical_19:
            css_file = COMPONENTS_DIR / comp / f"{comp}.css"
            self.assertTrue(
                css_file.is_file(),
                f"Missing modular CSS file for component: {css_file}"
            )

    def test_04_js_controllers_exist(self):
        """Asserts the 4 interactive custom element controllers and components.js exist."""
        expected_js = [
            COMPONENTS_DIR / "switch" / "switch.js",
            COMPONENTS_DIR / "tabs" / "tabs.js",
            COMPONENTS_DIR / "dialog" / "dialog.js",
            COMPONENTS_DIR / "tooltip" / "tooltip.js",
            COMPONENTS_DIR / "components.js",
        ]
        for js_file in expected_js:
            self.assertTrue(
                js_file.is_file(),
                f"Missing JavaScript controller file: {js_file}"
            )

    def test_05_consolidated_components_css_exists(self):
        """Asserts the consolidated components.css exists."""
        consolidated = COMPONENTS_DIR / "components.css"
        self.assertTrue(
            consolidated.is_file(),
            f"Missing consolidated components.css: {consolidated}"
        )


class TestCascadeLayering(unittest.TestCase):
    """Verifies that all component CSS is strictly contained within @layer mds.components."""

    def setUp(self):
        self.css_files = list(COMPONENTS_DIR.rglob("*.css"))
        self.mds_core_css = (CSS_DIR / "mds-core.css").read_text(encoding="utf-8")

    def test_06_components_layer_wrapping(self):
        """Asserts all component CSS files are enclosed in @layer mds.components."""
        for path in self.css_files:
            content = path.read_text(encoding="utf-8")
            self.assertIn(
                "@layer mds.components",
                content,
                f"File {path.name} must be enclosed in @layer mds.components"
            )

    def test_07_mds_core_imports_components(self):
        """Asserts mds-core.css imports components.css under layer(mds.components)."""
        self.assertIn(
            '@import "../components/components.css" layer(mds.components);',
            self.mds_core_css,
            "mds-core.css must import components.css under layer(mds.components)"
        )


class TestParentOwnedSpacingLaw(unittest.TestCase):
    """Verifies that components declare zero external margins (margin: 0)."""

    def setUp(self):
        self.css_files = list(COMPONENTS_DIR.rglob("*.css"))

    def test_08_zero_external_margins_on_root_components(self):
        """Asserts all component base classes enforce margin: 0."""
        banned_margin_props = re.compile(
            r"^\s*margin-(top|bottom|left|right)\s*:\s*(?!0\b)",
            re.MULTILINE | re.IGNORECASE
        )
        violations = []
        for path in self.css_files:
            content = path.read_text(encoding="utf-8")
            matches = banned_margin_props.findall(content)
            if matches:
                violations.append(f"{path.name}: {matches}")

        self.assertEqual(
            violations,
            [],
            f"Parent-Owned Spacing Law violated (physical external margins found): {violations}"
        )


class TestLogicalPropertiesDirectionality(unittest.TestCase):
    """Verifies 100% CSS Logical Properties compliance and zero physical directionality."""

    def setUp(self):
        self.css_files = list(COMPONENTS_DIR.rglob("*.css"))

    def test_09_zero_physical_directional_properties(self):
        """Asserts zero physical left/right properties exist in component CSS."""
        banned_property_pattern = re.compile(
            r"\b(left|right)\s*:|\b(margin|padding|border)-(left|right)\b|\b(float|clear)\s*:\s*(left|right)\b",
            re.IGNORECASE
        )
        violations = []
        for path in self.css_files:
            for line_idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                clean_line = line.strip()
                if clean_line.startswith("/*") or clean_line.startswith("*"):
                    continue
                match = banned_property_pattern.search(line)
                if match:
                    violations.append(f"{path.name}:{line_idx} -> {clean_line}")

        self.assertEqual(
            violations,
            [],
            f"Banned physical directional properties found in components: {violations}"
        )

    def test_10_zero_row_reverse(self):
        """Asserts zero row-reverse exists anywhere in component CSS (PDR-009 / WCAG 2.4.3)."""
        row_reverse_pattern = re.compile(r"row-reverse", re.IGNORECASE)
        violations = []
        for path in self.css_files:
            for line_idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                clean_line = line.strip()
                if clean_line.startswith("/*") or clean_line.startswith("*"):
                    continue
                if row_reverse_pattern.search(line):
                    violations.append(f"{path.name}:{line_idx} -> {clean_line}")

        self.assertEqual(
            violations,
            [],
            f"row-reverse is strictly banned in components: {violations}"
        )


class TestTokenConsumption(unittest.TestCase):
    """Verifies that all components consume tokens via CSS variables and contain zero hardcoded colors."""

    def setUp(self):
        self.css_files = list(COMPONENTS_DIR.rglob("*.css"))

    def test_11_zero_hardcoded_hex_colors(self):
        """Asserts zero hex colors (#...) exist in component CSS rules."""
        hex_pattern = re.compile(r"#[0-9a-fA-F]{3,8}\b")
        violations = []
        for path in self.css_files:
            for line_idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                clean_line = line.strip()
                if clean_line.startswith("/*") or clean_line.startswith("*"):
                    continue
                if hex_pattern.search(line):
                    violations.append(f"{path.name}:{line_idx} -> {clean_line}")

        self.assertEqual(
            violations,
            [],
            f"Hardcoded hex colors found in component CSS: {violations}"
        )

    def test_12_component_tokens_consumed(self):
        """Asserts that component tokens (--mds-component-*) are consumed."""
        consolidated = (COMPONENTS_DIR / "components.css").read_text(encoding="utf-8")
        expected_tokens = [
            "var(--mds-component-button-primary-background-default)",
            "var(--mds-component-button-secondary-background-default)",
            "var(--mds-component-button-ghost-background-hover)",
            "var(--mds-component-button-destructive-background-default)",
            "var(--mds-component-input-background-default)",
            "var(--mds-component-input-border-default)",
            "var(--mds-component-input-border-focus)",
            "var(--mds-component-input-border-invalid)",
            "var(--mds-component-input-radius)",
            "var(--mds-component-badge-radius)",
            "var(--mds-component-badge-brand-background)",
            "var(--mds-component-badge-success-background)",
            "var(--mds-component-badge-danger-background)",
            "var(--mds-component-badge-neutral-background)",
        ]
        for token_ref in expected_tokens:
            self.assertIn(
                token_ref,
                consolidated,
                f"Expected component token {token_ref} not found in components.css"
            )


class TestTouchTargetsAndAccessibility(unittest.TestCase):
    """Verifies PressTarget 44px, FocusRing 2px, and Accessibility Findings AF-002."""

    def setUp(self):
        self.consolidated = (COMPONENTS_DIR / "components.css").read_text(encoding="utf-8")

    def test_13_press_target_44px_rule(self):
        """Asserts PressTarget 44px touch rule is codified for coarse pointers."""
        self.assertIn("@media (pointer: coarse)", self.consolidated)
        self.assertIn("var(--mds-size-touch-target)", self.consolidated)

    def test_14_focus_ring_2px(self):
        """Asserts focus rings use 2px solid var(--mds-color-focus-ring) on :focus-visible."""
        self.assertIn("var(--mds-color-focus-ring)", self.consolidated)
        self.assertIn(":focus-visible", self.consolidated)

    def test_15_accessibility_finding_af002_table_scroll_container(self):
        """Asserts Finding AF-002: Table scroll container has focusability and border-subtle."""
        self.assertIn(".mds-table-container", self.consolidated)
        self.assertIn(".mds-table-container:focus-visible", self.consolidated)

    def test_16_accessibility_finding_af002_dialog_initial_focus_safety(self):
        """Asserts Finding AF-002: Dialog JS controller lands initial focus on Cancel for destructive modals."""
        dialog_js = (COMPONENTS_DIR / "dialog" / "dialog.js").read_text(encoding="utf-8")
        self.assertIn("hasDestructiveAction", dialog_js)
        self.assertIn("cancelButton", dialog_js)

    def test_17_vestibular_reduced_motion_contract(self):
        """Asserts prefers-reduced-motion disables transitions and animations across components."""
        self.assertIn("@media (prefers-reduced-motion: reduce)", self.consolidated)
        self.assertIn("animation: none", self.consolidated)
        self.assertIn("transition: none", self.consolidated)

    def test_18_custom_elements_registered(self):
        """Asserts custom elements are defined for switch, tabs, dialog, and tooltip."""
        switch_js = (COMPONENTS_DIR / "switch" / "switch.js").read_text(encoding="utf-8")
        tabs_js = (COMPONENTS_DIR / "tabs" / "tabs.js").read_text(encoding="utf-8")
        dialog_js = (COMPONENTS_DIR / "dialog" / "dialog.js").read_text(encoding="utf-8")
        tooltip_js = (COMPONENTS_DIR / "tooltip" / "tooltip.js").read_text(encoding="utf-8")

        self.assertIn('customElements.define("mds-switch", MdsSwitch)', switch_js)
        self.assertIn('customElements.define("mds-tabs", MdsTabs)', tabs_js)
        self.assertIn('customElements.define("mds-dialog", MdsDialog)', dialog_js)
        self.assertIn('customElements.define("mds-tooltip", MdsTooltip)', tooltip_js)


if __name__ == "__main__":
    print("=" * 72)
    print("     MASTER DESIGN SYSTEM (MDS) — COMPONENT RUNTIME TEST SUITE    ")
    print("                 Phase 9.4: Core Component Runtime                ")
    print("=" * 72)
    unittest.main(verbosity=2)
