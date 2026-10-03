#!/usr/bin/env python3
"""
Accessibility Models & Evaluation Policy
Phase 9.7.5: Dynamic Accessibility Automation (Layer I)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Defines strongly-typed data structures for axe-core results, violation summaries,
affected nodes, severity classification, and accessibility pass/fail policies.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple

from browser.models import BrowserExecutionStatus, Viewport


class AccessibilityImpact(str, Enum):
    """WCAG violation severity levels classified by axe-core."""
    CRITICAL = "critical"
    SERIOUS = "serious"
    MODERATE = "moderate"
    MINOR = "minor"


@dataclass
class AccessibilityNode:
    """Represents a specific DOM element affected by an accessibility rule."""
    target: List[str]
    html: str
    failure_summary: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target": self.target,
            # Prevent uncontrolled HTML dump; clamp at 200 characters
            "html": (self.html[:197] + "...") if len(self.html) > 200 else self.html,
            "failure_summary": self.failure_summary
        }


@dataclass
class AccessibilityViolation:
    """Structured representation of an axe-core accessibility violation."""
    id: str
    impact: str
    description: str
    help: str
    help_url: str
    tags: List[str] = field(default_factory=list)
    nodes: List[AccessibilityNode] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "impact": self.impact,
            "description": self.description,
            "help": self.help,
            "helpUrl": self.help_url,
            "tags": self.tags,
            "nodes": [n.to_dict() for n in self.nodes],
            "nodes_count": len(self.nodes)
        }


@dataclass
class AccessibilityIncomplete:
    """Incomplete/ambiguous accessibility test item requiring manual review."""
    id: str
    impact: Optional[str]
    description: str
    help: str
    help_url: str
    tags: List[str] = field(default_factory=list)
    nodes_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "impact": self.impact,
            "description": self.description,
            "help": self.help,
            "helpUrl": self.help_url,
            "tags": self.tags,
            "nodes_count": self.nodes_count
        }


@dataclass
class AccessibilityPass:
    """Summary of passed accessibility rule."""
    id: str
    description: str
    nodes_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "nodes_count": self.nodes_count
        }


@dataclass
class AccessibilityPolicy:
    """
    Evaluation policy governing when accessibility results constitute PASS vs FAIL.
    
    Canonical Policy Contract: 'MDS-Standard-WCAG-AA'
    - Blocking Violations: Any violation with impact 'critical', 'serious', or 'moderate'
      triggers an immediate FAIL (fail_on_critical=True, fail_on_serious=True, fail_on_moderate=True).
    - Advisory Diagnostics: Violations with impact 'minor' and checks with status 'incomplete'
      do NOT block PASS; they are recorded in audit evidence as non-blocking advisory warnings
      (fail_on_minor=False, fail_on_incomplete=False).
    - PASS Condition: axe-core executes to completion on the rendered DOM and exactly 0 blocking
      violations (critical, serious, or moderate) are detected.
    """
    policy_name: str = "MDS-Standard-WCAG-AA"
    fail_on_critical: bool = True
    fail_on_serious: bool = True
    fail_on_moderate: bool = True
    fail_on_minor: bool = False
    fail_on_incomplete: bool = False
    exempted_rule_ids: List[str] = field(default_factory=list)

    def evaluate(
        self,
        violations: List[AccessibilityViolation],
        incomplete: List[AccessibilityIncomplete]
    ) -> Tuple[BrowserExecutionStatus, str]:
        """
        Evaluates violations against policy rules.
        Returns (BrowserExecutionStatus.PASS / FAIL, descriptive summary).
        """
        blocking_violations = []

        for v in violations:
            if v.id in self.exempted_rule_ids:
                continue

            impact_lower = (v.impact or "moderate").lower()
            if impact_lower == AccessibilityImpact.CRITICAL.value and self.fail_on_critical:
                blocking_violations.append(v)
            elif impact_lower == AccessibilityImpact.SERIOUS.value and self.fail_on_serious:
                blocking_violations.append(v)
            elif impact_lower == AccessibilityImpact.MODERATE.value and self.fail_on_moderate:
                blocking_violations.append(v)
            elif impact_lower == AccessibilityImpact.MINOR.value and self.fail_on_minor:
                blocking_violations.append(v)

        if self.fail_on_incomplete and incomplete:
            return (
                BrowserExecutionStatus.FAIL,
                f"Accessibility policy violation: {len(incomplete)} incomplete checks require manual review"
            )

        if blocking_violations:
            critical_cnt = sum(1 for v in blocking_violations if (v.impact or "").lower() == "critical")
            serious_cnt = sum(1 for v in blocking_violations if (v.impact or "").lower() == "serious")
            moderate_cnt = sum(1 for v in blocking_violations if (v.impact or "").lower() == "moderate")
            summary = (
                f"Policy '{self.policy_name}' breached: {len(blocking_violations)} blocking violation(s) "
                f"(Critical: {critical_cnt}, Serious: {serious_cnt}, Moderate: {moderate_cnt})"
            )
            return BrowserExecutionStatus.FAIL, summary

        return BrowserExecutionStatus.PASS, f"Policy '{self.policy_name}' satisfied: 0 blocking violations"


@dataclass
class AccessibilityResult:
    """Canonical structured accessibility result for capability execution."""
    capability_id: str
    status: BrowserExecutionStatus
    axe_version: Optional[str] = None
    page_url: Optional[str] = None
    browser: Optional[str] = None
    viewport: Optional[Dict[str, int]] = None
    violation_count: int = 0
    incomplete_count: int = 0
    pass_count: int = 0
    violations: List[Dict[str, Any]] = field(default_factory=list)
    incomplete: List[Dict[str, Any]] = field(default_factory=list)
    passes: List[Dict[str, Any]] = field(default_factory=list)
    duration_ms: float = 0.0
    evidence: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    exception_type: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "status": self.status.value if isinstance(self.status, BrowserExecutionStatus) else str(self.status),
            "axe_version": self.axe_version,
            "page_url": self.page_url,
            "browser": self.browser,
            "viewport": self.viewport,
            "violation_count": self.violation_count,
            "incomplete_count": self.incomplete_count,
            "pass_count": self.pass_count,
            "violations": self.violations,
            "incomplete": self.incomplete,
            "passes": self.passes,
            "duration_ms": self.duration_ms,
            "evidence": self.evidence,
            "error_message": self.error_message,
            "exception_type": self.exception_type,
        }
