#!/usr/bin/env python3
"""
MDS Browser Discovery Engine
Phase 9.7.4: Browser Automation Runner Bridge
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Automatically detects available Chromium-compatible browser binaries across Windows,
Linux, and macOS host environments without requiring external package dependencies.
"""

import os
import re
import sys
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional, Dict

from .models import BrowserInfo, BrowserType


class BrowserDiscovery:
    """
    Scans the host system for installed Chromium-based browsers:
    - Google Chrome
    - Microsoft Edge
    - Generic Chromium
    """

    @staticmethod
    def _get_candidate_paths() -> Dict[BrowserType, List[Path]]:
        candidates: Dict[BrowserType, List[Path]] = {
            BrowserType.CHROME: [],
            BrowserType.EDGE: [],
            BrowserType.CHROMIUM: [],
        }

        if sys.platform.startswith("win"):
            pf = os.environ.get("ProgramFiles", r"C:\Program Files")
            pf_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
            local_appdata = os.environ.get("LocalAppData", "")

            # Google Chrome on Windows
            candidates[BrowserType.CHROME].extend([
                Path(pf) / "Google" / "Chrome" / "Application" / "chrome.exe",
                Path(pf_x86) / "Google" / "Chrome" / "Application" / "chrome.exe",
            ])
            if local_appdata:
                candidates[BrowserType.CHROME].append(
                    Path(local_appdata) / "Google" / "Chrome" / "Application" / "chrome.exe"
                )

            # Microsoft Edge on Windows
            candidates[BrowserType.EDGE].extend([
                Path(pf_x86) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
                Path(pf) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
            ])
            if local_appdata:
                candidates[BrowserType.EDGE].append(
                    Path(local_appdata) / "Microsoft" / "Edge" / "Application" / "msedge.exe"
                )

        elif sys.platform.startswith("darwin"):
            # macOS
            candidates[BrowserType.CHROME].append(
                Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
            )
            candidates[BrowserType.EDGE].append(
                Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge")
            )
            candidates[BrowserType.CHROMIUM].append(
                Path("/Applications/Chromium.app/Contents/MacOS/Chromium")
            )

        else:
            # Linux and Unix
            for name in ["google-chrome", "google-chrome-stable"]:
                candidates[BrowserType.CHROME].append(Path(f"/usr/bin/{name}"))
            for name in ["microsoft-edge", "microsoft-edge-stable"]:
                candidates[BrowserType.EDGE].append(Path(f"/usr/bin/{name}"))
            for name in ["chromium", "chromium-browser"]:
                candidates[BrowserType.CHROMIUM].append(Path(f"/usr/bin/{name}"))
                candidates[BrowserType.CHROMIUM].append(Path(f"/snap/bin/{name}"))

        # Add any binaries located on the current system PATH
        for cmd, btype in [
            ("google-chrome", BrowserType.CHROME),
            ("chrome", BrowserType.CHROME),
            ("msedge", BrowserType.EDGE),
            ("microsoft-edge", BrowserType.EDGE),
            ("chromium", BrowserType.CHROMIUM),
            ("chromium-browser", BrowserType.CHROMIUM),
        ]:
            which_path = shutil.which(cmd)
            if which_path:
                candidates[btype].append(Path(which_path))

        return candidates

    @classmethod
    def get_version(cls, executable_path: Path) -> str:
        """Determines the version of the browser executable."""
        if not executable_path.exists():
            return "Unknown (Not Found)"

        # 1. On Windows, Chromium browsers place version-numbered directories alongside the binary
        if sys.platform.startswith("win"):
            try:
                parent = executable_path.parent
                versions = [
                    d.name for d in parent.iterdir()
                    if d.is_dir() and re.match(r"^\d+(\.\d+)+$", d.name)
                ]
                if versions:
                    # Sort version strings naturally
                    def vkey(v):
                        return [int(x) for x in v.split(".") if x.isdigit()]
                    latest = sorted(versions, key=vkey)[-1]
                    prefix = "Chrome" if "chrome" in executable_path.stem.lower() else "Edge"
                    return f"{prefix} {latest}"
            except Exception:
                pass

        # 2. Run --version subprocess for Linux/macOS or fallback
        try:
            res = subprocess.run(
                [str(executable_path), "--version"],
                capture_output=True,
                text=True,
                timeout=2.0,
                check=False
            )
            output = (res.stdout or res.stderr or "").strip()
            if output:
                first_line = output.splitlines()[0].strip()
                if not first_line.startswith("["):  # Avoid logging prefix lines
                    return first_line
        except Exception:
            pass

        return "Unknown"

    @classmethod
    def find_all(cls) -> List[BrowserInfo]:
        """Discovers all verified, executable browser binaries on host."""
        candidates = cls._get_candidate_paths()
        discovered: List[BrowserInfo] = []
        seen_paths = set()

        for btype, path_list in candidates.items():
            for p in path_list:
                try:
                    resolved = p.resolve()
                except Exception:
                    resolved = p

                if resolved in seen_paths:
                    continue

                if resolved.exists() and os.access(resolved, os.X_OK):
                    seen_paths.add(resolved)
                    version_str = cls.get_version(resolved)
                    name = resolved.stem.capitalize()
                    if btype == BrowserType.CHROME:
                        name = "Google Chrome"
                    elif btype == BrowserType.EDGE:
                        name = "Microsoft Edge"
                    elif btype == BrowserType.CHROMIUM:
                        name = "Chromium"

                    discovered.append(
                        BrowserInfo(
                            name=name,
                            path=resolved,
                            version=version_str,
                            browser_type=btype,
                            is_available=True
                        )
                    )

        return discovered

    @classmethod
    def find_chrome(cls) -> Optional[BrowserInfo]:
        """Finds Google Chrome if installed."""
        for b in cls.find_all():
            if b.browser_type == BrowserType.CHROME:
                return b
        return None

    @classmethod
    def find_edge(cls) -> Optional[BrowserInfo]:
        """Finds Microsoft Edge if installed."""
        for b in cls.find_all():
            if b.browser_type == BrowserType.EDGE:
                return b
        return None

    @classmethod
    def get_preferred(cls, prefer: Optional[str] = None) -> Optional[BrowserInfo]:
        """
        Returns the preferred browser binary.
        Default precedence: Chrome -> Edge -> Chromium.
        If prefer='edge', tries Edge first.
        """
        browsers = cls.find_all()
        if not browsers:
            return None

        if prefer:
            prefer_norm = prefer.lower().strip()
            for b in browsers:
                if prefer_norm in b.name.lower() or prefer_norm == b.browser_type.value:
                    return b

        # Default precedence
        for b in browsers:
            if b.browser_type == BrowserType.CHROME:
                return b
        for b in browsers:
            if b.browser_type == BrowserType.EDGE:
                return b
        for b in browsers:
            if b.browser_type == BrowserType.CHROMIUM:
                return b

        return browsers[0]
