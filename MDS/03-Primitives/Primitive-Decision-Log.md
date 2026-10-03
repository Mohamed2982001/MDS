# MDS Primitive Decision Records (PDR Log)
**Document Layer:** 03-Primitives  
**Status:** APPROVED (Phase 4 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## PDR-001: Selection of Core Layout Primitives & Scope Boundaries
- **Status:** APPROVED
- **Context:** Deciding which layout primitives are justified at the foundational layer without polluting the API with redundant abstractions.
- **Decision:** Implement **`Container`**, **`Stack`**, **`Inline`**, **`Grid`**, and **`Cluster`**. Reject `Center`, `Sidebar`, `Split`, and `Bleed` as distinct foundational primitives.
- **Evidence:** Industry layout systems (Braid, Chakra, Every Layout, Polaris) demonstrate that $95\%+$ of UI layouts are compositions of 1D vertical stacks, 1D horizontal rows, 2D wrapping groups, and 2D responsive grids.
- **Inference:** Introducing separate primitives for minor alignment variations creates API fatigue and contradictory layout paths.
- **Design Judgment:** Keep the primitive layer minimal, orthogonal, and strictly focused on parent-owned spacing.
- **Confidence:** High.

---

## PDR-002: Rejection of Standalone `Center` Primitive
- **Status:** APPROVED (Rejected as Standalone Primitive)
- **Context:** Evaluating whether `<Center>` warrants a separate primitive component.
- **Decision:** Reject `Center` as a standalone primitive. Alignment and centering are handled directly via `Stack(align="center", justify="center")` or `Inline(align="center", justify="center")`.
- **Evidence:** A dedicated `Center` component is merely a 1-line flexbox wrapper (`display: flex; align-items: center; justify-content: center;`) that does not introduce novel spacing or layout logic.
- **Implementation Constraint:** Adding `Center` creates ambiguity for developers choosing between `<Stack align="center">` and `<Center><Stack>`.
- **Confidence:** High.

---

## PDR-003: Categorization of `Sidebar` and `Split` as Layer 05 Patterns
- **Status:** APPROVED (Deferred to Layer 05 Patterns)
- **Context:** Evaluating whether multi-pane application layouts (`Sidebar` + main content, `Split` view) belong in Layer 03 Primitives.
- **Decision:** Formally defer `Sidebar` and `Split` to **Layer 05 Patterns**.
- **Rationale & Evidence:** True dual-pane and sidebar layouts require application-level responsive collapse state (e.g. converting a sidebar into an off-canvas slide-out drawer on tablet/mobile), master-detail selection synchronization, and navigation state. Primitives must remain pure, stateless structural wrappers.
- **Implementation Constraint:** Layer 03 primitives must not manage complex interactive navigation states.
- **Confidence:** High.

---

## PDR-004: Architectural Decoupling of Surface Planes from Elevation
- **Status:** APPROVED
- **Context:** Many component libraries collapse surface background color and box shadow into a single "elevation" token or card component.
- **Decision:** Strictly separate `Surface` (background fill, border, radius, internal padding) from `Elevation` (ambient shadows, z-index, Dark Mode luminance stepping).
- **Evidence:** Modern dark mode architectures (Material 3, Apple HIG) do not rely exclusively on drop shadows to indicate height; they use surface luminance shifts (`neutral.950` $\to$ `neutral.900` $\to$ `neutral.800` $\to$ `neutral.700`). In High Contrast Mode, shadows are suppressed entirely in favor of 1px/2px borders.
- **Design Judgment:** Surfaces must be composable with any appropriate elevation level without forcing shadow rendering on flat surfaces.
- **Confidence:** High.

---

## PDR-005: Decoupling Visual Size from Touch Interaction Area (`PressTarget`)
- **Status:** APPROVED
- **Context:** Balancing high desktop information throughput (32px controls, 16px/20px icons) with mandatory touch accessibility standards.
- **Decision:** Implement `PressTarget` to enforce the **Canonical MDS Touch Target Policy** (minimum $44 \times 44\text{px}$ hit area on touch viewports) via transparent hit-box expansion.
- **Standards Calibration:**
  - **MDS Internal Rule:** Mandatory $44 \times 44\text{px}$ touch target on mobile/touch interfaces.
  - **WCAG SC 2.5.5 (Target Size - Enhanced, Level AAA):** Recommends $44 \times 44\text{px}$ target size.
  - **WCAG SC 2.5.8 (Target Size - Minimum, Level AA):** Requires $24 \times 24\text{px}$ target size. MDS deliberately exceeds the Level AA baseline.
  - **Boundary:** Target size alone does not guarantee overall accessibility; hit-area overlap invariants ($\ge 8\text{px}$ sibling gap) and keyboard focus binding to visual boundaries must be enforced.
- **Confidence:** High.

---

## PDR-006: High-Visibility FocusRing Standard
- **Status:** APPROVED
- **Context:** Eliminating browser-dependent focus outlines without degrading keyboard accessibility.
- **Decision:** Mandate a 2px solid `brand.600` focus ring with a 2px offset (`outline-offset: 2px`), active strictly on `:focus-visible` (keyboard focus only). In High Contrast Mode, the ring renders pure `#000000` or `#FFFFFF`.
- **Evidence:** WCAG 2.1 SC 1.4.11 (Non-Text Contrast) requires $\ge 3:1$ contrast against adjacent colors. An offset ring prevents the focus indicator from clipping adjacent borders.
- **Design Judgment:** Focus rings must be invisible during mouse clicks and touch taps to maintain clean aesthetics, but instantly prominent during keyboard navigation.
- **Confidence:** High.

---

## PDR-007: Tabular Numerals Enforcement in `Numeric` Primitive
- **Status:** APPROVED
- **Context:** Proportional numbers in fonts cause changing numeric values (stock prices, timers, table metrics) to shift horizontally, producing visual vibration.
- **Decision:** Mandate `font-variant-numeric: tabular-nums` (`tnum`) for all instances of the `Numeric` primitive.
- **Evidence:** Cairo and JetBrains Mono both support OpenType `tnum` glyph substitution. Tabular figures guarantee equal character widths for digits 0–9.
- **Implementation Constraint:** Does not require a separate font; applies OpenType font features to the approved `Cairo` and `JetBrains Mono` fonts.
- **Confidence:** High.

---

## PDR-008: Vendor-Agnostic Contract for Icon Primitive with 4-Tier RTL Mirroring
- **Status:** APPROVED
- **Context:** Preventing design system lock-in to a specific third-party icon library while guaranteeing optical consistency and RTL accuracy.
- **Decision:** Define `Icon` as a contract specifying square bounding boxes (14, 16, 20, 24, 32px), optical weights, and the 4-tier RTL mirroring taxonomy.
- **Evidence:** Icons communicating directional flow or progress must mirror in RTL, while physical objects (clocks, magnifying glasses) must never mirror. A contract-based primitive allows projects to use SVGs, Lucide, or Flutter icons interchangeably without violating design system rules.
- **Confidence:** High.

---

## PDR-009: Logical Inline Progression vs. Forbidden `row-reverse` in RTL
- **Status:** APPROVED
- **Context:** Ensuring horizontal layouts adapt correctly to RTL script direction without breaking assistive navigation or visual hierarchy.
- **Decision:** Layout primitive `Inline` enforces native Flexbox inline-axis progression (`inline-start` $\to$ `inline-end`) using `flex-direction: row`. The use of `flex-direction: row-reverse` to achieve RTL layout is strictly prohibited across all primitives and downstream components.
- **Architectural Law & Evidence:** In RTL (`dir="rtl"`), `flex-direction: row` naturally starts at the right physical edge. Inverting order via `row-reverse` visually flips items while leaving the underlying DOM sequence unchanged, which creates a critical mismatch between visual order and keyboard `Tab` traversal order, directly violating **WCAG 2.1/2.2 SC 2.4.3 (Focus Order)**.
- **Confidence:** High.

