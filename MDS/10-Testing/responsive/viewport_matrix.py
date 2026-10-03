#!/usr/bin/env python3
"""
MDS Canonical Viewport Matrix & 17-Run Execution Specification
Phase 9.7.6: Responsive Viewport Automation (Layer K)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Defines the 4 Canonical Viewports and the Canonical 17-Run Deterministic
Execution Matrix adhering strictly to ADR-070, ADR-071, ADR-074, and ADR-075.
"""

from typing import Dict, List, Optional
try:
    from .responsive_models import (
        CanonicalViewportTier,
        ViewportDefinition,
        ResponsiveRunConfig,
    )
except ImportError:
    from responsive_models import (
        CanonicalViewportTier,
        ViewportDefinition,
        ResponsiveRunConfig,
    )


# -----------------------------------------------------------------------------
# 1. Canonical Viewport Profiles (03-Spacing-and-Grid.md & ADR-074)
# -----------------------------------------------------------------------------

VP_320 = ViewportDefinition(
    tier=CanonicalViewportTier.MOBILE,
    width=320,
    height=640,
    device_scale_factor=2.0,
    is_mobile=True,
)

VP_768 = ViewportDefinition(
    tier=CanonicalViewportTier.TABLET,
    width=768,
    height=1024,
    device_scale_factor=2.0,
    is_mobile=True,
)

VP_1024 = ViewportDefinition(
    tier=CanonicalViewportTier.DESKTOP,
    width=1024,
    height=768,
    device_scale_factor=1.0,
    is_mobile=False,
)

VP_1440 = ViewportDefinition(
    tier=CanonicalViewportTier.WIDE,
    width=1440,
    height=900,
    device_scale_factor=1.0,
    is_mobile=False,
)

CANONICAL_VIEWPORTS: Dict[str, ViewportDefinition] = {
    "320": VP_320,
    "768": VP_768,
    "1024": VP_1024,
    "1440": VP_1440,
}


def get_canonical_viewports() -> Dict[str, ViewportDefinition]:
    """Returns the dictionary of canonical viewport specifications."""
    return dict(CANONICAL_VIEWPORTS)


# -----------------------------------------------------------------------------
# 2. Canonical 17-Run Deterministic Execution Matrix (ADR-071 & ADR-075)
# -----------------------------------------------------------------------------

