"""
Master Design System (MDS) — DTCG Design Token Compiler & Dependency Resolver
Phase 10.3: Production Artifact Compilation & Zero-NPM Distribution
Layer 13: Implementation, Tooling & Operationalization
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .models import CANONICAL_COMPILATION_SOURCES, SourceValidationError


def token_path_to_css_var(path: str) -> str:
    """
    Converts a dotted token path to a standard kebab-case CSS custom property name.
    Handles camelCase segments (e.g. lineHeight -> line-height, focusRing -> focus-ring).
    Prefixed strictly with '--mds-'.
    """
    parts = path.split(".")
    kebab_parts = []
    for part in parts:
        s = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", part).lower()
        kebab_parts.append(s)
    return f"--mds-{'-'.join(kebab_parts)}"


def format_css_value(value: Any, token_type: str = "") -> str:
    """
    Formats a resolved Python data structure into a valid CSS property value string.
    """
    if token_type == "cubicBezier" or (
        isinstance(value, list)
        and len(value) == 4
        and all(isinstance(x, (int, float)) for x in value)
    ):
        return f"cubic-bezier({value[0]}, {value[1]}, {value[2]}, {value[3]})"

    if token_type == "shadow" or (
        isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict)
    ):
        if len(value) == 1:
            item = value[0]
            if (
                item.get("offsetX") == "0px"
                and item.get("offsetY") == "0px"
                and item.get("blur") == "0px"
                and item.get("spread") == "0px"
                and (
                    "rgba(0, 0, 0, 0)" in item.get("color", "")
                    or "transparent" in item.get("color", "")
                )
            ):
                return "none"

        layers = []
        for item in value:
            ox = item.get("offsetX", "0px")
            oy = item.get("offsetY", "0px")
            blur = item.get("blur", "0px")
            spread = item.get("spread", "0px")
            color = item.get("color", "#000000")
            layers.append(f"{ox} {oy} {blur} {spread} {color}")
        return ", ".join(layers)

    if isinstance(value, (int, float)):
        return str(value)

    if isinstance(value, str):
        return value

    return str(value)


class TokenCompiler:
    """
    Compiles DTCG-compliant design token JSON files into:
    - Canonical platform-neutral token dictionary (tokens.json)
    - Cascade layer scoped CSS Custom Properties (tokens.css)
    - TypeScript declarations (tokens.d.ts)
    """

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()
        self.base_tokens: Dict[str, Dict[str, Any]] = {}
        self.theme_tokens: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self.resolved_base: Dict[str, Any] = {}
        self.resolved_themes: Dict[str, Dict[str, Any]] = {}

    def _extract_tokens_recursive(
        self, data: Dict[str, Any], current_path: str = ""
    ) -> Dict[str, Dict[str, Any]]:
        tokens: Dict[str, Dict[str, Any]] = {}
        if not isinstance(data, dict):
            return tokens

        if "$value" in data:
            tokens[current_path] = {
                "path": current_path,
                "value": data["$value"],
                "type": data.get("$type", ""),
                "description": data.get("$description", ""),
                "extensions": data.get("$extensions", {}),
            }
        else:
            for key, val in data.items():
                if key.startswith("$"):
                    continue
                sub_path = f"{current_path}.{key}" if current_path else key
                if isinstance(val, dict):
                    tokens.update(self._extract_tokens_recursive(val, sub_path))
        return tokens

    def load_sources(self) -> None:
        """Ingests all 18 DTCG token files from CANONICAL_COMPILATION_SOURCES."""
        token_paths = [
            p for p in CANONICAL_COMPILATION_SOURCES if p.startswith("MDS/02-Tokens/") and p.endswith(".tokens.json")
        ]
        if len(token_paths) != 18:
            raise SourceValidationError(
                f"Expected exactly 18 DTCG token files in allowlist, found {len(token_paths)}"
            )

        for rel_path in sorted(token_paths):
            full_path = self.workspace_root / rel_path
            if not full_path.exists():
                raise SourceValidationError(f"Required token file not found: {rel_path}")

            with open(full_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception as e:
                    raise SourceValidationError(f"Malformed JSON in token file {rel_path}: {e}")

            extracted = self._extract_tokens_recursive(data)

            if "themes/" in rel_path:
                theme_name = Path(rel_path).stem.replace(".tokens", "")
                self.theme_tokens[theme_name] = extracted
            else:
                self.base_tokens.update(extracted)

    def resolve_aliases(self) -> None:
        """
        Resolves token aliases with topological cycle detection and 5-hop depth limit.
        """
        alias_pattern = re.compile(r"^\{([a-zA-Z0-9_\.\-]+)\}$")

        def resolve_single_token(
            token_path: str,
            token_def: Dict[str, Any],
            active_stack: List[str],
            pool: Dict[str, Dict[str, Any]],
        ) -> Tuple[Any, str]:
            if token_path in active_stack:
                cycle_str = " -> ".join(active_stack + [token_path])
                raise SourceValidationError(f"Circular token dependency detected: {cycle_str}")

            if len(active_stack) > 5:
                depth_str = " -> ".join(active_stack + [token_path])
                raise SourceValidationError(f"Max token alias depth (5) exceeded: {depth_str}")

            raw_val = token_def["value"]
            token_type = token_def.get("type", "")

            if isinstance(raw_val, str):
                match = alias_pattern.match(raw_val.strip())
                if match:
                    ref_path = match.group(1)
                    if ref_path not in pool and ref_path not in self.base_tokens:
                        raise SourceValidationError(
                            f"Missing token reference '{ref_path}' referenced by '{token_path}'"
                        )
                    ref_def = pool.get(ref_path) or self.base_tokens[ref_path]
                    resolved_val, ref_type = resolve_single_token(
                        ref_path, ref_def, active_stack + [token_path], pool
                    )
                    return resolved_val, token_type or ref_type

            return raw_val, token_type

        # 1. Resolve base tokens
        for path, defn in sorted(self.base_tokens.items()):
            val, ttype = resolve_single_token(path, defn, [], self.base_tokens)
            self.resolved_base[path] = {
                "value": val,
                "type": ttype,
                "description": defn.get("description", ""),
                "css_var": token_path_to_css_var(path),
            }

        # 2. Resolve theme tokens
        for theme_name, theme_dict in sorted(self.theme_tokens.items()):
            self.resolved_themes[theme_name] = {}
            for path, defn in sorted(theme_dict.items()):
                val, ttype = resolve_single_token(path, defn, [], theme_dict)
                self.resolved_themes[theme_name][path] = {
                    "value": val,
                    "type": ttype,
                    "description": defn.get("description", ""),
                    "css_var": token_path_to_css_var(path),
                }

    def generate_tokens_json(self) -> str:
        """Emits canonical platform-neutral token dictionary as formatted JSON."""
        output = {
            "schema_version": "1.0.0",
            "metadata": {
                "name": "master-design-system-tokens",
                "version": "1.0.0",
                "total_base_tokens": len(self.resolved_base),
                "themes": sorted(list(self.resolved_themes.keys())),
            },
            "tokens": self.resolved_base,
            "themes": self.resolved_themes,
        }
        return json.dumps(output, indent=2, sort_keys=True) + "\n"

    def generate_tokens_css(self) -> str:
        """
        Emits Cascade Layer scoped CSS custom properties (--mds-*).
        """
        lines = [
            "/**",
            " * Master Design System (MDS) — Compiled Design Tokens",
            " * Layer: @layer mds.tokens",
            " * Zero-NPM Distribution",
            " */",
            "@layer mds.tokens {",
            "  :root {",
        ]

        for path, data in sorted(self.resolved_base.items()):
            css_var = data["css_var"]
            css_val = format_css_value(data["value"], data.get("type", ""))
            lines.append(f"    {css_var}: {css_val};")

        lines.append("  }")

        # Theme selectors
        theme_selector_map = {
            "mode.dark": '[data-theme="dark"]',
            "mode.high-contrast": '[data-contrast="high"]',
            "density.compact": '[data-density="compact"]',
            "preset.refined": '[data-preset="refined"]',
        }

        for theme_name, tokens in sorted(self.resolved_themes.items()):
            selector = theme_selector_map.get(theme_name, f'[data-theme="{theme_name}"]')
            lines.append(f"\n  {selector} {{")
            for path, data in sorted(tokens.items()):
                css_var = data["css_var"]
                css_val = format_css_value(data["value"], data.get("type", ""))
                lines.append(f"    {css_var}: {css_val};")
            lines.append("  }")

        lines.append("}\n")
        return "\n".join(lines)

    def generate_tokens_dts(self) -> str:
        """Emits TypeScript declarations for token dictionary."""
        lines = [
            "/**",
            " * Master Design System (MDS) — Token Type Declarations",
            " * Autogenerated by MDS Production Compiler",
            " */",
            "",
            "export interface MdsTokenValue {",
            "  value: string | number | boolean | any;",
            "  type: string;",
            "  description: string;",
            "  css_var: string;",
            "}",
            "",
            "export interface MdsTokenDictionary {",
            "  schema_version: string;",
            "  metadata: {",
            "    name: string;",
            "    version: string;",
            "    total_base_tokens: number;",
            "    themes: string[];",
            "  };",
            "  tokens: Record<string, MdsTokenValue>;",
            "  themes: Record<string, Record<string, MdsTokenValue>>;",
            "}",
            "",
            "export declare const tokens: MdsTokenDictionary;",
            "export default tokens;",
            "",
        ]
        return "\n".join(lines)

    def compile(self) -> Tuple[str, str, str]:
        """
        Executes complete token compilation.
        Returns: (tokens_json, tokens_css, tokens_dts)
        """
        self.load_sources()
        self.resolve_aliases()
        tokens_json = self.generate_tokens_json()
        tokens_css = self.generate_tokens_css()
        tokens_dts = self.generate_tokens_dts()
        return tokens_json, tokens_css, tokens_dts
