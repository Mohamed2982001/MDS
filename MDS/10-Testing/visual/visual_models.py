#!/usr/bin/env python3
"""
MDS Visual Models & Data Structures
Phase 9.7.7: Visual Regression Engine & Snapshot Diffing
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Provides strongly-typed dataclasses for baseline configurations,
pixel comparison results, diff metrics, and serialized evidence.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional
from pathlib import Path


class VisualExecutionStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    DEFERRED = "DEFERRED"
    ERROR = "ERROR"


@dataclass(frozen=True)
class BaselineConfig:
    baseline_id: str
    route: str
    screen: str
    width: int
    height: int
    theme: str
    direction: str
    density: str
    file_name: str
    file_sha256: Optional[str] = None
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "baseline_id": self.baseline_id,
            "route": self.route,
            "screen": self.screen,
            "viewport": {"width": self.width, "height": self.height},
            "theme": self.theme,
            "direction": self.direction,
            "density": self.density,
            "file_name": self.file_name,
            "file_sha256": self.file_sha256,
            "description": self.description,
        }


@dataclass
class ComparisonMetrics:
    total_pixels: int = 0
    mismatched_pixels: int = 0
    diff_ratio: float = 0.0
    pixel_threshold: float = 0.05
    image_threshold: float = 0.001
    duration_ms: float = 0.0
    width: int = 0
    height: int = 0

    @property
    def dimensions(self) -> str:
        return f"{self.width}x{self.height}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_pixels": self.total_pixels,
            "mismatched_pixels": self.mismatched_pixels,
            "diff_ratio": round(self.diff_ratio, 6),
            "diff_percent": round(self.diff_ratio * 100, 4),
            "pixel_threshold": self.pixel_threshold,
            "image_threshold": self.image_threshold,
            "duration_ms": round(self.duration_ms, 2),
            "dimensions": f"{self.width}x{self.height}"
        }


@dataclass
class ComparisonResult:
    baseline_id: str
    status: VisualExecutionStatus
    metrics: ComparisonMetrics
    diff_image_path: Optional[Path] = None
    actual_image_path: Optional[Path] = None
    baseline_image_path: Optional[Path] = None
    error_message: Optional[str] = None
    evidence: Dict[str, Any] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return self.status == VisualExecutionStatus.PASS

    def to_dict(self) -> Dict[str, Any]:
        return {
            "baseline_id": self.baseline_id,
            "status": self.status.value,
            "metrics": self.metrics.to_dict(),
            "diff_image": str(self.diff_image_path) if self.diff_image_path else None,
            "error_message": self.error_message,
            "evidence": self.evidence
        }


@dataclass
class VisualSweepResult:
    capability_id: str = "MDS-VIS-001"
    status: VisualExecutionStatus = VisualExecutionStatus.PASS
    total_baselines: int = 12
    passed_baselines: int = 0
    failed_baselines: int = 0
    deferred_baselines: int = 0
    results: List[ComparisonResult] = field(default_factory=list)
    total_duration_ms: float = 0.0
    error_message: Optional[str] = None
    evidence_file: Optional[Path] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "status": self.status.value,
            "total_baselines": self.total_baselines,
            "passed_baselines": self.passed_baselines,
            "failed_baselines": self.failed_baselines,
            "deferred_baselines": self.deferred_baselines,
            "total_duration_ms": round(self.total_duration_ms, 2),
            "error_message": self.error_message,
            "evidence_file": str(self.evidence_file) if self.evidence_file else None,
            "runs": [r.to_dict() for r in self.results]
        }
