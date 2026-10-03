#!/usr/bin/env python3
"""
Unit Tests for Browser Driver Base, Models, Session, and Dispatch Integration
Phase 9.7.4: Browser Automation Runner Bridge
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Tests driver abstraction contracts, value objects, error hierarchies, security gates,
and registry dispatch without requiring a live browser process.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add MDS/10-Testing to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from browser.models import (
    Viewport,
    BrowserInfo,
    BrowserType,
    ConsoleLogEntry,
    ConsoleLogLevel,
    BrowserCapabilityResult,
    BrowserExecutionStatus,
)
from browser.exceptions import (
    BrowserBridgeError,
    BrowserNotFoundError,
    BrowserLaunchError,
    CDPConnectionError,
    CDPCommandError,
    NavigationError,
    TimeoutError,
    ElementNotFoundError,
    InvalidCommandError,
    ServerStartupError,
)
from browser.driver_base import BrowserDriverBase
from browser.cdp_driver import CDPBrowserDriver, _CDPSocketClient
from browser.session import BrowserSession
from browser.dispatch_integration import BrowserCapabilityDispatcher
from static.dispatch_adapter import ExecutionStatus


class TestBrowserUnit(unittest.TestCase):
    """Category A: Unit tests executing without requiring a live browser."""

    def test_01_driver_base_abstract_contract(self):
        """U-01: Verifies BrowserDriverBase cannot be instantiated directly without abstract implementations."""
        with self.assertRaises(TypeError):
            BrowserDriverBase()

    def test_02_viewport_presets_and_serialization(self):
        """U-02: Verifies all canonical responsive presets produce valid dimensions."""
        m = Viewport.mobile_compact()
        self.assertEqual(m.width, 320)
        self.assertEqual(m.height, 640)
        self.assertTrue(m.is_mobile)

        t = Viewport.tablet_portrait()
        self.assertEqual(t.width, 768)
        self.assertEqual(t.height, 1024)
        self.assertFalse(t.is_mobile)

        d_std = Viewport.desktop_standard()
        self.assertEqual(d_std.width, 1024)
        self.assertEqual(d_std.height, 768)

        d_wide = Viewport.desktop_wide()
        self.assertEqual(d_wide.width, 1440)
        self.assertEqual(d_wide.height, 900)

        d = d_wide.to_dict()
        self.assertEqual(d["width"], 1440)
        self.assertEqual(d["height"], 900)
        self.assertEqual(d["device_scale_factor"], 1.0)

    def test_03_console_log_entry_model(self):
        """U-03: Verifies ConsoleLogEntry stores metadata and converts to dict."""
        entry = ConsoleLogEntry(
            level="error",
            text="Uncaught ReferenceError: foo is not defined",
            timestamp=123456789.0,
            url="http://127.0.0.1:8000/test.html"
        )
        d = entry.to_dict()
        self.assertEqual(d["level"], "error")
        self.assertIn("foo is not defined", d["text"])
        self.assertEqual(d["timestamp"], 123456789.0)

    def test_04_browser_capability_result_structure(self):
        """U-04: Verifies BrowserCapabilityResult enforces status types and serialization."""
        res = BrowserCapabilityResult(
            capability_id="MDS-TEST-001",
            status=BrowserExecutionStatus.PASS,
            duration_ms=45.2,
            evidence={"title": "MDS Workspace"}
        )
        d = res.to_dict()
        self.assertEqual(d["capability_id"], "MDS-TEST-001")
        self.assertEqual(d["status"], "PASS")
        self.assertEqual(d["duration_ms"], 45.2)
        self.assertIn("title", d["evidence"])

    def test_05_exceptions_hierarchy(self):
        """U-05: Verifies domain exception hierarchy correctly subclasses BrowserBridgeError."""
        self.assertTrue(issubclass(BrowserNotFoundError, BrowserBridgeError))
        self.assertTrue(issubclass(BrowserLaunchError, BrowserBridgeError))
        self.assertTrue(issubclass(CDPConnectionError, BrowserBridgeError))
        self.assertTrue(issubclass(CDPCommandError, BrowserBridgeError))
        self.assertTrue(issubclass(NavigationError, BrowserBridgeError))
        self.assertTrue(issubclass(TimeoutError, BrowserBridgeError))
        self.assertTrue(issubclass(ElementNotFoundError, BrowserBridgeError))
        self.assertTrue(issubclass(InvalidCommandError, BrowserBridgeError))
        self.assertTrue(issubclass(ServerStartupError, BrowserBridgeError))

        # Check CDPCommandError fields
        err = CDPCommandError("SyntaxError", code=-32000, details="eval failed", capability_id="CAP-1")
        self.assertEqual(err.code, -32000)
        self.assertEqual(err.capability_id, "CAP-1")

    def test_06_browser_session_deferred_when_no_browser(self):
        """U-06: Verifies BrowserSession returns explicit DEFERRED without fabrication when no browser is available."""
        session = BrowserSession(browser_info=None)
        # Mock availability property
        with patch.object(BrowserSession, "is_browser_available", False):
            result = session.run_capability("MDS-MOCK-001", lambda s: "ok")
            self.assertEqual(result.status, BrowserExecutionStatus.DEFERRED)
            self.assertFalse(result.evidence.get("browser_available"))
            self.assertIn("missing", result.error_message.lower())

    def test_07_invalid_host_navigation_rejected(self):
        """U-07: Verifies security policy blocks external internet navigation."""
        driver = CDPBrowserDriver()
        driver._is_launched = True
        driver.proc = MagicMock()
        driver.proc.poll.return_value = None
        driver.cdp_client = MagicMock()
        driver.cdp_client._is_closed = False

        # Should reject external domain
        with self.assertRaises(InvalidCommandError):
            driver.navigate("https://www.google.com")

        with self.assertRaises(InvalidCommandError):
            driver.navigate("http://evil-tracker.com/steal")

    def test_08_invalid_viewport_dimensions_rejected(self):
        """U-08: Verifies driver rejects non-positive viewport dimensions."""
        driver = CDPBrowserDriver()
        driver._is_launched = True
        driver.proc = MagicMock()
        driver.proc.poll.return_value = None
        driver.cdp_client = MagicMock()
        driver.cdp_client._is_closed = False

        with self.assertRaises(InvalidCommandError):
            driver.set_viewport(0, 800)

        with self.assertRaises(InvalidCommandError):
            driver.set_viewport(1024, -100)

    def test_09_dispatch_integration_deferred_preservation(self):
        """U-09: Verifies BrowserCapabilityDispatcher preserves deferred capabilities when configured."""
        dispatcher = BrowserCapabilityDispatcher()
        dispatcher.DEFERRED_BROWSER_CAPABILITIES["MDS-TEST-DEF"] = "Deferred test capability"
        try:
            res = dispatcher.execute_browser_capability("MDS-TEST-DEF")
            self.assertEqual(res.status, BrowserExecutionStatus.DEFERRED)
            self.assertIsNotNone(res.error_message)
        finally:
            dispatcher.DEFERRED_BROWSER_CAPABILITIES.pop("MDS-TEST-DEF", None)

    def test_10_dispatch_integration_conversion_to_execution_result(self):
        """U-10: Verifies BrowserCapabilityResult cleanly converts to dispatch adapter ExecutionResult."""
        dispatcher = BrowserCapabilityDispatcher()
        b_res = BrowserCapabilityResult(
            capability_id="MDS-TEST-002",
            status=BrowserExecutionStatus.DEFERRED,
            duration_ms=0.0,
            error_message="Requires browser"
        )
        exec_res = dispatcher.to_execution_result(b_res)
        self.assertEqual(exec_res.capability_id, "MDS-TEST-002")
        self.assertEqual(exec_res.status, ExecutionStatus.DEFERRED)
        self.assertIn("Requires browser", exec_res.details)

    def test_11_cdp_client_connection_error_on_invalid_port(self):
        """U-11: Verifies CDP socket client raises CDPConnectionError when port is unreachable."""
        with self.assertRaises(CDPConnectionError):
            _CDPSocketClient("ws://127.0.0.1:59999/devtools/page/invalid", timeout=0.5)

    def test_12_wait_for_timeout_behavior_raises_timeout_error(self):
        """U-12 (Failure Mode): Verifies wait_for raises TimeoutError when element does not appear."""
        driver = CDPBrowserDriver()
        driver._is_launched = True
        driver.proc = MagicMock()
        driver.proc.poll.return_value = None
        driver.cdp_client = MagicMock()
        driver.cdp_client._is_closed = False

        # Mock evaluate to always return False (element not found)
        driver.evaluate = MagicMock(return_value=False)

        with self.assertRaises(TimeoutError) as ctx:
            driver.wait_for("#element-never-exists", timeout_ms=80)
        self.assertIn("Timed out waiting for element", str(ctx.exception))

    def test_13_click_missing_element_raises_timeout(self):
        """U-13 (Failure Mode): Verifies click on non-existent element raises TimeoutError."""
        driver = CDPBrowserDriver()
        driver._is_launched = True
        driver.proc = MagicMock()
        driver.proc.poll.return_value = None
        driver.cdp_client = MagicMock()
        driver.cdp_client._is_closed = False

        driver.evaluate = MagicMock(return_value=False)

        with self.assertRaises(TimeoutError):
            driver.click("#nonexistent-button", timeout_ms=50)

    def test_14_invalid_javascript_raises_cdp_command_error(self):
        """U-14 (Failure Mode): Verifies evaluate raises CDPCommandError on JavaScript exceptions."""
        driver = CDPBrowserDriver()
        driver._is_launched = True
        driver.proc = MagicMock()
        driver.proc.poll.return_value = None
        driver.cdp_client = MagicMock()
        driver.cdp_client._is_closed = False

        # Simulate CDP exceptionDetails response
        driver.cdp_client.send_command.return_value = {
            "id": 1,
            "result": {
                "exceptionDetails": {
                    "text": "Uncaught ReferenceError: variableNotDefined is not defined",
                    "exception": {"description": "ReferenceError: variableNotDefined is not defined"}
                }
            }
        }

        with self.assertRaises(CDPCommandError) as ctx:
            driver.evaluate("variableNotDefined.doSomething()")
        self.assertIn("ReferenceError", str(ctx.exception))

    def test_15_session_catches_exception_as_fail_status(self):
        """U-15 (Result Contract): Verifies unhandled task exception produces FAIL with exception_type."""
        session = BrowserSession(browser_info=MagicMock())
        session._is_active = True
        session.driver = MagicMock()
        session.driver._active_url = "http://127.0.0.1:8000/"
        session.driver._viewport = Viewport(1440, 900)
        session.driver.get_console_logs.return_value = []

        def failing_task(sess):
            raise ValueError("Simulated DOM assertion failure in test")

        res = session.run_capability("MDS-FAIL-TEST-001", failing_task)
        self.assertEqual(res.status, BrowserExecutionStatus.FAIL)
        self.assertEqual(res.exception_type, "ValueError")
        self.assertIn("Simulated DOM assertion failure", res.error_message)

    def test_16_structural_registry_dispatch_integration(self):
        """U-16 (Finding B-003 Structural): Verifies Registry -> Dispatcher -> BrowserBridge structural integration."""
        dispatcher = BrowserCapabilityDispatcher()
        self.assertTrue(dispatcher.workspace_root.exists())

        # Test capability routing for deferred capability handling
        dispatcher.DEFERRED_BROWSER_CAPABILITIES["MDS-TEST-DEF"] = "Deferred test"
        try:
            deferred_res = dispatcher.execute_browser_capability("MDS-TEST-DEF")
            self.assertEqual(deferred_res.status, BrowserExecutionStatus.DEFERRED)
            self.assertEqual(deferred_res.capability_id, "MDS-TEST-DEF")

            # Test translation to ExecutionResult
            exec_res = dispatcher.to_execution_result(deferred_res)
            self.assertEqual(exec_res.status, ExecutionStatus.DEFERRED)
            self.assertEqual(exec_res.capability_id, "MDS-TEST-DEF")
        finally:
            dispatcher.DEFERRED_BROWSER_CAPABILITIES.pop("MDS-TEST-DEF", None)

        # Test simulated task dispatch
        mock_task = MagicMock(return_value="Component mounted")
        with patch.object(BrowserSession, "run_capability") as mock_run:
            mock_run.return_value = BrowserCapabilityResult(
                capability_id="MDS-CMP-001",
                status=BrowserExecutionStatus.PASS,
                duration_ms=12.5,
                evidence={"dom_result": "Component mounted"}
            )
            dispatcher.preferred_browser = MagicMock(is_available=True)
            res = dispatcher.execute_browser_capability("MDS-CMP-001", mock_task)
            self.assertEqual(res.status, BrowserExecutionStatus.PASS)
            self.assertEqual(res.capability_id, "MDS-CMP-001")


if __name__ == "__main__":
    unittest.main()
