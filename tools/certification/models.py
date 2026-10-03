"""
Master Design System (MDS) — Certification Models & Data Contracts
Phase 10.4: MDS v1.0.0 Production Certification Gate
Layer 13: Implementation, Tooling & Operationalization
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class GateSeverity(str, Enum):
    BLOCKER = "BLOCKER"
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    ADVISORY = "ADVISORY"


class GateStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    WAIVED = "WAIVED"


class SealStatus(str, Enum):
    SEALED_APPROVED = "SEALED_APPROVED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"


ZERO_WAIVER_DOMAIN: Set[str] = {
    "Gate_A",
    "Gate_B",
    "Gate_D",
    "Gate_F1",
    "Gate_I_03",
}

CANONICAL_EVIDENCE_MANIFEST_PATH: str = "evidence/certification/certification_evidence_manifest.json"
STANDALONE_TRUSTED_SEAL_PATH: str = "evidence/certification/trusted_certification_seal.json"
PRODUCTION_CERTIFICATE_PATH: str = "evidence/certification/MDS_v1.0.0_PRODUCTION_CERTIFICATE.json"


@dataclass
class GateResult:
    gate_id: str
    name: str
    status: GateStatus
    blockers: int = 0
    majors: int = 0
    minors: int = 0
    evidence_digest: str = ""
    log_file: str = ""
    byte_size: int = 0
    details: Dict[str, Any] = field(default_factory=dict)
    log_content: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status.value,
            "blockers": self.blockers,
            "majors": self.majors,
            "minors": self.minors,
            "evidence_digest": self.evidence_digest,
        }


@dataclass
class CertificationVerdict:
    status: str
    total_blockers: int
    total_majors: int
    total_minors: int
    total_waived: int
    total_na: int
    certification_decision: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "total_blockers": self.total_blockers,
            "total_majors": self.total_majors,
            "total_minors": self.total_minors,
            "total_waived": self.total_waived,
            "total_na": self.total_na,
            "certification_decision": self.certification_decision,
        }


def canonical_json_serialize(data: Any, exclude_keys: Optional[List[str]] = None) -> str:
    """
    RFC 8785 Canonical JSON Serialization.
    Keys are sorted recursively, no whitespace between separators, UTF-8 strings.
    """
    sanitized = copy.deepcopy(data)
    if exclude_keys and isinstance(sanitized, dict):
        for k in exclude_keys:
            sanitized.pop(k, None)

    return json.dumps(sanitized, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_canonical_hash(data: Any, exclude_keys: Optional[List[str]] = None) -> Tuple[str, str]:
    """
    Computes deterministic SHA-256 hash over RFC 8785 canonical JSON serialization.
    Returns (sha256_hex, canonical_json_string).
    """
    serialized = canonical_json_serialize(data, exclude_keys=exclude_keys)
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    return digest, serialized
