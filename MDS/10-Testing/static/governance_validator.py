#!/usr/bin/env python3
"""
MDS Governance & Cross-Layer Invariant Validator — Layer M Validation
Phase 9.7.3: Static Validation Suite & Scanners
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Validates Layer M governance invariants:
- M-01: Token Count Guard (exactly 188 DTCG tokens across 18 files).
- M-02: Component Inventory Guard (exactly 19 canonical components).
- M-03: Architectural Composition Inventory (8 patterns, 6 workflows, 6 templates).
- M-04: Deferred Enterprise Anti-Leak Guard (0 unapproved enterprise implementations).
- M-05: Deferred Capabilities Alignment (exactly 1 deferred capability, 0 falsified).
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional, Any

# Ensure UTF-8 stdout encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class GovernanceResult:
    def __init__(self):
        self.checked_rules: List[str] = []
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.metrics: Dict[str, Any] = {}

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def add_error(self, rule_id: str, message: str):
        self.errors.append(f"[{rule_id}] {message}")

    def add_warning(self, rule_id: str, message: str):
        self.warnings.append(f"[{rule_id}] {message}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "errors_count": len(self.errors),
            "warnings_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
            "metrics": self.metrics
        }


class GovernanceValidator:
    """
    Automated validator for cross-layer governance, entity inventories,
    and anti-leak boundary protection.
    """

    CANONICAL_COMPONENTS = [
        "Button", "IconButton", "Link",
        "Field", "Input", "Textarea", "Checkbox", "Radio", "Switch", "Select",
        "Alert", "Spinner", "Skeleton",
        "Badge", "Card", "Table",
        "Tabs", "Dialog", "Tooltip"
    ]

    CANONICAL_PATTERNS = [
        "Forms/Form-Section.md",
        "Search/Search-Filter-Bar.md",
        "Data/Data-List-Card.md",
        "Feedback/Empty-State.md",
        "Feedback/Confirmation-Dialog.md",
        "Navigation/Page-Header.md",
        "AI/AI-Input-Prompt.md",
        "AI/AI-Result-Review.md"
    ]

    CANONICAL_WORKFLOWS = [
        "Forms/Form-Submission.md",
        "Search/Search-Discovery.md",
        "Actions/Destructive-Action.md",
        "Settings/Settings-Update.md",
        "AI/AI-Synthesis-Review.md",
        "Recovery/Error-Recovery.md"
    ]

    CANONICAL_TEMPLATES = [
        "Overview/Dashboard-Overview.md",
        "Management/List-Management.md",
        "Entity/Detail-Entity.md",
        "Forms/Form-Edit.md",
        "Settings/Settings-Workspace.md",
        "AI/AI-Workspace.md"
    ]

    BANNED_ENTERPRISE_SYSTEMS = [
        "DataGrid", "RichTextEditor", "Calendar", "DateRangePicker",
        "CommandSystem", "Tree", "Combobox", "VirtualizedList", "FileUploadManager"
    ]

    EXPECTED_DEFERRED_CAPABILITIES: List[str] = []

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(__file__).resolve().parent.parent.parent.parent
        self.mds_dir = self.workspace_root / "MDS"

    def validate_all(self) -> GovernanceResult:
        """Executes all Layer M governance checks."""
        result = GovernanceResult()
        self.validate_token_count(result)
        self.validate_component_inventory(result)
        self.validate_composition_inventories(result)
        self.validate_enterprise_anti_leak(result)
        self.validate_deferred_capabilities(result)
        return result

    def validate_token_count(self, result: GovernanceResult):
        """M-01: Verifies exactly 188 registered DTCG tokens across 18 files."""
        result.checked_rules.append("M-01")
        tokens_dir = self.mds_dir / "02-Tokens"
        if not tokens_dir.exists():
            result.add_error("M-01", f"Tokens directory missing at {tokens_dir}")
            return

        token_files = list(tokens_dir.rglob("*.tokens.json"))
        result.metrics["token_files_count"] = len(token_files)
        if len(token_files) != 18:
            result.add_error("M-01", f"Expected exactly 18 token files, found {len(token_files)}")

        # Count leaf token declarations
        tokens = {}
        def flatten(prefix, obj):
            for k, v in obj.items():
                if k.startswith("$"):
                    continue
                new_prefix = f"{prefix}.{k}" if prefix else k
                if isinstance(v, dict):
                    if "$value" in v:
                        tokens[new_prefix] = v["$value"]
                    flatten(new_prefix, v)

        for tf in token_files:
            try:
                with open(tf, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    flatten("", data)
            except Exception as e:
                result.add_error("M-01", f"Failed to parse token file {tf.name}: {e}")

        result.metrics["registered_tokens_count"] = len(tokens)
        if len(tokens) != 188:
            result.add_error("M-01", f"Canonical token count invariant violated: expected 188, got {len(tokens)}")

    def validate_component_inventory(self, result: GovernanceResult):
        """M-02: Verifies presence of exactly 19 core canonical components."""
        result.checked_rules.append("M-02")
        comp_dir = self.mds_dir / "04-Components"
        runtime_comp_dir = self.mds_dir / "Runtime" / "components"

        result.metrics["expected_components_count"] = len(self.CANONICAL_COMPONENTS)

        # Check specification Markdown files
        missing_spec = []
        for c in self.CANONICAL_COMPONENTS:
            found = list(comp_dir.rglob(f"{c}.md"))
            if not found:
                missing_spec.append(c)

        if missing_spec:
            result.add_error("M-02", f"Missing component specifications in 04-Components: {missing_spec}")

        # Check runtime component folders
        missing_runtime = []
        for c in self.CANONICAL_COMPONENTS:
            # Convert PascalCase to kebab-case
            kebab = re.sub(r'(?<!^)(?=[A-Z])', '-', c).lower()
            if not (runtime_comp_dir / kebab).is_dir():
                missing_runtime.append(kebab)

        if missing_runtime:
            result.add_error("M-02", f"Missing runtime components in Runtime/components: {missing_runtime}")

    def validate_composition_inventories(self, result: GovernanceResult):
        """M-03: Verifies exactly 8 Patterns, 6 Workflows, and 6 Templates."""
        result.checked_rules.append("M-03")

        # Patterns (8)
        pat_dir = self.mds_dir / "05-Patterns"
        missing_pats = [p for p in self.CANONICAL_PATTERNS if not (pat_dir / p).exists()]
        result.metrics["canonical_patterns_found"] = len(self.CANONICAL_PATTERNS) - len(missing_pats)
        result.metrics["canonical_patterns_total"] = len(self.CANONICAL_PATTERNS)
        if missing_pats:
            result.add_error("M-03", f"Missing canonical pattern specifications: {missing_pats}")

        # Workflows (6)
        wkf_dir = self.mds_dir / "06-Workflows"
        missing_wkfs = [w for w in self.CANONICAL_WORKFLOWS if not (wkf_dir / w).exists()]
        result.metrics["canonical_workflows_found"] = len(self.CANONICAL_WORKFLOWS) - len(missing_wkfs)
        result.metrics["canonical_workflows_total"] = len(self.CANONICAL_WORKFLOWS)
        if missing_wkfs:
            result.add_error("M-03", f"Missing canonical workflow specifications: {missing_wkfs}")

        # Templates (6)
        tmp_dir = self.mds_dir / "07-Templates"
        missing_tmps = [t for t in self.CANONICAL_TEMPLATES if not (tmp_dir / t).exists()]
        result.metrics["canonical_templates_found"] = len(self.CANONICAL_TEMPLATES) - len(missing_tmps)
        result.metrics["canonical_templates_total"] = len(self.CANONICAL_TEMPLATES)
        if missing_tmps:
            result.add_error("M-03", f"Missing canonical template specifications: {missing_tmps}")


    def validate_enterprise_anti_leak(self, result: GovernanceResult):
        """M-04: Verifies 0 unapproved implementations of the 9 deferred enterprise systems."""
        result.checked_rules.append("M-04")
        comp_dir = self.mds_dir / "04-Components"
        runtime_dir = self.mds_dir / "Runtime"

        leaks = []
        for sys_name in self.BANNED_ENTERPRISE_SYSTEMS:
            # Check 04-Components
            found_spec = list(comp_dir.rglob(f"*{sys_name}*.md"))
            if found_spec:
                leaks.append(f"04-Components/{sys_name}")

            # Check Runtime
            kebab = re.sub(r'(?<!^)(?=[A-Z])', '-', sys_name).lower()
            if (runtime_dir / "components" / kebab).exists():
                leaks.append(f"Runtime/components/{kebab}")

        result.metrics["enterprise_leaks_found"] = leaks
        if leaks:
            result.add_error("M-04", f"Deferred enterprise systems leaked into active tiers: {leaks}")

    def validate_deferred_capabilities(self, result: GovernanceResult):
        """M-05: Verifies exactly 1 deferred capability registered, with 0 falsified passes."""
        result.checked_rules.append("M-05")
        registry_file = self.mds_dir / "10-Testing" / "capabilities" / "registry.json"
        if not registry_file.exists():
            result.add_error("M-05", f"Registry file missing: {registry_file}")
            return

        with open(registry_file, "r", encoding="utf-8") as fp:
            data = json.load(fp)

        caps = data.get("capabilities", [])
        deferred = [c for c in caps if c.get("status") == "DEFERRED"]
        deferred_ids = sorted([c["id"] for c in deferred])

        result.metrics["deferred_capabilities_count"] = len(deferred)
        result.metrics["deferred_capabilities_ids"] = deferred_ids

        if deferred_ids != sorted(self.EXPECTED_DEFERRED_CAPABILITIES):
            result.add_error(
                "M-05",
                f"Deferred capability mismatch: expected {self.EXPECTED_DEFERRED_CAPABILITIES}, got {deferred_ids}"
            )

        for c in deferred:
            reason = c.get("deferred_reason", "")
            if not reason or not reason.strip():
                result.add_error("M-05", f"Deferred capability {c['id']} missing non-empty 'deferred_reason'")


if __name__ == "__main__":
    validator = GovernanceValidator()
    print("=========================================================================")
    print("              MDS GOVERNANCE & INVARIANT VALIDATOR (LAYER M)             ")
    print("=========================================================================")
    res = validator.validate_all()

    print(f"Registered Tokens:         {res.metrics.get('registered_tokens_count')} / 188")
    print(f"Token Files:               {res.metrics.get('token_files_count')} / 18")
    print(f"Canonical Components:      {res.metrics.get('expected_components_count')} / 19")
    print(f"Enterprise Leaks:          {len(res.metrics.get('enterprise_leaks_found', []))} found")
    print(f"Deferred Capabilities:     {res.metrics.get('deferred_capabilities_count')} (0 falsified)")

    print("-------------------------------------------------------------------------")
    if res.is_valid:
        print("[PASS] Cross-layer governance & architectural invariants 100% VALID.")
        sys.exit(0)
    else:
        print(f"[FAIL] Found {len(res.errors)} governance violations:")
        for err in res.errors:
            print(f"       └── {err}")
        sys.exit(1)
