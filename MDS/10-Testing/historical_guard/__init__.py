"""
Master Design System (MDS) — Historical Phase Guard Subsystem
Phase 9.7.9: Historical Phase Guard & Architectural Immutability Engine
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Standard library only (Zero external dependencies).
"""

from .models import (
    HistoricalDocumentClassification,
    ImmutabilityState,
    DocumentRecord,
    PhaseManifest,
    AmendmentRecord,
    AmendmentLedger,
    TrustAnchor,
    HistoryBlock,
    HistoryBlockRecord,
    HistoricalFinding,
    HistoricalVerificationResult,
)
from .canonical_hasher import CanonicalStreamHasher
from .classifier import HistoricalClassifier
from .block_parser import ProjectHistoryBlockParser
from .amendment_engine import AmendmentOverlayEngine
from .engine import HistoricalGuardEngine

__all__ = [
    "HistoricalDocumentClassification",
    "ImmutabilityState",
    "DocumentRecord",
    "PhaseManifest",
    "AmendmentRecord",
    "AmendmentLedger",
    "TrustAnchor",
    "HistoryBlock",
    "HistoricalFinding",
    "HistoricalVerificationResult",
    "CanonicalStreamHasher",
    "HistoricalClassifier",
    "ProjectHistoryBlockParser",
    "AmendmentOverlayEngine",
    "HistoricalGuardEngine",
]
