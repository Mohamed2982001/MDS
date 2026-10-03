#!/usr/bin/env python3
"""
Unit Tests for MDS Capability Registry Validator
Covers all 12 mandatory failure modes and accounting integrity constraints.
"""

import sys
import os
import unittest
import copy
import json
from pathlib import Path

TESTING_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = TESTING_DIR.parent.parent
sys.path.insert(0, str(TESTING_DIR))

from registry.validator import RegistryValidator, ValidationResult

CANONICAL_REGISTRY_PATH = TESTING_DIR / "capabilities" / "registry.json"

class TestRegistryValidator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(CANONICAL_REGISTRY_PATH, "r", encoding="utf-8") as f:
            cls.canonical_data = json.load(f)
        cls.validator = RegistryValidator(workspace_root=WORKSPACE_ROOT)

    def get_clean_data(self):
        return copy.deepcopy(self.canonical_data)

    # 1. Valid registry
    def test_01_valid_canonical_registry(self):
        res = self.validator.validate(self.canonical_data)
        self.assertTrue(res.is_valid, f"Canonical registry should be valid, errors: {res.errors}")
        self.assertEqual(len(res.errors), 0)
        self.assertEqual(res.accounting["total_capabilities"], 170)
        self.assertEqual(res.accounting["unique_defined_ids"], 170)
        self.assertEqual(res.accounting["active_executable_assertions"], 170)
        self.assertEqual(res.accounting["deferred_capabilities"], 0)
        self.assertEqual(res.accounting["quarantined_capabilities"], 0)
        self.assertEqual(res.accounting["disabled_capabilities"], 0)
        self.assertEqual(res.accounting["wrapped_assertions"], 37)

    # 2. Duplicate ID
    def test_02_duplicate_id_detection(self):
        data = self.get_clean_data()
        # Duplicate the first capability
        dup_cap = copy.deepcopy(data["capabilities"][0])
        data["capabilities"].append(dup_cap)
        data["metadata"]["total_capabilities"] += 1
        res = self.validator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("Duplicate capability ID detected" in err for err in res.errors))

    # 3. Invalid layer
    def test_03_invalid_layer(self):
        data = self.get_clean_data()
        data["capabilities"][0]["layer"] = "Z_INVALID_LAYER"
        res = self.validator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("unknown layer: 'Z_INVALID_LAYER'" in err for err in res.errors))

    # 4. Invalid category
    def test_04_invalid_category(self):
        data = self.get_clean_data()
        data["capabilities"][0]["category"] = "EXPLORATORY_CHAOS"
        res = self.validator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("unknown category: 'EXPLORATORY_CHAOS'" in err for err in res.errors))

    # 5. Invalid status
    def test_05_invalid_status(self):
        data = self.get_clean_data()
        data["capabilities"][0]["status"] = "MAYBE_RUNNING"
        res = self.validator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("unknown status: 'MAYBE_RUNNING'" in err for err in res.errors))

    # 6. Invalid severity
    def test_06_invalid_severity(self):
        data = self.get_clean_data()
        data["capabilities"][0]["severity"] = "APOCALYPTIC"
        res = self.validator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("unknown severity: 'APOCALYPTIC'" in err for err in res.errors))

    # 7. Missing required field
    def test_07_missing_required_field(self):
        data = self.get_clean_data()
        del data["capabilities"][0]["owner"]
        res = self.validator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("missing required field: 'owner'" in err for err in res.errors))

    # 8. Deferred without reason
    def test_08_deferred_without_reason(self):
        data = self.get_clean_data()
        data["capabilities"][0]["status"] = "DEFERRED"
        data["capabilities"][0]["deferred_reason"] = None
        # Adjust metadata to avoid accounting mismatch masking this error
        data["metadata"]["accounting"]["active_executable_assertions"] -= 1
        data["metadata"]["accounting"]["deferred_capabilities"] += 1
        res = self.validator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("must specify a non-empty 'deferred_reason'" in err for err in res.errors))

    # 9. Quarantine without reason
    def test_09_quarantine_without_reason(self):
        data = self.get_clean_data()
        data["capabilities"][0]["status"] = "QUARANTINED"
        data["capabilities"][0]["quarantine_reason"] = "   "  # whitespace only
        data["metadata"]["accounting"]["active_executable_assertions"] -= 1
        data["metadata"]["accounting"]["quarantined_capabilities"] += 1
        res = self.validator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("must specify a non-empty 'quarantine_reason'" in err for err in res.errors))

    # 10. Invalid wrap reference
    def test_10_invalid_wrap_reference(self):
        data = self.get_clean_data()
        data["capabilities"][0]["wraps"] = ["MDS-FAKE-999"]
        res = self.validator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("references unknown wrapped ID: 'MDS-FAKE-999'" in err for err in res.errors))

        # Test self-wrap
        data2 = self.get_clean_data()
        cid = data2["capabilities"][0]["id"]
        data2["capabilities"][0]["wraps"] = [cid]
        res2 = self.validator.validate(data2)
        self.assertFalse(res2.is_valid)
        self.assertTrue(any("cannot wrap itself" in err for err in res2.errors))

    # 11. Circular dependency
    def test_11_circular_dependency(self):
        data = self.get_clean_data()
        # Cap 0 depends on Cap 1, Cap 1 depends on Cap 0
        cid0 = data["capabilities"][0]["id"]
        cid1 = data["capabilities"][1]["id"]
        data["capabilities"][0]["depends_on"] = [cid1]
        data["capabilities"][1]["depends_on"] = [cid0]
        res = self.validator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("Circular dependency detected" in err for err in res.errors))

    # 12. ACTIVE capability without runner
    def test_12_active_capability_without_runner(self):
        data = self.get_clean_data()
        data["capabilities"][0]["runner"] = None
        res = self.validator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("must specify an executable 'runner' object" in err for err in res.errors))

        # Test runner missing file
        data2 = self.get_clean_data()
        data2["capabilities"][0]["runner"] = {"file": "", "entrypoint": "test_foo", "type": "standalone_test"}
        res2 = self.validator.validate(data2)
        self.assertFalse(res2.is_valid)
        self.assertTrue(any("runner missing non-empty 'file'" in err for err in res2.errors))

    # Additional Bonus Integrity Tests
    def test_13_disabled_without_reason(self):
        data = self.get_clean_data()
        data["capabilities"][0]["status"] = "DISABLED"
        data["capabilities"][0]["disabled_reason"] = ""
        data["metadata"]["accounting"]["active_executable_assertions"] -= 1
        data["metadata"]["accounting"]["disabled_capabilities"] += 1
        res = self.validator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("must specify a non-empty 'disabled_reason'" in err for err in res.errors))

    def test_14_self_dependency(self):
        data = self.get_clean_data()
        cid = data["capabilities"][0]["id"]
        data["capabilities"][0]["depends_on"] = [cid]
        res = self.validator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("cannot depend on itself" in err for err in res.errors))

    def test_15_invalid_id_pattern(self):
        data = self.get_clean_data()
        data["capabilities"][0]["id"] = "INVALID_ID_FORMAT"
        res = self.validator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("does not match canonical pattern" in err for err in res.errors))

    # Phase 9.7.2 Remediation Tests (F-01, F-02, F-03)
    def test_16_derived_wrapped_assertions_count(self):
        """Verify wrapped_assertions is strictly derived from capability wraps lists."""
        data = self.get_clean_data()
        res = self.validator.validate(data)
        self.assertEqual(res.accounting["wrapped_assertions"], 37)

        # Remove wraps from MDS-DSS-000 and update metadata accounting to match
        for cap in data["capabilities"]:
            if cap["id"] == "MDS-DSS-000":
                cap["wraps"] = []
                break
        data["metadata"]["accounting"]["wrapped_assertions"] = 0
        res2 = self.validator.validate(data)
        self.assertTrue(res2.is_valid)
        self.assertEqual(res2.accounting["wrapped_assertions"], 0)

    def test_17_metadata_wrapped_mismatch(self):
        """Verify validator fails when metadata wrapped_assertions does not match derived wraps."""
        data = self.get_clean_data()
        data["metadata"]["accounting"]["wrapped_assertions"] = 99
        res = self.validator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("Accounting wrapped_assertions (99) != actual derived wrapped count (37)" in err for err in res.errors))

    def test_18_playground_runner_entrypoint_validity(self):
        """Verify all MDS-PLG-* capability entrypoints exist in test_playground.py (Fixes F-01)."""
        plg_caps = [c for c in self.canonical_data["capabilities"] if c["id"].startswith("MDS-PLG-")]
        self.assertEqual(len(plg_caps), 13)

        playground_test_file = WORKSPACE_ROOT / "MDS" / "Playground" / "tests" / "test_playground.py"
        self.assertTrue(playground_test_file.exists(), f"File missing: {playground_test_file}")
        playground_test_content = playground_test_file.read_text(encoding="utf-8")

        for cap in plg_caps:
            entrypoint = cap["runner"]["entrypoint"]
            self.assertIn(
                f"def {entrypoint}(",
                playground_test_content,
                f"Capability {cap['id']} entrypoint '{entrypoint}' not defined in test_playground.py!"
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)

