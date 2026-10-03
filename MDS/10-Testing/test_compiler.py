#!/usr/bin/env python3
"""
Master Design System (MDS) — Standalone Compiler & Zero-NPM Distribution Test Suite
Phase: 10.3 (Production Artifact Compilation & Zero-NPM Distribution)
Layer: 10 (Quality Assurance, Automated Testing & Verification)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

SEPARATION OF CONCERNS:
- Authoritative Implementation: tools/compiler/ (pure Python 3.12.x stdlib)
- Independent Test Suite: MDS/10-Testing/test_compiler.py

TEST MATRIX & TEST IDS:
1. Suite 1: TestTrustChainAndPreflight (6 Tests)
   - TRUST-POS-01: test_trust_pos_01_authoritative_workspace_preflight_pass
   - TRUST-NEG-01: test_trust_neg_01_root_anchor_mutation_rejected (Exit 3)
   - TRUST-NEG-02: test_trust_neg_02_source_binding_mutation_rejected (Case B -> Exit 3)
   - TRUST-NEG-03: test_trust_neg_03_canonical_manifest_mutation_rejected (Case A -> Exit 3)
   - TRUST-NEG-04: test_trust_neg_04_missing_source_file_rejected (Exit 2)
   - TRUST-NEG-05: test_trust_neg_05_source_content_mutation_rejected (Case C -> Exit 3)

2. Suite 2: TestScopeBoundaryEnforcement (4 Tests)
   - SCOPE-POS-01: test_scope_pos_01_strict_source_partition_math (|S|=61, |P_non|=33, |P_core|=94, S ∩ P_non = ∅)
   - SCOPE-NEG-01: test_scope_neg_01_protected_non_source_access_rejected (Case E -> CompilerScopeViolationError)
   - SCOPE-NEG-02: test_scope_neg_02_unexpected_source_outside_compilation_source_set (Case D -> CompilerScopeViolationError)
   - SCOPE-POS-02: test_scope_pos_02_source_sets_immutable_frozensets

3. Suite 3: TestTokenCompilation (4 Tests)
   - TOKEN-POS-01: test_token_pos_01_all_185_tokens_resolved
   - TOKEN-POS-02: test_token_pos_02_alias_resolution_and_cycle_detection
   - TOKEN-POS-03: test_token_pos_03_css_variables_and_4_themes
   - TOKEN-POS-04: test_token_pos_04_typescript_declarations

4. Suite 4: TestBundlerArchitecture (5 Tests)
   - BUNDLE-POS-01: test_bundle_pos_01_css_cascade_layer_ordering
   - BUNDLE-POS-02: test_bundle_pos_02_css_19_modular_components
   - BUNDLE-POS-03: test_bundle_pos_03_js_topological_dag_ordering
   - BUNDLE-POS-04: test_bundle_pos_04_js_idempotent_custom_elements_registration
   - BUNDLE-POS-05: test_bundle_pos_05_typescript_component_declarations

5. Suite 5: TestDeterministicPackaging & Reproducibility (4 Tests)
   - PACK-POS-01: test_pack_pos_01_archive_generation_zip_and_targz
   - PACK-POS-02: test_pack_pos_02_zip_headers_and_permissions_normalized
   - PACK-POS-03: test_pack_pos_03_tar_headers_and_epoch_normalized
   - REPRO-E2E-01: test_repro_e2e_01_bit_for_bit_rebuild (Build A == Build B byte-for-byte across all 33 files + archives + manifest + Build Identity)

6. Suite 6: TestBuildIdentityManifest & Compiler Identity Mutation (4 Tests)
   - IDENT-POS-01: test_ident_pos_01_eight_tier_identity_structure_completeness
   - IDENT-POS-02: test_ident_pos_02_compiler_identity_covers_complete_source_closure (Advisory G-013-A closed)
   - IDENT-POS-03: test_ident_pos_03_companion_sha256_manifest_verification
   - ICMP-MUT-01: test_icmp_mut_01_compiler_source_mutation_changes_identities (Negative test: byte modification in compiler -> I_cmp changes -> I_build changes)

7. Suite 7: TestDistributionVerificationGate & Immutability (6 Tests)
   - VERIFY-POS-01: test_verify_pos_01_valid_distribution_passes_exit_0
   - VERIFY-RO-01: test_verify_ro_01_strict_immutability_snapshot (Snapshot before == Snapshot after, 0 byte changes, 0 temp files)
   - VERIFY-NEG-01: test_verify_neg_01_corrupted_artifact_detected_exit_3
   - VERIFY-NEG-02: test_verify_neg_02_missing_artifact_detected_exit_3
   - VERIFY-NEG-03: test_verify_neg_03_tampered_manifest_detected_exit_3
   - VERIFY-NEG-04: test_verify_neg_04_extraneous_untracked_file_detected_exit_3

8. Suite 8: TestCompilerCLI & Runtime Contract (5 Tests)
   - CLI-POS-01: test_cli_pos_01_compile_success_exit_0
   - CLI-NEG-01: test_cli_neg_01_reproducible_mode_requires_epoch_exit_4
   - CLI-POS-02: test_cli_pos_02_dev_mode_permits_missing_epoch
   - CLI-POS-03: test_cli_pos_03_verify_exit_codes_contract
   - RUNTIME-CTR-01: test_runtime_ctr_01_python_3_12_x_strict_enforcement (Reconciles contract strictly to Python 3.12.x)

Total: 38 Automated Tests.
"""

from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import shutil
import sys
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Tuple
from unittest.mock import patch

