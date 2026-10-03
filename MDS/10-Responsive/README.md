# MDS Layer 10 — Responsive Architecture & Device Strategy (Canonical Pointer)

## Architectural Role & Scope
Layer 10 defines the multi-device layout recomposition models, breakpoint boundaries, viewport constraints, and ergonomics across mobile, tablet, desktop, and ultra-wide form factors.

## Core Architectural Invariants
1. **Recomposition, Not Shrinking:** Responsive design in MDS is the structural reorganization of visual hierarchy, navigation, and information density—not scaling desktop elements down mechanically.
2. **Canonical Viewports & Breakpoints:**
   - **Mobile:** 320px – 767px (Single-column, bottom sheets, sticky action footer)
   - **Tablet:** 768px – 1023px (Dedicated master-detail / dual-pane layout standard)
   - **Desktop:** 1024px – 1439px (Persistent sidebar, multi-column workspace)
   - **Wide:** ≥ 1440px (Max-width container containment)
3. **Canonical Container Max-Widths:**
   - **Standard Container:** **1152px** (`container.lg`)
   - **Wide Container:** **1440px** (`container.xl`)
   - *Constraint:* 1280px container max-width is strictly prohibited in MDS.
4. **Hit-Box & Touch Target:** Mandatory minimum **44×44px** interaction target across all viewports (WCAG 2.5.5 / 2.5.8).

## Canonical Sources of Truth
Responsive contracts are maintained in:

1. **Foundations Specification (Grid & Spacing):**
   - [`MDS/01-Foundations/03-Spacing-and-Grid.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/01-Foundations/03-Spacing-and-Grid.md) — Modular grid, gutters, margins, and container tokens.
2. **Device & Interaction Strategy Rules:**
   - [`.agents/rules/03_responsive_and_devices.md`](file:///d:/Work/Dev/Master%20Design%20System/.agents/rules/03_responsive_and_devices.md) — Form-factor rules, tablet master-detail strategy, and touch/pointer parity.
3. **Master Specification Summary:**
   - [`MDS/MDS_MASTER_SPECIFICATION.md` (Section 14)](file:///d:/Work/Dev/Master%20Design%20System/MDS/MDS_MASTER_SPECIFICATION.md#14-responsive-architecture--device-strategy-layer-10)
