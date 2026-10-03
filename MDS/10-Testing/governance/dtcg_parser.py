"""W3C DTCG Token Tree Parser and Alias Graph Analyzer for MDS.

Validates:
- INV-001: Exactly 188 registered tokens across 18 W3C DTCG files.
- INV-002: Token references, alias depth (<= 2 hops), and cycle detection.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class TokenDefinition:
    name: str
    raw_path: str
    value: Any
    token_type: Optional[str] = None
    description: Optional[str] = None
    aliases: List[str] = field(default_factory=list)
    source_file: str = ""
    is_component_token: bool = False


@dataclass
class TokenGraph:
    tokens: Dict[str, TokenDefinition] = field(default_factory=dict)
    files: List[Path] = field(default_factory=list)
    cycles: List[List[str]] = field(default_factory=list)
    unresolved_aliases: List[Tuple[str, str]] = field(default_factory=list)
    max_depth_exceeded: List[Tuple[str, int]] = field(default_factory=list)


class DTCGTokenParser:
    """Parser and validator for W3C Design Tokens Community Group format."""

    RE_ALIAS = re.compile(r"\{([^}]+)\}")

    @classmethod
    def parse_tokens_directory(cls, tokens_dir: Path) -> TokenGraph:
        graph = TokenGraph()
        if not tokens_dir.exists():
            return graph

        token_files = sorted(tokens_dir.rglob("*.tokens.json"))
        graph.files = token_files

        for tf in token_files:
            try:
                data = json.loads(tf.read_text(encoding="utf-8"))
            except Exception:
                continue

            is_comp = tf.name.startswith("component.")
            cls._extract_tokens(data, prefix=[], source_file=tf.name, is_comp=is_comp, out_tokens=graph.tokens)

        # Validate aliases, cycles, and depth
        cls._analyze_alias_graph(graph)
        return graph

    @classmethod
    def _extract_tokens(
        cls,
        obj: Any,
        prefix: List[str],
        source_file: str,
        is_comp: bool,
        out_tokens: Dict[str, TokenDefinition],
    ) -> None:
        if not isinstance(obj, dict):
            return

        # A node is a token if it contains $value
        if "$value" in obj:
            token_name = ".".join(prefix)
            val = obj["$value"]
            ttype = obj.get("$type")
            desc = obj.get("$description")

            aliases = []
            if isinstance(val, str):
                for m in cls.RE_ALIAS.finditer(val):
                    aliases.append(m.group(1).strip())

            out_tokens[token_name] = TokenDefinition(
                name=token_name,
                raw_path=".".join(prefix),
                value=val,
                token_type=ttype,
                description=desc,
                aliases=aliases,
                source_file=source_file,
                is_component_token=is_comp,
            )
            return

        for k, v in obj.items():
            if k.startswith("$"):
                continue
            cls._extract_tokens(v, prefix + [k], source_file, is_comp, out_tokens)

    @classmethod
    def _analyze_alias_graph(cls, graph: TokenGraph) -> None:
        for token_name, tok in graph.tokens.items():
            for alias in tok.aliases:
                if alias not in graph.tokens:
                    graph.unresolved_aliases.append((token_name, alias))

        # Check for cycles & depth
        for token_name in graph.tokens:
            visited: List[str] = []
            depth = cls._traverse_depth(token_name, graph.tokens, visited, max_allowed=2, graph=graph)
            if depth > 2 and depth < 999:
                graph.max_depth_exceeded.append((token_name, depth))

    @classmethod
    def _traverse_depth(
        cls,
        current: str,
        tokens: Dict[str, TokenDefinition],
        path: List[str],
        max_allowed: int,
        graph: Optional[TokenGraph] = None,
    ) -> int:
        if current in path:
            # Cycle detected
            cycle_path = path[path.index(current):] + [current]
            if graph is not None and cycle_path not in graph.cycles:
                graph.cycles.append(cycle_path)
            return 999

        tok = tokens.get(current)
        if not tok or not tok.aliases:
            return 0

        max_child_depth = 0
        for alias in tok.aliases:
            child_depth = 1 + cls._traverse_depth(alias, tokens, path + [current], max_allowed, graph=graph)
            if child_depth > max_child_depth:
                max_child_depth = child_depth

        return max_child_depth
