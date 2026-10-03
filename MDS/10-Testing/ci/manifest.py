"""
Master Design System (MDS) -- Canonical Manifest Serializer & Integrity Engine
Document Reference: MDS-SPEC-9711-REV5 / Section 9 & 10 (ADR-146)
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, Tuple

from .models import ManifestIntegrityError


HEX64_REGEX = re.compile(r"^[0-9a-f]{64}$")


def serialize_canonical_json(data: Dict[str, Any]) -> bytes:
    """
    Serializes a dictionary to deterministic, byte-level canonical JSON.
    Invariants (ADR-146):
      - Keys sorted lexicographically
      - Compact separators (',', ':') with zero whitespace
      - UTF-8 encoding
      - ensure_ascii=False
    """
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def compute_manifest_digest(manifest_dict: Dict[str, Any]) -> str:
    """
    Computes the canonical SHA-256 digest of a manifest dictionary.
    Eliminates circularity by evaluating with 'manifest_sha256' set to None.
    """
    payload_copy = dict(manifest_dict)
    payload_copy["manifest_sha256"] = None
    canonical_bytes = serialize_canonical_json(payload_copy)
    return hashlib.sha256(canonical_bytes).hexdigest()


def sign_manifest(manifest_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes and injects the canonical SHA-256 digest into the manifest.
    Returns the updated manifest dictionary.
    """
    digest = compute_manifest_digest(manifest_dict)
    manifest_dict["manifest_sha256"] = digest
    return manifest_dict


def write_manifest(manifest_dict: Dict[str, Any], output_path: Path) -> Path:
    """
    Writes the signed manifest to output_path using formatted indentation for readability,
    while guaranteeing that canonical recomputation matches manifest_sha256.
    """
    if "manifest_sha256" not in manifest_dict or not manifest_dict["manifest_sha256"]:
        manifest_dict = sign_manifest(manifest_dict)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest_dict, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return output_path


def verify_manifest_integrity(manifest_path: Path) -> Tuple[bool, str, str]:
    """
    Step 1 Verification: Asserts internal canonical hash matches payload.
    Detects file corruption, truncation, or payload tampering (Case A).
    Returns (True, expected_hash, recomputed_hash).
    Raises ManifestIntegrityError on failure.
    """
    if not manifest_path.exists():
        raise ManifestIntegrityError(f"Manifest file does not exist: {manifest_path}")

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest_dict = json.load(f)
    except Exception as e:
        raise ManifestIntegrityError(f"Corrupt or invalid JSON in manifest: {e}")

    internal_hash = manifest_dict.get("manifest_sha256")
    if not internal_hash or not isinstance(internal_hash, str) or not HEX64_REGEX.match(internal_hash.lower()):
        raise ManifestIntegrityError(f"Malformed or missing internal 'manifest_sha256' digest: {internal_hash}")

    internal_hash = internal_hash.lower()
    recomputed_hash = compute_manifest_digest(manifest_dict)

    if recomputed_hash != internal_hash:
        raise ManifestIntegrityError(
            f"Internal integrity breach (Case A): internal digest '{internal_hash}' != recomputed '{recomputed_hash}'"
        )

    return True, internal_hash, recomputed_hash
