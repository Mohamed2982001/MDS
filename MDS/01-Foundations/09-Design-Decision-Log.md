# MDS Architecture Decision Records (ADR Log)
**Document Layer:** 01-Foundations  
**Status:** APPROVED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## ADR-001: Unified Multilingual Typographic Standard (Cairo & JetBrains Mono)
- **Status:** APPROVED
- **Context:** Design systems supporting both Arabic and Latin often maintain separate fonts (e.g. Inter for English and Cairo/Tajawal for Arabic). This introduces x-height discrepancies, baseline misalignments, and visual jarring in mixed-language strings.
- **Decision:** Adopt **Cairo** (Google Fonts) as the primary unified typeface for both Latin and Arabic scripts, and **JetBrains Mono** for code and telemetry data.
- **Rationale & Evidence:** Cairo provides harmonious geometric proportions across both Arabic and Latin character sets, avoiding multi-font fallbacks. To maintain vertical rhythm, Arabic script uses an intentional +0.15 context-aware leading multiplier.
- **Typographic Scale:** Discretized Typographic Scale (12, 14, 16, 20, 24, 30, 36, 48px), optimized for pixel-snapping and UI readability, loosely structured around a Minor Third interval stepping (1.200–1.250).
- **Trade-offs:** Cairo has a distinct geometric personality. Projects requiring a neutral corporate grotesque may override `font.family.primary` via Brand overrides.
- **Confidence:** High.

---

## ADR-002: Modular Spacing Scale (4px Base Grid)
- **Status:** APPROVED
- **Context:** Balancing spatial consistency with high data-density requirements across mobile and desktop.
- **Decision:** Adopt a **4px modular grid** (`0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64px`) with mandatory **Parent-Owned Spacing** (components never declare external margins).
- **Rationale & Evidence:** 4px provides fine-grained control for compact chips and form controls while aligning with standard 8px layout blocks. Spacing is strictly owned by layout containers (`Stack`, `Inline`, `Grid`).
- **Confidence:** High.

---

## ADR-003: Chromatic Slate Neutrals & Royal Sapphire Brand
- **Status:** APPROVED
- **Context:** Achromatic pure gray looks sterile and cold, while heavily tinted grays clash with brand colors.
- **Decision:** Adopt **Chromatic Slate** neutrals (nominal HSL 210°–222°, saturation 16%–47%) and **Royal Sapphire** (`#2563EB`) as primary brand anchor.
- **Empirical Validation:**
  - `neutral.900` (`#0F172A`) on white: **17.85:1** (WCAG AAA Pass).
  - `neutral.500` (`#64748B`) on white: **4.76:1** (WCAG AA Pass).
  - `brand.600` (`#2563EB`) on white: **5.17:1** (WCAG AA Pass).
  - `brand.700` (`#1D4ED8`) on white: **6.70:1** (WCAG AA Pass).
  - `brand.800` (`#1E40AF`) on white: **8.72:1** (WCAG AAA Pass).
  - `red.600` (`#DC2626`) on white: **4.83:1** (WCAG AA Pass).
- **Confidence:** High.

---

## ADR-004: Refined Softness Shape Grammar (`radius.md` = 10px)
- **Status:** APPROVED
- **Context:** Choosing corner radii that balance modern warmth with enterprise data density.
- **Decision:** Adopt **Refined Softness** with 10px (`radius.md`) default for primary buttons, inputs, and cards. Scale: 0, 4, 6, 10, 14, 20, 9999px.
- **Concentricity:** Contextual geometric alignment rule for nested surface fills and inset containers ($R_{\text{inner}} \approx \max(0, R_{\text{outer}} - P)$).
- **Confidence:** High.

---

## ADR-005: Elevation Depth Triad & Dark Mode Stepping
- **Status:** APPROVED
- **Context:** Communicating z-axis elevation across light and dark modes without muddy drop shadows.
- **Decision:** Enforce the **Depth Triad** (Surface Luminance > Subtle 1px Border > Dual-Layer Soft Ambient Shadow).
- **Dark Mode Strategy:** Progressive surface lightening (`neutral.950` canvas $\to$ `neutral.900` surface $\to$ `neutral.800` raised $\to$ `neutral.700` overlay).
- **Confidence:** High.

---

## ADR-006: Responsive Grid Container Max-Widths (1152px Standard & 1440px Wide)
- **Status:** APPROVED
- **Context:** An inconsistency was flagged during Phase 3.5 Gate review where `03-Spacing-and-Grid.md` had referenced 1280px without an authoritative ADR, whereas the original Phase 3 requirement specified 1152px and 1440px.
- **Decision:** Restore the authoritative standard application container max-width to **1152px** (`container.lg`), and retain **1440px** (`container.xl`) for wide/high-throughput dashboards and data grids.
- **Rationale & Evidence:** 1152px maintains ideal line length (65–75 characters per line at `font.size.base = 16px` with comfortable margins) and maps cleanly to 12 columns with 24px/32px gutters. 1440px accommodates dense multi-column enterprise layouts without unconstrained horizontal stretching.
- **Confidence:** High.

---

## ADR-007: Formal Deferral of Continuous Loop Motion & 28px Control Primitives
- **Status:** APPROVED (Decided: Formally Deferred)
- **Context:** During the calibration audit, two future enhancements were proposed: `motion.loop.*` for continuous ambient AI loops, and `size.control.xs = 28px` for extreme desktop density.
- **Decision:** Formally classify both proposals as **DEFERRED — FUTURE PHASE**. Zero tokens are added to the active token repository in Phase 3.5.
- **Rationale:** Concrete token requirements for continuous loops and ultra-compact controls can only be properly validated when actual Loading/AI/Streaming components (Proposal 1) and dense Data Grid components (Proposal 2) are designed in Phase 5. The active primitive control scale remains strictly 32px, 40px, and 48px.
- **Confidence:** High.
