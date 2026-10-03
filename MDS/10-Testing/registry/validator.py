#!/usr/bin/env python3
"""
MDS Capability Registry Validator
Enforces canonical schema, business logic, dependency DAG constraints,
and exact test accounting for the Master Design System.
"""

import sys
import os
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Any, Optional, Tuple

# Canonical Enumerations according to schema.json & Phase 9.7 Architecture
CANONICAL_LAYERS = {
    "A_REPOSITORY",
    "B_TOKENS",
    "C_CSS",
    "D_COMPONENTS",
    "E_PRIMITIVES",
    "F_PATTERNS_WORKFLOWS_TEMPLATES",
    "G_DSSE",
    "H_REFERENCE_APPLICATION",
    "I_BROWSER",
    "J_ACCESSIBILITY",
    "K_RESPONSIVE",
    "L_VISUAL",
    "M_GOVERNANCE",
    "N_PHASE_GUARD"
}

CANONICAL_CATEGORIES = {
    "STATIC",
    "UNIT",
    "INTEGRATION",
    "BROWSER",
    "ACCESSIBILITY",
    "RESPONSIVE",
    "VISUAL",
    "GOVERNANCE"
}

CANONICAL_STATUSES = {
    "ACTIVE",
    "QUARANTINED",
    "DEFERRED",
    "DISABLED"
}

CANONICAL_SEVERITIES = {
    "BLOCKER",
    "CRITICAL",
    "MAJOR",
    "MINOR",
    "WARNING",
    "INFO"
}

CANONICAL_EXECUTIONS = {
    "PYTHON_UNIT",
    "PYTHON_STATIC",
    "AST_PARSER",
    "BROWSER_AUTOMATION",
    "DOC_SCANNER",
    "COMPOSITE_HARNESS"
}

RUNNER_TYPES = {
    "standalone_test",
    "harness_capability",
    "composite_suite",
    "browser_test"
}

CAPABILITY_ID_REGEX = re.compile(r"^MDS-[A-Z0-9]+-[0-9]{3}$")

REQUIRED_CAPABILITY_FIELDS = [
    "id",
    "name",
    "layer",
    "category",
    "execution",
    "severity",
    "status",
    "owner",
    "runner"
]

class ValidationResult:
    def __init__(self):
        self.is_valid: bool = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.accounting: Dict[str, int] = {
            "total_capabilities": 0,
            "unique_defined_ids": 0,
            "active_executable_assertions": 0,
            "deferred_capabilities": 0,
            "quarantined_capabilities": 0,
            "disabled_capabilities": 0,
            "wrapped_assertions": 0
        }

    def add_error(self, message: str):
        self.is_valid = False
        self.errors.append(message)

    def add_warning(self, message: str):
        self.warnings.append(message)


