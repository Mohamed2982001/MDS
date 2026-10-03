#!/usr/bin/env python3
"""
MDS Responsive Viewport Automation Engine (Layer K)
Phase 9.7.6: Responsive Viewport Automation
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Public package exports for responsive viewport testing, multi-viewport sweeping,
and tri-class assertion evaluation.
"""

from .responsive_models import (
    AssertionClass,
    CanonicalViewportTier,
    ViewportDefinition,
    ResponsiveRunConfig,
    ResponsiveAssertion,
    ResponsiveRunResult,
    ResponsiveMatrixResult,
)
from .viewport_matrix import (
    VP_320,
    VP_768,
    VP_1024,
    VP_1440,
    CANONICAL_VIEWPORTS,
    CANONICAL_MATRIX_RUNS,
    get_canonical_viewports,
    get_canonical_matrix,
    get_run_config_by_id,
)
from .responsive_assertions import ResponsiveAssertionsEvaluator
from .responsive_runner import ResponsiveRunner
from .evidence import ResponsiveEvidenceGenerator
from .responsive_dispatch import (
    ResponsiveDispatcher,
    run_responsive_capability,
)

__all__ = [
    "AssertionClass",
    "CanonicalViewportTier",
    "ViewportDefinition",
    "ResponsiveRunConfig",
    "ResponsiveAssertion",
    "ResponsiveRunResult",
    "ResponsiveMatrixResult",
    "VP_320",
    "VP_768",
    "VP_1024",
    "VP_1440",
    "CANONICAL_VIEWPORTS",
    "CANONICAL_MATRIX_RUNS",
    "get_canonical_viewports",
    "get_canonical_matrix",
    "get_run_config_by_id",
    "ResponsiveAssertionsEvaluator",
    "ResponsiveRunner",
    "ResponsiveEvidenceGenerator",
    "ResponsiveDispatcher",
    "run_responsive_capability",
]
