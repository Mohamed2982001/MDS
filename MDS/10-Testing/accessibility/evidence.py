#!/usr/bin/env python3
"""
Accessibility Evidence Generator & Serializer
Phase 9.7.5: Dynamic Accessibility Automation (Layer I)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Transforms raw axe-core audit results into structured, audit-grade evidence
conforming to the Master Design System governance contracts.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from .accessibility_models import (
    AccessibilityResult,
    AccessibilityViolation,
    AccessibilityIncomplete,
    AccessibilityPass,
    AccessibilityNode,
)


class AccessibilityEvidenceGenerator:
    """Utilities for serializing and formatting accessibility validation evidence."""

    @staticmethod
    def build_evidence(
        result: AccessibilityResult,
        raw_axe_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Assembles a comprehensive audit evidence bundle."""
        evidence = {
            "capability_id": result.capability_id,
            "status": result.status.value if hasattr(result.status, "value") else str(result.status),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "audit_environment": {
                "browser": result.browser,
                "axe_version": result.axe_version,
                "page_url": result.page_url,
                "viewport": result.viewport,
            },
            "summary_metrics": {
                "violation_count": result.violation_count,
                "incomplete_count": result.incomplete_count,
                "pass_count": result.pass_count,
                "duration_ms": result.duration_ms,
            },
            "violations_summary": [
                {
                    "id": v.get("id"),
                    "impact": v.get("impact"),
                    "description": v.get("description"),
                    "help": v.get("help"),
                    "helpUrl": v.get("helpUrl"),
                    "affected_nodes_count": len(v.get("nodes", [])),
                    "targets": [node.get("target") for node in v.get("nodes", [])[:5]]
                }
                for v in result.violations
            ],
            "incomplete_summary": [
                {
                    "id": inc.get("id"),
                    "impact": inc.get("impact"),
                    "description": inc.get("description"),
                    "nodes_count": inc.get("nodes_count", 0)
                }
                for inc in result.incomplete
            ]
        }

        if result.error_message:
            evidence["error_details"] = {
                "error_message": result.error_message,
                "exception_type": result.exception_type,
            }

        return evidence

    @staticmethod
    def format_text_report(result: AccessibilityResult) -> str:
        """Renders an executive human-readable text summary of the audit."""
        lines = [
            "=" * 70,
            f"          MDS ACCESSIBILITY AUDIT REPORT: {result.capability_id}",
            "=" * 70,
            f"Status:       {result.status.value if hasattr(result.status, 'value') else result.status}",
            f"Page URL:     {result.page_url or 'N/A'}",
            f"Browser:      {result.browser or 'Unknown'}",
            f"axe-core:     v{result.axe_version or 'N/A'}",
            f"Duration:     {result.duration_ms:.1f}ms",
            f"Metrics:      Violations: {result.violation_count} | Incomplete: {result.incomplete_count} | Passed: {result.pass_count}",
            "-" * 70,
        ]

        if result.violations:
            lines.append("VIOLATIONS DETECTED:")
            for idx, v in enumerate(result.violations, 1):
                impact = (v.get("impact") or "UNKNOWN").upper()
                lines.append(f"  {idx}. [{impact}] {v.get('id')}: {v.get('help')}")
                lines.append(f"     Description: {v.get('description')}")
                lines.append(f"     Help URL:    {v.get('helpUrl')}")
                nodes = v.get("nodes", [])
                lines.append(f"     Affected Elements ({len(nodes)}):")
                for n in nodes[:3]:
                    target_str = ", ".join(n.get("target", []))
                    lines.append(f"       - Target: {target_str}")
                    lines.append(f"         Snippet: {n.get('html')}")
                if len(nodes) > 3:
                    lines.append(f"       - ... and {len(nodes) - 3} more element(s)")
                lines.append("")
        else:
            lines.append("VIOLATIONS: None detected (0 violations).")

        if result.incomplete:
            lines.append("-" * 70)
            lines.append(f"INCOMPLETE CHECKS ({len(result.incomplete)} items requiring review):")
            for inc in result.incomplete:
                lines.append(f"  * {inc.get('id')}: {inc.get('description')} ({inc.get('nodes_count', 0)} node(s))")

        if result.error_message:
            lines.append("-" * 70)
            lines.append(f"ERROR: {result.error_message}")
            if result.exception_type:
                lines.append(f"Exception Type: {result.exception_type}")

        lines.append("=" * 70)
        return "\n".join(lines)
