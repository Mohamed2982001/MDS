#!/usr/bin/env python3
"""
DSSE Requirements & Constraints Analyzer
Analyzes unstructured project text, requirements briefs, PRD/SDD files, or repository
structures to infer the 12 DSSE dimension priorities and mandatory hard constraints.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from tools.dsse.validator import CANONICAL_DIMENSIONS

# Keyword mappings for the 12 canonical DSSE dimensions
DIMENSION_KEYWORD_PATTERNS = {
    "D1": [
        r"\bflutter\b", r"\bnext\.?js\b", r"\breact\b", r"\bvue\b", r"\bweb\b",
        r"\bmobile\b", r"\bdesktop\b", r"\bcross-platform\b", r"\bnative\b", r"\bios\b", r"\bandroid\b"
    ],
    "D2": [
        r"\baesthetic\b", r"\bdesign language\b", r"\bminimal\b", r"\bsoft modern\b",
        r"\bexpressive\b", r"\bdark mode\b", r"\blight mode\b", r"\bvisual\b", r"\bclean ui\b"
    ],
    "D3": [
        r"\bwcag\b", r"\baccessibility\b", r"\ba11y\b", r"\bscreen reader\b",
        r"\bkeyboard\b", r"\bfocus\b", r"\bcontrast\b", r"\bcompliance\b", r"\baria\b"
    ],
    "D4": [
        r"\barabic\b", r"\brtl\b", r"\bbidirectional\b", r"\bcairo\b",
        r"\blocalization\b", r"\bi18n\b", r"\bl10n\b", r"\btranslation\b"
    ],
    "D5": [
        r"\bdensity\b", r"\bcompact\b", r"\bcomfortable\b", r"\bdata-dense\b",
        r"\btable\b", r"\bspreadsheet\b", r"\badmin\b", r"\bdata ergonomics\b"
    ],
    "D6": [
        r"\bcomponents?\b", r"\bbutton\b", r"\binput\b", r"\bdialog\b",
        r"\bmodal\b", r"\btabs\b", r"\bforms?\b", r"\becosystem\b", r"\bbreadth\b"
    ],
    "D7": [
        r"\btokens?\b", r"\bdtcg\b", r"\bw3c\b", r"\bextensibility\b",
        r"\bdesign tokens\b", r"\bsemantic aliasing\b", r"\bheadless\b"
    ],
    "D8": [
        r"\bresponsive\b", r"\brecomposition\b", r"\bviewports?\b",
        r"\btablet\b", r"\bbreakpoint\b", r"\bmaster-detail\b", r"\b320px\b", r"\b1440px\b"
    ],
    "D9": [
        r"\benterprise\b", r"\brbac\b", r"\baudit log\b", r"\bpermissions?\b",
        r"\bdata grid\b", r"\bbatch actions?\b", r"\bback-office\b"
    ],
    "D10": [
        r"\bai\b", r"\bai-native\b", r"\bprompt\b", r"\bstreaming\b",
        r"\bllm\b", r"\blive region\b", r"\bspeech\b", r"\bgenerative ui\b", r"\bchat\b"
    ],
    "D11": [
        r"\bcustomization\b", r"\bwhite-label\b", r"\bmulti-brand\b",
        r"\btheme overrides?\b", r"\bpreset\b", r"\btheming\b"
    ],
    "D12": [
        r"\bdeveloper ecosystem\b", r"\btypescript\b", r"\bdart\b",
        r"\bpub\.dev\b", r"\bnpm\b", r"\bdocs\b", r"\bdocumentation\b", r"\bunit tests?\b"
    ]
}

CRITICAL_INTENSIFIERS = [
    r"\bmust\b", r"\bcritical\b", r"\bmandatory\b", r"\bnon-negotiable\b",
    r"\brequired\b", r"\bessential\b", r"\bstrictly\b"
]

HIGH_INTENSIFIERS = [
    r"\bhigh priority\b", r"\bimportant\b", r"\bmajor\b", r"\bsignificant\b", r"\bkey\b"
]


class DSSEAnalyzer:
    def __init__(self):
        self.dim_regexes = {
            dim: [re.compile(p, re.IGNORECASE) for p in patterns]
            for dim, patterns in DIMENSION_KEYWORD_PATTERNS.items()
        }
        self.critical_regexes = [re.compile(p, re.IGNORECASE) for p in CRITICAL_INTENSIFIERS]
        self.high_regexes = [re.compile(p, re.IGNORECASE) for p in HIGH_INTENSIFIERS]

    def analyze_text(
        self,
        text: str,
        project_name: str = "Inferred Project",
        source_evidence: str = "INFERRED"
    ) -> Dict[str, Any]:
        """
        Analyzes requirements text to infer project profile and dimensions.
        """
        sentences = re.split(r"[.\n;]+", text)
        dim_scores: Dict[str, int] = {dim: 0 for dim in CANONICAL_DIMENSIONS}
        dim_intensified_critical: Set[str] = set()
        dim_intensified_high: Set[str] = set()

        for sent in sentences:
            s_clean = sent.strip()
            if not s_clean:
                continue

            is_crit = any(r.search(s_clean) for r in self.critical_regexes)
            is_high = any(r.search(s_clean) for r in self.high_regexes)

            for dim, regex_list in self.dim_regexes.items():
                match_count = sum(1 for r in regex_list if r.search(s_clean))
                if match_count > 0:
                    dim_scores[dim] += match_count
                    if is_crit:
                        dim_intensified_critical.add(dim)
                    elif is_high:
                        dim_intensified_high.add(dim)

        # Assign priority tier for each dimension
        inferred_dimensions: Dict[str, str] = {}
        for dim, count in dim_scores.items():
            if count == 0:
                # Omitted dimension (unmentioned in requirements text)
                continue

            if dim in dim_intensified_critical or count >= 4:
                inferred_dimensions[dim] = "Critical"
            elif dim in dim_intensified_high or count >= 2:
                inferred_dimensions[dim] = "High"
            elif count == 1:
                inferred_dimensions[dim] = "Medium"

        # Detect mandatory hard constraints
        hard_constraints: List[Dict[str, str]] = []
        text_lower = text.lower()

        if "flutter" in text_lower and any(w in text_lower for w in ["must", "mandatory", "compile", "native"]):
            hard_constraints.append({
                "id": "HC-FLUTTER-NATIVE",
                "description": "Must natively compile to Flutter without webviews or wrappers",
                "dimension": "D1"
            })

        if "wcag" in text_lower or ("accessibility" in text_lower and "aa" in text_lower):
            hard_constraints.append({
                "id": "HC-WCAG-AA",
                "description": "Must satisfy WCAG 2.1/2.2 AA accessibility requirements",
                "dimension": "D3"
            })

        if "arabic" in text_lower or "rtl" in text_lower:
            hard_constraints.append({
                "id": "HC-ARABIC-RTL",
                "description": "Must support first-class Arabic bidirectional layout out of the box",
                "dimension": "D4"
            })

        if "zero-dependency" in text_lower or "no npm" in text_lower:
            hard_constraints.append({
                "id": "HC-ZERO-DEPENDENCY",
                "description": "Must operate with zero external package dependencies",
                "dimension": "D12"
            })

        # Infer target platform
        target_platform = "Web"
        if "flutter" in text_lower:
            target_platform = "Flutter (Mobile & Web)"
        elif "next" in text_lower or "react" in text_lower:
            target_platform = "Next.js / React (Web)"

        return {
            "projectName": project_name,
            "context": text[:200].replace("\n", " ").strip() + ("..." if len(text) > 200 else ""),
            "targetPlatform": target_platform,
            "dimensions": inferred_dimensions,
            "hardConstraints": hard_constraints,
            "metadata": {
                "sourceEvidenceTier": source_evidence,
                "inferredBy": "DSSEAnalyzer v1.0.0"
            }
        }

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyzes a file from disk.
        """
        p = Path(file_path).resolve()
        if not p.exists():
            raise FileNotFoundError(f"Input file not found: {p}")

        content = p.read_text(encoding="utf-8")
        project_name = p.stem.replace("-", " ").replace("_", " ").title()

        # If it's a formal PRD or SDD, assign OFFICIAL_DOCS evidence tier
        tier = "OFFICIAL_DOCS" if any(k in p.name.upper() for k in ["PRD", "SDD", "SPEC", "ROADMAP"]) else "INFERRED"

        return self.analyze_text(content, project_name=project_name, source_evidence=tier)
