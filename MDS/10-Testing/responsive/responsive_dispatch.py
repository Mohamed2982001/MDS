#!/usr/bin/env python3
"""
MDS Responsive Capability Dispatcher Bridge
Phase 9.7.6: Responsive Viewport Automation (Layer K)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Bridges the Canonical Capability Registry and Dispatch Adapter with the
Responsive Viewport Automation Engine:
registry.json -> CapabilityDispatcher -> BrowserCapabilityDispatcher -> ResponsiveDispatcher -> ExecutionResult
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any

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
    from .responsive_models import (
        ResponsiveMatrixResult,
        ResponsiveRunResult,
    )
    from .responsive_runner import ResponsiveRunner
    from .viewport_matrix import get_canonical_matrix
    from .evidence import ResponsiveEvidenceGenerator
except (ImportError, ValueError):
    from responsive.responsive_models import (
        ResponsiveMatrixResult,
        ResponsiveRunResult,
    )
    from responsive.responsive_runner import ResponsiveRunner
    from responsive.viewport_matrix import get_canonical_matrix
    from responsive.evidence import ResponsiveEvidenceGenerator

try:
    from static.dispatch_adapter import ExecutionResult, ExecutionStatus
except ImportError:
    from ..static.dispatch_adapter import ExecutionResult, ExecutionStatus


class ResponsiveDispatcher:
    """
    Dispatcher managing execution of MDS-RWD-003 across real browser environments.
    """

    CAPABILITY_ID = "MDS-RWD-003"
    DEFAULT_PAGE = "MDS/Reference-Application/index.html"

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(__file__).resolve().parent.parent.parent.parent
        self.preferred_browser = BrowserDiscovery.get_preferred()

    @property
    def is_browser_available(self) -> bool:
        return self.preferred_browser is not None and self.preferred_browser.is_available

    def run_matrix(
        self,
        target_path: Optional[str] = None,
        capability_id: Optional[str] = None,
        timeout_ms: int = 15000,
        artifacts_dir: Optional[Path] = None,
    ) -> ResponsiveMatrixResult:
        """
        Executes the Canonical 17-Run Responsive Matrix in a live Chromium browser.
        Returns canonical ResponsiveMatrixResult.
        """
        cid = capability_id or self.CAPABILITY_ID
        page_rel = target_path or self.DEFAULT_PAGE

        # 1. Guard against missing browser binary
        if not self.is_browser_available:
            return ResponsiveMatrixResult(
                capability_id=cid,
                status="DEFERRED",
                runs=[],
                total_assertions=0,
                passed_assertions=0,
                failed_assertions=0,
                hard_failures=0,
                duration_ms=0.0,
                error_message="Host environment lacks Chromium-compatible browser binary (Chrome/Edge/Chromium).",
                exception_type="BrowserUnavailableError",
            )

        # 2. Execute matrix inside an isolated BrowserSession
        art_dir = artifacts_dir or (Path(__file__).resolve().parent.parent / "artifacts")
        with BrowserSession(
            serve_dir=self.workspace_root,
            browser_info=self.preferred_browser,
            headless=True,
            artifacts_dir=art_dir,
        ) as session:
            # Navigate to target page
            target_url = session.server.get_url(page_rel)
            session.driver.navigate(target_url)

            # Wait for body to be ready
            session.driver.wait_for("body", timeout_ms=timeout_ms)

            # Execute canonical 17-run matrix
            runner = ResponsiveRunner()
            matrix_result = runner.execute_matrix(session.driver)
            matrix_result.evidence = ResponsiveEvidenceGenerator.to_dict(matrix_result)

            # Save evidence artifact
            try:
                evidence_path = art_dir / "responsive_evidence.json"
                ResponsiveEvidenceGenerator.save_artifact(matrix_result, evidence_path)
            except Exception:
                pass

            return matrix_result

    def to_browser_capability_result(self, m_res: ResponsiveMatrixResult) -> BrowserCapabilityResult:
        """Converts ResponsiveMatrixResult into standard BrowserCapabilityResult."""
        status_map = {
            "PASS": BrowserExecutionStatus.PASS,
            "FAIL": BrowserExecutionStatus.FAIL,
            "DEFERRED": BrowserExecutionStatus.DEFERRED,
        }
        b_status = status_map.get(m_res.status, BrowserExecutionStatus.FAIL)

        return BrowserCapabilityResult(
            capability_id=m_res.capability_id,
            status=b_status,
            duration_ms=m_res.duration_ms,
            evidence=m_res.evidence,
            error_message=m_res.error_message,
            exception_type=m_res.exception_type,
        )

    def to_execution_result(self, m_res: ResponsiveMatrixResult) -> ExecutionResult:
        """Translates ResponsiveMatrixResult into Master Harness ExecutionResult."""
        status_map = {
            "PASS": ExecutionStatus.PASS,
            "FAIL": ExecutionStatus.FAIL,
            "DEFERRED": ExecutionStatus.DEFERRED,
        }
        details = (
            f"17-Run Matrix: {len(m_res.runs)} runs, {m_res.passed_assertions}/{m_res.total_assertions} passed, "
            f"{m_res.hard_failures} hard failures in {m_res.duration_ms:.1f}ms"
        )
        if m_res.error_message:
            details = f"{details} — {m_res.error_message}"

        return ExecutionResult(
            capability_id=m_res.capability_id,
            status=status_map.get(m_res.status, ExecutionStatus.FAIL),
            details=details,
            duration_ms=m_res.duration_ms,
        )


def run_responsive_capability(session: Optional[BrowserSession] = None) -> ResponsiveMatrixResult:
    """Standard entrypoint callable by Master Test Harness and Dispatch Adapter."""
    dispatcher = ResponsiveDispatcher()
    return dispatcher.run_matrix()


if __name__ == "__main__":
    dispatcher = ResponsiveDispatcher()
    print("Executing standalone Responsive Viewport Automation Matrix...")
    res = dispatcher.run_matrix()
    print(ResponsiveEvidenceGenerator.format_text_report(res))
