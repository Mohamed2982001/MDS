# MDS Implementation Decision Log (IDR-001 through IDR-010)

**Layer:** 13-Implementation  
**Target Specification:** [`MDS-Implementation-Architecture.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/13-Implementation/MDS-Implementation-Architecture.md)  
**Status:** APPROVED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Ratification Date:** 2026-09-20  

---

## IDR-001: Technology Stack — Hybrid Modern Web Standards Architecture

- **Context:** Transitioning MDS from canonical architecture into Phase 9 implementation requires choosing an underlying runtime technology. Options evaluated: Option A (React / Next.js), Option B (Pure HTML/CSS), Option C (Hybrid Web Standards: Custom Elements + CSS `@layer` + DTCG Python Compiler).
- **Evidence:** The repository currently has zero `package.json` or `node_modules` dependencies, while containing Node v24.14.0 and Python 3.12.10. Existing showcase sandboxes (`03-Primitives`, `05-Patterns`, `06-Workflows`, `07-Templates`, `Documentation`) run instantly via pure HTML5, CSS custom properties, and vanilla ES6 without build step failures.
- **Inference:** Introducing heavy third-party framework dependencies (React, Vite, Webpack) locks the design system to a single vendor ecosystem, introduces package version decay, and hinders direct consumption by Flutter, Laravel, or other non-React stacks.
- **Decision:** Ratified **Option C (Hybrid Modern Web Standards Architecture)**. The runtime is delivered as pure CSS cascade layers and native HTML5/Custom Elements, compiled via a zero-dependency Python tool. Downstream frameworks wrap these native elements trivially.

---

## IDR-002: Token Compilation Strategy — Native Python DTCG Compiler

- **Context:** 18 W3C DTCG token files in `MDS/02-Tokens/` must be converted into runtime CSS variables and typed constants.
- **Evidence:** `MDS/10-Testing/run_tests.py` already includes an internal parser that reads, resolves, and validates all 188 tokens in sub-millisecond execution without external libraries.
- **Inference:** A standalone, zero-dependency Python script (`compile_tokens.py`) eliminates reliance on heavy Node-based tools like Style Dictionary while guaranteeing 100% deterministic compilation, alias resolution, and circularity detection.
- **Decision:** Build `compile_tokens.py` in Phase 9.2. Outputs: `dist/tokens/tokens.css` (CSS Custom Properties in `@layer mds.tokens`) and `dist/tokens/tokens.d.ts` (TypeScript interfaces).

---

## IDR-003: CSS Specificity Management — Native CSS Cascade Layers (`@layer`)

- **Context:** As the design system scales across primitives, components, patterns, and templates, CSS specificity collisions and `!important` escalation can contaminate styles.
- **Evidence:** W3C CSS Cascade Layers (`@layer`) are supported across all modern browsers (Chrome 99+, Safari 15.4+, Firefox 97+), providing native specificity isolation based on layer order rather than selector weight.
- **Inference:** Wrapping all MDS stylesheets in a predefined layer sequence permanently prevents lower-tier resets from clobbering components and prevents component styles from overriding consumer layout utilities.
- **Decision:** Enforce the following mandatory CSS layer hierarchy:
  ```css
  @layer mds.reset, mds.tokens, mds.foundations, mds.primitives, mds.components, mds.patterns, mds.templates, mds.overrides;
  ```

---

## IDR-004: Component Encapsulation — Light DOM Custom Elements with Semantic HTML

- **Context:** Interactive components (`Dialog`, `Tabs`, `Switch`, `Tooltip`, `Select`) require stateful behavior and keyboard listeners. We must decide between Shadow DOM vs Light DOM custom elements.
- **Evidence:** Shadow DOM encapsulates styles completely but creates severe barriers for design token CSS custom property inheritance, global themes, screen-reader accessibility tools, and server-side rendering.
- **Inference:** Light DOM Custom Elements provide lifecycle hooks (`connectedCallback`, `disconnectedCallback`) and clean HTML tag ergonomics (`<mds-dialog>`, `<mds-tabs>`) while allowing direct token consumption and transparent DOM inspection by testing tools and screen readers.
- **Decision:** Standardize on **Light DOM Custom Elements** for interactive behaviors, preserving semantic HTML elements internally (e.g. `<dialog>`, `<button>`, `<input>`).

---

## IDR-005: Theme Resolution Order — Strict Cascading Precedence

- **Context:** MDS supports 3 Modes (Light, Dark, High Contrast), 3 Presets (Refined, Soft Modern, Expressive), 3 Density tiers (Comfortable, Compact, Dense), and 2 Directions (LTR, RTL).
- **Evidence:** Foundations Decision ADR-005 and Token Architecture Section 10 define the canonical resolution order: `Base` $\to$ `Brand` $\to$ `Mode` $\to$ `Preset` $\to$ `Density` $\to$ `Direction`.
- **Inference:** Allowing themes to modify component CSS selectors directly leads to combinatorial explosion ($3 \times 3 \times 3 \times 2 = 54$ variations per component).
- **Decision:** Runtime theming is implemented strictly by re-aliasing CSS custom properties at the container root (`[data-mode]`, `[data-preset]`, `[data-density]`, `[dir]`). Component CSS rules remain 100% invariant across themes.

---

## IDR-006: Bidirectional Layout Standard — 100% CSS Logical Properties

- **Context:** Arabic (RTL) is a first-class citizen alongside Latin (LTR). Physical layout hacks (`float: right`, `left: 10px`, `row-reverse`) break accessibility and focus order.
- **Evidence:** MDS automated tests (`MDS-RTL-001`, `MDS-RTL-002`) already mandate zero `row-reverse` to protect WCAG 2.4.3 focus order.
- **Inference:** Designing exclusively with CSS Logical Properties (`inline`, `block`, `start`, `end`) renders layouts inherently bidirectional without generating separate RTL stylesheets.
- **Decision:** Ban all physical horizontal properties (`margin-left`, `right`, `left`, `float`) in runtime stylesheets. All horizontal styling must use `*-inline-start` and `*-inline-end`. Directional icons mirror; static icons do not mirror.

---

## IDR-007: Interaction Hit Target Standard — 44×44px PressTarget Contract

- **Context:** Touch targets on mobile and tablet devices must ensure effortless tactile activation without accidental taps.
- **Evidence:** Master Specification Section 11 and agent rules mandate a 44×44px hit-box as an internal MDS design-system rule (stricter than WCAG AA 2.5.8 24×24px minimum).
- **Inference:** Visual sizes of small controls (e.g. 32px small button or 20px checkbox) must not be forced to 44px visually, as this degrades desktop information density.
- **Decision:** Implement the `PressTarget` contract via pseudo-elements (`::after`) or transparent padding on touch viewports (`@media (pointer: coarse)`), expanding the hit area to $\ge 44 \times 44\text{px}$ without distorting visual geometry.

---

## IDR-008: Motion Discipline — Purpose-Driven Motion & Reduced-Motion Safety

- **Context:** Animations can communicate spatial relationships and state transitions but can cause cognitive overload or vestibular discomfort.
- **Evidence:** MDS foundations define 4 calibrated durations (0ms, 150ms, 250ms, 350ms) and natural deceleration curve `cubic-bezier(0.2, 0, 0, 1)`.
- **Inference:** Motion must never be decorative. If the user prefers reduced motion, transitions must collapse instantly without breaking functional state changes.
- **Decision:** Bind all transitions to MDS motion tokens. Enforce global `@media (prefers-reduced-motion: reduce)` block resetting all transition durations to `0.01ms` (or `0ms`).

---

## IDR-009: Shared Runtime Core — Zero Playground-Only Implementations

- **Context:** The Phase 9 implementation consists of both an Interactive Playground (Phase 9.5) and a Reference Application (Phase 9.6).
- **Evidence:** In fragmented design systems, playgrounds often maintain duplicate mock components that diverge from production application code.
- **Inference:** Maintaining separate component code for the playground creates two sources of truth and invalidates playground testing.
- **Decision:** The Playground and Reference Application must consume the **identical Runtime Core** (`dist/tokens/`, `dist/css/`, `dist/components/`). The Playground only provides inspection wrappers; it never implements components.

---

## IDR-010: Governance of Implementation Debt — No Implicit Baseline Mutability

- **Context:** During implementation, developers or AI agents may discover missing tokens, desirable component variants, or convenient style overrides.
- **Evidence:** MDS Architecture Baseline v1.0.0 was formally ratified with 188 tokens, 19 components, 8 patterns, 6 workflows, and 6 templates.
- **Inference:** Permitting implementation files to alter baseline architecture without formal governance destroys architectural traceability.
- **Decision:** Implementation code cannot add tokens, primitives, components, or patterns to MDS. If a missing architectural element is identified, it must follow formal MDS governance: author an ADR, propose in Layer 12, calibrate, audit, and obtain Lead Architect approval.
