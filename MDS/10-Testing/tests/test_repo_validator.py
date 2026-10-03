#!/usr/bin/env python3
"""
Unit Tests for MDS Repository Integrity Validator (Layer A)
Phase 9.7.3: Static Validation Suite & Scanners
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Validates Layer A rules: canonical directory layout, clean workspace,
intra-doc link verification with percent decoding, and zero npm dependencies.
"""

import sys
import unittest
from pathlib import Path

TESTING_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TESTING_DIR))

from static.repo_validator import RepoValidator, RepoValidationResult


class TestRepoValidator(unittest.TestCase):
    def setUp(self):
        self.validator = RepoValidator()

    # 1. Canonical Repository Structure (Current Workspace)
    def test_01_canonical_directory_layout(self):
        res = RepoValidationResult()
        self.validator.validate_directory_layout(res)
        self.assertTrue(res.is_valid, f"Directory layout violations: {res.errors}")
        self.assertEqual(res.metrics.get("total_canonical_dirs"), 20)
        self.assertEqual(len(res.metrics.get("missing_canonical_dirs", [])), 0)

    # 2. Missing Directory Detection (Simulated)
    def test_02_missing_directory_detected(self):
        res = RepoValidationResult()
        original_dirs = self.validator.CANONICAL_MDS_DIRS
        try:
            self.validator.CANONICAL_MDS_DIRS = original_dirs + ["99-Fictional-Layer"]
            self.validator.validate_directory_layout(res)
            self.assertFalse(res.is_valid)
            self.assertTrue(any("99-Fictional-Layer" in err for err in res.errors))
        finally:
            self.validator.CANONICAL_MDS_DIRS = original_dirs

    # 3. Clean Workspace (Zero stray files in current repository)
    def test_03_clean_workspace(self):
        res = RepoValidationResult()
        self.validator.validate_clean_workspace(res)
        self.assertTrue(res.is_valid, f"Stray scratch files found: {res.errors}")
        self.assertEqual(len(res.metrics.get("stray_files_found", [])), 0)

    # 4. Zero NPM Runtime Dependencies
    def test_04_zero_npm_dependencies(self):
        res = RepoValidationResult()
        self.validator.validate_zero_npm_dependencies(res)
        self.assertTrue(res.is_valid, f"Illegal npm artifacts detected: {res.errors}")
        self.assertEqual(len(res.metrics.get("npm_violations", [])), 0)

    # 5. Markdown Link Verification & Percent Decoding
    def test_05_markdown_links_scanned(self):
        res = RepoValidationResult()
        total_links, broken_count = self.validator.validate_markdown_links(res)
        self.assertGreater(total_links, 50, "Should have verified over 50 intra-doc links")
        self.assertIn("markdown_files_scanned", res.metrics)
        self.assertGreater(res.metrics["markdown_files_scanned"], 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
