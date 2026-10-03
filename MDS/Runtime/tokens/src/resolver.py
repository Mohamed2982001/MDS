"""
MDS Token Runtime Engine — Token Resolver & DAG Constructor
Phase 9.2: Token Runtime Engine

Constructs token dependency graph, detects circular references, enforces 3-hop limit,
and resolves aliases down to terminal primitive values.
"""

import re
from typing import Any, Dict, List, Optional, Set, Tuple

from .models import (
    AliasDepthExceededError,
    CycleDetectedError,
    MissingTokenError,
    ResolvedToken,
    ThemeOverride,
    Token,
)


def token_path_to_css_var(path: str) -> str:
    """
    Converts a dotted token path to a standard kebab-case CSS custom property name.
    Handles camelCase segments (e.g. lineHeight -> line-height, focusRing -> focus-ring).
    Prefixed strictly with '--mds-'.

    Examples:
        color.brand.600 -> --mds-color-brand-600
        font.lineHeight.normal -> --mds-font-line-height-normal
        component.button.primary.focusRing -> --mds-component-button-primary-focus-ring
    """
    parts = path.split(".")
    kebab_parts = []
    for part in parts:
        # Convert camelCase to kebab-case
        s = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", part).lower()
        kebab_parts.append(s)
    return f"--mds-{'-'.join(kebab_parts)}"


def format_css_value(value: Any, token_type: str = "") -> str:
    """
    Formats a resolved Python data structure into a valid CSS property value string.
    """
    if token_type == "cubicBezier" or (isinstance(value, list) and len(value) == 4 and all(isinstance(x, (int, float)) for x in value)):
        return f"cubic-bezier({value[0]}, {value[1]}, {value[2]}, {value[3]})"
    
    if token_type == "shadow" or (isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict)):
        # Check for level 0 flat elevation / transparent shadow
        if len(value) == 1:
            item = value[0]
            if (
                item.get("offsetX") == "0px"
                and item.get("offsetY") == "0px"
                and item.get("blur") == "0px"
                and item.get("spread") == "0px"
                and ("rgba(0, 0, 0, 0)" in item.get("color", "") or "transparent" in item.get("color", ""))
            ):
                return "none"
        
        layers = []
        for item in value:
            ox = item.get("offsetX", "0px")
            oy = item.get("offsetY", "0px")
            blur = item.get("blur", "0px")
            spread = item.get("spread", "0px")
            color = item.get("color", "#000000")
            layers.append(f"{ox} {oy} {blur} {spread} {color}")
        return ", ".join(layers)

    if isinstance(value, (int, float)):
        return str(value)
    
    return str(value)


