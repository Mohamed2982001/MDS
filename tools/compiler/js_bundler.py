"""
Master Design System (MDS) — JavaScript Dependency DAG & Bundling Engine
Phase 10.3: Production Artifact Compilation & Zero-NPM Distribution
Layer 13: Implementation, Tooling & Operationalization
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

from .models import CANONICAL_COMPILATION_SOURCES, SourceValidationError


def strip_es_imports_and_exports(code: str) -> str:
    """
    Strips top-level ES module import and export statements for IIFE embedding.
    Converts 'export class Foo' -> 'class Foo'
    Converts 'export function bar' -> 'function bar'
    Converts 'export const baz' -> 'const baz'
    Removes 'import { ... } from "..."'
    Removes standalone 'export { ... };'
    """
    lines = []
    for line in code.split("\n"):
        stripped = line.strip()
        if stripped.startswith("import ") and "from " in stripped:
            continue
        if stripped.startswith("export {") and stripped.endswith("};"):
            continue
        if stripped.startswith("export default "):
            continue
        if stripped.startswith("export class "):
            line = line.replace("export class ", "class ")
        elif stripped.startswith("export function "):
            line = line.replace("export function ", "function ")
        elif stripped.startswith("export const "):
            line = line.replace("export const ", "const ")
        elif stripped.startswith("export let "):
            line = line.replace("export let ", "let ")
        elif stripped.startswith("export var "):
            line = line.replace("export var ", "var ")
        lines.append(line)
    return "\n".join(lines)


class JsBundler:
    """
    Bundles JavaScript runtime files following topological DAG order:
    FocusTrap -> LiveRegion -> MdsSwitch -> MdsTabs -> MdsTooltip -> MdsDialog
    Emits IIFE, ESM, modular scripts, and TypeScript declarations.
    """

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()

    def _read_normalized(self, rel_path: str) -> str:
        full_path = self.workspace_root / rel_path
        if not full_path.exists():
            raise SourceValidationError(f"Required JavaScript file missing: {rel_path}")
        content = full_path.read_text(encoding="utf-8")
        return content.replace("\r\n", "\n").replace("\r", "\n")

    def build_bundles(self) -> Dict[str, str]:
        """
        Constructs all distribution JavaScript bundles.
        Returns dict mapping destination relative path -> file content.
        """
        # Canonical JavaScript sources in strict topological order (ADR-208)
        topological_sources = [
            ("FocusTrap", "MDS/Runtime/primitives/interaction/focus-trap.js"),
            ("LiveRegion", "MDS/Runtime/primitives/interaction/live-region.js"),
            ("MdsSwitch", "MDS/Runtime/components/switch/switch.js"),
            ("MdsTabs", "MDS/Runtime/components/tabs/tabs.js"),
            ("MdsTooltip", "MDS/Runtime/components/tooltip/tooltip.js"),
            ("MdsDialog", "MDS/Runtime/components/dialog/dialog.js"),
        ]

        raw_contents = {name: self._read_normalized(path) for name, path in topological_sources}
        clean_contents = {name: strip_es_imports_and_exports(raw) for name, raw in raw_contents.items()}

        # ----------------------------------------------------------------------
        # A. Monolithic IIFE: dist/bundles/mds.all.js
        # ----------------------------------------------------------------------
        iife_body = "\n\n".join([
            clean_contents["FocusTrap"],
            clean_contents["LiveRegion"],
            clean_contents["MdsSwitch"],
            clean_contents["MdsTabs"],
            clean_contents["MdsTooltip"],
            clean_contents["MdsDialog"],
        ])

        mds_all_js = (
            "/**\n"
            " * Master Design System (MDS) — Production Monolithic JavaScript Runtime\n"
            " * Version: 1.0.0\n"
            " * Zero-NPM Distribution\n"
            " * Topological Order: FocusTrap -> LiveRegion -> MdsSwitch -> MdsTabs -> MdsTooltip -> MdsDialog\n"
            " */\n"
            "(function (global, factory) {\n"
            "  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :\n"
            "  typeof define === 'function' && define.amd ? define(factory) :\n"
            "  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.MDS = factory());\n"
            "})(this, (function () {\n"
            "  'use strict';\n\n"
            + iife_body
            + "\n\n"
            "  if (typeof window !== 'undefined' && window.customElements) {\n"
            "    if (!window.customElements.get('mds-switch') && typeof MdsSwitch !== 'undefined') window.customElements.define('mds-switch', MdsSwitch);\n"
            "    if (!window.customElements.get('mds-tabs') && typeof MdsTabs !== 'undefined') window.customElements.define('mds-tabs', MdsTabs);\n"
            "    if (!window.customElements.get('mds-tooltip') && typeof MdsTooltip !== 'undefined') window.customElements.define('mds-tooltip', MdsTooltip);\n"
            "    if (!window.customElements.get('mds-dialog') && typeof MdsDialog !== 'undefined') window.customElements.define('mds-dialog', MdsDialog);\n"
            "  }\n\n"
            "  return {\n"
            "    FocusTrap: typeof FocusTrap !== 'undefined' ? FocusTrap : null,\n"
            "    LiveRegion: typeof LiveRegion !== 'undefined' ? LiveRegion : null,\n"
            "    MdsSwitch: typeof MdsSwitch !== 'undefined' ? MdsSwitch : null,\n"
            "    MdsTabs: typeof MdsTabs !== 'undefined' ? MdsTabs : null,\n"
            "    MdsTooltip: typeof MdsTooltip !== 'undefined' ? MdsTooltip : null,\n"
            "    MdsDialog: typeof MdsDialog !== 'undefined' ? MdsDialog : null\n"
            "  };\n"
            "}));\n"
        )

        # ----------------------------------------------------------------------
        # B. Monolithic ESM: dist/bundles/mds.all.esm.js
        # ----------------------------------------------------------------------
        esm_body = "\n\n".join([
            clean_contents["FocusTrap"],
            clean_contents["LiveRegion"],
            clean_contents["MdsSwitch"],
            clean_contents["MdsTabs"],
            clean_contents["MdsTooltip"],
            clean_contents["MdsDialog"],
        ])

        mds_all_esm = (
            "/**\n"
            " * Master Design System (MDS) — Production Monolithic ES Module\n"
            " * Version: 1.0.0\n"
            " * Zero-NPM Distribution\n"
            " */\n\n"
            + esm_body
            + "\n\n"
            "export function registerMdsCustomElements() {\n"
            "  if (typeof window !== 'undefined' && window.customElements) {\n"
            "    if (!window.customElements.get('mds-switch') && typeof MdsSwitch !== 'undefined') window.customElements.define('mds-switch', MdsSwitch);\n"
            "    if (!window.customElements.get('mds-tabs') && typeof MdsTabs !== 'undefined') window.customElements.define('mds-tabs', MdsTabs);\n"
            "    if (!window.customElements.get('mds-tooltip') && typeof MdsTooltip !== 'undefined') window.customElements.define('mds-tooltip', MdsTooltip);\n"
            "    if (!window.customElements.get('mds-dialog') && typeof MdsDialog !== 'undefined') window.customElements.define('mds-dialog', MdsDialog);\n"
            "  }\n"
            "}\n\n"
            "export {\n"
            "  FocusTrap,\n"
            "  LiveRegion,\n"
            "  MdsSwitch,\n"
            "  MdsTabs,\n"
            "  MdsTooltip,\n"
            "  MdsDialog\n"
            "};\n\n"
            "export default {\n"
            "  FocusTrap,\n"
            "  LiveRegion,\n"
            "  MdsSwitch,\n"
            "  MdsTabs,\n"
            "  MdsTooltip,\n"
            "  MdsDialog,\n"
            "  registerMdsCustomElements\n"
            "};\n"
        )

        # ----------------------------------------------------------------------
        # C. Modular Primitives: dist/js/mds.primitives.js
        # ----------------------------------------------------------------------
        mds_primitives_js = (
            "/**\n"
            " * Master Design System (MDS) — Modular Primitives Runtime\n"
            " */\n"
            "(function (global, factory) {\n"
            "  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :\n"
            "  typeof define === 'function' && define.amd ? define(factory) :\n"
            "  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.MDS_Primitives = factory());\n"
            "})(this, (function () {\n"
            "  'use strict';\n\n"
            + clean_contents["FocusTrap"]
            + "\n\n"
            + clean_contents["LiveRegion"]
            + "\n\n"
            "  return { FocusTrap, LiveRegion };\n"
            "}));\n"
        )

        # ----------------------------------------------------------------------
        # D. Modular Components: dist/js/mds.components.js
        # ----------------------------------------------------------------------
        mds_components_js = (
            "/**\n"
            " * Master Design System (MDS) — Modular Components Runtime\n"
            " */\n"
            "(function (global, factory) {\n"
            "  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :\n"
            "  typeof define === 'function' && define.amd ? define(factory) :\n"
            "  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.MDS_Components = factory());\n"
            "})(this, (function () {\n"
            "  'use strict';\n\n"
            + clean_contents["FocusTrap"]  # FocusTrap required for MdsDialog dependency closure
            + "\n\n"
            + clean_contents["MdsSwitch"]
            + "\n\n"
            + clean_contents["MdsTabs"]
            + "\n\n"
            + clean_contents["MdsTooltip"]
            + "\n\n"
            + clean_contents["MdsDialog"]
            + "\n\n"
            "  return { MdsSwitch, MdsTabs, MdsTooltip, MdsDialog };\n"
            "}));\n"
        )

        # ----------------------------------------------------------------------
        # E. TypeScript Declarations: dist/types/components.d.ts
        # ----------------------------------------------------------------------
        components_dts = (
            "/**\n"
            " * Master Design System (MDS) — Component Type Declarations\n"
            " * Autogenerated by MDS Production Compiler\n"
            " */\n\n"
            "export declare class FocusTrap {\n"
            "  constructor(element: HTMLElement, options?: Record<string, any>);\n"
            "  activate(): void;\n"
            "  deactivate(): void;\n"
            "  pause(): void;\n"
            "  unpause(): void;\n"
            "}\n\n"
            "export declare class LiveRegion {\n"
            "  constructor(options?: Record<string, any>);\n"
            "  announce(message: string, priority?: 'polite' | 'assertive'): void;\n"
            "  destroy(): void;\n"
            "}\n\n"
            "export declare class MdsSwitch extends HTMLElement {\n"
            "  checked: boolean;\n"
            "  disabled: boolean;\n"
            "  toggle(): void;\n"
            "}\n\n"
            "export declare class MdsTabs extends HTMLElement {\n"
            "  selectedTab: string;\n"
            "  select(tabId: string): void;\n"
            "}\n\n"
            "export declare class MdsTooltip extends HTMLElement {\n"
            "  show(): void;\n"
            "  hide(): void;\n"
            "}\n\n"
            "export declare class MdsDialog extends HTMLElement {\n"
            "  readonly isOpen: boolean;\n"
            "  open(triggerElement?: HTMLElement | null): void;\n"
            "  close(): void;\n"
            "}\n\n"
            "export declare function registerMdsCustomElements(): void;\n\n"
            "declare global {\n"
            "  interface HTMLElementTagNameMap {\n"
            "    'mds-switch': MdsSwitch;\n"
            "    'mds-tabs': MdsTabs;\n"
            "    'mds-tooltip': MdsTooltip;\n"
            "    'mds-dialog': MdsDialog;\n"
            "  }\n"
            "}\n"
        )

        return {
            "bundles/mds.all.js": mds_all_js,
            "bundles/mds.all.esm.js": mds_all_esm,
            "js/mds.primitives.js": mds_primitives_js,
            "js/mds.components.js": mds_components_js,
            "types/components.d.ts": components_dts,
        }
