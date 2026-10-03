"""
MDS Token Runtime Engine — Token Compiler
Phase 9.2: Token Runtime Engine

Compiles resolved design tokens into deterministic runtime artifacts:
1. CSS custom properties wrapped in @layer mds.tokens (dist/tokens.css)
2. Fast-lookup JSON catalog (dist/tokens.json)
3. TypeScript type definitions (dist/tokens.d.ts)
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import CompileResult, ResolvedToken, ThemeOverride, Token


THEME_ORDER = [
    ("mode.dark", "Dark Mode Luminance Overrides", '[data-mode="dark"]'),
    ("mode.high-contrast", "High Contrast Mode Overrides", '[data-mode="high-contrast"]'),
    ("preset.refined", "Refined Minimal Visual Preset Overrides", '[data-preset="refined"]'),
    ("density.compact", "Compact Density Spatial Overrides", '[data-density="compact"]'),
]


class TokenCompiler:
    """Emits production-ready CSS, JSON, and TypeScript distribution files."""

    def __init__(
        self,
        base_resolved: Dict[str, ResolvedToken],
        theme_resolved: Dict[str, Dict[str, ResolvedToken]],
        all_tokens: Dict[str, Token],
        theme_overrides: Dict[str, ThemeOverride]
    ):
        self.base_resolved = base_resolved
        self.theme_resolved = theme_resolved
        self.all_tokens = all_tokens
        self.theme_overrides = theme_overrides

    def emit_css(self) -> str:
        """
        Generates production CSS custom properties wrapped strictly within @layer mds.tokens.
        Emits :root base definitions followed by scoped theme selectors.
        """
        lines: List[str] = [
            "/**",
            " * MDS (Master Design System) — Compiled CSS Tokens",
            " * Architecture Layer: Layer 13 (Implementation / Token Runtime)",
            " * Source of Truth: MDS/02-Tokens/ (18 DTCG JSON files)",
            " * Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)",
            " * Standard: Native CSS Cascade Layers (@layer mds.tokens)",
            " * Determinism: 100% Deterministic (Alphabetically sorted, zero timestamps)",
            " */",
            "",
            "@layer mds.tokens {",
            "  :root {"
        ]

        # Group tokens logically for cleaner readability while maintaining determinism
        for path in sorted(self.base_resolved.keys()):
            resolved = self.base_resolved[path]
            desc = f" /* {resolved.description} */" if resolved.description else ""
            lines.append(f"    {resolved.css_var_name}: {resolved.css_value};{desc}")

        lines.append("  }")

        # Theme override blocks
        for theme_id, label, selector in THEME_ORDER:
            if theme_id in self.theme_resolved:
                tokens_in_theme = self.theme_resolved[theme_id]
                lines.append("")
                lines.append(f"  /* Theme Overrides: {label} ({len(tokens_in_theme)} tokens) */")
                lines.append(f"  {selector} {{")
                for path in sorted(tokens_in_theme.keys()):
                    resolved = tokens_in_theme[path]
                    desc = f" /* {resolved.description} */" if resolved.description else ""
                    lines.append(f"    {resolved.css_var_name}: {resolved.css_value};{desc}")
                lines.append("  }")

        lines.append("}")
        lines.append("")
        return "\n".join(lines)

    def emit_json(self) -> Dict[str, Any]:
        """
        Generates machine-readable pre-resolved JSON dictionary for AI tooling, tests, and portals.
        Adheres to MDS Token Runtime Architecture Section 4.2.
        """
        tokens_dict: Dict[str, Any] = {}

        # 1. Base tokens
        for path in sorted(self.base_resolved.keys()):
            res = self.base_resolved[path]
            entry: Dict[str, Any] = {
                "value": res.value,
                "css_value": res.css_value,
                "css_var": res.css_var_name,
                "type": res.type,
                "tier": res.tier,
                "hops": res.hops,
            }
            if res.resolved_from:
                entry["resolved_from"] = res.resolved_from
            if res.resolution_chain and len(res.resolution_chain) > 1:
                entry["resolution_chain"] = res.resolution_chain
            if res.description:
                entry["description"] = res.description
            tokens_dict[path] = entry

        # 2. Theme-only tokens (tokens existing in themes but not in base, e.g. component.card.radius)
        theme_only_paths = set(self.all_tokens.keys()) - set(self.base_resolved.keys())
        for path in sorted(theme_only_paths):
            raw_token = self.all_tokens[path]
            tokens_dict[path] = {
                "value": raw_token.raw_value,
                "type": raw_token.type,
                "tier": raw_token.layer,
                "description": raw_token.description,
                "is_theme_only": True
            }

        # 3. Themes dictionary
        themes_dict: Dict[str, Any] = {}
        for theme_id, label, selector in THEME_ORDER:
            if theme_id in self.theme_resolved:
                t_override = self.theme_overrides.get(theme_id)
                t_tokens = self.theme_resolved[theme_id]
                theme_entry: Dict[str, Any] = {
                    "selector": selector,
                    "description": t_override.description if t_override else label,
                    "token_count": len(t_tokens),
                    "tokens": {}
                }
                for path in sorted(t_tokens.keys()):
                    res = t_tokens[path]
                    t_entry: Dict[str, Any] = {
                        "value": res.value,
                        "css_value": res.css_value,
                        "css_var": res.css_var_name,
                        "type": res.type,
                    }
                    if res.resolved_from:
                        t_entry["resolved_from"] = res.resolved_from
                    theme_entry["tokens"][path] = t_entry
                themes_dict[theme_id] = theme_entry

        component_token_count = sum(1 for r in self.base_resolved.values() if r.tier == "component")

        return {
            "system": "Master Design System (MDS)",
            "version": "1.0.0",
            "phase": "9.2",
            "tokens_total": len(self.all_tokens),
            "base_tokens_total": len(self.base_resolved),
            "component_tokens_total": component_token_count,
            "tokens": tokens_dict,
            "themes": themes_dict,
        }

    def emit_dts(self) -> str:
        """
        Generates TypeScript declaration file (tokens.d.ts) providing static autocomplete.
        """
        # Collect all distinct CSS variable names across base and themes
        css_vars: Set[str] = set()
        for r in self.base_resolved.values():
            css_vars.add(r.css_var_name)
        for theme_tokens in self.theme_resolved.values():
            for r in theme_tokens.values():
                css_vars.add(r.css_var_name)

        sorted_vars = sorted(list(css_vars))

        lines: List[str] = [
            "/**",
            " * MDS (Master Design System) — TypeScript Type Definitions",
            " * Generated by MDS Token Runtime Engine (Phase 9.2)",
            " * Source of Truth: MDS/02-Tokens/ (18 DTCG JSON files)",
            " * Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)",
            " */",
            "",
            "export type MDSTokenName ="
        ]

        for var_name in sorted_vars:
            lines.append(f"  | '{var_name}'")

        lines.extend([
            ";",
            "",
            "export interface MDSTokenDictionary {",
            "  [token: string]: string;",
            "}",
            "",
            "export interface MDSTokenMetadata {",
            "  path: string;",
            "  cssVar: MDSTokenName;",
            "  value: string | number | unknown;",
            "  cssValue: string;",
            "  type: string;",
            "  tier: 'primitive' | 'semantic' | 'component' | 'theme';",
            "  resolvedFrom?: string;",
            "  description?: string;",
            "}",
            "",
            "export declare const tokens: Record<MDSTokenName, string>;",
            "export declare const tokenCatalog: Record<string, MDSTokenMetadata>;",
            ""
        ])

        return "\n".join(lines)

    def compile(self) -> CompileResult:
        """Executes compilation pass and bundles all output artifacts."""
        css = self.emit_css()
        json_data = self.emit_json()
        dts = self.emit_dts()

        stats = {
            "tokens_total": len(self.all_tokens),
            "base_tokens": len(self.base_resolved),
            "themes_count": len(self.theme_resolved),
            "theme_overrides_total": sum(len(t) for t in self.theme_resolved.values()),
            "component_tokens": sum(1 for r in self.base_resolved.values() if r.tier == "component"),
            "max_alias_depth": max((r.hops for r in self.base_resolved.values()), default=0),
        }

        return CompileResult(
            css=css,
            json_data=json_data,
            dts=dts,
            base_resolved=self.base_resolved,
            theme_resolved=self.theme_resolved,
            stats=stats
        )