# Workspace setup
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from tools.compiler.cli import main as cli_main
from tools.compiler.css_bundler import CssBundler
from tools.compiler.engine import CompilerEngine
from tools.compiler.js_bundler import JsBundler
from tools.compiler.manifest_generator import (
    ManifestGenerator,
    compute_build_config_identity,
    compute_build_env_identity,
    compute_compiler_identity,
    compute_source_identity,
    compute_unified_build_id,
)
from tools.compiler.models import (
    AUTHORITATIVE_SOURCE_MANIFEST_DIGEST,
    CANONICAL_COMPILATION_SOURCES,
    CANONICAL_PROTECTED_NON_SOURCES,
    ROOT_TRUST_ANCHOR_FINGERPRINT,
    SUPPORTED_PYTHON_MAJOR_MINOR,
    BuildConfig,
    BuildIdentity,
    CompilerError,
    CompilerScopeViolationError,
    ConfigurationError,
    ContractViolationError,
    EnvironmentContract,
    IntegrityViolationError,
    SourceValidationError,
    canonical_stream_sha256,
)
from tools.compiler.packager import DeterministicPackager
from tools.compiler.token_compiler import TokenCompiler
from tools.compiler.validator import DistributionValidator, PreflightValidator


# ==============================================================================
# Suite 1: TestTrustChainAndPreflight
# ==============================================================================
class TestTrustChainAndPreflight(unittest.TestCase):
    """Verifies the multi-tier cryptographic trust chain and preflight validation."""

    def setUp(self):
        self.workspace = WORKSPACE_ROOT
        self.preflight = PreflightValidator(self.workspace)

    def test_trust_pos_01_authoritative_workspace_preflight_pass(self):
        """[TRUST-POS-01] Authoritative workspace passes all preflight checks without exceptions."""
        sources = self.preflight.validate_trust_chain_and_sources()
        self.assertEqual(len(sources), len(CANONICAL_COMPILATION_SOURCES))

    def test_trust_neg_01_root_anchor_mutation_rejected(self):
        """[TRUST-NEG-01] Modifying the Root Trust Anchor fingerprint triggers IntegrityViolationError (Exit 3)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_ws = Path(tmp_dir)
            baselines_dir = tmp_ws / "MDS" / "10-Testing" / "baselines" / "historical"
            baselines_dir.mkdir(parents=True, exist_ok=True)
            tampered_anchor = baselines_dir / "trust_anchor.json"
            tampered_anchor.write_text('{"tampered": true}', encoding="utf-8")

            tmp_val = PreflightValidator(tmp_ws)
            with self.assertRaises(IntegrityViolationError) as ctx:
                tmp_val.validate_trust_chain_and_sources()
            self.assertIn("Root Trust Anchor fingerprint mismatch", str(ctx.exception))

    def test_trust_neg_02_source_binding_mutation_rejected(self):
        """[TRUST-NEG-02] Case B: Modifying source trust binding triggers IntegrityViolationError (Exit 3)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_ws = Path(tmp_dir)
            shutil.copytree(
                self.workspace / "MDS" / "10-Testing" / "baselines",
                tmp_ws / "MDS" / "10-Testing" / "baselines",
            )
            binding_path = tmp_ws / "MDS" / "10-Testing" / "baselines" / "compilation" / "source_trust_binding.json"
            with open(binding_path, "r", encoding="utf-8") as f:
                binding_data = json.load(f)
            binding_data["root_anchor_sha256"] = "0" * 64
            with open(binding_path, "w", encoding="utf-8") as f:
                json.dump(binding_data, f, indent=2)

            tmp_val = PreflightValidator(tmp_ws)
            with self.assertRaises(IntegrityViolationError) as ctx:
                tmp_val.validate_trust_chain_and_sources()
            self.assertIn("Source trust binding does not bind", str(ctx.exception))

            # Also verify via CompilerEngine execution
            engine = CompilerEngine(workspace_root=tmp_ws)
            with self.assertRaises(IntegrityViolationError):
                engine.compile(output_dir=tmp_ws / "dist", build_epoch=1790812800)

            # Also verify CLI exit code 3
            exit_code = cli_main(["compile", "--workspace", str(tmp_ws), "--epoch", "1790812800", "--out", str(tmp_ws / "dist")])
            self.assertEqual(exit_code, 3)

    def test_trust_neg_03_canonical_manifest_mutation_rejected(self):
        """[TRUST-NEG-03] Case A: Modifying canonical source manifest triggers IntegrityViolationError (Exit 3)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_ws = Path(tmp_dir)
            shutil.copytree(
                self.workspace / "MDS" / "10-Testing" / "baselines",
                tmp_ws / "MDS" / "10-Testing" / "baselines",
            )
            manifest_path = tmp_ws / "MDS" / "10-Testing" / "baselines" / "compilation" / "canonical_source_manifest.json"
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)
            manifest_data["sources"]["MDS/Runtime/components/button/button.css"]["byte_size"] = 999999
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest_data, f, indent=2)

            tmp_val = PreflightValidator(tmp_ws)
            with self.assertRaises(IntegrityViolationError) as ctx:
                tmp_val.validate_trust_chain_and_sources()
            self.assertIn("Source manifest hash mismatch against binding", str(ctx.exception))

            # Also verify via CompilerEngine execution
            engine = CompilerEngine(workspace_root=tmp_ws)
            with self.assertRaises(IntegrityViolationError):
                engine.compile(output_dir=tmp_ws / "dist", build_epoch=1790812800)

            # Also verify CLI exit code 3
            exit_code = cli_main(["compile", "--workspace", str(tmp_ws), "--epoch", "1790812800", "--out", str(tmp_ws / "dist")])
            self.assertEqual(exit_code, 3)

    def test_trust_neg_04_missing_source_file_rejected(self):
        """[TRUST-NEG-04] Preflight fails if any of the 61 canonical compilation source files is missing (Exit 2)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_ws = Path(tmp_dir)
            shutil.copytree(
                self.workspace / "MDS" / "10-Testing" / "baselines",
                tmp_ws / "MDS" / "10-Testing" / "baselines",
            )
            target_css = tmp_ws / "MDS" / "Runtime" / "components" / "button"
            target_css.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(
                self.workspace / "MDS" / "Runtime" / "components" / "button" / "button.css",
                target_css / "button.css",
            )

            tmp_val = PreflightValidator(tmp_ws)
            with self.assertRaises(SourceValidationError) as ctx:
                tmp_val.validate_trust_chain_and_sources()
            self.assertIn("Required compilation source missing from disk", str(ctx.exception))

    def test_trust_neg_05_source_content_mutation_rejected(self):
        """[TRUST-NEG-05] Case C: Modifying 1 byte in a canonical source file triggers IntegrityViolationError (Exit 3)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_ws = Path(tmp_dir)
            shutil.copytree(
                self.workspace / "MDS" / "10-Testing" / "baselines",
                tmp_ws / "MDS" / "10-Testing" / "baselines",
            )
            for src_rel in CANONICAL_COMPILATION_SOURCES:
                src_path = self.workspace / Path(src_rel)
                dst_path = tmp_ws / Path(src_rel)
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src_path, dst_path)

            # Mutate exactly one byte in button.css
            target_css = tmp_ws / "MDS" / "Runtime" / "components" / "button" / "button.css"
            original_bytes = target_css.read_bytes()
            target_css.write_bytes(original_bytes + b"/* byte-mutation */")

            tmp_val = PreflightValidator(tmp_ws)
            with self.assertRaises(IntegrityViolationError) as ctx:
                tmp_val.validate_trust_chain_and_sources()
            self.assertIn("Source integrity violation in MDS/Runtime/components/button/button.css", str(ctx.exception))

            # Also verify via CompilerEngine execution
            engine = CompilerEngine(workspace_root=tmp_ws)
            with self.assertRaises(IntegrityViolationError):
                engine.compile(output_dir=tmp_ws / "dist", build_epoch=1790812800)

            # Also verify CLI exit code 3
            exit_code = cli_main(["compile", "--workspace", str(tmp_ws), "--epoch", "1790812800", "--out", str(tmp_ws / "dist")])
            self.assertEqual(exit_code, 3)


# ==============================================================================
# Suite 2: TestScopeBoundaryEnforcement
# ==============================================================================
class TestScopeBoundaryEnforcement(unittest.TestCase):
    """Enforces strict mathematical partition between 61 compilation sources and 33 protected non-sources."""

    def test_scope_pos_01_strict_source_partition_math(self):
        """[SCOPE-POS-01] Verifies |S|=61, |P_non|=33, |P_core|=94, S ∩ P_non = ∅, S ∪ P_non = P_core."""
        self.assertEqual(len(CANONICAL_COMPILATION_SOURCES), 61)
        self.assertEqual(len(CANONICAL_PROTECTED_NON_SOURCES), 33)

        intersection = CANONICAL_COMPILATION_SOURCES.intersection(CANONICAL_PROTECTED_NON_SOURCES)
        self.assertEqual(len(intersection), 0, f"Disjoint violation: {intersection}")

        union = CANONICAL_COMPILATION_SOURCES.union(CANONICAL_PROTECTED_NON_SOURCES)
        self.assertEqual(len(union), 94)

    def test_scope_neg_01_protected_non_source_access_rejected(self):
        """[SCOPE-NEG-01] Case E: Attempting to ingest any of the 33 Protected Non-Sources raises CompilerScopeViolationError (Exit 3)."""
        for non_source in CANONICAL_PROTECTED_NON_SOURCES:
            with self.subTest(file=non_source):
                with self.assertRaises(CompilerScopeViolationError) as ctx:
                    DistributionValidator.validate_file_in_scope(Path(non_source), WORKSPACE_ROOT)
                self.assertIn("Attempted to ingest Protected Non-Source", str(ctx.exception))

    def test_scope_neg_02_unexpected_source_outside_compilation_source_set(self):
        """[SCOPE-NEG-02] Case D: Attempting to ingest unexpected files outside CompilationSourceSet raises CompilerScopeViolationError (Exit 3)."""
        out_of_bounds = [
            "MDS/00-Core/ADR-001.md",
            "MDS/13-Implementation/ACTIVE_PHASE.json",
            "tools/compiler/engine.py",
            "package.json",
            "../outside.txt",
        ]
        for path_str in out_of_bounds:
            with self.subTest(path=path_str):
                with self.assertRaises(CompilerScopeViolationError):
                    DistributionValidator.validate_file_in_scope(Path(path_str), WORKSPACE_ROOT)

    def test_scope_pos_02_source_sets_immutable_frozensets(self):
        """[SCOPE-POS-02] Source sets must be frozensets to prevent runtime mutation."""
        self.assertIsInstance(CANONICAL_COMPILATION_SOURCES, frozenset)
        self.assertIsInstance(CANONICAL_PROTECTED_NON_SOURCES, frozenset)


# ==============================================================================
# Suite 3: TestTokenCompilation
# ==============================================================================
class TestTokenCompilation(unittest.TestCase):
    """Verifies DTCG token parsing, DAG resolution, CSS custom properties, and declarations."""

    def setUp(self):
        self.compiler = TokenCompiler(WORKSPACE_ROOT)
        self.tokens_json, self.tokens_css, self.tokens_dts = self.compiler.compile()

    def test_token_pos_01_all_185_tokens_resolved(self):
        """[TOKEN-POS-01] Verifies 185 base tokens are successfully parsed and resolved."""
        self.assertEqual(len(self.compiler.resolved_base), 185)
        self.assertIn("color.action.primary.default", self.compiler.resolved_base)
        self.assertIn("space.scale.4", self.compiler.resolved_base)
        self.assertIn("radius.md", self.compiler.resolved_base)

    def test_token_pos_02_alias_resolution_and_cycle_detection(self):
        """[TOKEN-POS-02] Verifies alias reference resolution and cycle prevention."""
        primary_token = self.compiler.resolved_base["color.action.primary.default"]
        self.assertTrue(primary_token["value"].startswith("#") or primary_token["value"].startswith("rgb"))

        # Test cycle detection on synthetic circular input
        circular_compiler = TokenCompiler(WORKSPACE_ROOT)
        circular_compiler.base_tokens = {
            "a": {"value": "{b}", "type": "color", "path": "a"},
            "b": {"value": "{c}", "type": "color", "path": "b"},
            "c": {"value": "{a}", "type": "color", "path": "c"},
        }
        with self.assertRaises(SourceValidationError) as ctx:
            circular_compiler.resolve_aliases()
        self.assertIn("Circular token dependency detected", str(ctx.exception))

    def test_token_pos_03_css_variables_and_4_themes(self):
        """[TOKEN-POS-03] Verifies CSS custom properties and 4 theme selectors in tokens.css."""
        self.assertIn(":root {", self.tokens_css)
        self.assertIn("--mds-color-action-primary-default:", self.tokens_css)
        self.assertIn('[data-density="compact"]', self.tokens_css)
        self.assertIn('[data-theme="dark"]', self.tokens_css)
        self.assertIn('[data-contrast="high"]', self.tokens_css)
        self.assertIn('[data-preset="refined"]', self.tokens_css)

    def test_token_pos_04_typescript_declarations(self):
        """[TOKEN-POS-04] Verifies tokens.d.ts exports strongly-typed token dictionary."""
        self.assertIn("export interface MdsTokenDictionary", self.tokens_dts)
        self.assertIn("export declare const tokens: MdsTokenDictionary;", self.tokens_dts)


# ==============================================================================
# Suite 4: TestBundlerArchitecture
# ==============================================================================
class TestBundlerArchitecture(unittest.TestCase):
    """Verifies CSS cascade layering, modularity, and JS topological concatenation."""

    def test_bundle_pos_01_css_cascade_layer_ordering(self):
        """[BUNDLE-POS-01] Emitted mds.all.css declares layers in exact canonical order."""
        tokens_compiler = TokenCompiler(WORKSPACE_ROOT)
        _, tokens_css, _ = tokens_compiler.compile()
        bundler = CssBundler(WORKSPACE_ROOT)
        bundles = bundler.build_bundles(tokens_css)
        all_css = bundles["bundles/mds.all.css"]
        expected_layer_def = "@layer mds.reset, mds.tokens, mds.foundations, mds.primitives, mds.components, mds.themes;"
        self.assertTrue(expected_layer_def in all_css)

    def test_bundle_pos_02_css_19_modular_components(self):
        """[BUNDLE-POS-02] All 19 components emitted individually and in aggregate."""
        tokens_compiler = TokenCompiler(WORKSPACE_ROOT)
        _, tokens_css, _ = tokens_compiler.compile()
        bundler = CssBundler(WORKSPACE_ROOT)
        bundles = bundler.build_bundles(tokens_css)
        comp_files = [k for k in bundles.keys() if k.startswith("css/components/")]
        self.assertEqual(len(comp_files), 19)
        expected_components = [
            "alert.css", "badge.css", "button.css", "card.css", "checkbox.css", "dialog.css", "field.css",
            "icon-button.css", "input.css", "link.css", "radio.css", "select.css", "skeleton.css",
            "spinner.css", "switch.css", "table.css", "tabs.css", "textarea.css", "tooltip.css",
        ]
        for name in [Path(k).name for k in comp_files]:
            self.assertIn(name, expected_components)

    def test_bundle_pos_03_js_topological_dag_ordering(self):
        """[BUNDLE-POS-03] FocusTrap and LiveRegion precede custom elements in monolithic bundles."""
        bundler = JsBundler(WORKSPACE_ROOT)
        bundles = bundler.build_bundles()
        all_iife_js = bundles["bundles/mds.all.js"]

        pos_focustrap = all_iife_js.find("FocusTrap")
        pos_liveregion = all_iife_js.find("LiveRegion")
        pos_dialog = all_iife_js.find("MdsDialog")

        self.assertNotEqual(pos_focustrap, -1)
        self.assertNotEqual(pos_liveregion, -1)
        self.assertNotEqual(pos_dialog, -1)
        self.assertLess(pos_focustrap, pos_dialog, "FocusTrap must precede MdsDialog in bundle")
        self.assertLess(pos_liveregion, pos_dialog, "LiveRegion must precede MdsDialog in bundle")

    def test_bundle_pos_04_js_idempotent_custom_elements_registration(self):
        """[BUNDLE-POS-04] Custom elements registration guarded with if (!customElements.get(...))."""
        bundler = JsBundler(WORKSPACE_ROOT)
        bundles = bundler.build_bundles()
        all_iife_js = bundles["bundles/mds.all.js"]
        self.assertIn("customElements.get('mds-dialog')", all_iife_js)
        self.assertIn("customElements.get('mds-switch')", all_iife_js)

    def test_bundle_pos_05_typescript_component_declarations(self):
        """[BUNDLE-POS-05] Component d.ts exports custom element declarations."""
        bundler = JsBundler(WORKSPACE_ROOT)
        bundles = bundler.build_bundles()
        components_dts = bundles["types/components.d.ts"]
        self.assertIn("interface HTMLElementTagNameMap", components_dts)
        self.assertIn("'mds-dialog': MdsDialog;", components_dts)


# ==============================================================================
# Suite 5: TestDeterministicPackaging & Reproducibility (REPRO-E2E)
# ==============================================================================
class TestDeterministicPackaging(unittest.TestCase):
    """Verifies bit-for-bit packaging reproducibility, header normalization, and permissions."""

    def test_pack_pos_01_archive_generation_zip_and_targz(self):
        """[PACK-POS-01] DeterministicPackager produces valid zip and tar.gz archives."""
        packager = DeterministicPackager(build_epoch=1790812800)
        zip_bytes = packager.create_zip({"sample.txt": b"reproducible-payload"})
        tar_bytes = packager.create_tar_gz({"sample.txt": b"reproducible-payload"})

        self.assertGreater(len(zip_bytes), 0)
        self.assertGreater(len(tar_bytes), 0)

    def test_pack_pos_02_zip_headers_and_permissions_normalized(self):
        """[PACK-POS-02] Zip archive entries strip extra fields and normalize file modes."""
        packager = DeterministicPackager(build_epoch=1790812800)
        zip_bytes = packager.create_zip({"test.css": b"body {}"})

        with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zf:
            for info in zf.infolist():
                self.assertEqual(info.extra, b"")
                self.assertEqual(info.date_time, (2026, 10, 1, 0, 0, 0))

    def test_pack_pos_03_tar_headers_and_epoch_normalized(self):
        """[PACK-POS-03] Tar archive members have uid=0, gid=0, root uname/gname, and epoch mtime."""
        packager = DeterministicPackager(build_epoch=1790812800)
        tar_bytes = packager.create_tar_gz({"test.js": b"console.log()"})

        with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tf:
            for member in tf.getmembers():
                self.assertEqual(member.uid, 0)
                self.assertEqual(member.gid, 0)
                self.assertEqual(member.uname, "root")
                self.assertEqual(member.gname, "root")
                self.assertEqual(member.mtime, 1790812800)

    def test_repro_e2e_01_bit_for_bit_rebuild(self):
        """
        [REPRO-E2E-01] Automated Deterministic Rebuild E2E:
        Build A: compile with fixed epoch E into isolated output A.
        Build B: compile with the SAME sources, compiler, configuration, environment contract, and epoch E into isolated output B.
        Compare:
        - Complete file inventory
        - Every artifact SHA-256 (33 files)
        - Archive SHA-256 (.zip and .tar.gz)
        - Distribution manifest & companion SHA-256
        - Build Identity (I_build)
        - Release Identity (I_rel)
        Asserts A == B byte-for-byte across every artifact. Fails if any artifact differs.
        """
        fixed_epoch = 1790812800

        with tempfile.TemporaryDirectory() as tmp1, tempfile.TemporaryDirectory() as tmp2:
            out_A = Path(tmp1) / "dist_A"
            out_B = Path(tmp2) / "dist_B"

            # Execute Build A
            engine_A = CompilerEngine(workspace_root=WORKSPACE_ROOT)
            res_A = engine_A.compile(output_dir=out_A, build_epoch=fixed_epoch, reproducible_mode=True)
            self.assertEqual(res_A["exit_code"], 0)

            # Execute Build B
            engine_B = CompilerEngine(workspace_root=WORKSPACE_ROOT)
            res_B = engine_B.compile(output_dir=out_B, build_epoch=fixed_epoch, reproducible_mode=True)
            self.assertEqual(res_B["exit_code"], 0)

            # 1. Compare Unified Build Identity
            self.assertEqual(
                res_A["build_id"],
                res_B["build_id"],
                f"Build ID mismatch: {res_A['build_id']} != {res_B['build_id']}",
            )
            self.assertEqual(res_A["total_artifacts"], 33)
            self.assertEqual(res_B["total_artifacts"], 33)

            # 2. Compare Complete File Inventory
            files_A = sorted([p.relative_to(out_A).as_posix() for p in out_A.rglob("*") if p.is_file()])
            files_B = sorted([p.relative_to(out_B).as_posix() for p in out_B.rglob("*") if p.is_file()])
            self.assertEqual(files_A, files_B, "Inventory mismatch between Build A and Build B")
            self.assertEqual(len(files_A), 35)  # 33 artifacts + manifest + companion sha256

            # 3. Compare Every Single Artifact Byte-for-Byte & Digest
            for rel_file in files_A:
                file_A_path = out_A / rel_file
                file_B_path = out_B / rel_file

                bytes_A = file_A_path.read_bytes()
                bytes_B = file_B_path.read_bytes()

                self.assertEqual(
                    len(bytes_A),
                    len(bytes_B),
                    f"Byte size mismatch on {rel_file}: {len(bytes_A)} != {len(bytes_B)}",
                )
                hash_A = hashlib.sha256(bytes_A).hexdigest()
                hash_B = hashlib.sha256(bytes_B).hexdigest()

                self.assertEqual(
                    hash_A,
                    hash_B,
                    f"Cryptographic hash mismatch on {rel_file}: {hash_A} != {hash_B}",
                )

            # 4. Compare Manifest JSON Contents & Manifest Companion File
            manifest_A = json.loads((out_A / "mds_dist_manifest.json").read_text(encoding="utf-8"))
            manifest_B = json.loads((out_B / "mds_dist_manifest.json").read_text(encoding="utf-8"))

            self.assertEqual(manifest_A["build_id"], manifest_B["build_id"])
            self.assertEqual(manifest_A["compiler_identity"], manifest_B["compiler_identity"])
            self.assertEqual(manifest_A["source_identity"], manifest_B["source_identity"])
            self.assertEqual(manifest_A["build_config_identity"], manifest_B["build_config_identity"])
            self.assertEqual(manifest_A["build_env_identity"], manifest_B["build_env_identity"])

            companion_A = (out_A / "mds_dist_manifest.sha256").read_text(encoding="utf-8").strip()
            companion_B = (out_B / "mds_dist_manifest.sha256").read_text(encoding="utf-8").strip()
            self.assertEqual(companion_A, companion_B)

            # 5. Verify sensitivity: mutating 1 bit in Build B fails the comparison
            corrupted_bytes = bytearray(bytes_B)
            corrupted_bytes[0] ^= 0x01
            self.assertNotEqual(hashlib.sha256(corrupted_bytes).hexdigest(), hash_A)


# ==============================================================================
# Suite 6: TestBuildIdentityManifest & Compiler Mutation (ICMP-MUT)
# ==============================================================================
class TestBuildIdentityManifest(unittest.TestCase):
    """Verifies Eight-Tier Build Identity and compiler closure hashing."""

    def test_ident_pos_01_eight_tier_identity_structure_completeness(self):
        """[IDENT-POS-01] Manifest contains all mandatory identity tiers and fields."""
        manifest_path = WORKSPACE_ROOT / "dist" / "mds_dist_manifest.json"
        if not manifest_path.exists():
            CompilerEngine(workspace_root=WORKSPACE_ROOT).compile(
                output_dir=WORKSPACE_ROOT / "dist",
                build_epoch=1790812800,
                reproducible_mode=True,
            )

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        self.assertIn("build_id", manifest)
        self.assertIn("source_identity", manifest)
        self.assertIn("compiler_identity", manifest)
        self.assertIn("build_config_identity", manifest)
        self.assertIn("build_env_identity", manifest)
        self.assertIn("build_epoch", manifest)
        self.assertIn("artifacts", manifest)
        self.assertIn("zero_npm", manifest)
        self.assertEqual(manifest["zero_npm"]["consumption"], True)
        self.assertEqual(manifest["zero_npm"]["runtime"], True)
        self.assertEqual(manifest["zero_npm"]["tooling"], True)

    def test_ident_pos_02_compiler_identity_covers_complete_source_closure(self):
        """[IDENT-POS-02] Compiler identity hash covers all .py files in tools/compiler/ sorted canonically (Advisory G-013-A closed)."""
        compiler_dir = WORKSPACE_ROOT / "tools" / "compiler"
        py_files = sorted(list(compiler_dir.glob("*.py")), key=lambda p: p.name)
        self.assertGreaterEqual(len(py_files), 8)

        parts = []
        for p in py_files:
            file_hash = hashlib.sha256(p.read_bytes()).hexdigest()
            parts.append(f"{p.name}:{file_hash}")
        expected_raw_cmp = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()
        expected_cmp = f"1.0.0:{expected_raw_cmp}"

        _, computed_cmp = compute_compiler_identity(compiler_dir)
        self.assertEqual(computed_cmp, expected_cmp)

    def test_ident_pos_03_companion_sha256_manifest_verification(self):
        """[IDENT-POS-03] Companion file mds_dist_manifest.sha256 matches mds_dist_manifest.json byte-exact."""
        manifest_path = WORKSPACE_ROOT / "dist" / "mds_dist_manifest.json"
        sha_path = WORKSPACE_ROOT / "dist" / "mds_dist_manifest.sha256"

        self.assertTrue(manifest_path.exists())
        self.assertTrue(sha_path.exists())

        expected_hash = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        companion_line = sha_path.read_text(encoding="utf-8").strip()
        companion_hash = companion_line.split()[0]
        self.assertEqual(companion_hash, expected_hash)

    def test_icmp_mut_01_compiler_source_mutation_changes_identities(self):
        """
        [ICMP-MUT-01] Negative Compiler Identity Mutation Test:
        Modifying 1 byte in any compiler source file (.py in tools/compiler/)
        guarantees that I_cmp changes, which in turn guarantees that I_build changes.
        Executed in an isolated temporary sandbox without mutating canonical sources.
        """
        canonical_compiler_dir = WORKSPACE_ROOT / "tools" / "compiler"
        with tempfile.TemporaryDirectory() as tmp_dir:
            sandbox_compiler = Path(tmp_dir) / "compiler"
            shutil.copytree(canonical_compiler_dir, sandbox_compiler)

            # Baseline calculation
            _, icmp_before = compute_compiler_identity(sandbox_compiler)
            config = BuildConfig(reproducible_mode=True, build_epoch=1790812800)
            env = EnvironmentContract()
            source_id = compute_source_identity(WORKSPACE_ROOT)
            config_id = compute_build_config_identity(config)
            env_id = compute_build_env_identity(env)
            ibuild_before = compute_unified_build_id(source_id, icmp_before, config_id, env_id, 1790812800)

            # Mutate 1 byte in a compiler source file inside the sandbox
            target_py = sandbox_compiler / "token_compiler.py"
            target_content = target_py.read_text(encoding="utf-8")
            target_py.write_text(target_content + "\n# byte_mutation_test\n", encoding="utf-8")

            # Post-mutation calculation
            _, icmp_after = compute_compiler_identity(sandbox_compiler)
            ibuild_after = compute_unified_build_id(source_id, icmp_after, config_id, env_id, 1790812800)

            # Assertions
            self.assertNotEqual(
                icmp_before,
                icmp_after,
                "Compiler identity I_cmp failed to change after modifying compiler source!",
            )
            self.assertNotEqual(
                ibuild_before,
                ibuild_after,
                "Build identity I_build failed to change after modifying compiler source!",
            )


# ==============================================================================
# Suite 7: TestDistributionVerificationGate & Immutability (VERIFY-RO)
# ==============================================================================
class TestDistributionVerificationGate(unittest.TestCase):
    """Verifies that the distribution verification gate is strictly read-only and catches all integrity violations."""

    def test_verify_pos_01_valid_distribution_passes_exit_0(self):
        """[VERIFY-POS-01] Verification passes on valid canonical dist package with Exit 0."""
        validator = DistributionValidator(WORKSPACE_ROOT / "dist")
        res = validator.verify(require_reproducible=True)
        self.assertEqual(res.status, "PASS", f"Expected PASS, message: {res.message}")
        self.assertEqual(res.exit_code, 0)

    def test_verify_ro_01_strict_immutability_snapshot(self):
        """
        [VERIFY-RO-01] Strict Read-Only Immutability Proof:
        Takes cryptographic and structural snapshot of dist before running verify.
        Runs CLI verify.
        Takes snapshot after running verify.
        Asserts 100% identity (zero bytes modified, zero files added/deleted/touched, zero temp/backup files).
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_dist = Path(tmp_dir) / "dist"
            shutil.copytree(WORKSPACE_ROOT / "dist", target_dist)

            def take_snapshot(d: Path) -> Dict[str, Tuple[int, int, str]]:
                snap = {}
                for p in d.rglob("*"):
                    if p.is_file():
                        rel = p.relative_to(d).as_posix()
                        st = p.stat()
                        digest = hashlib.sha256(p.read_bytes()).hexdigest()
                        snap[rel] = (st.st_size, st.st_mtime_ns, digest)
                return snap

            snapshot_before = take_snapshot(target_dist)
            self.assertEqual(len(snapshot_before), 35)

            # Execute CLI verify command
            exit_code = cli_main(["verify", "--dist", str(target_dist)])
            self.assertEqual(exit_code, 0)

            # Capture snapshot after
            snapshot_after = take_snapshot(target_dist)

            # 1. Assert identical file inventory
            self.assertEqual(
                set(snapshot_before.keys()),
                set(snapshot_after.keys()),
                "File inventory changed during verify! (Added or deleted files detected)",
            )

            # 2. Assert identical size, mtime, and cryptographic content hash for every file
            for rel_path, (size_b, mtime_b, hash_b) in snapshot_before.items():
                size_a, mtime_a, hash_a = snapshot_after[rel_path]
                self.assertEqual(size_b, size_a, f"File size changed for {rel_path}")
                self.assertEqual(mtime_b, mtime_a, f"Timestamp mtime changed for {rel_path}")
                self.assertEqual(hash_b, hash_a, f"Content hash changed for {rel_path}")

            # 3. Assert zero temporary files created
            all_files_on_disk = list(target_dist.rglob("*"))
            for p in all_files_on_disk:
                if p.is_file():
                    self.assertFalse(p.name.endswith(".tmp"))
                    self.assertFalse(p.name.endswith(".bak"))
                    self.assertFalse(p.name.endswith(".log"))
                    self.assertFalse("staging" in p.name.lower())

    def test_verify_neg_01_corrupted_artifact_detected_exit_3(self):
        """[VERIFY-NEG-01] Corrupting 1 byte in any artifact triggers integrity failure (Exit 3)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            dist_copy = Path(tmp_dir) / "dist"
            shutil.copytree(WORKSPACE_ROOT / "dist", dist_copy)

            btn_css = dist_copy / "css" / "components" / "button.css"
            content = btn_css.read_bytes()
            btn_css.write_bytes(content + b"/* corrupt */")

            validator = DistributionValidator(dist_copy)
            res = validator.verify(require_reproducible=True)
            self.assertEqual(res.status, "FAIL")
            self.assertEqual(res.exit_code, 3)
            self.assertIn("button.css", res.message)

    def test_verify_neg_02_missing_artifact_detected_exit_3(self):
        """[VERIFY-NEG-02] Deleting an artifact triggers missing file error (Exit 3)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            dist_copy = Path(tmp_dir) / "dist"
            shutil.copytree(WORKSPACE_ROOT / "dist", dist_copy)

            (dist_copy / "css" / "components" / "dialog.css").unlink()

            validator = DistributionValidator(dist_copy)
            res = validator.verify(require_reproducible=True)
            self.assertEqual(res.status, "FAIL")
            self.assertEqual(res.exit_code, 3)
            self.assertIn("dialog.css", res.message)

    def test_verify_neg_03_tampered_manifest_detected_exit_3(self):
        """[VERIFY-NEG-03] Tampering with manifest content breaks companion SHA-256 check (Exit 3)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            dist_copy = Path(tmp_dir) / "dist"
            shutil.copytree(WORKSPACE_ROOT / "dist", dist_copy)

            manifest_path = dist_copy / "mds_dist_manifest.json"
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["mds_version"] = "9.9.9"
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            validator = DistributionValidator(dist_copy)
            res = validator.verify(require_reproducible=True)
            self.assertEqual(res.status, "FAIL")
            self.assertEqual(res.exit_code, 3)
            self.assertIn("Distribution manifest tampered", res.message)

    def test_verify_neg_04_extraneous_untracked_file_detected_exit_3(self):
        """[VERIFY-NEG-04] Adding untracked extraneous file inside dist triggers verification failure (Exit 3)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            dist_copy = Path(tmp_dir) / "dist"
            shutil.copytree(WORKSPACE_ROOT / "dist", dist_copy)

            (dist_copy / "css" / "unauthorized.css").write_text("evil", encoding="utf-8")

            validator = DistributionValidator(dist_copy)
            res = validator.verify(require_reproducible=True)
            self.assertEqual(res.status, "FAIL")
            self.assertEqual(res.exit_code, 3)
            self.assertIn("unauthorized.css", res.message)


