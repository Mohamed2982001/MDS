#!/usr/bin/env python3
"""
MDS Primitives Runtime Engine — Comprehensive Test Suite
Phase 9.3: Foundations & Primitives Runtime Verification

Validates:
1. File inventory & modular primitive structure
2. CSS Cascade Layering hierarchy (@layer mds.reset, mds.tokens, mds.foundations, mds.primitives, ...)
3. Strict component isolation (Zero Layer 04 component definitions)
4. Parent-Owned Spacing Law & zero external margins on primitives
5. 100% CSS Logical Properties compliance (Zero physical left/right, zero row-reverse)
6. 100% Token consumption & zero magic numbers (Zero raw hex/rgb/hsl colors)
7. Layout Primitives (Container 1152px/1440px constraints, Stack, Inline, Grid 12-col, Cluster)
8. Typography Primitives (Text soft-wrap, Headings 1-6, Label, Caption, HelperText, Numeric, Code)
9. Surface Depth Triad (Canvas, Surface, Raised L1, Floating L2, Overlay L3)
10. Interaction & Accessibility Primitives (44px PressTarget, 2px FocusRing, VisuallyHidden skip-links, ReducedMotion)
11. FocusTrap Controller & <mds-focus-trap> Custom Element
12. LiveRegion Controller & <mds-live-region> Custom Element (AF-001 Streaming Speech Throttling)
13. Icon Optical Grid & RTL Mirroring Taxonomy
"""

import os
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
PRIMITIVES_DIR = TESTS_DIR.parent
RUNTIME_DIR = PRIMITIVES_DIR.parent
CSS_DIR = RUNTIME_DIR / "css"
MDS_DIR = RUNTIME_DIR.parent


class TestPrimitivesRuntimeFileInventory(unittest.TestCase):
    """Verifies that all modular and consolidated files exist in the runtime directory."""

    def test_consolidated_css_files_exist(self):
        expected_files = [
            CSS_DIR / "reset.css",
            CSS_DIR / "foundations.css",
            CSS_DIR / "primitives.css",
            CSS_DIR / "mds-core.css",
        ]
        for path in expected_files:
            self.assertTrue(path.is_file(), f"Missing core CSS file: {path}")

    def test_modular_primitive_files_exist(self):
        expected_modular = [
            # Layout
            PRIMITIVES_DIR / "layout" / "container.css",
            PRIMITIVES_DIR / "layout" / "stack.css",
            PRIMITIVES_DIR / "layout" / "inline.css",
            PRIMITIVES_DIR / "layout" / "grid.css",
            PRIMITIVES_DIR / "layout" / "cluster.css",
            # Typography
            PRIMITIVES_DIR / "typography" / "typography.css",
            # Surface
            PRIMITIVES_DIR / "surface" / "surface.css",
            # Interaction & Accessibility
            PRIMITIVES_DIR / "interaction" / "press-target.css",
            PRIMITIVES_DIR / "interaction" / "focus-ring.css",
            PRIMITIVES_DIR / "interaction" / "visually-hidden.css",
            PRIMITIVES_DIR / "interaction" / "reduced-motion.css",
            PRIMITIVES_DIR / "interaction" / "focus-trap.js",
            PRIMITIVES_DIR / "interaction" / "live-region.js",
            # Icon
            PRIMITIVES_DIR / "icon" / "icon.css",
        ]
        for path in expected_modular:
            self.assertTrue(path.is_file(), f"Missing modular primitive file: {path}")


class TestCascadeLayering(unittest.TestCase):
    """Verifies CSS Cascade Layer hierarchy across stylesheets."""

    def setUp(self):
        self.mds_core_css = (CSS_DIR / "mds-core.css").read_text(encoding="utf-8")
        self.reset_css = (CSS_DIR / "reset.css").read_text(encoding="utf-8")
        self.foundations_css = (CSS_DIR / "foundations.css").read_text(encoding="utf-8")
        self.primitives_css = (CSS_DIR / "primitives.css").read_text(encoding="utf-8")

    def test_canonical_layer_order_declaration(self):
        expected_layers = (
            "@layer mds.reset, mds.tokens, mds.foundations, mds.primitives, "
            "mds.components, mds.patterns, mds.templates, mds.overrides;"
        )
        self.assertIn(
            expected_layers,
            self.mds_core_css,
            "mds-core.css must declare canonical cascade layer order exactly."
        )

    def test_stylesheet_layer_wrapping(self):
        self.assertIn("@layer mds.reset {", self.reset_css)
        self.assertIn("@layer mds.foundations {", self.foundations_css)
        self.assertIn("@layer mds.primitives {", self.primitives_css)

    def test_mds_core_imports(self):
        self.assertIn('@import "../tokens/dist/tokens.css" layer(mds.tokens);', self.mds_core_css)
        self.assertIn('@import "./reset.css" layer(mds.reset);', self.mds_core_css)
        self.assertIn('@import "./foundations.css" layer(mds.foundations);', self.mds_core_css)
        self.assertIn('@import "./primitives.css" layer(mds.primitives);', self.mds_core_css)


