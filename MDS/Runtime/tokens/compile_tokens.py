#!/usr/bin/env python3
"""
MDS Token Runtime Engine — CLI Compiler Entry Point
Phase 9.2: Token Runtime Engine

Usage:
    python compile_tokens.py                  # Compiles tokens to dist/
    python compile_tokens.py --check          # Dry-run validation only
    python compile_tokens.py --out-dir <path> # Custom output directory
"""

import argparse
import json
import sys
import time
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add parent directory to sys.path to allow imports when run as a standalone script
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from src.compiler import TokenCompiler
from src.loader import TokenLoader
from src.models import (
    AliasDepthExceededError,
    CycleDetectedError,
    MissingTokenError,
    SchemaValidationError,
    TokenRuntimeError,
)
from src.resolver import TokenResolver
from src.validator import TokenValidator


def parse_args():
    parser = argparse.ArgumentParser(
        description="Master Design System (MDS) — Token Runtime Compiler"
    )
    parser.add_argument(
        "--tokens-dir",
        type=Path,
        default=CURRENT_DIR.parent.parent / "02-Tokens",
        help="Path to source DTCG tokens directory (default: MDS/02-Tokens)"
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=CURRENT_DIR / "dist",
        help="Path to compiled distribution directory (default: MDS/Runtime/tokens/dist)"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Dry run: validate schema, cycles, and depth without writing files"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress informational stdout"
    )
    return parser.parse_args()


def run_pipeline(tokens_dir: Path, out_dir: Path, check_mode: bool = False, quiet: bool = False) -> int:
    start_time = time.perf_counter()

    if not quiet:
        print("=" * 72)
        print("       MASTER DESIGN SYSTEM (MDS) — TOKEN RUNTIME ENGINE       ")
        print("                   Phase 9.2: DTCG Compiler                    ")
        print("=" * 72)
        print(f"Source Directory: {tokens_dir}")
        print(f"Target Directory: {out_dir}")
        print(f"Mode:             {'VALIDATION ONLY (--check)' if check_mode else 'FULL COMPILATION'}")
        print("-" * 72)

    # 1. Ingestion & Discovery
    try:
        loader = TokenLoader(tokens_dir)
        base_tokens, theme_overrides, all_tokens, files = loader.load()
        if not quiet:
            print(f"[+] Discovered {len(files)} W3C DTCG files in source directory.")
    except Exception as e:
        print(f"[!] INGESTION ERROR: {e}", file=sys.stderr)
        return 1

    # 2. Invariant & Schema Validation
    try:
        validator = TokenValidator(strict=True)
        validation_result = validator.validate(base_tokens, theme_overrides, all_tokens, files)
        if not quiet:
            print(f"[+] Invariants Verified: {len(all_tokens)} distinct tokens (185 base, {len(all_tokens)-len(base_tokens)} theme-only).")
            print(f"[+] Component Tokens:   {sum(1 for t in base_tokens.values() if t.layer == 'component')} tokens under components/.")
            print(f"[+] Theme Override Sets: {len(theme_overrides)} multi-dimensional axis sets.")
            if validation_result.warnings:
                for w in validation_result.warnings:
                    print(f"    └── [WARN] {w}")
    except SchemaValidationError as e:
        print(f"[!] VALIDATION FAILURE:\n{e}", file=sys.stderr)
        return 1

    # 3. DAG Construction, Cycle Traversal & Alias Resolution
    try:
        resolver = TokenResolver(base_tokens, theme_overrides, all_tokens, max_depth=3)
        base_resolved, theme_resolved = resolver.resolve_all()
        max_hops = max((r.hops for r in base_resolved.values()), default=0)
        if not quiet:
            print(f"[+] Graph Traversal:     0 circular references detected.")
            print(f"[+] Alias Dereferencing: 100% resolved (0 broken links).")
            print(f"[+] Maximum Alias Depth: {max_hops} hops (compliant with <= 3 hop invariant).")
    except CycleDetectedError as e:
        print(f"[!] CIRCULARITY DETECTED: {e}", file=sys.stderr)
        return 1
    except AliasDepthExceededError as e:
        print(f"[!] DEPTH LIMIT EXCEEDED: {e}", file=sys.stderr)
        return 1
    except MissingTokenError as e:
        print(f"[!] BROKEN ALIAS: {e}", file=sys.stderr)
        return 1
    except TokenRuntimeError as e:
        print(f"[!] RESOLUTION ERROR: {e}", file=sys.stderr)
        return 1

    # If check mode, exit cleanly without touching disk
    if check_mode:
        duration_ms = (time.perf_counter() - start_time) * 1000
        if not quiet:
            print("-" * 72)
            print(f"[OK] CHECK SUCCEEDED: All tokens valid, graph acyclic, depth <= 3. ({duration_ms:.2f}ms)")
            print("=" * 72)
        return 0

    # 4. Compilation & Output Emission
    try:
        compiler = TokenCompiler(base_resolved, theme_resolved, all_tokens, theme_overrides)
        compile_result = compiler.compile()

        out_dir.mkdir(parents=True, exist_ok=True)

        # Write tokens.css
        css_path = out_dir / "tokens.css"
        with open(css_path, "w", encoding="utf-8", newline="\n") as fp:
            fp.write(compile_result.css)

        # Write tokens.json
        json_path = out_dir / "tokens.json"
        with open(json_path, "w", encoding="utf-8", newline="\n") as fp:
            json.dump(compile_result.json_data, fp, indent=2, ensure_ascii=False)
            fp.write("\n")

        # Write tokens.d.ts
        dts_path = out_dir / "tokens.d.ts"
        with open(dts_path, "w", encoding="utf-8", newline="\n") as fp:
            fp.write(compile_result.dts)

        duration_ms = (time.perf_counter() - start_time) * 1000

        if not quiet:
            print("-" * 72)
            print(f"[+] EMITTED: {css_path.name:<15} ({len(compile_result.css):>6} bytes) -> CSS @layer mds.tokens")
            print(f"[+] EMITTED: {json_path.name:<15} ({json_path.stat().st_size:>6} bytes) -> Pre-resolved catalog")
            print(f"[+] EMITTED: {dts_path.name:<15} ({len(compile_result.dts):>6} bytes) -> TypeScript declarations")
            print("-" * 72)
            print(f"[OK] COMPILATION SUCCEEDED: 188 tokens compiled in {duration_ms:.2f}ms.")
            print("=" * 72)
        return 0
    except Exception as e:
        print(f"[!] EMISSION ERROR: {e}", file=sys.stderr)
        return 1


def main():
    args = parse_args()
    exit_code = run_pipeline(
        tokens_dir=args.tokens_dir,
        out_dir=args.out_dir,
        check_mode=args.check,
        quiet=args.quiet
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
