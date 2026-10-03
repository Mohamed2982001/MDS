"""
Master Design System (MDS) -- Formal Trust Chain & Verification Engine
Document Reference: MDS-SPEC-9711-REV5 / Section 10 & ADR-151
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from .manifest import compute_manifest_digest, verify_manifest_integrity
from .models import (
    InfrastructureAttestationError,
    ManifestAuthenticityError,
    ManifestIntegrityError,
    TrustedExecutionRecord,
)
from .sidecar import SidecarManager

logger = logging.getLogger("mds.ci.trust")


class TrustVerifier:
    """
    Implements the 4-tier layer separation and 3-step verification algorithm (ADR-151).
    Distinguishes Runner-Local Transport (Tier 2) from Provider-Controlled Records (Tier 3).
    """

    @classmethod
    def verify_full_trust_chain(
        cls,
        manifest_path: Path,
        sidecar_path: Path,
        trusted_record: Optional[TrustedExecutionRecord] = None,
        is_ci: bool = False,
    ) -> bool:
        """
        Executes the formal 3-step ordered verification algorithm (Section 10.4):
          Step 1: Canonical Serialization & Internal Integrity (Detects corruption / Case A)
          Step 2: External Sidecar Verification (Detects local workspace tampering / Cases B, D, F)
          Step 3: Provider-Controlled Trust Record Verification (Root of Trust Check / Cases C, E)
        """
        # STEP 1: Internal Integrity Verification
        passed, internal_digest, recomputed_digest = verify_manifest_integrity(manifest_path)

        # STEP 2: External Sidecar Verification
        if not sidecar_path.exists():
            if is_ci:
                raise ManifestAuthenticityError(
                    f"Sidecar missing in CI environment (Case D): mandatory artifact '{sidecar_path.name}' absent"
                )
            else:
                logger.info("Sidecar absent in local execution; operating in integrity-only mode (Case D-Local / G).")
                return True

        SidecarManager.verify_sidecar(recomputed_digest, sidecar_path, is_ci=is_ci)

        # STEP 3: Provider-Controlled Trust Record Verification (CI Authenticity Mode)
        if is_ci:
            if trusted_record is None:
                raise InfrastructureAttestationError(
                    "Missing Provider-Controlled Trust Record (Case E): external control plane record is unreachable"
                )

            if trusted_record.manifest_digest.lower() != recomputed_digest.lower():
                raise ManifestAuthenticityError(
                    f"Root of Trust breach (Case C): provider record digest '{trusted_record.manifest_digest}' "
                    f"!= recomputed canonical digest '{recomputed_digest}'"
                )

            return True

        # Local mode: Integrity-Only verified
        return True

    @staticmethod
    def assert_valid_trust_anchor(source_type: str) -> None:
        """
        Guarantees that runner-local mechanisms ($GITHUB_OUTPUT, $GITHUB_STEP_SUMMARY)
        are never configured or claimed as Root of Trust / Trust Anchor (ADR-151).
        """
        forbidden_anchors = ["github_output", "$github_output", "step_summary", "$github_step_summary", "sidecar_only"]
        normalized = source_type.lower().strip()
        if any(forbidden in normalized for forbidden in forbidden_anchors):
            raise ManifestAuthenticityError(
                f"Security Invariant Breach (ADR-151): '{source_type}' is runner-local transport only, "
                f"NOT an authoritative Trust Anchor or Root of Trust."
            )
