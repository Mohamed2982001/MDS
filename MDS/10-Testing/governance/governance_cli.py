"""Command-Line Interface (CLI) for MDS Governance & Consistency Engine.

Usage:
    python MDS/10-Testing/governance/governance_cli.py [--strict] [--json] [--output PATH] [--fast] [--benchmark]
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Add testing directory to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
TESTING_DIR = SCRIPT_DIR.parent
REPO_ROOT = TESTING_DIR.parent.parent

if str(TESTING_DIR) not in sys.path:
    sys.path.insert(0, str(TESTING_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from governance.engine import GovernanceEngine
from governance.reporters import ConsoleReporter, JsonReporter


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Master Design System (MDS) — Layer M Governance & Cross-Document Consistency Engine"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Strict mode: Fails build on BLOCKER, CRITICAL, or MAJOR findings.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Outputs machine-readable JSON to stdout.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to write the machine-readable JSON report file.",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Fast mode: Skips deep link integrity verification for pre-commit hooks (< 150ms).",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        default=False,
        help="Full mode: Executes comprehensive cross-document audit including deep link validation (default mode).",
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Runs 5 consecutive audit iterations and calculates averaged performance benchmark metrics.",
    )
    parser.add_argument(
        "--root",
        type=str,
        default=str(REPO_ROOT),
        help="Workspace root directory (defaults to repository root).",
    )

    args = parser.parse_args()
    workspace_root = Path(args.root).resolve()

    if args.benchmark:
        times = []
        last_res = None
        for i in range(5):
            eng = GovernanceEngine(workspace_root=workspace_root)
            t0 = time.perf_counter()
            last_res = eng.audit_all(strict_mode=args.strict, fast_mode=args.fast)
            times.append((time.perf_counter() - t0) * 1000.0)

        avg_ms = sum(times) / len(times)
        min_ms = min(times)
        max_ms = max(times)
        print("=" * 80)
        print("        MDS GOVERNANCE PERFORMANCE BENCHMARK REPORT (5 RUNS)")
        print("=" * 80)
        print(f"  Warm Target Benchmark : <= 500.0 ms (ADVISORY)")
        print(f"  Averaged Duration     : {avg_ms:.1f} ms")
        print(f"  Fastest Iteration     : {min_ms:.1f} ms")
        print(f"  Slowest Iteration     : {max_ms:.1f} ms")
        print(f"  Benchmark Status      : {'PASS' if avg_ms <= 500.0 else 'ADVISORY_EXCEEDED'}")
        print("=" * 80)
        res = last_res
    else:
        engine = GovernanceEngine(workspace_root=workspace_root)
        res = engine.audit_all(strict_mode=args.strict, fast_mode=args.fast)

    if args.output:
        JsonReporter.write_to_file(res, Path(args.output))

    if args.json:
        import json
        print(json.dumps(JsonReporter.serialize(res), indent=2, ensure_ascii=False))
    else:
        print(ConsoleReporter.render(res))

    return res.exit_code


if __name__ == "__main__":
    sys.exit(main())
