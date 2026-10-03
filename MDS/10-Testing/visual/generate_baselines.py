#!/usr/bin/env python3
"""
MDS Golden Visual Baseline Generator
Phase 9.7.7: Visual Regression Engine & Snapshot Diffing
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Administrative tool for capturing initial golden visual baselines from the
locked MDS Reference Application, calculating SHA-256 hashes, and updating
`baselines_manifest.json`.

Usage:
    python generate_baselines.py [--baseline-id VIS-BASE-001] [--all]
"""

import sys
import json
import argparse
from pathlib import Path

# Setup paths
SCRIPT_DIR = Path(__file__).resolve().parent
TESTING_DIR = SCRIPT_DIR.parent
WORKSPACE_ROOT = TESTING_DIR.parent.parent
if str(TESTING_DIR) not in sys.path:
    sys.path.insert(0, str(TESTING_DIR))

from browser.cdp_driver import CDPBrowserDriver
from browser.local_server import LocalTestServer
from browser.browser_discovery import BrowserDiscovery
from visual.baseline_manager import BaselineManager
from visual.visual_runner import VisualRunner


def generate_baselines(target_baseline_ids=None):
    mgr = BaselineManager(workspace_root=WORKSPACE_ROOT)
    runner = VisualRunner(workspace_root=WORKSPACE_ROOT)

    is_font_valid, font_msg, font_telemetry = mgr.verify_fonts()
    if not is_font_valid:
        print(f"[ERROR] Font verification failed: {font_msg}")
        sys.exit(1)

    preferred = BrowserDiscovery.get_preferred()
    if not preferred or not preferred.is_available:
        print("[ERROR] No Chromium browser available for baseline generation.")
        sys.exit(1)

    manifest = mgr.load_manifest()
    all_configs = {b["baseline_id"]: b for b in manifest.get("baselines", [])}
    ids_to_process = target_baseline_ids or mgr.CANONICAL_BASELINE_IDS

    print(f"Generating {len(ids_to_process)} golden visual baselines...")
    server = LocalTestServer(serve_dir=WORKSPACE_ROOT)
    server.start()

    try:
        with CDPBrowserDriver(browser_info=preferred) as driver:
            driver.launch(headless=True)

            for b_id in ids_to_process:
                if b_id not in all_configs:
                    print(f"  [-] Skipping unknown baseline: {b_id}")
                    continue

                cfg = mgr.get_baseline_config(b_id)
                print(f"  [+] Capturing {b_id} ({cfg.screen} {cfg.width}x{cfg.height} {cfg.theme} {cfg.direction})...", end="", flush=True)

                png_bytes = runner.capture_baseline_snapshot(driver, server, cfg)
                file_hash = mgr.save_baseline_image(b_id, png_bytes, allow_write=True)
                print(f" DONE! [{len(png_bytes)} bytes, SHA-256: {file_hash[:12]}...]")

    finally:
        server.stop()

    print("[SUCCESS] All targeted visual baselines generated and manifest locked.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate MDS Golden Visual Baselines")
    parser.add_argument("--baseline-id", type=str, help="Single baseline ID to generate (e.g. VIS-BASE-001)")
    parser.add_argument("--all", action="store_true", help="Generate all 12 canonical baselines")
    args = parser.parse_args()

    targets = [args.baseline_id] if args.baseline_id else None
    generate_baselines(targets)
