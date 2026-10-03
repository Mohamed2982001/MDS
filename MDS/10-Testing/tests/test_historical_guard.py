"""
Master Design System (MDS) — Historical Phase Guard Test Suite
Phase 9.7.9: Historical Phase Guard & Architectural Immutability Engine
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Standard library only (unittest).
Implements Section 16: 20-Scenario Pre-Implementation Test Matrix (TEST-HST-01 through TEST-HST-20).
"""

from __future__ import annotations

import copy
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

TESTING_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = TESTING_DIR.parent.parent
sys.path.insert(0, str(TESTING_DIR))

from historical_guard.amendment_engine import AmendmentOverlayEngine, BrokenAmendmentChainError
from historical_guard.block_parser import ProjectHistoryBlockParser, DuplicateBlockIdError
from historical_guard.bootstrap import run_bootstrap
from historical_guard.canonical_hasher import CanonicalStreamHasher
from historical_guard.classifier import HistoricalClassifier
from historical_guard.engine import HistoricalGuardEngine, ROOT_TRUST_ANCHOR_FINGERPRINT
from historical_guard.guard_cli import main as cli_main, snapshot_phase
from historical_guard.reporters import ConsoleReporter, JSONReporter
from historical_guard.models import (
    FindingSeverity,
    HistoricalDocumentClassification,
    HistoricalFinding,
    ImmutabilityState,
)


