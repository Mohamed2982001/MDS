"""Master Governance & Consistency Engine Orchestrator for MDS.

Ingests repository files, constructs normalized IR Knowledge Graph,
executes invariant rules INV-001 through INV-012, and produces telemetry reports.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from .authority import AuthorityManager
from .concept_dictionary import ConceptDictionary
from .dtcg_parser import DTCGTokenParser, TokenGraph
from .knowledge_graph import EdgeType, GraphEdge, GraphNode, KnowledgeGraph, NodeType
from .md_scanner import MarkdownScanner, ParseResult, ParseStatus
from .rules import FindingSeverity, GovernanceFinding, InvariantRulesEngine


@dataclass
class PerformanceTelemetry:
    wall_clock_ms: float
    files_scanned: int
    markdown_files: int
    token_files: int
    nodes_count: int
    edges_count: int
    benchmark_status: str = "PASS"  # PASS or ADVISORY_EXCEEDED
    benchmark_note: Optional[str] = None


@dataclass
class GovernanceResult:
    is_success: bool
    exit_code: int
    findings: List[GovernanceFinding] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)
    telemetry: Optional[PerformanceTelemetry] = None
    capability_coverage_stats: Dict[str, Any] = field(default_factory=dict)

    @property
    def blocker_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == FindingSeverity.BLOCKER)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == FindingSeverity.CRITICAL)

    @property
    def major_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == FindingSeverity.MAJOR)

    @property
    def minor_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == FindingSeverity.MINOR)

    @property
    def advisory_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == FindingSeverity.ADVISORY)


class GovernanceEngine:
    """Master engine orchestrating static discovery, IR ingestion, and invariant audits."""

    WARM_BENCHMARK_MS = 500.0
    COLD_BENCHMARK_MS = 1200.0

    def __init__(self, workspace_root: Optional[Path] = None) -> None:
        if workspace_root is None:
            # Detect root from current file path
            self.root = Path(__file__).resolve().parent.parent.parent.parent
        else:
            self.root = Path(workspace_root).resolve()

        self.mds_dir = self.root / "MDS"
        self.knowledge_graph = KnowledgeGraph()
        self.concept_dict = ConceptDictionary()
        self.rules_engine = InvariantRulesEngine(workspace_root=self.root)

    def discover_files(self) -> Dict[str, List[Path]]:
        """Discovers markdown, JSON tokens, and python test files."""
        discovered: Dict[str, List[Path]] = {
            "markdown": [],
            "tokens": [],
            "tests": [],
        }

        # Scan MDS/ and docs/
        target_dirs = [self.root / "MDS", self.root / "docs"]
        for td in target_dirs:
            if not td.exists():
                continue
            for p in td.rglob("*.md"):
                # Ignore temp / cache dirs
                if any(part.startswith(".") or part in ("node_modules", "__pycache__", "scratch") for part in p.parts):
                    continue
                discovered["markdown"].append(p)

        tokens_dir = self.mds_dir / "02-Tokens"
        if tokens_dir.exists():
            discovered["tokens"] = sorted(tokens_dir.rglob("*.tokens.json"))

        tests_dir = self.mds_dir / "10-Testing"
        if tests_dir.exists():
            discovered["tests"] = sorted(tests_dir.rglob("test_*.py"))

        return discovered

    def build_knowledge_graph(self, discovered: Dict[str, List[Path]], token_graph: TokenGraph) -> None:
        """Ingests tokens, documents, and specifications into the KnowledgeGraph."""
        # 1. Ingest Tokens
        for tok_name, tok in token_graph.tokens.items():
            tier, rank = AuthorityManager.resolve_file_tier_and_rank(f"MDS/02-Tokens/{tok.source_file}")
            node = GraphNode(
                canonical_id=f"token:{tok_name}",
                concept_id=f"TOKEN.{tok_name.upper()}",
                node_type=NodeType.TOKEN,
                source_file=f"MDS/02-Tokens/{tok.source_file}",
                line_start=1,
                line_end=1,
                authority_tier=int(tier),
                authority_rank=int(rank),
                attributes={"raw_value": tok.value, "aliases": tok.aliases, "type": tok.token_type},
            )
            self.knowledge_graph.add_node(node)

            for alias in tok.aliases:
                self.knowledge_graph.add_edge(
                    GraphEdge(
                        source_id=f"token:{tok_name}",
                        target_id=f"token:{alias}",
                        edge_type=EdgeType.REFERENCES,
                    )
                )

        # 2. Ingest Markdown Documents
        for mf in discovered["markdown"]:
            rel_path = mf.relative_to(self.root).as_posix()
            tier, rank = AuthorityManager.resolve_file_tier_and_rank(rel_path)
            doc_node = GraphNode(
                canonical_id=f"doc:{rel_path}",
                concept_id="NONE",
                node_type=NodeType.DOCUMENT,
                source_file=rel_path,
                line_start=1,
                line_end=1,
                authority_tier=int(tier),
                authority_rank=int(rank),
            )
            self.knowledge_graph.add_node(doc_node)

    def audit_all(self, strict_mode: bool = False, fast_mode: bool = False) -> GovernanceResult:
        """Executes full cross-document governance audit."""
        start_time = time.perf_counter()

        # Step 1: Discovery
        discovered = self.discover_files()

        # Step 2: Parse Tokens
        token_graph = DTCGTokenParser.parse_tokens_directory(self.mds_dir / "02-Tokens")

        # Step 3: Build Normalized IR Knowledge Graph
        self.build_knowledge_graph(discovered, token_graph)

        findings: List[GovernanceFinding] = []

        # Step 4: Run Invariants
        findings.extend(self.rules_engine.validate_inv_001_tokens(token_graph))
        findings.extend(self.rules_engine.validate_inv_002_aliases(token_graph))
        findings.extend(self.rules_engine.validate_inv_003_components())
        findings.extend(self.rules_engine.validate_inv_004_anatomy())
        findings.extend(self.rules_engine.validate_inv_005_patterns())
        findings.extend(self.rules_engine.validate_inv_006_workflows())
        findings.extend(self.rules_engine.validate_inv_007_templates())
        findings.extend(self.rules_engine.validate_inv_008_anti_leak(discovered["markdown"]))

        cov_findings, cov_stats = self.rules_engine.validate_inv_009_capability_coverage()
        findings.extend(cov_findings)

        findings.extend(self.rules_engine.validate_inv_010_dsse())
        findings.extend(self.rules_engine.validate_inv_011_doc_index())

        if not fast_mode:
            findings.extend(self.rules_engine.validate_inv_012_links(discovered["markdown"]))

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        # Performance Benchmark Telemetry
        bench_status = "PASS"
        bench_note = None
        if elapsed_ms > self.WARM_BENCHMARK_MS:
            bench_status = "ADVISORY_EXCEEDED"
            bench_note = f"Warm benchmark target ({self.WARM_BENCHMARK_MS}ms) exceeded ({elapsed_ms:.1f}ms). Non-blocking ADVISORY."
            findings.append(
                GovernanceFinding(
                    rule_id="PERF-001",
                    severity=FindingSeverity.ADVISORY,
                    title="Performance Benchmark Target Advisory",
                    description=bench_note,
                    source_file="governance_engine",
                )
            )

        telemetry = PerformanceTelemetry(
            wall_clock_ms=elapsed_ms,
            files_scanned=len(discovered["markdown"]) + len(discovered["tokens"]) + len(discovered["tests"]),
            markdown_files=len(discovered["markdown"]),
            token_files=len(discovered["tokens"]),
            nodes_count=len(self.knowledge_graph.nodes),
            edges_count=len(self.knowledge_graph.edges),
            benchmark_status=bench_status,
            benchmark_note=bench_note,
        )

        # Determine Exit Code & Success
        blockers = sum(1 for f in findings if f.severity == FindingSeverity.BLOCKER)
        criticals = sum(1 for f in findings if f.severity == FindingSeverity.CRITICAL)
        majors = sum(1 for f in findings if f.severity == FindingSeverity.MAJOR)

        if blockers > 0:
            exit_code = 2
            is_success = False
        elif criticals > 0:
            exit_code = 1
            is_success = False
        elif strict_mode and majors > 0:
            exit_code = 1
            is_success = False
        else:
            exit_code = 0
            is_success = True

        stats = {
            "total_findings": len(findings),
            "blockers": blockers,
            "criticals": criticals,
            "majors": majors,
            "minors": sum(1 for f in findings if f.severity == FindingSeverity.MINOR),
            "advisories": sum(1 for f in findings if f.severity == FindingSeverity.ADVISORY),
        }

        return GovernanceResult(
            is_success=is_success,
            exit_code=exit_code,
            findings=findings,
            stats=stats,
            telemetry=telemetry,
            capability_coverage_stats=cov_stats,
        )
