#!/usr/bin/env python3
"""
Dynamic Axe-Core Execution Engine
Phase 9.7.5: Dynamic Accessibility Automation (Layer I)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Injects verified local axe-core artifact into real browser sessions,
executes dynamic DOM auditing against WCAG 2.1 AA rules, and constructs
canonical accessibility results.
"""

import time
import json
from typing import Optional, Dict, Any, List

from browser.models import BrowserExecutionStatus
from browser.cdp_driver import CDPBrowserDriver
from browser.exceptions import BrowserBridgeError, CDPCommandError
from .accessibility_models import (
    AccessibilityResult,
    AccessibilityViolation,
    AccessibilityIncomplete,
    AccessibilityPass,
    AccessibilityNode,
    AccessibilityPolicy,
)
from .axe_loader import AxeLoader, AxeArtifact, AxeArtifactNotFoundError, AxeIntegrityError
from .evidence import AccessibilityEvidenceGenerator


class AxeRunner:
    """
    Orchestrates axe-core injection and dynamic DOM analysis on live browser pages.
    Guarantees strict No False-Green semantics and complete failure isolation.
    """

    def __init__(
        self,
        policy: Optional[AccessibilityPolicy] = None,
        axe_artifact: Optional[AxeArtifact] = None
    ):
        self.policy = policy or AccessibilityPolicy()
        self.axe_artifact = axe_artifact

    def _resolve_artifact(self) -> AxeArtifact:
        """Resolves verified local artifact, or raises domain errors."""
        if self.axe_artifact:
            return self.axe_artifact
        return AxeLoader.get_artifact()

    def inject(self, driver: CDPBrowserDriver) -> str:
        """
        Injects axe-core into the active page context if not already present.
        Returns the confirmed axe-core version string.
        """
        if not driver.is_connected:
            raise BrowserBridgeError("Cannot inject axe-core: Browser driver is not connected")

        # Check if axe is already loaded in page
        try:
            is_loaded = driver.evaluate("typeof window.axe !== 'undefined' && typeof window.axe.run === 'function'")
            if is_loaded:
                version = driver.evaluate("window.axe.version")
                return str(version)
        except Exception:
            pass

        artifact = self._resolve_artifact()
        source = artifact.get_source()

        # Inject into frame context
        driver.evaluate(source)

        # Confirm injection success
        is_available = driver.evaluate("typeof window.axe !== 'undefined' && typeof window.axe.run === 'function'")
        if not is_available:
            raise BrowserBridgeError("Axe-core script evaluated, but window.axe is not defined on global object")

        version = driver.evaluate("window.axe.version")
        return str(version)

    def audit_page(
        self,
        driver: CDPBrowserDriver,
        capability_id: str = "MDS-A11Y-004",
        context_selector: str = "document",
        axe_options: Optional[Dict[str, Any]] = None
    ) -> AccessibilityResult:
        """
        Executes dynamic accessibility validation on the current document in driver.
        Returns canonical AccessibilityResult adhering strictly to the Tri-State contract.
        """
        start_time = time.perf_counter()

        # Guard: Check driver connectivity
        if not driver.is_connected:
            return AccessibilityResult(
                capability_id=capability_id,
                status=BrowserExecutionStatus.FAIL,
                duration_ms=0.0,
                error_message="Browser driver is not connected to active page",
                exception_type="BrowserBridgeError"
            )

        # 1. Inject axe-core
        try:
            axe_version = self.inject(driver)
        except AxeArtifactNotFoundError as e:
            # Missing artifact in environment is formally DEFERRED
            return AccessibilityResult(
                capability_id=capability_id,
                status=BrowserExecutionStatus.DEFERRED,
                duration_ms=(time.perf_counter() - start_time) * 1000.0,
                error_message=str(e),
                exception_type="AxeArtifactNotFoundError"
            )
        except AxeIntegrityError as e:
            # Corrupted artifact fails immediately with integrity breach
            return AccessibilityResult(
                capability_id=capability_id,
                status=BrowserExecutionStatus.FAIL,
                duration_ms=(time.perf_counter() - start_time) * 1000.0,
                error_message=str(e),
                exception_type="AxeIntegrityError"
            )
        except Exception as e:
            return AccessibilityResult(
                capability_id=capability_id,
                status=BrowserExecutionStatus.FAIL,
                duration_ms=(time.perf_counter() - start_time) * 1000.0,
                error_message=f"Failed to inject axe-core: {e}",
                exception_type=type(e).__name__
            )

        # 2. Build axe.run script
        options_json = json.dumps(axe_options or {
            "runOnly": {
                "type": "tag",
                "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "best-practice"]
            }
        })

        run_script = f"""
        (async () => {{
            if (typeof window.axe === 'undefined' || typeof window.axe.run !== 'function') {{
                throw new Error('axe-core is missing in page context');
            }}
            const context = {context_selector};
            const options = {options_json};
            const results = await window.axe.run(context, options);
            return {{
                axeVersion: window.axe.version,
                url: window.location.href,
                violations: (results.violations || []).map(v => ({{
                    id: v.id,
                    impact: v.impact,
                    description: v.description,
                    help: v.help,
                    helpUrl: v.helpUrl,
                    tags: v.tags || [],
                    nodes: (v.nodes || []).map(n => ({{
                        target: n.target || [],
                        html: (n.html || '').substring(0, 200),
                        failureSummary: n.failureSummary || null
                    }}))
                }})),
                incomplete: (results.incomplete || []).map(inc => ({{
                    id: inc.id,
                    impact: inc.impact,
                    description: inc.description,
                    help: inc.help,
                    helpUrl: inc.helpUrl,
                    tags: inc.tags || [],
                    nodesCount: (inc.nodes || []).length
                }})),
                passes: (results.passes || []).map(p => ({{
                    id: p.id,
                    description: p.description,
                    nodesCount: (p.nodes || []).length
                }}))
            }};
        }})()
        """

        # 3. Execute axe.run in page context
        try:
            raw_res = driver.evaluate(run_script)
            if not isinstance(raw_res, dict):
                raise BrowserBridgeError(f"Unexpected non-dict result returned by axe runner: {type(raw_res)}")
        except Exception as e:
            return AccessibilityResult(
                capability_id=capability_id,
                status=BrowserExecutionStatus.FAIL,
                duration_ms=(time.perf_counter() - start_time) * 1000.0,
                axe_version=axe_version,
                error_message=f"axe.run execution failed: {e}",
                exception_type=type(e).__name__
            )

        duration = (time.perf_counter() - start_time) * 1000.0

        # 4. Parse violations, incomplete, and passes into domain models
        violations: List[AccessibilityViolation] = []
        for v_data in raw_res.get("violations", []):
            nodes = [
                AccessibilityNode(
                    target=n.get("target", []),
                    html=n.get("html", ""),
                    failure_summary=n.get("failureSummary")
                )
                for n in v_data.get("nodes", [])
            ]
            violations.append(
                AccessibilityViolation(
                    id=v_data.get("id", "unknown"),
                    impact=v_data.get("impact", "moderate"),
                    description=v_data.get("description", ""),
                    help=v_data.get("help", ""),
                    help_url=v_data.get("helpUrl", ""),
                    tags=v_data.get("tags", []),
                    nodes=nodes
                )
            )

        incomplete: List[AccessibilityIncomplete] = [
            AccessibilityIncomplete(
                id=inc.get("id", "unknown"),
                impact=inc.get("impact"),
                description=inc.get("description", ""),
                help=inc.get("help", ""),
                help_url=inc.get("helpUrl", ""),
                tags=inc.get("tags", []),
                nodes_count=inc.get("nodesCount", 0)
            )
            for inc in raw_res.get("incomplete", [])
        ]

        passes: List[AccessibilityPass] = [
            AccessibilityPass(
                id=p.get("id", "unknown"),
                description=p.get("description", ""),
                nodes_count=p.get("nodesCount", 0)
            )
            for p in raw_res.get("passes", [])
        ]

        # 5. Apply Policy Evaluation
        eval_status, eval_summary = self.policy.evaluate(violations, incomplete)

        page_url = raw_res.get("url") or getattr(driver, "_active_url", None)
        browser_name = getattr(driver.browser_info, "name", "Chromium") if driver.browser_info else "Chromium"
        viewport_dict = driver._viewport.to_dict() if hasattr(driver, "_viewport") and driver._viewport else None

        result = AccessibilityResult(
            capability_id=capability_id,
            status=eval_status,
            axe_version=raw_res.get("axeVersion", axe_version),
            page_url=page_url,
            browser=browser_name,
            viewport=viewport_dict,
            violation_count=len(violations),
            incomplete_count=len(incomplete),
            pass_count=len(passes),
            violations=[v.to_dict() for v in violations],
            incomplete=[inc.to_dict() for inc in incomplete],
            passes=[p.to_dict() for p in passes],
            duration_ms=duration,
            evidence={},
            error_message=eval_summary if eval_status == BrowserExecutionStatus.FAIL else None,
            exception_type=None
        )

        # Assemble full audit evidence
        result.evidence = AccessibilityEvidenceGenerator.build_evidence(result, raw_res)
        return result
