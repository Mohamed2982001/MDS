#!/usr/bin/env python3
"""
MDS Browser Session Orchestrator
Phase 9.7.4: Browser Automation Runner Bridge
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Provides disposable, isolated test sessions coordinating:
1. Ephemeral Local HTTP Test Server (LocalTestServer)
2. Chromium Browser Driver (CDPBrowserDriver)
3. Structured result reporting (BrowserCapabilityResult)
"""

import time
from pathlib import Path
from typing import Optional, Callable, Dict, Any, List

from .models import (
    BrowserCapabilityResult,
    BrowserExecutionStatus,
    BrowserInfo,
    Viewport,
    ConsoleLogEntry,
)
from .exceptions import (
    BrowserBridgeError,
    BrowserNotFoundError,
    CDPConnectionError,
    ServerStartupError,
)
from .local_server import LocalTestServer
from .cdp_driver import CDPBrowserDriver
from .browser_discovery import BrowserDiscovery


class BrowserSession:
    """
    High-level context manager providing an isolated browser testing environment.
    Coordinates local server lifecycle, browser launching, evidence collection,
    and deterministic cleanup.
    """

    def __init__(
        self,
        serve_dir: Optional[Path] = None,
        browser_info: Optional[BrowserInfo] = None,
        headless: bool = True,
        timeout: float = 15.0,
        artifacts_dir: Optional[Path] = None,
    ):
        self.serve_dir = serve_dir or Path(__file__).resolve().parent.parent.parent.parent
        self.browser_info = browser_info or BrowserDiscovery.get_preferred()
        self.headless = headless
        self.timeout = timeout
        self.artifacts_dir = artifacts_dir or (
            Path(__file__).resolve().parent.parent / "artifacts"
        )

        self.server: Optional[LocalTestServer] = None
        self.driver: Optional[CDPBrowserDriver] = None
        self._is_active = False

    @property
    def is_browser_available(self) -> bool:
        """Returns True if a compatible browser binary exists on the host."""
        return self.browser_info is not None and self.browser_info.is_available

    def start(self) -> "BrowserSession":
        """Starts both local server and browser driver."""
        if self._is_active:
            return self

        if not self.is_browser_available:
            raise BrowserNotFoundError(
                "Cannot start session: No Chromium-compatible browser found on host."
            )

        # 1. Start local server
        self.server = LocalTestServer(serve_dir=self.serve_dir)
        self.server.start()

        # 2. Launch browser driver
        self.driver = CDPBrowserDriver(
            browser_info=self.browser_info,
            timeout=self.timeout
        )
        self.driver.launch(headless=self.headless)

        self._is_active = True
        return self

    def close(self) -> None:
        """Deterministically tears down browser process and local server."""
        if self.driver:
            try:
                self.driver.close()
            except Exception:
                pass
            self.driver = None

        if self.server:
            try:
                self.server.stop()
            except Exception:
                pass
            self.server = None

        self._is_active = False

    def __enter__(self) -> "BrowserSession":
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def run_capability(
        self,
        capability_id: str,
        task_fn: Callable[["BrowserSession"], Any]
    ) -> BrowserCapabilityResult:
        """
        Executes a browser validation capability task and produces a structured result.
        Captures evidence: URL, viewport, timing, console logs, and errors.
        """
        # If no browser is installed, return DEFERRED immediately without fabricating
        if not self.is_browser_available:
            return BrowserCapabilityResult(
                capability_id=capability_id,
                status=BrowserExecutionStatus.DEFERRED,
                duration_ms=0.0,
                evidence={
                    "browser_available": False,
                    "reason": "No Chromium-compatible browser binary found on host system."
                },
                error_message="Environment missing compatible browser binary."
            )

        start_time = time.time()
        evidence: Dict[str, Any] = {
            "browser_name": self.browser_info.name if self.browser_info else "Unknown",
            "browser_version": self.browser_info.version if self.browser_info else "Unknown",
            "browser_executable": str(self.browser_info.path) if self.browser_info else "",
        }

        try:
            # Ensure session is active
            if not self._is_active:
                self.start()

            # Execute caller's test routine
            task_result = task_fn(self)

            # Record telemetry
            duration_ms = (time.time() - start_time) * 1000.0
            evidence["url"] = self.driver._active_url if self.driver else ""
            evidence["viewport"] = self.driver._viewport.to_dict() if self.driver and self.driver._viewport else {}
            evidence["dom_result"] = task_result
            evidence["console_logs"] = [l.to_dict() for l in (self.driver.get_console_logs() if self.driver else [])]

            return BrowserCapabilityResult(
                capability_id=capability_id,
                status=BrowserExecutionStatus.PASS,
                duration_ms=duration_ms,
                evidence=evidence,
                error_message=None
            )

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000.0
            evidence["url"] = self.driver._active_url if self.driver else ""
            evidence["viewport"] = self.driver._viewport.to_dict() if self.driver and self.driver._viewport else {}
            evidence["console_logs"] = [l.to_dict() for l in (self.driver.get_console_logs() if self.driver else [])]

            # Execution exceptions are classified as FAIL with detailed exception metadata
            return BrowserCapabilityResult(
                capability_id=capability_id,
                status=BrowserExecutionStatus.FAIL,
                duration_ms=duration_ms,
                evidence=evidence,
                error_message=str(e),
                exception_type=type(e).__name__
            )
