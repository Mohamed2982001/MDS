#!/usr/bin/env python3
"""
DSSE Candidate Catalog Provider & Loader
Handles loading, caching, and validation of candidate design system benchmarks.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from tools.dsse.validator import validate_candidate_catalog, DSSEValidationError


@dataclass
class DimensionRating:
    score: float
    evidence_tier: str
    provenance: str = ""
    notes: str = ""


@dataclass
class Candidate:
    id: str
    name: str
    description: str
    dimensions: Dict[str, DimensionRating]
    hard_constraints: Dict[str, str] = field(default_factory=dict)
    suggested_configuration: Dict[str, str] = field(default_factory=dict)

    def get_score(self, dim: str) -> float:
        return self.dimensions[dim].score if dim in self.dimensions else 0.0

    def get_tier(self, dim: str) -> str:
        return self.dimensions[dim].evidence_tier if dim in self.dimensions else "UNKNOWN"


class CandidateCatalog:
    def __init__(self, raw_data: Dict[str, Any]):
        self.raw_data = raw_data
        self.schema_version = raw_data.get("schemaVersion", "1.0.0")
        self.catalog_name = raw_data.get("catalogName", "")
        self.last_updated = raw_data.get("lastUpdated", "")
        self.candidates: List[Candidate] = []
        self._parse_candidates()

    def _parse_candidates(self) -> None:
        for c in self.raw_data.get("candidates", []):
            dims: Dict[str, DimensionRating] = {}
            for d_id, rating_dict in c.get("dimensions", {}).items():
                dims[d_id] = DimensionRating(
                    score=float(rating_dict.get("score", 0.0)),
                    evidence_tier=rating_dict.get("evidenceTier", "UNKNOWN"),
                    provenance=rating_dict.get("provenance", ""),
                    notes=rating_dict.get("notes", "")
                )
            self.candidates.append(Candidate(
                id=c.get("id", ""),
                name=c.get("name", ""),
                description=c.get("description", ""),
                dimensions=dims,
                hard_constraints=c.get("hardConstraints", {}),
                suggested_configuration=c.get("suggestedConfiguration", {})
            ))

    def get_candidate(self, candidate_id: str) -> Optional[Candidate]:
        for c in self.candidates:
            if c.id == candidate_id:
                return c
        return None


def get_default_catalog_path() -> Path:
    return Path(__file__).resolve().parent / "default_catalog.json"


def load_candidate_catalog(catalog_path: Optional[Path] = None) -> CandidateCatalog:
    """
    Loads and validates candidate catalog JSON.
    If catalog_path is None, loads default_catalog.json.
    """
    target_path = Path(catalog_path) if catalog_path else get_default_catalog_path()
    if not target_path.exists():
        raise FileNotFoundError(f"Catalog file not found: {target_path}")

    with open(target_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    is_valid, errors = validate_candidate_catalog(data)
    if not is_valid:
        raise DSSEValidationError([f"Catalog validation failed: {err}" for err in errors])

    return CandidateCatalog(data)
