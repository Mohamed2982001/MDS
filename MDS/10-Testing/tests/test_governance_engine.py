#!/usr/bin/env python3
"""
Unit Tests for MDS Governance & Cross-Document Consistency Engine (Layer M - Phase 9.7.8).

Covers all 28 mandatory test areas including:
- Markdown Lexer & AST Scanner (Headings, Tables, Code Fences, Links, Alerts)
- W3C DTCG Token Parser (Cardinality, Types, Aliases, Cycle Detection)
- Safe Python AST Inspector
- Normalized IR Knowledge Graph (12 Node Types, 10 Edge Types)
- Canonical Concept Dictionary (4-Stage Pipeline)
- 5-Tier Authority Hierarchy & Intra-Tier 1 Precedence
- Invariants INV-001 through INV-012
- Bipartite Capability Coverage Matrix & 37-Assertion DSSE Wrapper
- Dual-Mode Historical Document Invariant
- Console & JSON Telemetry Reporters
- Master Governance Engine Orchestration (< 500ms benchmark)
"""

from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

TESTING_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = TESTING_DIR.parent.parent
sys.path.insert(0, str(TESTING_DIR))

from governance.authority import AuthorityManager, AuthorityRank, AuthorityTier
from governance.concept_dictionary import ConceptDictionary
from governance.dtcg_parser import DTCGTokenParser, TokenGraph
from governance.engine import GovernanceEngine, GovernanceResult
from governance.knowledge_graph import EdgeType, GraphEdge, GraphNode, KnowledgeGraph, NodeType
from governance.md_scanner import MarkdownScanner, ParseStatus
from governance.python_ast_extractor import PythonAstExtractor
from governance.reporters import ConsoleReporter, JsonReporter
from governance.rules import FindingSeverity, GovernanceFinding, InvariantRulesEngine


