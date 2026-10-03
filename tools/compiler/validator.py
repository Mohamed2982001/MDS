"""
Master Design System (MDS) — Source Trust, Scope & Distribution Verification Engine
Phase 10.3: Production Artifact Compilation & Zero-NPM Distribution
Layer 13: Implementation, Tooling & Operationalization
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Set, Tuple

from .models import (
    AUTHORITATIVE_SOURCE_MANIFEST_DIGEST,
    CANONICAL_COMPILATION_SOURCES,
    CANONICAL_PROTECTED_NON_SOURCES,
    ROOT_TRUST_ANCHOR_FINGERPRINT,
    SUPPORTED_PYTHON_MAJOR_MINOR,
    BuildConfig,
    CompilerScopeViolationError,
    ConfigurationError,
    ContractViolationError,
    IntegrityViolationError,
    SourceValidationError,
    VerificationResult,
)


class PreflightValidator:
    """
    Stage 1 Pre-Flight Validation Engine:
    - Verifies Python runtime version (3.12.x)
    - Verifies Root Trust Anchor (MDS-ROOT-ANCHOR-v1)
    - Verifies source_trust_binding.json
    - Verifies canonical_source_manifest.json against AUTHORITATIVE_SOURCE_MANIFEST_DIGEST
    - Verifies all 61 canonical compilation source files byte-for-byte
    - Enforces strict Protected Non-Source isolation
    """

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()

    def validate_runtime(self, reproducible_mode: bool) -> None:
        """Enforces Python 3.12.x runtime contract in reproducible mode."""
        current_version = sys.version_info[:2]
        if current_version != SUPPORTED_PYTHON_MAJOR_MINOR:
            msg = (
                f"Unsupported Python runtime version: {sys.version.split()[0]}. "
                f"MDS compilation strictly requires Python {SUPPORTED_PYTHON_MAJOR_MINOR[0]}.{SUPPORTED_PYTHON_MAJOR_MINOR[1]}.x."
            )
            if reproducible_mode:
                raise ConfigurationError(msg)
            # In convenience mode, log advisory warning

    def validate_trust_chain_and_sources(self) -> Dict[str, Dict[str, Any]]:
        """
        Validates the 4-tier cryptographic trust chain and computes source digests.
        Returns: manifest sources dictionary
        """
        # Tier 1: Root Trust Anchor
        anchor_path = self.workspace_root / "MDS/10-Testing/baselines/historical/trust_anchor.json"
        if not anchor_path.exists():
            raise IntegrityViolationError(f"Root Trust Anchor missing: {anchor_path}")

        anchor_bytes = anchor_path.read_bytes()
        # Canonical cross-platform text hashing (ADR-106 / ADR-211: BOM stripped, CRLF -> LF)
        if anchor_bytes.startswith(b"\xef\xbb\xbf"):
            anchor_bytes = anchor_bytes[3:]
        anchor_normalized = anchor_bytes.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
        anchor_hash = hashlib.sha256(anchor_normalized).hexdigest()
        if anchor_hash != ROOT_TRUST_ANCHOR_FINGERPRINT:
            raise IntegrityViolationError(
                f"Root Trust Anchor fingerprint mismatch! Expected {ROOT_TRUST_ANCHOR_FINGERPRINT}, found {anchor_hash}"
            )

        # Tier 2: Source Trust Binding
        binding_path = self.workspace_root / "MDS/10-Testing/baselines/compilation/source_trust_binding.json"
        if not binding_path.exists():
            raise IntegrityViolationError(f"Source trust binding record missing: {binding_path}")

        try:
            binding_data = json.loads(binding_path.read_text(encoding="utf-8"))
        except Exception as e:
            raise IntegrityViolationError(f"Malformed source trust binding JSON: {e}")

        if binding_data.get("root_anchor_sha256") != ROOT_TRUST_ANCHOR_FINGERPRINT:
            raise IntegrityViolationError("Source trust binding does not bind to authoritative Root Trust Anchor")

        # Tier 3: Canonical Source Manifest
        manifest_path = self.workspace_root / "MDS/10-Testing/baselines/compilation/canonical_source_manifest.json"
        if not manifest_path.exists():
            raise IntegrityViolationError(f"Canonical source manifest missing: {manifest_path}")

        manifest_bytes = manifest_path.read_bytes()
        manifest_normalized = manifest_bytes.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
        manifest_hash = hashlib.sha256(manifest_normalized).hexdigest()

        expected_binding_digest = binding_data.get("source_manifest_sha256")
        if manifest_hash != expected_binding_digest:
            raise IntegrityViolationError(
                f"Source manifest hash mismatch against binding! Computed: {manifest_hash}, Binding: {expected_binding_digest}"
            )

        if manifest_hash != AUTHORITATIVE_SOURCE_MANIFEST_DIGEST:
            raise IntegrityViolationError(
                f"Source manifest tampered! Does not match compiled constant AUTHORITATIVE_SOURCE_MANIFEST_DIGEST: {manifest_hash}"
            )

        try:
            manifest_data = json.loads(manifest_bytes.decode("utf-8"))
        except Exception as e:
            raise IntegrityViolationError(f"Malformed source manifest JSON: {e}")

        manifest_sources = manifest_data.get("sources", {})
        if len(manifest_sources) != len(CANONICAL_COMPILATION_SOURCES):
            raise IntegrityViolationError(
                f"Source manifest count mismatch: expected {len(CANONICAL_COMPILATION_SOURCES)}, found {len(manifest_sources)}"
            )

        # Tier 4: Verify 61 Allowlisted Source Files on Disk
        for rel_posix_path in sorted(CANONICAL_COMPILATION_SOURCES):
            # Scope check: never allow traversing out of workspace or reading protected non-sources
            if rel_posix_path in CANONICAL_PROTECTED_NON_SOURCES:
                raise CompilerScopeViolationError(
                    f"Compiler scope violation: attempted ingestion of protected non-source: {rel_posix_path}"
                )

            full_path = self.workspace_root / rel_posix_path
            if not full_path.exists():
                raise SourceValidationError(f"Required compilation source missing from disk: {rel_posix_path}")

            actual_digest = hashlib.sha256(full_path.read_bytes()).hexdigest()
            expected_info = manifest_sources.get(rel_posix_path)
            if not expected_info:
                raise IntegrityViolationError(f"Source file {rel_posix_path} not found in verified manifest")

            if actual_digest != expected_info.get("sha256"):
                raise IntegrityViolationError(
                    f"Source integrity violation in {rel_posix_path}! Expected {expected_info.get('sha256')}, got {actual_digest}"
                )

        return manifest_sources


class DistributionValidator:
    """
    Exclusively READ-ONLY Distribution Verification Gate:
    - Never compiles, never packs, never writes to disk
    - Verifies manifest self-integrity companion hash
    - Verifies every artifact SHA-256 and byte size against manifest
    - Asserts reproducibility flag (reproducible === true)
    - Asserts major version lock-step
    """

    @staticmethod
    def validate_file_in_scope(file_path: Path, workspace_root: Path) -> str:
        """
        Enforces strict compiler scope boundary control:
        1. Resolves path against workspace_root (prevents traversal).
        2. Asserts normalized POSIX path is in CANONICAL_COMPILATION_SOURCES.
        3. Rejects any file in CANONICAL_PROTECTED_NON_SOURCES with CompilerScopeViolationError.
        4. Rejects any out-of-bounds file with CompilerScopeViolationError.
        """
        ws_root = workspace_root.resolve()
        resolved_file = file_path if file_path.is_absolute() else (ws_root / file_path).resolve()

        try:
            rel = resolved_file.relative_to(ws_root)
        except ValueError:
            raise CompilerScopeViolationError(
                f"Scope violation: Path '{file_path}' resolves outside workspace root."
            )

        rel_posix = rel.as_posix()
        if rel_posix in CANONICAL_PROTECTED_NON_SOURCES:
            raise CompilerScopeViolationError(
                f"Scope violation: Attempted to ingest Protected Non-Source '{rel_posix}'. Ingestion is strictly prohibited."
            )

        if rel_posix not in CANONICAL_COMPILATION_SOURCES:
            raise CompilerScopeViolationError(
                f"Scope violation: Path '{rel_posix}' is not in CANONICAL_COMPILATION_SOURCES."
            )

        return rel_posix

    def __init__(self, dist_root: Path):
        self.dist_root = dist_root.resolve()

    def verify(self, require_reproducible: bool = True) -> VerificationResult:
        """Executes strictly read-only distribution verification."""
        if not self.dist_root.exists() or not self.dist_root.is_dir():
            return VerificationResult(
                status="FAIL",
                exit_code=4,
                message=f"Distribution directory does not exist: {self.dist_root}",
            )

        manifest_path = self.dist_root / "mds_dist_manifest.json"
        companion_path = self.dist_root / "mds_dist_manifest.sha256"

        if not manifest_path.exists():
            return VerificationResult(
                status="FAIL",
                exit_code=4,
                message="mds_dist_manifest.json missing from distribution package",
            )

        if not companion_path.exists():
            return VerificationResult(
                status="FAIL",
                exit_code=3,
                message="mds_dist_manifest.sha256 companion digest missing",
            )

        # 1. Verify companion hash
        manifest_bytes = manifest_path.read_bytes()
        computed_manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()

        companion_text = companion_path.read_text(encoding="utf-8").strip()
        expected_manifest_hash = companion_text.split()[0] if companion_text else ""

        if computed_manifest_hash != expected_manifest_hash:
            return VerificationResult(
                status="FAIL",
                exit_code=3,
                message=(
                    f"Distribution manifest tampered! "
                    f"Computed hash: {computed_manifest_hash}, Expected in companion: {expected_manifest_hash}"
                ),
            )

        # 2. Parse manifest JSON
        try:
            manifest_data = json.loads(manifest_bytes.decode("utf-8"))
        except Exception as e:
            return VerificationResult(
                status="FAIL",
                exit_code=3,
                message=f"Malformed distribution manifest JSON: {e}",
            )

        # 3. Check reproducibility flag
        is_reproducible = manifest_data.get("reproducible", False)
        if require_reproducible and not is_reproducible:
            return VerificationResult(
                status="FAIL",
                exit_code=2,
                message="Package marked as non-reproducible (reproducible=false); rejected by Bootstrap Gate.",
            )

        # 4. Check version format
        version_str = manifest_data.get("mds_version", "")
        if not version_str or not version_str.startswith("1."):
            return VerificationResult(
                status="FAIL",
                exit_code=2,
                message=f"Incompatible MDS major version: {version_str}",
            )

        # 5. Check all artifacts on disk
        artifacts = manifest_data.get("artifacts", {})
        if not artifacts:
            return VerificationResult(
                status="FAIL",
                exit_code=3,
                message="Distribution manifest contains zero artifacts",
            )

        verified_count = 0
        total_bytes = 0

        for rel_posix_path, meta in sorted(artifacts.items()):
            # Path traversal check
            if ".." in rel_posix_path.split("/") or rel_posix_path.startswith("/"):
                return VerificationResult(
                    status="FAIL",
                    exit_code=3,
                    message=f"Path traversal detected in artifact path: '{rel_posix_path}'",
                )

            artifact_file = self.dist_root / rel_posix_path
            if not artifact_file.exists():
                return VerificationResult(
                    status="FAIL",
                    exit_code=3,
                    message=f"Artifact declared in manifest missing from disk: '{rel_posix_path}'",
                )

            data = artifact_file.read_bytes()
            actual_hash = hashlib.sha256(data).hexdigest()
            expected_hash = meta.get("sha256")

            if actual_hash != expected_hash:
                return VerificationResult(
                    status="FAIL",
                    exit_code=3,
                    message=(
                        f"Artifact '{rel_posix_path}' checksum mismatch! "
                        f"Expected {expected_hash}, found {actual_hash}"
                    ),
                )

            if len(data) != meta.get("byte_size"):
                return VerificationResult(
                    status="FAIL",
                    exit_code=3,
                    message=(
                        f"Artifact '{rel_posix_path}' byte size mismatch! "
                        f"Expected {meta.get('byte_size')}, found {len(data)}"
                    ),
                )

            verified_count += 1
            total_bytes += len(data)

        # 6. Check for unmanifested / extraneous files on disk
        manifest_files = set(artifacts.keys())
        manifest_files.add("mds_dist_manifest.json")
        manifest_files.add("mds_dist_manifest.sha256")

        for disk_file in self.dist_root.rglob("*"):
            if disk_file.is_file():
                rel_disk = disk_file.relative_to(self.dist_root).as_posix()
                if rel_disk not in manifest_files:
                    return VerificationResult(
                        status="FAIL",
                        exit_code=3,
                        message=f"Extraneous unmanifested file found on disk: '{rel_disk}'",
                    )

        return VerificationResult(
            status="PASS",
            exit_code=0,
            message="Distribution package verified with 100% cryptographic integrity.",
            details={
                "verified_artifacts": verified_count,
                "total_bytes": total_bytes,
                "build_id": manifest_data.get("build_id"),
                "reproducible": is_reproducible,
            },
        )
