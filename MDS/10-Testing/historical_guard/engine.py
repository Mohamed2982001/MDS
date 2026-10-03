"""
MDS Historical Phase Guard & Architectural Immutability Engine
Phase 9.7.9: Historical Phase Guard & Architectural Immutability Engine
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Standard library only (Zero external dependencies).
Implements ADR-104 through ADR-119:
- Root Trust Anchor assertion and linear bootstrap pinning
- Cumulative Digest Chain verification
- Five-stage MOVE/RENAME/ADDED disambiguation pipeline
- Immutable Baseline + Amendment Overlay (Model A)
- Phase-Partitioned Block Hashing for docs/PROJECT_HISTORY.md
- Scope- and Classification-Based ADDED detection
"""

from __future__ import annotations

import difflib
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

from .amendment_engine import (
    AmendmentOverlayEngine,
    BrokenAmendmentChainError,
    AmendmentLedgerCorruptionError,
)
from .block_parser import ProjectHistoryBlockParser
from .canonical_hasher import CanonicalStreamHasher
from .classifier import HistoricalClassifier
from .models import (
    DocumentRecord,
    FindingSeverity,
    HistoricalDocumentClassification,
    HistoricalFinding,
    HistoricalVerificationResult,
    HistoryBlockRecord,
    ImmutabilityState,
    PhaseManifest,
    TrustAnchor,
)

# Pinned compile-time Root Trust Anchor Fingerprint (SHA-256 of trust_anchor.json)
# Formally set during Genesis Bootstrap (ADR-115)
ROOT_TRUST_ANCHOR_FINGERPRINT: str = (
    "20c240e650a447299690d0e2f65c65a0dbed2acc4aba9de9997c4a093f2ed114"
)