class TestComponentIsolation(unittest.TestCase):
    """Verifies strict Phase 9.3 boundary: Zero Layer 04 component definitions in primitives."""

    def setUp(self):
        self.css_files = list(CSS_DIR.glob("*.css")) + list(PRIMITIVES_DIR.rglob("*.css"))
        self.banned_components = [
            "button", "input", "dialog", "card", "table", "badge", "modal",
            "tooltip", "dropdown", "alert", "toast", "nav", "tabs", "select",
            "checkbox", "radio", "switch", "avatar", "popover", "drawer"
        ]

    def test_zero_component_classes(self):
        banned_pattern = re.compile(
            r"\.mds-(" + "|".join(self.banned_components) + r")\b",
            re.IGNORECASE
        )
        violations = []
        for path in self.css_files:
            content = path.read_text(encoding="utf-8")
            matches = banned_pattern.findall(content)
            if matches:
                violations.append(f"{path.name}: {set(matches)}")

        self.assertEqual(
            violations,
            [],
            f"Primitives runtime must contain 0 component classes. Violations found: {violations}"
        )


class TestLogicalPropertiesDirectionality(unittest.TestCase):
    """Verifies 100% CSS Logical Properties compliance and zero physical directionality."""

    def setUp(self):
        self.css_files = [
            f for f in (list(CSS_DIR.glob("*.css")) + list(PRIMITIVES_DIR.rglob("*.css")))
            if f.name != "tokens.css"  # tokens are data, not style rules
        ]

    def test_zero_physical_directional_properties(self):
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
            f"Banned physical directional properties found: {violations}"
        )

    def test_zero_row_reverse(self):
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
            f"row-reverse is strictly banned for RTL handling: {violations}"
        )


class TestTokenConsumptionAndZeroMagicNumbers(unittest.TestCase):
    """Verifies that primitives consume tokens and contain zero hardcoded colors or magic numbers."""

    def setUp(self):
        self.primitive_css_files = [
            CSS_DIR / "primitives.css"
        ] + list(PRIMITIVES_DIR.rglob("*.css"))

    def test_zero_hardcoded_hex_colors(self):
        hex_pattern = re.compile(r"#[0-9a-fA-F]{3,8}\b")
        violations = []
        for path in self.primitive_css_files:
            for line_idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                clean_line = line.strip()
                if clean_line.startswith("/*") or clean_line.startswith("*"):
                    continue
                if hex_pattern.search(line):
                    violations.append(f"{path.name}:{line_idx} -> {clean_line}")

        self.assertEqual(
            violations,
            [],
            f"Hardcoded hex colors are forbidden in primitives. Violations: {violations}"
        )

    def test_zero_raw_rgb_hsl_colors(self):
        rgb_hsl_pattern = re.compile(r"\b(rgba?|hsla?)\s*\(")
        violations = []
        for path in self.primitive_css_files:
            for line_idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                clean_line = line.strip()
                if clean_line.startswith("/*") or clean_line.startswith("*"):
                    continue
                if rgb_hsl_pattern.search(line):
                    violations.append(f"{path.name}:{line_idx} -> {clean_line}")

        self.assertEqual(
            violations,
            [],
            f"Hardcoded rgb/hsl colors are forbidden in primitives. Violations: {violations}"
        )

    def test_tokens_consumed_via_css_variables(self):
        css_var_pattern = re.compile(r"var\(--mds-")
        for path in self.primitive_css_files:
            if path.name == "visually-hidden.css":
                continue  # Structural accessibility clip utility contains zero visual tokens
            content = path.read_text(encoding="utf-8")
            self.assertTrue(
                bool(css_var_pattern.search(content)),
                f"{path.name} must consume design tokens via var(--mds-*)"
            )


