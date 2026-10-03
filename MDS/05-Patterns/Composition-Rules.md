# MDS Pattern Composition Rules & Layout Laws

**Document Layer:** 05-Patterns  
**Status:** APPROVED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-16  

---

## 1. Purpose & Guiding Principles

This document establishes the binding **structural, spatial, and semantic composition laws** governing how MDS Primitives (Layer 03) and Components (Layer 04) are combined to form Layer 05 Patterns. Every pattern must comply with these 10 inviolable rules.

---

## 2. The 10 Inviolable Composition Laws

### Rule 1: Parent-Owned Spacing (Zero External Margins)
- **Law:** Components and pattern sub-elements must **never** declare external margins (`margin`, `margin-block`, `margin-inline`, `margin-top`, `margin-left`).
- **Mechanism:** All spatial distribution between elements is owned exclusively by layout primitives:
  - Vertical sequencing $\longrightarrow$ `<Stack gap="...">`
  - Horizontal inline arrangement $\longrightarrow$ `<Inline gap="..." align="..." justify="...">`
  - Multi-row wrapping tags / chips $\longrightarrow$ `<Cluster gap="...">`
  - 2D responsive grids $\longrightarrow$ `<Grid columns="..." gap="...">`
- **Violation Example:** `<Button style="margin-top: 16px;">` is strictly forbidden.

---

### Rule 2: Surface & Depth Triad (Strict Layering)
- **Law:** Elevation planes must always progress in natural, continuous strata. A pattern may never render an elevated layer directly on an inappropriate background plane:
  $$\text{Canvas (Layer 0)} \longrightarrow \text{Surface (Layer 1)} \longrightarrow \text{Raised / Card (Layer 2)} \longrightarrow \text{Floating / Overlay (Layer 3)}$$
- **Visual Contrast:** When nesting cards inside surfaces, contrast must be maintained via border (`color.border.default`) or elevation shift (`elevation.level1`).
- **Violation Example:** Placing an overlay modal directly on an empty Canvas without a semi-transparent scrim (`color.surface.overlay`).

---

### Rule 3: Interaction Hit-Box Preservation ($\ge 44 \times 44\text{px}$)
- **Law:** Visual compactness must never compromise physical motor accessibility.
- **Rule:** Interactive controls preserve the MDS minimum interaction target where applicable. Regardless of density mode (`Comfortable`, `Compact`, `Dense`) or control size (`32px` sm, `40px` md, `48px` lg), every interactive element in a pattern (buttons, links, form controls, clickable chips) must retain an effective hit-box of at least **$44 \times 44\text{px}$** (`PressTarget`) on touch viewports.
- **Non-Interactive Distinction:** Static visual elements (such as purely informative Badges, static captions, and decorative icons) are not interactive controls and are not subject to the $44 \times 44\text{px}$ target requirement.
- **Visual vs. Hit-Box Separation:** A small button or icon button may visually render at 32px height, but its touch wrapper must expand transparently to $\ge 44\text{px}$.

---

### Rule 4: Native Inline-Axis Progression & Reading Order (Anti-Row-Reverse)
- **Law:** Patterns must always flow along the logical inline axis (`inline-start` $\to$ `inline-end`).
- **DOM Order Integrity:** Visual reading order and keyboard `Tab` traversal order must be identical.
- **Strict Prohibition:** `flex-direction: row-reverse` is strictly prohibited. For RTL locales, layout direction is handled entirely by `dir="rtl"`.
- **Property Discipline:** Never use physical CSS coordinates (`left`, `right`, `margin-left`, `padding-right`). Always use logical CSS properties (`margin-inline-start`, `padding-inline-end`, `inset-inline-start`).

---

### Rule 5: Non-Truncation & SoftWrap Discipline
- **Law:** Descriptive, functional, or instruction text must **never** be truncated with `text-overflow: ellipsis`.
- **Rule:** All titles, descriptions, error alerts, and field labels must have `softWrap: true` (or `white-space: normal`) and expand gracefully to 2+ lines.
- **Allowed Exception:** Only single-line technical identifiers, URLs, file paths, or entity hash strings may use truncation or middle-ellipsis where wrapping would break meaning.

---

### Rule 6: Action Placement & Visual Hierarchy
- **Law:** Every pattern with actions must establish a single primary call to action (CTA).
- **Hierarchy:**
  - `Primary Action`: Exactly ONE prominent button (`variant="primary"`).
  - `Secondary Actions`: Outline or surface buttons (`variant="secondary"`).
  - `Tertiary Actions`: Borderless subtle buttons (`variant="ghost"`).
  - `Destructive Actions`: Isolated, distinct styling (`variant="destructive"`), placed apart from non-destructive primary actions to prevent mis-clicks.
- **Alignment:**
  - In LTR: Primary CTA is anchored at the trailing edge (`inline-end` / right) in modal footers, or leading edge in form bars.
  - In RTL: Naturally mirrors along the inline axis (`inline-start` / `inline-end`).

---

### Rule 7: Centralized Form Field Integration
- **Law:** Individual inputs (`Input`, `Select`, `Textarea`, `Checkbox`, `Radio`) must never be placed in a pattern as isolated, unlabelled elements.
- **Architecture:** All form inputs must be composed inside the centralized `Field` primitive wrapper:
  $$\text{Field} = \text{Stack} + \text{Label} + \text{Control} + \text{HelperText} + \text{LiveRegion (Alert)}$$
- This guarantees unified ARIA relationships (`htmlFor`, `aria-describedby`, `aria-invalid`) across the pattern.

---

### Rule 8: Density Mode Adaptation
- **Law:** Density modes alter spatial packaging and internal component dimensions without breaking structural semantics:
  - `Comfortable`: Default mode. Spacious padding (`space.4` to `space.6`), generous control heights (`40px` md, `48px` lg).
  - `Compact`: Reduced padding (`space.2` to `space.3`), tighter stack gaps, control height `32px` sm.
  - `Dense`: Reserved for specialized data-heavy technical dashboards.
- **Invariant:** The deferred `28px` control height remains strictly deferred; `32px` remains the minimum visual control boundary.

---

### Rule 9: Motion & Animation Discipline
- **Law:** Patterns must never introduce unapproved custom transition durations or raw cubic-bezier curves.
- **Binding Tokens:**
  - Micro-interactions (hover, focus, toggles): `var(--mds-motion-fast)` (150ms).
  - Macro-transitions (accordion expansion, dialog reveal, card expansion): `var(--mds-motion-normal)` (250ms) with `var(--mds-motion-ease-standard)`.
- **Reduced Motion:** When `@media (prefers-reduced-motion: reduce)` is active, all transitions and animations collapse to `0s !important` or static state indicators.

---

### Rule 10: Anti-Bloat & Enterprise Deferral Enforcement
- **Law:** Patterns must strictly respect the formal deferral of the 9 complex enterprise systems.
- **Prohibited Substitutions:**
  - Do NOT build inline cell-editable tables in place of `DataGrid`.
  - Do NOT build multi-month calendars in place of `Calendar` / `DateRangePicker`.
  - Do NOT build searchable multi-tag dropdowns in place of `Combobox`.
- Use the approved static `Table` component with pagination and external filter bars.
