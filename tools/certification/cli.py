"""
Master Design System (MDS) — Certification CLI
Phase 10.4: MDS v1.0.0 Production Certification Gate
Layer 13: Implementation, Tooling & Operationalization
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

try:
    from .engine import CertificationEngine
    from .models import (
        CANONICAL_EVIDENCE_MANIFEST_PATH,
        PRODUCTION_CERTIFICATE_PATH,
        STANDALONE_TRUSTED_SEAL_PATH,
        compute_canonical_hash,
    )
except (ImportError, ValueError):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
    from tools.certification.engine import CertificationEngine
    from tools.certification.models import (
        CANONICAL_EVIDENCE_MANIFEST_PATH,
        PRODUCTION_CERTIFICATE_PATH,
        STANDALONE_TRUSTED_SEAL_PATH,
        compute_canonical_hash,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mds-certify",
        description="Master Design System (MDS) Production Certification Gate CLI",
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # Subcommand: certify
    certify_p = subparsers.add_parser("certify", help="Execute 13-gate production certification pipeline")
    certify_p.add_argument("--dist", type=Path, default=Path("dist"), help="Path to distribution directory")
    certify_p.add_argument("--epoch", type=int, default=1790812800, help="Build epoch timestamp")
    certify_p.add_argument("--author", type=str, default="Mohamed Khalid", help="Authorizing Lead Architect")
    certify_p.add_argument("--workspace", type=Path, default=None, help="Workspace root directory")
    certify_p.add_argument("--json", action="store_true", help="Output summary in JSON format")

    # Subcommand: verify-certificate
    verify_p = subparsers.add_parser("verify-certificate", help="Verify integrity of certificate, manifest and seal")
    verify_p.add_argument("--workspace", type=Path, default=None, help="Workspace root directory")
    verify_p.add_argument("--json", action="store_true", help="Output verification report in JSON format")

    return parser


def handle_certify(args: argparse.Namespace) -> int:
    workspace_root = (args.workspace or Path.cwd()).resolve()
    dist_dir = (args.dist or (workspace_root / "dist")).resolve()

    engine = CertificationEngine(workspace_root=workspace_root, dist_dir=dist_dir)
    res = engine.certify(authorized_by=args.author)

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("================================================================================")
        print("  MDS PRODUCTION CERTIFICATION GATE — EVALUATION COMPLETE")
        print("================================================================================")
        print(f"  Status:               {res['verdict']['status']}")
        print(f"  Decision:             {res['verdict']['certification_decision']}")
        print(f"  Gates Evaluated:      {res['gates_evaluated']}/13")
        print(f"  Blockers:             {res['verdict']['total_blockers']}")
        print(f"  Majors:               {res['verdict']['total_majors']}")
        print(f"  Minors:               {res['verdict']['total_minors']}")
        print(f"  Certificate ID:       {res['certificate_id']}")
        print(f"  Certificate Digest:   {res['certificate_digest']}")
        print(f"  Evidence Manifest:    {res['evidence_manifest_sha256']}")
        print(f"  Trusted Seal ID:      {res['seal_id']}")
        print(f"  Certificate File:     {res['certificate_path']}")
        print(f"  Seal File:            {res['seal_path']}")
        print("================================================================================")

    return 0 if res["is_certified"] else 1


def handle_verify_certificate(args: argparse.Namespace) -> int:
    workspace_root = (args.workspace or Path.cwd()).resolve()
    cert_path = workspace_root / PRODUCTION_CERTIFICATE_PATH
    manifest_path = workspace_root / CANONICAL_EVIDENCE_MANIFEST_PATH
    seal_path = workspace_root / STANDALONE_TRUSTED_SEAL_PATH

    errors = []

    if not cert_path.exists():
        errors.append(f"Missing Production Certificate: {cert_path}")
    if not manifest_path.exists():
        errors.append(f"Missing Canonical Evidence Manifest: {manifest_path}")
    if not seal_path.exists():
        errors.append(f"Missing Standalone Trusted Seal: {seal_path}")

    if errors:
        for err in errors:
            sys.stderr.write(f"[FAIL] {err}\n")
        return 1

    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    seal = json.loads(seal_path.read_text(encoding="utf-8"))

    # 1. Verify Evidence Manifest Hash
    expected_manifest_h, _ = compute_canonical_hash(manifest)
    recorded_manifest_h = cert["evidence_manifest_binding"]["evidence_manifest_sha256"]
    if expected_manifest_h != recorded_manifest_h:
        errors.append(f"Evidence Manifest SHA-256 mismatch! Computed: {expected_manifest_h}, Certificate: {recorded_manifest_h}")

    # 2. Verify Certificate Integrity Digest
    expected_cert_digest, _ = compute_canonical_hash(cert, exclude_keys=["certificate_integrity_digest"])
    recorded_cert_digest = cert["certificate_integrity_digest"]
    if expected_cert_digest != recorded_cert_digest:
        errors.append(f"Certificate Integrity Digest mismatch! Computed: {expected_cert_digest}, Certificate: {recorded_cert_digest}")

    # 3. Verify Standalone Seal Linkages
    if seal["certificate_id"] != cert["certificate_id"]:
        errors.append(f"Seal certificate_id mismatch: {seal['certificate_id']} != {cert['certificate_id']}")
    if seal["certificate_integrity_digest"] != recorded_cert_digest:
        errors.append(f"Seal certificate_integrity_digest mismatch: {seal['certificate_integrity_digest']} != {recorded_cert_digest}")
    if seal["evidence_manifest_sha256"] != recorded_manifest_h:
        errors.append(f"Seal evidence_manifest_sha256 mismatch: {seal['evidence_manifest_sha256']} != {recorded_manifest_h}")
    if seal["authorized_by"] != "Mohamed Khalid":
        errors.append(f"Seal authorized_by is not Mohamed Khalid: {seal['authorized_by']}")
    if seal["seal_status"] != "SEALED_APPROVED":
        errors.append(f"Seal status is not SEALED_APPROVED: {seal['seal_status']}")

    if errors:
        for err in errors:
            sys.stderr.write(f"[FAIL] {err}\n")
        return 1

    if args.json:
        print(json.dumps({"verified": True, "certificate_id": cert["certificate_id"], "seal_id": seal["seal_id"]}, indent=2))
    else:
        print("================================================================================")
        print("  MDS PRODUCTION CERTIFICATE & SEAL VERIFICATION — PASS (Exit 0)")
        print("================================================================================")
        print(f"  Certificate ID:       {cert['certificate_id']}")
        print(f"  Certificate Digest:   {recorded_cert_digest}")
        print(f"  Evidence Manifest:    {recorded_manifest_h}")
        print(f"  Seal Authorized By:   {seal['authorized_by']} ({seal['architect_title']})")
        print(f"  Seal Status:          {seal['seal_status']}")
        print("  Verdict:              100% Cryptographic Integrity & Governance Ratification Valid.")
        print("================================================================================")

    return 0


def main(argv: Optional[list] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.subcommand == "certify":
        return handle_certify(args)
    elif args.subcommand == "verify-certificate":
        return handle_verify_certificate(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
