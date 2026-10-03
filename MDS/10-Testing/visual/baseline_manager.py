#!/usr/bin/env python3
"""
MDS Baseline Manager & Cryptographic Integrity Guard
Phase 9.7.7: Visual Regression Engine & Snapshot Diffing
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Manages golden baseline PNGs, enforces read-only access during test runs,
verifies cryptographic SHA-256 hashes against `baselines_manifest.json`,
and validates deterministic font artifacts.
"""

import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

from .visual_models import BaselineConfig, VisualExecutionStatus


class BaselineIntegrityError(ValueError):
    """Raised when a baseline PNG fails its cryptographic SHA-256 manifest check."""
    pass


class FontArtifactUnavailableError(FileNotFoundError):
    """Raised when canonical local font artifacts are missing or corrupted."""
    pass


class BaselineManager:
    """
    Guarantees immutable baseline storage, cryptographic SHA-256 verification,
    and truthful local font artifact checks.
    """

    CANONICAL_BASELINE_IDS = [
        f"VIS-BASE-{i:03d}" for i in range(1, 13)
    ]

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(__file__).resolve().parent.parent.parent.parent
        self.visual_dir = self.workspace_root / "MDS" / "10-Testing" / "visual"
        self.baselines_dir = self.visual_dir / "baselines"
        self.manifest_path = self.baselines_dir / "baselines_manifest.json"
        self.fonts_dir = self.visual_dir / "vendor" / "fonts"

    @staticmethod
    def compute_sha256(data: bytes) -> str:
        """Computes lowercase hex SHA-256 hash of bytes."""
        return hashlib.sha256(data).hexdigest().lower()

    @staticmethod
    def compute_file_sha256(file_path: Path) -> str:
        """Computes lowercase hex SHA-256 hash of a file on disk."""
        return hashlib.sha256(file_path.read_bytes()).hexdigest().lower()

    def verify_fonts(self) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Verifies that canonical local Cairo font artifacts are present on disk
        and match their documented cryptographic SHA-256 hashes.
        Returns (is_valid, diagnostic_message, font_telemetry).
        """
        if not self.fonts_dir.exists():
            return False, "FONT_ARTIFACT_UNAVAILABLE: Fonts directory does not exist.", {}

        # Look for Cairo-Regular.ttf and Cairo-Bold.ttf
        reg_file = self.fonts_dir / "Cairo-Regular.ttf"
        bold_file = self.fonts_dir / "Cairo-Bold.ttf"

        if not reg_file.exists():
            # Check alternative naming
            reg_alt = self.fonts_dir / "cairo-regular.woff2"
            if reg_alt.exists():
                reg_file = reg_alt
            else:
                return False, f"FONT_ARTIFACT_UNAVAILABLE: Missing regular font artifact at {reg_file}", {}

        if not bold_file.exists():
            bold_alt = self.fonts_dir / "cairo-bold.woff2"
            if bold_alt.exists():
                bold_file = bold_alt
            else:
                return False, f"FONT_ARTIFACT_UNAVAILABLE: Missing bold font artifact at {bold_file}", {}

        reg_hash = self.compute_file_sha256(reg_file)
        bold_hash = self.compute_file_sha256(bold_file)

        # Expected canonical hashes calculated from Google Fonts upstream release
        expected_reg = "44786a38e27c58262cbd65341beda4fa4f6c7085ec42e830b35ba1ae37807030"
        expected_bold = "a0e58d71b85b15902ea87914d8e31a6d22da48ac2db70213dcfd1a7dad3f198a"

        if reg_hash != expected_reg:
            return False, f"FONT_ARTIFACT_CORRUPTED: Cairo-Regular SHA-256 mismatch ({reg_hash} != {expected_reg})", {}

        if bold_hash != expected_bold:
            return False, f"FONT_ARTIFACT_CORRUPTED: Cairo-Bold SHA-256 mismatch ({bold_hash} != {expected_bold})", {}

        font_info = {
            "regular": {
                "file": reg_file.name,
                "path": str(reg_file),
                "sha256": reg_hash,
                "size_bytes": reg_file.stat().st_size,
                "provenance": "Google Fonts official repository (google/fonts)"
            },
            "bold": {
                "file": bold_file.name,
                "path": str(bold_file),
                "sha256": bold_hash,
                "size_bytes": bold_file.stat().st_size,
                "provenance": "Google Fonts official repository (google/fonts)"
            }
        }
        return True, "FONTS_VERIFIED", font_info

    def load_manifest(self) -> Dict[str, Any]:
        """Loads and parses the baselines_manifest.json."""
        if not self.manifest_path.exists():
            return {"baselines": []}
        try:
            return json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except Exception as e:
            raise ValueError(f"Failed to parse baselines manifest: {e}")

    def get_baseline_config(self, baseline_id: str) -> Optional[BaselineConfig]:
        """Retrieves BaselineConfig for a given baseline ID from manifest."""
        manifest = self.load_manifest()
        for b in manifest.get("baselines", []):
            if b.get("baseline_id") == baseline_id:
                viewport = b.get("viewport", {})
                return BaselineConfig(
                    baseline_id=b["baseline_id"],
                    route=b["route"],
                    screen=b.get("screen", "unknown"),
                    width=viewport.get("width", 1440),
                    height=viewport.get("height", 900),
                    theme=b.get("theme", "light"),
                    direction=b.get("direction", "rtl"),
                    density=b.get("density", "comfortable"),
                    file_name=b["file_name"],
                    file_sha256=b.get("file_sha256"),
                    description=b.get("description", "")
                )
        return None

    def get_baseline_image(self, baseline_id: str) -> bytes:
        """
        Reads golden baseline PNG bytes from disk in read-only mode.
        Asserts that the file exists and passes cryptographic SHA-256 check.
        """
        cfg = self.get_baseline_config(baseline_id)
        if not cfg:
            raise FileNotFoundError(f"Baseline {baseline_id} not registered in manifest.")

        baseline_file = self.baselines_dir / cfg.file_name
        if not baseline_file.exists():
            raise FileNotFoundError(f"Baseline image file missing on disk: {baseline_file}")

        data = baseline_file.read_bytes()
        actual_hash = self.compute_sha256(data)

        if cfg.file_sha256 and actual_hash != cfg.file_sha256.lower():
            raise BaselineIntegrityError(
                f"Cryptographic SHA-256 mismatch for baseline {baseline_id}: "
                f"expected {cfg.file_sha256}, actual {actual_hash}"
            )

        return data

    def save_baseline_image(
        self,
        baseline_id: str,
        png_bytes: bytes,
        allow_write: bool = False
    ) -> str:
        """
        Saves a baseline PNG to disk and updates manifest.
        Strictly requires allow_write=True to prevent inadvertent overwrite during testing.
        """
        if not allow_write:
            raise PermissionError("Baseline writing is prohibited during automated test execution.")

        cfg = self.get_baseline_config(baseline_id)
        if not cfg:
            raise ValueError(f"Baseline {baseline_id} not registered in manifest.")

        baseline_file = self.baselines_dir / cfg.file_name
        self.baselines_dir.mkdir(parents=True, exist_ok=True)
        baseline_file.write_bytes(png_bytes)

        file_hash = self.compute_sha256(png_bytes)

        # Update manifest
        manifest = self.load_manifest()
        for b in manifest.get("baselines", []):
            if b.get("baseline_id") == baseline_id:
                b["file_sha256"] = file_hash
                b["file_size_bytes"] = len(png_bytes)
                break

        self.manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return file_hash
