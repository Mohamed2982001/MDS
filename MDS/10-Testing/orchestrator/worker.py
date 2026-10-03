"""
Master Design System (MDS) — Subprocess Isolation Worker
Phase 9.7.10: Unified Local Orchestrator CLI & Master Validation Pipeline
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
import traceback
from pathlib import Path
from typing import Dict, Any, Optional

# Ensure UTF-8 stdout encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def run_worker_dispatch(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes the specified subsystem within this isolated child process.
    Captures raw stdout/stderr to artifacts/traces/<SUB_ID>.log.
    Returns clean serialized SubsystemResult dict.
    """
    from .models import ExecutionStatus, FindingSeverity, Finding, SubsystemResult
    from .registry import ORCHESTRATOR_SUBSYSTEM_REGISTRY

    subsystem_id = payload["subsystem_id"]
    workspace_root = Path(payload.get("workspace_root", os.getcwd())).resolve()
    strict = payload.get("strict", False)
    strict_env = payload.get("strict_env", False)

    if subsystem_id not in ORCHESTRATOR_SUBSYSTEM_REGISTRY:
        return SubsystemResult(
            subsystem_id=subsystem_id,
            subsystem_name=subsystem_id,
            status=ExecutionStatus.FAIL,
            findings=[
                Finding(
                    severity=FindingSeverity.BLOCKER,
                    target=subsystem_id,
                    code="ORCHESTRATOR_UNKNOWN_SUBSYSTEM",
                    message=f"Subsystem '{subsystem_id}' not found in registry",
                )
            ],
        ).to_dict()

    s_def = ORCHESTRATOR_SUBSYSTEM_REGISTRY[subsystem_id]

    # Trace log file setup
    trace_dir = workspace_root / "MDS" / "10-Testing" / "artifacts" / "traces"
    trace_dir.mkdir(parents=True, exist_ok=True)
    trace_file = trace_dir / f"{subsystem_id}.log"

    old_stdout = sys.stdout
    old_stderr = sys.stderr

    log_fp = open(trace_file, "w", encoding="utf-8")
    sys.stdout = log_fp
    sys.stderr = log_fp

    import time
    start_time = time.perf_counter()
    findings: list[Finding] = []
    status = ExecutionStatus.PASS
    metrics: dict[str, Any] = {}

    try:
        # Import engine dispatcher
        from .engine import OrchestratorEngine
        engine = OrchestratorEngine(workspace_root=workspace_root)
        result = engine.execute_subsystem_direct(s_def, strict=strict, strict_env=strict_env)
        return result.to_dict()

    except Exception as exc:
        duration_ms = (time.perf_counter() - start_time) * 1000
        tb_str = traceback.format_exc()
        log_fp.write(f"\n[EXCEPTION]\n{tb_str}\n")
        return SubsystemResult(
            subsystem_id=subsystem_id,
            subsystem_name=s_def.subsystem_name,
            status=ExecutionStatus.FAIL,
            duration_ms=duration_ms,
            findings=[
                Finding(
                    severity=FindingSeverity.BLOCKER,
                    target=subsystem_id,
                    code="SUBPROCESS_UNCAUGHT_EXCEPTION",
                    message=f"Subsystem crashed with unhandled exception: {exc}",
                )
            ],
        ).to_dict()

    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        log_fp.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="MDS Subprocess Isolation Worker")
    parser.add_argument("--subsystem", required=True, help="Subsystem ID to execute")
    args = parser.parse_args()

    # Read JSON payload from stdin
    try:
        line = sys.stdin.readline()
        if not line:
            payload = {"subsystem_id": args.subsystem}
        else:
            payload = json.loads(line.strip())
            payload["subsystem_id"] = args.subsystem
    except Exception as e:
        sys.stderr.write(f"Failed to read payload from stdin: {e}\n")
        return 2

    # Execute
    result_dict = run_worker_dispatch(payload)

    # Write serialized JSON result to stdout
    sys.stdout.write(json.dumps(result_dict) + "\n")
    sys.stdout.flush()

    status = result_dict.get("status")
    if status == "PASS" or status == "CACHED" or status == "DEFERRED" or status == "SKIPPED":
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