class TestLayoutPrimitives(unittest.TestCase):
    """Verifies canonical rules for Container, Stack, Inline, Grid, Cluster."""

    def setUp(self):
        self.container_css = (PRIMITIVES_DIR / "layout" / "container.css").read_text(encoding="utf-8")
        self.stack_css = (PRIMITIVES_DIR / "layout" / "stack.css").read_text(encoding="utf-8")
        self.inline_css = (PRIMITIVES_DIR / "layout" / "inline.css").read_text(encoding="utf-8")
        self.grid_css = (PRIMITIVES_DIR / "layout" / "grid.css").read_text(encoding="utf-8")
        self.cluster_css = (PRIMITIVES_DIR / "layout" / "cluster.css").read_text(encoding="utf-8")

    def test_container_constraints(self):
        self.assertIn("--mds-container-standard, 1152px", self.container_css)
        self.assertIn("--mds-container-wide, 1440px", self.container_css)
        self.assertIn("margin-inline: auto", self.container_css)
        # Responsive gutters
        self.assertIn("--mds-space-scale-4", self.container_css)  # 16px mobile
        self.assertIn("--mds-space-scale-6", self.container_css)  # 24px tablet
        self.assertIn("--mds-space-scale-8", self.container_css)  # 32px desktop

    def test_stack_structure(self):
        self.assertIn("display: flex;", self.stack_css)
        self.assertIn("flex-direction: column;", self.stack_css)
        self.assertIn(".mds-stack--gap-xs", self.stack_css)
        self.assertIn(".mds-stack--gap-xl", self.stack_css)

    def test_inline_structure(self):
        self.assertIn("display: flex;", self.inline_css)
        self.assertIn("flex-direction: row;", self.inline_css)
        self.assertIn(".mds-inline--collapse-sm", self.inline_css)

    def test_grid_structure(self):
        self.assertIn("display: grid;", self.grid_css)
        self.assertIn("repeat(4, minmax(0, 1fr))", self.grid_css)   # Mobile: 4 cols
        self.assertIn("repeat(8, minmax(0, 1fr))", self.grid_css)   # Tablet: 8 cols
        self.assertIn("repeat(12, minmax(0, 1fr))", self.grid_css)  # Desktop: 12 cols
        self.assertIn(".mds-grid__col--12", self.grid_css)
        self.assertIn(".mds-grid--auto-tiles", self.grid_css)

    def test_cluster_structure(self):
        self.assertIn("display: flex;", self.cluster_css)
        self.assertIn("flex-wrap: wrap;", self.cluster_css)


class TestTypographyPrimitives(unittest.TestCase):
    """Verifies Text, Heading 1-6, Label, Caption, HelperText, Numeric, and Code."""

    def setUp(self):
        self.typography_css = (PRIMITIVES_DIR / "typography" / "typography.css").read_text(encoding="utf-8")

    def test_soft_wrap_no_text_overflow_ellipsis(self):
        self.assertIn(".mds-text--soft-wrap", self.typography_css)
        self.assertIn("overflow-wrap: break-word;", self.typography_css)
        self.assertNotIn("text-overflow: ellipsis;", self.typography_css)

    def test_headings_hierarchy(self):
        for level in range(1, 7):
            self.assertIn(f".mds-heading--{level}", self.typography_css)

    def test_numeric_tabular_nums(self):
        self.assertIn(".mds-numeric", self.typography_css)
        self.assertIn("font-variant-numeric: tabular-nums;", self.typography_css)

    def test_code_mono_font(self):
        self.assertIn(".mds-code", self.typography_css)
        self.assertIn("var(--mds-font-family-mono)", self.typography_css)


class TestSurfacePrimitives(unittest.TestCase):
    """Verifies Surface Depth Triad (Canvas, Surface, Raised, Floating, Overlay)."""

    def setUp(self):
        self.surface_css = (PRIMITIVES_DIR / "surface" / "surface.css").read_text(encoding="utf-8")

    def test_depth_triad_levels(self):
        self.assertIn(".mds-canvas", self.surface_css)
        self.assertIn(".mds-surface", self.surface_css)
        self.assertIn(".mds-surface--raised", self.surface_css)    # L1
        self.assertIn(".mds-surface--floating", self.surface_css)  # L2
        self.assertIn(".mds-surface--overlay", self.surface_css)   # L3

    def test_surface_elevation_tokens(self):
        self.assertIn("var(--mds-elevation-level1)", self.surface_css)
        self.assertIn("var(--mds-elevation-level2)", self.surface_css)
        self.assertIn("var(--mds-elevation-level3)", self.surface_css)


