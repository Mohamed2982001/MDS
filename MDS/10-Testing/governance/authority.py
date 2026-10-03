"""Five-Tier Authority Hierarchy and Intra-Tier 1 Precedence Engine.

Implements ADR-087 and ADR-097:
- Cross-Tier Rule: Tier 1 > Tier 2 > Tier 3 > Tier 4 > Tier 5
- Intra-Tier 1 Order: Rank 1 (Master Spec) > Rank 2 (DTCG) > Rank 3 (Layer Specs) > Rank 4 (DSSE)
- Same-Rank Conflict: Triggers a CRITICAL finding requiring an approved ADR.
"""

from __future__ import annotations

from enum import IntEnum
from typing import Tuple


class AuthorityTier(IntEnum):
    TIER_1_CANONICAL = 1
    TIER_2_REALIZATION = 2
    TIER_3_DERIVED = 3
    TIER_4_OPERATIONAL = 4
    TIER_5_ADVISORY = 5


class AuthorityRank(IntEnum):
    RANK_1_MASTER_SPEC = 1
    RANK_2_DTCG_TOKENS = 2
    RANK_3_LAYER_SPECS = 3
    RANK_4_DSSE_SPEC = 4
    RANK_5_GENERAL = 5


class AuthorityManager:
    """Evaluates authority precedence between documents, nodes, or assertions."""

    @classmethod
    def resolve_file_tier_and_rank(cls, file_path_str: str) -> Tuple[AuthorityTier, AuthorityRank]:
        p = file_path_str.replace("\\", "/")

        # Tier 1 documents
        if "MDS/00-Master-Architecture.md" in p:
            return AuthorityTier.TIER_1_CANONICAL, AuthorityRank.RANK_1_MASTER_SPEC
        if "MDS/02-Tokens/" in p and p.endswith(".tokens.json"):
            return AuthorityTier.TIER_1_CANONICAL, AuthorityRank.RANK_2_DTCG_TOKENS
        if "01-Foundations/" in p or "03-Primitives/MDS-Primitives-Architecture.md" in p or "04-Components/MDS-Components-Architecture.md" in p or "05-Patterns/Pattern-Composition-Rules.md" in p or "06-Workflows/Workflow-State-Model.md" in p or "07-Templates/MDS-Templates-Architecture.md" in p:
            return AuthorityTier.TIER_1_CANONICAL, AuthorityRank.RANK_3_LAYER_SPECS
        if "DESIGN_SYSTEM_SELECTION_ENGINE.md" in p:
            return AuthorityTier.TIER_1_CANONICAL, AuthorityRank.RANK_4_DSSE_SPEC

        # Tier 2: Realization & Contracts
        if "Component-Implementation-Contract.md" in p or "MDS/10-Testing/capabilities/registry.json" in p or "04-Components/specifications/" in p or "Runtime/" in p:
            return AuthorityTier.TIER_2_REALIZATION, AuthorityRank.RANK_5_GENERAL

        # Tier 3: Derived catalogs
        if "Documentation-Index.json" in p or "docs/ROADMAP.md" in p:
            return AuthorityTier.TIER_3_DERIVED, AuthorityRank.RANK_5_GENERAL

        # Tier 4: Operational & Historical
        if "MDS/13-Implementation/Phase-" in p or "PROJECT_HISTORY.md" in p or "artifacts/" in p:
            return AuthorityTier.TIER_4_OPERATIONAL, AuthorityRank.RANK_5_GENERAL

        # Tier 5: Advisory
        return AuthorityTier.TIER_5_ADVISORY, AuthorityRank.RANK_5_GENERAL

    @classmethod
    def compare_precedence(
        cls, tier_a: AuthorityTier, rank_a: AuthorityRank, tier_b: AuthorityTier, rank_b: AuthorityRank
    ) -> int:
        """Returns 1 if A > B, -1 if A < B, 0 if equal precedence (conflict)."""
        if tier_a < tier_b:
            return 1
        elif tier_a > tier_b:
            return -1

        # Same tier, check intra-tier rank
        if rank_a < rank_b:
            return 1
        elif rank_a > rank_b:
            return -1

        return 0
