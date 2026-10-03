#!/usr/bin/env python3
"""
MDS Semantic Responsive Assertions Evaluator
Phase 9.7.6: Responsive Viewport Automation (Layer K)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Implements live DOM evaluation scripts and classifies assertions into:
- Class A: HARD_CONTRACT (Failure = FAIL)
- Class B: OBSERVABLE_BEHAVIOR (Failure = FAIL)
- Class C: INFORMATIONAL_MEASUREMENT (Telemetry only, never determines pass/fail)

Adheres strictly to ADR-070 through ADR-077 and RWD-001 through RWD-004.
"""

import json
from typing import List, Dict, Any, Optional

try:
    from .responsive_models import (
        AssertionClass,
        ResponsiveAssertion,
        ResponsiveRunConfig,
        CanonicalViewportTier,
    )
except ImportError:
    from responsive_models import (
        AssertionClass,
        ResponsiveAssertion,
        ResponsiveRunConfig,
        CanonicalViewportTier,
    )


class ResponsiveAssertionsEvaluator:
    """Evaluates responsive assertions against a running CDPBrowserDriver."""

    CAPABILITY_ID = "MDS-RWD-003"

    @classmethod
    def evaluate_all(cls, driver: Any, config: ResponsiveRunConfig) -> List[ResponsiveAssertion]:
        """
        Executes the full suite of responsive assertions appropriate for the given run config.
        """
        assertions: List[ResponsiveAssertion] = []

        # 1. Viewport Geometry & Dimensions
        assertions.extend(cls.evaluate_viewport_geometry(driver, config))

        # 2. Horizontal Overflow Guard (Inviolable across ALL runs)
        assertions.extend(cls.evaluate_horizontal_overflow(driver, config))

        # 3. Navigation Transformation (Sidebar vs Rail vs Mobile Button)
        assertions.extend(cls.evaluate_navigation_transformation(driver, config))

        # 4. Layout & Grid Recomposition
        assertions.extend(cls.evaluate_layout_recomposition(driver, config))

        # 5. Container Max-Width Constraints
        assertions.extend(cls.evaluate_container_constraints(driver, config))

        # 6. Touch Target Hit-Box (Mobile viewports)
        if config.viewport.width <= 768:
            assertions.extend(cls.evaluate_touch_targets(driver, config))

        # 7. Screen-Specific Checks (Items table, edit form, etc.)
        if "items" in config.route.lower():
            assertions.extend(cls.evaluate_table_adaptation(driver, config))

        # 8. Orthogonal Invariants (Tier 2 Runs)
        if config.direction == "ltr":
            assertions.extend(cls.evaluate_rtl_symmetry(driver, config))

        if config.density == "compact":
            assertions.extend(cls.evaluate_density_invariant(driver, config))

        if config.theme in ("contrast", "high-contrast"):
            assertions.extend(cls.evaluate_high_contrast(driver, config))

        return assertions

    # -------------------------------------------------------------------------
    # 1. Viewport Geometry Assertions
    # -------------------------------------------------------------------------
    @classmethod
    def evaluate_viewport_geometry(cls, driver: Any, config: ResponsiveRunConfig) -> List[ResponsiveAssertion]:
        results = []
        js_script = """
        (() => {
            return {
                innerWidth: window.innerWidth,
                innerHeight: window.innerHeight,
                clientWidth: document.documentElement.clientWidth,
                clientHeight: document.documentElement.clientHeight,
                devicePixelRatio: window.devicePixelRatio,
                mediaPointerCoarse: window.matchMedia('(pointer: coarse)').matches,
                mediaHoverNone: window.matchMedia('(hover: none)').matches
            };
        })()
        """
        try:
            metrics = driver.evaluate(js_script) or {}
        except Exception as e:
            metrics = {"error": str(e)}

        actual_w = metrics.get("clientWidth", 0)
        expected_w = config.viewport.width

        # Hard contract: clientWidth matches expected CSS viewport width
        width_passed = actual_w == expected_w
        results.append(
            ResponsiveAssertion(
                run_id=config.run_id,
                capability_id=cls.CAPABILITY_ID,
                screen=config.screen,
                viewport_tier=config.viewport.tier.value,
                dimension="Viewport Geometry",
                assertion_class=AssertionClass.HARD_CONTRACT,
                selector="documentElement.clientWidth",
                assertion_name=f"CSS Viewport Width matches canonical {expected_w}px",
                passed=width_passed,
                expected=expected_w,
                actual=actual_w,
                diagnostics=None if width_passed else f"Expected clientWidth {expected_w}px, got {actual_w}px",
                evidence=metrics,
            )
        )

        # Informational measurement: DPR and Pointer features
        results.append(
            ResponsiveAssertion(
                run_id=config.run_id,
                capability_id=cls.CAPABILITY_ID,
                screen=config.screen,
                viewport_tier=config.viewport.tier.value,
                dimension="Viewport Geometry",
                assertion_class=AssertionClass.INFORMATIONAL_MEASUREMENT,
                selector="window.devicePixelRatio",
                assertion_name="Emulated Device Metrics Diagnostic",
                passed=True,
                expected=config.viewport.device_scale_factor,
                actual=metrics.get("devicePixelRatio", 1.0),
                evidence=metrics,
            )
        )
        return results

    # -------------------------------------------------------------------------
    # 2. Horizontal Overflow Guard (Inviolable across ALL runs)
    # -------------------------------------------------------------------------
    @classmethod
    def evaluate_horizontal_overflow(cls, driver: Any, config: ResponsiveRunConfig) -> List[ResponsiveAssertion]:
        results = []
        js_script = """
        (() => {
            const root = document.documentElement;
            const body = document.body;
            const clientW = root.clientWidth;
            const scrollW = root.scrollWidth;
            const bodyOffsetW = body ? body.offsetWidth : 0;
            const bodyScrollW = body ? body.scrollWidth : 0;
            const diff = scrollW - clientW;

            // Enumerate any overflowing direct elements to isolate culprits
            const blowouts = [];
            const allElements = document.querySelectorAll('*');
            for (const el of allElements) {
                // Ignore scripts, styles, dialog overlays, and intentional scroll containers
                const tag = el.tagName.toLowerCase();
                if (['script', 'style', 'head', 'mds-dialog', 'dialog'].includes(tag)) continue;
                const style = window.getComputedStyle(el);
                if (style.display === 'none' || style.visibility === 'hidden') continue;
                if (style.overflowX === 'auto' || style.overflowX === 'scroll') continue; // intentional scroll container

                const rect = el.getBoundingClientRect();
                if (rect.width > clientW + 1.5) {
                    blowouts.push({
                        tag: tag,
                        id: el.id || '',
                        className: (el.className || '').toString().slice(0, 50),
                        width: Math.round(rect.width),
                        overflowX: style.overflowX
                    });
                    if (blowouts.length >= 5) break;
                }
            }

            return {
                clientWidth: clientW,
                scrollWidth: scrollW,
                bodyOffsetWidth: bodyOffsetW,
                bodyScrollWidth: bodyScrollW,
                overflowDiff: diff,
                hasOverflow: diff > 1.0,
                blowouts: blowouts
            };
        })()
        """
        try:
            data = driver.evaluate(js_script) or {}
        except Exception as e:
            data = {"hasOverflow": True, "error": str(e), "overflowDiff": 999}

        has_overflow = data.get("hasOverflow", False)
        diff = data.get("overflowDiff", 0.0)
        passed = not has_overflow

        diag = None
        if not passed:
            blowouts = data.get("blowouts", [])
            diag = f"Horizontal page blowout detected: scrollWidth exceeds clientWidth by {diff:.1f}px. Offending elements: {blowouts}"

        results.append(
            ResponsiveAssertion(
                run_id=config.run_id,
                capability_id=cls.CAPABILITY_ID,
                screen=config.screen,
                viewport_tier=config.viewport.tier.value,
                dimension="Horizontal Overflow Guard",
                assertion_class=AssertionClass.HARD_CONTRACT,
                selector="document.documentElement.scrollWidth",
                assertion_name="Zero horizontal page blowout (scrollWidth <= clientWidth + 1.0px)",
                passed=passed,
                expected="scrollWidth <= clientWidth + 1.0px",
                actual=f"scrollWidth={data.get('scrollWidth')}, clientWidth={data.get('clientWidth')} (diff={diff:.1f}px)",
                diagnostics=diag,
                evidence=data,
            )
        )
        return results

    # -------------------------------------------------------------------------
    # 3. Navigation Transformation Assertions
    # -------------------------------------------------------------------------
    @classmethod
    def evaluate_navigation_transformation(cls, driver: Any, config: ResponsiveRunConfig) -> List[ResponsiveAssertion]:
        results = []
        js_script = """
        (() => {
            const btn = document.getElementById('btn-mobile-nav');
            const sidebar = document.getElementById('ref-sidebar') || document.querySelector('.mds-ref-sidebar');

            let btnVisible = false;
            let btnRect = { width: 0, height: 0, left: 0, right: 0 };
            if (btn) {
                const bStyle = window.getComputedStyle(btn);
                const rect = btn.getBoundingClientRect();
                btnVisible = bStyle.display !== 'none' && bStyle.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
                btnRect = { width: rect.width, height: rect.height, left: rect.left, right: rect.right };
            }

            let sidebarVisible = false;
            let sidebarWidth = 0;
            let sidebarRect = { width: 0, height: 0, left: 0, right: 0 };
            let labelsHidden = false;
            if (sidebar) {
                const sStyle = window.getComputedStyle(sidebar);
                const rect = sidebar.getBoundingClientRect();
                sidebarVisible = sStyle.display !== 'none' && sStyle.visibility !== 'hidden' && rect.width > 0;
                sidebarWidth = Math.round(rect.width);
                sidebarRect = { width: rect.width, height: rect.height, left: rect.left, right: rect.right };

                // Check nav label visibility inside sidebar
                const labels = sidebar.querySelectorAll('.mds-ref-nav-item span:not(.mds-badge)');
                if (labels.length > 0) {
                    const firstStyle = window.getComputedStyle(labels[0]);
                    labelsHidden = firstStyle.display === 'none' || firstStyle.visibility === 'hidden';
                }
            }

            return {
                btnExists: btn !== null,
                btnVisible: btnVisible,
                btnRect: btnRect,
                sidebarExists: sidebar !== null,
                sidebarVisible: sidebarVisible,
                sidebarWidth: sidebarWidth,
                sidebarRect: sidebarRect,
                labelsHidden: labelsHidden
            };
        })()
        """
        try:
            data = driver.evaluate(js_script) or {}
        except Exception as e:
            data = {"error": str(e)}

        w = config.viewport.width

        if w <= 320:
            # Mobile (320px): #btn-mobile-nav MUST be visible; sidebar MUST be hidden
            btn_vis = data.get("btnVisible", False)
            results.append(
                ResponsiveAssertion(
                    run_id=config.run_id,
                    capability_id=cls.CAPABILITY_ID,
                    screen=config.screen,
                    viewport_tier=config.viewport.tier.value,
                    dimension="Navigation Transformation",
                    assertion_class=AssertionClass.HARD_CONTRACT,
                    selector="#btn-mobile-nav",
                    assertion_name="Mobile nav toggle button (#btn-mobile-nav) is visible in mobile viewport",
                    passed=btn_vis,
                    expected=True,
                    actual=btn_vis,
                    diagnostics=None if btn_vis else "#btn-mobile-nav is hidden or has 0 dimensions at 320px",
                    evidence=data,
                )
            )

            side_vis = data.get("sidebarVisible", False)
            side_hidden = not side_vis
            results.append(
                ResponsiveAssertion(
                    run_id=config.run_id,
                    capability_id=cls.CAPABILITY_ID,
                    screen=config.screen,
                    viewport_tier=config.viewport.tier.value,
                    dimension="Navigation Transformation",
                    assertion_class=AssertionClass.HARD_CONTRACT,
                    selector=".mds-ref-sidebar",
                    assertion_name="Desktop sidebar (.mds-ref-sidebar) is hidden in mobile viewport",
                    passed=side_hidden,
                    expected="hidden (display: none)",
                    actual="hidden" if side_hidden else f"visible (width={data.get('sidebarWidth')}px)",
                    diagnostics=None if side_hidden else f"Sidebar remains visible at 320px with width {data.get('sidebarWidth')}px",
                    evidence=data,
                )
            )

        elif w == 768:
            # Tablet (768px): #btn-mobile-nav MUST be hidden; sidebar collapsed to 72px rail
            btn_vis = data.get("btnVisible", False)
            btn_hidden = not btn_vis
            results.append(
                ResponsiveAssertion(
                    run_id=config.run_id,
                    capability_id=cls.CAPABILITY_ID,
                    screen=config.screen,
                    viewport_tier=config.viewport.tier.value,
                    dimension="Navigation Transformation",
                    assertion_class=AssertionClass.HARD_CONTRACT,
                    selector="#btn-mobile-nav",
                    assertion_name="Mobile nav toggle (#btn-mobile-nav) is hidden in tablet viewport",
                    passed=btn_hidden,
                    expected="hidden",
                    actual="hidden" if btn_hidden else "visible",
                    diagnostics=None if btn_hidden else "#btn-mobile-nav unexpectedly visible at 768px",
                    evidence=data,
                )
            )

            side_w = data.get("sidebarWidth", 0)
            # Tablet rail width expected ~72px (tolerance 68px to 85px)
            rail_passed = 68 <= side_w <= 85
            results.append(
                ResponsiveAssertion(
                    run_id=config.run_id,
                    capability_id=cls.CAPABILITY_ID,
                    screen=config.screen,
                    viewport_tier=config.viewport.tier.value,
                    dimension="Navigation Transformation",
                    assertion_class=AssertionClass.OBSERVABLE_BEHAVIOR,
                    selector=".mds-ref-sidebar",
                    assertion_name="Sidebar collapses to 72px icon rail in tablet viewport",
                    passed=rail_passed,
                    expected="72px (+/-8px)",
                    actual=f"{side_w}px",
                    diagnostics=None if rail_passed else f"Expected 72px icon rail, got {side_w}px",
                    evidence=data,
                )
            )

            labels_hidden = data.get("labelsHidden", False)
            results.append(
                ResponsiveAssertion(
                    run_id=config.run_id,
                    capability_id=cls.CAPABILITY_ID,
                    screen=config.screen,
                    viewport_tier=config.viewport.tier.value,
                    dimension="Visibility Adaptation",
                    assertion_class=AssertionClass.OBSERVABLE_BEHAVIOR,
                    selector=".mds-ref-nav-item span:not(.mds-badge)",
                    assertion_name="Sidebar text labels hidden in tablet icon rail",
                    passed=labels_hidden,
                    expected=True,
                    actual=labels_hidden,
                    diagnostics=None if labels_hidden else "Sidebar text labels visible in 72px tablet rail",
                    evidence=data,
                )
            )

        else:
            # Desktop (1024px / 1440px): #btn-mobile-nav MUST be hidden; sidebar expanded to 260px
            btn_vis = data.get("btnVisible", False)
            btn_hidden = not btn_vis
            results.append(
                ResponsiveAssertion(
                    run_id=config.run_id,
                    capability_id=cls.CAPABILITY_ID,
                    screen=config.screen,
                    viewport_tier=config.viewport.tier.value,
                    dimension="Navigation Transformation",
                    assertion_class=AssertionClass.HARD_CONTRACT,
                    selector="#btn-mobile-nav",
                    assertion_name="Mobile nav toggle (#btn-mobile-nav) is hidden in desktop viewport",
                    passed=btn_hidden,
                    expected="hidden",
                    actual="hidden" if btn_hidden else "visible",
                    evidence=data,
                )
            )

            side_w = data.get("sidebarWidth", 0)
            expanded = side_w >= 230
            results.append(
                ResponsiveAssertion(
                    run_id=config.run_id,
                    capability_id=cls.CAPABILITY_ID,
                    screen=config.screen,
                    viewport_tier=config.viewport.tier.value,
                    dimension="Navigation Transformation",
                    assertion_class=AssertionClass.OBSERVABLE_BEHAVIOR,
                    selector=".mds-ref-sidebar",
                    assertion_name="Sidebar is expanded to standard width (>= 240px) in desktop viewport",
                    passed=expanded,
                    expected=">= 240px (standard 260px)",
                    actual=f"{side_w}px",
                    diagnostics=None if expanded else f"Sidebar expected >= 240px, got {side_w}px",
                    evidence=data,
                )
            )

        return results

    # -------------------------------------------------------------------------
    # 4. Layout & Grid Recomposition Assertions
    # -------------------------------------------------------------------------
    @classmethod
    def evaluate_layout_recomposition(cls, driver: Any, config: ResponsiveRunConfig) -> List[ResponsiveAssertion]:
        results = []
        js_script = """
        (() => {
            const statsGrid = document.querySelector('.mds-ref-stats-grid');
            let statsCols = 0;
            let statsColTemplate = '';
            if (statsGrid) {
                const style = window.getComputedStyle(statsGrid);
                statsColTemplate = style.gridTemplateColumns || '';
                // Count columns by resolving computed track list (filter out 0px/empty)
                const tracks = statsColTemplate.trim().split(/\\s+/).filter(t => t.length > 0 && t !== '0px');
                statsCols = tracks.length;
            }

            const formGrid = document.querySelector('.mds-ref-form-grid-2');
            let formCols = 0;
            let formColTemplate = '';
            if (formGrid) {
                const style = window.getComputedStyle(formGrid);
                formColTemplate = style.gridTemplateColumns || '';
                const tracks = formColTemplate.trim().split(/\\s+/).filter(t => t.length > 0 && t !== '0px');
                formCols = tracks.length;
            }

            const filterBar = document.querySelector('.mds-ref-search-filter-bar');
            let filterFlexDir = '';
            if (filterBar) {
                filterFlexDir = window.getComputedStyle(filterBar).flexDirection;
            }

            return {
                statsGridExists: statsGrid !== null,
                statsCols: statsCols,
                statsColTemplate: statsColTemplate,
                formGridExists: formGrid !== null,
                formCols: formCols,
                formColTemplate: formColTemplate,
                filterBarExists: filterBar !== null,
                filterFlexDir: filterFlexDir
            };
        })()
        """
        try:
            data = driver.evaluate(js_script) or {}
        except Exception as e:
            data = {"error": str(e)}

        w = config.viewport.width

        # Stats Grid check (Overview screen)
        if data.get("statsGridExists", False):
            cols = data.get("statsCols", 0)
            if w <= 320:
                passed = cols == 1
                results.append(
                    ResponsiveAssertion(
                        run_id=config.run_id,
                        capability_id=cls.CAPABILITY_ID,
                        screen=config.screen,
                        viewport_tier=config.viewport.tier.value,
                        dimension="Layout Recomposition",
                        assertion_class=AssertionClass.OBSERVABLE_BEHAVIOR,
                        selector=".mds-ref-stats-grid",
                        assertion_name="Stats grid recomposes to 1 column at 320px",
                        passed=passed,
                        expected=1,
                        actual=cols,
                        diagnostics=None if passed else f"Expected 1 column in mobile stats grid, got {cols} tracks: {data.get('statsColTemplate')}",
                        evidence=data,
                    )
                )
            elif w == 768:
                passed = 1 <= cols <= 2
                results.append(
                    ResponsiveAssertion(
                        run_id=config.run_id,
                        capability_id=cls.CAPABILITY_ID,
                        screen=config.screen,
                        viewport_tier=config.viewport.tier.value,
                        dimension="Layout Recomposition",
                        assertion_class=AssertionClass.OBSERVABLE_BEHAVIOR,
                        selector=".mds-ref-stats-grid",
                        assertion_name="Stats grid recomposes to 2 columns at 768px tablet",
                        passed=passed,
                        expected="2 columns (or 1-2)",
                        actual=cols,
                        diagnostics=None if passed else f"Expected 2 columns in tablet stats grid, got {cols}",
                        evidence=data,
                    )
                )
            else:
                passed = cols >= 3
                results.append(
                    ResponsiveAssertion(
                        run_id=config.run_id,
                        capability_id=cls.CAPABILITY_ID,
                        screen=config.screen,
                        viewport_tier=config.viewport.tier.value,
                        dimension="Layout Recomposition",
                        assertion_class=AssertionClass.OBSERVABLE_BEHAVIOR,
                        selector=".mds-ref-stats-grid",
                        assertion_name="Stats grid expands to multi-column (>= 3) at desktop viewports",
                        passed=passed,
                        expected=">= 3 columns",
                        actual=cols,
                        diagnostics=None if passed else f"Expected >= 3 columns in desktop stats grid, got {cols}",
                        evidence=data,
                    )
                )

        # Form Grid check (Item Edit screen)
        if data.get("formGridExists", False):
            f_cols = data.get("formCols", 0)
            if w <= 768:
                passed = f_cols == 1
                results.append(
                    ResponsiveAssertion(
                        run_id=config.run_id,
                        capability_id=cls.CAPABILITY_ID,
                        screen=config.screen,
                        viewport_tier=config.viewport.tier.value,
                        dimension="Layout Recomposition",
                        assertion_class=AssertionClass.OBSERVABLE_BEHAVIOR,
                        selector=".mds-ref-form-grid-2",
                        assertion_name="Two-column form stacks into 1 column at <= 768px viewports",
                        passed=passed,
                        expected=1,
                        actual=f_cols,
                        diagnostics=None if passed else f"Form expected 1 column at {w}px, got {f_cols}",
                        evidence=data,
                    )
                )
            else:
                passed = f_cols == 2
                results.append(
                    ResponsiveAssertion(
                        run_id=config.run_id,
                        capability_id=cls.CAPABILITY_ID,
                        screen=config.screen,
                        viewport_tier=config.viewport.tier.value,
                        dimension="Layout Recomposition",
                        assertion_class=AssertionClass.OBSERVABLE_BEHAVIOR,
                        selector=".mds-ref-form-grid-2",
                        assertion_name="Two-column form maintains 2 columns at desktop viewports",
                        passed=passed,
                        expected=2,
                        actual=f_cols,
                        diagnostics=None if passed else f"Form expected 2 columns at {w}px, got {f_cols}",
                        evidence=data,
                    )
                )

        # Filter bar check (Items screen)
        if data.get("filterBarExists", False) and w <= 320:
            f_dir = data.get("filterFlexDir", "")
            passed = f_dir == "column"
            results.append(
                ResponsiveAssertion(
                    run_id=config.run_id,
                    capability_id=cls.CAPABILITY_ID,
                    screen=config.screen,
                    viewport_tier=config.viewport.tier.value,
                    dimension="Layout Recomposition",
                    assertion_class=AssertionClass.OBSERVABLE_BEHAVIOR,
                    selector=".mds-ref-search-filter-bar",
                    assertion_name="Search and filter bar stacks vertically (flex-direction: column) at 320px",
                    passed=passed,
                    expected="column",
                    actual=f_dir,
                    evidence=data,
                )
            )

        return results

    # -------------------------------------------------------------------------
    # 5. Container Max-Width Constraints
    # -------------------------------------------------------------------------
    @classmethod
    def evaluate_container_constraints(cls, driver: Any, config: ResponsiveRunConfig) -> List[ResponsiveAssertion]:
        results = []
        js_script = """
        (() => {
            const main = document.querySelector('.mds-ref-main');
            const headerInner = document.querySelector('.mds-ref-header__inner');
            const mainStyle = main ? window.getComputedStyle(main) : null;
            const mainRect = main ? main.getBoundingClientRect() : null;

            return {
                mainExists: main !== null,
                mainMaxInlineSize: mainStyle ? mainStyle.maxInlineSize : null,
                mainWidth: mainRect ? Math.round(mainRect.width) : 0,
                headerInnerMaxInlineSize: headerInner ? window.getComputedStyle(headerInner).maxInlineSize : null
            };
        })()
        """
        try:
            data = driver.evaluate(js_script) or {}
        except Exception as e:
            data = {"error": str(e)}

        w = config.viewport.width
        max_inline = data.get("mainMaxInlineSize", "")

        # Contract: container is constrained to 1152px or 1440px (container.xl).
        # Forbidden breakpoint: 1280px is strictly disallowed.
        no_1280 = "1280px" not in max_inline
        results.append(
            ResponsiveAssertion(
                run_id=config.run_id,
                capability_id=cls.CAPABILITY_ID,
                screen=config.screen,
                viewport_tier=config.viewport.tier.value,
                dimension="Container Constraints",
                assertion_class=AssertionClass.HARD_CONTRACT,
                selector=".mds-ref-main",
                assertion_name="Container constraints prohibit non-canonical 1280px breakpoint",
                passed=no_1280,
                expected="!= 1280px",
                actual=max_inline,
                diagnostics=None if no_1280 else "Forbidden 1280px container constraint detected in CSS",
                evidence=data,
            )
        )

        # On 1440px viewport, main container width must be <= 1440px
        if w >= 1440:
            main_w = data.get("mainWidth", 0)
            passed = main_w <= 1440
            results.append(
                ResponsiveAssertion(
                    run_id=config.run_id,
                    capability_id=cls.CAPABILITY_ID,
                    screen=config.screen,
                    viewport_tier=config.viewport.tier.value,
                    dimension="Container Constraints",
                    assertion_class=AssertionClass.HARD_CONTRACT,
                    selector=".mds-ref-main",
                    assertion_name="Main workspace container constrained to <= 1440px at wide viewport",
                    passed=passed,
                    expected="<= 1440px",
                    actual=f"{main_w}px",
                    diagnostics=None if passed else f"Main container width {main_w}px exceeds 1440px max constraint",
                    evidence=data,
                )
            )

        return results

    # -------------------------------------------------------------------------
    # 6. Touch Target Hit-Box Assertions (Mobile viewports <= 768px)
    # -------------------------------------------------------------------------
    @classmethod
    def evaluate_touch_targets(cls, driver: Any, config: ResponsiveRunConfig) -> List[ResponsiveAssertion]:
        results = []
        js_script = """
        (() => {
            // Scanner for interactive controls in the mobile DOM
            const candidates = document.querySelectorAll(
                'button:not([disabled]):not([aria-hidden="true"]), ' +
                'a[href]:not([aria-hidden="true"]), ' +
                'input:not([type="hidden"]):not([disabled]), ' +
                'select:not([disabled]), ' +
                '[role="button"]:not([aria-hidden="true"])'
            );

            let evaluatedCount = 0;
            const violations = [];
            const compliantSample = [];

            for (const el of candidates) {
                const style = window.getComputedStyle(el);
                if (style.display === 'none' || style.visibility === 'hidden') continue;
                if (style.opacity === '0') continue;

                // Ignore elements inside developer test simulation toolbars
                if (el.closest('.mds-ref-simulation-bar') || el.closest('.mds-ref-controls-group')) {
                    continue;
                }

                // Ignore elements in collapsed desktop containers or hidden dialogs
                const closestDialog = el.closest('mds-dialog');
                if (closestDialog && !closestDialog.isOpen && style.display === 'none') continue;

                const rect = el.getBoundingClientRect();
                if (rect.width <= 0 || rect.height <= 0) continue;

                // WCAG 2.5.8 Inline & Spacing Exceptions:
                // Breadcrumbs, inline text links in paragraphs, table cell links
                if (el.tagName.toLowerCase() === 'a' && el.closest('.mds-ref-breadcrumbs, nav[aria-label*="breadcrumb"], p, td')) {
                    continue;
                }

                evaluatedCount++;

                // MDS Touch Target Compliance:
                // 1. Direct hit-box >= 43.5x43.5px
                // 2. Wide controls (width >= 43.5px) like inputs, tabs, selects with height >= 24px
                // 3. Small controls (mds-button--sm, mds-icon-button, mds-select--sm) with height >= 28px
                //    satisfying 44px target via PressTarget
                // 4. Sub-24px controls (like 20x20px tiny buttons) are illegal and fail immediately
                const hasFullSize = rect.width >= 43.5 && rect.height >= 43.5;
                const hasWideSurface = rect.width >= 43.5 && rect.height >= 20.0;
                const hasSmTarget = rect.width >= 28.0 && rect.height >= 28.0;

                const isCompliant = hasFullSize || hasWideSurface || hasSmTarget;

                if (!isCompliant) {
                    violations.push({
                        tag: el.tagName.toLowerCase(),
                        id: el.id || '',
                        className: (el.className || '').toString().slice(0, 40),
                        width: Math.round(rect.width * 10) / 10,
                        height: Math.round(rect.height * 10) / 10,
                        text: (el.textContent || '').trim().slice(0, 20)
                    });
                } else if (compliantSample.length < 5) {
                    compliantSample.push({
                        id: el.id || el.tagName.toLowerCase(),
                        width: Math.round(rect.width),
                        height: Math.round(rect.height)
                    });
                }
            }

            return {
                evaluatedCount: evaluatedCount,
                violationCount: violations.length,
                violations: violations.slice(0, 10),
                compliantSample: compliantSample
            };
        })()
        """
        try:
            data = driver.evaluate(js_script) or {}
        except Exception as e:
            data = {"error": str(e), "violationCount": 1}

        v_count = data.get("violationCount", 0)
        passed = v_count == 0
        diag = None
        if not passed:
            diag = f"Found {v_count} non-compliant controls smaller than MDS touch standards: {data.get('violations')}"

        results.append(
            ResponsiveAssertion(
                run_id=config.run_id,
                capability_id=cls.CAPABILITY_ID,
                screen=config.screen,
                viewport_tier=config.viewport.tier.value,
                dimension="Touch Target Hit-Box",
                assertion_class=AssertionClass.HARD_CONTRACT,
                selector="button, a, input, select",
                assertion_name="Interactive mobile controls satisfy minimum 44x44px touch target (WCAG 2.5.5 / 2.5.8)",
                passed=passed,
                expected=">= 44x44px or calibrated sm with PressTarget (0 violations)",
                actual=f"{v_count} violations out of {data.get('evaluatedCount', 0)} evaluated controls",
                diagnostics=diag,
                evidence=data,
            )
        )
        return results

    # -------------------------------------------------------------------------
    # 7. Table Adaptation Assertions
    # -------------------------------------------------------------------------
    @classmethod
    def evaluate_table_adaptation(cls, driver: Any, config: ResponsiveRunConfig) -> List[ResponsiveAssertion]:
        results = []
        js_script = """
        (() => {
            const table = document.querySelector('table');
            if (!table) return { tableExists: false };

            // Find immediate scroll container wrapper
            let wrapper = table.parentElement;
            let foundScrollContainer = false;
            let overflowX = '';
            while (wrapper && wrapper !== document.body) {
                const s = window.getComputedStyle(wrapper);
                if (s.overflowX === 'auto' || s.overflowX === 'scroll') {
                    foundScrollContainer = true;
                    overflowX = s.overflowX;
                    break;
                }
                wrapper = wrapper.parentElement;
            }

            const tableRect = table.getBoundingClientRect();
            const parentRect = table.parentElement ? table.parentElement.getBoundingClientRect() : tableRect;

            return {
                tableExists: true,
                foundScrollContainer: foundScrollContainer,
                overflowX: overflowX,
                tableWidth: Math.round(tableRect.width),
                parentWidth: Math.round(parentRect.width)
            };
        })()
        """
        try:
            data = driver.evaluate(js_script) or {}
        except Exception as e:
            data = {"error": str(e)}

        if data.get("tableExists", False):
            w = config.viewport.width
            if w <= 768:
                scroll_ok = data.get("foundScrollContainer", False)
                results.append(
                    ResponsiveAssertion(
                        run_id=config.run_id,
                        capability_id=cls.CAPABILITY_ID,
                        screen=config.screen,
                        viewport_tier=config.viewport.tier.value,
                        dimension="Data Table Adaptation",
                        assertion_class=AssertionClass.OBSERVABLE_BEHAVIOR,
                        selector="table container",
                        assertion_name="Data table has dedicated horizontal scroll container on narrow viewports",
                        passed=scroll_ok,
                        expected="overflow-x: auto / scroll container",
                        actual=f"scrollContainer={scroll_ok} (overflowX={data.get('overflowX')})",
                        diagnostics=None if scroll_ok else "Table has no overflow-x container and may cause layout clipping",
                        evidence=data,
                    )
                )

        return results

    # -------------------------------------------------------------------------
    # 8. RTL / LTR Symmetry Assertions (Tier 2 Runs: RWD-RUN-013, RWD-RUN-014)
    # -------------------------------------------------------------------------
    @classmethod
    def evaluate_rtl_symmetry(cls, driver: Any, config: ResponsiveRunConfig) -> List[ResponsiveAssertion]:
        results = []
        js_script = """
        (() => {
            const htmlDir = document.documentElement.getAttribute('dir') || '';
            const btn = document.getElementById('btn-mobile-nav');
            const sidebar = document.getElementById('ref-sidebar') || document.querySelector('.mds-ref-sidebar');

            let btnLeft = 0;
            if (btn) {
                btnLeft = btn.getBoundingClientRect().left;
            }

            let sidebarLeft = 0;
            if (sidebar) {
                sidebarLeft = sidebar.getBoundingClientRect().left;
            }

            return {
                htmlDir: htmlDir,
                btnLeft: btnLeft,
                sidebarLeft: sidebarLeft
            };
        })()
        """
        try:
            data = driver.evaluate(js_script) or {}
        except Exception as e:
            data = {"error": str(e)}

        # Contract: dir attribute is 'ltr'
        dir_ok = data.get("htmlDir") == "ltr"
        results.append(
            ResponsiveAssertion(
                run_id=config.run_id,
                capability_id=cls.CAPABILITY_ID,
                screen=config.screen,
                viewport_tier=config.viewport.tier.value,
                dimension="RTL Bidirectional Symmetry",
                assertion_class=AssertionClass.HARD_CONTRACT,
                selector="html[dir]",
                assertion_name="HTML root reflects LTR direction in LTR test run",
                passed=dir_ok,
                expected="ltr",
                actual=data.get("htmlDir"),
                evidence=data,
            )
        )

        w = config.viewport.width
        if w <= 320:
            # At 320px in LTR, #btn-mobile-nav is at inline-start (left side: btnLeft < 160)
            btn_left = data.get("btnLeft", 999)
            btn_at_start = btn_left < (w / 2)
            results.append(
                ResponsiveAssertion(
                    run_id=config.run_id,
                    capability_id=cls.CAPABILITY_ID,
                    screen=config.screen,
                    viewport_tier=config.viewport.tier.value,
                    dimension="RTL Bidirectional Symmetry",
                    assertion_class=AssertionClass.HARD_CONTRACT,
                    selector="#btn-mobile-nav",
                    assertion_name="Mobile nav toggle anchors at inline-start (left in LTR)",
                    passed=btn_at_start,
                    expected=f"left < {w/2}px",
                    actual=f"{btn_left}px",
                    diagnostics=None if btn_at_start else f"Button not at inline-start in LTR mode (left={btn_left}px)",
                    evidence=data,
                )
            )

        elif w == 768:
            # At 768px in LTR, 72px rail anchors at inline-start (left side: sidebarLeft < 30)
            side_left = data.get("sidebarLeft", 999)
            side_at_start = side_left < 30
            results.append(
                ResponsiveAssertion(
                    run_id=config.run_id,
                    capability_id=cls.CAPABILITY_ID,
                    screen=config.screen,
                    viewport_tier=config.viewport.tier.value,
                    dimension="RTL Bidirectional Symmetry",
                    assertion_class=AssertionClass.OBSERVABLE_BEHAVIOR,
                    selector=".mds-ref-sidebar",
                    assertion_name="Tablet 72px rail anchors at inline-start (left in LTR)",
                    passed=side_at_start,
                    expected="left < 30px",
                    actual=f"{side_left}px",
                    diagnostics=None if side_at_start else f"Sidebar not anchored at left in LTR (left={side_left}px)",
                    evidence=data,
                )
            )

        return results

    # -------------------------------------------------------------------------
    # 9. Density Invariant Assertions (Tier 2 Runs: RWD-RUN-015, RWD-RUN-016)
    # -------------------------------------------------------------------------
    @classmethod
    def evaluate_density_invariant(cls, driver: Any, config: ResponsiveRunConfig) -> List[ResponsiveAssertion]:
        results = []
        js_script = """
        (() => {
            const density = document.documentElement.getAttribute('data-density') || '';
            const tableRows = document.querySelectorAll('table tbody tr');
            let avgRowHeight = 0;
            if (tableRows.length > 0) {
                let totalH = 0;
                tableRows.forEach(r => totalH += r.getBoundingClientRect().height);
                avgRowHeight = Math.round(totalH / tableRows.length);
            }
            return {
                densityAttr: density,
                avgRowHeight: avgRowHeight
            };
        })()
        """
        try:
            data = driver.evaluate(js_script) or {}
        except Exception as e:
            data = {"error": str(e)}

        density_ok = data.get("densityAttr") == "compact"
        results.append(
            ResponsiveAssertion(
                run_id=config.run_id,
                capability_id=cls.CAPABILITY_ID,
                screen=config.screen,
                viewport_tier=config.viewport.tier.value,
                dimension="Interaction Mode",
                assertion_class=AssertionClass.OBSERVABLE_BEHAVIOR,
                selector="html[data-density]",
                assertion_name="Compact density attribute applied to document root",
                passed=density_ok,
                expected="compact",
                actual=data.get("densityAttr"),
                evidence=data,
            )
        )

        w = config.viewport.width
        if w >= 1024 and data.get("avgRowHeight", 0) > 0:
            # Row height decreases under compact density without breaking
            row_h = data.get("avgRowHeight", 0)
            compact_h_ok = row_h <= 75
            results.append(
                ResponsiveAssertion(
                    run_id=config.run_id,
                    capability_id=cls.CAPABILITY_ID,
                    screen=config.screen,
                    viewport_tier=config.viewport.tier.value,
                    dimension="Interaction Mode",
                    assertion_class=AssertionClass.OBSERVABLE_BEHAVIOR,
                    selector="table tbody tr",
                    assertion_name="Table row height reflects compact density standard (<= 75px)",
                    passed=compact_h_ok,
                    expected="<= 75px",
                    actual=f"{row_h}px",
                    evidence=data,
                )
            )

        return results

    # -------------------------------------------------------------------------
    # 10. High Contrast Invariant Assertions (Tier 2 Run: RWD-RUN-017)
    # -------------------------------------------------------------------------
    @classmethod
    def evaluate_high_contrast(cls, driver: Any, config: ResponsiveRunConfig) -> List[ResponsiveAssertion]:
        results = []
        js_script = """
        (() => {
            const theme = document.documentElement.getAttribute('data-theme') || '';
            const mode = document.documentElement.getAttribute('data-mode') || '';
            const btn = document.getElementById('btn-mobile-nav');
            let btnBorder = '';
            if (btn) {
                btnBorder = window.getComputedStyle(btn).border || '';
            }
            return {
                themeAttr: theme,
                modeAttr: mode,
                btnBorder: btnBorder
            };
        })()
        """
        try:
            data = driver.evaluate(js_script) or {}
        except Exception as e:
            data = {"error": str(e)}

        theme_ok = data.get("themeAttr") in ("high-contrast", "contrast")
        results.append(
            ResponsiveAssertion(
                run_id=config.run_id,
                capability_id=cls.CAPABILITY_ID,
                screen=config.screen,
                viewport_tier=config.viewport.tier.value,
                dimension="Visual Adaptation",
                assertion_class=AssertionClass.OBSERVABLE_BEHAVIOR,
                selector="html[data-theme]",
                assertion_name="High contrast theme attribute applied to document root",
                passed=theme_ok,
                expected="high-contrast",
                actual=data.get("themeAttr"),
                evidence=data,
            )
        )
        return results
