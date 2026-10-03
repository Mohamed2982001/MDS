"""
MDS Amendment Ledger & Overlay Resolution Engine
Phase 9.7.9: Historical Phase Guard & Architectural Immutability Engine
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Implements ADR-109 and ADR-118:
- Immutable Baseline + Amendment Overlay Resolution Model
- Internal cryptographic hash chain in amendments_ledger.json
- Chaining validation and broken predecessor detection
- Retraction protocol via append-only RETRACTED_ERRATUM records
- Linear acyclic dependency DAG
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

from .models import AmendmentRecord, AmendmentLedger


class BrokenAmendmentChainError(ValueError):
    """Raised when an amendment references a mismatched predecessor hash."""
    pass


class AmendmentLedgerCorruptionError(ValueError):
    """Raised when the internal cryptographic chain of the ledger is broken."""
    pass


class AmendmentOverlayEngine:
    """Manages the append-only amendment ledger and resolves expected historical hashes."""

    GENESIS_DIGEST = "0" * 64

    def __init__(self, ledger_file: Optional[Path] = None):
        self.ledger_file = ledger_file
        self.ledger: Optional[AmendmentLedger] = None
        if self.ledger_file and self.ledger_file.exists():
            self.load_ledger()
        else:
            self.ledger = AmendmentLedger(
                schema_version="1.0.0",
                guard_version="1.0.0",
                ledger_id="MDS-AMENDMENTS-LEDGER-v1",
                total_amendments=0,
                ledger_digest=self.GENESIS_DIGEST,
                amendments=[],
            )

    @classmethod
    def compute_record_digest(cls, prev_digest: str, rec: AmendmentRecord) -> str:
        """Computes chained cryptographic digest for a single amendment entry."""
        payload = f"{prev_digest}|{rec.amendment_id}|{rec.target_file}|{rec.prior_canonical_hash}|{rec.new_canonical_hash}|{rec.authorizing_adr}|{rec.authorized_by}|{rec.authorized_at}|{rec.amendment_type}|{rec.justification}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def load_ledger(self) -> AmendmentLedger:
        """Loads and cryptographically verifies amendments_ledger.json from disk."""
        if not self.ledger_file or not self.ledger_file.exists():
            raise FileNotFoundError(f"Amendment ledger file not found: {self.ledger_file}")

        data = json.loads(self.ledger_file.read_text(encoding="utf-8"))
        ledger = AmendmentLedger.from_dict(data)

        # Cryptographically verify the internal chain
        current_digest = self.GENESIS_DIGEST
        for idx, entry in enumerate(ledger.amendments):
            computed = self.compute_record_digest(current_digest, entry)
            if entry.record_digest and entry.record_digest != computed:
                raise AmendmentLedgerCorruptionError(
                    f"Cryptographic chain break at amendment index {idx} ('{entry.amendment_id}'): "
                    f"recorded '{entry.record_digest}' != computed '{computed}'"
                )
            current_digest = computed

        if ledger.ledger_digest != current_digest:
            raise AmendmentLedgerCorruptionError(
                f"Ledger terminal digest mismatch: recorded '{ledger.ledger_digest}' != computed '{current_digest}'"
            )

        self.ledger = ledger
        return ledger

    def save_ledger(self) -> None:
        """Serializes verified ledger to disk."""
        if not self.ledger_file:
            raise ValueError("Cannot save ledger: ledger_file path not provided.")

        self.ledger_file.parent.mkdir(parents=True, exist_ok=True)
        data = self.ledger.to_dict()
        self.ledger_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def resolve_expected_hash(
        self, target_file: str, baseline_hash: str
    ) -> Tuple[str, Optional[AmendmentRecord], List[str]]:
        """
        Mechanically resolves expected hash using Model A (Immutable Baseline + Amendment Overlay).
        Returns: (expected_hash, terminal_amendment_or_None, list_of_chained_amendment_ids)
        """
        norm_target = target_file.replace("\\", "/")
        if not self.ledger or not self.ledger.amendments:
            return baseline_hash, None, []

        matching = [a for a in self.ledger.amendments if a.target_file == norm_target]
        if not matching:
            return baseline_hash, None, []

        # Validate linear amendment chain
        current_hash = baseline_hash
        chain_ids: List[str] = []
        terminal_record: Optional[AmendmentRecord] = None

        for idx, record in enumerate(matching):
            if record.prior_canonical_hash != current_hash:
                raise BrokenAmendmentChainError(
                    f"Broken amendment chain on '{norm_target}' at amendment '{record.amendment_id}': "
                    f"prior_hash '{record.prior_canonical_hash}' does not match expected predecessor '{current_hash}'."
                )
            current_hash = record.new_canonical_hash
            chain_ids.append(record.amendment_id)
            terminal_record = record

        return current_hash, terminal_record, chain_ids

    def append_amendment(
        self,
        amendment_id: str,
        target_file: str,
        prior_canonical_hash: str,
        new_canonical_hash: str,
        authorizing_adr: str,
        authorized_by: str,
        authorized_at: str,
        justification: str,
        amendment_type: str = "TYPOGRAPHICAL_OR_LINK_ERRATUM",
    ) -> AmendmentRecord:
        """
        Appends an audited amendment record, computing its chained digest.
        """
        if not self.ledger:
            self.ledger = AmendmentLedger(
                schema_version="1.0.0",
                guard_version="1.0.0",
                ledger_id="MDS-AMENDMENTS-LEDGER-v1",
                total_amendments=0,
                ledger_digest=self.GENESIS_DIGEST,
                amendments=[],
            )

        norm_target = target_file.replace("\\", "/")

        rec = AmendmentRecord(
            amendment_id=amendment_id,
            target_file=norm_target,
            prior_canonical_hash=prior_canonical_hash,
            new_canonical_hash=new_canonical_hash,
            authorizing_adr=authorizing_adr,
            authorized_by=authorized_by,
            authorized_at=authorized_at,
            amendment_type=amendment_type,
            justification=justification,
        )

        prev_digest = self.ledger.ledger_digest or self.GENESIS_DIGEST
        rec.record_digest = self.compute_record_digest(prev_digest, rec)

        self.ledger.amendments.append(rec)
        self.ledger.total_amendments = len(self.ledger.amendments)
        self.ledger.ledger_digest = rec.record_digest

        if self.ledger_file:
            self.save_ledger()

        return rec