class TokenResolver:
    """Constructs DAG, detects cycles, enforces max depth, and resolves token aliases."""

    def __init__(
        self,
        base_tokens: Dict[str, Token],
        theme_overrides: Dict[str, ThemeOverride],
        all_tokens: Dict[str, Token],
        max_depth: int = 3
    ):
        self.base_tokens = base_tokens
        self.theme_overrides = theme_overrides
        self.all_tokens = all_tokens
        self.max_depth = max_depth

    def _build_dependency_graph(self, tokens: Dict[str, Token]) -> Dict[str, List[str]]:
        """Constructs an adjacency list mapping each token to its referenced targets."""
        graph: Dict[str, List[str]] = {path: [] for path in tokens}
        for path, token in tokens.items():
            if token.is_alias:
                target = token.alias_target
                if target:
                    graph[path].append(target)
        return graph

    def check_circular_references(self, tokens: Dict[str, Token]) -> None:
        """
        Detects circular dependencies using depth-first cycle traversal.
        Raises CycleDetectedError with the full cycle path if any loop is detected.
        """
        graph = self._build_dependency_graph(tokens)
        visited: Set[str] = set()
        recursion_stack: List[str] = []

        def dfs(node: str):
            visited.add(node)
            recursion_stack.append(node)

            for neighbor in graph.get(node, []):
                if neighbor in recursion_stack:
                    # Found cycle: extract path slice from neighbor to end + [neighbor]
                    cycle_start = recursion_stack.index(neighbor)
                    cycle_path = recursion_stack[cycle_start:] + [neighbor]
                    raise CycleDetectedError(cycle_path)
                if neighbor not in visited and neighbor in graph:
                    dfs(neighbor)

            recursion_stack.pop()

        for node in sorted(graph.keys()):
            if node not in visited:
                dfs(node)

    def resolve_token_chain(
        self,
        start_path: str,
        token_lookup: Dict[str, Token]
    ) -> Tuple[Any, Optional[str], List[str], int, str]:
        """
        Resolves a token through its alias chain.

        Returns:
            Tuple of:
            - terminal_value: Any
            - resolved_from: Optional[str] (immediate alias target)
            - resolution_chain: List[str] (sequence of paths visited)
            - hops: int (number of alias dereferences)
            - terminal_type: str
        """
        if start_path not in token_lookup:
            raise MissingTokenError(start_path, start_path)

        chain: List[str] = [start_path]
        curr_token = token_lookup[start_path]
        terminal_type = curr_token.type
        hops = 0
        resolved_from: Optional[str] = None

        while curr_token.is_alias:
            target = curr_token.alias_target
            if resolved_from is None:
                resolved_from = target

            if target in chain:
                cycle_path = chain[chain.index(target):] + [target]
                raise CycleDetectedError(cycle_path)

            chain.append(target)
            hops += 1

            if hops > self.max_depth:
                raise AliasDepthExceededError(
                    token_path=start_path,
                    depth=hops,
                    max_depth=self.max_depth,
                    chain=chain
                )

            if target not in token_lookup:
                raise MissingTokenError(curr_token.path, target)

            curr_token = token_lookup[target]
            if curr_token.type and curr_token.type != "unknown":
                terminal_type = curr_token.type

        terminal_value = curr_token.raw_value
        return terminal_value, resolved_from, chain, hops, terminal_type

    def resolve_all(self) -> Tuple[Dict[str, ResolvedToken], Dict[str, Dict[str, ResolvedToken]]]:
        """
        Resolves all base tokens and theme override tokens.

        Returns:
            Tuple of:
            - base_resolved: Dict[token_path, ResolvedToken]
            - theme_resolved: Dict[theme_id, Dict[token_path, ResolvedToken]]
        """
        # 1. Global cycle detection on all registered tokens
        self.check_circular_references(self.all_tokens)

        # 2. Resolve Base Tokens
        base_resolved: Dict[str, ResolvedToken] = {}
        for path in sorted(self.base_tokens.keys()):
            token = self.base_tokens[path]
            val, resolved_from, chain, hops, t_type = self.resolve_token_chain(path, self.all_tokens)
            css_val = format_css_value(val, t_type)
            css_var = token_path_to_css_var(path)

            base_resolved[path] = ResolvedToken(
                path=path,
                value=val,
                css_value=css_val,
                css_var_name=css_var,
                type=t_type,
                tier=token.layer,
                resolved_from=resolved_from,
                resolution_chain=chain,
                hops=hops,
                description=token.description
            )

        # 3. Resolve Theme Overrides
        theme_resolved: Dict[str, Dict[str, ResolvedToken]] = {}
        for theme_id, theme_override in sorted(self.theme_overrides.items()):
            theme_resolved[theme_id] = {}
            # Context dictionary: theme-specific tokens take precedence over base/all tokens
            context_lookup = {**self.all_tokens, **theme_override.tokens}
            
            # Check for circularity within theme context
            self.check_circular_references(context_lookup)

            for path in sorted(theme_override.tokens.keys()):
                theme_token = theme_override.tokens[path]
                val, resolved_from, chain, hops, t_type = self.resolve_token_chain(path, context_lookup)
                css_val = format_css_value(val, t_type)
                css_var = token_path_to_css_var(path)

                theme_resolved[theme_id][path] = ResolvedToken(
                    path=path,
                    value=val,
                    css_value=css_val,
                    css_var_name=css_var,
                    type=t_type,
                    tier="theme",
                    resolved_from=resolved_from,
                    resolution_chain=chain,
                    hops=hops,
                    description=theme_token.description
                )

        return base_resolved, theme_resolved
