# MDS Phase 9.6 — Architectural Gap Detection & Composition Analysis

**Architecture Layer:** Layer 13 / Phase 9.6 (Reference Application Architecture)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Date:** 2026-09-21  
**Status:** **ACTIVE AUDIT LOG**  
**Governance:** Strict Non-Invention Policy — Document Gaps, Do Not Patch Runtime  

---

## 1. Executive Summary & Policy

During the architectural definition of the **MDS Workspace Reference Application**, complex enterprise screens (Dashboard, List Management, Detail Entity, Form Edit, Settings, and AI Workspace) were analyzed to determine whether the canonical 19 core components, 18 primitives, 8 patterns, and 6 templates provide 100% sufficient building blocks.

In accordance with the **Zero-Fabrication Mandate**:
> *"If an application need cannot be satisfied directly by MDS, developers and agents MUST NOT invent ad-hoc components or tokens. Every gap must be logged, categorized, and solved strictly through composition of existing primitives, or slated for formal post-v1.0 governance review."*

This document catalogs all 8 discovered architectural gaps, proves how they are cleanly resolved via **Composition over Invention** in Phase 9.6, and outlines proposed future enhancements for MDS v1.1.0+.

---

## 2. Architectural Gap Register

| Gap ID | Gap Name | Evidence from Real Screens | Severity | Existing MDS Coverage | Phase 9.6 Composition Strategy (No Inventions) | Proposed Future Action (v1.1.0+) |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **GAP-001** | **App Shell Header (Top Navigation Bar)** | Global persistent top bar needed across all 11 screens for Workspace branding, global search shortcut, role switcher, and user profile. | **Medium** | `Page-Header` pattern (`MDS-PAT-006`), `Container`, `Inline`, `Button`, `IconButton`, `Badge`. | Compose via `<header class="mds-container">` with `Inline` flex distribution containing branding, search trigger, and profile badge. | Formalize `App-Header` pattern in Layer 05 (`05-Patterns/Navigation/`). |
| **GAP-002** | **Table Pagination (Data Pager)** | High-throughput record management (`Items` list) requires pagination controls (previous/next, page numbers, page size). | **Medium** | `Table` focusable container (`AF-002`), `Select` for page size, `IconButton` for navigation, `Text` for status. | Compose footer bar using `Inline` + `IconButton` (`mds-icon-button--secondary`) + `Text` (`mds-text--numeric`) + native `Select`. | Formalize `Pagination` pattern in Layer 05 (`05-Patterns/Data/`). |
| **GAP-003** | **Breadcrumb Navigation Trail** | Hierarchical navigation paths (`Items` $\to$ `Item #104` $\to$ `Edit`) require clear location affordance. | **Low** | `Link` (`.mds-link--subtle`), `Text`, `Inline` primitive. | Compose within the header slot of `Page-Header` using `Inline` flex with `Link` items and slash `/` text separators. | Formalize `Breadcrumbs` component in Layer 04 or pattern in Layer 05. |
| **GAP-004** | **Metric KPI Stat Card** | Executive Dashboard Overview requires summary cards (Metric value, label, percentage delta, trend indicator). | **Low** | `Card` (`.mds-card--raised`), `Stack`, `Text` (`.mds-text--numeric`), `Badge` (`.mds-badge--success`). | Compose directly using `Card` with `Stack` layout: header label, large numeric text, and status badge with trend arrow. | Codify `Metric-Stat-Card` pattern in Layer 05 (`05-Patterns/Data/`). |
| **GAP-005** | **Global Toast Notification Queue** | Ephemeral non-modal feedback for asynchronous operations (Settings saved, Item archived, AI approved). | **Medium** | `Alert` component (`.mds-alert`), `--mds-layer-toast: 2000`, `VisuallyHidden`. | Render contextual alerts inside designated page notification shelves or sticky top containers using `Alert` and CSS transitions. | Design accessible `Toast` overlay controller in Layer 04 (`04-Components/Feedback/`). |
| **GAP-006** | **Responsive Off-Canvas Drawer** | Mobile viewports (<768px) require compact sidebar navigation and off-canvas filter panels. | **Medium** | `Dialog` (`<mds-dialog>`) with responsive bottom sheet (`<480px`), `Container`. | On mobile, navigation transforms into a full-screen or bottom-sheet overlay using `<mds-dialog>` with FocusTrap. | Formalize `Drawer` slide-over overlay component in Layer 04. |
| **GAP-007** | **Row Context Menu (Action Popover)** | Table rows require secondary actions (Duplicate, Export, Archive, Delete) without cluttering columns. | **Medium** | `IconButton` (`.mds-icon-button--ghost`), native `Select`, inline action buttons, `<mds-dialog>`. | Provide primary action buttons inline within the action cell; destructive operations trigger `<mds-dialog>`. | Formalize `Menu` / `Popover` floating overlay controller in Layer 04. |
| **GAP-008** | **Multi-Step Stepper / Wizard** | Multi-stage workflows (e.g. structured multi-step item creation or onboarding). | **Low** | `Tabs` (`<mds-tabs>`), `Badge`, `Inline`, `Stack`. | Compose using sequential step indicators rendered with `Badge` and `Tabs` panels with programmatic lockouts. | Codify `Stepper` pattern in Layer 05 (`05-Patterns/Navigation/`). |

---

## 3. Forensic Evaluation of Gap Severity

### 3.1 Why Zero Gaps are "Critical" (Blockers)
A gap is **Critical** only if an application cannot be constructed without inventing a new design token or violating an accessibility invariant.
- Every single gap above (GAP-001 through GAP-008) is **100% resolvable through the composition of existing MDS primitives and core components**.
- The parent-owned spacing law, CSS logical properties, Cairo typography, color palettes, and WAI-ARIA contracts remain completely uncompromised.

### 3.2 Verification of "Compose over Invent" Feasibility
- **Pagination:** `Inline` (gap: 8px) + `IconButton` (prev/next) + `Text` ("Page 1 of 12") provides an accessible, tactile paging interface that passes WCAG 2.1 AA without adding a single byte to the design system runtime.
- **KPI Cards:** `Card` (`--mds-elevation-level1`) + `Stack` (gap: 4px) + `Heading` (`--mds-font-size-2xl`) + `Badge` (`--mds-radius-full`) delivers a modern, executive dashboard card using pure MDS foundations.
- **Top Header:** `Container` + `Inline` provides a clean, responsive app shell header using existing layout primitives.

---

## 4. Governance Action Plan for Post-v1.0 Releases

Following the completion and lock of Phase 9.6, these 8 documented gaps will form the official candidate backlog for **MDS v1.1.0** (Next Minor Feature Release):

```text
MDS v1.1.0 Backlog Candidates (Post-Reference Audit):
├── Layer 04 Components:
│   ├── Drawer (Slide-Over Panel Overlay)
│   ├── Menu / Popover (Action Dropdown)
│   └── Toast (Floating Feedback Manager)
└── Layer 05 Patterns:
    ├── App-Header (Global Shell Navigation)
    ├── Pagination (Data Table Pager)
    ├── Breadcrumbs (Hierarchical Trail)
    ├── Metric-Stat-Card (KPI Summary Card)
    └── Stepper (Linear Multi-Step Workflow)
```

**Conclusion:** Phase 9.6 proceeds with **ZERO runtime modifications**, resolving all application requirements through composition.
