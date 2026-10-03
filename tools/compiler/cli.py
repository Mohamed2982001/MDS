"""
Master Design System (MDS) — Standalone Compiler & Verification CLI
Phase 10.3: Production Artifact Compilation & Zero-NPM Distribution
Layer 13: Implementation, Tooling & Operationalization
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Optional

try:
    from .engine import CompilerEngine
    from .models import (
        CompilerError,
        ConfigurationError,
        ContractViolationError,
        IntegrityViolationError,
        SourceValidationError,
    )
    from .packager import DeterministicPackager
    from .validator import DistributionValidator
except (ImportError, ValueError):
    # Allow running as standalone script: python tools/compiler/cli.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
    from tools.compiler.engine import CompilerEngine
    from tools.compiler.models import (
        CompilerError,
        ConfigurationError,
        ContractViolationError,
        IntegrityViolationError,
        SourceValidationError,
    )
    from tools.compiler.packager import DeterministicPackager
    from tools.compiler.validator import DistributionValidator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mds-compiler",
        description="Master Design System (MDS) Production Compiler & Verification CLI",
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # Subcommand: compile
    compile_p = subparsers.add_parser("compile", help="Execute 6-stage production compilation pipeline")
    compile_p.add_argument("--out", type=Path, default=Path("dist"), help="Output distribution directory (default: dist)")
    compile_p.add_argument("--epoch", type=int, default=None, help="Explicit build epoch timestamp (SOURCE_DATE_EPOCH)")
    compile_p.add_argument("--dev", action="store_true", help="Development/convenience mode (non-reproducible)")
    compile_p.add_argument("--workspace", type=Path, default=None, help="Workspace root directory")
    compile_p.add_argument("--json", action="store_true", help="Output execution summary in JSON format")

    # Subcommand: verify (Strictly READ-ONLY)
    verify_p = subparsers.add_parser("verify", help="Strictly read-only distribution verification gate")
    verify_p.add_argument("--dist", type=Path, default=Path("dist"), help="Path to distribution directory to verify")
    verify_p.add_argument("--allow-non-reproducible", action="store_true", help="Allow convenience mode builds")
    verify_p.add_argument("--json", action="store_true", help="Output verification report in JSON format")

    # Subcommand: pack
    pack_p = subparsers.add_parser("pack", help="Assemble deterministic zip and tar.gz archives from dist")
    pack_p.add_argument("--dist", type=Path, default=Path("dist"), help="Distribution directory containing compiled assets")
    pack_p.add_argument("--epoch", type=int, default=None, help="Build epoch timestamp")
    pack_p.add_argument("--json", action="store_true", help="Output packing summary in JSON format")

    return parser


def handle_compile(args: argparse.Namespace) -> int:
    workspace_root = args.workspace or Path.cwd()
    engine = CompilerEngine(workspace_root=workspace_root)
    reproducible = not args.dev

    try:
        res = engine.compile(
            output_dir=args.out,
            reproducible_mode=reproducible,
            build_epoch=args.epoch,
        )
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("================================================================================")
            print("  MDS PRODUCTION COMPILATION — SUCCESS (Exit 0)")
            print("================================================================================")
            print(f"  Output Directory:  {res.get('output_dir')}")
            print(f"  Build Identity:    {res.get('build_id')}")
            print(f"  Total Artifacts:   {res.get('total_artifacts')}")
            print(f"  Total Byte Size:   {res.get('total_bytes'):,} bytes")
            print(f"  Reproducible:      {res.get('reproducible')}")
            print(f"  Build Epoch:       {res.get('build_epoch')}")
            print("================================================================================")
        return 0

    except SourceValidationError as e:
        sys.stderr.write(f"[ERROR: SOURCE_VALIDATION_FAILURE] {e.message}\n")
        return 2
    except ContractViolationError as e:
        sys.stderr.write(f"[ERROR: CONTRACT_VIOLATION] {e.message}\n")
        return 2
    except IntegrityViolationError as e:
        sys.stderr.write(f"[ERROR: INTEGRITY_VIOLATION] {e.message}\n")
        return 3
    except ConfigurationError as e:
        sys.stderr.write(f"[ERROR: CONFIGURATION_ERROR] {e.message}\n")
        return 4
    except Exception as e:
        sys.stderr.write(f"[ERROR: FATAL_SYSTEM_ERROR] {e}\n")
        return 4


def handle_verify(args: argparse.Namespace) -> int:
    dist_dir = args.dist.resolve()
    validator = DistributionValidator(dist_dir)
    require_reproducible = not args.allow_non_reproducible
    result = validator.verify(require_reproducible=require_reproducible)

    if args.json:
        payload = {
            "status": result.status,
            "exit_code": result.exit_code,
            "message": result.message,
            "details": result.details,
        }
        print(json.dumps(payload, indent=2))
    else:
        print("================================================================================")
        print(f"  MDS DISTRIBUTION VERIFICATION GATE — {result.status} (Exit {result.exit_code})")
        print("================================================================================")
        print(f"  Target Package:    {dist_dir}")
        print(f"  Status:            {result.status}")
        print(f"  Verdict:           {result.message}")
        if result.details:
            print(f"  Verified Files:    {result.details.get('verified_artifacts', 0)}")
            print(f"  Total Size:        {result.details.get('total_bytes', 0):,} bytes")
            print(f"  Build ID:          {result.details.get('build_id', 'N/A')}")
            print(f"  Reproducible:      {result.details.get('reproducible', False)}")
        print("================================================================================")

    return result.exit_code


def handle_pack(args: argparse.Namespace) -> int:
    dist_dir = args.dist.resolve()
    if not dist_dir.exists():
        sys.stderr.write(f"[ERROR: CONFIGURATION_ERROR] Distribution directory does not exist: {dist_dir}\n")
        return 4

    epoch = args.epoch
    if epoch is None:
        env_epoch = os.environ.get("SOURCE_DATE_EPOCH")
        if env_epoch:
            try:
                epoch = int(env_epoch)
            except ValueError:
                pass
    if epoch is None:
        epoch = 1790812800

    packager = DeterministicPackager(build_epoch=epoch)
    files_payload = {}
    for p in dist_dir.rglob("*"):
        if p.is_file() and not p.name.endswith(".zip") and not p.name.endswith(".tar.gz"):
            rel_posix = p.relative_to(dist_dir).as_posix()
            files_payload[rel_posix] = p.read_bytes()

    zip_bytes, tar_bytes = packager.package_distribution(files_payload)
    archives_dir = dist_dir / "archives"
    archives_dir.mkdir(parents=True, exist_ok=True)

    (archives_dir / "mds-v1.0.0-dist.zip").write_bytes(zip_bytes)
    (archives_dir / "mds-v1.0.0-dist.tar.gz").write_bytes(tar_bytes)

    if args.json:
        print(json.dumps({
            "status": "SUCCESS",
            "exit_code": 0,
            "archives": [
                "archives/mds-v1.0.0-dist.zip",
                "archives/mds-v1.0.0-dist.tar.gz",
            ],
            "epoch": epoch,
        }, indent=2))
    else:
        print("================================================================================")
        print("  MDS DETERMINISTIC PACKAGER — SUCCESS (Exit 0)")
        print("================================================================================")
        print(f"  ZIP Archive:       {archives_dir / 'mds-v1.0.0-dist.zip'}")
        print(f"  TAR.GZ Archive:    {archives_dir / 'mds-v1.0.0-dist.tar.gz'}")
        print(f"  Build Epoch:       {epoch}")
        print("================================================================================")

    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.subcommand == "compile":
        return handle_compile(args)
    elif args.subcommand == "verify":
        return handle_verify(args)
    elif args.subcommand == "pack":
        return handle_pack(args)
    else:
        parser.print_help()
        return 4


if __name__ == "__main__":
    sys.exit(main())