CANONICAL_MATRIX_RUNS: List[ResponsiveRunConfig] = [
    # -------------------------------------------------------------------------
    # Tier 1: Canonical Recomposition Sweep (12 Independent Runs)
    # Baseline: Theme=Light, Density=Comfortable, Direction=RTL
    # -------------------------------------------------------------------------
    ResponsiveRunConfig(
        run_id="RWD-RUN-001",
        route="#/overview",
        screen="Overview",
        viewport=VP_320,
        theme="light",
        density="comfortable",
        direction="rtl",
        fresh_session=True,
        expected_contracts=[
            "#btn-mobile-nav visible",
            ".mds-ref-sidebar hidden",
            ".mds-ref-stats-grid cols=1",
            "overflow <= 321px",
            "touch targets >= 44x44px",
        ],
    ),
    ResponsiveRunConfig(
        run_id="RWD-RUN-002",
        route="#/overview",
        screen="Overview",
        viewport=VP_768,
        theme="light",
        density="comfortable",
        direction="rtl",
        fresh_session=False,
        expected_contracts=[
            "#btn-mobile-nav hidden",
            ".mds-ref-sidebar rail (72px)",
            "sidebar labels hidden",
            ".mds-ref-stats-grid cols=2",
            "overflow <= 769px",
        ],
    ),
    ResponsiveRunConfig(
        run_id="RWD-RUN-003",
        route="#/overview",
        screen="Overview",
        viewport=VP_1024,
        theme="light",
        density="comfortable",
        direction="rtl",
        fresh_session=False,
        expected_contracts=[
            "#btn-mobile-nav hidden",
            ".mds-ref-sidebar width=260px",
            "sidebar labels visible",
            ".mds-ref-stats-grid cols >= 3",
            "container max-width <= 1152px",
            "overflow <= 1025px",
        ],
    ),
    ResponsiveRunConfig(
        run_id="RWD-RUN-004",
        route="#/overview",
        screen="Overview",
        viewport=VP_1440,
        theme="light",
        density="comfortable",
        direction="rtl",
        fresh_session=False,
        expected_contracts=[
            "#btn-mobile-nav hidden",
            ".mds-ref-sidebar width=260px",
            "container max-width <= 1440px",
            "overflow <= 1441px",
        ],
    ),
    ResponsiveRunConfig(
        run_id="RWD-RUN-005",
        route="#/items",
        screen="Items List",
        viewport=VP_320,
        theme="light",
        density="comfortable",
        direction="rtl",
        fresh_session=True,
        expected_contracts=[
            "filter bar column/wrap",
            "table container overflowX=auto",
            "touch targets >= 44x44px",
            "overflow <= 321px",
        ],
    ),
    ResponsiveRunConfig(
        run_id="RWD-RUN-006",
        route="#/items",
        screen="Items List",
        viewport=VP_768,
        theme="light",
        density="comfortable",
        direction="rtl",
        fresh_session=False,
        expected_contracts=[
            "table container responsive scroll",
            "action button cluster wrapped",
            "overflow <= 769px",
        ],
    ),
    ResponsiveRunConfig(
        run_id="RWD-RUN-007",
        route="#/items",
        screen="Items List",
        viewport=VP_1024,
        theme="light",
        density="comfortable",
        direction="rtl",
        fresh_session=False,
        expected_contracts=[
            "full data table visible",
            "pagination inline",
            "container max-width <= 1152px",
            "overflow <= 1025px",
        ],
    ),
    ResponsiveRunConfig(
        run_id="RWD-RUN-008",
        route="#/items",
        screen="Items List",
        viewport=VP_1440,
        theme="light",
        density="comfortable",
        direction="rtl",
        fresh_session=False,
        expected_contracts=[
            "high-throughput data layout",
            "container max-width <= 1440px",
            "overflow <= 1441px",
        ],
    ),
    ResponsiveRunConfig(
        run_id="RWD-RUN-009",
        route="#/items/edit",
        screen="Item Edit",
        viewport=VP_320,
        theme="light",
        density="comfortable",
        direction="rtl",
        fresh_session=True,
        expected_contracts=[
            ".mds-ref-form-grid-2 cols=1",
            "danger zone stacked",
            "touch targets >= 44x44px",
            "overflow <= 321px",
        ],
    ),
    ResponsiveRunConfig(
        run_id="RWD-RUN-010",
        route="#/items/edit",
        screen="Item Edit",
        viewport=VP_768,
        theme="light",
        density="comfortable",
        direction="rtl",
        fresh_session=False,
        expected_contracts=[
            ".mds-ref-form-grid-2 cols=1",
            "stepper/tabs scrollable",
            "overflow <= 769px",
        ],
    ),
    ResponsiveRunConfig(
        run_id="RWD-RUN-011",
        route="#/items/edit",
        screen="Item Edit",
        viewport=VP_1024,
        theme="light",
        density="comfortable",
        direction="rtl",
        fresh_session=False,
        expected_contracts=[
            ".mds-ref-form-grid-2 cols=2",
            "stepper tabs inline",
            "container max-width <= 1152px",
            "overflow <= 1025px",
        ],
    ),
    ResponsiveRunConfig(
        run_id="RWD-RUN-012",
        route="#/items/edit",
        screen="Item Edit",
        viewport=VP_1440,
        theme="light",
        density="comfortable",
        direction="rtl",
        fresh_session=False,
        expected_contracts=[
            ".mds-ref-form-grid-2 cols=2",
            "full side-by-side editing",
            "container max-width <= 1440px",
            "overflow <= 1441px",
        ],
    ),

    # -------------------------------------------------------------------------
    # Tier 2: Orthogonal Invariant Checks (5 Independent Runs)
    # -------------------------------------------------------------------------
    ResponsiveRunConfig(
        run_id="RWD-RUN-013",
        route="#/overview",
        screen="Overview",
        viewport=VP_320,
        theme="light",
        density="comfortable",
        direction="ltr",
        fresh_session=True,
        expected_contracts=[
            "LTR mobile symmetry",
            "#btn-mobile-nav inline-start (left)",
            "zero row-reverse in CSS",
            "overflow <= 321px",
        ],
    ),
    ResponsiveRunConfig(
        run_id="RWD-RUN-014",
        route="#/overview",
        screen="Overview",
        viewport=VP_768,
        theme="light",
        density="comfortable",
        direction="ltr",
        fresh_session=False,
        expected_contracts=[
            "LTR tablet symmetry",
            "72px rail anchors inline-start (left)",
            "zero physical left/right margin hacks",
            "overflow <= 769px",
        ],
    ),
    ResponsiveRunConfig(
        run_id="RWD-RUN-015",
        route="#/items",
        screen="Items List",
        viewport=VP_320,
        theme="light",
        density="compact",
        direction="rtl",
        fresh_session=True,
        expected_contracts=[
            "Density touch target invariant",
            "buttons retain >= 44x44px despite compact",
            "overflow <= 321px",
        ],
    ),
    ResponsiveRunConfig(
        run_id="RWD-RUN-016",
        route="#/items",
        screen="Items List",
        viewport=VP_1024,
        theme="light",
        density="compact",
        direction="rtl",
        fresh_session=False,
        expected_contracts=[
            "Density desktop invariant",
            "compact table rows without truncation",
            "overflow <= 1025px",
        ],
    ),
    ResponsiveRunConfig(
        run_id="RWD-RUN-017",
        route="#/overview",
        screen="Overview",
        viewport=VP_320,
        theme="high-contrast",
        density="comfortable",
        direction="rtl",
        fresh_session=True,
        expected_contracts=[
            "High contrast mobile invariant",
            "borders and focus rings visible",
            "mobile reflow intact",
            "overflow <= 321px",
        ],
    ),
]


def get_canonical_matrix() -> List[ResponsiveRunConfig]:
    """Returns a list of all 17 canonical run configurations."""
    return list(CANONICAL_MATRIX_RUNS)


def get_run_config_by_id(run_id: str) -> Optional[ResponsiveRunConfig]:
    """Retrieves a specific run config by its canonical run_id."""
    for run in CANONICAL_MATRIX_RUNS:
        if run.run_id == run_id:
            return run
    return None