class RegistryValidator:
    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(__file__).resolve().parent.parent.parent.parent

    def validate(self, registry_data: Dict[str, Any]) -> ValidationResult:
        result = ValidationResult()

        # 1. Structure and top-level keys
        for key in ["version", "schema_version", "metadata", "capabilities"]:
            if key not in registry_data:
                result.add_error(f"Missing required top-level key: '{key}'")
                return result

        if not isinstance(registry_data["capabilities"], list):
            result.add_error("'capabilities' must be a list")
            return result

        capabilities = registry_data["capabilities"]
        result.accounting["total_capabilities"] = len(capabilities)

        # 2. Capability ID Uniqueness & Syntax Check
        seen_ids: Set[str] = set()
        duplicate_ids: Set[str] = set()
        capability_map: Dict[str, Dict[str, Any]] = {}

        for idx, cap in enumerate(capabilities):
            if not isinstance(cap, dict):
                result.add_error(f"Capability at index {idx} is not an object")
                continue

            cid = cap.get("id")
            if not cid:
                result.add_error(f"Capability at index {idx} is missing required field: 'id'")
                continue

            if not isinstance(cid, str) or not CAPABILITY_ID_REGEX.match(cid):
                result.add_error(f"Capability ID '{cid}' does not match canonical pattern ^MDS-[A-Z0-9]+-[0-9]{{3}}$")

            if cid in seen_ids:
                duplicate_ids.add(cid)
            else:
                seen_ids.add(cid)
                capability_map[cid] = cap

        if duplicate_ids:
            for dup in sorted(duplicate_ids):
                result.add_error(f"Duplicate capability ID detected: '{dup}'")

        result.accounting["unique_defined_ids"] = len(seen_ids)

        # 3. Individual Capability Schema & Semantic Rules
        active_count = 0
        deferred_count = 0
        quarantined_count = 0
        disabled_count = 0
        total_wrapped = 0

        for cap in capabilities:
            cid = cap.get("id", "<unknown>")

            # Required fields
            for field in REQUIRED_CAPABILITY_FIELDS:
                if field not in cap or cap[field] is None:
                    result.add_error(f"Capability '{cid}' missing required field: '{field}'")

            # Layer validation
            layer = cap.get("layer")
            if layer and layer not in CANONICAL_LAYERS:
                result.add_error(f"Capability '{cid}' has unknown layer: '{layer}'")

            # Category validation
            category = cap.get("category")
            if category and category not in CANONICAL_CATEGORIES:
                result.add_error(f"Capability '{cid}' has unknown category: '{category}'")

            # Status validation
            status = cap.get("status")
            if status not in CANONICAL_STATUSES:
                result.add_error(f"Capability '{cid}' has unknown status: '{status}'")
            else:
                if status == "ACTIVE":
                    active_count += 1
                elif status == "DEFERRED":
                    deferred_count += 1
                elif status == "QUARANTINED":
                    quarantined_count += 1
                elif status == "DISABLED":
                    disabled_count += 1

            # Severity validation
            severity = cap.get("severity")
            if severity and severity not in CANONICAL_SEVERITIES:
                result.add_error(f"Capability '{cid}' has unknown severity: '{severity}'")

            # Execution validation
            execution = cap.get("execution")
            if execution and execution not in CANONICAL_EXECUTIONS:
                result.add_error(f"Capability '{cid}' has unknown execution method: '{execution}'")

            # Status-specific reason validations
            if status == "DEFERRED":
                reason = cap.get("deferred_reason")
                if not reason or not isinstance(reason, str) or not reason.strip():
                    result.add_error(f"DEFERRED capability '{cid}' must specify a non-empty 'deferred_reason'")

            if status == "QUARANTINED":
                reason = cap.get("quarantine_reason")
                if not reason or not isinstance(reason, str) or not reason.strip():
                    result.add_error(f"QUARANTINED capability '{cid}' must specify a non-empty 'quarantine_reason'")

            if status == "DISABLED":
                reason = cap.get("disabled_reason")
                if not reason or not isinstance(reason, str) or not reason.strip():
                    result.add_error(f"DISABLED capability '{cid}' must specify a non-empty 'disabled_reason'")

            # Runner validation
            runner = cap.get("runner")
            if status == "ACTIVE":
                if not runner or not isinstance(runner, dict):
                    result.add_error(f"ACTIVE capability '{cid}' must specify an executable 'runner' object")
                else:
                    rfile = runner.get("file")
                    rentry = runner.get("entrypoint")
                    rtype = runner.get("type")
                    if not rfile or not isinstance(rfile, str) or not rfile.strip():
                        result.add_error(f"ACTIVE capability '{cid}' runner missing non-empty 'file'")
                    if not rentry or not isinstance(rentry, str) or not rentry.strip():
                        result.add_error(f"ACTIVE capability '{cid}' runner missing non-empty 'entrypoint'")
                    if not rtype or rtype not in RUNNER_TYPES:
                        result.add_error(f"ACTIVE capability '{cid}' runner specifies invalid 'type': '{rtype}'")

            # Wrap validation
            wraps = cap.get("wraps", [])
            if not isinstance(wraps, list):
                result.add_error(f"Capability '{cid}' 'wraps' field must be a list")
            else:
                total_wrapped += len(wraps)
                for w_id in wraps:
                    if w_id == cid:
                        result.add_error(f"Capability '{cid}' cannot wrap itself")
                    elif w_id not in capability_map:
                        result.add_error(f"Capability '{cid}' references unknown wrapped ID: '{w_id}'")

        result.accounting["active_executable_assertions"] = active_count
        result.accounting["deferred_capabilities"] = deferred_count
        result.accounting["quarantined_capabilities"] = quarantined_count
        result.accounting["disabled_capabilities"] = disabled_count
        
        # wrapped_assertions is derived strictly from capability wraps
        meta_accounting = registry_data.get("metadata", {}).get("accounting", {})
        result.accounting["wrapped_assertions"] = total_wrapped

        # 4. Dependency Graph Validation (DAG & Cycle Detection)
        adj: Dict[str, List[str]] = {}
        for cid, cap in capability_map.items():
            deps = cap.get("depends_on", [])
            if not isinstance(deps, list):
                result.add_error(f"Capability '{cid}' 'depends_on' must be a list")
                continue
            adj[cid] = []
            for dep_id in deps:
                if dep_id == cid:
                    result.add_error(f"Capability '{cid}' cannot depend on itself")
                elif dep_id not in capability_map:
                    result.add_error(f"Capability '{cid}' depends on non-existent capability: '{dep_id}'")
                else:
                    adj[cid].append(dep_id)

        # DFS Cycle Detection
        visited: Dict[str, int] = {}  # 0: unvisited, 1: visiting, 2: visited
        cycle_paths: List[List[str]] = []

        def dfs(node: str, path: List[str]):
            visited[node] = 1
            for neighbor in adj.get(node, []):
                if visited.get(neighbor, 0) == 1:
                    # Found cycle
                    cycle_start = path.index(neighbor) if neighbor in path else 0
                    cycle_paths.append(path[cycle_start:] + [neighbor])
                elif visited.get(neighbor, 0) == 0:
                    dfs(neighbor, path + [neighbor])
            visited[node] = 2

        for cid in capability_map:
            if visited.get(cid, 0) == 0:
                dfs(cid, [cid])

        if cycle_paths:
            for c_path in cycle_paths:
                result.add_error(f"Circular dependency detected: {' -> '.join(c_path)}")

        # 5. Metadata Accounting Reconciliation
        metadata = registry_data.get("metadata", {})
        if metadata:
            meta_total = metadata.get("total_capabilities")
            if meta_total is not None and meta_total != result.accounting["total_capabilities"]:
                result.add_error(
                    f"Metadata total_capabilities ({meta_total}) does not match actual count ({result.accounting['total_capabilities']})"
                )

            if meta_accounting:
                if meta_accounting.get("unique_defined_ids") != result.accounting["unique_defined_ids"]:
                    result.add_error(
                        f"Accounting unique_defined_ids ({meta_accounting.get('unique_defined_ids')}) != "
                        f"actual unique IDs ({result.accounting['unique_defined_ids']})"
                    )
                if meta_accounting.get("active_executable_assertions") != result.accounting["active_executable_assertions"]:
                    result.add_error(
                        f"Accounting active_executable_assertions ({meta_accounting.get('active_executable_assertions')}) != "
                        f"actual active count ({result.accounting['active_executable_assertions']})"
                    )
                if meta_accounting.get("deferred_capabilities") != result.accounting["deferred_capabilities"]:
                    result.add_error(
                        f"Accounting deferred_capabilities ({meta_accounting.get('deferred_capabilities')}) != "
                        f"actual deferred count ({result.accounting['deferred_capabilities']})"
                    )
                if meta_accounting.get("quarantined_capabilities") != result.accounting["quarantined_capabilities"]:
                    result.add_error(
                        f"Accounting quarantined_capabilities ({meta_accounting.get('quarantined_capabilities')}) != "
                        f"actual quarantined count ({result.accounting['quarantined_capabilities']})"
                    )
                if meta_accounting.get("disabled_capabilities") != result.accounting["disabled_capabilities"]:
                    result.add_error(
                        f"Accounting disabled_capabilities ({meta_accounting.get('disabled_capabilities')}) != "
                        f"actual disabled count ({result.accounting['disabled_capabilities']})"
                    )
                if "wrapped_assertions" in meta_accounting and meta_accounting["wrapped_assertions"] != result.accounting["wrapped_assertions"]:
                    result.add_error(
                        f"Accounting wrapped_assertions ({meta_accounting.get('wrapped_assertions')}) != "
                        f"actual derived wrapped count ({result.accounting['wrapped_assertions']})"
                    )

        return result

    def validate_file(self, registry_file: Path) -> ValidationResult:
        if not registry_file.exists():
            res = ValidationResult()
            res.add_error(f"Registry file not found: {registry_file}")
            return res

        try:
            with open(registry_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            res = ValidationResult()
            res.add_error(f"Failed to parse JSON file {registry_file}: {str(e)}")
            return res

        return self.validate(data)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    default_path = Path(__file__).resolve().parent.parent / "capabilities" / "registry.json"
    target_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_path

    print(f"=========================================================================")
    print(f"             MDS CAPABILITY REGISTRY VALIDATOR                          ")
    print(f"=========================================================================")
    print(f"Target Registry: {target_path}")

    validator = RegistryValidator()
    res = validator.validate_file(target_path)

    print("\n--- Test Accounting Summary ---")
    for k, v in res.accounting.items():
        print(f"  {k:30}: {v}")

    print("\n-------------------------------------------------------------------------")
    if res.is_valid:
        print(f"[PASS] Registry is 100% VALID. All {res.accounting['total_capabilities']} capabilities conform to architecture.")
        print("-------------------------------------------------------------------------")
        sys.exit(0)
    else:
        print(f"[FAIL] Registry validation FAILED with {len(res.errors)} error(s):")
        for err in res.errors:
            print(f"  [-] {err}")
        print("-------------------------------------------------------------------------")
        sys.exit(1)


if __name__ == "__main__":
    main()
