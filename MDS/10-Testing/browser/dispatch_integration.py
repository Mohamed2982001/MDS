#!/usr/bin/env python3
"""
MDS Browser Dispatch Integration Bridge
Phase 9.7.4: Browser Automation Runner Bridge
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Provides a clean integration point connecting the Canonical Capability Registry
and Dispatch Adapter with the Browser Automation Bridge:
Registry -> Dispatch Adapter -> Browser Capability -> Browser Driver -> Structured Result
"""

from typing import Optional, Callable, Dict, Any
from pathlib import Path

from .models import (
    BrowserCapabilityResult,
    BrowserExecutionStatus,
    BrowserInfo,
)
from .browser_discovery import BrowserDiscovery
from .session import BrowserSession
try:
    from static.dispatch_adapter import ExecutionResult, ExecutionStatus
except ImportError:
    from ..static.dispatch_adapter import ExecutionResult, ExecutionStatus


class BrowserCapabilityDispatcher:
    """
    Integrates the browser automation bridge with the MDS Capability Registry.
    Guarantees zero false passes and returns structured results adhering to the
    canonical test accounting:
    170 Defined = 167 Active Executable + 3 Deferred (MDS-A11Y-004, MDS-RWD-003, MDS-VIS-001)
    """

    # All browser capabilities promoted (170 defined = 170 active + 0 deferred)
    DEFERRED_BROWSER_CAPABILITIES: Dict[str, str] = {}

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(__file__).resolve().parent.parent.parent.parent
        self.preferred_browser = BrowserDiscovery.get_preferred()

    @property
    def is_browser_available(self) -> bool:
        return self.preferred_browser is not None and self.preferred_browser.is_available

    def execute_browser_capability(
        self,
        capability_id: str,
        custom_task: Optional[Callable[[BrowserSession], Any]] = None
    ) -> BrowserCapabilityResult:
        """
        Executes a browser-level validation capability.
        If the capability is deferred, returns an explicit DEFERRED result with reason.
        If a browser task is supplied, executes within an isolated BrowserSession.
        """
        # 1. Guard deferred capabilities until their dedicated phases
        if capability_id in self.DEFERRED_BROWSER_CAPABILITIES and custom_task is None:
            return BrowserCapabilityResult(
                capability_id=capability_id,
                status=BrowserExecutionStatus.DEFERRED,
                duration_ms=0.0,
                evidence={
                    "browser_available": self.is_browser_available,
                    "deferred_reason": self.DEFERRED_BROWSER_CAPABILITIES[capability_id],
                },
                error_message=self.DEFERRED_BROWSER_CAPABILITIES[capability_id]
            )

        # 2. Route promoted accessibility capability MDS-A11Y-004 (Phase 9.7.5)
        if capability_id == "MDS-A11Y-004" and custom_task is None:
            try:
                from accessibility.accessibility_dispatch import AccessibilityDispatcher
            except ImportError:
                from ..accessibility.accessibility_dispatch import AccessibilityDispatcher
            a11y_disp = AccessibilityDispatcher(workspace_root=self.workspace_root)
            a_res = a11y_disp.run_audit(capability_id=capability_id)
            return a11y_disp.to_browser_capability_result(a_res)

        # 3. Route promoted responsive capability MDS-RWD-003 (Phase 9.7.6)
        if capability_id == "MDS-RWD-003" and custom_task is None:
            try:
                from responsive.responsive_dispatch import ResponsiveDispatcher
            except ImportError:
                from ..responsive.responsive_dispatch import ResponsiveDispatcher
            rwd_disp = ResponsiveDispatcher(workspace_root=self.workspace_root)
            r_res = rwd_disp.run_matrix(capability_id=capability_id)
            return rwd_disp.to_browser_capability_result(r_res)

        # 4. Route promoted visual regression capability MDS-VIS-001 (Phase 9.7.7)
        if capability_id == "MDS-VIS-001" and custom_task is None:
            try:
                from visual.visual_dispatch import VisualDispatcher
            except ImportError:
                from ..visual.visual_dispatch import VisualDispatcher
            vis_disp = VisualDispatcher(workspace_root=self.workspace_root)
            v_res = vis_disp.run_sweep(capability_id=capability_id)
            return vis_disp.to_browser_capability_result(v_res)

        # 2. Guard against missing browser binaries
        if not self.is_browser_available:
            return BrowserCapabilityResult(
                capability_id=capability_id,
                status=BrowserExecutionStatus.DEFERRED,
                duration_ms=0.0,
                evidence={
                    "browser_available": False,
                    "reason": "No Chromium-compatible browser binary (Chrome/Edge/Chromium) found."
                },
                error_message="Environment missing browser binary."
            )

        # 3. If a task is provided, run it in an isolated session
        if custom_task is not None:
            session = BrowserSession(
                serve_dir=self.workspace_root,
                browser_info=self.preferred_browser,
                headless=True
            )
            try:
                return session.run_capability(capability_id, custom_task)
            finally:
                session.close()

        # Fallback for unrecognized capabilities
        return BrowserCapabilityResult(
            capability_id=capability_id,
            status=BrowserExecutionStatus.FAIL,
            duration_ms=0.0,
            evidence={},
            error_message=f"No execution routine registered for browser capability {capability_id}",
            exception_type="UnregisteredCapabilityError"
        )

    def to_execution_result(self, b_res: BrowserCapabilityResult) -> ExecutionResult:
        """Translates a BrowserCapabilityResult into a standard ExecutionResult."""
        status_map = {
            BrowserExecutionStatus.PASS: ExecutionStatus.PASS,
            BrowserExecutionStatus.FAIL: ExecutionStatus.FAIL,
            BrowserExecutionStatus.DEFERRED: ExecutionStatus.DEFERRED,
        }
        return ExecutionResult(
            capability_id=b_res.capability_id,
            status=status_map.get(b_res.status, ExecutionStatus.FAIL),
            details=b_res.error_message or f"Executed in {b_res.duration_ms:.1f}ms",
            duration_ms=b_res.duration_ms
        )
