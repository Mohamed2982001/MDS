"""
MDS Project History Block Parser & Immutability Engine
Phase 9.7.9: Historical Phase Guard & Architectural Immutability Engine
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Implements ADR-117:
- Phase-Partitioned Block Hashing for docs/PROJECT_HISTORY.md
- Canonical Block Demarcation and ID generation (BLOCK:<date>:<phase_slug>)
- Heading inclusion in hash stream
- Detection of mutation, deletion, insertion, reorder, duplicate IDs, split, and merge
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional

from .canonical_hasher import CanonicalStreamHasher
from .models import (
    HistoryBlockRecord,
    HistoricalFinding,
    ImmutabilityState,
    FindingSeverity,
)


class DuplicateBlockIdError(ValueError):
    """Raised when duplicate block IDs exist in PROJECT_HISTORY.md."""
    pass


class ProjectHistoryBlockParser:
    """Parses and verifies historical blocks in docs/PROJECT_HISTORY.md."""

    HEADING_PATTERN = re.compile(
        r"^##\s+\[([0-9]{4}-[0-9]{2}-[0-9]{2})\]\s+[\u2013\u2014\-]\s+(.+)$"
    )

    @classmethod
    def slugify(cls, title: str) -> str:
        """Derives deterministic normalized slug from milestone title."""
        cleaned = re.sub(r"[^a-z0-9\.]+", "-", title.lower()).strip("-")
        return cleaned

    @classmethod
    def parse_file(cls, file_path: Path) -> List[HistoryBlockRecord]:
        """Parses PROJECT_HISTORY.md from disk."""
        content = file_path.read_text(encoding="utf-8")
        return cls.parse_blocks(content)

    @classmethod
    def parse_blocks(cls, markdown_text: str) -> List[HistoryBlockRecord]:
        """
        Parses text into discrete, hashed history blocks.
        The H2 heading line is included in the block stream.
        """
        lines = markdown_text.splitlines(keepends=True)
        block_starts: List[Tuple[int, str, str, str]] = []  # line_idx, date, slug, raw_title

        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("## "):
                match = cls.HEADING_PATTERN.match(stripped)
                if match:
                    date_str = match.group(1)
                    title_str = match.group(2)
                    slug_str = cls.slugify(title_str)
                    block_starts.append((idx, date_str, slug_str, title_str))

        if not block_starts:
            return []

        blocks: List[HistoryBlockRecord] = []
        seen_ids: Dict[str, int] = {}

        for i in range(len(block_starts)):
            start_idx, date_str, slug_str, title_str = block_starts[i]
            end_idx = block_starts[i + 1][0] if (i + 1 < len(block_starts)) else len(lines)

            block_id = f"BLOCK:{date_str}:{slug_str}"
            if block_id in seen_ids:
                raise DuplicateBlockIdError(
                    f"Duplicate block ID '{block_id}' detected at lines {seen_ids[block_id]} and {start_idx}."
                )
            seen_ids[block_id] = start_idx

            block_content = "".join(lines[start_idx:end_idx])
            digest = CanonicalStreamHasher.hash_string(block_content)
            norm_content = block_content.replace("\r\n", "\n").replace("\r", "\n")
            byte_size = len(norm_content.encode("utf-8"))
            line_count = len(norm_content.splitlines())

            blocks.append(
                HistoryBlockRecord(
                    block_id=block_id,
                    date=date_str,
                    phase_slug=slug_str,
                    title=title_str,
                    canonical_sha256=digest,
                    byte_size=byte_size,
                    line_count=line_count,
                )
            )

        return blocks

    @classmethod
    def compare_blocks(
        cls,
        current_blocks: List[HistoryBlockRecord],
        baseline_blocks: List[HistoryBlockRecord],
        locked_phase_ids: Optional[List[str]] = None,
    ) -> List[HistoricalFinding]:
        """
        Compares active history blocks against ratified baseline blocks.
        Detects block mutation, deletion, insertion, and reordering.
        """
        findings: List[HistoricalFinding] = []
        curr_map = {b.block_id: b for b in current_blocks}
        base_map = {b.block_id: b for b in baseline_blocks}

        # 1. Check for Missing (Deleted) Blocks
        for b_id, base_b in base_map.items():
            if b_id not in curr_map:
                findings.append(
                    HistoricalFinding(
                        state=ImmutabilityState.DELETED,
                        severity=FindingSeverity.BLOCKER,
                        target=f"PROJECT_HISTORY.md::{b_id}",
                        expected_hash=base_b.canonical_sha256,
                        actual_hash=None,
                        reason=f"Historical block '{b_id}' ({base_b.title}) missing from docs/PROJECT_HISTORY.md",
                    )
                )

        # 2. Check for Content Mutations on existing baseline blocks
        for b_id, base_b in base_map.items():
            if b_id in curr_map:
                curr_b = curr_map[b_id]
                if curr_b.canonical_sha256 != base_b.canonical_sha256:
                    findings.append(
                        HistoricalFinding(
                            state=ImmutabilityState.MODIFIED,
                            severity=FindingSeverity.CRITICAL,
                            target=f"PROJECT_HISTORY.md::{b_id}",
                            expected_hash=base_b.canonical_sha256,
                            actual_hash=curr_b.canonical_sha256,
                            reason=f"Historical block '{b_id}' content/heading modified without authorization",
                        )
                    )

        # 3. Check for Unexpected Insertions among historical blocks
        base_ids = list(base_map.keys())
        for curr_b in current_blocks:
            if curr_b.block_id not in base_map:
                # If block precedes or is inserted among baseline blocks
                # Check if it should be locked
                findings.append(
                    HistoricalFinding(
                        state=ImmutabilityState.ADDED,
                        severity=FindingSeverity.CRITICAL,
                        target=f"PROJECT_HISTORY.md::{curr_b.block_id}",
                        expected_hash=None,
                        actual_hash=curr_b.canonical_sha256,
                        reason=f"Unrecognized historical block '{curr_b.block_id}' inserted into docs/PROJECT_HISTORY.md",
                    )
                )

        # 4. Check Sequence Order of shared blocks
        shared_in_curr = [b.block_id for b in current_blocks if b.block_id in base_map]
        shared_in_base = [b.block_id for b in baseline_blocks if b.block_id in curr_map]
        if shared_in_curr != shared_in_base:
            findings.append(
                HistoricalFinding(
                    state=ImmutabilityState.MODIFIED,
                    severity=FindingSeverity.BLOCKER,
                    target="PROJECT_HISTORY.md::sequence",
                    expected_hash=",".join(shared_in_base),
                    actual_hash=",".join(shared_in_curr),
                    reason="Historical blocks in docs/PROJECT_HISTORY.md have been reordered or permuted",
                )
            )

        return findings
