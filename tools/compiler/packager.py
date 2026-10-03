"""
Master Design System (MDS) — Deterministic Archive Packager
Phase 10.3: Production Artifact Compilation & Zero-NPM Distribution
Layer 13: Implementation, Tooling & Operationalization
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import gzip
import io
import os
import tarfile
import time
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .models import BuildConfig


class DeterministicPackager:
    """
    Creates bit-exact reproducible archives (.zip and .tar.gz) from distribution artifacts:
    - Normalizes timestamps, permissions, ownership, and archive headers
    - Strips ZIP extra fields
    - Fixes Gzip OS byte and mtime
    """

    def __init__(self, build_epoch: int = 1790812800):
        self.build_epoch = build_epoch
        # GM time tuple (YYYY, MM, DD, HH, MM, SS)
        self.gm_time = time.gmtime(self.build_epoch)[:6]

    def create_zip(self, files_dict: Dict[str, bytes]) -> bytes:
        """
        Creates a deterministic ZIP archive from in-memory file dictionary.
        Keys are POSIX relative paths (e.g. 'bundles/mds.all.css').
        """
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for rel_path in sorted(files_dict.keys()):
                data = files_dict[rel_path]
                zinfo = zipfile.ZipInfo(filename=rel_path, date_time=self.gm_time)
                # Unix regular file permissions: 0644
                zinfo.external_attr = 0o100644 << 16
                zinfo.create_system = 3  # Unix
                zinfo.extra = b""  # Strip non-deterministic extra fields
                zf.writestr(zinfo, data)

        return buf.getvalue()

    def create_tar_gz(self, files_dict: Dict[str, bytes]) -> bytes:
        """
        Creates a deterministic .tar.gz archive from in-memory file dictionary.
        Normalizes TarInfo and Gzip header (mtime, OS byte 255).
        """
        # 1. Uncompressed tar
        tar_buf = io.BytesIO()
        with tarfile.open(fileobj=tar_buf, mode="w", format=tarfile.PAX_FORMAT) as tf:
            for rel_path in sorted(files_dict.keys()):
                data = files_dict[rel_path]
                ti = tarfile.TarInfo(name=rel_path)
                ti.size = len(data)
                ti.mtime = self.build_epoch
                ti.mode = 0o644
                ti.uid = 0
                ti.gid = 0
                ti.uname = "root"
                ti.gname = "root"
                tf.addfile(ti, io.BytesIO(data))

        uncompressed_tar = tar_buf.getvalue()

        # 2. Deterministic gzip compression
        gz_buf = io.BytesIO()
        with gzip.GzipFile(
            filename="",
            mode="wb",
            fileobj=gz_buf,
            mtime=float(self.build_epoch),
        ) as gz:
            gz.write(uncompressed_tar)

        gz_bytes = bytearray(gz_buf.getvalue())
        # Set OS byte at index 9 to 255 (unknown OS) to prevent Windows/Unix header divergence
        if len(gz_bytes) >= 10:
            gz_bytes[9] = 255

        return bytes(gz_bytes)

    def package_distribution(
        self, artifacts: Dict[str, bytes]
    ) -> Tuple[bytes, bytes]:
        """
        Builds both zip and tar.gz archives excluding any pre-existing archive entries.
        Returns: (zip_bytes, tar_gz_bytes)
        """
        # Exclude archives themselves to prevent recursion
        archive_payload = {
            k: v for k, v in artifacts.items() if not k.startswith("archives/")
        }
        zip_bytes = self.create_zip(archive_payload)
        tar_gz_bytes = self.create_tar_gz(archive_payload)
        return zip_bytes, tar_gz_bytes
