"""
Master Design System (MDS) -- latest.json Logical Pointer Manager
Document Reference: MDS-SPEC-9711-REV5 / Section 14 (ADR-148)
"""

from __future__ import annotations

import datetime
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger("mds.ci.pointer")


class LatestPointerManager:
    """
    Manages the mutable cross-platform latest.json logical pointer.
    Invariants (ADR-148):
      1. Plain JSON file, NOT an OS symlink.
      2. Non-circular: resides outside runs/{run_id} and not included in manifest hash.
      3. Non-gating failure semantics: failures log an advisory warning, never altering exit codes.
    """

    POINTER_FILENAME = "latest.json"

    @classmethod
    def write_pointer(
        cls,
        ci_artifacts_root: Path,
        run_id: str,
        manifest_relative_path: str,
        manifest_digest: str,
    ) -> Optional[Path]:
        """
        Creates or updates the latest.json logical pointer file.
        """
        pointer_data: Dict[str, Any] = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "schema_version": "1.0.0",
            "pointer_updated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "run_id": run_id,
            "manifest_relative_path": manifest_relative_path,
            "manifest_sha256": manifest_digest.lower(),
        }

        pointer_file = ci_artifacts_root / cls.POINTER_FILENAME

        try:
            ci_artifacts_root.mkdir(parents=True, exist_ok=True)
            with open(pointer_file, "w", encoding="utf-8") as f:
                json.dump(pointer_data, f, indent=2, ensure_ascii=False)
                f.write("\n")
            return pointer_file
        except Exception as e:
            logger.warning(
                f"[ADR-148 Non-Gating Advisory] Failed to write '{cls.POINTER_FILENAME}': {e}. "
                f"Execution exit code remains strictly preserved."
            )
            return None

    @classmethod
    def read_pointer(cls, ci_artifacts_root: Path) -> Optional[Dict[str, Any]]:
        """
        Reads and returns the current latest.json pointer data, or None if absent/invalid.
        """
        pointer_file = ci_artifacts_root / cls.POINTER_FILENAME
        if not pointer_file.exists():
            return None

        try:
            with open(pointer_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("schema_version") == "1.0.0" and "manifest_relative_path" in data:
                return data
            return None
        except Exception as e:
            logger.warning(f"Failed to read latest pointer '{pointer_file}': {e}")
            return None
