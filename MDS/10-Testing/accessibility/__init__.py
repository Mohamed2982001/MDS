#!/usr/bin/env python3
"""
MDS Dynamic Accessibility Engine (axe-core)
Phase 9.7.5: Dynamic Accessibility Automation (Layer I)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from .accessibility_models import (
    AccessibilityImpact,
    AccessibilityNode,
    AccessibilityViolation,
    AccessibilityIncomplete,
    AccessibilityPass,
    AccessibilityPolicy,
    AccessibilityResult,
)
from .axe_loader import (
    AxeArtifact,
    AxeLoader,
    AxeArtifactNotFoundError,
    AxeIntegrityError,
)
from .axe_runner import AxeRunner
from .evidence import AccessibilityEvidenceGenerator
from .accessibility_dispatch import (
    AccessibilityDispatcher,
    run_accessibility_capability,
)

__all__ = [
    "AccessibilityImpact",
    "AccessibilityNode",
    "AccessibilityViolation",
    "AccessibilityIncomplete",
    "AccessibilityPass",
    "AccessibilityPolicy",
    "AccessibilityResult",
    "AxeArtifact",
    "AxeLoader",
    "AxeArtifactNotFoundError",
    "AxeIntegrityError",
    "AxeRunner",
    "AccessibilityEvidenceGenerator",
    "AccessibilityDispatcher",
    "run_accessibility_capability",
]