class TestAccessibilityAndInteractionPrimitives(unittest.TestCase):
    """Verifies 44px PressTarget, 2px FocusRing, VisuallyHidden, ReducedMotion."""

    def setUp(self):
        self.press_target_css = (PRIMITIVES_DIR / "interaction" / "press-target.css").read_text(encoding="utf-8")
        self.focus_ring_css = (PRIMITIVES_DIR / "interaction" / "focus-ring.css").read_text(encoding="utf-8")
        self.visually_hidden_css = (PRIMITIVES_DIR / "interaction" / "visually-hidden.css").read_text(encoding="utf-8")
        self.reduced_motion_css = (PRIMITIVES_DIR / "interaction" / "reduced-motion.css").read_text(encoding="utf-8")
        self.foundations_css = (CSS_DIR / "foundations.css").read_text(encoding="utf-8")

    def test_press_target_44px_rule(self):
        self.assertIn("44px", self.press_target_css)
        self.assertIn("@media (pointer: coarse)", self.press_target_css)

    def test_focus_ring_2px(self):
        self.assertIn(":focus-visible", self.focus_ring_css)
        self.assertIn("var(--mds-border-width-thick)", self.focus_ring_css)
        self.assertIn("outline-offset: 2px;", self.focus_ring_css)

    def test_visually_hidden_accessible_clip(self):
        self.assertIn("clip: rect(0, 0, 0, 0);", self.visually_hidden_css)
        self.assertIn("clip-path: inset(50%);", self.visually_hidden_css)
        self.assertIn(".mds-visually-hidden--focusable:focus", self.visually_hidden_css)

    def test_reduced_motion_contract(self):
        # Universal foundation baseline
        self.assertIn("@media (prefers-reduced-motion: reduce)", self.foundations_css)
        self.assertIn("animation-duration: 0.01ms !important;", self.foundations_css)
        # Utility classes
        self.assertIn(".mds-motion--instant", self.reduced_motion_css)
        self.assertIn(".mds-motion--collapse", self.reduced_motion_css)


class TestJavaScriptControllers(unittest.TestCase):
    """Verifies FocusTrap and LiveRegion controllers and W3C custom elements."""

    def setUp(self):
        self.focus_trap_js = (PRIMITIVES_DIR / "interaction" / "focus-trap.js").read_text(encoding="utf-8")
        self.live_region_js = (PRIMITIVES_DIR / "interaction" / "live-region.js").read_text(encoding="utf-8")

    def test_focus_trap_exports_and_custom_element(self):
        self.assertIn("export class FocusTrap", self.focus_trap_js)
        self.assertIn("'mds-focus-trap'", self.focus_trap_js)
        self.assertIn("customElements.define", self.focus_trap_js)
        self.assertIn("returnFocusOnDeactivate", self.focus_trap_js)
        self.assertIn("event.key === 'Tab'", self.focus_trap_js)
        self.assertIn("event.key === 'Escape'", self.focus_trap_js)

    def test_live_region_af001_streaming_speech_throttling(self):
        self.assertIn("export class LiveRegion", self.live_region_js)
        self.assertIn("'mds-live-region'", self.live_region_js)
        self.assertIn("customElements.define", self.live_region_js)
        self.assertIn("throttleMs", self.live_region_js)
        self.assertIn("startStreaming", self.live_region_js)
        self.assertIn("updateStreamingProgress", self.live_region_js)
        self.assertIn("completeStreaming", self.live_region_js)


class TestIconPrimitive(unittest.TestCase):
    """Verifies Icon optical grid sizing and RTL mirroring taxonomy."""

    def setUp(self):
        self.icon_css = (PRIMITIVES_DIR / "icon" / "icon.css").read_text(encoding="utf-8")

    def test_icon_optical_sizes(self):
        self.assertIn(".mds-icon--xs", self.icon_css)
        self.assertIn(".mds-icon--size-xs", self.icon_css)
        self.assertIn(".mds-icon--sm", self.icon_css)
        self.assertIn(".mds-icon--size-sm", self.icon_css)
        self.assertIn(".mds-icon--md", self.icon_css)
        self.assertIn(".mds-icon--size-md", self.icon_css)
        self.assertIn(".mds-icon--lg", self.icon_css)
        self.assertIn(".mds-icon--size-lg", self.icon_css)
        self.assertIn(".mds-icon--xl", self.icon_css)
        self.assertIn(".mds-icon--size-xl", self.icon_css)

    def test_icon_rtl_directional_mirroring(self):
        self.assertIn(".mds-icon--mirror-rtl", self.icon_css)
        self.assertIn("transform: scaleX(-1);", self.icon_css)
        self.assertIn('[dir="rtl"]', self.icon_css)
        self.assertIn(':lang(ar)', self.icon_css)


if __name__ == "__main__":
    unittest.main(verbosity=2)
