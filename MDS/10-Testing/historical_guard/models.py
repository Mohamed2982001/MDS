"""
MDS Historical Phase Guard — Data Models and Enums
Phase 9.7.9: Historical Phase Guard & Architectural Immutability Engine
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Any, Optional


class HistoricalDocumentClassification(str, Enum):
    HISTORICAL_PHASE_RECORD = "HISTORICAL_PHASE_RECORD"
    HISTORICAL_DECISION_LOG = "HISTORICAL_DECISION_LOG"
    HISTORICAL_GATE_REPORT = "HISTORICAL_GATE_REPORT"
    HISTORICAL_BLOCK_LEDGER = "HISTORICAL_BLOCK_LEDGER"
    CURRENT_SPECIFICATION = "CURRENT_SPECIFICATION"
    CURRENT_IMPLEMENTATION_RECORD = "CURRENT_IMPLEMENTATION_RECORD"
    ADVISORY_GUIDANCE = "ADVISORY_GUIDANCE"
    GENERATED_ARTIFACT = "GENERATED_ARTIFACT"
    UNKNOWN = "UNKNOWN"


class ImmutabilityState(str, Enum):
    UNCHANGED = "UNCHANGED"
    MODIFIED = "MODIFIED"
    ADDED = "ADDED"
    DELETED = "DELETED"
    MOVED = "MOVED"
    RENAMED = "RENAMED"
    AUTHORIZED_AMENDMENT = "AUTHORIZED_AMENDMENT"
    UNKNOWN_BASELINE = "UNKNOWN_BASELINE"
    UNVERIFIABLE = "UNVERIFIABLE"


class FindingSeverity(str, Enum):
    BLOCKER = "BLOCKER"
    CRITICAL = "CRITICAL"
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    ADVISORY = "ADVISORY"


@dataclass
class DocumentRecord:
    normalized_path: str
    canonical_sha256: str
    byte_size: int
    line_count: int
    classification: str
    provenance: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DocumentRecord:
        return cls(
            normalized_path=data["normalized_path"],
            canonical_sha256=data["canonical_sha256"],
            byte_size=data["byte_size"],
            line_count=data["line_count"],
            classification=data["classification"],
            provenance=data["provenance"],
        )


@dataclass
class HistoryBlockRecord:
    block_id: str
    date: str
    phase_slug: str
    title: str
    canonical_sha256: str
    byte_size: int
    line_count: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> HistoryBlockRecord:
        return cls(
            block_id=data["block_id"],
            date=data["date"],
            phase_slug=data["phase_slug"],
            title=data["title"],
            canonical_sha256=data["canonical_sha256"],
            byte_size=data["byte_size"],
            line_count=data["line_count"],
        )


HistoryBlock = HistoryBlockRecord


@dataclass
class PhaseManifest:
    schema_version: str
    guard_version: str
    phase_id: str
    phase_name: str
    locked_at: str
    authorized_by: str
    authorizing_adr: str
    prev_manifest_digest: str
    manifest_digest: str
    total_documents: int
    documents: List[DocumentRecord]
    history_blocks: List[HistoryBlockRecord] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["documents"] = [doc.to_dict() for doc in self.documents]
        d["history_blocks"] = [blk.to_dict() for blk in self.history_blocks]
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PhaseManifest:
        docs = [DocumentRecord.from_dict(d) for d in data.get("documents", [])]
        blks = [HistoryBlockRecord.from_dict(b) for b in data.get("history_blocks", [])]
        return cls(
            schema_version=data["schema_version"],
            guard_version=data["guard_version"],
            phase_id=data["phase_id"],
            phase_name=data["phase_name"],
            locked_at=data["locked_at"],
            authorized_by=data["authorized_by"],
            authorizing_adr=data["authorizing_adr"],
            prev_manifest_digest=data["prev_manifest_digest"],
            manifest_digest=data["manifest_digest"],
            total_documents=data["total_documents"],
            documents=docs,
            history_blocks=blks,
        )


@dataclass
class AmendmentRecord:
    amendment_id: str
    target_file: str
    prior_canonical_hash: str
    new_canonical_hash: str
    authorizing_adr: str
    authorized_by: str
    authorized_at: str
    amendment_type: str
    justification: str
    record_digest: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AmendmentRecord:
        return cls(
            amendment_id=data["amendment_id"],
            target_file=data["target_file"],
            prior_canonical_hash=data["prior_canonical_hash"],
            new_canonical_hash=data["new_canonical_hash"],
            authorizing_adr=data["authorizing_adr"],
            authorized_by=data["authorized_by"],
            authorized_at=data["authorized_at"],
            amendment_type=data["amendment_type"],
            justification=data["justification"],
            record_digest=data.get("record_digest", ""),
        )


@dataclass
class AmendmentLedger:
    schema_version: str
    guard_version: str
    ledger_id: str
    total_amendments: int
    ledger_digest: str
    amendments: List[AmendmentRecord] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["amendments"] = [a.to_dict() for a in self.amendments]
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AmendmentLedger:
        amends = [AmendmentRecord.from_dict(a) for a in data.get("amendments", [])]
        return cls(
            schema_version=data["schema_version"],
            guard_version=data["guard_version"],
            ledger_id=data["ledger_id"],
            total_amendments=data["total_amendments"],
            ledger_digest=data["ledger_digest"],
            amendments=amends,
        )


@dataclass
class TrustAnchor:
    schema_version: str
    trust_anchor_id: str
    genesis_phase_id: str
    genesis_manifest_digest: str
    ratified_at: str
    authorized_by: str
    signature_block: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TrustAnchor:
        return cls(
            schema_version=data["schema_version"],
            trust_anchor_id=data["trust_anchor_id"],
            genesis_phase_id=data["genesis_phase_id"],
            genesis_manifest_digest=data["genesis_manifest_digest"],
            ratified_at=data["ratified_at"],
            authorized_by=data["authorized_by"],
            signature_block=data["signature_block"],
        )


@dataclass
class HistoricalFinding:
    state: ImmutabilityState
    severity: FindingSeverity
    target: str
    expected_hash: Optional[str] = None
    actual_hash: Optional[str] = None
    reason: str = ""
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["state"] = self.state.value
        d["severity"] = self.severity.value
        return d


@dataclass
class HistoricalVerificationResult:
    status: str
    exit_code: int
    duration_ms: float
    trust_anchor_verified: bool
    chain_verified: bool
    total_documents: int
    unchanged_count: int
    amendment_count: int
    modified_count: int
    added_count: int
    deleted_count: int
    moved_count: int
    renamed_count: int
    unverifiable_count: int
    unknown_count: int
    findings: List[HistoricalFinding] = field(default_factory=list)
    phase_statuses: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["findings"] = [f.to_dict() for f in self.findings]
        return d
