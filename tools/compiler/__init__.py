"""
Master Design System (MDS) — Production Artifact Compiler & Zero-NPM Distribution
Phase 10.3: Production Artifact Compilation & Zero-NPM Distribution
Layer 13: Implementation, Tooling & Operationalization
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Standalone, zero-dependency, deterministic compiler for MDS web runtime assets.
Built strictly with Python 3.12.x standard library (zero third-party dependencies).
"""

__version__ = "1.0.0"
__author__ = "Lead Architect Mohamed Khalid"
__all__ = [
    "models",
    "token_compiler",
    "css_bundler",
    "js_bundler",
    "manifest_generator",
    "packager",
    "validator",
    "engine",
    "cli",
]