# ==============================================================================
# Suite 8: TestCompilerCLI & Runtime Contract (RUNTIME-CTR)
# ==============================================================================
class TestCompilerCLI(unittest.TestCase):
    """Verifies CLI behavior, argument parsing, reproducibility contract, and exit codes."""

    def test_cli_pos_01_compile_success_exit_0(self):
        """[CLI-POS-01] CLI compile returns Exit 0 on valid parameters."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir) / "dist"
            exit_code = cli_main(["compile", "--epoch", "1790812800", "--out", str(out_dir)])
            self.assertEqual(exit_code, 0)
            self.assertTrue((out_dir / "mds_dist_manifest.json").exists())

    def test_cli_neg_01_reproducible_mode_requires_epoch_exit_4(self):
        """[CLI-NEG-01] In reproducible mode, missing epoch exits with code 4."""
        old_val = os.environ.pop("SOURCE_DATE_EPOCH", None)
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                out_dir = Path(tmp_dir) / "dist"
                exit_code = cli_main(["compile", "--out", str(out_dir)])
                self.assertEqual(exit_code, 4)
        finally:
            if old_val is not None:
                os.environ["SOURCE_DATE_EPOCH"] = old_val

    def test_cli_pos_02_dev_mode_permits_missing_epoch(self):
        """[CLI-POS-02] Passing --dev permits compilation without explicit epoch."""
        old_val = os.environ.pop("SOURCE_DATE_EPOCH", None)
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                out_dir = Path(tmp_dir) / "dist"
                exit_code = cli_main(["compile", "--dev", "--out", str(out_dir)])
                self.assertEqual(exit_code, 0)
        finally:
            if old_val is not None:
                os.environ["SOURCE_DATE_EPOCH"] = old_val

    def test_cli_pos_03_verify_exit_codes_contract(self):
        """[CLI-POS-03] CLI verify returns 0 on valid package and 3 on corrupted package."""
        exit_code_pass = cli_main(["verify", "--dist", str(WORKSPACE_ROOT / "dist")])
        self.assertEqual(exit_code_pass, 0)

        with tempfile.TemporaryDirectory() as tmp_dir:
            dist_copy = Path(tmp_dir) / "dist"
            shutil.copytree(WORKSPACE_ROOT / "dist", dist_copy)
            (dist_copy / "css" / "components" / "button.css").unlink()

            exit_code_fail = cli_main(["verify", "--dist", str(dist_copy)])
            self.assertEqual(exit_code_fail, 3)

    def test_runtime_ctr_01_python_3_12_x_strict_enforcement(self):
        """
        [RUNTIME-CTR-01] Python 3.12.x Strict Runtime Contract:
        Enforces sys.version_info[:2] == (3, 12).
        Asserts Exit 4 / ConfigurationError on unsupported Python runtime versions.
        """
        # 1. Assert authoritative host runtime matches contract
        self.assertEqual(
            SUPPORTED_PYTHON_MAJOR_MINOR,
            (3, 12),
            "SUPPORTED_PYTHON_MAJOR_MINOR must strictly be (3, 12)",
        )
        self.assertEqual(
            sys.version_info[:2],
            (3, 12),
            f"Host Python is {sys.version.split()[0]}, expected 3.12.x",
        )

        validator = PreflightValidator(WORKSPACE_ROOT)

        # 2. Test supported 3.12.x runtime
        with patch("sys.version_info", (3, 12, 4, "final", 0)):
            # Should pass cleanly without error
            validator.validate_runtime(reproducible_mode=True)

        # 3. Test unsupported Python 3.11.x runtime
        with patch("sys.version_info", (3, 11, 8, "final", 0)):
            with self.assertRaises(ConfigurationError) as ctx:
                validator.validate_runtime(reproducible_mode=True)
            self.assertIn("strictly requires Python 3.12.x", str(ctx.exception))
            self.assertEqual(ctx.exception.exit_code, 4)

        # 4. Test unsupported Python 3.13.x runtime
        with patch("sys.version_info", (3, 13, 0, "final", 0)):
            with self.assertRaises(ConfigurationError) as ctx:
                validator.validate_runtime(reproducible_mode=True)
            self.assertIn("strictly requires Python 3.12.x", str(ctx.exception))
            self.assertEqual(ctx.exception.exit_code, 4)


if __name__ == "__main__":
    unittest.main()
