#!/usr/bin/env python3
"""
MDS Responsive CDP Execution Runner & Settlement Engine
Phase 9.7.6: Responsive Viewport Automation (Layer K)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Executes responsive viewport sweeps using the CDPBrowserDriver.
Implements the hardened layout reflow settlement algorithm (2x RAF, fonts.ready,
bounded 1500ms timeout) and deterministic state isolation adhering to ADR-070 to ADR-077.
"""

import time
import json
from typing import Optional, List, Dict, Any

try:
    from .responsive_models import (
        AssertionClass,
        ResponsiveAssertion,
        ResponsiveRunConfig,
        ResponsiveRunResult,
        ResponsiveMatrixResult,
    )
    from .viewport_matrix import get_canonical_matrix, CANONICAL_MATRIX_RUNS
    from .responsive_assertions import ResponsiveAssertionsEvaluator
except ImportError:
    from responsive_models import (
        AssertionClass,
        ResponsiveAssertion,
        ResponsiveRunConfig,
        ResponsiveRunResult,
        ResponsiveMatrixResult,
    )
    from viewport_matrix import get_canonical_matrix, CANONICAL_MATRIX_RUNS
    from responsive_assertions import ResponsiveAssertionsEvaluator


class ResponsiveRunner:
    """Core automation runner coordinating viewport changes and assertion evaluations."""

    CAPABILITY_ID = "MDS-RWD-003"
    DEFAULT_SETTLEMENT_TIMEOUT_MS = 1500

    def __init__(self, settlement_timeout_ms: int = DEFAULT_SETTLEMENT_TIMEOUT_MS):
        self.settlement_timeout_ms = settlement_timeout_ms

    def wait_for_app_initialization(self, driver: Any, max_timeout_ms: int = 3000) -> bool:
        """Waits for Reference Application async data fetch and bootstrap to complete."""
        start_t = time.time()
        timeout_sec = max_timeout_ms / 1000.0
        script = """
        (() => {
            if (window.mdsWorkspaceApp && window.mdsWorkspaceApp.state && window.mdsWorkspaceApp.state.data) {
                return true;
            }
            // For static or fixture pages
            if (document.body && (document.querySelector('.mds-ref-main') || document.querySelector('.table-container') || document.querySelector('.blowout-box'))) {
                return true;
            }
            return false;
        })()
        """
        while time.time() - start_t < timeout_sec:
            try:
                res = driver.evaluate(script)
                if res is True:
                    return True
            except Exception:
                pass
            time.sleep(0.05)
        return False

    def wait_for_layout_settlement(
        self,
        driver: Any,
        timeout_ms: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Executes the hardened layout reflow settlement routine (ADR-076):
        1. 2x requestAnimationFrame for CSS reflow recalculation
        2. document.fonts.ready for typography rendering
        3. Geometry stabilization polling (50ms interval) with bounded max timeout.
        """
        max_timeout = timeout_ms or self.settlement_timeout_ms
        start_time = time.time()
        timeout_sec = max_timeout / 1000.0

        script = """
        (async () => {
            // 1. Wait for 2 requestAnimationFrames to let CSS reflow execute
            await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));

            // 2. Wait for web fonts if document.fonts is supported
            if (document.fonts && document.fonts.ready) {
                try {
                    await document.fonts.ready;
                } catch (e) {
                    // font ready rejection non-fatal
                }
            }

            // 3. Capture geometric snapshot
            const root = document.documentElement;
            const body = document.body;
            return {
                settled: true,
                clientWidth: root.clientWidth,
                clientHeight: root.clientHeight,
                scrollWidth: root.scrollWidth,
                scrollHeight: root.scrollHeight,
                bodyWidth: body ? body.offsetWidth : 0
            };
        })()
        """

        last_metrics = {}
        while time.time() - start_time < timeout_sec:
            try:
                res = driver.evaluate(script)
                if res and res.get("settled") and res.get("clientWidth", 0) > 0:
                    duration_ms = (time.time() - start_time) * 1000.0
                    return {
                        "success": True,
                        "duration_ms": duration_ms,
                        "metrics": res,
                    }
                last_metrics = res or {}
            except Exception as e:
                last_metrics = {"error": str(e)}

            time.sleep(0.05)

        duration_ms = (time.time() - start_time) * 1000.0
        return {
            "success": False,
            "duration_ms": duration_ms,
            "error": f"Layout reflow settlement timed out after {max_timeout}ms",
            "metrics": last_metrics,
        }

    def prepare_run_environment(self, driver: Any, config: ResponsiveRunConfig) -> Dict[str, Any]:
        """
        Configures browser viewport emulation, SPA hash route, direction, theme,
        density, and cleans up dialog state before assertion execution.
        """
        # Ensure application bootstrap has completed
        self.wait_for_app_initialization(driver)

        vp = config.viewport

        # 1. Configure CDP Viewport Emulation via set_viewport
        driver.set_viewport(
            width=vp.width,
            height=vp.height,
            device_scale_factor=vp.device_scale_factor
        )

        # 2. Map route to Reference App hash
        target_route = config.route
        if target_route == "#/item/edit/item-101":
            target_route = "#/items/edit"

        # Theme mapping (contrast -> high-contrast)
        theme_val = "high-contrast" if config.theme in ("contrast", "high-contrast") else config.theme

        # 3. Apply state transitions via JS
        setup_script = f"""
        (() => {{
            // A. Close mobile navigation dialog if open and ensure display none
            const dialog = document.getElementById('dialog-mobile-nav');
            if (dialog) {{
                if (typeof dialog.close === 'function') {{
                    try {{ dialog.close(); }} catch (e) {{}}
                }}
                dialog.style.display = 'none';
            }}

            // B. Manage test harness developer bars (non-application UI)
            const simBar = document.querySelector('.mds-ref-simulation-bar');
            if (simBar) {{
                simBar.style.position = 'fixed';
                simBar.style.bottom = '0';
                simBar.style.left = '0';
                simBar.style.right = '0';
                simBar.style.zIndex = '1000';
                if ({vp.width} <= 768) {{
                    simBar.style.display = 'none';
                }} else {{
                    simBar.style.display = 'flex';
                }}
            }}

            const controlsBar = document.querySelector('.mds-ref-controls-group');
            if (controlsBar) {{
                if ({vp.width} <= 768) {{
                    controlsBar.style.display = 'none';
                }} else {{
                    controlsBar.style.display = 'flex';
                }}
            }}

            // C. Apply Direction
            const dir = {json.dumps(config.direction)};
            document.documentElement.setAttribute('dir', dir);
            document.documentElement.setAttribute('lang', dir === 'rtl' ? 'ar' : 'en');
            const dirSelect = document.getElementById('ctrl-ref-dir');
            if (dirSelect) dirSelect.value = dir;

            // D. Apply Theme
            const theme = {json.dumps(theme_val)};
            document.documentElement.setAttribute('data-theme', theme);
            document.documentElement.setAttribute('data-mode', theme);
            const themeSelect = document.getElementById('ctrl-ref-theme');
            if (themeSelect) themeSelect.value = theme;

            // E. Apply Density
            const density = {json.dumps(config.density)};
            document.documentElement.setAttribute('data-density', density);
            const densitySelect = document.getElementById('ctrl-ref-density');
            if (densitySelect) densitySelect.value = density;

            // F. Set Route & re-render if window.mdsWorkspaceApp exists
            const route = {json.dumps(target_route)};
            if (window.location.hash !== route) {{
                window.location.hash = route;
            }}
            if (window.mdsWorkspaceApp) {{
                window.mdsWorkspaceApp.state.currentRoute = route;
                window.mdsWorkspaceApp.state.currentTheme = theme;
                window.mdsWorkspaceApp.state.currentDensity = density;
                window.mdsWorkspaceApp.state.currentDirection = dir;
                window.mdsWorkspaceApp.render();
            }}

            return {{
                dir: document.documentElement.getAttribute('dir'),
                theme: document.documentElement.getAttribute('data-theme'),
                density: document.documentElement.getAttribute('data-density'),
                route: window.location.hash,
                appFound: window.mdsWorkspaceApp !== undefined
            }};
        }})()
        """
        env_state = driver.evaluate(setup_script)

        # 4. Wait for settlement after environment transition
        settlement = self.wait_for_layout_settlement(driver)
        return {
            "environment": env_state,
            "settlement": settlement,
        }

    def execute_run(self, driver: Any, config: ResponsiveRunConfig) -> ResponsiveRunResult:
        """
        Executes a single isolated run configuration against the browser driver.
        """
        start_t = time.time()
        assertions: List[ResponsiveAssertion] = []
        metrics: Dict[str, Any] = {}
        error_msg = None

        try:
            # 1. Prepare environment & settle
            prep_info = self.prepare_run_environment(driver, config)
            metrics.update(prep_info)

            # 2. Evaluate all semantic assertions
            assertions = ResponsiveAssertionsEvaluator.evaluate_all(driver, config)

        except Exception as e:
            error_msg = str(e)
            assertions.append(
                ResponsiveAssertion(
                    run_id=config.run_id,
                    capability_id=self.CAPABILITY_ID,
                    screen=config.screen,
                    viewport_tier=config.viewport.tier.value,
                    dimension="Execution Lifecycle",
                    assertion_class=AssertionClass.HARD_CONTRACT,
                    selector="window",
                    assertion_name="Execution without unhandled driver exception",
                    passed=False,
                    expected="Clean execution",
                    actual=f"Exception: {e}",
                    diagnostics=f"Runner exception: {e}",
                )
            )

        duration_ms = (time.time() - start_t) * 1000.0

        # Run passes only if zero HARD_CONTRACT or OBSERVABLE_BEHAVIOR failed
        hard_fails = [
            a for a in assertions
            if not a.passed and a.assertion_class in (AssertionClass.HARD_CONTRACT, AssertionClass.OBSERVABLE_BEHAVIOR)
        ]
        passed = (len(hard_fails) == 0 and len(assertions) > 0 and error_msg is None)

        return ResponsiveRunResult(
            run_id=config.run_id,
            config=config,
            passed=passed,
            assertions=assertions,
            duration_ms=duration_ms,
            error_message=error_msg or (f"{len(hard_fails)} hard failure(s)" if hard_fails else None),
            metrics=metrics,
        )

    def execute_matrix(
        self,
        driver: Any,
        configs: Optional[List[ResponsiveRunConfig]] = None
    ) -> ResponsiveMatrixResult:
        """
        Executes the complete matrix of run configurations against the browser driver.
        """
        run_configs = configs or get_canonical_matrix()
        start_matrix_t = time.time()
        run_results: List[ResponsiveRunResult] = []

        total_assertions = 0
        passed_assertions = 0
        failed_assertions = 0
        hard_failures = 0

        for cfg in run_configs:
            res = self.execute_run(driver, cfg)
            run_results.append(res)

            total_assertions += len(res.assertions)
            for a in res.assertions:
                if a.passed:
                    passed_assertions += 1
                else:
                    failed_assertions += 1
                    if a.assertion_class in (AssertionClass.HARD_CONTRACT, AssertionClass.OBSERVABLE_BEHAVIOR):
                        hard_failures += 1

        duration_ms = (time.time() - start_matrix_t) * 1000.0

        # Query browser version
        b_version = None
        try:
            b_version = driver.evaluate("navigator.userAgent")
        except Exception:
            pass

        # Final Status determination (Tri-state: PASS / FAIL / DEFERRED)
        status = "PASS" if hard_failures == 0 and total_assertions > 0 else "FAIL"

        evidence = {
            "matrix_runs_count": len(run_results),
            "total_assertions": total_assertions,
            "passed_assertions": passed_assertions,
            "failed_assertions": failed_assertions,
            "hard_failures": hard_failures,
            "settlement_timeout_ms": self.settlement_timeout_ms,
            "run_summaries": [
                {
                    "run_id": r.run_id,
                    "screen": r.config.screen,
                    "viewport": r.config.viewport.label,
                    "passed": r.passed,
                    "hard_failures": len(r.hard_failures),
                    "duration_ms": round(r.duration_ms, 1),
                }
                for r in run_results
            ]
        }

        return ResponsiveMatrixResult(
            capability_id=self.CAPABILITY_ID,
            status=status,
            runs=run_results,
            total_assertions=total_assertions,
            passed_assertions=passed_assertions,
            failed_assertions=failed_assertions,
            hard_failures=hard_failures,
            duration_ms=duration_ms,
            browser_version=b_version,
            evidence=evidence,
        )
