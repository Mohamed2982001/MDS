# MDS Phase 9.6 — Implementation Decision Log (IDRs)

**Architecture Layer:** Layer 13 / Phase 9.6 (Reference Application Architecture)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Date:** 2026-09-21  
**Status:** **APPROVED & RATIFIED**  
**Governance:** Strict Non-Invention Policy — Architecture Definition Gate  

---

## Overview

This decision log documents the Architectural Decision Records (ADRs / IDRs) established during the **Phase 9.6 Reference Application Architecture Definition**. It strictly adheres to the principle:
> *"The Reference Application is an architectural validation instrument. It must prove that MDS works without turning itself into another design system."*

---

## Decision Index

- **IDR-011:** Reference Product Concept Selection — Fictional "MDS Workspace"
- **IDR-012:** Zero-Backend & Zero-Dependency Deterministic Mock Store
- **IDR-013:** 11-Screen Information Architecture & 100% Template Coverage
- **IDR-014:** Compositional Gap Policy — Compose over Invent
- **IDR-015:** AI Human-in-the-Loop 5-Stage Operational Topology
- **IDR-016:** Responsive App Shell & Responsive Recomposition Strategy
- **IDR-017:** Lightweight Deterministic State Management without Frameworks

---

### IDR-011: Reference Product Concept Selection — Fictional "MDS Workspace"

- **Status:** **APPROVED**
- **Context:**
  Phase 9.6 requires a realistic multi-screen product to test the compositional viability of MDS. Selecting a hyper-specific domain (e.g. medical telemetry, clinical trial CRM, or high-frequency crypto trading) introduces domain-specific baggage and non-transferable assumptions. Conversely, a trivial "To-Do" app fails to stress-test complex workflows, tables, permissions, and AI synthesis.
- **Decision:**
  Adopt a generic, high-density productivity and operations workspace called **"MDS Workspace"**. The product model encompasses:
  - Executive KPI dashboards
  - Entity lifecycle management (Items / Work Packages)
  - Workflow task tracking
  - AI-assisted synthesis and review
  - System activity and audit trails
  - Multi-tab workspace settings (General, Appearance, Notifications, Access)
- **Consequences:**
  - *Positive:* Provides adequate domain breadth to exercise all 6 canonical templates and 8 patterns in natural contexts.
  - *Positive:* Remains generic and universally understandable without business jargon.
  - *Constraint:* Domain logic must remain simulated; business rules must not eclipse design system validation.

---

### IDR-012: Zero-Backend & Zero-Dependency Deterministic Mock Store

- **Status:** **APPROVED**
- **Context:**
  A reference application could tempt developers to integrate REST/GraphQL backends, IndexedDB, Firebase, or Mock Service Worker (MSW) libraries, introducing external runtime dependencies and build toolchains.
- **Decision:**
  Enforce a **100% Frontend-Only, Zero-External-Dependency** architecture. All entity stores (`items`, `tasks`, `users`, `activity`, `settings`, `aiResults`) will be hosted in deterministic, in-memory JavaScript fixtures loaded from JSON.
- **Consequences:**
  - *Positive:* Zero npm/pip runtime packages. Runs instantaneously on any static file server or GitHub Pages.
  - *Positive:* 100% deterministic test execution and reproducibility.
  - *Boundary:* Network latency, offline mode, and error states will be simulated through intentional UI state toggles and deterministic timing promises.

---

### IDR-013: 11-Screen Information Architecture & 100% Template Coverage

- **Status:** **APPROVED**
- **Context:**
  The MDS specification defines exactly 6 canonical page templates (`Overview`, `List Management`, `Detail Entity`, `Form Edit`, `Settings Workspace`, `AI Workspace`). We must establish a concrete screen inventory that covers 100% of these templates while exercising real navigation transitions.
- **Decision:**
  Establish an 11-screen information architecture mapping directly to the 6 canonical templates:
  1. `Overview` $\to$ Dashboard Overview Template (`MDS-TMP-001`)
  2. `Items (List)` $\to$ List Management Template (`MDS-TMP-002`)
  3. `Item Detail` $\to$ Detail Entity Template (`MDS-TMP-003`)
  4. `Item Edit` $\to$ Form Edit Template (`MDS-TMP-004`)
  5. `Tasks` $\to$ Workflow-Oriented Management (`MDS-TMP-002` + `MDS-WKF-002`)
  6. `AI Workspace` $\to$ AI Workspace Template (`MDS-TMP-006`)
  7. `Activity` $\to$ Audit Trail Entity View (`MDS-TMP-003` variant)
  8. `Settings — General` $\to$ Form Edit Template (`MDS-TMP-004` / `MDS-TMP-005`)
  9. `Settings — Appearance` $\to$ Settings Workspace Template (`MDS-TMP-005`)
  10. `Settings — Notifications` $\to$ Settings Workspace Template (`MDS-TMP-005`)
  11. `Settings — Access` $\to$ Settings Workspace Template (`MDS-TMP-005`)
