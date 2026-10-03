# Master Design System (MDS) — Template Composition Rules

**Document Layer:** 07-Templates / Composition Rules  
**Status:** APPROVED (Phase 8.1.3 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-17  

---

## 1. Executive Summary

This document establishes the **10 Inviolable Composition Laws** governing the assembly, structural boundaries, and usage of Layer 07 Templates in the Master Design System (MDS). Any template specification or product screen layout that violates these laws fails MDS architectural review.

---

## 2. The 10 Inviolable Composition Laws

```text
┌─────────────────────────────────────────────────────────────┐
│             10 INVIOLABLE TEMPLATE COMPOSITION LAWS         │
├─────────────────────────────────────────────────────────────┤
│ Law 1:  Templates Compose; They Do Not Reinvent            │
│ Law 2:  Template Owns Page-Level Composition               │
│ Law 3:  Business Content Is Injected via Slots             │
│ Law 4:  Workflow Intent Must Remain Visible                │
│ Law 5:  Responsive Recomposition Belongs to the Template   │
│ Law 6:  Page-Level States Remain Explicit & Contextual     │
│ Law 7:  Accessibility Is Structural & Invariant            │
│ Law 8:  RTL Preserves Semantic Reading & Focus Order       │
│ Law 9:  Templates Must Remain Domain-Neutral               │
│ Law 10: Avoid Template Explosion (The Parsimony Principle) │
└─────────────────────────────────────────────────────────────┘
```

---

### Law 1: Templates Compose; They Do Not Reinvent
A Template must be composed strictly from existing Layer 05 Patterns, Layer 06 Workflows, Layer 04 Components, Layer 03 Primitives, and Layer 02 Tokens. A Template must never define internal atomic controls, create ad-hoc styled wrappers, or introduce new design tokens. If a recurring UI structure is missing, it must be authored and approved at the Pattern or Component layer first.

### Law 2: Template Owns Page-Level Composition
The Template owns macro page spacing, container bounds (`container.lg: 1152px`, `container.xl: 1440px`), structural grid gutters, and regional positioning. Internal padding, margins, and layout rules within embedded components and patterns remain strictly owned by those lower layers. A template must never reach into a pattern to override internal margins (`!important` overrides or deep CSS selectors are prohibited).

### Law 3: Business Content Is Injected via Slots
Templates provide structural layout scaffolding and named slots (`slot="header"`, `slot="toolbar"`, `slot="primary"`, `slot="secondary"`, `slot="actions"`). Templates never hardcode product-specific business data, entity schemas, customer names, or database field lists. Business entities are injected by downstream product applications into the template's designated slots.

### Law 4: Workflow Intent Must Remain Visible
When a Template hosts a Layer 06 Workflow (e.g. `Form-Submission`, `Destructive-Action`, `AI-Synthesis-Review`), the behavioral progression, status banners, feedback spinners, and action triggers of that workflow must be prominently positioned in their primary regional slots. A template must never hide, clip, or obscure active workflow states or confirmation dialogs.

### Law 5: Responsive Recomposition Belongs to the Template
Page-level responsive adaptation is the sole responsibility of the Template. The Template dictates how regions reorganize across breakpoints (Mobile 320px $\to$ Tablet 768px $\to$ Desktop 1152px $\to$ Wide 1440px). Under the MDS philosophy of **Recomposition over Shrinking**, templates reorganize multi-column layouts into focused single-column stacks, convert sidebars to off-canvas sheets, and pin action bars to sticky bottom rails with $\ge 44\text{px}$ touch targets.

### Law 6: Page-Level States Remain Explicit & Contextual
Every Template must provide structural definitions for all relevant Layer 08 Experience States:
- **`Loading`:** Full-page structural skeleton matching real content geometry (avoiding blocking blank spinners).
- **`Empty`:** Explicit integration of the `Empty-State` pattern with diagnostic message and actionable recovery CTA.
- **`Error`:** Top-level error banner or full-view error card with non-destructive retry affordance.
- **`Access / Boundary`:** Contextual prompts for Authentication Required or Permission Denied.

### Law 7: Accessibility Is Structural & Invariant
Accessibility is an inherent structural property of the Template, not an afterthought:
1. Every Template must declare exactly one primary `<main>` landmark, with semantic `<header>`, `<footer>`, `<nav>`, and `<aside>` boundaries.
2. A single `<h1>` is mandated per template, located within the Page Header region.
3. Skip navigation (`Skip to main content`) must be supported at the top of the DOM.
4. Keyboard tab sequence must follow the natural logical visual reading order.

### Law 8: RTL Preserves Semantic Reading & Focus Order
Templates must maintain 100% bidirectional symmetry:
1. All spatial positioning must use CSS Logical Properties (`margin-inline`, `padding-inline`, `inset-inline-start`).
2. The use of `flex-direction: row-reverse` to force right-to-left layout is strictly prohibited, as it breaks the physical DOM tab order and violates WCAG 2.4.3 (Focus Order).
3. Primary content remains on the inline-start edge (`right` in RTL, `left` in LTR); secondary sidebars remain on the inline-end edge.

### Law 9: Templates Must Remain Domain-Neutral
Templates represent universal information architecture archetypes, not vertical product screens:
- **Prohibited:** `BillingInvoicePageTemplate`, `HospitalPatientRecordTemplate`, `ECommerceCheckoutTemplate`.
- **Approved:** `Detail-Entity Template` (which can render an invoice, a patient record, or an order), `Form-Edit Template` (which can render a checkout, a profile edit, or an intake form), `List-Management Template` (which can render products, patients, or transactions).

### Law 10: Avoid Template Explosion (The Parsimony Principle)
MDS strictly adheres to architectural parsimony. If two candidate templates differ only in action button text, minor slot arrangements, or business data types, **they are the same template**. Standalone templates must only be approved when they embody a genuinely distinct, recurring macro layout structure. The canonical set is strictly capped at 6–8 core templates.
