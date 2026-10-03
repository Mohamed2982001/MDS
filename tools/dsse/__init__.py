"""
Master Design System (MDS) — Design System Selection Engine (DSSE)
Standalone operational CLI and decoupled 5-pillar mathematical evaluation package.
"""

__version__ = "1.0.0"
__author__ = "Mohamed Khalid (Senior Full Stack & Flutter Developer)"

from tools.dsse.engine import DSSEEngine, EvaluationOutput, ENGINE_VERSION
from tools.dsse.catalog import CandidateCatalog, load_candidate_catalog
from tools.dsse.analyzer import DSSEAnalyzer
from tools.dsse.explainer import DSSEExplainer
from tools.dsse.validator import (
    validate_project_profile,
    validate_candidate_catalog,
    validate_decision_tuple,
    DSSEValidationError,
)

__all__ = [
    "DSSEEngine",
    "EvaluationOutput",
    "CandidateCatalog",
    "load_candidate_catalog",
    "DSSEAnalyzer",
    "DSSEExplainer",
    "validate_project_profile",
    "validate_candidate_catalog",
    "validate_decision_tuple",
    "DSSEValidationError",
    "ENGINE_VERSION",
]