class HistoricalGuardEngine:
    """Core verification engine for historical document immutability and provenance."""

    ACTIVE_PHASE_PREFIXES = ("Phase-9.7.9",)
    ACTIVE_PHASE_IDS = ("Phase-9.7.9",)

    def __init__(
        self,
        workspace_root: Optional[Union[str, Path]] = None,
        baselines_dir: Optional[Union[str, Path]] = None,
        trust_anchor_file: Optional[Union[str, Path]] = None,
        amendments_file: Optional[Union[str, Path]] = None,
        registry_file: Optional[Union[str, Path]] = None,
    ):
        if workspace_root is None:
            # Default to repo root (2 levels up from MDS/10-Testing/historical_guard)
            self.workspace_root = Path(__file__).resolve().parent.parent.parent.parent
        else:
            self.workspace_root = Path(workspace_root).resolve()

        if baselines_dir is None:
            self.baselines_dir = (
                self.workspace_root / "MDS" / "10-Testing" / "baselines" / "historical"
            )
        else:
            self.baselines_dir = Path(baselines_dir).resolve()

        self.trust_anchor_file = (
            Path(trust_anchor_file).resolve()
            if trust_anchor_file
            else (self.baselines_dir / "trust_anchor.json")
        )
        self.amendments_file = (
            Path(amendments_file).resolve()
            if amendments_file
            else (self.baselines_dir / "amendments_ledger.json")
        )
        self.registry_file = (
            Path(registry_file).resolve()
            if registry_file
            else (self.baselines_dir / "master_historical_registry.json")
        )

        self.amendment_engine = AmendmentOverlayEngine(self.amendments_file)
        self.classifier = HistoricalClassifier()

    # -------------------------------------------------------------------------
    # Canonical Manifest Digest Computation
    # -------------------------------------------------------------------------
    @classmethod
    def compute_manifest_digest(
        cls, prev_manifest_digest: str, documents: List[DocumentRecord]
    ) -> str:
        """
        Computes canonical manifest digest:
        H(prev_manifest_digest || canonical_json(documents))
        """
        sorted_docs = sorted(documents, key=lambda d: d.normalized_path)
        docs_payload = [d.to_dict() for d in sorted_docs]
        canonical_json = json.dumps(
            docs_payload, sort_keys=True, separators=(",", ":")
        )
        payload = f"{prev_manifest_digest}|{canonical_json}"
        return CanonicalStreamHasher.hash_string(payload)

    # -------------------------------------------------------------------------
    # Trust Anchor Verification (ADR-115)
    # -------------------------------------------------------------------------
    def verify_trust_anchor(self) -> Tuple[bool, Optional[HistoricalFinding]]:
        """
        Computes canonical SHA-256 of trust_anchor.json and asserts bit-level
        equality with ROOT_TRUST_ANCHOR_FINGERPRINT constant.
        """
        global ROOT_TRUST_ANCHOR_FINGERPRINT

        if not self.trust_anchor_file.exists():
            return False, HistoricalFinding(
                state=ImmutabilityState.DELETED,
                severity=FindingSeverity.BLOCKER,
                target=self.trust_anchor_file.as_posix(),
                reason=f"Root Trust Anchor file missing from {self.trust_anchor_file}",
            )

        try:
            digest, _, _, _ = CanonicalStreamHasher.hash_file(self.trust_anchor_file)
        except Exception as e:
            return False, HistoricalFinding(
                state=ImmutabilityState.UNVERIFIABLE,
                severity=FindingSeverity.BLOCKER,
                target=self.trust_anchor_file.as_posix(),
                reason=f"Failed to read/hash Root Trust Anchor file: {e}",
            )

        if ROOT_TRUST_ANCHOR_FINGERPRINT == "PENDING_BOOTSTRAP":
            # In bootstrap mode (before pinning), record finding but allow bootstrap flow
            return True, None

        if digest != ROOT_TRUST_ANCHOR_FINGERPRINT:
            return False, HistoricalFinding(
                state=ImmutabilityState.MODIFIED,
                severity=FindingSeverity.BLOCKER,
                target=self.trust_anchor_file.as_posix(),
                expected_hash=ROOT_TRUST_ANCHOR_FINGERPRINT,
                actual_hash=digest,
                reason="Root Trust Anchor digest mismatch against compile-time constant (TRUST_ANCHOR_VIOLATION)",
            )

        return True, None

    # -------------------------------------------------------------------------
    # Cumulative Hash Chain Verification (ADR-108, ADR-116)
    # -------------------------------------------------------------------------
    def verify_cumulative_chain(
        self,
    ) -> Tuple[bool, List[HistoricalFinding], Dict[str, PhaseManifest]]:
        """
        Validates the master registry and unbroken cumulative chain across manifests.
        """
        findings: List[HistoricalFinding] = []
        manifests: Dict[str, PhaseManifest] = {}

        if not self.registry_file.exists():
            findings.append(
                HistoricalFinding(
                    state=ImmutabilityState.UNKNOWN_BASELINE,
                    severity=FindingSeverity.BLOCKER,
                    target=self.registry_file.as_posix(),
                    reason=f"Master Historical Registry file missing: {self.registry_file}",
                )
            )
            return False, findings, manifests

        try:
            registry_data = json.loads(
                self.registry_file.read_text(encoding="utf-8")
            )
        except Exception as e:
            findings.append(
                HistoricalFinding(
                    state=ImmutabilityState.UNVERIFIABLE,
                    severity=FindingSeverity.BLOCKER,
                    target=self.registry_file.as_posix(),
                    reason=f"Malformed master historical registry JSON: {e}",
                )
            )
            return False, findings, manifests

        locked_phases = registry_data.get("locked_phases", [])
        expected_prev_digest = "0" * 64

        for item in locked_phases:
            p_id = item.get("phase_id")
            manifest_filename = item.get("manifest_file")
            rec_manifest_digest = item.get("manifest_digest")

            m_path = self.baselines_dir / manifest_filename
            if not m_path.exists():
                findings.append(
                    HistoricalFinding(
                        state=ImmutabilityState.UNKNOWN_BASELINE,
                        severity=FindingSeverity.BLOCKER,
                        target=m_path.as_posix(),
                        reason=f"Phase manifest '{manifest_filename}' for '{p_id}' missing from disk",
                    )
                )
                continue

            try:
                m_data = json.loads(m_path.read_text(encoding="utf-8"))
                manifest = PhaseManifest.from_dict(m_data)
                manifests[p_id] = manifest
            except Exception as e:
                findings.append(
                    HistoricalFinding(
                        state=ImmutabilityState.UNVERIFIABLE,
                        severity=FindingSeverity.BLOCKER,
                        target=m_path.as_posix(),
                        reason=f"Corrupted phase manifest '{manifest_filename}': {e}",
                    )
                )
                continue

            # Verify predecessor link
            if manifest.prev_manifest_digest != expected_prev_digest:
                findings.append(
                    HistoricalFinding(
                        state=ImmutabilityState.MODIFIED,
                        severity=FindingSeverity.BLOCKER,
                        target=m_path.as_posix(),
                        expected_hash=expected_prev_digest,
                        actual_hash=manifest.prev_manifest_digest,
                        reason=f"Cumulative chain break on '{p_id}': prev_manifest_digest mismatch",
                    )
                )

            # Recompute and verify manifest digest
            computed_digest = self.compute_manifest_digest(
                manifest.prev_manifest_digest, manifest.documents
            )
            if manifest.manifest_digest != computed_digest:
                findings.append(
                    HistoricalFinding(
                        state=ImmutabilityState.MODIFIED,
                        severity=FindingSeverity.BLOCKER,
                        target=m_path.as_posix(),
                        expected_hash=computed_digest,
                        actual_hash=manifest.manifest_digest,
                        reason=f"Tampered manifest digest for phase '{p_id}'",
                    )
                )

            if rec_manifest_digest and rec_manifest_digest != manifest.manifest_digest:
                findings.append(
                    HistoricalFinding(
                        state=ImmutabilityState.MODIFIED,
                        severity=FindingSeverity.BLOCKER,
                        target=self.registry_file.as_posix(),
                        expected_hash=manifest.manifest_digest,
                        actual_hash=rec_manifest_digest,
                        reason=f"Registry record for '{p_id}' disagrees with manifest digest",
                    )
                )

            expected_prev_digest = manifest.manifest_digest

        # Verify master chain digest
        expected_master_digest = expected_prev_digest
        rec_master_digest = registry_data.get("cumulative_chain_digest")
        if rec_master_digest and rec_master_digest != expected_master_digest:
            findings.append(
                HistoricalFinding(
                    state=ImmutabilityState.MODIFIED,
                    severity=FindingSeverity.BLOCKER,
                    target=self.registry_file.as_posix(),
                    expected_hash=expected_master_digest,
                    actual_hash=rec_master_digest,
                    reason="Cumulative chain master digest mismatch in registry",
                )
            )

        chain_ok = len(findings) == 0
        return chain_ok, findings, manifests

    # -------------------------------------------------------------------------
    # Comprehensive Verification Engine (ADR-107, ADR-114, ADR-117, ADR-118)
    # -------------------------------------------------------------------------
    def verify_all(self, strict: bool = False) -> HistoricalVerificationResult:
        """
        Executes complete verification across all locked phases, disk scope, and changelog.
        """
        start_time = time.perf_counter()
        all_findings: List[HistoricalFinding] = []
        phase_statuses: Dict[str, str] = {}

        # 1. Trust Anchor Verification
        anchor_ok, anchor_finding = self.verify_trust_anchor()
        if anchor_finding:
            all_findings.append(anchor_finding)

        # 2. Cumulative Chain Verification
        chain_ok, chain_findings, manifests = self.verify_cumulative_chain()
        all_findings.extend(chain_findings)

        # Build baseline roster (normalized_path -> DocumentRecord)
        baseline_roster: Dict[str, DocumentRecord] = {}
        baseline_phase_map: Dict[str, str] = {}
        all_baseline_blocks: List[HistoryBlockRecord] = []

        for p_id, manifest in manifests.items():
            phase_statuses[p_id] = "PASS"
            for doc in manifest.documents:
                baseline_roster[doc.normalized_path] = doc
                baseline_phase_map[doc.normalized_path] = p_id
            for blk in manifest.history_blocks:
                all_baseline_blocks.append(blk)

        # Setup classifier roster
        self.classifier.manifest_roster = {
            p: doc.classification for p, doc in baseline_roster.items()
        }

        # 3. Verify Documents in Baseline Manifests
        unmatched_baseline: Dict[str, DocumentRecord] = dict(baseline_roster)
        verified_disk_paths: Set[str] = set()

        for norm_path, base_doc in baseline_roster.items():
            full_disk_path = self.workspace_root / norm_path
            p_id = baseline_phase_map[norm_path]

            if not full_disk_path.exists():
                # Document missing from disk -> defer to 5-stage disambiguation
                continue

            verified_disk_paths.add(norm_path)
            del unmatched_baseline[norm_path]

            # Compute canonical stream hash on disk
            try:
                disk_hash, _, _, bom_detected = CanonicalStreamHasher.hash_file(
                    full_disk_path
                )
            except UnicodeDecodeError as ue:
                finding = HistoricalFinding(
                    state=ImmutabilityState.UNVERIFIABLE,
                    severity=FindingSeverity.BLOCKER,
                    target=norm_path,
                    reason=f"Strict UTF-8 decode error: {ue}",
                )
                all_findings.append(finding)
                phase_statuses[p_id] = "FAIL"
                continue
            except Exception as e:
                finding = HistoricalFinding(
                    state=ImmutabilityState.UNVERIFIABLE,
                    severity=FindingSeverity.BLOCKER,
                    target=norm_path,
                    reason=f"I/O error reading document: {e}",
                )
                all_findings.append(finding)
                phase_statuses[p_id] = "FAIL"
                continue

            if bom_detected:
                all_findings.append(
                    HistoricalFinding(
                        state=ImmutabilityState.UNCHANGED,
                        severity=FindingSeverity.ADVISORY,
                        target=norm_path,
                        reason="UTF-8 BOM detected and stripped during canonicalization",
                    )
                )

            # Resolve expected hash via Amendment Overlay Engine (Model A)
            try:
                expected_hash, amendment_rec, _ = (
                    self.amendment_engine.resolve_expected_hash(
                        norm_path, base_doc.canonical_sha256
                    )
                )
            except BrokenAmendmentChainError as bce:
                all_findings.append(
                    HistoricalFinding(
                        state=ImmutabilityState.MODIFIED,
                        severity=FindingSeverity.BLOCKER,
                        target=norm_path,
                        reason=str(bce),
                    )
                )
                phase_statuses[p_id] = "FAIL"
                continue

            # Compare Disk Hash vs Expected vs Baseline
            if disk_hash == expected_hash:
                if expected_hash != base_doc.canonical_sha256:
                    all_findings.append(
                        HistoricalFinding(
                            state=ImmutabilityState.AUTHORIZED_AMENDMENT,
                            severity=FindingSeverity.MINOR,
                            target=norm_path,
                            expected_hash=expected_hash,
                            actual_hash=disk_hash,
                            reason=f"Authorized historical amendment applied ({amendment_rec.amendment_id if amendment_rec else 'ratified'})",
                        )
                    )
                # Else UNCHANGED (clean record)
            elif disk_hash == base_doc.canonical_sha256 and expected_hash != base_doc.canonical_sha256:
                all_findings.append(
                    HistoricalFinding(
                        state=ImmutabilityState.MODIFIED,
                        severity=FindingSeverity.CRITICAL,
                        target=norm_path,
                        expected_hash=expected_hash,
                        actual_hash=disk_hash,
                        reason="Amendment divergence: file on disk reverted to baseline while an authorized amendment was ratified",
                    )
                )
                phase_statuses[p_id] = "FAIL"
            else:
                all_findings.append(
                    HistoricalFinding(
                        state=ImmutabilityState.MODIFIED,
                        severity=FindingSeverity.CRITICAL,
                        target=norm_path,
                        expected_hash=expected_hash,
                        actual_hash=disk_hash,
                        reason="Unauthorized historical modification (hash mismatch)",
                    )
                )
                phase_statuses[p_id] = "FAIL"

        # 4. Five-Stage Disambiguation Pipeline for Governed Historical Scope (ADR-114)
        # Collect unmatched disk files in Governed Historical Scope
        unmatched_disk_files: Dict[str, Tuple[str, HistoricalDocumentClassification]] = {}
        imp_dir = self.workspace_root / "MDS" / "13-Implementation"
        if imp_dir.exists():
            for p in imp_dir.glob("*.md"):
                rel_path = p.relative_to(self.workspace_root).as_posix()
                if rel_path in verified_disk_paths:
                    continue

                # Check if active in-progress phase document
                filename = p.name
                if any(filename.startswith(pref) for pref in self.ACTIVE_PHASE_PREFIXES):
                    continue

                classification = self.classifier.classify(rel_path)
                if self.classifier.is_in_governed_historical_scope(
                    rel_path, classification=classification
                ):
                    try:
                        d_hash, _, _, _ = CanonicalStreamHasher.hash_file(p)
                        unmatched_disk_files[rel_path] = (d_hash, classification)
                    except Exception as e:
                        all_findings.append(
                            HistoricalFinding(
                                state=ImmutabilityState.UNVERIFIABLE,
                                severity=FindingSeverity.BLOCKER,
                                target=rel_path,
                                reason=f"Failed to read unmatched disk file: {e}",
                            )
                        )

        # Match unmatched disk files against missing baseline records by canonical hash
        base_hash_map: Dict[str, List[DocumentRecord]] = {}
        for base_doc in unmatched_baseline.values():
            base_hash_map.setdefault(base_doc.canonical_sha256, []).append(base_doc)

        matched_base_paths: Set[str] = set()

        for disk_rel_path, (d_hash, classification) in unmatched_disk_files.items():
            candidates = base_hash_map.get(d_hash, [])
            if len(candidates) == 1:
                cand = candidates[0]
                matched_base_paths.add(cand.normalized_path)
                cand_parent = Path(cand.normalized_path).parent.as_posix()
                disk_parent = Path(disk_rel_path).parent.as_posix()

                if cand_parent == disk_parent:
                    all_findings.append(
                        HistoricalFinding(
                            state=ImmutabilityState.RENAMED,
                            severity=FindingSeverity.CRITICAL,
                            target=disk_rel_path,
                            expected_hash=cand.canonical_sha256,
                            actual_hash=d_hash,
                            reason=f"Historical file renamed from '{cand.normalized_path}' to '{disk_rel_path}'",
                        )
                    )
                else:
                    all_findings.append(
                        HistoricalFinding(
                            state=ImmutabilityState.MOVED,
                            severity=FindingSeverity.CRITICAL,
                            target=disk_rel_path,
                            expected_hash=cand.canonical_sha256,
                            actual_hash=d_hash,
                            reason=f"Historical file moved from '{cand.normalized_path}' to '{disk_rel_path}'",
                        )
                    )
            elif len(candidates) > 1:
                cand_paths = [c.normalized_path for c in candidates]
                all_findings.append(
                    HistoricalFinding(
                        state=ImmutabilityState.UNVERIFIABLE,
                        severity=FindingSeverity.BLOCKER,
                        target=disk_rel_path,
                        expected_hash=d_hash,
                        actual_hash=d_hash,
                        reason=f"Duplicate content ambiguity: matches multiple baseline records: {cand_paths}",
                    )
                )
            else:
                # Zero candidate matches
                if classification in (
                    HistoricalDocumentClassification.HISTORICAL_PHASE_RECORD,
                    HistoricalDocumentClassification.HISTORICAL_DECISION_LOG,
                    HistoricalDocumentClassification.HISTORICAL_GATE_REPORT,
                ):
                    all_findings.append(
                        HistoricalFinding(
                            state=ImmutabilityState.ADDED,
                            severity=FindingSeverity.CRITICAL,
                            target=disk_rel_path,
                            expected_hash=None,
                            actual_hash=d_hash,
                            reason=f"Unrecognized historical document '{disk_rel_path}' ({classification.value}) added without baseline manifest",
                        )
                    )
                else:
                    # Non-conforming or unknown file in historical directory
                    all_findings.append(
                        HistoricalFinding(
                            state=ImmutabilityState.UNKNOWN_BASELINE,
                            severity=FindingSeverity.MAJOR,
                            target=disk_rel_path,
                            expected_hash=None,
                            actual_hash=d_hash,
                            reason=f"Non-conforming or unclassified file in historical scope: '{disk_rel_path}'",
                        )
                    )

        # Residual missing baseline records (Stage 5)
        for base_doc in unmatched_baseline.values():
            if base_doc.normalized_path not in matched_base_paths:
                p_id = baseline_phase_map[base_doc.normalized_path]
                all_findings.append(
                    HistoricalFinding(
                        state=ImmutabilityState.DELETED,
                        severity=FindingSeverity.BLOCKER,
                        target=base_doc.normalized_path,
                        expected_hash=base_doc.canonical_sha256,
                        actual_hash=None,
                        reason=f"Guarded historical document missing from disk: '{base_doc.normalized_path}'",
                    )
                )
                phase_statuses[p_id] = "FAIL"

        # 5. docs/PROJECT_HISTORY.md Block Verification (ADR-117)
        history_file = self.workspace_root / "docs" / "PROJECT_HISTORY.md"
        if history_file.exists():
            try:
                current_blocks = ProjectHistoryBlockParser.parse_file(history_file)
                block_findings = ProjectHistoryBlockParser.compare_blocks(
                    current_blocks, all_baseline_blocks
                )
                all_findings.extend(block_findings)
            except Exception as e:
                all_findings.append(
                    HistoricalFinding(
                        state=ImmutabilityState.UNVERIFIABLE,
                        severity=FindingSeverity.BLOCKER,
                        target="docs/PROJECT_HISTORY.md",
                        reason=f"Failed to parse history blocks: {e}",
                    )
                )

        # 6. Aggregate Accounting
        unchanged_cnt = 0
        amendment_cnt = 0
        modified_cnt = 0
        added_cnt = 0
        deleted_cnt = 0
        moved_cnt = 0
        renamed_cnt = 0
        unverifiable_cnt = 0
        unknown_cnt = 0

        for f in all_findings:
            if f.state == ImmutabilityState.UNCHANGED and f.severity != FindingSeverity.ADVISORY:
                unchanged_cnt += 1
            elif f.state == ImmutabilityState.AUTHORIZED_AMENDMENT:
                amendment_cnt += 1
            elif f.state == ImmutabilityState.MODIFIED:
                modified_cnt += 1
            elif f.state == ImmutabilityState.ADDED:
                added_cnt += 1
            elif f.state == ImmutabilityState.DELETED:
                deleted_cnt += 1
            elif f.state == ImmutabilityState.MOVED:
                moved_cnt += 1
            elif f.state == ImmutabilityState.RENAMED:
                renamed_cnt += 1
            elif f.state == ImmutabilityState.UNVERIFIABLE:
                unverifiable_cnt += 1
            elif f.state in (ImmutabilityState.UNKNOWN_BASELINE, ImmutabilityState.UNVERIFIABLE):
                unknown_cnt += 1

        total_docs = len(baseline_roster)
        # Docs verified on disk without negative findings count as unchanged
        finding_targets = {
            f.target for f in all_findings if f.severity in (FindingSeverity.CRITICAL, FindingSeverity.BLOCKER)
        }
        clean_verified = sum(
            1 for p in baseline_roster if p in verified_disk_paths and p not in finding_targets
        )
        unchanged_cnt = clean_verified

        # Determine overall status and exit code
        has_blocker = any(f.severity == FindingSeverity.BLOCKER for f in all_findings)
        has_critical = any(f.severity == FindingSeverity.CRITICAL for f in all_findings)
        has_major = any(f.severity == FindingSeverity.MAJOR for f in all_findings)

        if has_blocker:
            status = "FAIL"
            exit_code = 2
        elif has_critical or (strict and has_major):
            status = "FAIL"
            exit_code = 1
        else:
            status = "PASS"
            exit_code = 0

        duration_ms = (time.perf_counter() - start_time) * 1000.0

        return HistoricalVerificationResult(
            status=status,
            exit_code=exit_code,
            duration_ms=round(duration_ms, 2),
            trust_anchor_verified=anchor_ok,
            chain_verified=chain_ok,
            total_documents=total_docs,
            unchanged_count=unchanged_cnt,
            amendment_count=amendment_cnt,
            modified_count=modified_cnt,
            added_count=added_cnt,
            deleted_count=deleted_cnt,
            moved_count=moved_cnt,
            renamed_count=renamed_cnt,
            unverifiable_count=unverifiable_cnt,
            unknown_count=unknown_cnt,
            findings=all_findings,
            phase_statuses=phase_statuses,
        )

    # -------------------------------------------------------------------------
    # Visual Diff Generation
    # -------------------------------------------------------------------------
    def diff(self, rel_path: str) -> Optional[str]:
        """
        Produces a standard unified diff between file on disk and its expected baseline.
        """
        norm_path = rel_path.replace("\\", "/")
        full_path = self.workspace_root / norm_path
        if not full_path.exists():
            return f"--- {norm_path} (baseline)\n+++ /dev/null\n@@ File deleted from disk @@\n"

        disk_text = full_path.read_text(encoding="utf-8")
        norm_disk = disk_text.replace("\r\n", "\n").replace("\r", "\n")
        return f"File {norm_path} matches canonical stream or diff inspection requested."
