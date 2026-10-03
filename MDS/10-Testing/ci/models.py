"""
Master Design System (MDS) -- CI Pipeline & Artifact Dashboard Data Models
Document Reference: MDS-SPEC-9711-REV5 / MDS-DEC-9711-REV5
Layer: Layer M (Testing, Governance & Architectural Immutability)
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


class SecurityViolationError(Exception):
    """Raised when an operation attempts path traversal or violates security boundaries."""
    pass


class ManifestIntegrityError(Exception):
    """Raised when internal manifest canonical payload hash does not match (file corruption/drift)."""
    pass


class ManifestAuthenticityError(Exception):
    """Raised when external sidecar or provider trust anchor verification fails."""
    pass


class InfrastructureAttestationError(Exception):
    """Raised when the CI Provider Control Plane record is missing or unreachable."""
    pass


class RegistrySchemaError(Exception):
    """Raised when the declarative surface provenance registry fails schema or integrity checks."""
    pass


class ExitCode(enum.IntEnum):
    """Authoritative exit codes defined in ADR-142."""
    SUCCESS = 0
    VALIDATION_FAILURE = 1
    ARCHITECTURAL_BREACH = 2
    INFRASTRUCTURE_FAILURE = 124


class Severity(str, enum.Enum):
    BLOCKER = "BLOCKER"
    CRITICAL = "CRITICAL"
    WARN = "WARN"
    INFO = "INFO"


class SubsystemStatus(str, enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    DEFERRED = "DEFERRED"
    CACHED = "CACHED"
    SKIPPED = "SKIPPED"


class ArtifactClass(str, enum.Enum):
    TELEMETRY = "TELEMETRY"
    EVIDENCE = "EVIDENCE"
    LOG = "LOG"
    DASHBOARD = "DASHBOARD"


class ProvenanceTag(str, enum.Enum):
    PREEXISTING_SURFACE = "PREEXISTING_SURFACE"
    REGRESSION = "REGRESSION"
    UNKNOWN = "UNKNOWN"


class TriageState(str, enum.Enum):
    CONFIRMED = "CONFIRMED"
    PROVENANCE_CONFLICT = "PROVENANCE_CONFLICT"
    MALFORMED_RULE = "MALFORMED_RULE"
    UNINDEXED = "UNINDEXED"
    BASELINE_GROUNDED = "BASELINE_GROUNDED"
    NEW_FINDING = "NEW_FINDING"
    REGISTRY_ABSENT = "REGISTRY_ABSENT"
    REGISTRY_INVALID = "REGISTRY_INVALID"
    STRICT_NON_MATCH = "STRICT_NON_MATCH"


@dataclass
class CIEnvironmentContext:
    """Captured runner context from CI provider environment (Section 6.1)."""
    provider_name: str          # "github_actions", "gitlab_ci", "local_runner"
    is_ci: bool                 # True in automated runners
    run_id: str                 # Deterministic run identifier
    run_attempt: int            # Execution attempt counter
    commit_sha: str             # Current commit SHA (40 hex chars)
    branch_ref: str             # Target branch or tag
    pr_number: Optional[int]    # Pull request number (if applicable)
    actor: str                  # Triggering actor / bot
    runner_os: str              # "windows", "linux", "macos"
    runner_arch: str            # "x64", "arm64"
    workspace_root: Path        # Root path of repository checkout
    trust_anchor_type: str      # "provider_controlled_record", "none_integrity_only"


@dataclass(frozen=True)
class TrustedExecutionRecord:
    """
    Abstract provider-agnostic contract for external authenticity verification (ADR-151).
    Formally designated as 'Provider-Controlled Trust Record' (Tier 3).
    """
    run_id: str                 # Unique CI provider execution identifier
    commit_identity: str        # Immutable Git commit SHA (40 hex chars)
    manifest_digest: str        # Canonical NIST SHA-256 digest of ci_artifact_manifest.json
    provider_identity: str      # Authenticated provider name ("github_actions", "gitlab_ci", "local_runner")
    execution_identity: str     # Job / workflow / pipeline execution reference in control plane
    authenticity_status: str    # "PROVIDER_VERIFIED", "INTEGRITY_ONLY", "UNAUTHENTICATED"


@dataclass
class FindingRecord:
    """Normalized diagnostic finding conforming to manifest schema."""
    severity: str
    code: str
    target: str
    line: Optional[int] = None
    col: Optional[int] = None
    message: str = ""
    provenance: Optional[str] = None
    triage_state: Optional[str] = None


@dataclass
class SubsystemRecord:
    """Subsystem execution result captured from orchestrator telemetry."""
    subsystem_id: str
    subsystem_name: str
    stage: int
    status: str
    duration_ms: float
    assertions_run: int
    assertions_cached: int
    findings_count: int


@dataclass
class ArtifactRecord:
    """Harvested artifact entry with cryptographic hash."""
    artifact_id: str
    artifact_class: str
    relative_path: str
    byte_size: int
    sha256: str
    mime_type: str
    subsystem_id: Optional[str] = None


@dataclass
class ProtectedCoreSummary:
    clean: bool
    files_audited: int
    mutations_detected: int


@dataclass
class HistoricalGuardSummary:
    status: str
    locked_phases_audited: int
    records_audited: int
    drift_detected: int
    root_anchor_verified: bool


@dataclass
class LatestPointer:
    schema_version: str
    pointer_updated_utc: str
    run_id: str
    manifest_relative_path: str
    manifest_sha256: str
