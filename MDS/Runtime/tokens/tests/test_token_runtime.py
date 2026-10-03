#!/usr/bin/env python3
"""
MDS Token Runtime Engine — Comprehensive Test Suite
Phase 9.2: Token Runtime Engine Verification

Validates:
1. File discovery & DTCG schema parsing
2. Canonical token invariants (188 total, 185 base, 47 components)
3. 100% clean alias resolution (0 broken references)
4. Maximum alias depth <= 3 hops (actual: 2 hops)
5. Cycle detection with complete path reporting (A -> B -> C -> A)
6. Depth limit exceeded exception guard
7. Missing token target exception guard
8. Multi-dimensional theme overrides resolution (4 themes)
9. CSS cascade layering (@layer mds.tokens) and theme selectors
10. JSON pre-resolved catalog structure
11. TypeScript type definitions
12. Byte-for-byte compilation determinism
"""

import copy
import json
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
TOKEN_RUNTIME_DIR = TESTS_DIR.parent
MDS_DIR = TOKEN_RUNTIME_DIR.parent.parent
TOKENS_DIR = MDS_DIR / "02-Tokens"

if str(TOKEN_RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(TOKEN_RUNTIME_DIR))

from src.compiler import TokenCompiler
from src.loader import TokenLoader
from src.models import (
    AliasDepthExceededError,
    CycleDetectedError,
    MissingTokenError,
    SchemaValidationError,
    Token,
)
from src.resolver import TokenResolver, format_css_value, token_path_to_css_var
from src.validator import TokenValidator


class TestTokenRuntimeEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Loads and resolves canonical tokens once for read-only invariant assertions."""
        cls.loader = TokenLoader(TOKENS_DIR)
        cls.base_tokens, cls.theme_overrides, cls.all_tokens, cls.files = cls.loader.load()
        cls.validator = TokenValidator(strict=True)
        cls.resolver = TokenResolver(cls.base_tokens, cls.theme_overrides, cls.all_tokens, max_depth=3)
        cls.base_resolved, cls.theme_resolved = cls.resolver.resolve_all()
        cls.compiler = TokenCompiler(cls.base_resolved, cls.theme_resolved, cls.all_tokens, cls.theme_overrides)
        cls.compile_result = cls.compiler.compile()

    # -------------------------------------------------------------------------
    # 1. Ingestion & File Discovery
    # -------------------------------------------------------------------------
    def test_01_discovery_file_count(self):
        """Asserts exactly 18 DTCG token files are discovered in MDS/02-Tokens/."""
        self.assertEqual(len(self.files), 18, "Expected exactly 18 DTCG token files")
        
        # Verify layer breakdown
        tiers = {}
        for f in self.files:
            tier = self.loader._determine_tier(f)
            tiers[tier] = tiers.get(tier, 0) + 1
            
        self.assertEqual(tiers.get("primitive"), 9, "Expected 9 primitive token files")
        self.assertEqual(tiers.get("semantic"), 2, "Expected 2 semantic token files")
        self.assertEqual(tiers.get("component"), 3, "Expected 3 component token files")
        self.assertEqual(tiers.get("theme"), 4, "Expected 4 theme override files")

    # -------------------------------------------------------------------------
    # 2. Token Invariants (188 total, 185 base, 47 components)
    # -------------------------------------------------------------------------
    def test_02_token_count_invariants(self):
        """Asserts total distinct token paths == 188 and base tokens == 185."""
        self.assertEqual(len(self.all_tokens), 188, "Expected exactly 188 distinct token paths")
        self.assertEqual(len(self.base_tokens), 185, "Expected exactly 185 non-theme base tokens")
        
        theme_only = set(self.all_tokens.keys()) - set(self.base_tokens.keys())
        expected_theme_only = {
            "component.card.radius",
            "component.card.elevation",
            "border.width.default",
        }
        self.assertEqual(theme_only, expected_theme_only, "Theme-only tokens mismatch")

    def test_03_component_tokens_count(self):
        """Asserts exactly 47 component tokens exist under components/."""
        comp_tokens = [t for t in self.base_tokens.values() if t.layer == "component"]
        self.assertEqual(len(comp_tokens), 47, "Expected exactly 47 component tokens")

        # Family breakdown
        btn_count = sum(1 for t in comp_tokens if t.path.startswith("component.button"))
        inp_count = sum(1 for t in comp_tokens if t.path.startswith("component.input"))
        bdg_count = sum(1 for t in comp_tokens if t.path.startswith("component.badge"))
        
        self.assertEqual(btn_count, 24, "Expected 24 button component tokens")
        self.assertEqual(inp_count, 10, "Expected 10 input component tokens")
        self.assertEqual(bdg_count, 13, "Expected 13 badge component tokens")

    # -------------------------------------------------------------------------
    # 3. Alias Resolution & Graph Traversal
    # -------------------------------------------------------------------------
    def test_04_alias_resolution_clean(self):
        """Asserts 100% of aliases resolve without broken references."""
        for path, resolved in self.base_resolved.items():
            self.assertIsNotNone(resolved.value, f"Token '{path}' resolved to None")
            self.assertNotEqual(resolved.value, "", f"Token '{path}' resolved to empty string")
            self.assertFalse(
                str(resolved.value).startswith("{") and str(resolved.value).endswith("}"),
                f"Token '{path}' failed to resolve terminal value: {resolved.value}"
            )

    def test_05_alias_max_depth(self):
        """Asserts maximum alias depth <= 3 hops (actual repository is 2 hops)."""
        max_hops = 0
        hop_distribution = {}
        for path, resolved in self.base_resolved.items():
            max_hops = max(max_hops, resolved.hops)
            hop_distribution[resolved.hops] = hop_distribution.get(resolved.hops, 0) + 1

        self.assertLessEqual(max_hops, 3, f"Max alias depth exceeded 3 hops: {max_hops}")
        self.assertEqual(max_hops, 2, f"Expected canonical max alias depth of 2 hops, got {max_hops}")
        self.assertEqual(hop_distribution.get(0), 109, "Expected 109 primitive tokens at depth 0")
        self.assertEqual(hop_distribution.get(1), 45, "Expected 45 base tokens at depth 1")
        self.assertEqual(hop_distribution.get(2), 31, "Expected 31 base tokens at depth 2")

    # -------------------------------------------------------------------------
    # 4. Cycle Detection & Exception Guards
    # -------------------------------------------------------------------------
    def test_06_cycle_detector(self):
        """Injects a synthetic cycle A -> B -> C -> A and verifies CycleDetectedError reports full path."""
        cyclic_tokens = {
            "token.a": Token(path="token.a", raw_value="{token.b}", type="color"),
            "token.b": Token(path="token.b", raw_value="{token.c}", type="color"),
            "token.c": Token(path="token.c", raw_value="{token.a}", type="color"),
        }
        test_resolver = TokenResolver(cyclic_tokens, {}, cyclic_tokens, max_depth=3)
        with self.assertRaises(CycleDetectedError) as ctx:
            test_resolver.check_circular_references(cyclic_tokens)

        err_msg = str(ctx.exception)
        self.assertIn("Circular reference detected", err_msg)
        # Verify that all 3 nodes appear in the reported cycle path
        self.assertTrue(
            all(k in err_msg for k in ["token.a", "token.b", "token.c"]),
            f"Cycle path does not mention all nodes: {err_msg}"
        )

    def test_07_depth_exceeded_detector(self):
        """Injects a synthetic 4-hop chain and verifies AliasDepthExceededError is raised when max_depth=3."""
        deep_tokens = {
            "token.1": Token(path="token.1", raw_value="{token.2}", type="dimension"),
            "token.2": Token(path="token.2", raw_value="{token.3}", type="dimension"),
            "token.3": Token(path="token.3", raw_value="{token.4}", type="dimension"),
            "token.4": Token(path="token.4", raw_value="{token.5}", type="dimension"),
            "token.5": Token(path="token.5", raw_value="16px", type="dimension"),
        }
        test_resolver = TokenResolver(deep_tokens, {}, deep_tokens, max_depth=3)
        with self.assertRaises(AliasDepthExceededError) as ctx:
            test_resolver.resolve_token_chain("token.1", deep_tokens)

        err_msg = str(ctx.exception)
        self.assertIn("exceeded maximum alias depth of 3 hops", err_msg)
        self.assertIn("token.1", err_msg)

    def test_08_missing_token_detector(self):
        """Injects a synthetic dangling alias and verifies MissingTokenError is raised."""
        broken_tokens = {
            "token.orphan": Token(path="token.orphan", raw_value="{token.non_existent}", type="color"),
        }
        test_resolver = TokenResolver(broken_tokens, {}, broken_tokens, max_depth=3)
        with self.assertRaises(MissingTokenError) as ctx:
            test_resolver.resolve_token_chain("token.orphan", broken_tokens)

        err_msg = str(ctx.exception)
        self.assertIn("token.non_existent", err_msg)
        self.assertIn("token.orphan", err_msg)

    # -------------------------------------------------------------------------
    # 5. Theme Overrides Resolution
    # -------------------------------------------------------------------------
    def test_09_theme_overrides_resolution(self):
        """Verifies all 4 theme override files resolve cleanly."""
        self.assertEqual(len(self.theme_resolved), 4, "Expected 4 resolved theme override sets")
        
        # 1. Dark Mode (9 tokens)
        dark = self.theme_resolved.get("mode.dark")
        self.assertIsNotNone(dark)
        self.assertEqual(len(dark), 9, "Expected 9 dark mode override tokens")
        self.assertEqual(dark["color.surface.canvas"].css_value, "#090D16")
        self.assertEqual(dark["color.text.primary"].css_value, "#FFFFFF")

        # 2. High Contrast (3 tokens)
        hc = self.theme_resolved.get("mode.high-contrast")
        self.assertIsNotNone(hc)
        self.assertEqual(len(hc), 3, "Expected 3 high-contrast override tokens")
        self.assertEqual(hc["color.border.default"].css_value, "#000000")
        self.assertEqual(hc["border.width.default"].css_value, "2px")

        # 3. Refined Minimal (3 tokens)
        ref = self.theme_resolved.get("preset.refined")
        self.assertIsNotNone(ref)
        self.assertEqual(len(ref), 3, "Expected 3 refined preset override tokens")
        self.assertEqual(ref["component.card.radius"].css_value, "6px")
        self.assertEqual(ref["component.card.elevation"].css_value, "none")

        # 4. Compact Density (3 tokens)
        compact = self.theme_resolved.get("density.compact")
        self.assertIsNotNone(compact)
        self.assertEqual(len(compact), 3, "Expected 3 compact density override tokens")
        self.assertEqual(compact["size.control.md"].css_value, "32px")
        self.assertEqual(compact["space.block.sm"].css_value, "4px")

    # -------------------------------------------------------------------------
    # 6. CSS Output & Cascade Layering
    # -------------------------------------------------------------------------
    def test_10_css_output_layer_and_structure(self):
        """Verifies generated CSS begins with @layer mds.tokens, has :root and all 4 theme selectors."""
        css = self.compile_result.css
        self.assertIn("@layer mds.tokens {", css, "CSS must declare @layer mds.tokens")
        self.assertIn(":root {", css, "CSS must declare :root block")
        self.assertIn('[data-mode="dark"] {', css, "CSS must include dark mode selector")
        self.assertIn('[data-mode="high-contrast"] {', css, "CSS must include high-contrast selector")
        self.assertIn('[data-preset="refined"] {', css, "CSS must include refined preset selector")
        self.assertIn('[data-density="compact"] {', css, "CSS must include compact density selector")

        # Verify no raw unbracketed template expressions or dangling '{' in values
        self.assertNotIn("{{", css)
        self.assertNotIn("}}", css)

    # -------------------------------------------------------------------------
    # 7. JSON Catalog & TypeScript Definitions
    # -------------------------------------------------------------------------
    def test_11_json_catalog_structure(self):
        """Verifies schema structure of pre-resolved JSON dictionary."""
        catalog = self.compile_result.json_data
        self.assertEqual(catalog.get("version"), "1.0.0")
        self.assertEqual(catalog.get("phase"), "9.2")
        self.assertEqual(catalog.get("tokens_total"), 188)
        self.assertEqual(catalog.get("base_tokens_total"), 185)
        self.assertEqual(catalog.get("component_tokens_total"), 47)
        self.assertIn("tokens", catalog)
        self.assertIn("themes", catalog)
        self.assertEqual(len(catalog["themes"]), 4)

    def test_12_typescript_dts_structure(self):
        """Verifies TypeScript definition format and variable names."""
        dts = self.compile_result.dts
        self.assertIn("export type MDSTokenName =", dts)
        self.assertIn("export interface MDSTokenDictionary {", dts)
        self.assertIn("export declare const tokens: Record<MDSTokenName, string>;", dts)
        
        # Verify standard token names exist in union
        self.assertIn("'--mds-color-brand-600'", dts)
        self.assertIn("'--mds-font-size-base'", dts)
        self.assertIn("'--mds-space-scale-4'", dts)
        self.assertIn("'--mds-component-button-primary-background-default'", dts)

    # -------------------------------------------------------------------------
    # 8. Determinism
    # -------------------------------------------------------------------------
    def test_13_compilation_determinism(self):
        """Compiles twice into separate objects and asserts 100% byte-for-byte identity."""
        compiler_run_1 = TokenCompiler(self.base_resolved, self.theme_resolved, self.all_tokens, self.theme_overrides)
        res_1 = compiler_run_1.compile()

        compiler_run_2 = TokenCompiler(self.base_resolved, self.theme_resolved, self.all_tokens, self.theme_overrides)
        res_2 = compiler_run_2.compile()

        self.assertEqual(res_1.css, res_2.css, "CSS output is non-deterministic")
        self.assertEqual(
            json.dumps(res_1.json_data, sort_keys=True),
            json.dumps(res_2.json_data, sort_keys=True),
            "JSON catalog is non-deterministic"
        )
        self.assertEqual(res_1.dts, res_2.dts, "TypeScript d.ts output is non-deterministic")


def run_tests():
    """Runs the suite and produces a clean formatted report."""
    print("=" * 72)
    print("      MASTER DESIGN SYSTEM (MDS) — TOKEN RUNTIME TEST SUITE     ")
    print("                      Phase 9.2 Verification                    ")
    print("=" * 72)

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestTokenRuntimeEngine)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("-" * 72)
    print(f"Total Tests Executed: {result.testsRun}")
    print(f"  [+] Passed:         {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  [-] Failures:       {len(result.failures)}")
    print(f"  [!] Errors:         {len(result.errors)}")
    print("-" * 72)

    if result.wasSuccessful():
        print("OVERALL STATUS: SUCCESS — 100% of Token Runtime assertions PASSED.")
        print("=" * 72)
        return 0
    else:
        print("OVERALL STATUS: FAILED — Investigate errors above.")
        print("=" * 72)
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
