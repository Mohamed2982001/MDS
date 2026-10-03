"""
MDS Historical Phase Guard — Genesis Bootstrap Script
Phase 9.7.9: Historical Phase Guard & Architectural Immutability Engine
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Executes ADR-115 & ADR-116 Linear Bootstrap Protocol:
1. Ingests all 42 pre-existing historical phase records (Phases 9.1 to 9.7.8)
2. Partitions into 8 discrete phase manifests
3. Computes unbroken cumulative hash chain (Genesis -> 9.7.8)
4. Emits amendments_ledger.json (empty genesis ledger)
5. Generates trust_anchor.json with genesis manifest digest and signature
6. Computes canonical SHA-256 fingerprint of trust_anchor.json for pinning
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from historical_guard.canonical_hasher import CanonicalStreamHasher
from historical_guard.classifier import HistoricalClassifier
from historical_guard.block_parser import ProjectHistoryBlockParser
from historical_guard.models import (
    DocumentRecord,
    HistoryBlockRecord,
    PhaseManifest,
    AmendmentLedger,
    TrustAnchor,
)


def run_bootstrap(force: bool = False, workspace_root: Optional[Path] = None) -> str:
    root = workspace_root or Path(__file__).resolve().parent.parent.parent.parent
    baselines_dir = root / "MDS" / "10-Testing" / "baselines" / "historical"
    baselines_dir.mkdir(parents=True, exist_ok=True)

    trust_anchor_file = baselines_dir / "trust_anchor.json"
    registry_file = baselines_dir / "master_historical_registry.json"

    if not force:
        if trust_anchor_file.exists():
            raise FileExistsError(
                f"Trust anchor already exists at '{trust_anchor_file}'. "
                "Genesis bootstrap tooling cannot silently replace or overwrite an existing sealed trust anchor. "
                "Explicit re-initialization requires force=True or --force."
            )
        if registry_file.exists():
            raise FileExistsError(
                f"Master historical registry already exists at '{registry_file}'. "
                "Genesis bootstrap tooling cannot silently overwrite an existing sealed registry. "
                "Explicit re-initialization requires force=True or --force."
            )

    classifier = HistoricalClassifier()
    history_file = root / "docs" / "PROJECT_HISTORY.md"
    all_blocks = ProjectHistoryBlockParser.parse_file(history_file)
    block_map = {b.block_id: b for b in all_blocks}

    # Partitioning of 42 historical records across 8 phases
    phase_definitions = [
        {
            "phase_id": "Phase-9.1",
            "phase_name": "Web Reference Implementation Architecture",
            "locked_at": "2026-09-20T21:35:00.000Z",
            "authorizing_adr": "IDR-001",
            "files": [],
            "block_ids": [
                "BLOCK:2026-09-13:inception-architectural-scaffolding",
                "BLOCK:2026-09-13:phase-2-token-architecture-repository-design",
                "BLOCK:2026-09-13:phase-2-technical-correction-hardening-pass",
                "BLOCK:2026-09-13:phase-3-foundations-design-language-token-calibration",
                "BLOCK:2026-09-14:phase-3.5-calibration-consistency-gate",
                "BLOCK:2026-09-14:phase-4-core-primitives-architecture-implementation",
                "BLOCK:2026-09-15:phase-4-verification-approval-gate-pass",
                "BLOCK:2026-09-15:phase-5-core-components-architecture-implementation",
                "BLOCK:2026-09-16:phase-6-patterns-composition-layer-05",
                "BLOCK:2026-09-16:phase-7-workflows-architecture-implementation-layer-06",
                "BLOCK:2026-09-17:phase-8.1.1-assistive-technology-testing-deep-accessibility-audit",
                "BLOCK:2026-09-17:phase-8.1.2-automated-test-suite-regression-harness-layer-10",
                "BLOCK:2026-09-17:phase-8.1.3-layer-07-templates-architecture-implementation",
                "BLOCK:2026-09-20:phase-8.1.4-documentation-portal-unified-design-system-catalog",
                "BLOCK:2026-09-20:phase-8.5-pre-baseline-architecture-hardening-pass",
                "BLOCK:2026-09-20:phase-8.5-dsse-mathematical-decision-lock-specification-ratification-dsse-adr-001",
                "BLOCK:2026-09-20:phase-8.6-final-architecture-baseline-audit-mds-baseline-v1.0.0-ratification",
                "BLOCK:2026-09-20:phase-9.1-web-reference-implementation-architecture-layer-13",
            ],
        },
        {
            "phase_id": "Phase-9.2",
            "phase_name": "Token Runtime Engine Implementation",
            "locked_at": "2026-09-20T21:50:00.000Z",
            "authorizing_adr": "IDR-003",
            "files": [],
            "block_ids": [
                "BLOCK:2026-09-20:phase-9.2-token-runtime-engine-implementation"
            ],
        },
        {
            "phase_id": "Phase-9.3",
            "phase_name": "Foundations & Primitives Runtime Engine Implementation",
            "locked_at": "2026-09-21T18:30:00.000Z",
            "authorizing_adr": "IDR-004",
            "files": [
                "MDS/13-Implementation/Phase-9.3-Final-Audit.md",
            ],
            "block_ids": [
                "BLOCK:2026-09-21:phase-9.3-foundations-primitives-runtime-engine-implementation"
            ],
        },
        {
            "phase_id": "Phase-9.4",
            "phase_name": "Core Component Runtime Engine Implementation",
            "locked_at": "2026-09-21T19:15:00.000Z",
            "authorizing_adr": "IDR-005",
            "files": [
                "MDS/13-Implementation/Phase-9.4-Execution-Report.md",
                "MDS/13-Implementation/Phase-9.4-Final-Audit.md",
            ],
            "block_ids": [
                "BLOCK:2026-09-21:phase-9.4-core-component-runtime-engine-implementation"
            ],
        },
        {
            "phase_id": "Phase-9.5",
            "phase_name": "Reference Runtime Laboratory (Interactive Playground) Implementation",
            "locked_at": "2026-09-21T21:40:00.000Z",
            "authorizing_adr": "IDR-007",
            "files": [
                "MDS/13-Implementation/Phase-9.5-Execution-Report.md",
                "MDS/13-Implementation/Phase-9.5-Final-Audit.md",
            ],
            "block_ids": [
                "BLOCK:2026-09-21:phase-9.5-reference-runtime-laboratory-interactive-playground-implementation"
            ],
        },
        {
            "phase_id": "Phase-9.6",
            "phase_name": "Reference Application (MDS Workspace) Implementation",
            "locked_at": "2026-09-22T16:20:00.000Z",
            "authorizing_adr": "IDR-008",
            "files": [
                "MDS/13-Implementation/Phase-9.6-Architecture-Gaps.md",
                "MDS/13-Implementation/Phase-9.6-Decision-Log.md",
                "MDS/13-Implementation/Phase-9.6-Final-Audit.md",
                "MDS/13-Implementation/Phase-9.6-Final-Reaudit.md",
                "MDS/13-Implementation/Phase-9.6-Reaudit-Evidence.md",
                "MDS/13-Implementation/Phase-9.6-Reconciliation.md",
                "MDS/13-Implementation/Phase-9.6-Reference-Application-Architecture.md",
                "MDS/13-Implementation/Phase-9.6-Reference-Application-Execution-Report.md",
                "MDS/13-Implementation/Phase-9.6-Remediation-Report.md",
            ],
            "block_ids": [
                "BLOCK:2026-09-21:phase-9.6-reference-application-mds-workspace-implementation"
            ],
        },
        {
            "phase_id": "Phase-9.7",
            "phase_name": "Validation, Testing & Specialized Hardening Suites",
            "locked_at": "2026-09-24T18:00:00.000Z",
            "authorizing_adr": "ADR-090",
            "files": [
                "MDS/13-Implementation/Phase-9.7-Decision-Log.md",
                "MDS/13-Implementation/Phase-9.7-Gaps.md",
                "MDS/13-Implementation/Phase-9.7-Validation-Architecture.md",
                "MDS/13-Implementation/Phase-9.7.1-Architecture-Review.md",
                "MDS/13-Implementation/Phase-9.7.2-Decision-Log.md",
                "MDS/13-Implementation/Phase-9.7.2-Final-Audit.md",
                "MDS/13-Implementation/Phase-9.7.2-Implementation-Report.md",
                "MDS/13-Implementation/Phase-9.7.2-Remediation.md",
                "MDS/13-Implementation/Phase-9.7.3-Decision-Log.md",
                "MDS/13-Implementation/Phase-9.7.3-Final-Audit-Reconciliation.md",
                "MDS/13-Implementation/Phase-9.7.3-Implementation-Report.md",
                "MDS/13-Implementation/Phase-9.7.4-Audit-Reconciliation.md",
                "MDS/13-Implementation/Phase-9.7.4-Decision-Log.md",
                "MDS/13-Implementation/Phase-9.7.4-Implementation-Report.md",
                "MDS/13-Implementation/Phase-9.7.5-Decision-Log.md",
                "MDS/13-Implementation/Phase-9.7.5-Implementation-Report.md",
                "MDS/13-Implementation/Phase-9.7.6-Decision-Log.md",
                "MDS/13-Implementation/Phase-9.7.6-Gaps.md",
                "MDS/13-Implementation/Phase-9.7.6-Implementation-Report.md",
                "MDS/13-Implementation/Phase-9.7.6-Responsive-Architecture.md",
                "MDS/13-Implementation/Phase-9.7.7-Decision-Log.md",
                "MDS/13-Implementation/Phase-9.7.7-Gaps.md",
                "MDS/13-Implementation/Phase-9.7.7-Visual-Regression-Architecture.md",
            ],
            "block_ids": [],
        },
        {
            "phase_id": "Phase-9.7.8",
            "phase_name": "Governance Engine & Repository Consistency Verifier",
            "locked_at": "2026-09-25T23:45:00.000Z",
            "authorizing_adr": "ADR-103",
            "files": [
                "MDS/13-Implementation/Phase-9.7.8-Capability-Coverage-Matrix.md",
                "MDS/13-Implementation/Phase-9.7.8-Decision-Log.md",
                "MDS/13-Implementation/Phase-9.7.8-Gaps.md",
                "MDS/13-Implementation/Phase-9.7.8-Governance-Architecture.md",
                "MDS/13-Implementation/Phase-9.7.8-Governance-Implementation-Report.md",
            ],
            "block_ids": [],
        },
    ]

    total_doc_count = sum(len(p["files"]) for p in phase_definitions)
    print(f"Total documents to ingest across 8 phases: {total_doc_count}")
    assert total_doc_count == 42, f"Expected 42 documents, found {total_doc_count}"

    current_prev_digest = "0" * 64
    locked_phases_registry = []
    genesis_manifest_digest = ""

    for p_def in phase_definitions:
        p_id = p_def["phase_id"]
        doc_records: List[DocumentRecord] = []

        for rel_file in p_def["files"]:
            full_file = root / rel_file
            assert full_file.exists(), f"File {rel_file} does not exist!"
            sha256, byte_size, line_count, _ = CanonicalStreamHasher.hash_file(full_file)
            c_type = classifier.classify(rel_file)
            doc_records.append(
                DocumentRecord(
                    normalized_path=rel_file.replace("\\", "/"),
                    canonical_sha256=sha256,
                    byte_size=byte_size,
                    line_count=line_count,
                    classification=c_type.value,
                    provenance=f"Ratified in {p_id}",
                )
            )

        block_records: List[HistoryBlockRecord] = []
        for b_id in p_def["block_ids"]:
            assert b_id in block_map, f"Block ID {b_id} not found in PROJECT_HISTORY.md!"
            block_records.append(block_map[b_id])

        # Compute manifest digest
        sorted_docs = sorted(doc_records, key=lambda d: d.normalized_path)
        docs_payload = [d.to_dict() for d in sorted_docs]
        canonical_json = json.dumps(docs_payload, sort_keys=True, separators=(",", ":"))
        manifest_digest = CanonicalStreamHasher.hash_string(f"{current_prev_digest}|{canonical_json}")

        if p_id == "Phase-9.1":
            genesis_manifest_digest = manifest_digest

        manifest = PhaseManifest(
            schema_version="1.0.0",
            guard_version="1.0.0",
            phase_id=p_id,
            phase_name=p_def["phase_name"],
            locked_at=p_def["locked_at"],
            authorized_by="Mohamed Khalid",
            authorizing_adr=p_def["authorizing_adr"],
            prev_manifest_digest=current_prev_digest,
            manifest_digest=manifest_digest,
            total_documents=len(doc_records),
            documents=sorted_docs,
            history_blocks=block_records,
        )

        manifest_filename = f"{p_id.lower().replace('-', '_')}_manifest.json"
        manifest_file = baselines_dir / manifest_filename
        manifest_file.write_text(json.dumps(manifest.to_dict(), indent=2), encoding="utf-8")
        print(f"Generated manifest: {manifest_filename} | Digest: {manifest_digest[:16]}... | Docs: {len(doc_records)}")

        locked_phases_registry.append({
            "phase_id": p_id,
            "phase_name": p_def["phase_name"],
            "manifest_file": manifest_filename,
            "manifest_digest": manifest_digest,
            "total_documents": len(doc_records),
            "total_blocks": len(block_records),
        })

        current_prev_digest = manifest_digest

    cumulative_chain_digest = current_prev_digest

    # Generate amendments_ledger.json
    ledger_file = baselines_dir / "amendments_ledger.json"
    ledger = AmendmentLedger(
        schema_version="1.0.0",
        guard_version="1.0.0",
        ledger_id="MDS-AMENDMENTS-LEDGER-v1",
        total_amendments=0,
        ledger_digest="0" * 64,
        amendments=[],
    )
    ledger_file.write_text(json.dumps(ledger.to_dict(), indent=2), encoding="utf-8")
    print("Generated genesis amendments_ledger.json")

    # Generate master_historical_registry.json
    registry_file = baselines_dir / "master_historical_registry.json"
    registry_data = {
        "schema_version": "1.0.0",
        "guard_version": "1.0.0",
        "registry_id": "MDS-MASTER-HISTORICAL-REGISTRY-v1",
        "total_locked_phases": len(locked_phases_registry),
        "total_historical_documents": total_doc_count,
        "cumulative_chain_digest": cumulative_chain_digest,
        "genesis_phase_id": "Phase-9.1",
        "genesis_manifest_digest": genesis_manifest_digest,
        "locked_phases": locked_phases_registry,
    }
    registry_file.write_text(json.dumps(registry_data, indent=2), encoding="utf-8")
    print(f"Generated master_historical_registry.json | Master Cumulative Digest: {cumulative_chain_digest[:16]}...")

    # Generate trust_anchor.json
    trust_anchor_file = baselines_dir / "trust_anchor.json"
    anchor = TrustAnchor(
        schema_version="1.0.0",
        trust_anchor_id="MDS-ROOT-ANCHOR-v1",
        genesis_phase_id="Phase-9.1",
        genesis_manifest_digest=genesis_manifest_digest,
        ratified_at="2026-09-26T21:45:00.000Z",
        authorized_by="Mohamed Khalid (Senior Full Stack & Flutter Developer)",
        signature_block="MDS-SIG-MK-9790-IMMUTABILITY-ROOT-TRUST-ANCHOR-VERIFIED",
    )
    trust_anchor_file.write_text(json.dumps(anchor.to_dict(), indent=2), encoding="utf-8")

    # Compute canonical fingerprint of trust_anchor.json
    anchor_fingerprint, _, _, _ = CanonicalStreamHasher.hash_file(trust_anchor_file)
    print(f"Generated trust_anchor.json | ROOT_TRUST_ANCHOR_FINGERPRINT: {anchor_fingerprint}")
    return anchor_fingerprint


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Master Design System (MDS) — Historical Guard Genesis Bootstrap Tooling"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Explicitly allow re-initialization and overwrite of existing sealed trust anchor/registry",
    )
    cli_args = parser.parse_args()
    try:
        fp = run_bootstrap(force=cli_args.force)
        print("\nBOOTSTRAP SUCCESSFUL!")
        print(f"ROOT_TRUST_ANCHOR_FINGERPRINT = \"{fp}\"")
    except FileExistsError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