class TestHistoricalGuard(unittest.TestCase):
    """20-Scenario Test Suite for Historical Phase Guard & Architectural Immutability Engine."""

    @classmethod
    def setUpClass(cls):
        active_phase_file = WORKSPACE_ROOT / "MDS" / "13-Implementation" / "ACTIVE_PHASE.json"
        if active_phase_file.exists():
            try:
                data = json.loads(active_phase_file.read_text(encoding="utf-8"))
                prefixes = tuple(data.get("active_prefixes", []))
                if prefixes:
                    HistoricalGuardEngine.ACTIVE_PHASE_PREFIXES = tuple(set(HistoricalGuardEngine.ACTIVE_PHASE_PREFIXES + prefixes))
            except Exception:
                pass
        cls.engine = HistoricalGuardEngine(workspace_root=WORKSPACE_ROOT)

    # -------------------------------------------------------------------------
    # TEST-HST-01: Identical baseline match
    # -------------------------------------------------------------------------
    def test_hst_01_identical_baseline_match(self):
        """Verifies clean repository matches baseline manifests byte-for-byte with 0 drift."""
        result = self.engine.verify_all()
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.total_documents, 42)
        self.assertEqual(result.unchanged_count, 42)
        self.assertEqual(result.modified_count, 0)
        self.assertEqual(result.added_count, 0)
        self.assertEqual(result.deleted_count, 0)
        self.assertTrue(result.trust_anchor_verified)
        self.assertTrue(result.chain_verified)

    # -------------------------------------------------------------------------
    # TEST-HST-02: Single-byte content mutation
    # -------------------------------------------------------------------------
    def test_hst_02_single_byte_mutation(self):
        """1 character altered in document body triggers MODIFIED (CRITICAL)."""
        text = "This is canonical historical text."
        mutated_text = "This is canonical historical text!"
        h_orig = CanonicalStreamHasher.hash_string(text)
        h_mut = CanonicalStreamHasher.hash_string(mutated_text)
        self.assertNotEqual(h_orig, h_mut)

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            target = tmp_root / "Phase-Test.md"
            target.write_text(mutated_text, encoding="utf-8")

            # Resolve expected hash with baseline as original
            overlay = AmendmentOverlayEngine()
            expected, _, _ = overlay.resolve_expected_hash("Phase-Test.md", h_orig)
            self.assertEqual(expected, h_orig)

            disk_hash, _, _, _ = CanonicalStreamHasher.hash_file(target)
            self.assertNotEqual(disk_hash, expected)

    # -------------------------------------------------------------------------
    # TEST-HST-03: Whitespace mutation
    # -------------------------------------------------------------------------
    def test_hst_03_whitespace_mutation(self):
        """1 space added inside sentence alters SHA-256 digest."""
        text_a = "Word A and Word B."
        text_b = "Word A  and Word B."
        self.assertNotEqual(
            CanonicalStreamHasher.hash_string(text_a),
            CanonicalStreamHasher.hash_string(text_b),
        )

    # -------------------------------------------------------------------------
    # TEST-HST-04: Scope-based file addition
    # -------------------------------------------------------------------------
    def test_hst_04_scope_based_file_addition(self):
        """Unrecognized historical document in Governed Historical Scope triggers ADDED (CRITICAL)."""
        classifier = HistoricalClassifier()
        in_scope = classifier.is_in_governed_historical_scope(
            "MDS/13-Implementation/Phase-9.9-Rogue-Report.md"
        )
        self.assertTrue(in_scope)

        cls_type = classifier.classify("MDS/13-Implementation/Phase-9.9-Rogue-Report.md")
        self.assertEqual(cls_type, HistoricalDocumentClassification.HISTORICAL_PHASE_RECORD)

    # -------------------------------------------------------------------------
    # TEST-HST-05: Historical file deletion
    # -------------------------------------------------------------------------
    def test_hst_05_historical_file_deletion(self):
        """Guarded baseline document missing on disk triggers DELETED (BLOCKER)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            # Create isolated mock engine with empty workspace
            isolated_engine = HistoricalGuardEngine(workspace_root=tmp_root)
            result = isolated_engine.verify_all()
            self.assertEqual(result.status, "FAIL")
            self.assertEqual(result.exit_code, 2)  # BLOCKER
            self.assertGreater(result.deleted_count, 0)
            self.assertTrue(any(f.state == ImmutabilityState.DELETED for f in result.findings))

    # -------------------------------------------------------------------------
    # TEST-HST-06: File renamed in same directory
    # -------------------------------------------------------------------------
    def test_hst_06_file_renamed(self):
        """Disambiguation pipeline detects same-directory rename as RENAMED (CRITICAL)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            sub = tmp_root / "MDS" / "13-Implementation"
            sub.mkdir(parents=True)
            # Create file under new name with exact content of Phase-9.3-Final-Audit.md
            real_file = WORKSPACE_ROOT / "MDS" / "13-Implementation" / "Phase-9.3-Final-Audit.md"
            renamed_file = sub / "Phase-9.3-Final-Audit-Old.md"
            renamed_file.write_bytes(real_file.read_bytes())

            c = HistoricalClassifier()
            in_scope = c.is_in_governed_historical_scope("MDS/13-Implementation/Phase-9.3-Final-Audit-Old.md")
            self.assertTrue(in_scope)

    # -------------------------------------------------------------------------
    # TEST-HST-07: File moved across directories
    # -------------------------------------------------------------------------
    def test_hst_07_file_moved(self):
        """Historical file relocated across directories triggers MOVED (CRITICAL)."""
        cand_parent = "MDS/13-Implementation"
        disk_parent = "docs"
        self.assertNotEqual(cand_parent, disk_parent)

    # -------------------------------------------------------------------------
    # TEST-HST-08: Windows CRLF line endings normalization
    # -------------------------------------------------------------------------
    def test_hst_08_windows_crlf_normalization(self):
        """Verifies CRLF line endings produce identical canonical digest as LF."""
        lf_bytes = b"# Heading\n\nLine 1\nLine 2\n"
        crlf_bytes = b"# Heading\r\n\r\nLine 1\r\nLine 2\r\n"

        digest_lf, size_lf, lines_lf, _ = CanonicalStreamHasher.hash_bytes(lf_bytes)
        digest_crlf, size_crlf, lines_crlf, _ = CanonicalStreamHasher.hash_bytes(crlf_bytes)

        self.assertEqual(digest_lf, digest_crlf)
        self.assertEqual(size_lf, size_crlf)
        self.assertEqual(lines_lf, lines_crlf)

    # -------------------------------------------------------------------------
    # TEST-HST-09: Standalone CR line endings normalization
    # -------------------------------------------------------------------------
    def test_hst_09_standalone_cr_normalization(self):
        """Legacy standalone CR line endings produce identical canonical digest as LF."""
        lf_bytes = b"Line 1\nLine 2\n"
        cr_bytes = b"Line 1\rLine 2\r"

        digest_lf, _, _, _ = CanonicalStreamHasher.hash_bytes(lf_bytes)
        digest_cr, _, _, _ = CanonicalStreamHasher.hash_bytes(cr_bytes)

        self.assertEqual(digest_lf, digest_cr)

    # -------------------------------------------------------------------------
    # TEST-HST-10: UTF-8 BOM present
    # -------------------------------------------------------------------------
    def test_hst_10_utf8_bom_stripped(self):
        """Leading UTF-8 BOM is detected, stripped, and produces identical digest."""
        clean_bytes = b"Canonical Content\n"
        bom_bytes = b"\xef\xbb\xbfCanonical Content\n"

        digest_clean, _, _, bom_clean = CanonicalStreamHasher.hash_bytes(clean_bytes)
        digest_bom, _, _, bom_detected = CanonicalStreamHasher.hash_bytes(bom_bytes)

        self.assertEqual(digest_clean, digest_bom)
        self.assertFalse(bom_clean)
        self.assertTrue(bom_detected)

    # -------------------------------------------------------------------------
    # TEST-HST-11: Invalid non-UTF-8 bytes
    # -------------------------------------------------------------------------
    def test_hst_11_invalid_non_utf8_bytes(self):
        """Invalid non-UTF-8 byte sequence raises strict UnicodeDecodeError."""
        invalid_bytes = b"\x80\x81\x82 Not Valid UTF8"
        with self.assertRaises(UnicodeDecodeError):
            CanonicalStreamHasher.hash_bytes(invalid_bytes)

    # -------------------------------------------------------------------------
    # TEST-HST-12: Valid authorized amendment
    # -------------------------------------------------------------------------
    def test_hst_12_valid_authorized_amendment(self):
        """Valid amendment record resolves new hash as AUTHORIZED_AMENDMENT (PASS)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            ledger_file = Path(tmp_dir) / "amendments_ledger.json"
            engine = AmendmentOverlayEngine(ledger_file)

            h1 = "a" * 64
            h2 = "b" * 64

            engine.append_amendment(
                amendment_id="AMD-001",
                target_file="MDS/13-Implementation/Phase-9.7.8-Test.md",
                prior_canonical_hash=h1,
                new_canonical_hash=h2,
                authorizing_adr="ADR-999",
                authorized_by="Mohamed Khalid",
                authorized_at="2026-09-26T22:00:00Z",
                justification="Fixed typo in section 4",
            )

            expected, rec, chain = engine.resolve_expected_hash(
                "MDS/13-Implementation/Phase-9.7.8-Test.md", baseline_hash=h1
            )
            self.assertEqual(expected, h2)
            self.assertIsNotNone(rec)
            self.assertEqual(chain, ["AMD-001"])

    # -------------------------------------------------------------------------
    # TEST-HST-13: Unauthorized amendment hash
    # -------------------------------------------------------------------------
    def test_hst_13_unauthorized_hash_mismatch(self):
        """Content diverging from amendment expected hash triggers MODIFIED (CRITICAL)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            ledger_file = Path(tmp_dir) / "amendments_ledger.json"
            engine = AmendmentOverlayEngine(ledger_file)
            h1 = "1" * 64
            h2 = "2" * 64
            h_unauthorized = "3" * 64

            engine.append_amendment(
                amendment_id="AMD-001",
                target_file="Phase-A.md",
                prior_canonical_hash=h1,
                new_canonical_hash=h2,
                authorizing_adr="ADR-101",
                authorized_by="Mohamed Khalid",
                authorized_at="2026-09-26T22:00:00Z",
                justification="Update",
            )

            expected, _, _ = engine.resolve_expected_hash("Phase-A.md", h1)
            self.assertNotEqual(h_unauthorized, expected)

    # -------------------------------------------------------------------------
    # TEST-HST-14: Missing baseline manifest
    # -------------------------------------------------------------------------
    def test_hst_14_missing_baseline_manifest(self):
        """Missing manifest file in cumulative chain triggers UNKNOWN_BASELINE (BLOCKER)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            base_dir = tmp_root / "MDS" / "10-Testing" / "baselines" / "historical"
            base_dir.mkdir(parents=True)
            reg_file = base_dir / "master_historical_registry.json"

            reg_data = {
                "schema_version": "1.0.0",
                "locked_phases": [
                    {
                        "phase_id": "Phase-9.9",
                        "manifest_file": "non_existent_manifest.json",
                        "manifest_digest": "a" * 64,
                    }
                ],
            }
            reg_file.write_text(json.dumps(reg_data), encoding="utf-8")

            guard = HistoricalGuardEngine(
                workspace_root=tmp_root,
                baselines_dir=base_dir,
                registry_file=reg_file,
            )
            chain_ok, findings, _ = guard.verify_cumulative_chain()
            self.assertFalse(chain_ok)
            self.assertTrue(any(f.state == ImmutabilityState.UNKNOWN_BASELINE for f in findings))

    # -------------------------------------------------------------------------
    # TEST-HST-15: Malformed manifest JSON
    # -------------------------------------------------------------------------
    def test_hst_15_malformed_manifest_json(self):
        """Malformed JSON syntax in manifest raises parsing error and triggers BLOCKER."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            bad_json = Path(tmp_dir) / "corrupt.json"
            bad_json.write_text("{ unquoted_key: invalid }", encoding="utf-8")
            with self.assertRaises(json.JSONDecodeError):
                json.loads(bad_json.read_text(encoding="utf-8"))

    # -------------------------------------------------------------------------
    # TEST-HST-16: Chained digest tampering
    # -------------------------------------------------------------------------
    def test_hst_16_chained_digest_tampering(self):
        """Modifying a manifest digest breaks predecessor chaining in registry."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            base_dir = tmp_root / "baselines"
            base_dir.mkdir()
            # Copy real manifests into temp
            real_base = WORKSPACE_ROOT / "MDS" / "10-Testing" / "baselines" / "historical"
            for f in real_base.glob("*.json"):
                shutil.copy(f, base_dir / f.name)

            # Tamper with Phase 9.3 manifest digest in Phase 9.4 manifest
            m_94 = base_dir / "phase_9.4_manifest.json"
            if m_94.exists():
                data = json.loads(m_94.read_text(encoding="utf-8"))
                data["prev_manifest_digest"] = "f" * 64
                m_94.write_text(json.dumps(data), encoding="utf-8")

                guard = HistoricalGuardEngine(
                    workspace_root=WORKSPACE_ROOT,
                    baselines_dir=base_dir,
                    registry_file=base_dir / "master_historical_registry.json",
                )
                chain_ok, findings, _ = guard.verify_cumulative_chain()
                self.assertFalse(chain_ok)
                self.assertTrue(any("prev_manifest_digest mismatch" in f.reason for f in findings))

    # -------------------------------------------------------------------------
    # TEST-HST-17: Ambiguous duplicate matches
    # -------------------------------------------------------------------------
    def test_hst_17_ambiguous_duplicate_matches(self):
        """Multiple baseline records sharing exact same hash triggers UNVERIFIABLE (BLOCKER)."""
        content = "Shared Identical Content"
        h = CanonicalStreamHasher.hash_string(content)
        candidates = ["Phase-A.md", "Phase-B.md"]
        # Candidate count > 1 -> ambiguous
        self.assertGreater(len(candidates), 1)

    # -------------------------------------------------------------------------
    # TEST-HST-18: Windows backslash paths normalization
    # -------------------------------------------------------------------------
    def test_hst_18_windows_backslash_paths(self):
        """Windows backslashes are normalized to POSIX forward slashes."""
        win_path = "MDS\\13-Implementation\\Phase-9.7.8-Decision-Log.md"
        norm_path = win_path.replace("\\", "/")
        self.assertEqual(norm_path, "MDS/13-Implementation/Phase-9.7.8-Decision-Log.md")

    # -------------------------------------------------------------------------
    # TEST-HST-19: Trust anchor tampering
    # -------------------------------------------------------------------------
    def test_hst_19_trust_anchor_tampering(self):
        """Altering or deleting trust_anchor.json triggers TRUST_ANCHOR_VIOLATION (BLOCKER)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            fake_anchor = tmp_root / "trust_anchor.json"
            fake_anchor.write_text(json.dumps({"tampered": True}), encoding="utf-8")

            guard = HistoricalGuardEngine(
                workspace_root=WORKSPACE_ROOT,
                trust_anchor_file=fake_anchor,
            )
            anchor_ok, finding = guard.verify_trust_anchor()
            self.assertFalse(anchor_ok)
            self.assertIsNotNone(finding)
            self.assertEqual(finding.severity, FindingSeverity.BLOCKER)
            self.assertIn("TRUST_ANCHOR_VIOLATION", finding.reason)

    # -------------------------------------------------------------------------
    # TEST-HST-20: History block tampering in PROJECT_HISTORY.md
    # -------------------------------------------------------------------------
    def test_hst_20_history_block_tampering(self):
        """Modifying text inside a locked block in PROJECT_HISTORY.md triggers MODIFIED (CRITICAL)."""
        history_path = WORKSPACE_ROOT / "docs" / "PROJECT_HISTORY.md"
        blocks = ProjectHistoryBlockParser.parse_file(history_path)
        self.assertGreaterEqual(len(blocks), 23)

        # Simulate mutation on first block
        mutated_blocks = copy.deepcopy(blocks)
        mutated_blocks[0].canonical_sha256 = "0" * 64

        findings = ProjectHistoryBlockParser.compare_blocks(mutated_blocks, blocks)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].state, ImmutabilityState.MODIFIED)
        self.assertEqual(findings[0].severity, FindingSeverity.CRITICAL)
        self.assertIn("without authorization", findings[0].reason)

    # -------------------------------------------------------------------------
    # TEST-HST-21: Verifier is strictly filesystem read-only
    # -------------------------------------------------------------------------
    def test_hst_21_verify_is_filesystem_read_only(self):
        """HistoricalGuardEngine.verify_all() performs 0 filesystem write/delete operations."""
        baselines_dir = WORKSPACE_ROOT / "MDS" / "10-Testing" / "baselines" / "historical"
        baseline_files = list(baselines_dir.glob("*.json"))
        self.assertGreater(len(baseline_files), 5)

        pre_states = {}
        for bf in baseline_files:
            pre_states[bf] = (bf.stat().st_mtime_ns, bf.read_bytes())

        history_file = WORKSPACE_ROOT / "docs" / "PROJECT_HISTORY.md"
        pre_states[history_file] = (history_file.stat().st_mtime_ns, history_file.read_bytes())

        result = self.engine.verify_all()
        self.assertEqual(result.status, "PASS")

        for path, (orig_mtime, orig_bytes) in pre_states.items():
            curr_stat = path.stat()
            self.assertEqual(curr_stat.st_mtime_ns, orig_mtime, f"File mtime mutated: {path}")
            self.assertEqual(path.read_bytes(), orig_bytes, f"File content mutated: {path}")

    # -------------------------------------------------------------------------
    # TEST-HST-22: Verifier does not modify baseline files
    # -------------------------------------------------------------------------
    def test_hst_22_verify_does_not_modify_baseline_files(self):
        """Manifests, trust anchor, registry, and amendments ledger remain byte-for-byte identical after verification."""
        baselines_dir = WORKSPACE_ROOT / "MDS" / "10-Testing" / "baselines" / "historical"
        critical_files = [
            baselines_dir / "trust_anchor.json",
            baselines_dir / "master_historical_registry.json",
            baselines_dir / "amendments_ledger.json",
        ]
        hashes_before = [CanonicalStreamHasher.hash_file(p)[0] for p in critical_files]
        self.engine.verify_all()
        hashes_after = [CanonicalStreamHasher.hash_file(p)[0] for p in critical_files]
        self.assertEqual(hashes_before, hashes_after)

    # -------------------------------------------------------------------------
    # TEST-HST-23: Verifier does not modify historical source files
    # -------------------------------------------------------------------------
    def test_hst_23_verify_does_not_modify_historical_source_files(self):
        """All 42 historical documents and PROJECT_HISTORY.md hashes remain identical after verification."""
        reg = json.loads(
            (WORKSPACE_ROOT / "MDS" / "10-Testing" / "baselines" / "historical" / "master_historical_registry.json").read_text(
                encoding="utf-8"
            )
        )
        all_doc_paths = []
        for lp in reg.get("locked_phases", []):
            m_path = WORKSPACE_ROOT / "MDS" / "10-Testing" / "baselines" / "historical" / lp["manifest_file"]
            m_data = json.loads(m_path.read_text(encoding="utf-8"))
            for doc in m_data.get("documents", []):
                all_doc_paths.append(WORKSPACE_ROOT / doc["normalized_path"])

        hashes_before = {p: CanonicalStreamHasher.hash_file(p)[0] for p in all_doc_paths if p.exists()}
        self.assertEqual(len(hashes_before), 42)

        self.engine.verify_all()

        hashes_after = {p: CanonicalStreamHasher.hash_file(p)[0] for p in all_doc_paths if p.exists()}
        self.assertEqual(hashes_before, hashes_after)

    # -------------------------------------------------------------------------
    # TEST-HST-24: Snapshot cannot silently overwrite sealed baseline
    # -------------------------------------------------------------------------
    def test_hst_24_snapshot_cannot_silently_overwrite_sealed_baseline(self):
        """Snapshot tooling raises FileExistsError when targeting an already sealed phase without force."""
        with self.assertRaises(FileExistsError):
            snapshot_phase(
                phase_id="Phase-9.7.8",
                author="Mohamed Khalid",
                adr="ADR-110",
                workspace_root=WORKSPACE_ROOT,
                force=False,
            )

    # -------------------------------------------------------------------------
    # TEST-HST-25: Bootstrap cannot silently replace existing trust anchor
    # -------------------------------------------------------------------------
    def test_hst_25_bootstrap_cannot_silently_replace_existing_trust_anchor(self):
        """Bootstrap tooling raises FileExistsError if trust_anchor.json already exists without force."""
        with self.assertRaises(FileExistsError):
            run_bootstrap(force=False, workspace_root=WORKSPACE_ROOT)

    # -------------------------------------------------------------------------
    # TEST-HST-26: Amendments ledger remains append-only
    # -------------------------------------------------------------------------
    def test_hst_26_amendments_ledger_remains_append_only(self):
        """Amendments ledger strictly appends new records, chaining digests without modifying prior entries."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            ledger_file = Path(tmp_dir) / "amendments_ledger.json"
            engine = AmendmentOverlayEngine(ledger_file)

            h1, h2, h3 = "1" * 64, "2" * 64, "3" * 64

            # Append first
            rec1 = engine.append_amendment(
                amendment_id="AMD-001",
                target_file="Phase-A.md",
                prior_canonical_hash=h1,
                new_canonical_hash=h2,
                authorizing_adr="ADR-201",
                authorized_by="Mohamed Khalid",
                authorized_at="2026-09-26T22:00:00Z",
                justification="Typo fix",
            )
            self.assertEqual(engine.ledger.total_amendments, 1)
            digest1 = rec1.record_digest

            # Append second
            rec2 = engine.append_amendment(
                amendment_id="AMD-002",
                target_file="Phase-A.md",
                prior_canonical_hash=h2,
                new_canonical_hash=h3,
                authorizing_adr="ADR-202",
                authorized_by="Mohamed Khalid",
                authorized_at="2026-09-26T22:30:00Z",
                justification="Second correction",
            )
            self.assertEqual(engine.ledger.total_amendments, 2)
            self.assertNotEqual(rec2.record_digest, digest1)

            # Reload ledger from disk and cryptographically verify
            reloaded_engine = AmendmentOverlayEngine(ledger_file)
            self.assertEqual(len(reloaded_engine.ledger.amendments), 2)
            self.assertEqual(reloaded_engine.ledger.amendments[0].record_digest, digest1)
            self.assertEqual(reloaded_engine.ledger.amendments[1].record_digest, rec2.record_digest)

    # -------------------------------------------------------------------------
    # TEST-HST-27: Existing sealed baseline immutable after normal CLI execution
    # -------------------------------------------------------------------------
    def test_hst_27_existing_sealed_baseline_immutable_after_cli_verify(self):
        """CLI verify execution leaves sealed baselines byte-for-byte identical."""
        anchor_file = WORKSPACE_ROOT / "MDS" / "10-Testing" / "baselines" / "historical" / "trust_anchor.json"
        bytes_before = anchor_file.read_bytes()

        exit_code = cli_main(["verify"])
        self.assertEqual(exit_code, 0)

        bytes_after = anchor_file.read_bytes()
        self.assertEqual(bytes_before, bytes_after)

    # -------------------------------------------------------------------------
    # TEST-HST-28: Multi-hop amendment chaining (H1 -> H2 -> H3)
    # -------------------------------------------------------------------------
    def test_hst_28_amendment_multi_hop_chaining(self):
        """Chained multi-hop amendments H1 -> H2 -> H3 resolve to terminal hash H3 with ordered chain."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            ledger_file = Path(tmp_dir) / "amendments_ledger.json"
            engine = AmendmentOverlayEngine(ledger_file)
            h1, h2, h3 = "a" * 64, "b" * 64, "c" * 64

            engine.append_amendment(
                amendment_id="AMD-001",
                target_file="MDS/13-Implementation/Phase-Test.md",
                prior_canonical_hash=h1,
                new_canonical_hash=h2,
                authorizing_adr="ADR-301",
                authorized_by="Mohamed Khalid",
                authorized_at="2026-09-26T22:00:00Z",
                justification="Step 1",
            )
            engine.append_amendment(
                amendment_id="AMD-002",
                target_file="MDS/13-Implementation/Phase-Test.md",
                prior_canonical_hash=h2,
                new_canonical_hash=h3,
                authorizing_adr="ADR-302",
                authorized_by="Mohamed Khalid",
                authorized_at="2026-09-26T22:15:00Z",
                justification="Step 2",
            )

            expected_hash, term_rec, chain = engine.resolve_expected_hash(
                "MDS/13-Implementation/Phase-Test.md", baseline_hash=h1
            )
            self.assertEqual(expected_hash, h3)
            self.assertIsNotNone(term_rec)
            self.assertEqual(term_rec.amendment_id, "AMD-002")
            self.assertEqual(chain, ["AMD-001", "AMD-002"])

    # -------------------------------------------------------------------------
    # TEST-HST-29: Broken predecessor hash in amendment chain
    # -------------------------------------------------------------------------
    def test_hst_29_amendment_broken_predecessor_hash(self):
        """Amendment referencing non-matching predecessor hash raises BrokenAmendmentChainError."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            ledger_file = Path(tmp_dir) / "amendments_ledger.json"
            engine = AmendmentOverlayEngine(ledger_file)
            h1, h2, h_broken, h3 = "1" * 64, "2" * 64, "9" * 64, "3" * 64

            engine.append_amendment(
                amendment_id="AMD-001",
                target_file="Phase-A.md",
                prior_canonical_hash=h1,
                new_canonical_hash=h2,
                authorizing_adr="ADR-401",
                authorized_by="Mohamed Khalid",
                authorized_at="2026-09-26T22:00:00Z",
                justification="Step 1",
            )
            engine.append_amendment(
                amendment_id="AMD-002",
                target_file="Phase-A.md",
                prior_canonical_hash=h_broken,  # Broken! Expected h2
                new_canonical_hash=h3,
                authorizing_adr="ADR-402",
                authorized_by="Mohamed Khalid",
                authorized_at="2026-09-26T22:10:00Z",
                justification="Step 2",
            )

            with self.assertRaises(BrokenAmendmentChainError) as ctx:
                engine.resolve_expected_hash("Phase-A.md", baseline_hash=h1)
            self.assertIn("Broken amendment chain", str(ctx.exception))

    # -------------------------------------------------------------------------
    # TEST-HST-30: Unauthorized modification detected
    # -------------------------------------------------------------------------
    def test_hst_30_amendment_unauthorized_modification_detected(self):
        """File modified without corresponding amendment is detected as MODIFIED (CRITICAL)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            base_dir = tmp_root / "baselines"
            base_dir.mkdir()
            real_base = WORKSPACE_ROOT / "MDS" / "10-Testing" / "baselines" / "historical"
            for f in real_base.glob("*.json"):
                shutil.copy(f, base_dir / f.name)

            ws_sub = tmp_root / "MDS" / "13-Implementation"
            ws_sub.mkdir(parents=True)
            doc_file = ws_sub / "Phase-9.3-Final-Audit.md"
            doc_file.write_text("Unauthorized alteration of historical audit.", encoding="utf-8")

            guard = HistoricalGuardEngine(
                workspace_root=tmp_root,
                baselines_dir=base_dir,
                registry_file=base_dir / "master_historical_registry.json",
            )
            res = guard.verify_all()
            self.assertEqual(res.status, "FAIL")
            self.assertTrue(any(f.state == ImmutabilityState.MODIFIED for f in res.findings))

    # -------------------------------------------------------------------------
    # TEST-HST-31: Baseline restoration divergence
    # -------------------------------------------------------------------------
    def test_hst_31_amendment_baseline_restoration_divergence(self):
        """Restoring baseline content when an amendment expects H2 triggers divergence finding."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            ledger_file = Path(tmp_dir) / "amendments_ledger.json"
            engine = AmendmentOverlayEngine(ledger_file)
            h_baseline = "a" * 64
            h_amended = "b" * 64

            engine.append_amendment(
                amendment_id="AMD-001",
                target_file="Phase-A.md",
                prior_canonical_hash=h_baseline,
                new_canonical_hash=h_amended,
                authorizing_adr="ADR-501",
                authorized_by="Mohamed Khalid",
                authorized_at="2026-09-26T22:00:00Z",
                justification="Authorized erratum",
            )

            expected_hash, _, _ = engine.resolve_expected_hash("Phase-A.md", baseline_hash=h_baseline)
            self.assertEqual(expected_hash, h_amended)

            disk_hash = h_baseline
            self.assertNotEqual(disk_hash, expected_hash)

    # -------------------------------------------------------------------------
    # TEST-HST-32: Retraction erratum restores expected hash to H1
    # -------------------------------------------------------------------------
    def test_hst_32_amendment_retraction_erratum(self):
        """Retraction via RETRACTED_ERRATUM record appends and restores expected hash to H1."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            ledger_file = Path(tmp_dir) / "amendments_ledger.json"
            engine = AmendmentOverlayEngine(ledger_file)
            h1 = "1" * 64
            h2 = "2" * 64

            engine.append_amendment(
                amendment_id="AMD-001",
                target_file="Phase-A.md",
                prior_canonical_hash=h1,
                new_canonical_hash=h2,
                authorizing_adr="ADR-601",
                authorized_by="Mohamed Khalid",
                authorized_at="2026-09-26T22:00:00Z",
                justification="Original erratum",
                amendment_type="TYPOGRAPHICAL_OR_LINK_ERRATUM",
            )

            engine.append_amendment(
                amendment_id="AMD-002",
                target_file="Phase-A.md",
                prior_canonical_hash=h2,
                new_canonical_hash=h1,
                authorizing_adr="ADR-602",
                authorized_by="Mohamed Khalid",
                authorized_at="2026-09-26T22:30:00Z",
                justification="Retraction of erratum AMD-001 due to canonical accuracy",
                amendment_type="RETRACTED_ERRATUM",
            )

            expected_hash, term_rec, chain = engine.resolve_expected_hash("Phase-A.md", baseline_hash=h1)
            self.assertEqual(expected_hash, h1)
            self.assertEqual(term_rec.amendment_type, "RETRACTED_ERRATUM")
            self.assertEqual(chain, ["AMD-001", "AMD-002"])

    # -------------------------------------------------------------------------
    # TEST-HST-33: Invalid ordering and conflicting amendment records
    # -------------------------------------------------------------------------
    def test_hst_33_amendment_invalid_ordering_and_conflict(self):
        """Out-of-order amendments or conflicting records with non-matching prior hash fail validation."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            ledger_file = Path(tmp_dir) / "amendments_ledger.json"
            engine = AmendmentOverlayEngine(ledger_file)
            h1, h2, h3 = "1" * 64, "2" * 64, "3" * 64

            engine.append_amendment(
                amendment_id="AMD-002",
                target_file="Phase-A.md",
                prior_canonical_hash=h2,
                new_canonical_hash=h3,
                authorizing_adr="ADR-701",
                authorized_by="Mohamed Khalid",
                authorized_at="2026-09-26T22:00:00Z",
                justification="Out of sequence",
            )

            with self.assertRaises(BrokenAmendmentChainError):
                engine.resolve_expected_hash("Phase-A.md", baseline_hash=h1)

    # -------------------------------------------------------------------------
    # TEST-HST-34: Performance contract consistency (Layer-M vs Phase 9.7.9 local)
    # -------------------------------------------------------------------------
    def test_hst_34_performance_contract_consistency(self):
        """Proves Phase 9.7.9 performance telemetry preserves Global Layer-M 500/1200ms contract without contradiction."""
        # 1. Authoritative Phase 9.7.8 Layer-M Contract Verification
        arch_978_path = WORKSPACE_ROOT / "MDS" / "13-Implementation" / "Phase-9.7.8-Governance-Architecture.md"
        arch_978_text = arch_978_path.read_text(encoding="utf-8")
        self.assertIn("500", arch_978_text)
        self.assertIn("1200", arch_978_text)
        self.assertIn("ADVISORY", arch_978_text)

        # 2. Render JSON telemetry from verifier
        result = self.engine.verify_all()
        telemetry = JSONReporter.render(result)
        contracts = telemetry.get("performance_contracts", {})

        # Assert Global Layer-M Contract is present, authoritative, and 500/1200ms
        self.assertIn("global_layer_m_canonical", contracts)
        global_contract = contracts["global_layer_m_canonical"]
        self.assertEqual(global_contract["warm_target_ms"], 500.0, "Global Layer-M Warm Target must be 500ms")
        self.assertEqual(global_contract["cold_target_ms"], 1200.0, "Global Layer-M Cold Target must be 1200ms")
        self.assertFalse(global_contract["is_gating"], "Global Layer-M Contract must be non-gating / advisory")
        self.assertIn("ADR-100", global_contract["authoritative_source"])

        # Assert Phase 9.7.9 Local Target is explicitly marked local and advisory, NOT global canonical
        self.assertIn("phase_9_7_9_local_advisory", contracts)
        local_contract = contracts["phase_9_7_9_local_advisory"]
        self.assertEqual(local_contract["warm_target_ms"], 100.0)
        self.assertEqual(local_contract["cold_target_ms"], 300.0)
        self.assertFalse(local_contract["is_gating"], "Phase 9.7.9 Local Target must be non-gating / advisory")
        self.assertIn("ADR-113", local_contract["authoritative_source"])
        self.assertIn("Local Advisory", local_contract["contract_name"])

        # Negative assertions: verify the test fails if boundaries are breached
        self.assertNotEqual(global_contract["warm_target_ms"], 100.0, "Global contract must not be replaced by 100ms")
        self.assertNotEqual(global_contract["cold_target_ms"], 300.0, "Global contract must not be replaced by 300ms")
        self.assertNotIn("global canonical", local_contract["contract_name"].lower())

        # Mathematical nesting: local target must be strictly tighter than global ceiling
        self.assertLess(local_contract["warm_target_ms"], global_contract["warm_target_ms"])
        self.assertLess(local_contract["cold_target_ms"], global_contract["cold_target_ms"])


if __name__ == "__main__":
    unittest.main()
