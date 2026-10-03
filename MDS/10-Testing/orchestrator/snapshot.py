"""
Master Design System (MDS) — Protected Core Post-State Cryptographic Snapshot
Phase 9.7.10: Unified Local Orchestrator CLI & Master Validation Pipeline
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from .models import Finding, FindingSeverity

PROTECTED_CORE_DIRECTORIES = [
    "MDS/02-Tokens",
    "MDS/Runtime",
    "MDS/Playground",
    "MDS/Reference-Application",
]


class ProtectedCoreSnapshotManager:
    """
    Computes preflight and postflight cryptographic NIST SHA-256 snapshots
    over all files in the protected core.
    Guarantees Post-State Final Cryptographic Content & Structural Integrity:
      - File additions: PROTECTED_CORE_ADDED
      - File deletions: PROTECTED_CORE_DELETED
      - File content mutations: PROTECTED_CORE_MODIFIED (NIST SHA-256 + byte size)
    Note: Metadata-only modifications (such as mtime/atime timestamp alterations)
    without content mutation, as well as transient write-restore sequences,
    are explicitly OUT OF SCOPE.
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        if workspace_root is None:
            self.workspace_root = Path(__file__).resolve().parent.parent.parent.parent
        else:
            self.workspace_root = Path(workspace_root).resolve()

    def compute_file_hash(self, file_path: Path) -> Tuple[int, str]:
        """Reads file in 64KB chunks and computes NIST SHA-256 digest and byte size."""
        hasher = hashlib.sha256()
        byte_size = 0
        with open(file_path, "rb") as fp:
            while chunk := fp.read(65536):
                hasher.update(chunk)
                byte_size += len(chunk)
        return byte_size, hasher.hexdigest()

    def capture_snapshot(self) -> Dict[str, Tuple[int, str]]:
        """
        Walks all protected core directories and maps:
        relative_posix_path -> (byte_size, sha256_digest)
        """
        snapshot: Dict[str, Tuple[int, str]] = {}

        for rel_dir in PROTECTED_CORE_DIRECTORIES:
            target_dir = self.workspace_root / rel_dir
            if not target_dir.exists():
                continue

            for p in sorted(target_dir.rglob("*")):
                if p.is_file():
                    # Ignore pycache, dotfiles
                    if "__pycache__" in p.parts or p.name.startswith("."):
                        continue

                    rel_path = p.relative_to(self.workspace_root).as_posix()
                    try:
                        size, digest = self.compute_file_hash(p)
                        snapshot[rel_path] = (size, digest)
                    except Exception:
                        pass

        return snapshot

    def compare_snapshots(
        self,
        pre_snapshot: Dict[str, Tuple[int, str]],
        post_snapshot: Dict[str, Tuple[int, str]],
    ) -> Tuple[bool, List[Finding]]:
        """
        Compares pre- and post-flight snapshots to determine post-state delta.
        Returns:
            clean: bool (True if byte-for-byte identical)
            delta_findings: List[Finding] (empty if clean, BLOCKER findings if mutated)
        """
        findings: List[Finding] = []

        pre_keys: Set[str] = set(pre_snapshot.keys())
        post_keys: Set[str] = set(post_snapshot.keys())

        # 1. Deleted files
        deleted = pre_keys - post_keys
        for path in sorted(deleted):
            findings.append(
                Finding(
                    severity=FindingSeverity.BLOCKER,
                    target=path,
                    code="PROTECTED_CORE_DELETED",
                    message=f"Protected core file was deleted during pipeline execution: {path}",
                )
            )

        # 2. Added files
        added = post_keys - pre_keys
        for path in sorted(added):
            findings.append(
                Finding(
                    severity=FindingSeverity.BLOCKER,
                    target=path,
                    code="PROTECTED_CORE_ADDED",
                    message=f"Unauthorized file was created in protected core during execution: {path}",
                )
            )

        # 3. Modified files
        common = pre_keys & post_keys
        for path in sorted(common):
            pre_size, pre_hash = pre_snapshot[path]
            post_size, post_hash = post_snapshot[path]

            if pre_size != post_size or pre_hash != post_hash:
                findings.append(
                    Finding(
                        severity=FindingSeverity.BLOCKER,
                        target=path,
                        code="PROTECTED_CORE_MODIFIED",
                        message=(
                            f"Protected core file mutated: {path} "
                            f"(pre_hash={pre_hash[:8]} vs post_hash={post_hash[:8]})"
                        ),
                    )
                )

        clean = len(findings) == 0
        return clean, findings
