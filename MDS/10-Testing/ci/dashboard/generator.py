"""
Master Design System (MDS) -- Static Dashboard Generator & Bundler
Document Reference: MDS-SPEC-9711-REV5 / Section 12 (ADR-140)
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Dict


class DashboardGenerator:
    """
    Assembles the dual-mode static dashboard inside runs/{run_id}/dashboard/
    Modes supported:
      1. file:/// offline browsing (via manifest_data.js)
      2. http:// hosted browsing (via ci_artifact_manifest.json fetch)
    """

    TEMPLATE_DIR = Path(__file__).parent

    @classmethod
    def generate_dashboard(
        cls,
        manifest_dict: Dict[str, Any],
        output_dir: Path,
    ) -> Path:
        """
        Emits index.html, styles.css, app.js, manifest_data.js, and a copy of the manifest.
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        # 1. Copy shell files
        shutil.copy2(cls.TEMPLATE_DIR / "template.html", output_dir / "index.html")
        shutil.copy2(cls.TEMPLATE_DIR / "styles.css", output_dir / "styles.css")
        shutil.copy2(cls.TEMPLATE_DIR / "app.js", output_dir / "app.js")

        # 2. Emit manifest_data.js for offline file:// loading (Zero CORS)
        manifest_json_str = json.dumps(manifest_dict, indent=2, ensure_ascii=False)
        manifest_data_js = f"window.__MDS_MANIFEST__ = {manifest_json_str};\n"
        (output_dir / "manifest_data.js").write_text(manifest_data_js, encoding="utf-8")

        # 3. Emit ci_artifact_manifest.json inside dashboard folder for hosted HTTP fetch mode
        (output_dir / "ci_artifact_manifest.json").write_text(manifest_json_str, encoding="utf-8")

        return output_dir / "index.html"
