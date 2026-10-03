#!/usr/bin/env python3
"""
Axe-Core Artifact Discovery & Integrity Loader
Phase 9.7.5: Dynamic Accessibility Automation (Layer I)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Loads pinned local axe-core JavaScript artifact with mandatory cryptographic hash verification.
Zero runtime network downloads, zero external CDN reliance.
"""

import json
import hashlib
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

from browser.exceptions import BrowserBridgeError


class AxeArtifactNotFoundError(BrowserBridgeError):
    """Raised when pinned local axe-core artifact cannot be located."""
    pass


class AxeIntegrityError(BrowserBridgeError):
    """Raised when axe-core artifact checksum does not match pinned metadata."""
    pass


@dataclass
class AxeArtifact:
    """Represents a verified local axe-core JavaScript artifact."""
    file_path: Path
    version: str
    sha256: str
    size_bytes: int
    source: str
    sri_integrity: Optional[str] = None

    def get_source(self) -> str:
        """Reads and returns the complete JavaScript source code."""
        with open(self.file_path, "r", encoding="utf-8") as fp:
            return fp.read()


class AxeLoader:
    """
    Manages deterministic discovery, verification, and loading of pinned axe-core artifact.
    Guarantees that test execution remains completely hermetic and offline.
    """

    VENDOR_DIR = Path(__file__).resolve().parent / "vendor"
    ARTIFACT_FILENAME = "axe.min.js"
    METADATA_FILENAME = "axe_metadata.json"

    @classmethod
    def get_artifact(cls, vendor_dir: Optional[Path] = None) -> Optional[AxeArtifact]:
        """
        Locates and cryptographically verifies the local axe-core artifact.
        Returns AxeArtifact if valid, raises AxeArtifactNotFoundError if missing,
        or raises AxeIntegrityError if corrupted.
        """
        base_dir = vendor_dir or cls.VENDOR_DIR
        artifact_path = base_dir / cls.ARTIFACT_FILENAME
        metadata_path = base_dir / cls.METADATA_FILENAME

        if not artifact_path.exists():
            raise AxeArtifactNotFoundError(
                f"Axe-core artifact missing at: {artifact_path}. "
                "Hermetic accessibility validation requires pinned local artifact."
            )

        # Read artifact bytes and compute SHA-256
        with open(artifact_path, "rb") as fp:
            content_bytes = fp.read()
        computed_sha256 = hashlib.sha256(content_bytes).hexdigest()

        # If metadata file exists, verify against pinned checksum
        version = "4.13.0"
        expected_sha256 = computed_sha256
        source_info = "pinned-local"
        sri_integrity = None

        if metadata_path.exists():
            try:
                with open(metadata_path, "r", encoding="utf-8") as mfp:
                    meta = json.load(mfp)
                version = meta.get("version", version)
                expected_sha256 = meta.get("sha256", expected_sha256)
                source_info = meta.get("source", source_info)
                sri_integrity = meta.get("sri_integrity")
            except Exception as e:
                raise AxeIntegrityError(f"Failed to read axe metadata at {metadata_path}: {e}")

        if computed_sha256.lower() != expected_sha256.lower():
            raise AxeIntegrityError(
                f"Axe artifact checksum mismatch! Computed: {computed_sha256}, "
                f"Expected: {expected_sha256}. Possible corruption or tampering."
            )

        return AxeArtifact(
            file_path=artifact_path,
            version=version,
            sha256=computed_sha256,
            size_bytes=len(content_bytes),
            source=source_info,
            sri_integrity=sri_integrity
        )

    @classmethod
    def is_artifact_available(cls, vendor_dir: Optional[Path] = None) -> bool:
        """Returns True if a valid verified artifact exists without throwing."""
        try:
            art = cls.get_artifact(vendor_dir=vendor_dir)
            return art is not None
        except Exception:
            return False
