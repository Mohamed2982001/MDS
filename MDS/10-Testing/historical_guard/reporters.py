"""
MDS Historical Phase Guard Reporters
Phase 9.7.9: Historical Phase Guard & Architectural Immutability Engine
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Standard library only (Zero external dependencies).
Implements Section 12: Dual Reporting Contract (Console Dashboard & JSON Telemetry).
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Dict, Any, Optional

from .models import HistoricalVerificationResult, FindingSeverity


class ConsoleReporter:
    """Renders human-readable ANSI/terminal dashboard for Historical Guard."""

    @classmethod
    def render(
        cls,
        result: HistoricalVerificationResult,
        manifest_digests: Optional[Dict[str, str]] = None,
        anchor_id: str = "MDS-ROOT-ANCHOR-v1",
    ) -> str:
        lines = []
        sep = "=" * 80
        thin_sep = "-" * 80

        lines.append(sep)
        lines.append("         MASTER DESIGN SYSTEM (MDS) — HISTORICAL PHASE GUARD REPORT")
        lines.append(sep)

        status_text = (
            "PASS (All Historical Phase Records Sealed & Intact)"
            if result.status == "PASS"
            else f"FAIL ({result.status} - Invariants Violated)"
        )
        lines.append(f"Overall Status        : {status_text}")

        # Dual-Tier Advisory Performance Contract:
        # Tier 1 (Authoritative): Global Layer-M Canonical Contract (ADR-100 / Section 8): Warm <= 500ms, Cold <= 1200ms
        # Tier 2 (Subsystem): Phase 9.7.9 Local Advisory Target (ADR-113 / Section 18): Warm <= 100ms, Cold <= 300ms
        # Semantics: Strictly ADVISORY / NON-GATING across both tiers.
        if result.duration_ms <= 100.0:
            benchmark_badge = "Target Met (Layer-M <=500ms | Local <=100ms)"
            benchmark_note = (
                f"Execution duration ({result.duration_ms:.1f}ms) satisfies both Global Layer-M "
                "Canonical Contract (<=500ms) and Phase 9.7.9 Local Advisory Target (<=100ms); "
                "performance remains advisory (non-gating)."
            )
        elif result.duration_ms <= 500.0:
            benchmark_badge = "Layer-M Warm Target Met (<=500ms)"
            benchmark_note = (
                f"Execution duration ({result.duration_ms:.1f}ms) satisfies Global Layer-M "
                "Canonical Warm Contract (<=500ms); performance remains advisory (non-gating)."
            )
        elif result.duration_ms <= 1200.0:
            benchmark_badge = "Layer-M Cold Target Met (<=1200ms)"
            benchmark_note = (
                f"Execution duration ({result.duration_ms:.1f}ms) satisfies Global Layer-M "
                "Canonical Cold Contract (<=1200ms); performance remains advisory (non-gating)."
            )
        else:
            benchmark_badge = "Advisory Target Exceeded (>1200ms)"
            benchmark_note = (
                f"Target exceeded ({result.duration_ms:.1f}ms > 1200ms); "
                "performance remains advisory (non-gating)."
            )
        lines.append(
            f"Execution Duration    : {result.duration_ms:.1f} ms (Benchmark Advisory: {benchmark_badge})"
        )
        lines.append(f"Benchmark Note        : {benchmark_note}")

        anchor_status = (
            f"VERIFIED ({anchor_id} matching compile-time fingerprint)"
            if result.trust_anchor_verified
            else "VIOLATION (Fingerprint mismatch or missing trust anchor)"
        )
        lines.append(f"Root Trust Anchor     : {anchor_status}")

        total_phases = len(result.phase_statuses)
        lines.append(f"Phases Audited        : {total_phases} locked phases")
        lines.append(f"Total Guarded Docs    : {result.total_documents} historical records")

        chain_status = (
            "VALID (Cumulative chain unbroken and verified)"
            if result.chain_verified
            else "BROKEN (Cumulative digest chain failure)"
        )
        lines.append(f"Cumulative Chain      : {chain_status}")

        lines.append(thin_sep)
        lines.append("Immutability Breakdown:")
        lines.append(f"  UNCHANGED           : {result.unchanged_count}")
        lines.append(f"  AUTHORIZED AMENDMENT: {result.amendment_count}")
        lines.append(f"  MODIFIED (DRIFT)    : {result.modified_count}")
        lines.append(f"  ADDED (UNAUTHORIZED): {result.added_count}")
        lines.append(f"  DELETED (MISSING)   : {result.deleted_count}")
        lines.append(f"  MOVED               : {result.moved_count}")
        lines.append(f"  RENAMED             : {result.renamed_count}")
        lines.append(f"  UNVERIFIABLE        : {result.unverifiable_count}")

        if result.phase_statuses:
            lines.append(thin_sep)
            lines.append("Phase Ledger Status:")
            for p_id, p_stat in sorted(result.phase_statuses.items()):
                digest_str = ""
                if manifest_digests and p_id in manifest_digests:
                    digest_str = f" | Digest: {manifest_digests[p_id][:16]}..."
                lines.append(f"  [{p_stat}] {p_id:<14}: Verified sealed{digest_str}")

        if result.findings:
            non_advisory = [f for f in result.findings if f.severity != FindingSeverity.ADVISORY]
            if non_advisory:
                lines.append(thin_sep)
                lines.append(f"Findings ({len(non_advisory)}):")
                for f in non_advisory:
                    lines.append(
                        f"  - [{f.severity.value}] {f.state.value} on '{f.target}': {f.reason}"
                    )

        lines.append(sep)
        return "\n".join(lines)


class JSONReporter:
    """Formats structured JSON telemetry adhering to Section 12.2 schema."""

    @classmethod
    def render(
        cls,
        result: HistoricalVerificationResult,
        master_digest: str = "",
        anchor_id: str = "MDS-ROOT-ANCHOR-v1",
    ) -> Dict[str, Any]:
        # Global Layer-M Authoritative Contract Status (ADR-100 / Phase 9.7.8 Section 8)
        if result.duration_ms <= 500.0:
            layer_m_status = "WARM_TARGET_MET"
        elif result.duration_ms <= 1200.0:
            layer_m_status = "COLD_TARGET_MET"
        else:
            layer_m_status = "TARGET_EXCEEDED"

        # Phase 9.7.9 Local Subsystem Advisory Status (ADR-113 / Phase 9.7.9 Section 18)
        if result.duration_ms <= 100.0:
            local_status = "WARM_TARGET_MET"
        elif result.duration_ms <= 300.0:
            local_status = "COLD_TARGET_MET"
        else:
            local_status = "TARGET_EXCEEDED"

        return {
            "guard_version": "1.0.0",
            "executed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": result.status,
            "exit_code": result.exit_code,
            "execution_duration_ms": result.duration_ms,
            "benchmark_advisory": layer_m_status,
            "performance_contracts": {
                "global_layer_m_canonical": {
                    "contract_name": "Global Layer-M Canonical Performance Contract",
                    "authoritative_source": "ADR-100 / Phase 9.7.8 Architecture Section 8",
                    "warm_target_ms": 500.0,
                    "cold_target_ms": 1200.0,
                    "is_gating": False,
                    "advisory_status": layer_m_status,
                },
                "phase_9_7_9_local_advisory": {
                    "contract_name": "Phase 9.7.9 Local Advisory Benchmark Target",
                    "authoritative_source": "ADR-113 / Phase 9.7.9 Architecture Section 18",
                    "warm_target_ms": 100.0,
                    "cold_target_ms": 300.0,
                    "is_gating": False,
                    "advisory_status": local_status,
                },
            },
            "root_trust_anchor": {
                "status": "VERIFIED" if result.trust_anchor_verified else "FAILED",
                "anchor_id": anchor_id,
            },
            "cumulative_chain_status": "VALID" if result.chain_verified else "BROKEN",
            "master_digest": master_digest,
            "accounting": {
                "total_phases": len(result.phase_statuses),
                "total_documents": result.total_documents,
                "unchanged": result.unchanged_count,
                "authorized_amendments": result.amendment_count,
                "modified": result.modified_count,
                "added": result.added_count,
                "deleted": result.deleted_count,
                "moved": result.moved_count,
                "renamed": result.renamed_count,
                "unverifiable": result.unverifiable_count,
            },
            "findings": [f.to_dict() for f in result.findings],
        }

    @classmethod
    def write_to_file(
        cls,
        result: HistoricalVerificationResult,
        output_path: Path,
        master_digest: str = "",
        anchor_id: str = "MDS-ROOT-ANCHOR-v1",
    ) -> None:
        data = cls.render(result, master_digest=master_digest, anchor_id=anchor_id)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
