"""
Master Design System (MDS) — Distribution Manifest & Eight-Tier Build Identity Generator
Phase 10.3: Production Artifact Compilation & Zero-NPM Distribution
Layer 13: Implementation, Tooling & Operationalization
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import datetime
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from .models import (
    BuildConfig,
    CANONICAL_COMPILATION_SOURCES,
    COMPILER_VERSION,
    EnvironmentContract,
    MDS_VERSION,
    PACKAGE_NAME,
    SCHEMA_VERSION,
)


def compute_source_identity(workspace_root: Path) -> str:
    """
    Computes I_src: SHA-256 over canonically ordered (path, file_hash) pairs for all 61 sources.
    """
    parts = []
    for rel_path in sorted(CANONICAL_COMPILATION_SOURCES):
        fp = workspace_root / rel_path
        digest = hashlib.sha256(fp.read_bytes()).hexdigest()
        parts.append(f"{rel_path}:{digest}")
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def compute_compiler_identity(compiler_root: Path) -> Tuple[str, str]:
    """
    Computes I_cmp: Covers the COMPLETE compiler source closure (Advisory G-013-A).
    Discovers all .py files in tools/compiler/, sorts them canonically,
    and computes SHA-256 over their aggregated digests.
    Returns: (compiler_closure_digest, full_compiler_identity_string)
    """
    py_files = sorted([p for p in compiler_root.glob("*.py") if p.is_file()], key=lambda p: p.name)
    parts = []
    for py_file in py_files:
        digest = hashlib.sha256(py_file.read_bytes()).hexdigest()
        parts.append(f"{py_file.name}:{digest}")

    closure_digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()
    compiler_id = f"{COMPILER_VERSION}:{closure_digest}"
    return closure_digest, compiler_id


def compute_build_config_identity(config: BuildConfig) -> str:
    """
    Computes I_cfg: Canonical JSON SHA-256 of reproducibility-critical configuration.
    """
    canonical_json = json.dumps(config.canonical_dict(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def compute_build_env_identity(env: EnvironmentContract) -> str:
    """
    Computes I_env: Canonical JSON SHA-256 of deterministic execution environment contract.
    """
    canonical_json = json.dumps(env.canonical_dict(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def compute_unified_build_id(
    source_identity: str,
    compiler_identity: str,
    config_identity: str,
    env_identity: str,
    epoch: Optional[int],
) -> str:
    """
    Computes I_build = SHA256(I_src : I_cmp : I_cfg : I_env : str(T_epoch)).
    """
    epoch_str = str(epoch) if epoch is not None else "convenience-mode"
    composite = f"{source_identity}:{compiler_identity}:{config_identity}:{env_identity}:{epoch_str}"
    return hashlib.sha256(composite.encode("utf-8")).hexdigest()


def determine_artifact_metadata(rel_path: str) -> Dict[str, str]:
    """Infers content_type, tier, and role for artifact entry in manifest."""
    if rel_path.startswith("bundles/"):
        if rel_path.endswith(".css"):
            return {
                "content_type": "text/css; charset=utf-8",
                "tier": "bundle",
                "role": "monolithic_bundle",
            }
        elif rel_path.endswith(".js"):
            return {
                "content_type": "application/javascript; charset=utf-8",
                "tier": "bundle",
                "role": "monolithic_bundle",
            }
    elif rel_path.startswith("css/"):
        return {
            "content_type": "text/css; charset=utf-8",
            "tier": "modular_css",
            "role": "theme_override" if "tokens" in rel_path else "monolithic_bundle",
        }
    elif rel_path.startswith("js/"):
        return {
            "content_type": "application/javascript; charset=utf-8",
            "tier": "modular_js",
            "role": "monolithic_bundle",
        }
    elif rel_path.startswith("tokens/"):
        if rel_path.endswith(".json"):
            return {
                "content_type": "application/json; charset=utf-8",
                "tier": "tokens",
                "role": "token_dictionary",
            }
        elif rel_path.endswith(".css"):
            return {
                "content_type": "text/css; charset=utf-8",
                "tier": "tokens",
                "role": "theme_override",
            }
        elif rel_path.endswith(".d.ts"):
            return {
                "content_type": "text/typescript; charset=utf-8",
                "tier": "declarations",
                "role": "type_definition",
            }
    elif rel_path.startswith("types/"):
        return {
            "content_type": "text/typescript; charset=utf-8",
            "tier": "declarations",
            "role": "type_definition",
        }
    elif rel_path.startswith("archives/"):
        return {
            "content_type": "application/gzip" if rel_path.endswith(".tar.gz") else "application/zip",
            "tier": "archive",
            "role": "distribution_archive",
        }

    return {
        "content_type": "application/octet-stream",
        "tier": "bundle",
        "role": "monolithic_bundle",
    }


class ManifestGenerator:
    """
    Constructs the canonical distribution manifest (mds_dist_manifest.json)
    and external companion digest (mds_dist_manifest.sha256).
    """

    def __init__(self, workspace_root: Path, compiler_root: Path):
        self.workspace_root = workspace_root.resolve()
        self.compiler_root = compiler_root.resolve()

    def generate_manifest(
        self,
        config: BuildConfig,
        env: EnvironmentContract,
        emitted_artifacts: Dict[str, bytes],
    ) -> Tuple[str, str]:
        """
        Builds manifest and companion digest from in-memory or on-disk emitted artifacts.
        Returns: (manifest_json_str, manifest_sha256_companion_str)
        """
        source_id = compute_source_identity(self.workspace_root)
        _, compiler_id = compute_compiler_identity(self.compiler_root)
        config_id = compute_build_config_identity(config)
        env_id = compute_build_env_identity(env)
        build_id = compute_unified_build_id(source_id, compiler_id, config_id, env_id, config.build_epoch)

        # Artifacts roster
        artifacts_dict: Dict[str, Dict[str, Any]] = {}
        for rel_posix_path in sorted(emitted_artifacts.keys()):
            data = emitted_artifacts[rel_posix_path]
            meta = determine_artifact_metadata(rel_posix_path)
            artifacts_dict[rel_posix_path] = {
                "sha256": hashlib.sha256(data).hexdigest(),
                "byte_size": len(data),
                "content_type": meta["content_type"],
                "tier": meta["tier"],
                "role": meta["role"],
            }

        epoch_str = (
            datetime.datetime.fromtimestamp(config.build_epoch, tz=datetime.timezone.utc).isoformat()
            if config.build_epoch is not None
            else "convenience-mode"
        )

        manifest_data = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "schema_version": SCHEMA_VERSION,
            "package_name": PACKAGE_NAME,
            "mds_version": MDS_VERSION,
            "compiler_version": COMPILER_VERSION,
            "build_id": build_id,
            "build_epoch": epoch_str,
            "reproducible": config.reproducible_mode,
            "source_identity": {
                "source_hash": source_id,
                "source_file_count": len(CANONICAL_COMPILATION_SOURCES),
                "source_revision": "canonical-phase-10.3",
            },
            "compiler_identity": {
                "compiler_hash": compiler_id,
            },
            "build_config_identity": {
                "config_hash": config_id,
            },
            "build_env_identity": {
                "env_hash": env_id,
            },
            "zero_npm": {
                "runtime": True,
                "tooling": True,
                "consumption": True,
            },
            "artifacts": artifacts_dict,
        }

        manifest_json = json.dumps(manifest_data, indent=2, sort_keys=True) + "\n"
        manifest_digest = hashlib.sha256(manifest_json.encode("utf-8")).hexdigest()
        companion_sha256 = f"{manifest_digest}  mds_dist_manifest.json\n"

        return manifest_json, companion_sha256
