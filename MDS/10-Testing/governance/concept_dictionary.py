"""Canonical Concept Dictionary & Semantic Normalization Pipeline for MDS.

Implements:
1. Canonical Concept IDs and Aliases (ADR-098)
2. Four-Stage Semantic Normalization Pipeline:
   Lexical Normalization -> Concept Matching -> Value Extraction -> Contradiction Evaluation
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ConceptEntry:
    concept_id: str
    canonical_name: str
    canonical_value: Any
    category: str
    aliases: List[str] = field(default_factory=list)
    regex_patterns: List[str] = field(default_factory=list)
    unit: Optional[str] = None


class ConceptDictionary:
    """Canonical registry of normalized system concepts."""

    def __init__(self) -> None:
        self.entries: Dict[str, ConceptEntry] = {}
        self._alias_lookup: Dict[str, str] = {}
        self._populate_canonical_concepts()

    def _populate_canonical_concepts(self) -> None:
        raw_concepts = [
            ConceptEntry(
                concept_id="CONTAINER.MAX_WIDTH.DEFAULT",
                canonical_name="Default Container Max Width",
                canonical_value="1152px",
                category="LAYOUT",
                aliases=["standard container", "container max width", "base container width", "max-width: 1152px"],
                regex_patterns=[r"container\s+(?:max-width|width)\s*[:=]?\s*(\d+px)"],
                unit="px",
            ),
            ConceptEntry(
                concept_id="CONTAINER.MAX_WIDTH.WIDE",
                canonical_name="Wide Container Max Width",
                canonical_value="1440px",
                category="LAYOUT",
                aliases=["wide container", "expanded container", "1440px container"],
                regex_patterns=[r"wide\s+container\s*[:=]?\s*(\d+px)"],
                unit="px",
            ),
            ConceptEntry(
                concept_id="TOUCH_TARGET.MIN_SIZE",
                canonical_name="Minimum Touch Target Size",
                canonical_value="44px",
                category="ACCESSIBILITY",
                aliases=["touch target", "minimum target size", "press target", "44x44px", "44px touch target"],
                regex_patterns=[r"touch\s+target\s*[:=]?\s*(\d+px)", r"(\d+)x(\d+)\s*px\s+touch\s+target"],
                unit="px",
            ),
            ConceptEntry(
                concept_id="FOCUS_RING.WIDTH",
                canonical_name="Focus Ring Width",
                canonical_value="2px",
                category="ACCESSIBILITY",
                aliases=["focus ring width", "focus outline width", "2px focus ring"],
                regex_patterns=[r"focus\s+ring\s*[:=]?\s*(\d+px)"],
                unit="px",
            ),
            ConceptEntry(
                concept_id="TYPOGRAPHY.FONT_FAMILY.PRIMARY",
                canonical_name="Primary Font Family",
                canonical_value="Cairo",
                category="TYPOGRAPHY",
                aliases=["primary font", "body font", "cairo font", "global font"],
                regex_patterns=[r"font-family\s*:\s*['\"]?([A-Za-z]+)['\"]?"],
            ),
            ConceptEntry(
                concept_id="INTERNATIONALIZATION.DIRECTION.DEFAULT",
                canonical_name="Default Text Direction",
                canonical_value="rtl",
                category="I18N",
                aliases=["default direction", "dir='rtl'", "rtl default", "right to left"],
                regex_patterns=[r"dir\s*=\s*['\"]?([a-z]{3})['\"]?"],
            ),
            ConceptEntry(
                concept_id="TOKENS.TOTAL_COUNT",
                canonical_name="Total Registered Tokens",
                canonical_value=188,
                category="CARDINALITY",
                aliases=["registered tokens", "total tokens", "188 tokens", "canonical token count"],
                regex_patterns=[r"(\d+)\s+tokens"],
            ),
            ConceptEntry(
                concept_id="COMPONENTS.TOTAL_COUNT",
                canonical_name="Total Canonical Components",
                canonical_value=19,
                category="CARDINALITY",
                aliases=["canonical components", "core components", "19 components"],
                regex_patterns=[r"(\d+)\s+components"],
            ),
            ConceptEntry(
                concept_id="PATTERNS.TOTAL_COUNT",
                canonical_name="Total Canonical Patterns",
                canonical_value=8,
                category="CARDINALITY",
                aliases=["canonical patterns", "8 patterns"],
                regex_patterns=[r"(\d+)\s+patterns"],
            ),
            ConceptEntry(
                concept_id="WORKFLOWS.TOTAL_COUNT",
                canonical_name="Total Canonical Workflows",
                canonical_value=6,
                category="CARDINALITY",
                aliases=["canonical workflows", "6 workflows"],
                regex_patterns=[r"(\d+)\s+workflows"],
            ),
            ConceptEntry(
                concept_id="TEMPLATES.TOTAL_COUNT",
                canonical_name="Total Canonical Templates",
                canonical_value=6,
                category="CARDINALITY",
                aliases=["canonical templates", "6 templates"],
                regex_patterns=[r"(\d+)\s+templates"],
            ),
            ConceptEntry(
                concept_id="FSM.STATES.COUNT",
                canonical_name="Universal FSM Operational States Count",
                canonical_value=11,
                category="STATE_MACHINE",
                aliases=["fsm states", "11 states", "operational states"],
                regex_patterns=[r"(\d+)\s+standardized\s+operational\s+states"],
            ),
            ConceptEntry(
                concept_id="CAPABILITIES.TOTAL_COUNT",
                canonical_name="Total Declarative Capabilities",
                canonical_value=170,
                category="CAPABILITY",
                aliases=["total capabilities", "170 capabilities", "registered capabilities"],
                regex_patterns=[r"(\d+)\s+capabilities"],
            ),
        ]

        for entry in raw_concepts:
            self.entries[entry.concept_id] = entry
            self._alias_lookup[self.normalize_lexical(entry.canonical_name)] = entry.concept_id
            for alias in entry.aliases:
                self._alias_lookup[self.normalize_lexical(alias)] = entry.concept_id

    # -------------------------------------------------------------------------
    # Stage 1: Lexical Normalization
    # -------------------------------------------------------------------------
    @staticmethod
    def normalize_lexical(text: str) -> str:
        """Lowercases, trims whitespace, and standardizes spacing and units."""
        t = text.lower().strip()
        t = re.sub(r"pixels?", "px", t)
        t = re.sub(r"\s+", " ", t)
        t = re.sub(r"['\"]", "", t)
        return t

    # -------------------------------------------------------------------------
    # Stage 2: Concept Matching
    # -------------------------------------------------------------------------
    def match_concept(self, phrase: str) -> Optional[ConceptEntry]:
        norm = self.normalize_lexical(phrase)
        if norm in self._alias_lookup:
            cid = self._alias_lookup[norm]
            return self.entries.get(cid)

        # Substring / fuzzy match with delimiter normalization
        norm_space = re.sub(r"[-_:]", " ", norm)
        norm_space = re.sub(r"\s+", " ", norm_space)

        for alias, cid in self._alias_lookup.items():
            if alias in norm or norm in alias or alias in norm_space:
                return self.entries.get(cid)

        return None

    # -------------------------------------------------------------------------
    # Stage 3: Value Extraction
    # -------------------------------------------------------------------------
    def extract_value(self, phrase: str, entry: ConceptEntry) -> Optional[Any]:
        norm = self.normalize_lexical(phrase)
        for pattern in entry.regex_patterns:
            m = re.search(pattern, norm)
            if m:
                raw_val = m.group(1)
                if isinstance(entry.canonical_value, int):
                    try:
                        return int(raw_val)
                    except ValueError:
                        pass
                return raw_val

        # Fallback unit extraction if defined
        if entry.unit:
            m = re.search(r"(\d+" + re.escape(entry.unit) + r")", norm)
            if m:
                return m.group(1)

        # If phrase contains exact canonical value
        if str(entry.canonical_value).lower() in norm:
            return entry.canonical_value

        return None

    # -------------------------------------------------------------------------
    # Stage 4: Contradiction Evaluation
    # -------------------------------------------------------------------------
    def evaluate_contradiction(
        self, phrase_a: str, phrase_b: str
    ) -> Tuple[bool, Optional[str], Optional[Any], Optional[Any]]:
        """Evaluates whether two phrases refer to the same concept but express contradictory values."""
        entry_a = self.match_concept(phrase_a)
        entry_b = self.match_concept(phrase_b)

        if not entry_a or not entry_b:
            return False, None, None, None

        if entry_a.concept_id != entry_b.concept_id:
            # Different concepts, no contradiction
            return False, None, None, None

        val_a = self.extract_value(phrase_a, entry_a)
        val_b = self.extract_value(phrase_b, entry_b)

        if val_a is not None and val_b is not None and val_a != val_b:
            return True, entry_a.concept_id, val_a, val_b

        return False, entry_a.concept_id, val_a, val_b
