#!/usr/bin/env python3
"""
Unit Tests for Local Test HTTP Server
Phase 9.7.4: Browser Automation Runner Bridge
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Tests ephemeral port allocation, open CORS headers, static file serving,
and clean socket release without requiring a browser process.
"""

import sys
import unittest
import urllib.request
import urllib.error
from pathlib import Path

# Add MDS/10-Testing to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from browser.local_server import LocalTestServer


class TestLocalServer(unittest.TestCase):
    """Category A: Unit tests executing without requiring a live browser."""

    def test_01_ephemeral_port_startup_and_shutdown(self):
        """S-01: Verifies server starts on port 0, binds an ephemeral port, and stops cleanly."""
        server = LocalTestServer(port=0)
        self.assertFalse(server.is_running)
        port = server.start()
        self.assertTrue(server.is_running)
        self.assertGreater(port, 1024)
        self.assertEqual(server.port, port)

        server.stop()
        self.assertFalse(server.is_running)

    def test_02_server_serves_static_files(self):
        """S-02: Verifies server serves repository files with HTTP 200."""
        with LocalTestServer() as server:
            url = server.get_url("MDS/10-Testing/browser/models.py")
            with urllib.request.urlopen(url) as resp:
                self.assertEqual(resp.status, 200)
                body = resp.read().decode("utf-8")
                self.assertIn("class BrowserType", body)

    def test_03_cors_headers_present(self):
        """S-03: Verifies Access-Control-Allow-Origin: * is sent on all static responses."""
        with LocalTestServer() as server:
            url = server.get_url("MDS/10-Testing/browser/models.py")
            with urllib.request.urlopen(url) as resp:
                headers = dict(resp.headers)
                self.assertEqual(headers.get("Access-Control-Allow-Origin"), "*")
                self.assertIn("GET", headers.get("Access-Control-Allow-Methods", ""))

    def test_04_cache_control_headers_present(self):
        """S-04: Verifies cache-busting headers are enforced for test determinism."""
        with LocalTestServer() as server:
            url = server.get_url("MDS/10-Testing/browser/models.py")
            with urllib.request.urlopen(url) as resp:
                headers = dict(resp.headers)
                self.assertIn("no-cache", headers.get("Cache-Control", ""))

    def test_05_options_preflight_handled(self):
        """S-05: Verifies OPTIONS requests return HTTP 200 for CORS preflight."""
        with LocalTestServer() as server:
            url = server.get_url("MDS/10-Testing/browser/models.py")
            req = urllib.request.Request(url, method="OPTIONS")
            with urllib.request.urlopen(req) as resp:
                self.assertEqual(resp.status, 200)
                self.assertEqual(resp.headers.get("Access-Control-Allow-Origin"), "*")

    def test_06_nonexistent_file_returns_404(self):
        """S-06: Verifies 404 is returned for non-existent files."""
        with LocalTestServer() as server:
            url = server.get_url("MDS/nonexistent_file_12345.xyz")
            with self.assertRaises(urllib.error.HTTPError) as ctx:
                urllib.request.urlopen(url)
            self.assertEqual(ctx.exception.code, 404)

    def test_07_get_url_formatting(self):
        """S-07: Verifies get_url cleans slashes and normalizes Windows backslashes."""
        with LocalTestServer() as server:
            url1 = server.get_url("MDS/Playground/index.html")
            url2 = server.get_url("/MDS/Playground/index.html")
            url3 = server.get_url("MDS\\Playground\\index.html")
            self.assertEqual(url1, f"http://127.0.0.1:{server.port}/MDS/Playground/index.html")
            self.assertEqual(url2, url1)
            self.assertEqual(url3, url1)


if __name__ == "__main__":
    unittest.main()
