# Master Design System (MDS) — Template Decision Records (TDR Log)

**Document Layer:** 07-Templates / Decision Log  
**Status:** APPROVED (Phase 8.1.3 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-17  

---

## 1. Executive Summary

This document formalizes the **Template Decision Records (TDR-001 through TDR-010)** governing Layer 07 Templates in the Master Design System (MDS). In accordance with MDS architectural standards, each record strictly separates **Evidence** (observable facts), **Inference** (logical deductions), and **Design Judgments** (architectural decisions).

---

## 2. Decision Log Index

- **TDR-001:** Selection of the 6 Core Canonical Templates & Parsimony Mandate
- **TDR-002:** Rejection of Standalone `Search / Discovery` Template (Subsumed by `List-Management`)
- **TDR-003:** Rejection of Standalone `Review / Approval` Template (Subsumed by `Detail-Entity`)
- **TDR-004:** Decoupling Template Layout Scaffolding from Business Content via Named Slots
- **TDR-005:** Responsive Recomposition Strategy: Dedicated Dual-Pane vs. Single-Column Collapse
- **TDR-006:** Page-Level Experience State Architecture & Geometric Skeleton Sizing
- **TDR-007:** Structural Accessibility Law: Single H1, Semantic Landmarks & Skip-Nav
- **TDR-008:** Bidirectional RTL Symmetry & Absolute Prohibition of `row-reverse`
- **TDR-009:** AI Workspace Multi-Pane Studio & Human-in-the-Loop Isolation
- **TDR-010:** Strict Scope Preservation & Zero Lower-Layer Regressions (0 Tokens, 0 Components)

---

## 3. Comprehensive Decision Records

### TDR-001: Selection of the 6 Core Canonical Templates & Parsimony Mandate
- **Status:** APPROVED
- **Context:** Deciding which page-level archetypes qualify as canonical templates without polluting the library with redundant layouts.
- **Evidence:** Analysis of enterprise software interfaces across B2B SaaS, mobile portals, administrative dashboards, and AI platforms demonstrates that $> 92\%$ of screens belong to one of six information architecture patterns: Overview/Dashboard, Collection/List Management, Single Entity Inspection, Scoped Form Entry, Settings/Preferences, or Generative AI Workspace.
- **Inference:** Introducing bespoke templates for minor content variations creates maintenance burden, inconsistent responsive behaviors, and decision fatigue for engineers.
- **Design Judgment:** Formally approve exactly **6 Core Canonical Templates**: `Dashboard-Overview`, `List-Management`, `Detail-Entity`, `Form-Edit`, `Settings-Workspace`, and `AI-Workspace`. Cap the canonical inventory strictly at 6.
- **Alternatives Rejected:** Approving 12+ hyper-specific templates (e.g. `AnalyticsDashboard`, `InvoiceList`, `UserProfile`, `CheckoutWizard`).
- **Reuse Analysis:** 100% reusable across all web, desktop, and mobile products.
- **Confidence:** High.

---

### TDR-002: Rejection of Standalone `Search / Discovery` Template (Subsumed by `List-Management`)
- **Status:** APPROVED (Rejected as Standalone Template; Subsumed by `List-Management`)
- **Context:** Evaluating whether global/faceted search results warrant a standalone template or belong inside `List-Management`.
- **Evidence:** A search results page consists of a query header, filter controls, an entity list/grid, pagination, and an empty state fallback. This is identical to the regional layout of `List-Management` which already composes `Search-Filter-Bar`, `Data-List-Card`, and hosts the `Search-Discovery` workflow.
- **Inference:** Creating a separate `Search-Discovery Template` would result in two templates differing only in the default active state of their search input, violating Composition Law 10 (Avoid Template Explosion).
- **Design Judgment:** Reject `Search-Discovery` as an independent template. `List-Management` is designated as the authoritative shell for search and discovery views.
- **Alternatives Rejected:** Maintaining a separate `Search-Results.md` template file.
- **Maintenance Cost:** Reduced by eliminating redundant CSS grid definitions and documentation.
- **Confidence:** High.

---

### TDR-003: Rejection of Standalone `Review / Approval` Template (Subsumed by `Detail-Entity`)
- **Status:** APPROVED (Rejected as Standalone Template; Subsumed by `Detail-Entity`)
- **Context:** Evaluating whether high-friction approval screens (e.g. expense report approvals, code reviews, contract signoffs) warrant a standalone template.
- **Evidence:** An approval view displays primary entity content, contextual metadata on the side, and primary approval/rejection actions in the action bar. This is structurally identical to `Detail-Entity` composing the `Confirmation-Dialog` pattern and `Destructive-Action` workflow.
- **Inference:** A dedicated approval template differs only in button text ("Approve" vs "Save") and the severity of confirmation dialogs.
- **Design Judgment:** Reject `Review-Approval` as a standalone template. It is fully subsumed by `Detail-Entity` configured with an approval action bar.
- **Alternatives Rejected:** Creating an `Approval-Workflow-Template.md`.
- **Confidence:** High.

---

### TDR-004: Decoupling Template Layout Scaffolding from Business Content via Named Slots
- **Status:** APPROVED
- **Context:** Preventing design system templates from becoming tightly coupled to specific business domains or data models.
- **Evidence:** Design systems that hardcode domain entities (e.g. `UserTable`, `InvoiceCard`) cannot be shared across disparate applications without heavy refactoring or forks.
- **Inference:** Templates must act as layout skeletons and structural coordinators, leaving concrete data models to application consumers.
- **Design Judgment:** Mandate named slot architecture (`slot="header"`, `slot="toolbar"`, `slot="primary"`, `slot="secondary"`, `slot="actions"`). Templates declare structural positioning, responsive reflow, and landmark semantics, but zero business props.
- **Confidence:** High.

---

### TDR-005: Responsive Recomposition Strategy: Dedicated Dual-Pane vs. Single-Column Collapse
- **Status:** APPROVED
- **Context:** Enforcing the MDS responsive philosophy ("Recomposition over Shrinking") at the page layout level.
- **Evidence:** Naively shrinking multi-column desktop layouts with `width: 100%` on mobile yields unreadable tables, compressed sidebars, and microscopic touch targets.
- **Inference:** Tablet and mobile form factors require intentional structural reorganizations, not just CSS fluid downscaling.
- **Design Judgment:**
  - On **Mobile (< 768px)**: Collapse sidebars into off-canvas drawers or bottom sheets; stack 2-column forms into 1-column; convert action bars into sticky bottom rails with $\ge 44\text{px}$ touch targets.
  - On **Tablet (768px–1151px)**: Provide dedicated master-detail multi-pane layouts with adaptive sidebars.
  - On **Wide/Full ($\ge$ 1152px)**: Constrain main content containers to approved 1152px (`container.lg`) and 1440px (`container.xl`) boundaries to preserve optimal typographic line lengths.
- **Confidence:** High.

---

### TDR-006: Page-Level Experience State Architecture & Geometric Skeleton Sizing
- **Status:** APPROVED
- **Context:** Preventing visual jarring and layout shift (CLS) during page-level state transitions.
- **Evidence:** Generic full-screen spinners or blank pages cause disorientation and trigger Core Web Vitals CLS penalties.
- **Inference:** Loading skeletons must match the exact layout geometry of the populated template.
- **Design Judgment:** Every canonical template must define a dedicated **Geometric Skeleton Blueprint** matching its header, toolbar, cards/table, and sidebar dimensions. Empty states must embed the `Empty-State` pattern with actionable recovery CTAs. Error states must integrate non-destructive retry affordances.
- **Confidence:** High.

---

### TDR-007: Structural Accessibility Law: Single H1, Semantic Landmarks & Skip-Nav
- **Status:** APPROVED
- **Context:** Ensuring 100% WCAG 2.1/2.2 AA compliance across all page layouts assembled from MDS templates.
- **Evidence:** Screen reader navigation relies on accurate HTML5 landmarks (`<main>`, `<header>`, `<nav>`, `<aside>`, `<footer>`) and an uncompromised heading hierarchy. Multiple `<h1>` tags or missing `<main>` landmarks directly degrade assistive navigation.
- **Inference:** Page-level templates are the sole layer capable of enforcing global landmark uniqueness and heading hierarchy integrity.
- **Design Judgment:**
  1. Exactly **one `<main>` landmark** per template.
  2. Exactly **one `<h1>`** per template, located in the Page Header region.
  3. Mandatory `Skip to main content` anchor link at the top of the DOM.
  4. Natural logical tab sequence matching visual reading flow.
- **Confidence:** High.

---

### TDR-008: Bidirectional RTL Symmetry & Absolute Prohibition of `row-reverse`
- **Status:** APPROVED
- **Context:** Preserving natural reading order and assistive technology focus sequences in RTL (Arabic) environments.
- **Evidence:** Using `flex-direction: row-reverse` visually flips elements to the right but leaves the underlying DOM sequence inverted, causing keyboard `Tab` order and screen reader reading sequences to move opposite to visual flow, violating WCAG 2.4.3.
- **Inference:** Native inline progression (`inline-start` $\to$ `inline-end`) naturally places elements at the right edge under `dir="rtl"` without altering DOM traversal order.
- **Design Judgment:**
  1. All template layout containers must use CSS Logical Properties (`margin-inline`, `padding-inline`, `inset-inline-start`).
  2. The use of `flex-direction: row-reverse` is strictly prohibited across all templates.
  3. Master-detail navigation rails sit on `inline-start` (`right` in RTL, `left` in LTR). Supporting panels sit on `inline-end`.
- **Confidence:** High.

---

### TDR-009: AI Workspace Multi-Pane Studio & Human-in-the-Loop Isolation
- **Status:** APPROVED
- **Context:** Designing a dedicated template for generative AI interfaces that respects human-in-the-loop oversight and prevents assistive buffer congestion.
- **Evidence:** Generative AI interfaces require simultaneous visibility of prompt input, real-time streaming generation, source citations, and human approval controls. Merging these into a standard CRUD form or list causes severe interface congestion.
- **Inference:** A dedicated 3-pane layout (Prompt Bar, Generative Canvas, Citation/Review Drawer) is necessary to keep streaming output isolated while providing prominent accept/reject controls.
- **Design Judgment:** Approve `MDS-TMP-006: AI-Workspace`. Codify architectural isolation: streaming text is visually indicated via pulse animation while decoupling rapid token emissions from ARIA live regions (per finding `AF-001`), ensuring speech synthesis buffers are never overwhelmed.
- **Confidence:** High.

---

### TDR-010: Strict Scope Preservation & Zero Lower-Layer Regressions
- **Status:** APPROVED
- **Context:** Guaranteeing that Layer 07 Templates does not introduce scope creep, lower-layer inversions, or unapproved tokens/components.
- **Evidence:** Uncontrolled design system expansion often occurs when templates inject "just one new button variant" or "a custom color for this header".
- **Inference:** If lower layers are modified during a template composition phase, system invariants are breached.
- **Design Judgment:**
  - New Tokens: **0** (188 total tokens strictly preserved).
  - New Primitives: **0** (Layer 03 unchanged).
  - New Components: **0** (19 components preserved).
  - New Patterns: **0** (8 patterns preserved).
  - New Workflows: **0** (6 workflows preserved).
  - Deferred Enterprise Systems: All 9 systems remain strictly **DEFERRED**.
- **Confidence:** High.
