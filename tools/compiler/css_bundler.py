"""
Master Design System (MDS) — CSS Layer Scoping & Bundle Packaging Engine
Phase 10.3: Production Artifact Compilation & Zero-NPM Distribution
Layer 13: Implementation, Tooling & Operationalization
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

from .models import CANONICAL_COMPILATION_SOURCES, SourceValidationError


class CssBundler:
    """
    Bundles runtime CSS stylesheets with W3C Cascade Layers:
    - Normalizes line endings to LF (\n)
    - Enforces @layer declaration order
    - Emits monolithic bundle (mds.all.css)
    - Emits modular stylesheets (mds.tokens.css, mds.primitives.css, mds.components.css)
    """

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()

    def _read_file_normalized(self, rel_path: str) -> str:
        full_path = self.workspace_root / rel_path
        if not full_path.exists():
            raise SourceValidationError(f"Required CSS file missing: {rel_path}")
        content = full_path.read_text(encoding="utf-8")
        # Normalize Windows CRLF to LF
        return content.replace("\r\n", "\n").replace("\r", "\n")

    def build_bundles(self, compiled_tokens_css: str) -> Dict[str, str]:
        """
        Constructs all distribution CSS bundles.
        Returns dict mapping destination relative path -> file content.
        """
        # 1. Foundation CSS (from MDS/Runtime/css/)
        foundation_files = [
            "MDS/Runtime/css/reset.css",
            "MDS/Runtime/css/foundations.css",
            "MDS/Runtime/css/primitives.css",
            "MDS/Runtime/css/mds-core.css",
        ]
        foundations_content = [self._read_file_normalized(f) for f in foundation_files]

        # 2. Primitive CSS (12 files)
        primitive_files = sorted([
            p for p in CANONICAL_COMPILATION_SOURCES
            if p.startswith("MDS/Runtime/primitives/") and p.endswith(".css")
        ])
        primitives_content = [self._read_file_normalized(f) for f in primitive_files]

        # 3. Component CSS (Consolidated components.css + individual component files)
        component_consolidated_path = "MDS/Runtime/components/components.css"
        component_content = self._read_file_normalized(component_consolidated_path)

        # Normalization of tokens CSS
        norm_tokens_css = compiled_tokens_css.replace("\r\n", "\n").replace("\r", "\n")

        # ----------------------------------------------------------------------
        # A. Monolithic Bundle: dist/bundles/mds.all.css
        # ----------------------------------------------------------------------
        layer_preamble = (
            "/**\n"
            " * Master Design System (MDS) — Production Monolithic Stylesheet\n"
            " * Version: 1.0.0\n"
            " * Zero-NPM Distribution\n"
            " * Standards: W3C CSS Cascade Layers, CSS Custom Properties\n"
            " */\n"
            "@layer mds.reset, mds.tokens, mds.foundations, mds.primitives, mds.components, mds.themes;\n\n"
        )

        all_css_sections = [
            layer_preamble,
            norm_tokens_css,
            "\n".join(foundations_content),
            "\n".join(primitives_content),
            component_content,
        ]
        mds_all_css = "\n\n".join(all_css_sections) + "\n"

        # ----------------------------------------------------------------------
        # B. Modular CSS: dist/css/mds.tokens.css
        # ----------------------------------------------------------------------
        mds_tokens_css = (
            "/**\n"
            " * Master Design System (MDS) — Modular Tokens Stylesheet\n"
            " * Layer: mds.tokens\n"
            " */\n"
            "@layer mds.tokens, mds.themes;\n\n"
            + norm_tokens_css
            + "\n"
        )

        # ----------------------------------------------------------------------
        # C. Modular CSS: dist/css/mds.primitives.css
        # ----------------------------------------------------------------------
        mds_primitives_css = (
            "/**\n"
            " * Master Design System (MDS) — Modular Primitives Stylesheet\n"
            " * Layers: mds.reset, mds.foundations, mds.primitives\n"
            " */\n"
            "@layer mds.reset, mds.foundations, mds.primitives;\n\n"
            + "\n\n".join(foundations_content)
            + "\n\n"
            + "\n\n".join(primitives_content)
            + "\n"
        )

        # ----------------------------------------------------------------------
        # D. Modular CSS: dist/css/mds.components.css
        # ----------------------------------------------------------------------
        mds_components_css = (
            "/**\n"
            " * Master Design System (MDS) — Modular Components Stylesheet\n"
            " * Layer: mds.components\n"
            " */\n"
            "@layer mds.components;\n\n"
            + component_content
            + "\n"
        )

        outputs: Dict[str, str] = {
            "bundles/mds.all.css": mds_all_css,
            "css/mds.tokens.css": mds_tokens_css,
            "css/mds.primitives.css": mds_primitives_css,
            "css/mds.components.css": mds_components_css,
        }

        # Also emit modular individual component stylesheets under dist/css/components/
        component_modular_files = sorted([
            p for p in CANONICAL_COMPILATION_SOURCES
            if p.startswith("MDS/Runtime/components/") and p.endswith(".css") and p != component_consolidated_path
        ])
        for comp_rel in component_modular_files:
            c_name = Path(comp_rel).name
            comp_content = self._read_file_normalized(comp_rel)
            outputs[f"css/components/{c_name}"] = comp_content + "\n"

        return outputs
