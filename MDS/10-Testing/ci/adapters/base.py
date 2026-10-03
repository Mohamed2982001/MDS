"""
Master Design System (MDS) -- CI Provider Adapter Interface
Document Reference: MDS-SPEC-9711-REV5 / Section 6
"""

from __future__ import annotations

import abc
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..models import CIEnvironmentContext, FindingRecord, TrustedExecutionRecord


class CIProviderAdapter(abc.ABC):
    """
    Abstract barrier maintaining CI provider independence (ADR-136).
    Restricted to three operational duties:
      1. Detecting and normalizing runner environment metadata.
      2. Invoking run_all.py with appropriate profile.
      3. Collecting output artifacts, recording provider trust records, and publishing step summaries.
    """

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root

    @abc.abstractmethod
    def detect_environment(self) -> CIEnvironmentContext:
        """Inspects environment variables and host platform to build normalized context."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_execution_flags(self) -> List[str]:
        """Returns command line flags to invoke run_all.py."""
        raise NotImplementedError

    @abc.abstractmethod
    def export_step_summary(self, manifest_dict: Dict[str, Any], output_path: Optional[Path] = None) -> str:
        """Formats and exports markdown step summary."""
        raise NotImplementedError

    @abc.abstractmethod
    def record_trusted_execution(self, manifest_dict: Dict[str, Any]) -> TrustedExecutionRecord:
        """
        Commits the execution record containing the canonical digest to the CI Provider's control plane.
        Formally a 'Provider-Controlled Trust Record' (ADR-151).
        """
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_trusted_execution(self, run_id: str) -> Optional[TrustedExecutionRecord]:
        """Queries the CI Provider Control Plane for a committed execution record."""
        raise NotImplementedError

    @abc.abstractmethod
    def format_pr_annotation(self, finding: FindingRecord) -> str:
        """Formats a single finding into a provider-specific PR annotation."""
        raise NotImplementedError
