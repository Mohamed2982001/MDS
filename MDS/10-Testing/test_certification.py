"""
Master Design System (MDS) — Unit Tests for Production Certification Engine
Phase 10.4: MDS v1.0.0 Production Certification Gate
Layer 13: Implementation, Tooling & Operationalization
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.certification.models import (
    CANONICAL_EVIDENCE_MANIFEST_PATH,
    PRODUCTION_CERTIFICATE_PATH,
    STANDALONE_TRUSTED_SEAL_PATH,
    ZERO_WAIVER_DOMAIN,
    GateResult,
    GateStatus,
    canonical_json_serialize,
    compute_canonical_hash,
)
from tools.certification.gates import GateEvaluator
from tools.certification.cli import build_parser, handle_verify_certificate


class TestCertificationModels(unittest.TestCase):
    def test_zero_waiver_domain_contains_required_gates(self):
        self.assertIn("Gate_A", ZERO_WAIVER_DOMAIN)
        self.assertIn("Gate_B", ZERO_WAIVER_DOMAIN)
        self.assertIn("Gate_D", ZERO_WAIVER_DOMAIN)
        self.assertIn("Gate_F1", ZERO_WAIVER_DOMAIN)
        self.assertIn("Gate_I_03", ZERO_WAIVER_DOMAIN)

    def test_canonical_json_serialize_is_deterministic(self):
        obj1 = {"b": 2, "a": 1, "c": [3, 2, 1]}
        obj2 = {"c": [3, 2, 1], "a": 1, "b": 2}
        s1 = canonical_json_serialize(obj1)
        s2 = canonical_json_serialize(obj2)
        self.assertEqual(s1, s2)
        self.assertEqual(s1, '{"a":1,"b":2,"c":[3,2,1]}')

    def test_compute_canonical_hash_excludes_keys_correctly(self):
        data = {"foo": "bar", "certificate_integrity_digest": "dummy_digest"}
        h1, s1 = compute_canonical_hash(data, exclude_keys=["certificate_integrity_digest"])
        h2, s2 = compute_canonical_hash({"foo": "bar"})
        self.assertEqual(h1, h2)
        self.assertEqual(s1, s2)

    def test_gate_result_to_dict(self):
        res = GateResult(
            gate_id="Gate_A",
            name="Determinism",
            status=GateStatus.PASS,
            blockers=0,
            majors=0,
            minors=0,
            evidence_digest="abc123hash",
        )
        d = res.to_dict()
        self.assertEqual(d["name"], "Determinism")
        self.assertEqual(d["status"], "PASS")
        self.assertEqual(d["blockers"], 0)
        self.assertEqual(d["evidence_digest"], "abc123hash")


class TestCertificationGates(unittest.TestCase):
    def setUp(self):
        self.workspace_root = Path(__file__).resolve().parent.parent.parent
        self.dist_dir = self.workspace_root / "dist"

    def test_gate_f1_toolchain_compliance(self):
        evaluator = GateEvaluator(self.workspace_root, self.dist_dir)
        res = evaluator.evaluate_gate_f1()
        self.assertEqual(res.status, GateStatus.PASS)
        self.assertEqual(res.blockers, 0)

    def test_gate_l_rejects_unauthorized_signatory(self):
        evaluator = GateEvaluator(self.workspace_root, self.dist_dir)
        dummy_prior = [
            GateResult(gate_id="Gate_A", name="Test", status=GateStatus.PASS)
        ]
        res = evaluator.evaluate_gate_l(dummy_prior, authorized_by="Unauthorized Person")
        self.assertEqual(res.status, GateStatus.FAIL)
        self.assertEqual(res.blockers, 1)

    def test_gate_l_rejects_if_blockers_present(self):
        evaluator = GateEvaluator(self.workspace_root, self.dist_dir)
        dummy_prior = [
            GateResult(gate_id="Gate_A", name="Test", status=GateStatus.FAIL, blockers=1)
        ]
        res = evaluator.evaluate_gate_l(dummy_prior, authorized_by="Mohamed Khalid")
        self.assertEqual(res.status, GateStatus.FAIL)
        self.assertEqual(res.blockers, 1)

    def test_gate_l_approves_when_clean_and_authorized(self):
        evaluator = GateEvaluator(self.workspace_root, self.dist_dir)
        dummy_prior = [
            GateResult(gate_id="Gate_A", name="Test", status=GateStatus.PASS, blockers=0, majors=0)
        ]
        res = evaluator.evaluate_gate_l(dummy_prior, authorized_by="Mohamed Khalid")
        self.assertEqual(res.status, GateStatus.PASS)
        self.assertEqual(res.blockers, 0)


class TestCertificationCLI(unittest.TestCase):
    def test_cli_parser_builds_successfully(self):
        parser = build_parser()
        self.assertIsNotNone(parser)
        args = parser.parse_args(["certify", "--epoch", "1790812800"])
        self.assertEqual(args.subcommand, "certify")
        self.assertEqual(args.epoch, 1790812800)


if __name__ == "__main__":
    unittest.main()
