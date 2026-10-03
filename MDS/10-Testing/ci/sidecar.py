"""
Master Design System (MDS) -- External Sidecar Manager
Document Reference: MDS-SPEC-9711-REV5 / Section 10 (ADR-149)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Tuple

from .models import ManifestAuthenticityError


HEX64_REGEX = re.compile(r"^[0-9a-f]{64}$")
SIDECAR_LINE_REGEX = re.compile(r"^([0-9a-fA-F]{64})\s{2}(.+)$")


class SidecarManager:
    """
    Manages external sidecar file `ci_artifact_manifest.sha256`.
    NOTE (ADR-151): The sidecar is a local convenience artifact.
    It does not independently establish authenticity unless verified against the Provider Control Plane.
    """

    @staticmethod
    def write_sidecar(manifest_path: Path, digest: str) -> Path:
        """
        Emits standard NIST sha256 sidecar file: `<digest>  ci_artifact_manifest.json`.
        """
        sidecar_path = manifest_path.with_name(f"{manifest_path.name.split('.')[0]}.sha256")
        if sidecar_path.name != "ci_artifact_manifest.sha256":
            sidecar_path = manifest_path.parent / "ci_artifact_manifest.sha256"

        content = f"{digest.lower()}  ci_artifact_manifest.json\n"
        sidecar_path.write_text(content, encoding="utf-8")
        return sidecar_path

    @staticmethod
    def parse_sidecar(sidecar_path: Path) -> Tuple[str, str]:
        """
        Parses sidecar file.
        Raises ManifestAuthenticityError if malformed (Case F).
        """
        if not sidecar_path.exists():
            raise ManifestAuthenticityError(f"Sidecar file does not exist: {sidecar_path}")

        raw = sidecar_path.read_text(encoding="utf-8").strip()
        match = SIDECAR_LINE_REGEX.match(raw)
        if not match:
            raise ManifestAuthenticityError(
                f"Malformed sidecar content (Case F): expected '<64-hex>  ci_artifact_manifest.json', got: {raw[:60]!r}"
            )

        digest = match.group(1).lower()
        filename = match.group(2).strip()

        if filename != "ci_artifact_manifest.json":
            raise ManifestAuthenticityError(
                f"Malformed sidecar content (Case F): target filename '{filename}' != 'ci_artifact_manifest.json'"
            )

        return digest, filename

    @classmethod
    def verify_sidecar(cls, expected_digest: str, sidecar_path: Path, is_ci: bool = True) -> bool:
        """
        Step 2 Verification: Asserts sidecar matches expected manifest digest.
        Handles Cases B, D, D-Local, and F.
        """
        if not sidecar_path.exists():
            if is_ci:
                raise ManifestAuthenticityError(
                    f"Sidecar missing in CI environment (Case D): mandatory artifact {sidecar_path} absent"
                )
            # Local mode: advisory only
            return False

        sidecar_digest, _ = cls.parse_sidecar(sidecar_path)

        if sidecar_digest != expected_digest.lower():
            raise ManifestAuthenticityError(
                f"Local sidecar digest mismatch (Case B): sidecar '{sidecar_digest}' != expected '{expected_digest}'"
            )

        return True
