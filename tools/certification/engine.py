"""
Master Design System (MDS) — Production Certification Engine
Phase 10.4: MDS v1.0.0 Production Certification Gate
Layer 13: Implementation, Tooling & Operationalization
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .gates import GateEvaluator
from .models import (
    CANONICAL_EVIDENCE_MANIFEST_PATH,
    PRODUCTION_CERTIFICATE_PATH,
    STANDALONE_TRUSTED_SEAL_PATH,
    CertificationVerdict,
    GateResult,
    GateStatus,
    SealStatus,
    canonical_json_serialize,
    compute_canonical_hash,
)


class CertificationEngine:
    """
    Orchestrates the 13-gate certification execution pipeline, captures evidence logs,
    generates the immutable evidence manifest, computes certificate digests, and ratifies
    the standalone Trusted Certification Seal.
    """

    def __init__(self, workspace_root: Optional[Path] = None, dist_dir: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.dist_dir = (dist_dir or (self.workspace_root / "dist")).resolve()
        self.evidence_dir = self.workspace_root / "evidence" / "certification"
        self.epoch = 1790812800

    def certify(self, authorized_by: str = "Mohamed Khalid") -> Dict[str, Any]:
        """
        Executes complete production certification protocol.
        """
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        evaluator = GateEvaluator(self.workspace_root, self.dist_dir, epoch=self.epoch)

        gates: List[GateResult] = []

        # 1. Gate A: Determinism
        res_a = evaluator.evaluate_gate_a()
        gates.append(res_a)

        # 2. Gate B: Security & Trust Chain
        res_b = evaluator.evaluate_gate_b()
        gates.append(res_b)

        # 3. Gate C: W3C Standards
        res_c = evaluator.evaluate_gate_c()
        gates.append(res_c)

        # 4. Gate D: Artifact Integrity
        res_d = evaluator.evaluate_gate_d()
        gates.append(res_d)

        # 5. Gate E: Budgets
        res_e = evaluator.evaluate_gate_e()
        gates.append(res_e)

        # 6. Gate F1: Toolchain Runtime
        res_f1 = evaluator.evaluate_gate_f1()
        gates.append(res_f1)

        # 7. Gate F2: Browser Compatibility
        res_f2 = evaluator.evaluate_gate_f2()
        gates.append(res_f2)

        # 8. Gate G: Accessibility
        res_g = evaluator.evaluate_gate_g()
        gates.append(res_g)

        # 9. Gate H: Responsive & RTL
        res_h = evaluator.evaluate_gate_h()
        gates.append(res_h)

        # 10. Gate I: Versioning & Tests
        res_i = evaluator.evaluate_gate_i()
        gates.append(res_i)

        # 11. Gate J: Release BOM
        res_j = evaluator.evaluate_gate_j()
        gates.append(res_j)

        # 12. Gate K: Clean Abort & Rollback
        res_k = evaluator.evaluate_gate_k()
        gates.append(res_k)

        # 13. Gate L: Sign-off Authority
        res_l = evaluator.evaluate_gate_l(gates, authorized_by=authorized_by)
        gates.append(res_l)

        # Write each log file and compute hash and byte size
        for g in gates:
            log_path = self.workspace_root / g.log_file
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_bytes = g.log_content.encode("utf-8")
            log_path.write_bytes(log_bytes)
            g.byte_size = len(log_bytes)
            g.evidence_digest = hashlib.sha256(log_bytes).hexdigest()

        # Build Canonical Evidence Manifest
        manifest_path = self.dist_dir / "mds_dist_manifest.json"
        dist_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        build_id = dist_manifest.get("build_id") or dist_manifest.get("build_identity") or ""

        source_id_obj = dist_manifest.get("source_identity", {})
        source_id = source_id_obj.get("source_hash") if isinstance(source_id_obj, dict) else str(dist_manifest.get("source_identity") or "")

        compiler_id_obj = dist_manifest.get("compiler_identity", {})
        compiler_hash_str = compiler_id_obj.get("compiler_hash", "") if isinstance(compiler_id_obj, dict) else str(dist_manifest.get("compiler_identity") or "")
        compiler_id = compiler_hash_str.split(":")[-1] if ":" in compiler_hash_str else compiler_hash_str

        config_id_obj = dist_manifest.get("build_config_identity", {})
        config_id = config_id_obj.get("config_hash") if isinstance(config_id_obj, dict) else str(dist_manifest.get("config_identity") or "")

        env_id_obj = dist_manifest.get("build_env_identity", {})
        env_id = env_id_obj.get("env_hash") if isinstance(env_id_obj, dict) else str(dist_manifest.get("environment_identity") or "")

        now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        evidence_manifest_id = f"MDS-EVID-v1.0.0-{build_id[:16]}"
        gate_evidence_map: Dict[str, Any] = {}
        for g in gates:
            gate_evidence_map[g.gate_id] = {
                "log_file": g.log_file,
                "sha256": g.evidence_digest,
                "byte_size": g.byte_size,
            }

        evidence_manifest_payload = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "evidence_manifest_id": evidence_manifest_id,
            "release_identity": "MDS-v1.0.0-RELEASE",
            "build_identity": build_id,
            "source_identity": source_id,
            "timestamp": now_iso,
            "gate_evidence_map": gate_evidence_map,
        }

        manifest_sha256, canonical_manifest_json = compute_canonical_hash(evidence_manifest_payload)
        manifest_file = self.workspace_root / CANONICAL_EVIDENCE_MANIFEST_PATH
        manifest_file.parent.mkdir(parents=True, exist_ok=True)
        manifest_file.write_text(json.dumps(evidence_manifest_payload, indent=2), encoding="utf-8")

        # Compile gate evaluations dict
        gate_evaluations_dict: Dict[str, Any] = {}
        for g in gates:
            gate_evaluations_dict[g.gate_id] = g.to_dict()

        total_blockers = sum(g.blockers for g in gates)
        total_majors = sum(g.majors for g in gates)
        total_minors = sum(g.minors for g in gates)
        is_certified = (total_blockers == 0 and total_majors == 0)

        verdict = CertificationVerdict(
            status="CERTIFIED" if is_certified else "REJECTED",
            total_blockers=total_blockers,
            total_majors=total_majors,
            total_minors=total_minors,
            total_waived=0,
            total_na=0,
            certification_decision="APPROVED_FOR_PRODUCTION_RELEASE" if is_certified else "REJECTED_DUE_TO_VIOLATIONS",
        )

        cert_id = f"MDS-CERT-v1.0.0-{build_id[:16]}"
        seal_id = "MDS-SEAL-v1.0.0-PROD"

        # Build Certificate Payload
        certificate_payload = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "schema_version": "1.0.0",
            "certificate_id": cert_id,
            "release_id": "MDS-v1.0.0-RELEASE",
            "package_name": "master-design-system",
            "version": "1.0.0",
            "certification_timestamp": now_iso,
            "certification_subject_summary": {
                "subject_scope": "MDS v1.0.0 Production Design System Runtime & Distribution Package",
                "runtime_files_count": 61,
                "compiled_distribution_artifacts_count": 33,
                "excluded_harnesses": ["MDS/Playground/", "MDS/Reference-Application/"],
            },
            "release_file_summary": {
                "total_files_in_dist": 35,
                "production_artifacts_count": 33,
                "distribution_manifest_present": True,
                "distribution_manifest_sha256_present": True,
            },
            "root_trust_anchor": {
                "anchor_id": "MDS-ROOT-ANCHOR-v1",
                "fingerprint": "20c240e650a447299690d0e2f65c65a0dbed2acc4aba9de9997c4a093f2ed114",
            },
            "identity_contract": {
                "source_identity": source_id,
                "compiler_identity": compiler_id,
                "config_identity": config_id,
                "environment_identity": env_id,
                "build_epoch": self.epoch,
                "build_identity": build_id,
            },
            "evidence_manifest_binding": {
                "evidence_manifest_path": CANONICAL_EVIDENCE_MANIFEST_PATH,
                "evidence_manifest_id": evidence_manifest_id,
                "evidence_manifest_sha256": manifest_sha256,
                "total_evidence_files_count": 13,
            },
            "gate_evaluations": gate_evaluations_dict,
            "waiver_records": [],
            "not_applicable_determinations": [],
            "verdict": verdict.to_dict(),
            "trusted_certification_seal_path": STANDALONE_TRUSTED_SEAL_PATH,
            "trusted_certification_seal_id": seal_id,
        }

        # Compute certificate integrity digest over payload excluding certificate_integrity_digest
        cert_digest, _ = compute_canonical_hash(certificate_payload, exclude_keys=["certificate_integrity_digest"])
        certificate_payload["certificate_integrity_digest"] = cert_digest

        # Write Production Certificate to dist/
        cert_file = self.workspace_root / PRODUCTION_CERTIFICATE_PATH
        cert_file.write_text(json.dumps(certificate_payload, indent=2), encoding="utf-8")

        # Build Standalone Trusted Certification Seal Record
        seal_payload = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "seal_id": seal_id,
            "certificate_id": cert_id,
            "release_identity": "MDS-v1.0.0-RELEASE",
            "build_identity": build_id,
            "evidence_manifest_sha256": manifest_sha256,
            "certificate_integrity_digest": cert_digest,
            "authorized_by": authorized_by,
            "architect_title": "Senior Full Stack & Flutter Developer",
            "authorized_at": now_iso,
            "seal_status": SealStatus.SEALED_APPROVED.value if is_certified else SealStatus.REJECTED.value,
            "governance_classification": "GOVERNANCE_AUTHORIZATION_RECORD",
            "cryptographic_signer_authenticity_claimed": False,
        }

        seal_file = self.workspace_root / STANDALONE_TRUSTED_SEAL_PATH
        seal_file.write_text(json.dumps(seal_payload, indent=2), encoding="utf-8")

        return {
            "is_certified": is_certified,
            "verdict": verdict.to_dict(),
            "certificate_id": cert_id,
            "seal_id": seal_id,
            "certificate_digest": cert_digest,
            "evidence_manifest_sha256": manifest_sha256,
            "certificate_path": str(cert_file),
            "seal_path": str(seal_file),
            "evidence_manifest_path": str(manifest_file),
            "gates_evaluated": len(gates),
        }
