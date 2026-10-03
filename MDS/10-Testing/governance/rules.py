"""Invariant Rules (INV-001 through INV-012) & Capability Coverage Validator for MDS.

Implements all 12 inviolable cross-document governance invariants,
dual-mode historical document validation, and the canonical capability coverage matrix validator.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .authority import AuthorityManager, AuthorityRank, AuthorityTier
from .concept_dictionary import ConceptDictionary
from .dtcg_parser import DTCGTokenParser, TokenGraph
from .knowledge_graph import KnowledgeGraph, NodeType
from .md_scanner import MarkdownScanner, ParseStatus


class FindingSeverity(str, Enum):
    BLOCKER = "BLOCKER"
    CRITICAL = "CRITICAL"
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    ADVISORY = "ADVISORY"


@dataclass
class GovernanceFinding:
    rule_id: str
    severity: FindingSeverity
    title: str
    description: str
    source_file: str
    line_number: int = 1
    remediation_hint: Optional[str] = None


class InvariantRulesEngine:
    """Executes INV-001 through INV-012 against the workspace."""

    BANNED_ENTERPRISE_SYSTEMS = [
        "RichTextEditor",
        "DataGrid",
        "MultiLevelNavigation",
        "ChartEngine",
        "FileTree",
        "WorkflowBuilder",
        "DateRangePicker",
        "KanbanBoard",
        "NotificationCenter",
    ]

    CANONICAL_19_COMPONENTS = [
        "Button", "IconButton", "Link",
        "Field", "Input", "Textarea", "Checkbox", "Radio", "Switch", "Select",
        "Alert", "Spinner", "Skeleton",
        "Badge", "Card", "Table",
        "Tabs", "Dialog", "Tooltip",
    ]

    CANONICAL_8_PATTERNS = [
        "Empty-State", "Filter-Bar", "Inline-Create", "Master-Detail",
        "Modal-Flow", "Notification-Stack", "Page-Header", "Search-Results",
    ]

    CANONICAL_6_WORKFLOWS = [
        "Form-Submission", "Search-Discovery", "Destructive-Action",
        "Settings-Update", "AI-Synthesis-Review", "Error-Recovery",
    ]

    CANONICAL_6_TEMPLATES = [
        "Dashboard-Overview", "Entity-List-View", "Entity-Detail-View",
        "Workflow-Form-Wizard", "Settings-Configuration", "Analytics-Report",
    ]

    UNIVERSAL_11_FSM_STATES = [
        "IDLE", "ACTIVE_INPUT", "VALIDATING", "CONFIRMING", "PROCESSING",
        "STREAMING", "REVIEWING", "SUCCESS_RESOLVED", "ERROR_INTERCEPTED",
        "FATAL_FAILURE", "ABORTED_CANCEL",
    ]

    def __init__(self, workspace_root: Path) -> None:
        self.root = workspace_root
        self.mds_dir = workspace_root / "MDS"
        self.concept_dict = ConceptDictionary()

    # -------------------------------------------------------------------------
    # Helper: Detect Historical Documents
    # -------------------------------------------------------------------------
    def is_historical_document(self, path: Path) -> bool:
        p_str = str(path).replace("\\", "/")
        if "MDS/13-Implementation/Phase-" in p_str:
            # Active phase vs historical
            if "Phase-9.7.8" in p_str:
                return False
            return True
        if "PROJECT_HISTORY.md" in p_str or "docs/history" in p_str:
            return True
        return False

    # -------------------------------------------------------------------------
    # INV-001: Token Inventory & DTCG Cardinality
    # -------------------------------------------------------------------------
    def validate_inv_001_tokens(self, token_graph: TokenGraph) -> List[GovernanceFinding]:
        findings = []
        tokens_dir = self.mds_dir / "02-Tokens"

        file_count = len(token_graph.files)
        token_count = len(token_graph.tokens)

        if file_count != 18:
            findings.append(
                GovernanceFinding(
                    rule_id="INV-001",
                    severity=FindingSeverity.CRITICAL,
                    title="DTCG Token File Cardinality Violation",
                    description=f"Expected exactly 18 W3C DTCG token files in MDS/02-Tokens/, found {file_count}.",
                    source_file=str(tokens_dir),
                    remediation_hint="Ensure all 18 canonical token files exist.",
                )
            )

        if token_count != 188:
            findings.append(
                GovernanceFinding(
                    rule_id="INV-001",
                    severity=FindingSeverity.CRITICAL,
                    title="Token Cardinality Invariant Violation",
                    description=f"Expected exactly 188 registered tokens, found {token_count}.",
                    source_file=str(tokens_dir),
                    remediation_hint="Synchronize token count with 188 canonical DTCG definitions.",
                )
            )

        return findings

    # -------------------------------------------------------------------------
    # INV-002: Token Reference & Alias Integrity
    # -------------------------------------------------------------------------
    def validate_inv_002_aliases(self, token_graph: TokenGraph) -> List[GovernanceFinding]:
        findings = []
        for token_name, unresolved in token_graph.unresolved_aliases:
            findings.append(
                GovernanceFinding(
                    rule_id="INV-002",
                    severity=FindingSeverity.CRITICAL,
                    title="Unresolved Token Alias Reference",
                    description=f"Token '{token_name}' references undefined alias '{{{unresolved}}}'.",
                    source_file="MDS/02-Tokens/",
                )
            )

        for token_name, depth in token_graph.max_depth_exceeded:
            findings.append(
                GovernanceFinding(
                    rule_id="INV-002",
                    severity=FindingSeverity.CRITICAL,
                    title="Token Alias Max Depth Exceeded",
                    description=f"Token '{token_name}' exceeds maximum alias resolution depth of 2 (found {depth}).",
                    source_file="MDS/02-Tokens/",
                )
            )

        return findings

    # -------------------------------------------------------------------------
    # INV-003: Core Component Inventory
    # -------------------------------------------------------------------------
    def validate_inv_003_components(self) -> List[GovernanceFinding]:
        findings = []
        comp_arch = self.mds_dir / "04-Components" / "MDS-Components-Architecture.md"
        if not comp_arch.exists():
            findings.append(
                GovernanceFinding(
                    rule_id="INV-003",
                    severity=FindingSeverity.BLOCKER,
                    title="Missing Components Master Architecture",
                    description="MDS-Components-Architecture.md is missing from 04-Components.",
                    source_file=str(comp_arch),
                )
            )
            return findings

        content = comp_arch.read_text(encoding="utf-8")
        missing_comps = [c for c in self.CANONICAL_19_COMPONENTS if f"### {c}" not in content and f"## {c}" not in content and f"`{c}`" not in content]
        if missing_comps:
            findings.append(
                GovernanceFinding(
                    rule_id="INV-003",
                    severity=FindingSeverity.CRITICAL,
                    title="Missing Canonical Component Definitions",
                    description=f"Missing {len(missing_comps)} canonical components: {missing_comps}",
                    source_file=str(comp_arch),
                )
            )

        return findings

    # -------------------------------------------------------------------------
    # INV-004: Component Anatomy Reconciliation
    # -------------------------------------------------------------------------
    def validate_inv_004_anatomy(self) -> List[GovernanceFinding]:
        findings = []
        contract_doc = self.mds_dir / "13-Implementation" / "Component-Implementation-Contract.md"
        if not contract_doc.exists():
            findings.append(
                GovernanceFinding(
                    rule_id="INV-004",
                    severity=FindingSeverity.CRITICAL,
                    title="Missing Component Implementation Contract",
                    description="Component-Implementation-Contract.md is missing from 13-Implementation.",
                    source_file=str(contract_doc),
                )
            )
            return findings

        content = contract_doc.read_text(encoding="utf-8")
        expected_points = [
            "Semantic Identifier",
            "DOM Anatomy",
            "Slot Topology",
            "Variant Hierarchy",
            "Standardized Control Scale",
            "State Coverage",
            "Token Binding",
            "Keyboard Protocol",
            "Accessibility & ARIA",
            "44×44px Hit Target",
            "Bidirectional RTL Symmetrical Flow",
            "Responsive Recomposition",
            "Custom Event Interface",
            "Error Affordances",
            "Reduced-Motion Safe",
            "Parent-Owned Spacing",
        ]

        missing_points = [p for p in expected_points if p not in content]
        if missing_points:
            findings.append(
                GovernanceFinding(
                    rule_id="INV-004",
                    severity=FindingSeverity.CRITICAL,
                    title="16-Point Implementation Contract Incomplete",
                    description=f"Component Implementation Contract missing {len(missing_points)} points: {missing_points}",
                    source_file=str(contract_doc),
                )
            )

        return findings

    # -------------------------------------------------------------------------
    # INV-005: Pattern Inventory & Inviolable Composition Laws
    # -------------------------------------------------------------------------
    def validate_inv_005_patterns(self) -> List[GovernanceFinding]:
        findings = []
        pat_dir = self.mds_dir / "05-Patterns"
        rules_doc = pat_dir / "Composition-Rules.md"
        if not rules_doc.exists():
            rules_doc = pat_dir / "Pattern-Composition-Rules.md"
        if not rules_doc.exists():
            findings.append(
                GovernanceFinding(
                    rule_id="INV-005",
                    severity=FindingSeverity.CRITICAL,
                    title="Missing Pattern Composition Rules Document",
                    description="Composition-Rules.md missing from 05-Patterns.",
                    source_file=str(rules_doc),
                )
            )
            return findings

        content = rules_doc.read_text(encoding="utf-8")
        for i in range(1, 11):
            if f"Rule {i}" not in content and f"Law {i}" not in content and f"Rule #{i}" not in content and f"Law #{i}" not in content:
                findings.append(
                    GovernanceFinding(
                        rule_id="INV-005",
                        severity=FindingSeverity.CRITICAL,
                        title=f"Missing Inviolable Pattern Composition Law {i}",
                        description=f"Rule/Law {i} is not codified in {rules_doc.name}.",
                        source_file=str(rules_doc),
                    )
                )
                break

        return findings

    # -------------------------------------------------------------------------
    # INV-006: Workflow FSM Determinism
    # -------------------------------------------------------------------------
    def validate_inv_006_workflows(self) -> List[GovernanceFinding]:
        findings = []
        fsm_doc = self.mds_dir / "06-Workflows" / "Workflow-State-Model.md"
        if not fsm_doc.exists():
            findings.append(
                GovernanceFinding(
                    rule_id="INV-006",
                    severity=FindingSeverity.CRITICAL,
                    title="Missing Universal Workflow State Model",
                    description="Workflow-State-Model.md missing from 06-Workflows.",
                    source_file=str(fsm_doc),
                )
            )
            return findings

        content = fsm_doc.read_text(encoding="utf-8")
        missing_states = [s for s in self.UNIVERSAL_11_FSM_STATES if s not in content]
        if missing_states:
            findings.append(
                GovernanceFinding(
                    rule_id="INV-006",
                    severity=FindingSeverity.CRITICAL,
                    title="Universal FSM States Incomplete",
                    description=f"Missing {len(missing_states)} standardized FSM states: {missing_states}",
                    source_file=str(fsm_doc),
                )
            )

        return findings

    # -------------------------------------------------------------------------
    # INV-007: Template Inventory & Layout Constraints
    # -------------------------------------------------------------------------
    def validate_inv_007_templates(self) -> List[GovernanceFinding]:
        findings = []
        tmp_arch = self.mds_dir / "07-Templates" / "MDS-Templates-Architecture.md"
        if not tmp_arch.exists():
            findings.append(
                GovernanceFinding(
                    rule_id="INV-007",
                    severity=FindingSeverity.CRITICAL,
                    title="Missing Templates Master Architecture",
                    description="MDS-Templates-Architecture.md missing from 07-Templates.",
                    source_file=str(tmp_arch),
                )
            )
            return findings

        content = tmp_arch.read_text(encoding="utf-8")
        if "1152px" not in content or "1440px" not in content:
            findings.append(
                GovernanceFinding(
                    rule_id="INV-007",
                    severity=FindingSeverity.CRITICAL,
                    title="Container Constraints Invariant Missing in Templates",
                    description="1152px / 1440px container constraints must be codified in Templates Architecture.",
                    source_file=str(tmp_arch),
                )
            )

        return findings

    # -------------------------------------------------------------------------
    # INV-008: Enterprise System Anti-Leak Guard
    # -------------------------------------------------------------------------
    def validate_inv_008_anti_leak(self, all_markdown_files: List[Path]) -> List[GovernanceFinding]:
        findings = []
        for mf in all_markdown_files:
            # Skip historical documents for semantic anti-leak checks if they discuss deferred items
            if self.is_historical_document(mf):
                continue

            # Core files must not implement banned enterprise systems
            if "04-Components/specifications/" in str(mf).replace("\\", "/"):
                for banned in self.BANNED_ENTERPRISE_SYSTEMS:
                    if banned in mf.name:
                        findings.append(
                            GovernanceFinding(
                                rule_id="INV-008",
                                severity=FindingSeverity.BLOCKER,
                                title=f"Banned Enterprise System Leaked in Core: {banned}",
                                description=f"File '{mf.name}' implements banned system '{banned}'. Must remain DEFERRED.",
                                source_file=str(mf),
                            )
                        )

        return findings

    # -------------------------------------------------------------------------
    # INV-009: Bipartite Capability Coverage Matrix Validator
    # -------------------------------------------------------------------------
    def validate_inv_009_capability_coverage(self) -> Tuple[List[GovernanceFinding], Dict[str, Any]]:
        findings = []
        stats: Dict[str, Any] = {
            "total_capabilities": 0,
            "direct_relations": 0,
            "wrapped_relations": 0,
            "indirect_relations": 0,
            "duplicate_covered": 0,
            "single_covered": 0,
            "uncovered": 0,
            "dsse_wrapped_count": 0,
        }

        registry_path = self.mds_dir / "10-Testing" / "capabilities" / "registry.json"
        matrix_path = self.mds_dir / "13-Implementation" / "Phase-9.7.8-Capability-Coverage-Matrix.md"

        if not registry_path.exists():
            findings.append(
                GovernanceFinding(
                    rule_id="INV-009",
                    severity=FindingSeverity.BLOCKER,
                    title="Missing Capabilities Registry",
                    description="registry.json is missing from MDS/10-Testing/capabilities/.",
                    source_file=str(registry_path),
                )
            )
            return findings, stats

        if not matrix_path.exists():
            findings.append(
                GovernanceFinding(
                    rule_id="INV-009",
                    severity=FindingSeverity.BLOCKER,
                    title="Missing Canonical Capability Coverage Matrix Artifact",
                    description="Phase-9.7.8-Capability-Coverage-Matrix.md is missing from MDS/13-Implementation/.",
                    source_file=str(matrix_path),
                )
            )
            return findings, stats

        try:
            reg_data = json.loads(registry_path.read_text(encoding="utf-8"))
            reg_caps = {c["id"]: c for c in reg_data.get("capabilities", [])}
        except Exception as e:
            findings.append(
                GovernanceFinding(
                    rule_id="INV-009",
                    severity=FindingSeverity.BLOCKER,
                    title="Corrupted Capabilities Registry JSON",
                    description=f"Failed to parse registry.json: {e}",
                    source_file=str(registry_path),
                )
            )
            return findings, stats

        matrix_content = matrix_path.read_text(encoding="utf-8")
        if "## 3. Canonical Capability-to-Test Mapping Table" not in matrix_content:
            findings.append(
                GovernanceFinding(
                    rule_id="INV-009",
                    severity=FindingSeverity.CRITICAL,
                    title="Malformed Capability Coverage Matrix Structure",
                    description="Section 3 Canonical Table is missing from matrix artifact.",
                    source_file=str(matrix_path),
                )
            )
            return findings, stats

        sec3_text = matrix_content.split("## 3. Canonical Capability-to-Test Mapping Table")[1]
        table_lines = [l for l in sec3_text.splitlines() if l.startswith("| **")]

        matrix_caps: Dict[str, Dict[str, Any]] = {}

        for l in table_lines:
            parts = [p.strip() for p in l.split("|")[1:-1]]
            if len(parts) < 8:
                continue
            num, cid_raw, domain, name, direct, wrapper, indirect, cls = parts
            cid = cid_raw.strip("`")

            # Check unknown capability ID
            if cid not in reg_caps:
                findings.append(
                    GovernanceFinding(
                        rule_id="INV-009",
                        severity=FindingSeverity.CRITICAL,
                        title=f"Unknown Capability ID in Coverage Matrix: {cid}",
                        description=f"Capability '{cid}' in matrix is not declared in registry.json.",
                        source_file=str(matrix_path),
                    )
                )

            # Check valid relation types
            valid_cls = ["`DIRECT_COVERAGE`", "`WRAPPED_COVERAGE`", "`INDIRECT_COVERAGE`", "`DUPLICATE_COVERAGE`", "`UNCOVERED`"]
            if cls not in valid_cls:
                findings.append(
                    GovernanceFinding(
                        rule_id="INV-009",
                        severity=FindingSeverity.CRITICAL,
                        title=f"Invalid Relation Type in Coverage Matrix: {cls}",
                        description=f"Capability '{cid}' uses invalid relation type '{cls}'.",
                        source_file=str(matrix_path),
                    )
                )

            # Check missing test references on disk
            if direct != "None":
                stats["direct_relations"] += 1
                test_file_ref = direct.strip("`").split("::")[0]
                full_test_path = self.root / "MDS" / test_file_ref
                if not full_test_path.exists() and not (self.root / test_file_ref).exists():
                    findings.append(
                        GovernanceFinding(
                            rule_id="INV-009",
                            severity=FindingSeverity.CRITICAL,
                            title=f"Missing Test Reference on Disk: {test_file_ref}",
                            description=f"Test file referenced by capability '{cid}' does not exist on disk.",
                            source_file=str(matrix_path),
                        )
                    )

            if wrapper != "None":
                stats["wrapped_relations"] += 1
                if "MDS-DSS-004" in wrapper:
                    stats["dsse_wrapped_count"] += 1

            if indirect != "None":
                stats["indirect_relations"] += len(indirect.split(","))

            matrix_caps[cid] = {
                "direct": direct,
                "wrapper": wrapper,
                "indirect": indirect,
                "cls": cls,
            }

        # Check every registered capability is represented
        missing_from_matrix = [cid for cid in reg_caps if cid not in matrix_caps]
        if missing_from_matrix:
            findings.append(
                GovernanceFinding(
                    rule_id="INV-009",
                    severity=FindingSeverity.CRITICAL,
                    title="Capabilities Missing from Canonical Coverage Matrix",
                    description=f"{len(missing_from_matrix)} capabilities from registry.json missing from matrix: {missing_from_matrix}",
                    source_file=str(matrix_path),
                )
            )

        # Check for uncovered capabilities (mechanical detection)
        uncovered_caps = []
        duplicate_caps = []
        single_caps = []

        for cid, data in matrix_caps.items():
            valid_relations = 0
            if data["direct"] != "None":
                valid_relations += 1
            if data["wrapper"] != "None":
                valid_relations += 1
            if data["indirect"] != "None":
                valid_relations += 1

            if valid_relations == 0:
                uncovered_caps.append(cid)
            elif valid_relations > 1:
                duplicate_caps.append(cid)
            else:
                single_caps.append(cid)

        if uncovered_caps:
            findings.append(
                GovernanceFinding(
                    rule_id="INV-009",
                    severity=FindingSeverity.BLOCKER,
                    title="Zero-Coverage Blocker Detected",
                    description=f"{len(uncovered_caps)} capabilities have 0 test relations: {uncovered_caps}",
                    source_file=str(matrix_path),
                )
            )

        # Check DSSE 37 wrapper completeness
        if stats["dsse_wrapped_count"] != 37:
            findings.append(
                GovernanceFinding(
                    rule_id="INV-009",
                    severity=FindingSeverity.CRITICAL,
                    title="DSSE 37-Assertion Wrapper Mismatch",
                    description=f"Expected exactly 37 DSSE assertions wrapped by MDS-DSS-004, found {stats['dsse_wrapped_count']}.",
                    source_file=str(matrix_path),
                )
            )

        stats["total_capabilities"] = len(matrix_caps)
        stats["duplicate_covered"] = len(duplicate_caps)
        stats["single_covered"] = len(single_caps)
        stats["uncovered"] = len(uncovered_caps)

        return findings, stats

    # -------------------------------------------------------------------------
    # INV-010: DSSE Mathematical Model Alignment
    # -------------------------------------------------------------------------
    def validate_inv_010_dsse(self) -> List[GovernanceFinding]:
        findings = []
        dsse_spec = self.mds_dir / "AGENT" / "DESIGN_SYSTEM_SELECTION_ENGINE.md"
        if not dsse_spec.exists():
            dsse_spec = self.root / "DESIGN_SYSTEM_SELECTION_ENGINE.md"
        if not dsse_spec.exists():
            findings.append(
                GovernanceFinding(
                    rule_id="INV-010",
                    severity=FindingSeverity.CRITICAL,
                    title="Missing DSSE Mathematical Specification",
                    description="DESIGN_SYSTEM_SELECTION_ENGINE.md missing from MDS/AGENT/.",
                    source_file=str(dsse_spec),
                )
            )
            return findings

        content = dsse_spec.read_text(encoding="utf-8")
        required_concepts = [
            ("C_req", ["C_req", "C_{\\text{req}}"]),
            ("C_eval", ["C_eval", "C_{\\text{eval}}"]),
            ("C_evid", ["C_evid", "C_{\\text{evid}}"]),
            ("C_epistemic", ["C_epistemic", "C_{\\text{epistemic}}"]),
            ("Virtual Tie", ["Virtual Tie"]),
            ("Tie-Break Zone", ["Tie-Break Zone"]),
            ("Decisive Lead", ["Decisive Lead"]),
        ]
        missing = []
        for concept_name, candidates in required_concepts:
            if not any(cand in content for cand in candidates):
                missing.append(concept_name)

        if missing:
            findings.append(
                GovernanceFinding(
                    rule_id="INV-010",
                    severity=FindingSeverity.CRITICAL,
                    title="DSSE Mathematical Specification Desynchronization",
                    description=f"Missing core mathematical formulas: {missing}",
                    source_file=str(dsse_spec),
                )
            )

        return findings

    # -------------------------------------------------------------------------
    # INV-011: Documentation Index Synchronization
    # -------------------------------------------------------------------------
    def validate_inv_011_doc_index(self) -> List[GovernanceFinding]:
        findings = []
        doc_index_path = self.mds_dir / "Documentation" / "Documentation-Index.json"
        if not doc_index_path.exists():
            findings.append(
                GovernanceFinding(
                    rule_id="INV-011",
                    severity=FindingSeverity.MAJOR,
                    title="Missing Documentation Index JSON",
                    description="Documentation-Index.json missing from MDS/Documentation/.",
                    source_file=str(doc_index_path),
                )
            )
            return findings

        try:
            data = json.loads(doc_index_path.read_text(encoding="utf-8"))
        except Exception as e:
            findings.append(
                GovernanceFinding(
                    rule_id="INV-011",
                    severity=FindingSeverity.CRITICAL,
                    title="Corrupted Documentation-Index.json",
                    description=f"Failed to parse JSON: {e}",
                    source_file=str(doc_index_path),
                )
            )
            return findings

        # Verify counts in invariants section (or fallback summary)
        invariants = data.get("invariants", {})
        tokens_total = invariants.get("tokens_total", data.get("summary", {}).get("tokens_total"))
        if tokens_total != 188:
            findings.append(
                GovernanceFinding(
                    rule_id="INV-011",
                    severity=FindingSeverity.MAJOR,
                    title="Documentation Index Token Count Drift",
                    description=f"Documentation index shows {tokens_total} tokens (expected 188).",
                    source_file=str(doc_index_path),
                )
            )

        return findings

    # -------------------------------------------------------------------------
    # INV-012: Intra-Repository Link & Path Integrity
    # -------------------------------------------------------------------------
    def validate_inv_012_links(self, all_markdown_files: List[Path]) -> List[GovernanceFinding]:
        findings = []
        from urllib.parse import unquote, urlparse

        placeholder_targets = {"url", "path/to/file.md", "relative/path.md", "link", "destination"}

        for mf in all_markdown_files:
            parse_res = MarkdownScanner.scan_file(mf)
            for link in parse_res.links:
                target = link.target
                if not target or target.startswith("http://") or target.startswith("https://") or target.startswith("mailto:") or target.startswith("#") or target.startswith("ref:"):
                    continue

                if target in placeholder_targets:
                    continue

                # Strip anchor
                path_part = target.split("#")[0]
                if not path_part or path_part in placeholder_targets:
                    continue

                # File URI vs Relative link resolution
                if path_part.startswith("file://"):
                    p = unquote(urlparse(path_part).path)
                    if p.startswith("/") and len(p) > 2 and p[2] == ":":
                        p = p[1:]
                    resolved = Path(p)
                else:
                    resolved = (mf.parent / path_part).resolve()

                if not resolved.exists():
                    is_hist = self.is_historical_document(mf)
                    sev = FindingSeverity.MAJOR
                    try:
                        rel_source = mf.relative_to(self.root).as_posix()
                    except ValueError:
                        rel_source = str(mf)

                    tier, rank = AuthorityManager.resolve_file_tier_and_rank(rel_source)

                    if "Runtime/" in rel_source:
                        classification = f"Tier {tier.value} Realization (Runtime Spec Pointer)"
                        reason = "Reference to historical/legacy phase filename (MDS/13-Implementation/Phase-9.1-Implementation-Architecture.md) rather than canonical architecture spec (MDS-Implementation-Architecture.md)"
                    elif "README.md" in rel_source:
                        classification = f"Tier {tier.value} Advisory Guidance (Layer Pointer README)"
                        if "Primitives-Decision-Log" in target:
                            reason = "Typographical pluralization mismatch ('Primitives' vs canonical 'Primitive-Decision-Log.md')"
                        else:
                            reason = "Provisional pre-standardization entity name referenced prior to final layer ratification"
                    elif is_hist:
                        classification = f"Tier {tier.value} Operational (Historical Document)"
                        reason = "Broken intra-repository reference in historical archive document"
                    else:
                        classification = f"Tier {tier.value} Canonical Specification"
                        reason = "Broken intra-repository reference in active specification"

                    findings.append(
                        GovernanceFinding(
                            rule_id="INV-012",
                            severity=sev,
                            title="Broken Intra-Repository Link",
                            description=(
                                f"Link '[{link.text}]({target})' does not resolve to a file on disk. "
                                f"[Classification: {classification}] "
                                f"[Validation Mode: Strict Structural] "
                                f"[Reason: {reason}]"
                            ),
                            source_file=rel_source,
                            line_number=link.line,
                            remediation_hint="Update target to resolve to canonical path on disk (Validation mode: Strict Structural).",
                        )
                    )

        return findings
