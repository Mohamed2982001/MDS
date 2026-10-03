"""
MDS Historical Document Classifier
Phase 9.7.9: Historical Phase Guard & Architectural Immutability Engine
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Implements ADR-110, ADR-114, and ADR-119:
- Four-Rank Classification Precedence Hierarchy
- Governed Historical Scope resolution
- Elimination of filename-only detection heuristics
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, Dict, Set, Union

from .models import HistoricalDocumentClassification


class HistoricalClassifier:
    """Classifies repository documents using four-rank precedence."""

    METADATA_REGEX = re.compile(
        r"^(?:<!--|\*{0,2})?\s*Classification:\s*([A-Za-z0-9_]+)\s*(?:-->|\*{0,2})?$",
        re.MULTILINE | re.IGNORECASE,
    )

    CURRENT_SPECS_13 = {
        "MDS/13-Implementation/Component-Implementation-Contract.md",
        "MDS/13-Implementation/CSS-Architecture.md",
        "MDS/13-Implementation/MDS-Implementation-Architecture.md",
        "MDS/13-Implementation/Playground-and-Reference-Architecture.md",
        "MDS/13-Implementation/Testing-and-Quality-Strategy.md",
        "MDS/13-Implementation/Theme-and-State-Architecture.md",
        "MDS/13-Implementation/Token-Runtime-Architecture.md",
        "MDS/13-Implementation/Implementation-Decision-Log.md",
    }

    DECISION_LOG_FILENAMES = {
        "09-Design-Decision-Log.md",
        "Primitive-Decision-Log.md",
        "Component-Decision-Log.md",
        "Pattern-Decision-Log.md",
        "Workflow-Decision-Log.md",
        "Template-Decision-Log.md",
        "Documentation-Decision-Log.md",
    }

    def __init__(self, manifest_roster: Optional[Dict[str, str]] = None):
        """
        manifest_roster: Optional map of normalized_path -> classification
        established from ratified baseline manifests (Rank 1).
        """
        self.manifest_roster = manifest_roster or {}

    def classify(
        self,
        rel_path: str,
        content: Optional[str] = None,
        canonical_hash: Optional[str] = None,
        hash_roster: Optional[Dict[str, str]] = None,
    ) -> HistoricalDocumentClassification:
        """
        Resolves document classification through 4-rank precedence:
        1. Manifest Roster Lookup (path or content hash match)
        2. Explicit Document Metadata Header
        3. Canonical Path Pattern Rules
        4. Unknown Fallback
        """
        norm_path = rel_path.replace("\\", "/")

        # Rank 1: Manifest Roster
        if norm_path in self.manifest_roster:
            c_str = self.manifest_roster[norm_path]
            return HistoricalDocumentClassification(c_str)

        if canonical_hash and hash_roster and canonical_hash in hash_roster:
            c_str = hash_roster[canonical_hash]
            return HistoricalDocumentClassification(c_str)

        # Rank 2: Explicit Document Metadata
        if content:
            meta_match = self.METADATA_REGEX.search(content)
            if meta_match:
                tag = meta_match.group(1).upper()
                for c in HistoricalDocumentClassification:
                    if c.value == tag:
                        return c

        # Rank 3: Canonical Path Pattern Rules
        # Generated artifacts
        if "artifacts/" in norm_path or norm_path.startswith("MDS/10-Testing/artifacts/"):
            return HistoricalDocumentClassification.GENERATED_ARTIFACT

        # Advisory guidance
        if norm_path.endswith("/README.md") or norm_path.endswith("README.md") or ".agents/rules/" in norm_path:
            return HistoricalDocumentClassification.ADVISORY_GUIDANCE

        # Runtime & Applications
        if (
            norm_path.startswith("MDS/Runtime/")
            or norm_path.startswith("MDS/Playground/")
            or norm_path.startswith("MDS/Reference-Application/")
        ):
            return HistoricalDocumentClassification.CURRENT_IMPLEMENTATION_RECORD

        # Project History Ledger
        if norm_path == "docs/PROJECT_HISTORY.md" or norm_path.endswith("/PROJECT_HISTORY.md"):
            return HistoricalDocumentClassification.HISTORICAL_BLOCK_LEDGER

        # Calibration Gate Reports
        if "10-Calibration-Gate-Report.md" in norm_path or "Gate-Report.md" in norm_path:
            return HistoricalDocumentClassification.HISTORICAL_GATE_REPORT

        # Current Implementation Specs in 13-Implementation
        if norm_path in self.CURRENT_SPECS_13:
            return HistoricalDocumentClassification.CURRENT_SPECIFICATION

        # Decision logs
        filename = Path(norm_path).name
        if filename in self.DECISION_LOG_FILENAMES or "-Decision-Log.md" in filename:
            return HistoricalDocumentClassification.HISTORICAL_DECISION_LOG

        # Phase records in 13-Implementation
        if norm_path.startswith("MDS/13-Implementation/") and filename.startswith("Phase-") and filename.endswith(".md"):
            if "Decision-Log" in filename:
                return HistoricalDocumentClassification.HISTORICAL_DECISION_LOG
            return HistoricalDocumentClassification.HISTORICAL_PHASE_RECORD

        # Core active specs in layers 00-07, 10-12
        if any(
            norm_path.startswith(prefix)
            for prefix in [
                "MDS/MDS_MASTER_SPECIFICATION.md",
                "MDS/01-Foundations/",
                "MDS/02-Tokens/",
                "MDS/03-Primitives/",
                "MDS/04-Components/",
                "MDS/05-Patterns/",
                "MDS/06-Workflows/",
                "MDS/07-Templates/",
                "MDS/AGENT/",
            ]
        ):
            return HistoricalDocumentClassification.CURRENT_SPECIFICATION

        # Rank 4: Fallback / Unknown
        if norm_path.startswith("MDS/13-Implementation/"):
            return HistoricalDocumentClassification.UNKNOWN

        return HistoricalDocumentClassification.CURRENT_SPECIFICATION

    def is_in_governed_historical_scope(
        self,
        rel_path: str,
        classification: Optional[HistoricalDocumentClassification] = None,
        content: Optional[str] = None,
    ) -> bool:
        """
        Determines whether a file falls within the Governed Historical Scope (ADR-114).
        """
        norm_path = rel_path.replace("\\", "/")
        if classification is None:
            classification = self.classify(norm_path, content=content)

        # Explicitly excluded categories
        if classification in (
            HistoricalDocumentClassification.GENERATED_ARTIFACT,
            HistoricalDocumentClassification.ADVISORY_GUIDANCE,
            HistoricalDocumentClassification.CURRENT_SPECIFICATION,
            HistoricalDocumentClassification.CURRENT_IMPLEMENTATION_RECORD,
        ):
            return False

        # Explicit historical classifications
        if classification in (
            HistoricalDocumentClassification.HISTORICAL_PHASE_RECORD,
            HistoricalDocumentClassification.HISTORICAL_DECISION_LOG,
            HistoricalDocumentClassification.HISTORICAL_GATE_REPORT,
            HistoricalDocumentClassification.HISTORICAL_BLOCK_LEDGER,
        ):
            return True

        # Any remaining or UNKNOWN file residing in MDS/13-Implementation/ is governed
        if norm_path.startswith("MDS/13-Implementation/"):
            return True

        return False
