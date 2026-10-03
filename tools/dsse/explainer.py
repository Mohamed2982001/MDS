#!/usr/bin/env python3
"""
DSSE Explain & Audit Report Generator
Transforms formal DSSE decision reports into human-readable engineering audit trails
in Markdown or terminal text format.
"""

from typing import Any, Dict, List


class DSSEExplainer:
    @staticmethod
    def to_markdown(report_data: Dict[str, Any]) -> str:
        """
        Renders a decision report into rich GitHub-flavored Markdown.
        """
        sr = report_data.get("selectionReport", {})
        proj = sr.get("projectProfile", {})
        rec = sr.get("recommendation", {})
        margin = sr.get("decisionMargin", {})
        conf = sr.get("epistemicConfidence", {})
        conf_metrics = conf.get("metrics", {})
        hc = sr.get("hardConstraints", {})
        ranking = sr.get("ranking", [])
        gov = sr.get("governance", {})
        cfg = sr.get("selectedConfiguration", {})
        digest = sr.get("reproducibilityDigest", "N/A")
        ver = sr.get("engineVersion", "1.0.0")

        lines: List[str] = []
        lines.append("# Design System Selection Engine (DSSE) -- Decision & Audit Report")
        lines.append(f"**Engine Version:** {ver}  ")
        lines.append(f"**Reproducibility Digest (SHA-256):** `{digest}`  ")
        lines.append(f"**Project:** {proj.get('projectName', 'N/A')}  ")
        if proj.get("context"):
            lines.append(f"**Context:** {proj.get('context')}  ")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 1. Executive Recommendation
        lines.append("## 1. Executive Recommendation")
        lines.append(f"- **Recommended System:** **{rec.get('selectedSystem', 'None')}**")
        lines.append(f"- **Selection Score:** `{rec.get('selectionScore', 0.0):.1f}%` (Rank #{rec.get('rank', 1)})")
        lines.append(f"- **Decision Margin (Delta):** `+{margin.get('delta', 0.0):.1f}%` -- **{margin.get('classification', 'N/A')}**")
        lines.append(f"- **Epistemic Confidence:** **{conf.get('tier', 'LOW')}** (Score: `{conf.get('score', 0.0):.4f}`)")
        lines.append("")

        # 2. Selected Configuration Blueprint
        if cfg:
            lines.append("## 2. Recommended Configuration Blueprint")
            lines.append("| Setting | Assigned Value |")
            lines.append("| :--- | :--- |")
            for k, v in cfg.items():
                nice_key = k.replace("primary", "Primary ").replace("preset", "Preset").replace("density", "Density").replace("mode", "Theme Mode").replace("Font", "Font")
                lines.append(f"| **{nice_key}** | `{v}` |")
            lines.append("")

        # 3. Decision Margin & Tie-Break Audit
        lines.append("## 3. Decision Margin & Tie-Break Analysis")
        lines.append(f"- **Score Lead over Runner-Up:** `+{margin.get('delta', 0.0):.1f}%`")
        lines.append(f"- **Margin Classification:** `{margin.get('classification')}`")
        lines.append(f"- **Tie-Break Cascade Triggered:** `{'Yes' if margin.get('tieBreakTriggered') else 'No'}`")
        if margin.get("tieBreakLog"):
            lines.append("\n**Tie-Break Cascade Execution Log:**")
            for log_entry in margin.get("tieBreakLog", []):
                lines.append(f"- {log_entry}")
        lines.append("")

        # 4. Epistemic Confidence Audit
        lines.append("## 4. Epistemic Confidence Audit (Information Fidelity)")
        lines.append(f"- **Confidence Tier:** **{conf.get('tier')}** (Conjunctive Metric: `{conf.get('score', 0.0):.4f}`)")
        lines.append(f"- **Requirements Coverage (C_req):** `{conf_metrics.get('requirementsCoverage', 0.0) * 100:.1f}%` ({proj.get('declaredDimensionsCount', 0)}/12 declared)")
        lines.append(f"- **Evaluation Coverage (C_eval):** `{conf_metrics.get('evaluationCoverage', 0.0) * 100:.1f}%` ({proj.get('activeDimensionsCount', 0)} active dimensions benchmarked)")
        lines.append(f"- **Evidence Quality (C_evid):** `{conf_metrics.get('evidenceQuality', 0.0):.4f}` (Importance-weighted evidence depth)")
        lines.append("")

        # 5. Hard Constraints Eligibility Gate
        lines.append("## 5. Hard Constraints & Disqualifications")
        lines.append(f"- **Overall Constraint Gate:** `{hc.get('status')}`")
        lines.append(f"- **Constraints Evaluated:** `{hc.get('evaluatedCount', 0)}`")
        lines.append(f"- **Candidates Disqualified:** `{hc.get('disqualifiedCount', 0)}`")
        lines.append("")

        # 6. Candidate Ranking Matrix
        lines.append("## 6. Candidate Ranking Matrix")
        lines.append("| Rank | Candidate Design System | Selection Score | Status |")
        lines.append("| :---: | :--- | :---: | :--- |")
        for item in ranking:
            status_display = f"**{item.get('status')}**" if "Disqualified" in item.get('status') else item.get('status')
            lines.append(f"| **{item.get('rank')}** | {item.get('system')} | `{item.get('score'):.1f}%` | {status_display} |")
        lines.append("")

        # 7. Governance & Human Review Directives
        lines.append("## 7. Governance & Human Review Directives")
        if gov.get("humanReviewRequired"):
            lines.append("> [!WARNING] **MANDATORY HUMAN ARCHITECT REVIEW REQUIRED**")
            lines.append("> Autonomous adoption is blocked. The following conditions necessitate human architect intervention:")
            for reason in gov.get("humanReviewReasons", []):
                lines.append(f"> - [!] **{reason}**")
        else:
            lines.append("> [!NOTE] **AUTONOMOUS CLEARANCE GRANTED**")
            lines.append("> All hard constraints passed, epistemic confidence is HIGH, and the decision lead is decisive. No human architect review is required.")
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def to_terminal_text(report_data: Dict[str, Any]) -> str:
        """
        Renders a decision report into clean formatted plain text suitable for terminal output.
        """
        sr = report_data.get("selectionReport", {})
        proj = sr.get("projectProfile", {})
        rec = sr.get("recommendation", {})
        margin = sr.get("decisionMargin", {})
        conf = sr.get("epistemicConfidence", {})
        conf_metrics = conf.get("metrics", {})
        ranking = sr.get("ranking", [])
        gov = sr.get("governance", {})
        cfg = sr.get("selectedConfiguration", {})
        digest = sr.get("reproducibilityDigest", "N/A")

        lines: List[str] = []
        lines.append("================================================================================")
        lines.append("           DESIGN SYSTEM SELECTION ENGINE (DSSE) -- EVALUATION REPORT          ")
        lines.append("================================================================================")
        lines.append(f"Project Name          : {proj.get('projectName', 'N/A')}")
        lines.append(f"Recommended System    : {rec.get('selectedSystem', 'None')} (Score: {rec.get('selectionScore', 0.0):.1f}%)")
        lines.append(f"Decision Margin (Delta): +{margin.get('delta', 0.0):.1f}% [{margin.get('classification', 'N/A')}]")
        lines.append(f"Epistemic Confidence  : {conf.get('tier', 'LOW')} (Score: {conf.get('score', 0.0):.4f})")
        lines.append(f"Human Review Required : {'YES (MANDATORY)' if gov.get('humanReviewRequired') else 'NO (Autonomous Clearance)'}")
        lines.append(f"Reproducibility Digest: {digest[:16]}...")
        lines.append("--------------------------------------------------------------------------------")
        lines.append("RECOMMENDED CONFIGURATION:")
        for k, v in cfg.items():
            lines.append(f"  - {k:<20}: {v}")
        lines.append("--------------------------------------------------------------------------------")
        lines.append("INFORMATION FIDELITY METRICS:")
        lines.append(f"  - Requirements Coverage (C_req) : {conf_metrics.get('requirementsCoverage', 0.0)*100:.1f}% ({proj.get('declaredDimensionsCount', 0)}/12 declared)")
        lines.append(f"  - Evaluation Coverage (C_eval)   : {conf_metrics.get('evaluationCoverage', 0.0)*100:.1f}% ({proj.get('activeDimensionsCount', 0)} active rated)")
        lines.append(f"  - Evidence Quality (C_evid)     : {conf_metrics.get('evidenceQuality', 0.0):.4f}")
        lines.append("--------------------------------------------------------------------------------")
        lines.append("CANDIDATE RANKING MATRIX:")
        for item in ranking:
            lines.append(f"  #{item.get('rank'):<2} {item.get('system'):<30} {item.get('score'):>5.1f}%  [{item.get('status')}]")
        lines.append("--------------------------------------------------------------------------------")
        if gov.get("humanReviewRequired"):
            lines.append("GOVERNANCE NOTICES (HUMAN REVIEW REQUIRED):")
            for r in gov.get("humanReviewReasons", []):
                lines.append(f"  [!] {r}")
        else:
            lines.append("GOVERNANCE NOTICES: All criteria satisfied; autonomous promotion approved.")
        lines.append("================================================================================")

        return "\n".join(lines)
