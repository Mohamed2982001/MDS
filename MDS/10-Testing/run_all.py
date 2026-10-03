#!/usr/bin/env python3
"""
Master Design System (MDS) — Unified Local Orchestrator CLI Entrypoint
Phase 9.7.10: Unified Local Orchestrator CLI & Master Validation Pipeline
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Single deterministic entrypoint for the complete MDS validation estate:
    python MDS/10-Testing/run_all.py --core
    python MDS/10-Testing/run_all.py --full
    python MDS/10-Testing/run_all.py --fast
    python MDS/10-Testing/run_all.py --ci
    python MDS/10-Testing/run_all.py --subsystem historical
"""

import sys
from pathlib import Path

# Ensure orchestrator package is importable
TESTING_DIR = Path(__file__).resolve().parent
if str(TESTING_DIR) not in sys.path:
    sys.path.insert(0, str(TESTING_DIR))

from orchestrator.cli import main

if __name__ == "__main__":
    sys.exit(main())
