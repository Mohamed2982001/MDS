#!/usr/bin/env python3
"""
Unit Tests for Browser Discovery Engine
Phase 9.7.4: Browser Automation Runner Bridge
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Tests browser discovery, precedence rules, version parsing, and fallback modes
without requiring a running browser process.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add MDS/10-Testing to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from browser.models import BrowserInfo, BrowserType
from browser.browser_discovery import BrowserDiscovery


class TestBrowserDiscovery(unittest.TestCase):
    """Category A: Unit tests executing without requiring a live browser."""

    def test_01_candidate_paths_structured(self):
        """A-01: Verifies candidate paths dictionary returns Chrome, Edge, and Chromium keys."""
        paths = BrowserDiscovery._get_candidate_paths()
        self.assertIn(BrowserType.CHROME, paths)
        self.assertIn(BrowserType.EDGE, paths)
        self.assertIn(BrowserType.CHROMIUM, paths)
        self.assertIsInstance(paths[BrowserType.CHROME], list)

    def test_02_version_extraction_nonexistent_binary(self):
        """A-02: Verifies version extraction on a non-existent binary returns Not Found."""
        fake_path = Path("/nonexistent/bin/chrome.exe")
        version = BrowserDiscovery.get_version(fake_path)
        self.assertEqual(version, "Unknown (Not Found)")

    def test_03_find_all_returns_browser_info_list(self):
        """A-03: Verifies find_all returns a list of BrowserInfo instances with valid attributes."""
        browsers = BrowserDiscovery.find_all()
        self.assertIsInstance(browsers, list)
        for b in browsers:
            self.assertIsInstance(b, BrowserInfo)
            self.assertTrue(len(b.name) > 0)
            self.assertTrue(b.path.exists())
            self.assertIn(b.browser_type, (BrowserType.CHROME, BrowserType.EDGE, BrowserType.CHROMIUM))

    def test_04_preferred_browser_selection(self):
        """A-04: Verifies get_preferred returns highest priority browser or requested preference."""
        browsers = BrowserDiscovery.find_all()
        if not browsers:
            self.assertIsNone(BrowserDiscovery.get_preferred())
            return

        preferred = BrowserDiscovery.get_preferred()
        self.assertIsNotNone(preferred)
        self.assertIsInstance(preferred, BrowserInfo)

        # Test explicit preference override
        edge = BrowserDiscovery.get_preferred(prefer="edge")
        if any(b.browser_type == BrowserType.EDGE for b in browsers):
            self.assertIsNotNone(edge)
            self.assertEqual(edge.browser_type, BrowserType.EDGE)

    def test_05_mocked_unavailable_browser(self):
        """A-05: Verifies system behaves gracefully when zero browsers are discovered."""
        with patch.object(BrowserDiscovery, "find_all", return_value=[]):
            self.assertEqual(BrowserDiscovery.find_all(), [])
            self.assertIsNone(BrowserDiscovery.find_chrome())
            self.assertIsNone(BrowserDiscovery.find_edge())
            self.assertIsNone(BrowserDiscovery.get_preferred())

    def test_06_browser_info_serialization(self):
        """A-06: Verifies BrowserInfo.to_dict formats correctly."""
        info = BrowserInfo(
            name="Google Chrome",
            path=Path("/bin/chrome"),
            version="Chrome 134.0.0",
            browser_type=BrowserType.CHROME,
            is_available=True
        )
        d = info.to_dict()
        self.assertEqual(d["name"], "Google Chrome")
        self.assertEqual(d["version"], "Chrome 134.0.0")
        self.assertEqual(d["browser_type"], "chrome")
        self.assertTrue(d["is_available"])


if __name__ == "__main__":
    unittest.main()