class TestGovernanceEngine(unittest.TestCase):
    """Exhaustive test suite for MDS Phase 9.7.8 Governance Engine."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = WORKSPACE_ROOT
        cls.engine = GovernanceEngine(workspace_root=cls.root)
        cls.rules_engine = InvariantRulesEngine(workspace_root=cls.root)

    # =========================================================================
    # 1. Markdown Lexer & AST Scanner Tests (4.1 & 4.2)
    # =========================================================================
    def test_01_md_scanner_headings(self) -> None:
        sample = (
            "# Top Level Title\n\n"
            "Intro paragraph.\n\n"
            "## Section 1: Overview\n\n"
            "### Subsection 1.1: Architecture Details ###\n"
        )
        res = MarkdownScanner.scan_content(sample)
        self.assertEqual(res.status, ParseStatus.PARSE_SUCCESS)
        self.assertEqual(len(res.headings), 3)
        self.assertEqual(res.headings[0].level, 1)
        self.assertEqual(res.headings[0].text, "Top Level Title")
        self.assertEqual(res.headings[0].slug, "top-level-title")
        self.assertEqual(res.headings[1].level, 2)
        self.assertEqual(res.headings[1].text, "Section 1: Overview")
        self.assertEqual(res.headings[1].slug, "section-1-overview")
        self.assertEqual(res.headings[2].level, 3)
        self.assertEqual(res.headings[2].text, "Subsection 1.1: Architecture Details")

    def test_02_md_scanner_tables(self) -> None:
        sample = (
            "| ID | Component | Intent |\n"
            "| :--- | :--- | ---: |\n"
            "| 01 | Button | Action |\n"
            "| 02 | Input | Data Entry |\n"
        )
        res = MarkdownScanner.scan_content(sample)
        self.assertEqual(res.status, ParseStatus.PARSE_SUCCESS)
        self.assertEqual(len(res.tables), 1)
        tbl = res.tables[0]
        self.assertEqual(tbl.headers, ["ID", "Component", "Intent"])
        self.assertEqual(len(tbl.rows), 2)
        self.assertEqual(tbl.rows[0], ["01", "Button", "Action"])
        self.assertEqual(tbl.rows[1], ["02", "Input", "Data Entry"])

    def test_03_md_scanner_code_fences(self) -> None:
        sample = (
            "Before fence\n\n"
            "```json\n"
            '{"name": "test", "items": [1, 2, 3]}\n'
            "# This is not a markdown heading\n"
            "[not a link](file.md)\n"
            "```\n\n"
            "After fence\n"
        )
        res = MarkdownScanner.scan_content(sample)
        self.assertEqual(res.status, ParseStatus.PARSE_SUCCESS)
        self.assertEqual(len(res.code_fences), 1)
        fence = res.code_fences[0]
        self.assertEqual(fence.language, "json")
        self.assertIn('"name": "test"', fence.content)
        # Content inside code fences must NOT leak into headings or links
        self.assertEqual(len(res.headings), 0)
        self.assertEqual(len(res.links), 0)

    def test_04_md_scanner_links_and_images(self) -> None:
        sample = (
            "Read [MDS Master Spec](MDS/MDS_MASTER_SPECIFICATION.md).\n"
            "See diagram: ![Arch Diagram](assets/arch.png).\n"
            "Ref link: [Reference Docs][ref1].\n"
        )
        res = MarkdownScanner.scan_content(sample)
        self.assertEqual(res.status, ParseStatus.PARSE_SUCCESS)
        self.assertEqual(len(res.links), 3)

        link_targets = {l.text: (l.target, l.is_image) for l in res.links}
        self.assertIn("MDS Master Spec", link_targets)
        self.assertEqual(link_targets["MDS Master Spec"], ("MDS/MDS_MASTER_SPECIFICATION.md", False))

        self.assertIn("Arch Diagram", link_targets)
        self.assertEqual(link_targets["Arch Diagram"], ("assets/arch.png", True))

        self.assertIn("Reference Docs", link_targets)
        self.assertEqual(link_targets["Reference Docs"][0], "ref:ref1")

    def test_05_md_scanner_blockquotes_and_alerts(self) -> None:
        sample = (
            "> Regular blockquote paragraph 1\n"
            "> Regular blockquote line 2\n\n"
            "> [!NOTE]\n"
            "> This is an architectural alert note.\n\n"
            "> [!WARNING]\n"
            "> Caution: do not mutate canonical files.\n"
        )
        res = MarkdownScanner.scan_content(sample)
        self.assertEqual(res.status, ParseStatus.PARSE_SUCCESS)
        self.assertEqual(len(res.blockquotes), 3)
        self.assertIsNone(res.blockquotes[0].alert_type)
        self.assertEqual(res.blockquotes[1].alert_type, "NOTE")
        self.assertIn("architectural alert note", res.blockquotes[1].content)
        self.assertEqual(res.blockquotes[2].alert_type, "WARNING")
        self.assertIn("do not mutate", res.blockquotes[2].content)

    def test_06_md_scanner_status_and_telemetry(self) -> None:
        sample = "# Valid Document\nSome content.\n"
        res = MarkdownScanner.scan_content(sample)
        self.assertEqual(res.status, ParseStatus.PARSE_SUCCESS)
        self.assertIn("total_lines", res.telemetry)
        self.assertIn("headings_count", res.telemetry)
        self.assertEqual(res.telemetry["headings_count"], 1)

    # =========================================================================
    # 2. W3C DTCG Token Parser Tests
    # =========================================================================
    def test_07_dtcg_parser_cardinality_and_types(self) -> None:
        tokens_dir = self.root / "MDS" / "02-Tokens"
        graph = DTCGTokenParser.parse_tokens_directory(tokens_dir)
        self.assertEqual(len(graph.files), 18, f"Expected 18 token files, found {len(graph.files)}")
        self.assertEqual(len(graph.tokens), 188, f"Expected 188 registered tokens, found {len(graph.tokens)}")

        # Verify key token types exist
        types = {t.token_type for t in graph.tokens.values()}
        self.assertIn("color", types)
        self.assertIn("dimension", types)

    def test_08_dtcg_parser_alias_resolution_and_hop_depth(self) -> None:
        tokens_dir = self.root / "MDS" / "02-Tokens"
        graph = DTCGTokenParser.parse_tokens_directory(tokens_dir)
        # All aliases in canonical repo must resolve and not exceed depth 2
        self.assertEqual(len(graph.unresolved_aliases), 0, f"Unresolved: {graph.unresolved_aliases}")
        self.assertEqual(len(graph.max_depth_exceeded), 0, f"Depth exceeded: {graph.max_depth_exceeded}")

    def test_09_dtcg_parser_circular_alias_detection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            tok_a = {"token_a": {"$value": "{token_b}", "$type": "color"}}
            tok_b = {"token_b": {"$value": "{token_a}", "$type": "color"}}

            (tmp_path / "a.tokens.json").write_text(json.dumps(tok_a), encoding="utf-8")
            (tmp_path / "b.tokens.json").write_text(json.dumps(tok_b), encoding="utf-8")

            graph = DTCGTokenParser.parse_tokens_directory(tmp_path)
            self.assertTrue(len(graph.cycles) > 0, "Should detect circular token dependency")

    # =========================================================================
    # 3. Python AST Safe Inspector Tests
    # =========================================================================
    def test_10_python_ast_extractor(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sample_file = Path(tmpdir) / "test_sample.py"
            sample_file.write_text(
                "import unittest\n\n"
                "class SampleTest(unittest.TestCase):\n"
                "    '''Docstring for SampleTest.'''\n"
                "    def test_feature_alpha(self):\n"
                "        self.record('MDS-TST-001', 'Test passed')\n"
                "    def test_feature_beta(self):\n"
                "        pass\n",
                encoding="utf-8",
            )
            extracted = PythonAstExtractor.inspect_file(sample_file)
            self.assertFalse(extracted.has_syntax_error)
            method_names = [m.name for m in extracted.test_methods]
            self.assertIn("test_feature_alpha", method_names)
            self.assertIn("test_feature_beta", method_names)
            self.assertIn("MDS-TST-001", extracted.asserted_capabilities)

    # =========================================================================
    # 4. Knowledge Graph & IR Schema Tests (5.1 - 5.3)
    # =========================================================================
    def test_11_knowledge_graph_node_and_edge_types(self) -> None:
        kg = KnowledgeGraph()
        n1 = GraphNode(
            canonical_id="cmp:Button",
            concept_id="COMPONENT.BUTTON",
            node_type=NodeType.COMPONENT,
            source_file="MDS/04-Components/Actions/Button.md",
            line_start=1,
            line_end=142,
            authority_tier=1,
            authority_rank=3,
        )
        n2 = GraphNode(
            canonical_id="tok:color.brand.primary",
            concept_id="TOKEN.COLOR.BRAND.PRIMARY",
            node_type=NodeType.TOKEN,
            source_file="MDS/02-Tokens/primitives/colors.tokens.json",
            line_start=1,
            line_end=10,
            authority_tier=1,
            authority_rank=2,
        )
        kg.add_node(n1)
        kg.add_node(n2)
        kg.add_edge(GraphEdge(source_id="cmp:Button", target_id="tok:color.brand.primary", edge_type=EdgeType.CONSUMES))

        self.assertEqual(len(kg.nodes), 2)
        self.assertEqual(len(kg.edges), 1)
        out_edges = kg.get_outbound_edges("cmp:Button")
        self.assertEqual(len(out_edges), 1)
        self.assertEqual(out_edges[0].target_id, "tok:color.brand.primary")
        self.assertEqual(out_edges[0].edge_type, EdgeType.CONSUMES)

    # =========================================================================
    # 5. Canonical Concept Dictionary Tests (6.1 - 6.4)
    # =========================================================================
    def test_12_concept_dictionary_pipeline(self) -> None:
        cd = ConceptDictionary()
        # Stage 1: Lexical Normalization
        norm = cd.normalize_lexical("  Container Max-Width : 1152 pixels  ")
        self.assertIn("1152 px", norm)

        # Stage 2: Concept Matching
        entry = cd.match_concept("standard container")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.concept_id, "CONTAINER.MAX_WIDTH.DEFAULT")

        # Stage 3: Value Extraction
        val = cd.extract_value("container max-width: 1152px", entry)
        self.assertEqual(val, "1152px")

        # Stage 4: Contradiction Evaluation
        has_contra, cid, v1, v2 = cd.evaluate_contradiction(
            "container max-width: 1152px",
            "container max-width: 1280px",
        )
        self.assertTrue(has_contra)
        self.assertEqual(cid, "CONTAINER.MAX_WIDTH.DEFAULT")
        self.assertEqual(v1, "1152px")
        self.assertEqual(v2, "1280px")

    # =========================================================================
    # 6. Authority Hierarchy & Intra-Tier 1 Precedence Tests (2.1 & 2.2)
    # =========================================================================
    def test_13_authority_hierarchy_and_intra_tier(self) -> None:
        # Master Spec: Tier 1, Rank 1
        t1, r1 = AuthorityManager.resolve_file_tier_and_rank("MDS/00-Master-Architecture.md")
        self.assertEqual(t1, AuthorityTier.TIER_1_CANONICAL)
        self.assertEqual(r1, AuthorityRank.RANK_1_MASTER_SPEC)

        # Tokens: Tier 1, Rank 2
        t2, r2 = AuthorityManager.resolve_file_tier_and_rank("MDS/02-Tokens/primitives/colors.tokens.json")
        self.assertEqual(t2, AuthorityTier.TIER_1_CANONICAL)
        self.assertEqual(r2, AuthorityRank.RANK_2_DTCG_TOKENS)

        # Master Spec outranks Token Data Truth in global architecture
        self.assertEqual(AuthorityManager.compare_precedence(t1, r1, t2, r2), 1)

        # Registry: Tier 2, Rank 5
        t3, r3 = AuthorityManager.resolve_file_tier_and_rank("MDS/10-Testing/capabilities/registry.json")
        self.assertEqual(t3, AuthorityTier.TIER_2_REALIZATION)
        self.assertEqual(AuthorityManager.compare_precedence(t1, r1, t3, r3), 1)

    # =========================================================================
    # 7. Invariants INV-001 through INV-012 Tests (3.1 - 3.12)
    # =========================================================================
    def test_14_inv_001_token_inventory(self) -> None:
        tokens_dir = self.root / "MDS" / "02-Tokens"
        token_graph = DTCGTokenParser.parse_tokens_directory(tokens_dir)
        findings = self.rules_engine.validate_inv_001_tokens(token_graph)
        self.assertEqual(len(findings), 0, f"INV-001 should pass on clean repo, found: {findings}")

    def test_15_inv_002_alias_integrity(self) -> None:
        tokens_dir = self.root / "MDS" / "02-Tokens"
        token_graph = DTCGTokenParser.parse_tokens_directory(tokens_dir)
        findings = self.rules_engine.validate_inv_002_aliases(token_graph)
        self.assertEqual(len(findings), 0, f"INV-002 should pass on clean repo, found: {findings}")

    def test_16_inv_003_component_inventory(self) -> None:
        findings = self.rules_engine.validate_inv_003_components()
        self.assertEqual(len(findings), 0, f"INV-003 should pass on clean repo, found: {findings}")

    def test_17_inv_004_anatomy_reconciliation(self) -> None:
        findings = self.rules_engine.validate_inv_004_anatomy()
        self.assertEqual(len(findings), 0, f"INV-004 should pass on clean repo, found: {findings}")

    def test_18_inv_005_pattern_composition_laws(self) -> None:
        findings = self.rules_engine.validate_inv_005_patterns()
        self.assertEqual(len(findings), 0, f"INV-005 should pass on clean repo, found: {findings}")

    def test_19_inv_006_workflow_fsm(self) -> None:
        findings = self.rules_engine.validate_inv_006_workflows()
        self.assertEqual(len(findings), 0, f"INV-006 should pass on clean repo, found: {findings}")

    def test_20_inv_007_container_scale(self) -> None:
        findings = self.rules_engine.validate_inv_007_templates()
        self.assertEqual(len(findings), 0, f"INV-007 should pass on clean repo, found: {findings}")

    def test_21_inv_008_enterprise_leak(self) -> None:
        discovered = self.engine.discover_files()
        findings = self.rules_engine.validate_inv_008_anti_leak(discovered["markdown"])
        self.assertEqual(len(findings), 0, f"INV-008 should find 0 enterprise leaks, found: {findings}")

    def test_22_inv_009_bipartite_coverage(self) -> None:
        findings, stats = self.rules_engine.validate_inv_009_capability_coverage()
        self.assertEqual(len(findings), 0, f"INV-009 should have 0 findings, found: {findings}")
        self.assertEqual(stats["total_capabilities"], 170)
        self.assertEqual(stats["direct_relations"], 170)
        self.assertEqual(stats["dsse_wrapped_count"], 37)
        self.assertEqual(stats["uncovered"], 0)
        self.assertEqual(stats["duplicate_covered"], 167)

    def test_23_inv_010_dsse_math_alignment(self) -> None:
        findings = self.rules_engine.validate_inv_010_dsse()
        self.assertEqual(len(findings), 0, f"INV-010 should pass on clean repo, found: {findings}")

    def test_24_inv_011_doc_index_sync(self) -> None:
        findings = self.rules_engine.validate_inv_011_doc_index()
        self.assertEqual(len(findings), 0, f"INV-011 should pass on clean repo, found: {findings}")

    def test_25_inv_012_link_integrity_support(self) -> None:
        # Test synthetic links with file URI and relative links
        with tempfile.TemporaryDirectory() as tmpdir:
            td = Path(tmpdir)
            target_f = td / "target.md"
            target_f.write_text("# Target Document\n", encoding="utf-8")

            source_f = td / "source.md"
            source_f.write_text(
                f"[Relative Link](target.md)\n"
                f"[File URI](file:///{target_f.as_posix()})\n"
                f"[Documentation Syntax Example](url)\n"
                f"[Broken Link](nonexistent.md)\n",
                encoding="utf-8",
            )

            findings = self.rules_engine.validate_inv_012_links([source_f])
            # Only broken link should be flagged
            self.assertEqual(len(findings), 1)
            self.assertIn("nonexistent.md", findings[0].description)

    # =========================================================================
    # 8. Dual-Mode Historical Document Invariant Tests (7.1 & 7.2)
    # =========================================================================
    def test_26_dual_mode_historical_validation(self) -> None:
        hist_path = self.root / "MDS" / "13-Implementation" / "Phase-9.7.7-Visual-Regression-Audit.md"
        active_path = self.root / "MDS" / "13-Implementation" / "Phase-9.7.8-Capability-Coverage-Matrix.md"

        self.assertTrue(self.rules_engine.is_historical_document(hist_path))
        self.assertFalse(self.rules_engine.is_historical_document(active_path))

    # =========================================================================
    # 9. Master Governance Engine Orchestration & Benchmark Tests (8.1 - 8.3)
    # =========================================================================
    def test_27_engine_orchestration_fast_and_full(self) -> None:
        # Fast mode: bypasses link checking for ultra-fast response
        res_fast = self.engine.audit_all(strict_mode=False, fast_mode=True)
        self.assertTrue(res_fast.is_success)
        self.assertEqual(res_fast.exit_code, 0)
        self.assertEqual(res_fast.blocker_count, 0)
        self.assertEqual(res_fast.critical_count, 0)
        self.assertIsNotNone(res_fast.telemetry)
        # Fast mode must easily meet benchmark < 500ms
        self.assertLess(res_fast.telemetry.wall_clock_ms, 500.0)

        # Full mode
        res_full = self.engine.audit_all(strict_mode=False, fast_mode=False)
        self.assertTrue(res_full.is_success)
        self.assertEqual(res_full.exit_code, 0)
        self.assertEqual(res_full.blocker_count, 0)
        self.assertEqual(res_full.critical_count, 0)

    # =========================================================================
    # 10. Reporters Tests (10.1 & 10.2)
    # =========================================================================
    def test_28_reporters_console_and_json(self) -> None:
        res = self.engine.audit_all(strict_mode=False, fast_mode=True)

        console_out = ConsoleReporter.render(res)
        self.assertIn("MASTER DESIGN SYSTEM (MDS)", console_out)
        self.assertIn("GOVERNANCE AUDIT REPORT", console_out)
        self.assertIn("Overall Status", console_out)

        serialized = JsonReporter.serialize(res)
        self.assertTrue(serialized["is_success"])
        self.assertEqual(serialized["exit_code"], 0)
        self.assertIn("telemetry", serialized)
        self.assertIn("capability_coverage", serialized)
        self.assertIn("findings", serialized)


if __name__ == "__main__":
    unittest.main()
