#!/usr/bin/env python3
"""
Unit Tests for MDS Capability Execution Dispatch Adapter (Resolving F-04)
Phase 9.7.3: Static Validation Suite & Scanners
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Validates runner resolution across all 170 capabilities in registry.json,
confirming 100% dispatchability of active assertions and strict preservation
of deferred status without fabrication.
"""

import sys
import unittest
from pathlib import Path

TESTING_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TESTING_DIR))

from static.dispatch_adapter import CapabilityDispatcher, ExecutionStatus


class TestDispatchAdapter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dispatcher = CapabilityDispatcher()

    # 1. Total Capabilities Count (170 Unique Defined IDs)
    def test_01_total_capabilities_count(self):
        self.assertEqual(len(self.dispatcher.capabilities), 170)

    # 2. 100% of Active Capabilities Resolvable (170 / 170)
    def test_02_all_active_capabilities_dispatchable(self):
        active, resolved, failures = self.dispatcher.verify_all_dispatchable()
        self.assertEqual(active, 170)
        self.assertEqual(resolved, 170)
        self.assertEqual(len(failures), 0, f"Dispatch failures: {failures}")

    # 3. 0 Deferred Capabilities in Canonical Registry (All 170 Promoted)
    def test_03_deferred_capabilities_gated(self):
        deferred_ids = [c["id"] for c in self.dispatcher.capabilities.values() if c.get("status") == "DEFERRED"]
        self.assertEqual(len(deferred_ids), 0)

    # 4. Standalone Test Runner Resolution
    def test_04_standalone_test_runner_resolution(self):
        # Reference App
        ok, msg, target = self.dispatcher.resolve_runner("MDS-REF-001")
        self.assertTrue(ok)
        self.assertIsNotNone(target)
        self.assertIn("test_01_core_files_exist", msg)

        # Playground
        ok_p, msg_p, target_p = self.dispatcher.resolve_runner("MDS-PLG-001")
        self.assertTrue(ok_p)
        self.assertIsNotNone(target_p)
        self.assertIn("test_01_core_files_exist", msg_p)

        # DSSE
        ok_d, msg_d, target_d = self.dispatcher.resolve_runner("MDS-DSS-001")
        self.assertTrue(ok_d)
        self.assertIsNotNone(target_d)

    # 5. Master Harness Composite Capability Resolution
    def test_05_master_harness_resolution(self):
        # Tokens
        ok_t, msg_t, target_t = self.dispatcher.resolve_runner("MDS-TKN-001")
        self.assertTrue(ok_t)
        self.assertIn("run_token_tests", msg_t)

        # DSSE Composite MDS-DSS-000 (Wraps 37 assertions)
        ok_d, msg_d, target_d = self.dispatcher.resolve_runner("MDS-DSS-000")
        self.assertTrue(ok_d)
        self.assertIn("run_dsse_tests", msg_d)

        # Responsive
        ok_r, msg_r, target_r = self.dispatcher.resolve_runner("MDS-RWD-001")
        self.assertTrue(ok_r)
        self.assertIn("run_responsive_tests", msg_r)

    # 6. Unknown Capability Error Handling
    def test_06_unknown_capability_handled(self):
        ok, msg, target = self.dispatcher.resolve_runner("MDS-UNKNOWN-999")
        self.assertFalse(ok)
        self.assertIn("Unknown capability ID", msg)
        self.assertIsNone(target)

        res = self.dispatcher.execute_capability("MDS-UNKNOWN-999")
        self.assertEqual(res.status, ExecutionStatus.ERROR)


if __name__ == "__main__":
    unittest.main(verbosity=2)
