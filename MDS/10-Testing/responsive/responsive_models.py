#!/usr/bin/env python3
"""
MDS Responsive Domain Models & Tri-Class Assertion Taxonomy
Phase 9.7.6: Responsive Viewport Automation (Layer K)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Codifies domain models, viewports, assertion classifications, and structured execution
results adhering to ADR-070 through ADR-077.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Any, Dict, List
from pathlib import Path


class AssertionClass(str, Enum):
    """
    Tri-Class Assertion Classification (RWD-003):
    - HARD_CONTRACT: Non-negotiable structural rules. Failure = hard FAIL.
    - OBSERVABLE_BEHAVIOR: Responsive layout recompositions. Failure = hard FAIL.
    - INFORMATIONAL_MEASUREMENT: Diagnostic telemetry only. Never determines PASS/FAIL.
    """
    HARD_CONTRACT = "HARD_CONTRACT"
    OBSERVABLE_BEHAVIOR = "OBSERVABLE_BEHAVIOR"
    INFORMATIONAL_MEASUREMENT = "INFORMATIONAL_MEASUREMENT"


class CanonicalViewportTier(str, Enum):
    """
    Four Canonical Viewports defined in 03-Spacing-and-Grid.md & ADR-074.
    Invented breakpoints (e.g. 1280px) are strictly forbidden.
    """
    MOBILE = "320px"
    TABLET = "768px"
    DESKTOP = "1024px"
    WIDE = "1440px"


@dataclass(frozen=True)
class ViewportDefinition:
    """Canonical Viewport specification with explicit display metrics."""
    tier: CanonicalViewportTier
    width: int
    height: int
    device_scale_factor: float = 1.0
    is_mobile: bool = False

    @property
    def label(self) -> str:
        return f"{self.tier.value} ({self.width}x{self.height})"


@dataclass
class ResponsiveRunConfig:
    """Configuration for an isolated, deterministic execution run."""
    run_id: str
    route: str
    screen: str
    viewport: ViewportDefinition
    theme: str = "light"             # Canonical modes: 'light' | 'dark' | 'high-contrast' (identifier)
    density: str = "comfortable"      # 'comfortable' | 'compact'
    direction: str = "rtl"            # 'rtl' (default) | 'ltr'
    fresh_session: bool = False
    expected_contracts: List[str] = field(default_factory=list)

    @property
    def theme_semantic_label(self) -> str:
        """Canonical semantic name (Light | Dark | High Contrast)."""
        if self.theme in ("high-contrast", "contrast"):
            return "High Contrast"
        elif self.theme == "dark":
            return "Dark"
        return "Light"


@dataclass
class ResponsiveAssertion:
    """Discrete assertion record evaluated against live browser DOM."""
    run_id: str
    capability_id: str
    screen: str
    viewport_tier: str
    dimension: str
    assertion_class: AssertionClass
    selector: str
    assertion_name: str
    passed: bool
    expected: Any
    actual: Any
    diagnostics: Optional[str] = None
    evidence: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "capability_id": self.capability_id,
            "screen": self.screen,
            "viewport_tier": self.viewport_tier,
            "dimension": self.dimension,
            "assertion_class": self.assertion_class.value,
            "selector": self.selector,
            "assertion_name": self.assertion_name,
            "passed": self.passed,
            "expected": str(self.expected),
            "actual": str(self.actual),
            "diagnostics": self.diagnostics,
            "evidence": self.evidence,
        }


@dataclass
class ResponsiveRunResult:
    """Aggregated result of a single run configuration."""
    run_id: str
    config: ResponsiveRunConfig
    passed: bool
    assertions: List[ResponsiveAssertion] = field(default_factory=list)
    duration_ms: float = 0.0
    error_message: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)

    @property
    def hard_failures(self) -> List[ResponsiveAssertion]:
        return [
            a for a in self.assertions
            if not a.passed and a.assertion_class in (AssertionClass.HARD_CONTRACT, AssertionClass.OBSERVABLE_BEHAVIOR)
        ]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "screen": self.config.screen,
            "route": self.config.route,
            "viewport": self.config.viewport.label,
            "theme": self.config.theme_semantic_label,
            "theme_identifier": self.config.theme,
            "density": self.config.density,
            "direction": self.config.direction,
            "passed": self.passed,
            "duration_ms": self.duration_ms,
            "error_message": self.error_message,
            "total_assertions": len(self.assertions),
            "hard_failures": len(self.hard_failures),
            "assertions": [a.to_dict() for a in self.assertions],
            "metrics": self.metrics,
        }


@dataclass
class ResponsiveMatrixResult:
    """Master result containing all runs of the Canonical 17-Run Matrix."""
    capability_id: str
    status: str                         # 'PASS' | 'FAIL' | 'DEFERRED'
    runs: List[ResponsiveRunResult] = field(default_factory=list)
    total_assertions: int = 0
    passed_assertions: int = 0
    failed_assertions: int = 0
    hard_failures: int = 0
    duration_ms: float = 0.0
    browser_version: Optional[str] = None
    evidence: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    exception_type: Optional[str] = None

    @property
    def is_pass(self) -> bool:
        return self.status == "PASS"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "status": self.status,
            "total_runs": len(self.runs),
            "total_assertions": self.total_assertions,
            "passed_assertions": self.passed_assertions,
            "failed_assertions": self.failed_assertions,
            "hard_failures": self.hard_failures,
            "duration_ms": self.duration_ms,
            "browser_version": self.browser_version,
            "error_message": self.error_message,
            "exception_type": self.exception_type,
            "runs": [r.to_dict() for r in self.runs],
            "evidence": self.evidence,
        }
