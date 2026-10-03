# MDS Pattern Decision Log (CDR & PAT Records)

**Document Layer:** 05-Patterns  
**Status:** APPROVED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-16  

---

## 1. Overview & Purpose

This log documents all binding architectural decisions made for **Layer 05: Patterns & Composition** within the Master Design System (MDS). Every architectural decision is recorded with its problem statement, decision rationale, alternatives considered, dependencies, and classification of **Evidence vs. Inference vs. Design Judgment**.

---

## 2. Decision Records (PAT-001 through PAT-010)

### PAT-001: Pattern Layer Boundary & Strict Unidirectional Flow
- **Date:** 2026-09-16
- **Status:** APPROVED
- **Problem:** Ambiguity between what constitutes an atomic component versus a composite pattern versus a page template.
- **Decision:** Codify Layer 05 as strictly composing Layer 03 Primitives and Layer 04 Components. Patterns must never import from Workflows (Layer 06) or Templates (Layer 07), and components must never import from patterns.
- **Alternatives Considered:** Allowing composite components inside Layer 04 (e.g. `SearchFilterBarComponent`). Rejected: bloated Layer 04 and obscured atomic vs. layout responsibilities.
- **Evidence:** Clean architectural separation in Shopify Polaris, Atlassian Design System, and IBM Carbon.
- **Design Judgment:** Strict layer unidirectional boundaries protect the system from circular compilation cycles.

---

### PAT-002: Mandatory 22-Point Pattern Anatomy Standard
- **Date:** 2026-09-16
- **Status:** APPROVED
- **Problem:** Patterns are often treated as casual code snippets, leading to missing accessibility, poor responsive behavior, and unhandled error states.
- **Decision:** Mandate a non-negotiable 22-point anatomy for every production pattern in Layer 05.
- **Alternatives Considered:** 10-point or 12-point lightweight template. Rejected: lightweight templates regularly drop RTL, density, motion, and AI usage rules.
- **Evidence:** Production outages and accessibility bugs predominantly stem from unhandled edge states (empty/error) and uncalibrated responsive breakpoints.
- **Design Judgment:** Comprehensive documentation prevents AI hallucinations and developer shortcuts.

---

### PAT-003: Existing-First Component Composition Law
- **Date:** 2026-09-16
- **Status:** APPROVED
- **Problem:** When designing patterns, developers frequently invent specialized one-off variants or add arbitrary CSS classes.
- **Decision:** Patterns must compose existing approved components (`Button`, `Input`, `Field`, `Card`, `Badge`, `Alert`, `Tabs`, etc.) and primitives. Zero new components and zero new tokens may be added during pattern creation.
- **Alternatives Considered:** Introducing "pattern-specific tokens". Rejected: fragments the design token repository and violates DTCG architectural coherence.
- **Evidence:** MDS token audit shows 188 registered tokens provide complete visual coverage for surfaces, actions, borders, text, and feedback.

---

### PAT-004: Responsive Recomposition over Viewport Shrinking
- **Date:** 2026-09-16
- **Status:** APPROVED
- **Problem:** Traditional responsive design scales down desktop layouts proportionally, resulting in unreadable typography and unusable touch targets.
- **Decision:** Patterns must define explicit **recomposition rules** across `Compact` (<640px), `Standard` (640–1024px), `Wide` (1024–1440px), and `Full` (>1440px). In Compact mode, inline toolbars stack vertically, action buttons expand to full width or convert to bottom-anchored bars, and secondary metadata collapses.
- **Alternatives Considered:** Fluid CSS clamp scaling alone. Rejected: fluid typography does not solve spatial layout collision on mobile.
- **Evidence:** Mobile ergonomics and touch target requirements ($\ge 44 \times 44\text{px}$) demand structural layout shifts.

---

### PAT-005: RTL Inline-Axis Progression & Anti-Row-Reverse Invariant
- **Date:** 2026-09-16
- **Status:** APPROVED
- **Problem:** Developers frequently use `flex-direction: row-reverse` to flip horizontal layouts for Arabic/RTL, inverting keyboard DOM tab sequence relative to visual reading order.
- **Decision:** Strictly forbid `row-reverse` in pattern layouts. Layouts must rely on native inline-axis flow (`inline-start` $\to$ `inline-end`). Visual reading order and DOM traversal order must match 100% in both LTR and RTL viewports.
- **Alternatives Considered:** Allowing `row-reverse` with manual `tabindex` re-indexing. Rejected: violates WCAG 2.1/2.2 SC 2.4.3 (Focus Order) and creates severe screen-reader navigation bugs.
- **Evidence:** Tested and verified in PDR-009 and CDR-003.