- **Consequences:**
  - Exactly 6/6 canonical templates are instantiated.
  - Zero unapproved templates are created.

---

### IDR-014: Compositional Gap Policy — Compose over Invent

- **Status:** **APPROVED**
- **Context:**
  When building a realistic application, common UI patterns like pagination, breadcrumbs, stat cards, or top navigation bars may appear "missing" from the 19 core components. Uncurated developer instinct is to immediately invent new components (`<mds-pagination>`, `<mds-navbar>`, `<mds-breadcrumbs>`).
- **Decision:**
  Enforce the **"Compose over Invent" Law**:
  1. Every UI need must be satisfied by composing existing primitives (`Stack`, `Inline`, `Grid`, `Container`, `Cluster`) and core components (`Button`, `IconButton`, `Link`, `Text`, `Badge`, `Card`).
  2. For example:
     - Pagination is composed of `Inline` + `IconButton` (`mds-icon-button--secondary`) + `Text`.
     - Breadcrumbs are composed of `Inline` + `Link` (`mds-link--subtle`) + `Text` separator.
     - Metric Stat Cards are composed of `Card` (`mds-card--raised`) + `Stack` + `Text--numeric` + `Badge`.
  3. If an undeniable systemic gap is identified, it must be logged in `Phase-9.6-Architecture-Gaps.md` for future governance review, rather than patched into the runtime.
- **Consequences:**
  - Guarantees zero component drift and zero token drift.
  - Validates whether the primitive layer is truly composable.

---

### IDR-015: AI Human-in-the-Loop 5-Stage Operational Topology

- **Status:** **APPROVED**
- **Context:**
  AI capabilities in enterprise applications risk autonomy runaway, screen reader disorientation, or destructive auto-commits.
- **Decision:**
  The AI Workspace screen must strictly implement the 5-Stage Human-in-the-Loop state model:
  $$\text{IDLE} \xrightarrow{\text{Prompt}} \text{PROCESSING} \xrightarrow{\text{Token Chunk}} \text{STREAMING} \xrightarrow{\text{Complete}} \text{REVIEW} \xrightarrow{\text{Action}} \text{RESOLVED}$$
  - **Decoupled LiveRegion (Finding AF-001):** Streaming token chunks are visual-only; screen reader announcements are throttled until generation reaches `REVIEW`.
  - **Human-as-Decider:** The system cannot auto-commit changes. The reviewer explicitly chooses: `Approve & Apply`, `Reject & Discard`, or `Refine & Retry`.
  - **Destructive Guard:** Consequential or overwriting actions trigger a `Confirmation-Dialog` pattern with cancel-first focus.
- **Consequences:**
  - Rigorous compliance with WCAG accessibility and safety directives.

---

### IDR-016: Responsive App Shell & Responsive Recomposition Strategy

- **Status:** **APPROVED**
- **Context:**
  Modern enterprise web applications must function across 320px (Mobile), 768px (Tablet), 1024px (Desktop), and 1440px (Wide). Traditional approaches simply shrink font sizes or hide columns randomly.
- **Decision:**
  Implement structural **Recomposition over Shrinking**:
  - **Desktop ($\ge 1024\text{px}$):** Persistent vertical sidebar navigation, multi-column form grids, expanded search-filter bars, full data tables.
  - **Tablet ($768\text{px} - 1023\text{px}$):** Compact sidebar, two-column form collapse, table horizontal scroll with shadow indicators.
  - **Mobile ($320\text{px} - 767\text{px}$):** Collapsed navigation accessible via top header trigger, single-column stacked forms, full-width action buttons, dialogs converted to bottom-sheet presentations.
- **Consequences:**
  - Layout transformation is driven entirely by CSS Media Queries and container queries, consuming token breakpoints (`1024px` / `1440px`).

---

### IDR-017: Lightweight Deterministic State Management without Frameworks

- **Status:** **APPROVED**
- **Context:**
  The application needs to track active screen, filter queries, mock data mutations, modal dialog visibility, active theme, and user permissions across 11 screens.
- **Decision:**
  Implement a lightweight, single-file Vanilla JS state store (`ReferenceStore`) using the Observer pattern:
  - **URL Hash Routing:** `#/[screen]` handles screen switching and browser history.
  - **Central State Object:** Holds immutable references to mock entities, filters, and current user role.
  - **Event Pub/Sub:** Components re-render locally upon state dispatch.
  - **Zero NPM Dependencies:** Pure modern JavaScript.
- **Consequences:**
  - No Redux, no Zustand, no React, no Vue. Pure web standards.
  - Extremely fast execution, fully auditable, zero external supply-chain risk.
