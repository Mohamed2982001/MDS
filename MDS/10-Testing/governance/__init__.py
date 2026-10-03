"""Master Design System (MDS) — Layer M Governance & Cross-Document Consistency Engine.

Pure Python 3.12 standard-library implementation for static analysis, normalized IR knowledge graph,
semantic invariant validation, and capability coverage verification.
"""

from .engine import GovernanceEngine, GovernanceResult, FindingSeverity, GovernanceFinding
from .knowledge_graph import KnowledgeGraph, GraphNode, GraphEdge, NodeType, EdgeType
from .authority import AuthorityTier, AuthorityRank, AuthorityManager
from .concept_dictionary import ConceptDictionary, ConceptEntry
from .md_scanner import MarkdownScanner, ParseResult, ParseStatus
from .dtcg_parser import DTCGTokenParser, TokenDefinition, TokenGraph
from .reporters import ConsoleReporter, JsonReporter

__version__ = "1.0.0"
__all__ = [
    "GovernanceEngine",
    "GovernanceResult",
    "FindingSeverity",
    "GovernanceFinding",
    "KnowledgeGraph",
    "GraphNode",
    "GraphEdge",
    "NodeType",
    "EdgeType",
    "AuthorityTier",
    "AuthorityRank",
    "AuthorityManager",
    "ConceptDictionary",
    "ConceptEntry",
    "MarkdownScanner",
    "ParseResult",
    "ParseStatus",
    "DTCGTokenParser",
    "TokenDefinition",
    "TokenGraph",
    "ConsoleReporter",
    "JsonReporter",
]
