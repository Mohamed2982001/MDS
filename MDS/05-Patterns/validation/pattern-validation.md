# MDS Pattern Validation Methodology & Verification Framework

**Document Layer:** 05-Patterns / Validation  
**Status:** APPROVED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-16  

---

## 1. Purpose & Guiding Principles

This document establishes the official **Pattern Validation Methodology** for Layer 05 of the Master Design System (MDS). Before any pattern is promoted to **Stable**, it must pass rigorous inspection across seven objective engineering dimensions.

---

## 2. The 7-Dimension Validation Framework

### 1. Structural & Compositional Integrity
- [ ] **Layer Hierarchy:** The pattern composes ONLY Layer 03 Primitives and Layer 04 Components. Lower layers do not import the pattern.
- [ ] **No Hidden Components:** The pattern does not disguise an unapproved atomic component or custom state machine as a pattern.
- [ ] **Parent-Owned Spacing (CDR-001):** Pattern elements declare zero external margins (`margin`, `margin-block`, `margin-inline`). All spacing is owned by `Stack`, `Inline`, `Grid`, or `Cluster`.
- [ ] **Surface & Depth Triad (CDR-006):** Layers follow continuous elevation strata: `Canvas` $\to$ `Surface` $\to$ `Raised/Card` $\to$ `Overlay`.

### 2. Semantic & Information Hierarchy
- [ ] **User Intent Fidelity:** The pattern directly solves a recognized, documented user intent.
- [ ] **Clear Primary CTA:** Exactly one primary call-to-action is established; destructive actions are visually isolated.
- [ ] **SoftWrap Invariant:** Text copy has `softWrap: true` and wraps gracefully across 2+ lines without truncation.

### 3. Accessibility & Interaction Compliance
> *Standards Scope:* Implemented accessibility behaviors were validated against selected WCAG success criteria where applicable. Comprehensive cross-platform assistive technology testing remains deferred to Phase 8.
- [ ] **Touch Target Invariant (CDR-002):** Interactive controls preserve the MDS minimum interaction target where applicable ($\ge 44 \times 44\text{px}$ via `PressTarget`). Static visual elements (e.g. non-clickable badges) are not subject to target sizing.
- [ ] **Focus Order (WCAG SC 2.4.3 Benchmark):** Keyboard `Tab` traversal follows visual reading order 100%.
- [ ] **Focus Visibility (WCAG SC 2.4.7 Benchmark):** All interactive elements display a contrasting 2px focus ring (`FocusRing`).
- [ ] **Programmatic Associations:** All form controls are connected to labels via `htmlFor`/`id`; error states are wired to `role="alert"` and `aria-invalid`.
- [ ] **Icon Accessibility:** All icon-only buttons declare a mandatory accessible name via `VisuallyHidden` or `aria-label`.

### 4. Responsive Recomposition
- [ ] **No Mere Shrinking:** Small viewports trigger structural recomposition (stacking, collapsing metadata) rather than proportional shrinking.
- [ ] **Compact (<640px):** Single-column layouts, full-width actions, and no observed horizontal overflow for the included Pattern examples in the current sandbox.
- [ ] **Standard (640–1024px):** 2-column grids, inline toolbars.
- [ ] **Wide (>1024px):** Line lengths constrained to readable maximums (`container.md` or `container.lg`).

### 5. RTL & Logical Axis Progression (PDR-009 / CDR-003)
- [ ] **Zero Row-Reverse:** `flex-direction: row-reverse` is strictly prohibited.
- [ ] **Logical Properties:** All margins, paddings, and insets use logical CSS properties (`margin-inline`, `padding-inline`, `inset-inline-*`).
- [ ] **Directional Iconography:** Chevrons, arrows, and navigation glyphs flip automatically in RTL viewports; non-directional icons remain unchanged.
- [ ] **Sandbox Scope:** RTL structural and logical-property checks passed in the current sandbox. Broader language/content localization testing remains outside this closure pass.

### 6. Token Discipline & Zero Visual Literals
- [ ] **Zero Raw Hex Colors:** All colors resolve through semantic or primitive tokens.
- [ ] **Zero Raw Spacing:** All padding and gaps resolve through the 4px base spacing scale (`space.1` through `space.16`).
- [ ] **Zero Raw Motion:** All transitions use `motion.duration.fast` (150ms) or `motion.duration.normal` (250ms); reduced-motion collapse to 0s is enforced.

### 7. AI Determinism & Anti-Pattern Elimination
- [ ] **Machine-Readable Selection:** Pattern selection rules can be deterministically executed by an LLM.
- [ ] **Zero Prohibited Combinations:** None of the 5 canonical anti-patterns are present (e.g. Empty State without Action, Dialog over Dialog).

---

## 3. Evidence-Based Verification Taxonomy

As codified in Phase 5 and Phase 6, all patterns must be reported under one of four explicit evidence levels:

```text
Specified                               → Complete 22-point architectural specification codified in markdown.
Implemented                             → Structural code/CSS classes exist in repository testbed.
Manually Verified                       → Tested interactively in the browser validation sandbox across themes and viewports.
Automated Verified                      → Verified via automated functional test suites.
Automated Token/Style Integrity Check   → Automated verification of tokens, alias resolution, and zero raw hex colors.
```

Claims of verification must strictly correspond to demonstrated technical reality without inflating evidence levels.
