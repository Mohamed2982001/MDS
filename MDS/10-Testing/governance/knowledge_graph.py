"""Normalized Intermediate Representation (IR) & Directed Knowledge Graph for MDS.

Implements the 12 Node Types, 10 Edge Types, and mandatory node metadata
codified in ADR-098 and Phase 9.7.8 Architecture Section 5.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple


class NodeType(str, Enum):
    DOCUMENT = "DOCUMENT"
    TOKEN = "TOKEN"
    PRIMITIVE = "PRIMITIVE"
    COMPONENT = "COMPONENT"
    PATTERN = "PATTERN"
    WORKFLOW = "WORKFLOW"
    TEMPLATE = "TEMPLATE"
    FSM_STATE = "FSM_STATE"
    CAPABILITY = "CAPABILITY"
    DECISION = "DECISION"
    TEST = "TEST"
    RUNTIME_ARTIFACT = "RUNTIME_ARTIFACT"


class EdgeType(str, Enum):
    DEFINES = "DEFINES"
    REFERENCES = "REFERENCES"
    IMPLEMENTS = "IMPLEMENTS"
    DERIVES_FROM = "DERIVES_FROM"
    VALIDATES = "VALIDATES"
    PROJECTS_TO = "PROJECTS_TO"
    CONSUMES = "CONSUMES"
    CONFLICTS_WITH = "CONFLICTS_WITH"
    SUPERSEDES = "SUPERSEDES"
    TRANSITIONS_TO = "TRANSITIONS_TO"


@dataclass
class GraphNode:
    canonical_id: str
    concept_id: str
    node_type: NodeType
    source_file: str
    line_start: int
    line_end: int
    authority_tier: int
    authority_rank: int
    version: str = "1.0.0"
    lifecycle_status: str = "ACTIVE"
    raw_evidence: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphEdge:
    source_id: str
    target_id: str
    edge_type: EdgeType
    attributes: Dict[str, Any] = field(default_factory=dict)


class KnowledgeGraph:
    """Directed multi-graph representing the normalized state of the design system."""

    def __init__(self) -> None:
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []
        self._outbound: Dict[str, List[GraphEdge]] = {}
        self._inbound: Dict[str, List[GraphEdge]] = {}

    def add_node(self, node: GraphNode) -> None:
        self.nodes[node.canonical_id] = node
        if node.canonical_id not in self._outbound:
            self._outbound[node.canonical_id] = []
        if node.canonical_id not in self._inbound:
            self._inbound[node.canonical_id] = []

    def add_edge(self, edge: GraphEdge) -> None:
        self.edges.append(edge)
        self._outbound.setdefault(edge.source_id, []).append(edge)
        self._inbound.setdefault(edge.target_id, []).append(edge)

    def get_node(self, canonical_id: str) -> Optional[GraphNode]:
        return self.nodes.get(canonical_id)

    def get_nodes_by_type(self, node_type: NodeType) -> List[GraphNode]:
        return [n for n in self.nodes.values() if n.node_type == node_type]

    def get_outbound_edges(self, node_id: str, edge_type: Optional[EdgeType] = None) -> List[GraphEdge]:
        edges = self._outbound.get(node_id, [])
        if edge_type:
            return [e for e in edges if e.edge_type == edge_type]
        return edges

    def get_inbound_edges(self, node_id: str, edge_type: Optional[EdgeType] = None) -> List[GraphEdge]:
        edges = self._inbound.get(node_id, [])
        if edge_type:
            return [e for e in edges if e.edge_type == edge_type]
        return edges

    def find_contradictions(self) -> List[Tuple[GraphNode, GraphNode, str]]:
        """Finds pairs of nodes with the same concept_id but conflicting canonical values."""
        contradictions = []
        concept_map: Dict[str, List[GraphNode]] = {}
        for node in self.nodes.values():
            if node.concept_id and node.concept_id != "NONE":
                concept_map.setdefault(node.concept_id, []).append(node)

        for concept_id, group in concept_map.items():
            if len(group) > 1:
                # Compare canonical values
                baseline = group[0]
                for other in group[1:]:
                    val_a = baseline.attributes.get("canonical_value")
                    val_b = other.attributes.get("canonical_value")
                    if val_a is not None and val_b is not None and val_a != val_b:
                        contradictions.append(
                            (baseline, other, f"Contradiction on concept {concept_id}: '{val_a}' vs '{val_b}'")
                        )
        return contradictions
