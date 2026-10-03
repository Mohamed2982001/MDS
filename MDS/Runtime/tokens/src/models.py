"""
MDS Token Runtime Engine — Models & Exceptions
Phase 9.2: Token Runtime Engine
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class TokenRuntimeError(Exception):
    """Base exception for all Token Runtime Engine errors."""
    pass


class CycleDetectedError(TokenRuntimeError):
    """Raised when a circular reference is detected in token aliases."""
    def __init__(self, cycle_path: List[str]):
        self.cycle_path = cycle_path
        super().__init__(f"Circular reference detected: {' -> '.join(cycle_path)}")


class AliasDepthExceededError(TokenRuntimeError):
    """Raised when token alias resolution exceeds the maximum allowable hop limit."""
    def __init__(self, token_path: str, depth: int, max_depth: int, chain: List[str]):
        self.token_path = token_path
        self.depth = depth
        self.max_depth = max_depth
        self.chain = chain
        super().__init__(
            f"Token '{token_path}' exceeded maximum alias depth of {max_depth} hops (actual: {depth}): "
            f"{' -> '.join(chain)}"
        )


class MissingTokenError(TokenRuntimeError):
    """Raised when an alias references a non-existent token target."""
    def __init__(self, source_token: str, missing_target: str):
        self.source_token = source_token
        self.missing_target = missing_target
        super().__init__(f"Token '{source_token}' references non-existent target '{missing_target}'")


class SchemaValidationError(TokenRuntimeError):
    """Raised when token definitions violate DTCG schema requirements."""
    pass


@dataclass
class Token:
    """Represents an un-resolved Design Token loaded from DTCG JSON."""
    path: str
    raw_value: Any
    type: str
    description: str = ""
    layer: str = "primitive"  # primitive, semantic, component, theme
    file_path: Optional[Path] = None
    extensions: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_alias(self) -> bool:
        """Determines if the raw value is a DTCG alias reference ({path.to.token})."""
        return (
            isinstance(self.raw_value, str)
            and self.raw_value.startswith("{")
            and self.raw_value.endswith("}")
        )

    @property
    def alias_target(self) -> Optional[str]:
        """Returns the unbracketed target token path if this is an alias."""
        if self.is_alias:
            return self.raw_value[1:-1].strip()
        return None


@dataclass
class ResolvedToken:
    """Represents a fully resolved Design Token ready for compilation."""
    path: str
    value: Any
    css_value: str
    css_var_name: str
    type: str
    tier: str
    resolved_from: Optional[str] = None
    resolution_chain: List[str] = field(default_factory=list)
    hops: int = 0
    description: str = ""


@dataclass
class ThemeOverride:
    """Represents a scoped theme override set."""
    theme_id: str
    selector: str
    file_path: Path
    description: str
    tokens: Dict[str, Token] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Results of DTCG schema and inventory validation."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class CompileResult:
    """Compilation bundle containing all emitted runtime artifacts."""
    css: str
    json_data: Dict[str, Any]
    dts: str
    base_resolved: Dict[str, ResolvedToken]
    theme_resolved: Dict[str, Dict[str, ResolvedToken]]
    stats: Dict[str, Any]
