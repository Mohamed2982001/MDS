#!/usr/bin/env python3
"""
MDS Design System Selection Engine (DSSE) — Command Line Interface
Usage:
    python tools/dsse/cli.py analyze --prompt "We are building a Flutter app..."
    python tools/dsse/cli.py evaluate --profile path/to/profile.json
    python tools/dsse/cli.py explain --report path/to/report.json
    python tools/dsse/cli.py validate --profile path/to/profile.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure repository root is on sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Safe UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from tools.dsse.analyzer import DSSEAnalyzer
from tools.dsse.catalog import load_candidate_catalog, get_default_catalog_path
from tools.dsse.engine import DSSEEngine
from tools.dsse.explainer import DSSEExplainer
from tools.dsse.validator import (
    validate_project_profile,
    validate_candidate_catalog,
    validate_decision_tuple,
    DSSEValidationError,
)

EXIT_SUCCESS = 0
EXIT_HUMAN_REVIEW_REQUIRED = 1
EXIT_VALIDATION_ERROR = 2
EXIT_INPUT_ERROR = 3
EXIT_INTERNAL_ERROR = 4


def cmd_analyze(args: argparse.Namespace) -> int:
    analyzer = DSSEAnalyzer()
    try:
        if args.input:
            in_path = Path(args.input)
            profile_data = analyzer.analyze_file(in_path)
        elif args.prompt:
            profile_data = analyzer.analyze_text(args.prompt, project_name=args.name or "Inferred Project")
        else:
            print("[ERROR] Either --input <file> or --prompt '<text>' must be specified for analyze.", file=sys.stderr)
            return EXIT_INPUT_ERROR

        # Validate generated profile
        is_valid, errors = validate_project_profile(profile_data)
        if not is_valid:
            print(f"[ERROR] Generated profile failed contract validation: {errors}", file=sys.stderr)
            return EXIT_VALIDATION_ERROR

        json_output = json.dumps(profile_data, indent=2, ensure_ascii=False)

        if args.output:
            out_path = Path(args.output).resolve()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json_output, encoding="utf-8")
            print(f"[SUCCESS] Project profile written to: {out_path}")
        else:
            print(json_output)

        return EXIT_SUCCESS

    except FileNotFoundError as fnf:
        print(f"[INPUT ERROR] {fnf}", file=sys.stderr)
        return EXIT_INPUT_ERROR
    except Exception as e:
        print(f"[INTERNAL ERROR] analyze failed: {e}", file=sys.stderr)
        return EXIT_INTERNAL_ERROR


def cmd_evaluate(args: argparse.Namespace) -> int:
    try:
        profile_path = Path(args.profile).resolve()
        if not profile_path.exists():
            print(f"[INPUT ERROR] Profile file not found: {profile_path}", file=sys.stderr)
            return EXIT_INPUT_ERROR

        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                profile_data = json.load(f)
        except json.JSONDecodeError as jde:
            print(f"[INPUT ERROR] Failed to parse profile JSON: {jde}", file=sys.stderr)
            return EXIT_INPUT_ERROR

        # Validate profile before evaluation
        is_valid, errors = validate_project_profile(profile_data)
        if not is_valid:
            print(f"[VALIDATION ERROR] Project profile invalid: {errors}", file=sys.stderr)
            return EXIT_VALIDATION_ERROR

        # Load candidate catalog
        cat_path = Path(args.catalog).resolve() if args.catalog else None
        try:
            catalog = load_candidate_catalog(cat_path)
        except DSSEValidationError as dse:
            print(f"[VALIDATION ERROR] Candidate catalog failed contract validation: {dse}", file=sys.stderr)
            return EXIT_VALIDATION_ERROR

        # Execute evaluation
        engine = DSSEEngine(catalog)
        output = engine.evaluate(profile_data)

        # Validate decision report output
        rep_valid, rep_errors = validate_decision_tuple(output.report)
        if not rep_valid:
            print(f"[INTERNAL ERROR] Engine produced invalid decision report schema: {rep_errors}", file=sys.stderr)
            return EXIT_INTERNAL_ERROR

        # Format output
        fmt = getattr(args, "format", "json") or "json"
        if fmt == "json":
            result_text = json.dumps(output.report, indent=2, ensure_ascii=False)
        elif fmt == "markdown":
            result_text = DSSEExplainer.to_markdown(output.report)
        else:
            result_text = DSSEExplainer.to_terminal_text(output.report)

        if args.output:
            out_path = Path(args.output).resolve()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(result_text, encoding="utf-8")
            if fmt == "json":
                # Print summary to terminal
                print(DSSEExplainer.to_terminal_text(output.report))
            print(f"\n[INFO] Decision report written to: {out_path}")
        else:
            print(result_text)

        # Return deterministic exit code: 0 if no review needed, 1 if review required
        return output.exit_code

    except FileNotFoundError as fnf:
        print(f"[INPUT ERROR] {fnf}", file=sys.stderr)
        return EXIT_INPUT_ERROR
    except Exception as e:
        print(f"[INTERNAL ERROR] evaluate failed: {e}", file=sys.stderr)
        return EXIT_INTERNAL_ERROR


def cmd_explain(args: argparse.Namespace) -> int:
    try:
        report_path = Path(args.report).resolve()
        if not report_path.exists():
            print(f"[INPUT ERROR] Report file not found: {report_path}", file=sys.stderr)
            return EXIT_INPUT_ERROR

        try:
            with open(report_path, "r", encoding="utf-8") as f:
                report_data = json.load(f)
        except json.JSONDecodeError as jde:
            print(f"[INPUT ERROR] Failed to parse report JSON: {jde}", file=sys.stderr)
            return EXIT_INPUT_ERROR

        is_valid, errors = validate_decision_tuple(report_data)
        if not is_valid:
            print(f"[VALIDATION ERROR] Report does not conform to decision report schema: {errors}", file=sys.stderr)
            return EXIT_VALIDATION_ERROR

        fmt = getattr(args, "format", "text") or "text"
        if fmt == "markdown":
            formatted = DSSEExplainer.to_markdown(report_data)
        else:
            formatted = DSSEExplainer.to_terminal_text(report_data)

        if args.output:
            out_path = Path(args.output).resolve()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(formatted, encoding="utf-8")
            print(f"[SUCCESS] Explanation written to: {out_path}")
        else:
            print(formatted)

        return EXIT_SUCCESS

    except Exception as e:
        print(f"[INTERNAL ERROR] explain failed: {e}", file=sys.stderr)
        return EXIT_INTERNAL_ERROR


def cmd_validate(args: argparse.Namespace) -> int:
    try:
        target_path_str = args.profile or args.catalog or args.report
        if not target_path_str:
            print("[ERROR] One of --profile, --catalog, or --report must be specified.", file=sys.stderr)
            return EXIT_INPUT_ERROR

        target_path = Path(target_path_str).resolve()
        if not target_path.exists():
            print(f"[INPUT ERROR] Target file not found: {target_path}", file=sys.stderr)
            return EXIT_INPUT_ERROR

        with open(target_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if args.profile:
            is_valid, errors = validate_project_profile(data)
            schema_type = "Project Profile"
        elif args.catalog:
            is_valid, errors = validate_candidate_catalog(data)
            schema_type = "Candidate Catalog"
        else:
            is_valid, errors = validate_decision_tuple(data)
            schema_type = "Decision Tuple Report"

        if is_valid:
            print(f"[VALIDATION PASS] {schema_type} ({target_path.name}) satisfies 100% of schema constraints.")
            return EXIT_SUCCESS
        else:
            print(f"[VALIDATION FAIL] {schema_type} ({target_path.name}) failed with {len(errors)} error(s):", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
            return EXIT_VALIDATION_ERROR

    except json.JSONDecodeError as jde:
        print(f"[INPUT ERROR] Malformed JSON syntax: {jde}", file=sys.stderr)
        return EXIT_INPUT_ERROR
    except Exception as e:
        print(f"[INTERNAL ERROR] validate failed: {e}", file=sys.stderr)
        return EXIT_INTERNAL_ERROR


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mds-dsse",
        description="Master Design System (MDS) -- Design System Selection Engine (DSSE) CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # analyze
    p_analyze = subparsers.add_parser("analyze", help="Analyze project requirements and generate ProjectProfile")
    p_analyze.add_argument("--input", "-i", help="Path to project requirements file or directory")
    p_analyze.add_argument("--prompt", "-p", help="Raw requirements prompt string")
    p_analyze.add_argument("--name", "-n", help="Project name (optional)")
    p_analyze.add_argument("--output", "-o", help="Output path for generated project_profile.json")

    # evaluate
    p_eval = subparsers.add_parser("evaluate", help="Evaluate candidates against project profile")
    p_eval.add_argument("--profile", "-p", required=True, help="Path to project_profile.json")
    p_eval.add_argument("--catalog", "-c", help="Path to candidate_catalog.json (defaults to built-in catalog)")
    p_eval.add_argument("--format", "-f", choices=["json", "text", "markdown"], default="json", help="Output format")
    p_eval.add_argument("--output", "-o", help="Output file path")

    # explain
    p_explain = subparsers.add_parser("explain", help="Generate detailed explanation and audit trail from report")
    p_explain.add_argument("--report", "-r", required=True, help="Path to decision report JSON")
    p_explain.add_argument("--format", "-f", choices=["text", "markdown"], default="text", help="Output format")
    p_explain.add_argument("--output", "-o", help="Output file path")

    # validate
    p_val = subparsers.add_parser("validate", help="Validate DSSE profile, catalog, or report against schema")
    p_val_group = p_val.add_mutually_exclusive_group(required=True)
    p_val_group.add_argument("--profile", help="Validate a project profile JSON file")
    p_val_group.add_argument("--catalog", help="Validate a candidate catalog JSON file")
    p_val_group.add_argument("--report", help="Validate a decision tuple report JSON file")

    return parser


def main() -> int:
    parser = build_parser()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return EXIT_SUCCESS

    args = parser.parse_args()
    if args.command == "analyze":
        return cmd_analyze(args)
    elif args.command == "evaluate":
        return cmd_evaluate(args)
    elif args.command == "explain":
        return cmd_explain(args)
    elif args.command == "validate":
        return cmd_validate(args)
    else:
        parser.print_help(sys.stderr)
        return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
