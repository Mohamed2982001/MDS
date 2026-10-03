#!/usr/bin/env python3
"""
Accessibility Capability Dispatcher Bridge
Phase 9.7.5: Dynamic Accessibility Automation (Layer I)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Bridges the Canonical Capability Registry and Dispatch Adapter with the
dynamic axe-core accessibility engine:
registry.json -> CapabilityDispatcher -> BrowserCapabilityDispatcher -> AccessibilityDispatcher -> axe-core -> ExecutionResult
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

# Ensure 10-Testing is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from browser.models import (
    BrowserCapabilityResult,
    BrowserExecutionStatus,
)
from browser.browser_discovery import BrowserDiscovery
from browser.session import BrowserSession
from browser.cdp_driver import CDPBrowserDriver

try:
    from .accessibility_models import (
        AccessibilityResult,
        AccessibilityPolicy,
    )
    from .axe_loader import AxeLoader, AxeArtifactNotFoundError, AxeIntegrityError
    from .axe_runner import AxeRunner
    from .evidence import AccessibilityEvidenceGenerator
except (ImportError, ValueError):
    from accessibility.accessibility_models import (
        AccessibilityResult,
        AccessibilityPolicy,
    )
    from accessibility.axe_loader import AxeLoader, AxeArtifactNotFoundError, AxeIntegrityError
    from accessibility.axe_runner import AxeRunner
    from accessibility.evidence import AccessibilityEvidenceGenerator

try:
    from static.dispatch_adapter import ExecutionResult, ExecutionStatus
except ImportError:
    from ..static.dispatch_adapter import ExecutionResult, ExecutionStatus


class AccessibilityDispatcher:
    """
    Dispatcher managing execution of MDS-A11Y-004 across real browser environments.
    """

    CAPABILITY_ID = "MDS-A11Y-004"
    DEFAULT_PAGE = "MDS/Reference-Application/index.html"

    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        policy: Optional[AccessibilityPolicy] = None
    ):
        self.workspace_root = workspace_root or Path(__file__).resolve().parent.parent.parent
        self.policy = policy or AccessibilityPolicy()
        self.preferred_browser = BrowserDiscovery.get_preferred()

    @property
    def is_browser_available(self) -> bool:
        return self.preferred_browser is not None and self.preferred_browser.is_available

    @property
    def is_axe_available(self) -> bool:
        return AxeLoader.is_artifact_available()

    def run_audit(
        self,
        target_path: Optional[str] = None,
        capability_id: Optional[str] = None,
        timeout_ms: int = 15000
    ) -> AccessibilityResult:
        """
        Executes a real browser accessibility audit against a target page path.
        Returns canonical AccessibilityResult.
        """
        cid = capability_id or self.CAPABILITY_ID
        page_rel = target_path or self.DEFAULT_PAGE

        # 1. Guard against missing browser binary
        if not self.is_browser_available:
            return AccessibilityResult(
                capability_id=cid,
                status=BrowserExecutionStatus.DEFERRED,
                duration_ms=0.0,
                error_message="Host environment lacks Chromium-compatible browser binary (Chrome/Edge/Chromium).",
                exception_type="BrowserUnavailableError"
            )

        # 2. Guard against missing axe-core artifact
        if not self.is_axe_available:
            return AccessibilityResult(
                capability_id=cid,
                status=BrowserExecutionStatus.DEFERRED,
                duration_ms=0.0,
                error_message="Local pinned axe-core artifact missing at vendor directory.",
                exception_type="AxeArtifactNotFoundError"
            )

        # 3. Execute audit inside an isolated BrowserSession
        with BrowserSession(
            serve_dir=self.workspace_root,
            browser_info=self.preferred_browser,
            headless=True
        ) as session:
            # Navigate to target page
            target_url = session.server.get_url(page_rel)
            session.driver.navigate(target_url)

            # Wait for DOM to stabilize
            time_start = session.driver.wait_for("body", timeout_ms=timeout_ms)

            # Run axe audit
            runner = AxeRunner(policy=self.policy)
            result = runner.audit_page(session.driver, capability_id=cid)
            return result

    def to_browser_capability_result(self, a_res: AccessibilityResult) -> BrowserCapabilityResult:
        """Converts AccessibilityResult into standard BrowserCapabilityResult."""
        return BrowserCapabilityResult(
            capability_id=a_res.capability_id,
            status=a_res.status,
            duration_ms=a_res.duration_ms,
            evidence=a_res.evidence,
            error_message=a_res.error_message,
            exception_type=a_res.exception_type
        )

    def to_execution_result(self, a_res: AccessibilityResult) -> ExecutionResult:
        """Translates AccessibilityResult into Master Harness ExecutionResult."""
        status_map = {
            BrowserExecutionStatus.PASS: ExecutionStatus.PASS,
            BrowserExecutionStatus.FAIL: ExecutionStatus.FAIL,
            BrowserExecutionStatus.DEFERRED: ExecutionStatus.DEFERRED,
        }
        details = (
            f"axe v{a_res.axe_version or 'N/A'} audit: {a_res.violation_count} violations, "
            f"{a_res.pass_count} passed in {a_res.duration_ms:.1f}ms"
        )
        if a_res.error_message:
            details = f"{details} — {a_res.error_message}"

        return ExecutionResult(
            capability_id=a_res.capability_id,
            status=status_map.get(a_res.status, ExecutionStatus.FAIL),
            details=details,
            duration_ms=a_res.duration_ms
        )


def run_accessibility_capability(session: Optional[BrowserSession] = None) -> AccessibilityResult:
    """Standard entrypoint callable by Master Test Harness and Dispatch Adapter."""
    dispatcher = AccessibilityDispatcher()
    return dispatcher.run_audit()


if __name__ == "__main__":
    dispatcher = AccessibilityDispatcher()
    print("Executing standalone Accessibility Audit...")
    res = dispatcher.run_audit()
    print(AccessibilityEvidenceGenerator.format_text_report(res))
