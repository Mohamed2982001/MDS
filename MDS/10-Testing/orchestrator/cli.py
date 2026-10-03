"""
Master Design System (MDS) — Orchestrator CLI & Policy Precedence Resolver
Phase 9.7.10: Unified Local Orchestrator CLI & Master Validation Pipeline
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

from .models import PipelineResult
from .engine import OrchestratorEngine
from .reporters import ConsoleReporter, JsonReporter
from .registry import resolve_subsystem_id


class CLIConfigurationError(ValueError):
    """Raised when conflicting CLI flags or arguments are supplied."""
    pass


@dataclass
class ResolvedPolicy:
    profile: str
    target_subsystem: Optional[str]
    strict: bool
    strict_env: bool
    fail_fast: bool
    isolate: bool
    quiet: bool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run_all.py",
        description="Master Design System (MDS) — Unified Local Orchestrator CLI",
    )

    # Layer 1: Base Execution Profile
    profile_group = parser.add_argument_group("Execution Profile")
    profile_group.add_argument(
        "--fast", action="store_true", help="Fast profile: Stages 0, 1, 2 only (< 2s)"
    )
    profile_group.add_argument(
        "--core", action="store_true", help="Core profile (Default): Stages 0, 1, 2, 3"
    )
    profile_group.add_argument(
        "--full", action="store_true", help="Full profile: All Stages 0-4 including browser live tests"
    )
    profile_group.add_argument(
        "--ci", action="store_true", help="CI preset: --full + --isolate + --fail-fast + --strict"
    )

    # Layer 2: Target Selection
    target_group = parser.add_argument_group("Target Selection")
    target_group.add_argument(
        "--subsystem",
        type=str,
        default=None,
        help="Target a specific subsystem by ID or alias (runs target execution closure)",
    )

    # Layer 3: Strictness & Environment Policy
    strict_group = parser.add_argument_group("Strictness & Environment Policy")
    strict_group.add_argument(
        "--strict", action="store_true", help="Strict mode: Treat WARN/ADVISORY findings as fatal (Exit 1)"
    )
    strict_group.add_argument(
        "--strict-environment",
        action="store_true",
        help="Strict environment: Missing headless Chrome escalates DEFERRED to fatal failure (Exit 1)",
    )

    # Layer 4: Failure Policy
    fail_group = parser.add_argument_group("Failure Policy")
    fail_group.add_argument(
        "--fail-fast", action="store_true", help="Fail fast: Abort execution immediately on first CRITICAL/BLOCKER"
    )

    # Layer 5: Isolation Policy
    isolate_group = parser.add_argument_group("Isolation Policy")
    isolate_group.add_argument(
        "--isolate", action="store_true", help="Subprocess isolation: Execute dynamic stages in child workers via IPC"
    )

    # Reporting options
    report_group = parser.add_argument_group("Reporting Options")
    report_group.add_argument(
        "--quiet", action="store_true", help="Suppress console dashboard output"
    )

    return parser


create_parser = build_parser


def resolve_execution_policy(args: argparse.Namespace) -> ResolvedPolicy:
    profile_flags = {
        "fast": getattr(args, "fast", False),
        "core": getattr(args, "core", False),
        "full": getattr(args, "full", False),
        "ci": getattr(args, "ci", False),
    }
    active_profile_count = sum(1 for v in profile_flags.values() if v)
    if active_profile_count > 1:
        raise CLIConfigurationError(
            "Conflicting execution profiles specified. "
            "Please specify only one of --fast, --core, --full, or --ci."
        )

    if getattr(args, "ci", False):
        profile = "full"
        isolate = True
        fail_fast = True
        strict = True
        strict_env = True
    elif getattr(args, "fast", False):
        profile = "fast"
        isolate = getattr(args, "isolate", False)
        fail_fast = getattr(args, "fail_fast", False)
        strict = getattr(args, "strict", False)
        strict_env = getattr(args, "strict_environment", False)
    elif getattr(args, "full", False):
        profile = "full"
        isolate = getattr(args, "isolate", False)
        fail_fast = getattr(args, "fail_fast", False)
        strict = getattr(args, "strict", False)
        strict_env = getattr(args, "strict_environment", False)
    elif getattr(args, "core", False):
        profile = "core"
        isolate = getattr(args, "isolate", False)
        fail_fast = getattr(args, "fail_fast", False)
        strict = getattr(args, "strict", False)
        strict_env = getattr(args, "strict_environment", False)
    else:
        profile = "core"
        isolate = getattr(args, "isolate", False)
        fail_fast = getattr(args, "fail_fast", False)
        strict = getattr(args, "strict", False)
        strict_env = getattr(args, "strict_environment", False)

    target = getattr(args, "subsystem", None)
    quiet = getattr(args, "quiet", False)

    return ResolvedPolicy(
        profile=profile,
        target_subsystem=target,
        strict=strict,
        strict_env=strict_env,
        fail_fast=fail_fast,
        isolate=isolate,
        quiet=quiet,
    )


def main(argv: Optional[List[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        policy = resolve_execution_policy(args)
    except CLIConfigurationError as e:
        sys.stderr.write(f"Error: {e}\n")
        return 2

    # Target Subsystem resolution
    target_subsystem: Optional[str] = None
    if policy.target_subsystem:
        resolved = resolve_subsystem_id(policy.target_subsystem)
        if not resolved:
            sys.stderr.write(f"Error: Unknown subsystem ID or alias '{policy.target_subsystem}'\n")
            return 2
        target_subsystem = resolved

    # Execute Orchestrator Engine
    engine = OrchestratorEngine()
    result = engine.run_pipeline(
        profile=policy.profile,
        subsystem=target_subsystem,
        strict=policy.strict,
        strict_env=policy.strict_env,
        fail_fast=policy.fail_fast,
        isolate=policy.isolate,
    )

    # Render Reports
    if not args.quiet:
        console_reporter = ConsoleReporter()
        console_reporter.render(result)

    json_reporter = JsonReporter()
    json_reporter.export(result)

    return result.exit_code


if __name__ == "__main__":
    sys.exit(main())
