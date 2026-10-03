"""
Master Design System (MDS) — Compiler Domain Models & Architectural Constants
Phase 10.3: Production Artifact Compilation & Zero-NPM Distribution
Layer 13: Implementation, Tooling & Operationalization
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import dataclasses
from typing import Any, Dict, List, Optional, Tuple


# ==============================================================================
# Domain Exceptions & Exit Code Taxonomy
# ==============================================================================

class CompilerError(Exception):
    """Base exception for all compiler pipeline errors."""
    def __init__(self, message: str, exit_code: int = 4):
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code


class SourceValidationError(CompilerError):
    """Raised when source validation fails (Exit 2)."""
    def __init__(self, message: str):
        super().__init__(message, exit_code=2)


class ContractViolationError(CompilerError):
    """Raised when an architectural or distribution contract is violated (Exit 2)."""
    def __init__(self, message: str):
        super().__init__(message, exit_code=2)


class IntegrityViolationError(CompilerError):
    """Raised when cryptographic integrity checks or trust bindings fail (Exit 3)."""
    def __init__(self, message: str):
        super().__init__(message, exit_code=3)


class CompilerScopeViolationError(CompilerError):
    """Raised when an unapproved file or protected non-source is accessed (Exit 3)."""
    def __init__(self, message: str):
        super().__init__(message, exit_code=3)


class ConfigurationError(CompilerError):
    """Raised when configuration, environment, or command parameters are invalid (Exit 4)."""
    def __init__(self, message: str):
        super().__init__(message, exit_code=4)


# ==============================================================================
# Inviolable Architectural Constants
# ==============================================================================

ROOT_TRUST_ANCHOR_FINGERPRINT = "20c240e650a447299690d0e2f65c65a0dbed2acc4aba9de9997c4a093f2ed114"
AUTHORITATIVE_SOURCE_MANIFEST_DIGEST = "bc77421d30408375ad4c197cfa2db12dbaa18b395bd06928da64bbc3f41c5744"
AUTHORITATIVE_SOURCE_IDENTITY_HASH = "34cd5128a6258cdfb09bed3f0002eaf9910610bc8ebf3fda16034cef6a815a73"

SUPPORTED_PYTHON_MAJOR_MINOR = (3, 12)
PACKAGE_NAME = "master-design-system"
MDS_VERSION = "1.0.0"
COMPILER_VERSION = "1.0.0"
SCHEMA_VERSION = "1.0.0"

CANONICAL_SOURCE_COUNT = 61
CANONICAL_NON_SOURCE_COUNT = 33
CANONICAL_PROTECTED_CORE_COUNT = 94


# ==============================================================================
# Exact Canonical Compilation Sources (61 Files — ADR-207 REV4)
# ==============================================================================

CANONICAL_COMPILATION_SOURCES: frozenset[str] = frozenset([
    # DTCG Tokens (18 files)
    "MDS/02-Tokens/components/badge.tokens.json",
    "MDS/02-Tokens/components/button.tokens.json",
    "MDS/02-Tokens/components/input.tokens.json",
    "MDS/02-Tokens/primitives/color.tokens.json",
    "MDS/02-Tokens/primitives/elevation.tokens.json",
    "MDS/02-Tokens/primitives/layer.tokens.json",
    "MDS/02-Tokens/primitives/motion.tokens.json",
    "MDS/02-Tokens/primitives/opacity.tokens.json",
    "MDS/02-Tokens/primitives/shape.tokens.json",
    "MDS/02-Tokens/primitives/size.tokens.json",
    "MDS/02-Tokens/primitives/space.tokens.json",
    "MDS/02-Tokens/primitives/typography.tokens.json",
    "MDS/02-Tokens/semantic/color.tokens.json",
    "MDS/02-Tokens/semantic/space.tokens.json",
    "MDS/02-Tokens/themes/density.compact.tokens.json",
    "MDS/02-Tokens/themes/mode.dark.tokens.json",
    "MDS/02-Tokens/themes/mode.high-contrast.tokens.json",
    "MDS/02-Tokens/themes/preset.refined.tokens.json",
    # Foundation Stylesheets (4 files)
    "MDS/Runtime/css/foundations.css",
    "MDS/Runtime/css/mds-core.css",
    "MDS/Runtime/css/primitives.css",
    "MDS/Runtime/css/reset.css",
    # Primitive Layout & Interaction Styles (12 files)
    "MDS/Runtime/primitives/icon/icon.css",
    "MDS/Runtime/primitives/interaction/focus-ring.css",
    "MDS/Runtime/primitives/interaction/press-target.css",
    "MDS/Runtime/primitives/interaction/reduced-motion.css",
    "MDS/Runtime/primitives/interaction/visually-hidden.css",
    "MDS/Runtime/primitives/layout/cluster.css",
    "MDS/Runtime/primitives/layout/container.css",
    "MDS/Runtime/primitives/layout/grid.css",
    "MDS/Runtime/primitives/layout/inline.css",
    "MDS/Runtime/primitives/layout/stack.css",
    "MDS/Runtime/primitives/surface/surface.css",
    "MDS/Runtime/primitives/typography/typography.css",
    # Primitive JavaScript (2 files)
    "MDS/Runtime/primitives/interaction/focus-trap.js",
    "MDS/Runtime/primitives/interaction/live-region.js",
    # Component Styles (20 files)
    "MDS/Runtime/components/alert/alert.css",
    "MDS/Runtime/components/badge/badge.css",
    "MDS/Runtime/components/button/button.css",
    "MDS/Runtime/components/card/card.css",
    "MDS/Runtime/components/checkbox/checkbox.css",
    "MDS/Runtime/components/components.css",
    "MDS/Runtime/components/dialog/dialog.css",
    "MDS/Runtime/components/field/field.css",
    "MDS/Runtime/components/icon-button/icon-button.css",
    "MDS/Runtime/components/input/input.css",
    "MDS/Runtime/components/link/link.css",
    "MDS/Runtime/components/radio/radio.css",
    "MDS/Runtime/components/select/select.css",
    "MDS/Runtime/components/skeleton/skeleton.css",
    "MDS/Runtime/components/spinner/spinner.css",
    "MDS/Runtime/components/switch/switch.css",
    "MDS/Runtime/components/table/table.css",
    "MDS/Runtime/components/tabs/tabs.css",
    "MDS/Runtime/components/textarea/textarea.css",
    "MDS/Runtime/components/tooltip/tooltip.css",
    # Component JavaScript (5 files)
    "MDS/Runtime/components/components.js",
    "MDS/Runtime/components/dialog/dialog.js",
    "MDS/Runtime/components/switch/switch.js",
    "MDS/Runtime/components/tabs/tabs.js",
    "MDS/Runtime/components/tooltip/tooltip.js",
])


# ==============================================================================
# Exact Canonical Protected Non-Sources (33 Files — ADR-207 REV4)
# ==============================================================================

CANONICAL_PROTECTED_NON_SOURCES: frozenset[str] = frozenset([
    "MDS/02-Tokens/MDS-Token-Architecture.md",
    "MDS/Playground/README.md",
    "MDS/Playground/fixtures/sample_data.json",
    "MDS/Playground/index.html",
    "MDS/Playground/playground.css",
    "MDS/Playground/playground.js",
    "MDS/Playground/tests/__init__.py",
    "MDS/Playground/tests/test_playground.py",
    "MDS/Reference-Application/README.md",
    "MDS/Reference-Application/app.css",
    "MDS/Reference-Application/app.js",
    "MDS/Reference-Application/fixtures/workspace_data.json",
    "MDS/Reference-Application/index.html",
    "MDS/Reference-Application/tests/__init__.py",
    "MDS/Reference-Application/tests/test_reference_app.py",
    "MDS/Runtime/components/README.md",
    "MDS/Runtime/components/tests/test_components_runtime.py",
    "MDS/Runtime/primitives/README.md",
    "MDS/Runtime/primitives/tests/__init__.py",
    "MDS/Runtime/primitives/tests/test_primitives_runtime.py",
    "MDS/Runtime/tokens/README.md",
    "MDS/Runtime/tokens/compile_tokens.py",
    "MDS/Runtime/tokens/dist/tokens.css",
    "MDS/Runtime/tokens/dist/tokens.d.ts",
    "MDS/Runtime/tokens/dist/tokens.json",
    "MDS/Runtime/tokens/src/__init__.py",
    "MDS/Runtime/tokens/src/compiler.py",
    "MDS/Runtime/tokens/src/loader.py",
    "MDS/Runtime/tokens/src/models.py",
    "MDS/Runtime/tokens/src/resolver.py",
    "MDS/Runtime/tokens/src/validator.py",
    "MDS/Runtime/tokens/tests/__init__.py",
    "MDS/Runtime/tokens/tests/test_token_runtime.py",
])


def canonical_stream_sha256(data: bytes) -> str:
    """
    Computes SHA-256 over cross-platform canonical normalized text
    (ADR-106 / ADR-211: BOM stripped, CRLF -> LF, UTF-8 encoded).
    """
    import hashlib
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    normalized = data.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return hashlib.sha256(normalized).hexdigest()


# ==============================================================================
# Configuration & Identity Data Classes
# ==============================================================================

@dataclasses.dataclass(frozen=True)
class BuildConfig:
    reproducible_mode: bool
    build_epoch: Optional[int]
    css_layer_order: Tuple[str, ...] = (
        "mds.reset",
        "mds.tokens",
        "mds.foundations",
        "mds.primitives",
        "mds.components",
        "mds.themes",
    )
    line_ending_mode: str = "LF"
    zip_compression_level: int = 9
    tar_compression_level: int = 9
    archive_permissions: Dict[str, str] = dataclasses.field(
        default_factory=lambda: {"file": "0644", "dir": "0755"}
    )
    archive_ownership: Dict[str, Any] = dataclasses.field(
        default_factory=lambda: {"uid": 0, "gid": 0, "uname": "root", "gname": "root"}
    )
    strip_zip_extra: bool = True
    theme_matrix: Tuple[str, ...] = (
        "mode.dark",
        "mode.high-contrast",
        "density.compact",
        "preset.refined",
    )

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "archive_ownership": self.archive_ownership,
            "archive_permissions": self.archive_permissions,
            "css_layer_order": list(self.css_layer_order),
            "line_ending_mode": self.line_ending_mode,
            "reproducible_mode": self.reproducible_mode,
            "strip_zip_extra": self.strip_zip_extra,
            "tar_compression_level": self.tar_compression_level,
            "theme_matrix": list(self.theme_matrix),
            "zip_compression_level": self.zip_compression_level,
        }


@dataclasses.dataclass(frozen=True)
class EnvironmentContract:
    python_runtime_major_minor: str = "3.12"
    archive_engine: str = "stdlib.zipfile+stdlib.tarfile"
    filesystem_sort_order: str = "posix_codepoint_utf8"
    locale_normalization: str = "C.UTF-8"
    newline_convention: str = "LF"
    text_encoding: str = "utf-8"
    timezone_normalization: str = "UTC"

    def canonical_dict(self) -> Dict[str, str]:
        return {
            "archive_engine": self.archive_engine,
            "filesystem_sort_order": self.filesystem_sort_order,
            "locale_normalization": self.locale_normalization,
            "newline_convention": self.newline_convention,
            "python_runtime_major_minor": self.python_runtime_major_minor,
            "text_encoding": self.text_encoding,
            "timezone_normalization": self.timezone_normalization,
        }


@dataclasses.dataclass
class BuildIdentity:
    source_identity: str
    compiler_identity: str
    build_config_identity: str
    build_env_identity: str
    build_epoch: Optional[int]
    build_id: str
    release_identity: str
    artifacts: Dict[str, Dict[str, Any]]


@dataclasses.dataclass
class VerificationResult:
    status: str
    exit_code: int
    message: str
    details: Dict[str, Any] = dataclasses.field(default_factory=dict)
