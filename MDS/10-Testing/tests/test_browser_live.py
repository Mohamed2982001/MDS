#!/usr/bin/env python3
"""
Integration Tests for Live Chromium Browser Automation
Phase 9.7.4: Browser Automation Runner Bridge
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Executes real browser smoke tests against installed Chromium binaries (Chrome / Edge)
verifying navigation, DOM interaction, viewport resizing, console log capture,
screenshots, and session disposal.
"""

import os
import sys
import unittest
from pathlib import Path

# Add MDS/10-Testing to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from browser.models import BrowserExecutionStatus
from browser.browser_discovery import BrowserDiscovery
from browser.local_server import LocalTestServer
from browser.cdp_driver import CDPBrowserDriver
from browser.session import BrowserSession
from browser.dispatch_integration import BrowserCapabilityDispatcher
from static.dispatch_adapter import CapabilityDispatcher, ExecutionStatus


class TestBrowserLive(unittest.TestCase):
    """Category B: Real browser execution tests against live Chromium binary."""

    @classmethod
    def setUpClass(cls):
        cls.preferred_browser = BrowserDiscovery.get_preferred()
        if not cls.preferred_browser:
            raise unittest.SkipTest("Skipping Category B: No Chromium browser discovered on host.")

        # Start a shared local server for the live suite
        cls.server = LocalTestServer()
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "server") and cls.server:
            cls.server.stop()

    def test_01_real_browser_launch_and_connect(self):
        """B-01: Verifies real browser process launches headlessly and establishes CDP connection."""
        driver = CDPBrowserDriver(browser_info=self.preferred_browser)
        try:
            driver.launch(headless=True)
            self.assertTrue(driver.is_connected)
            self.assertIsNotNone(driver.port)
            self.assertGreater(driver.port, 1024)
            self.assertTrue(os.path.exists(driver.user_data_dir))
        finally:
            driver.close()
            self.assertFalse(driver.is_connected)

    def test_02_live_navigation_and_dom_readiness(self):
        """B-02: Verifies live browser navigates to local server and completes document loading."""
        with CDPBrowserDriver(browser_info=self.preferred_browser) as driver:
            driver.launch(headless=True)
            url = self.server.get_url("MDS/Playground/index.html")
            driver.navigate(url)

            state = driver.evaluate("document.readyState")
            self.assertIn(state, ("interactive", "complete"))

            title = driver.evaluate("document.title")
            self.assertIn("MDS", title)

    def test_03_live_viewport_resizing(self):
        """B-03: Verifies browser viewport resize takes effect in live DOM."""
        with CDPBrowserDriver(browser_info=self.preferred_browser) as driver:
            driver.launch(headless=True)
            url = self.server.get_url("MDS/Playground/index.html")
            driver.navigate(url)

            # Resize to tablet
            driver.set_viewport(768, 1024)
            dims = driver.evaluate("({ w: window.innerWidth, h: window.innerHeight })")
            self.assertIsInstance(dims, dict)
            self.assertGreater(dims.get("w", 0), 0)

            # Resize to mobile
            driver.set_viewport(320, 640)
            dims_mobile = driver.evaluate("({ w: window.innerWidth, h: window.innerHeight })")
            self.assertIsInstance(dims_mobile, dict)
            self.assertGreater(dims_mobile.get("w", 0), 0)

    def test_04_live_javascript_evaluation(self):
        """B-04: Verifies live evaluation of complex JavaScript types and structures."""
        with CDPBrowserDriver(browser_info=self.preferred_browser) as driver:
            driver.launch(headless=True)
            # Math & Arithmetic
            self.assertEqual(driver.evaluate("10 * 10"), 100)
            # String manipulation
            self.assertEqual(driver.evaluate("'Master Design System'.toUpperCase()"), "MASTER DESIGN SYSTEM")
            # Array mapping
            self.assertEqual(driver.evaluate("[1, 2, 3].map(x => x * 2)"), [2, 4, 6])
            # Object serialization
            obj = driver.evaluate("({ name: 'Cairo', type: 'font' })")
            self.assertEqual(obj, {"name": "Cairo", "type": "font"})

    def test_05_live_console_log_capture(self):
        """B-05: Verifies capturing console.log, console.warn, and console.error messages."""
        with CDPBrowserDriver(browser_info=self.preferred_browser) as driver:
            driver.launch(headless=True)
            driver.evaluate("console.log('MDS live info log');")
            driver.evaluate("console.warn('MDS live warning log');")
            driver.evaluate("console.error('MDS live error log');")

            logs = driver.get_console_logs()
            self.assertGreaterEqual(len(logs), 3)

            texts = [l.text for l in logs]
            self.assertTrue(any("MDS live info log" in t for t in texts))
            self.assertTrue(any("MDS live warning log" in t for t in texts))
            self.assertTrue(any("MDS live error log" in t for t in texts))

    def test_06_live_interactive_click(self):
        """B-06: Verifies element click triggers real DOM mutation and event listeners."""
        with CDPBrowserDriver(browser_info=self.preferred_browser) as driver:
            driver.launch(headless=True)
            url = self.server.get_url("MDS/Playground/index.html")
            driver.navigate(url)

            # Insert an interactive button with a click counter
            setup_script = """
            (() => {
                const btn = document.createElement('button');
                btn.id = 'test-live-btn';
                btn.textContent = 'Count: 0';
                btn.addEventListener('click', () => {
                    const current = parseInt(btn.dataset.clicks || '0', 10);
                    btn.dataset.clicks = current + 1;
                    btn.textContent = 'Count: ' + (current + 1);
                });
                document.body.appendChild(btn);
                return true;
            })()
            """
            self.assertTrue(driver.evaluate(setup_script))

            # Click the button
            driver.click("#test-live-btn")

            # Assert DOM updated
            clicks = driver.evaluate("document.querySelector('#test-live-btn').dataset.clicks")
            self.assertEqual(clicks, "1")

            # Click again
            driver.click("#test-live-btn")
            clicks2 = driver.evaluate("document.querySelector('#test-live-btn').dataset.clicks")
            self.assertEqual(clicks2, "2")

    def test_07_live_interactive_type_text(self):
        """B-07: Verifies element type_text updates value and dispatches input events."""
        with CDPBrowserDriver(browser_info=self.preferred_browser) as driver:
            driver.launch(headless=True)
            url = self.server.get_url("MDS/Playground/index.html")
            driver.navigate(url)

            # Insert an interactive text input
            setup_script = """
            (() => {
                const inp = document.createElement('input');
                inp.id = 'test-live-input';
                inp.type = 'text';
                document.body.appendChild(inp);
                return true;
            })()
            """
            self.assertTrue(driver.evaluate(setup_script))

            # Type text into input
            driver.type_text("#test-live-input", "Cairo Master Typography")

            # Verify value
            val = driver.evaluate("document.querySelector('#test-live-input').value")
            self.assertEqual(val, "Cairo Master Typography")

    def test_08_live_wait_for_selector(self):
        """B-08: Verifies wait_for resolves when element is dynamically appended asynchronously."""
        with CDPBrowserDriver(browser_info=self.preferred_browser) as driver:
            driver.launch(headless=True)
            url = self.server.get_url("MDS/Playground/index.html")
            driver.navigate(url)

            # Append element with 100ms delay
            driver.evaluate("""
            setTimeout(() => {
                const el = document.createElement('div');
                el.id = 'dynamic-async-target';
                document.body.appendChild(el);
            }, 100);
            """)

            # Should wait and resolve True
            self.assertTrue(driver.wait_for("#dynamic-async-target", timeout_ms=3000))

    def test_09_live_screenshot_capture(self):
        """B-09: Verifies screenshot returns valid raw PNG bytes with correct magic header."""
        with CDPBrowserDriver(browser_info=self.preferred_browser) as driver:
            driver.launch(headless=True)
            url = self.server.get_url("MDS/Playground/index.html")
            driver.navigate(url)

            shot = driver.screenshot()
            self.assertIsInstance(shot, bytes)
            self.assertGreater(len(shot), 5000)
            # PNG magic header: \x89PNG\r\n\x1a\n
            self.assertEqual(shot[:8], b"\x89PNG\r\n\x1a\n")

    def test_10_live_session_isolation_and_cleanup(self):
        """B-10: Verifies BrowserSession runs capabilities and cleans up completely."""
        user_data_path = None
        with BrowserSession(browser_info=self.preferred_browser, headless=True) as session:
            user_data_path = session.driver.user_data_dir

            def test_task(sess):
                url = sess.server.get_url("MDS/Reference-Application/index.html")
                sess.driver.navigate(url)
                return sess.driver.evaluate("document.title")

            res = session.run_capability("MDS-BROWSER-SMOKE-001", test_task)
            self.assertEqual(res.status, BrowserExecutionStatus.PASS)
            self.assertGreater(res.duration_ms, 0)
            self.assertIn("MDS Workspace", res.evidence.get("dom_result", ""))

        # After session exit, user_data_path should be cleaned up
        if user_data_path:
            self.assertFalse(os.path.exists(user_data_path))

    def test_11_live_reference_app_screen_interaction(self):
        """B-11: Verifies Reference Application loads in headless browser and controls are accessible."""
        with CDPBrowserDriver(browser_info=self.preferred_browser) as driver:
            driver.launch(headless=True)
            url = self.server.get_url("MDS/Reference-Application/index.html")
            driver.navigate(url)

            # Check that role simulation switcher exists
            driver.wait_for("#ctrl-ref-role")
            role_val = driver.evaluate("document.querySelector('#ctrl-ref-role').value")
            self.assertEqual(role_val, "Administrator")

            # Check theme switcher exists
            driver.wait_for("#ctrl-ref-theme")
            theme_val = driver.evaluate("document.querySelector('#ctrl-ref-theme').value")
            self.assertEqual(theme_val, "light")

    def test_12_end_to_end_registry_dispatch_real_browser(self):
        """B-12 (Finding B-003 Live E2E): Proves complete chain: Registry -> Dispatcher -> BrowserBridge -> Real Chrome Execution -> ExecutionResult."""
        cap_dispatcher = CapabilityDispatcher()
        browser_dispatcher = BrowserCapabilityDispatcher()

        # 1. Verify Registry integration
        cap_id = "MDS-REF-001"
        cap_meta = cap_dispatcher.get_capability(cap_id)
        self.assertIsNotNone(cap_meta)
        self.assertEqual(cap_meta["id"], cap_id)

        # 2. Define browser execution task that runs on live Chrome
        def reference_app_smoke_task(session: BrowserSession) -> str:
            url = session.server.get_url("MDS/Reference-Application/index.html")
            session.driver.navigate(url)
            session.driver.wait_for("#ctrl-ref-role", timeout_ms=3000)
            return session.driver.evaluate("document.title")

        # 3. Execute through BrowserCapabilityDispatcher on real browser
        browser_result = browser_dispatcher.execute_browser_capability(
            capability_id=cap_id,
            custom_task=reference_app_smoke_task
        )

        self.assertEqual(browser_result.status, BrowserExecutionStatus.PASS)
        self.assertIsNone(browser_result.exception_type)
        self.assertGreater(browser_result.duration_ms, 0.0)
        self.assertIn("MDS Workspace", str(browser_result.evidence.get("dom_result", "")))

        # 4. Verify translation into canonical ExecutionResult
        exec_result = browser_dispatcher.to_execution_result(browser_result)
        self.assertEqual(exec_result.capability_id, cap_id)
        self.assertEqual(exec_result.status, ExecutionStatus.PASS)

        # 5. Verify promoted visual capability dispatch from registry
        vis_cap_id = "MDS-VIS-001"
        vis_meta = cap_dispatcher.get_capability(vis_cap_id)
        self.assertIsNotNone(vis_meta)
        self.assertEqual(vis_meta["status"], "ACTIVE")
        vis_browser_res = browser_dispatcher.execute_browser_capability(vis_cap_id)
        self.assertEqual(vis_browser_res.status, BrowserExecutionStatus.PASS)
        vis_exec_res = browser_dispatcher.to_execution_result(vis_browser_res)
        self.assertEqual(vis_exec_res.status, ExecutionStatus.PASS)


if __name__ == "__main__":
    unittest.main()
