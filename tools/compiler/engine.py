"""
Master Design System (MDS) — Six-Stage Production Compiler Orchestrator
Phase 10.3: Production Artifact Compilation & Zero-NPM Distribution
Layer 13: Implementation, Tooling & Operationalization
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from .css_bundler import CssBundler
from .js_bundler import JsBundler
from .manifest_generator import ManifestGenerator
from .models import (
    AUTHORITATIVE_SOURCE_MANIFEST_DIGEST,
    BuildConfig,
    CompilerError,
    ConfigurationError,
    ContractViolationError,
    EnvironmentContract,
    IntegrityViolationError,
    SourceValidationError,
    VerificationResult,
)
from .packager import DeterministicPackager
from .token_compiler import TokenCompiler
from .validator import DistributionValidator, PreflightValidator


class CompilerEngine:
    """
    Six-Stage Transactional Production Compiler Engine:
    Stage 1: Pre-Flight Source Validation & Trust Chain Verification
    Stage 2: Design Token Resolution & DAG Compilation
    Stage 3: CSS Cascade Layer Scoping & Bundle Concatenation
    Stage 4: Custom Elements JavaScript Topological Packaging
    Stage 5: Deterministic Archive Creation & Eight-Tier Build Identity Manifest Sealing
    Stage 6: Atomic Staging, Transactional Commit & Post-State Verification
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.compiler_root = Path(__file__).resolve().parent

    def compile(
        self,
        output_dir: Optional[Path] = None,
        reproducible_mode: bool = True,
        build_epoch: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Executes the complete transactional compilation pipeline.
        """
        out_root = (output_dir or (self.workspace_root / "dist")).resolve()
        staging_dir = out_root.parent / "dist_staging_tmp"

        # Check explicit epoch in reproducible mode
        if reproducible_mode:
            env_epoch = os.environ.get("SOURCE_DATE_EPOCH")
            if build_epoch is None and env_epoch:
                try:
                    build_epoch = int(env_epoch)
                except ValueError:
                    raise ConfigurationError(f"Invalid integer in SOURCE_DATE_EPOCH: {env_epoch}")

            if build_epoch is None:
                raise ConfigurationError(
                    "Missing mandatory build epoch! Reproducible mode requires explicit SOURCE_DATE_EPOCH "
                    "or --epoch <timestamp>. Silent Git fallback is strictly prohibited."
                )

        config = BuildConfig(
            reproducible_mode=reproducible_mode,
            build_epoch=build_epoch,
        )
        env_contract = EnvironmentContract()

        # Clean staging directory if lingering
        if staging_dir.exists():
            shutil.rmtree(staging_dir, ignore_errors=True)

        try:
            # ==================================================================
            # Stage 1: Preflight Verification
            # ==================================================================
            preflight = PreflightValidator(self.workspace_root)
            preflight.validate_runtime(reproducible_mode=reproducible_mode)
            preflight.validate_trust_chain_and_sources()

            # In-memory artifact dictionary mapping relative POSIX path -> bytes
            artifacts_payload: Dict[str, bytes] = {}

            # ==================================================================
            # Stage 2: Token Resolution & Compilation
            # ==================================================================
            tc = TokenCompiler(self.workspace_root)
            tokens_json, tokens_css, tokens_dts = tc.compile()
            artifacts_payload["tokens/tokens.json"] = tokens_json.encode("utf-8")
            artifacts_payload["tokens/tokens.css"] = tokens_css.encode("utf-8")
            artifacts_payload["tokens/tokens.d.ts"] = tokens_dts.encode("utf-8")

            # ==================================================================
            # Stage 3: CSS Layer Scoping & Bundling
            # ==================================================================
            cb = CssBundler(self.workspace_root)
            css_bundles = cb.build_bundles(tokens_css)
            for rel_path, content in css_bundles.items():
                artifacts_payload[rel_path] = content.encode("utf-8")

            # ==================================================================
            # Stage 4: Custom Elements JavaScript Topological Packaging
            # ==================================================================
            jb = JsBundler(self.workspace_root)
            js_bundles = jb.build_bundles()
            for rel_path, content in js_bundles.items():
                artifacts_payload[rel_path] = content.encode("utf-8")

            # ==================================================================
            # Stage 5: Archive Creation & Manifest Generation
            # ==================================================================
            epoch_val = build_epoch if build_epoch is not None else 1790812800
            packager = DeterministicPackager(build_epoch=epoch_val)
            zip_bytes, tar_gz_bytes = packager.package_distribution(artifacts_payload)
            artifacts_payload["archives/mds-v1.0.0-dist.zip"] = zip_bytes
            artifacts_payload["archives/mds-v1.0.0-dist.tar.gz"] = tar_gz_bytes

            mg = ManifestGenerator(self.workspace_root, self.compiler_root)
            manifest_json, companion_sha256 = mg.generate_manifest(config, env_contract, artifacts_payload)
            manifest_bytes = manifest_json.encode("utf-8")
            companion_bytes = companion_sha256.encode("utf-8")

            # ==================================================================
            # Stage 6: Atomic Staging, Transactional Commit & Verification
            # ==================================================================
            staging_dir.mkdir(parents=True, exist_ok=True)

            # Write all artifacts to staging
            for rel_path, data in artifacts_payload.items():
                dest_file = staging_dir / rel_path
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                dest_file.write_bytes(data)

            # Write manifest and companion
            (staging_dir / "mds_dist_manifest.json").write_bytes(manifest_bytes)
            (staging_dir / "mds_dist_manifest.sha256").write_bytes(companion_bytes)

            # Atomic swap
            if out_root.exists():
                shutil.rmtree(out_root, ignore_errors=True)

            staging_dir.rename(out_root)

            # Post-state read-only verification
            dist_validator = DistributionValidator(out_root)
            verify_res = dist_validator.verify(require_reproducible=reproducible_mode)
            if verify_res.exit_code != 0:
                raise IntegrityViolationError(f"Post-compilation verification failed: {verify_res.message}")

            return {
                "status": "SUCCESS",
                "exit_code": 0,
                "output_dir": str(out_root),
                "build_id": verify_res.details.get("build_id"),
                "total_artifacts": verify_res.details.get("verified_artifacts"),
                "total_bytes": verify_res.details.get("total_bytes"),
                "reproducible": reproducible_mode,
                "build_epoch": build_epoch,
            }

        except Exception as e:
            # Transaction rollback: cleanly remove staging on failure
            if staging_dir.exists():
                shutil.rmtree(staging_dir, ignore_errors=True)
            raise e
