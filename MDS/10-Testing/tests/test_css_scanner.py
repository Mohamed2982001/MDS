#!/usr/bin/env python3
"""
Unit Tests for MDS Semantic CSS AST Scanner (Layer C)
Phase 9.7.3: Static Validation Suite & Scanners
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Validates all Scope A, B, C, D rules, edge cases, and AST tokenization.
"""

import sys
import unittest
from pathlib import Path

TESTING_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TESTING_DIR))

from static.css_scanner import CssAstScanner, CssScope, ViolationType


class TestCssAstScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = CssAstScanner()

    # 1. Scope A Exemption (Tokens)
    def test_01_scope_a_token_exemption(self):
        css = """
        :root {
            --mds-color-primary: #1e293b;
            --mds-color-accent: #3b82f6;
            margin-left: 20px;
        }
        """
        res = self.scanner.scan_string(css, scope=CssScope.SCOPE_A)
        self.assertTrue(res.is_valid)
        self.assertEqual(len(res.violations), 0)

    # 2. Scope B Hex Detection
    def test_02_scope_b_raw_hex_detected(self):
        css = """
        .my-box {
            color: #ff0000;
            background: #abc;
        }
        """
        res = self.scanner.scan_string(css, scope=CssScope.SCOPE_B)
        self.assertFalse(res.is_valid)
        self.assertEqual(len(res.violations), 2)
        self.assertEqual(res.violations[0].violation_type, ViolationType.RAW_HEX_COLOR)
        self.assertIn("#ff0000", res.violations[0].message)

    # 3. ID Selector Distinction (Must NOT be flagged as hex color)
    def test_03_id_selector_not_flagged_as_hex(self):
        css = """
        #overview {
            color: var(--mds-color-text-primary);
        }
        #app {
            background-color: var(--mds-color-surface-canvas);
        }
        #def {
            border-color: var(--mds-color-border-subtle);
        }
        """
        res = self.scanner.scan_string(css, scope=CssScope.SCOPE_B)
        self.assertTrue(res.is_valid, f"ID selectors falsely flagged as hex: {res.violations}")

    # 4. SVG URL Fragment References (Must NOT be flagged as hex)
    def test_04_svg_url_fragment_not_flagged(self):
        css = """
        .masked-element {
            clip-path: url(#clip);
            filter: url('#filter');
            mask: url("#mask1");
        }
        """
        res = self.scanner.scan_string(css, scope=CssScope.SCOPE_B)
        self.assertTrue(res.is_valid, f"SVG url fragment falsely flagged: {res.violations}")

    # 5. Comment Stripping
    def test_05_comments_stripped_cleanly(self):
        css = """
        /* This is a comment containing #ff0000 and margin-left: 10px */
        .safe-class {
            color: var(--mds-color-text-primary); /* inline #123456 */
        }
        """
        res = self.scanner.scan_string(css, scope=CssScope.SCOPE_B)
        self.assertTrue(res.is_valid, f"Comment content falsely flagged: {res.violations}")

    # 6. Physical Directional Properties (Banned in Scope B)
    def test_06_physical_properties_detected(self):
        css = """
        .bad-spacing {
            margin-left: 16px;
            padding-right: 8px;
            border-left: 1px solid var(--mds-color-border-subtle);
            left: 0;
            float: right;
        }
        """
        res = self.scanner.scan_string(css, scope=CssScope.SCOPE_B)
        self.assertFalse(res.is_valid)
        self.assertEqual(len(res.violations), 5)
        for v in res.violations:
            self.assertEqual(v.violation_type, ViolationType.PHYSICAL_PROPERTY)

    # 7. Logical Directional Properties (Allowed in Scope B)
    def test_07_logical_properties_allowed(self):
        css = """
        .good-spacing {
            margin-inline-start: var(--mds-space-inline-md);
            padding-inline-end: var(--mds-space-inline-sm);
            border-inline-start: 1px solid var(--mds-color-border-subtle);
            inset-inline-start: 0;
            margin-block-start: var(--mds-space-block-sm);
        }
        """
        res = self.scanner.scan_string(css, scope=CssScope.SCOPE_B)
        self.assertTrue(res.is_valid, f"Logical properties falsely flagged: {res.violations}")

    # 8. Row-Reverse Banned (WCAG 2.4.3 focus order preservation)
    def test_08_row_reverse_detected(self):
        css = """
        .bad-flex {
            flex-direction: row-reverse;
        }
        """
        res = self.scanner.scan_string(css, scope=CssScope.SCOPE_B)
        self.assertFalse(res.is_valid)
        self.assertEqual(len(res.violations), 1)
        self.assertEqual(res.violations[0].violation_type, ViolationType.ROW_REVERSE)

    # 9. Parent-Owned Spacing in Component Stylesheets
    def test_09_component_host_external_margins_detected(self):
        css = """
        .mds-button {
            margin-top: 10px;
        }
        :host {
            margin-left: 20px;
        }
        """
        res = self.scanner.scan_string(css, scope=CssScope.SCOPE_B, file_path="MDS/Runtime/components/button/button.css")
        self.assertFalse(res.is_valid)
        self.assertTrue(any(v.violation_type == ViolationType.HOST_EXTERNAL_MARGIN for v in res.violations))

    # 10. Scope C Allowance (Compiled Distribution in @layer mds.tokens)
    def test_10_scope_c_compiled_tokens_allowed(self):
        css = """
        @layer mds.tokens {
            :root {
                --mds-color-brand-500: #3b82f6;
                --mds-space-4: 16px;
            }
        }
        """
        res = self.scanner.scan_string(css, scope=CssScope.SCOPE_C, file_path="MDS/Runtime/tokens/dist/tokens.css")
        self.assertTrue(res.is_valid, f"Scope C compiled tokens should be allowed: {res.violations}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