---

### PAT-006: Contextual Experience State Matrix
- **Date:** 2026-09-16
- **Status:** APPROVED
- **Problem:** Attempting to force all 20+ theoretical MDS experience states onto every pattern creates unmaintainable bloat.
- **Decision:** Patterns must evaluate experience states contextually, classifying them as `Required`, `Optional`, or `Not Applicable`. For example, `Search-Filter-Bar` requires `Loading`, `Empty (No Results)`, and `Active Filter`; it does not require `Permission Denied` or `Deleted`.
- **Alternatives Considered:** Universal state attachment requirement. Rejected: leads to boilerplate documentation that fails real-world use.
- **Design Judgment:** Focused, domain-relevant states ensure reliable developer implementation.

---

### PAT-007: Algorithmic Pattern Selection Engine (PSE) Integration
- **Date:** 2026-09-16
- **Status:** APPROVED
- **Problem:** AI agents and engineers often assemble arbitrary component combinations instead of reusing established patterns.
- **Decision:** Establish the Pattern Selection Engine (PSE) as a deterministic decision model that maps: User Intent $\to$ Task Type $\to$ Information Density $\to$ State Needs $\to$ Candidate Evaluation $\to$ Selected Pattern.
- **Alternatives Considered:** Freeform pattern browsing. Rejected: non-deterministic for automated agents.
- **Evidence:** Algorithmic selection mirrors the successful DSSE model in `AGENT/DESIGN_SYSTEM_SELECTION_ENGINE.md`.

---

### PAT-008: Strict Deferral of Complex Enterprise Systems in Patterns
- **Date:** 2026-09-16
- **Status:** APPROVED
- **Problem:** Patterns for data presentation can easily creep into implementing heavy enterprise widgets (`DataGrid`, `RichTextEditor`, `Combobox`, `Calendar`).
- **Decision:** The 9 complex enterprise systems remain strictly deferred. Patterns that display tabular data must compose the static `Table` component with standard responsive pagination or horizontal scroll containers.
- **Alternatives Considered:** Implementing a lightweight mini-grid. Rejected: creates technical debt and compromises Phase 5 boundaries.
- **Evidence:** Reaffirmed from Master Specification Sections 11 & 34 and Phase 5 CDR-008.

---

### PAT-009: AI Composition Contract & Hallucination Guardrails
- **Date:** 2026-09-16
- **Status:** APPROVED
- **Problem:** Generative AI tools frequently invent custom padding, arbitrary flex values, and unapproved wrapper divs.
- **Decision:** Establish binding AI usage rules in Section 21 of every pattern. AI must follow the strict resolution hierarchy: `Existing Pattern` $\to$ `Existing Component Composition` $\to$ `Existing Primitives` $\to$ `Documented Extension Proposal`. AI must never output raw hex values or physical CSS margins.
- **Alternatives Considered:** Prompt guidelines without system-level constraints. Rejected: leads to drift across multiple AI agent sessions.
- **Evidence:** Codified in `AGENT/MDS_AGENT_RULES.md`.

---

### PAT-010: Pattern Lifecycle Governance & Deprecation Protocol
- **Date:** 2026-09-16
- **Status:** APPROVED
- **Problem:** Design systems accumulate zombie patterns that are no longer recommended or have been superseded by better UX paradigms.
- **Decision:** Codify an 8-stage lifecycle: `Proposed` $\to$ `Reviewed` $\to$ `Approved` $\to$ `Experimental` $\to$ `Beta` $\to$ `Stable` $\to$ `Deprecated` $\to$ `Removed`. Deprecated patterns must document replacement paths and remain functional for one major release cycle before removal.
- **Alternatives Considered:** Immediate deletion of deprecated patterns. Rejected: breaks existing downstream product code.
- **Design Judgment:** Predictable deprecation ensures enterprise stability and developer trust.
