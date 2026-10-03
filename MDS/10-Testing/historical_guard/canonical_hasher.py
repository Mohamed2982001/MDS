"""
MDS Exact Canonical Stream Hasher
Phase 9.7.9: Historical Phase Guard & Architectural Immutability Engine
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Implements ADR-106:
- Binary ingestion
- UTF-8 BOM detection and stripping
- Strict UTF-8 decoding
- CRLF and standalone CR conversion to LF
- Exact body whitespace preservation
- NIST SHA-256 digest computation
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Tuple, Union


class CanonicalStreamHasher:
    """Computes cross-platform deterministic SHA-256 digests over text streams."""

    BOM_BYTES = b"\xef\xbb\xbf"

    @classmethod
    def hash_file(cls, file_path: Union[str, Path]) -> Tuple[str, int, int, bool]:
        """
        Reads a file from disk, normalizes stream, and computes SHA-256.
        Returns: (sha256_hexdigest, byte_size, line_count, bom_detected)
        """
        p = Path(file_path).resolve()
        raw_bytes = p.read_bytes()
        return cls.hash_bytes(raw_bytes)

    @classmethod
    def hash_bytes(cls, raw_bytes: bytes) -> Tuple[str, int, int, bool]:
        """
        Processes raw bytes through canonicalization pipeline.
        Returns: (sha256_hexdigest, byte_size, line_count, bom_detected)
        """
        bom_detected = False
        if raw_bytes.startswith(cls.BOM_BYTES):
            raw_bytes = raw_bytes[len(cls.BOM_BYTES):]
            bom_detected = True

        # Strict UTF-8 decode
        text = raw_bytes.decode("utf-8", errors="strict")

        # Normalize line endings to LF
        normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")

        canonical_bytes = normalized_text.encode("utf-8")
        digest = hashlib.sha256(canonical_bytes).hexdigest()
        byte_size = len(canonical_bytes)
        line_count = len(normalized_text.splitlines())

        return digest, byte_size, line_count, bom_detected

    @classmethod
    def hash_string(cls, text: str) -> str:
        """Computes SHA-256 over normalized string."""
        normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")
        canonical_bytes = normalized_text.encode("utf-8")
        return hashlib.sha256(canonical_bytes).hexdigest()
