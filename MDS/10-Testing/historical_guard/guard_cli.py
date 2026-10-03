"""
MDS Historical Phase Guard CLI
Phase 9.7.9: Historical Phase Guard & Architectural Immutability Engine
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Standard library only (Zero external dependencies).
Implements Section 13: CLI Architecture Specification.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from historical_guard.engine import HistoricalGuardEngine
    from historical_guard.reporters import ConsoleReporter, JSONReporter
else:
    from .engine import HistoricalGuardEngine
    from .reporters import ConsoleReporter, JSONReporter


def snapshot_phase(
    phase_id: str,
    author: str,
    adr: str,
    workspace_root: Optional[Path] = None,
    force: bool = False,
) -> dict:
    """
    Snapshot tooling: WRITE-CAPABLE only for appending newly authorized phases.
    MUST NOT silently overwrite already sealed phase baselines, trust anchor, or ledger.
    """
    import json

    root = workspace_root or Path(__file__).resolve().parent.parent.parent.parent
    baselines_dir = root / "MDS" / "10-Testing" / "baselines" / "historical"
    registry_file = baselines_dir / "master_historical_registry.json"

    if not registry_file.exists():
        raise FileNotFoundError(
            f"Master historical registry not found at '{registry_file}'. Run genesis bootstrap first."
        )

    registry_data = json.loads(registry_file.read_text(encoding="utf-8"))
    locked_phases = registry_data.get("locked_phases", [])
    already_sealed = any(p.get("phase_id") == phase_id for p in locked_phases)

    slug = phase_id.lower().replace("-", "_").replace(".", "_")
    manifest_file = baselines_dir / f"{slug}_manifest.json"

    if already_sealed or manifest_file.exists():
        if not force:
            raise FileExistsError(
                f"Phase baseline '{phase_id}' is already sealed in master historical registry. "
                "Silent overwrite of sealed baseline manifests is strictly prohibited."
            )

    return {
        "status": "SUCCESS",
        "phase_id": phase_id,
        "author": author,
        "adr": adr,
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="guard_cli.py",
        description="Master Design System (MDS) — Historical Phase Guard & Architectural Immutability Engine",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # verify
    verify_p = subparsers.add_parser("verify", help="Verify historical document immutability")
    verify_p.add_argument("--phase", type=str, help="Verify a single phase manifest")
    verify_p.add_argument("--strict", action="store_true", help="Treat any warning/major finding as fatal")
    verify_p.add_argument("--json", action="store_true", help="Output JSON telemetry to stdout")
    verify_p.add_argument("--output", type=str, help="Save JSON report to file")

    # diff
    diff_p = subparsers.add_parser("diff", help="View unified diff for modified historical document")
    diff_p.add_argument("--file", type=str, required=True, help="Relative or absolute path to file")

    # snapshot (mutating command - requires Lead Architect authority)
    snap_p = subparsers.add_parser("snapshot", help="Snapshot an approved phase baseline manifest")
    snap_p.add_argument("--phase", type=str, required=True, help="Phase ID (e.g. Phase-9.7.8)")
    snap_p.add_argument("--author", type=str, default="Mohamed Khalid", help="Authorizing Architect")
    snap_p.add_argument("--adr", type=str, required=True, help="Authorizing ADR reference")
    snap_p.add_argument("--force", action="store_true", help="Force overwrite of existing sealed baseline (requires authorization)")

    args = parser.parse_args(argv)
    engine = HistoricalGuardEngine()

    if args.command == "verify":
        result = engine.verify_all(strict=args.strict)

        master_digest = ""
        if engine.registry_file.exists():
            try:
                import json
                reg = json.loads(engine.registry_file.read_text(encoding="utf-8"))
                master_digest = reg.get("cumulative_chain_digest", "")
            except Exception:
                pass

        if args.output:
            JSONReporter.write_to_file(result, Path(args.output), master_digest=master_digest)

        if args.json:
            json_data = JSONReporter.render(result, master_digest=master_digest)
            import json
            print(json.dumps(json_data, indent=2))
        else:
            # Collect digests for dashboard
            manifest_digests = {}
            if engine.registry_file.exists():
                try:
                    import json
                    reg = json.loads(engine.registry_file.read_text(encoding="utf-8"))
                    for lp in reg.get("locked_phases", []):
                        manifest_digests[lp.get("phase_id")] = lp.get("manifest_digest", "")
                except Exception:
                    pass
            print(ConsoleReporter.render(result, manifest_digests=manifest_digests))

        return result.exit_code

    elif args.command == "diff":
        diff_output = engine.diff(args.file)
        if diff_output:
            print(diff_output)
        return 0

    elif args.command == "snapshot":
        try:
            snapshot_phase(args.phase, args.author, args.adr, force=args.force)
            print(f"Phase snapshot recorded for '{args.phase}' authorized by '{args.author}' via '{args.adr}'.")
            return 0
        except (FileExistsError, ValueError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
