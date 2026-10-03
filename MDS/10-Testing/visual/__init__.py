#!/usr/bin/env python3
"""
MDS Visual Regression Engine Package
Phase 9.7.7: Visual Regression Engine & Snapshot Diffing
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from .visual_models import (
    BaselineConfig,
    ComparisonMetrics,
    ComparisonResult,
    VisualSweepResult,
    VisualExecutionStatus
)
from .png_codec import decode_png, encode_png
from .visual_comparator import VisualComparator, DimensionMismatchError
from .baseline_manager import (
    BaselineManager,
    BaselineIntegrityError,
    FontArtifactUnavailableError
)
from .visual_runner import VisualRunner
from .evidence_generator import VisualEvidenceGenerator
from .visual_dispatch import VisualDispatcher

__all__ = [
    "BaselineConfig",
    "ComparisonMetrics",
    "ComparisonResult",
    "VisualSweepResult",
    "VisualExecutionStatus",
    "decode_png",
    "encode_png",
    "VisualComparator",
    "DimensionMismatchError",
    "BaselineManager",
    "BaselineIntegrityError",
    "FontArtifactUnavailableError",
    "VisualRunner",
    "VisualEvidenceGenerator",
    "VisualDispatcher",
]
