# MDS Phase 9.6 — Reference Application Architecture Specification

**Phase:** 9.6 (Reference Application Architecture Definition)  
**Layer:** 13-Implementation  
**Status:** **APPROVED ARCHITECTURE SPECIFICATION**  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Date:** 2026-09-21  
**Target Consumer:** Phase 9.6 Reference Application (`MDS/Reference-Application/`)  
**Companion Documents:**
- [`Phase-9.6-Architecture-Gaps.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/13-Implementation/Phase-9.6-Architecture-Gaps.md)
- [`Phase-9.6-Decision-Log.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/13-Implementation/Phase-9.6-Decision-Log.md)

---

## 1. Purpose

The Reference Application is the first complete, realistic enterprise web application built strictly as a consumer of the Master Design System (MDS).

Its fundamental architectural mission is to provide an unambiguous, verifiable answer to the core question:
> *"Can the MDS support a realistic modern enterprise application across all views, workflows, and viewports without requiring the application to invent its own design system, patch component CSS, or bypass architectural rules?"*

The Reference Application serves as the **supreme validation vehicle** for the complete compositional chain:
```text
MDS Core Tokens (Layer 02)
       ↓
MDS Primitives (Layer 03)
       ↓
MDS Core Components (Layer 04)
       ↓
MDS Patterns (Layer 05)
       ↓
MDS Workflows (Layer 06)
       ↓
MDS Templates (Layer 07)
       ↓
MDS Workspace Reference Application (Phase 9.6)
```

---

## 2. Scope & Boundaries

### 2.1 What the Reference Application IS
- **A Realistic Application:** Mimics genuine operations, metrics, records, forms, and workflows.
- **An Unprivileged Consumer:** Treats `MDS/Runtime/` as a strict, read-only external library.
- **A Compositional Testbed:** Proves that complex layouts arise naturally from primitives and patterns.
- **A Workflow Validation Engine:** Executes all 6 canonical workflows and their underlying state transitions.
- **A Multi-Axis Testing Lab:** Simultaneously exercises RTL, Themes, Density, Responsive Recomposition, and Accessibility.
- **Intentionally Generic:** Structured to serve as a reusable architectural template for any future web or Flutter product.

### 2.2 What the Reference Application IS NOT
- **NOT a commercial SaaS product:** No real billing, no actual authentication backends, no production databases.
- **NOT a marketing website:** Zero decorative hero banners, promotional carousels, or uncurated eye candy.
- **NOT a duplicate Playground:** The Playground tests *isolated components*; the Reference Application tests *composite systems*.
- **NOT a place to invent design decisions:** Zero new color tokens, zero new font sizes, zero custom component classes.
- **NOT the source of truth for MDS:** If an application need clashes with an MDS rule, the application must adapt or file a gap record.

---

## 3. Product Concept — "MDS Workspace"

The application models a modern, unified operations and productivity suite named **MDS Workspace**.

### Domain Scope:
MDS Workspace provides team collaboration, entity tracking, workflow orchestration, and AI synthesis across four operational pillars:
1. **Intelligence & Insights:** Executive dashboards, operational KPIs, and audit trails.
2. **Operations & Registry:** Tabular record management, batch filtering, entity details, and form workflows.
3. **Execution & Workflows:** Task lifecycles, assignment states, and safe destructive actions.
4. **AI-Assisted Synthesis:** Human-in-the-loop document summarization, drafting, and result review.

---

## 4. User Model (Conceptual Roles)

To validate permission states and security boundaries without building an actual backend, the application defines 4 conceptual roles selectable via the workspace switcher:

| Conceptual Role | Scope & Permissions | Key Interactive Triggers |
| :--- | :--- | :--- |
| **User (Standard)** | Read-only access to most views; can create items; can run AI prompts; cannot delete entities. | Triggering a delete action simulates `Permission Denied` state. |
| **Manager** | Full read/write access to items and tasks; can assign tasks and approve workflows. | Exercises assignment dropdowns, batch edits, and status transitions. |
| **Reviewer** | Specialized authority over AI synthesis outputs; can approve or reject AI generated artifacts. | Exercises the `AI-Result-Review` pattern and human sign-off flows. |
| **Administrator** | Master authority; can access workspace settings, change access control, and execute destructive operations. | Exercises destructive confirmation dialogs and security settings. |

---

## 5. Information Architecture

The application adopts a clean, hierarchical information architecture structured into 6 primary operational sections:

```text
MDS Workspace
│
├── 1. Overview                    (Dashboard Overview Template)
│
├── 2. Items                       (List Management & Detail Templates)
│   ├── 2.1 All Items              (Primary Data Table)
│   ├── 2.2 Favorites              (Filtered Sub-view)
│   └── 2.3 Archived               (Archived State Records)
│
├── 3. Tasks                       (Workflow Task Management)
│
├── 4. AI Workspace                (AI Human-in-the-Loop Canvas)
│
├── 5. Activity                    (Chronological Audit Trail)
│
└── 6. Settings                    (Settings Workspace Template)
    ├── 6.1 General                (Profile & Workspace Preferences)
    ├── 6.2 Appearance             (Themes, Presets, Density, RTL)
    ├── 6.3 Notifications          (Communication Toggles)
    └── 6.4 Access & Security      (Roles, Permissions, Danger Zone)
```

---

## 6. Screen Inventory (11 Canonical Screens)

### 6.1 Screen 1: Overview (`#/overview`)
- **Template:** `Dashboard Overview` (`MDS-TMP-001`).
- **Archetype:** High-density executive operational summary.
- **Composition:**
  - `Page-Header` pattern with workspace title, date badge, and "New Item" action button.
  - KPI Metric Grid: 4 composed stat cards (Total Items, Pending Tasks, AI Savings, Health Score).
  - Main Body: Two-column responsive split (`Stack` & `Grid`):
    - Left Pane: Priority task list (`Data-List-Card` pattern).
    - Right Pane: Recent system activity feed (`Activity` summary).
- **Experience States:** Populated metrics vs Skeleton loading state; error recovery banner.

### 6.2 Screen 2: Items — List Management (`#/items`)
- **Template:** `List Management` (`MDS-TMP-002`).
- **Archetype:** High-throughput data exploration and batch operations.
- **Composition:**
  - `Page-Header` with primary action button (`+ Create Item`).
  - `Search-Filter-Bar` pattern: text search input with prefix icon, status filter (`Select`), category chips (`Cluster`).
  - Canonical `Table` component with striped rows, status badges, right-aligned monetary values (`tabular-nums`), and focusable scroll container (`AF-002`).
  - Table footer pager composed via `Inline` + `IconButton` + `Text`.
- **Experience States:** Populated table, Empty search results (`Empty-State` pattern), loading shimmer, error state.
- **Workflow:** Executes **Search & Discovery Workflow** (`MDS-WKF-002`).

### 6.3 Screen 3: Item Detail (`#/items/detail`)
- **Template:** `Detail Entity` (`MDS-TMP-003`).
- **Archetype:** Deep single-entity inspection and governance.
- **Composition:**
  - `Page-Header` with back link (breadcrumb affordance), entity title, status badge, and action group (`Edit`, `Archive`, `Delete`).
  - Two-column layout:
    - Primary Pane: Tabbed content container (`Tabs`: Overview, Specifications, History).
    - Secondary Sidebar: Entity metadata card (Owner avatar, created timestamp, classification).
- **Experience States:** Populated entity, Not Found (`Empty-State` 404), Deleted / Archived state.
- **Workflow:** Triggers **Destructive Action Workflow** (`MDS-WKF-003`) via Delete button.

### 6.4 Screen 4: Item Edit (`#/items/edit`)
- **Template:** `Form Edit` (`MDS-TMP-004`).
- **Archetype:** Structured multi-field data entry and entity mutation.
- **Composition:**
  - `Page-Header` with "Unsaved Changes" indicator.
  - Form organized into two `Form-Section` patterns:
    - Section 1: Basic Information (Title `Input`, Category `Select`, Description `Textarea` with softWrap).
    - Section 2: Configuration & Settings (`Checkbox` toggles, `Radio` group, active `Switch`).
  - Sticky bottom action bar (`Button` Secondary Cancel, `Button` Primary Save).
- **Experience States:** Clean state, Dirty state (unsaved warning), Validating state, Error banner state.
- **Workflow:** Executes **Form Submission Workflow** (`MDS-WKF-001`).

### 6.5 Screen 5: Tasks (`#/tasks`)
- **Template:** `List Management` (`MDS-TMP-002`) & Workflow Engine.
- **Archetype:** Task lifecycle tracking and assignment.
- **Composition:**
  - Status column tabs (`Tabs`: All, In Progress, Review, Completed).
  - Task card list composed using `Data-List-Card` patterns with priority badges, assignee tags, and due dates.
  - Inline action toggles to advance task state (`Start` $\to$ `Complete`).
- **Experience States:** Active tasks vs Empty queue (`Empty-State` pattern).

### 6.6 Screen 6: AI Workspace (`#/ai-workspace`)
- **Template:** `AI Workspace` (`MDS-TMP-006`).
- **Archetype:** Human-in-the-loop AI canvas.
- **Composition:**
  - Split-pane layout:
    - Top/Input Pane: `AI-Input-Prompt` pattern with multi-line prompt textarea, model selector (`Select`), token count indicator (`Text--numeric`), and "Synthesize" button.
    - Bottom/Output Pane: `AI-Result-Review` pattern with streaming token indicator, confidence badge, metadata tag, and approval buttons (`Approve & Apply`, `Reject & Discard`, `Retry`).
  - Integrated `LiveRegion` announcer ensuring non-intrusive screen reader updates (`AF-001`).
- **Workflow:** Executes **AI Synthesis Review Workflow** (`MDS-WKF-005`).

### 6.7 Screen 7: Activity (`#/activity`)
- **Template:** `Detail Entity` / Audit Log (`MDS-TMP-003`).
- **Archetype:** Chronological event timeline and security audit.
- **Composition:**
  - `Page-Header` with event filter dropdown.
  - Vertical timeline stack composed of `Card` items, timestamp numerics (`tabular-nums`), actor names (`Text`), and action badges.
- **Experience States:** Loaded timeline vs Empty history.

### 6.8 Screen 8: Settings — General (`#/settings/general`)
- **Template:** `Settings Workspace` (`MDS-TMP-005`).
- **Archetype:** Core system configuration.
- **Composition:**
  - Form section with Workspace Name (`Input`), Default Language (`Select`), Team Timezone (`Select`).
  - Auto-save / explicit save toggle.
- **Workflow:** Executes **Settings Update Workflow** (`MDS-WKF-004`).

### 6.9 Screen 9: Settings — Appearance (`#/settings/appearance`)
- **Template:** `Settings Workspace` (`MDS-TMP-005`).
- **Archetype:** Live runtime system personalization.
- **Composition:**
  - Radio group cards for Themes: Light, Dark, High Contrast.
  - Radio group cards for Presets: Soft Modern, Refined Minimal, Expressive.
  - Radio group for Density: Comfortable (40px) vs Compact (32px), with Dense (28px) visibly disabled and tagged `[Deferred]`.
  - Direction switcher: LTR vs RTL with Cairo font preview.
- **Implementation:** Directly dispatches runtime DOM attributes (`data-theme`, `data-preset`, `data-density`, `dir`).

### 6.10 Screen 10: Settings — Notifications (`#/settings/notifications`)
- **Template:** `Settings Workspace` (`MDS-TMP-005`).
- **Archetype:** Communication preferences.
- **Composition:**
  - Grouped setting rows composed of `Switch` controls for Email Digest, Security Alerts, Task Mentions.
  - Frequency selector (`Radio` group).

### 6.11 Screen 11: Settings — Access & Security (`#/settings/access`)
- **Template:** `Settings Workspace` (`MDS-TMP-005`).
- **Archetype:** Role management and destructive boundary.
- **Composition:**
  - Role management table (`Table` with User, Role, Status, and Action).
  - Danger Zone panel (`Card` with destructive border) offering "Delete Workspace".
  - Triggering delete opens canonical `<mds-dialog>` with Cancel-first initial focus (`AF-002`).

---

## 7. Canonical Template Mapping (6/6 Covered)

| Canonical Template | Spec ID | Reference Application Screen | Primary Purpose |
| :--- | :---: | :--- | :--- |
| **Dashboard Overview** | `MDS-TMP-001` | **Screen 1: Overview** (`#/overview`) | High-level metrics, priority tasks, executive summary. |
| **List Management** | `MDS-TMP-002` | **Screen 2: Items List** (`#/items`) & **Screen 5: Tasks** (`#/tasks`) | High-throughput search, tabular browsing, batch selection. |
| **Detail Entity** | `MDS-TMP-003` | **Screen 3: Item Detail** (`#/items/detail`) & **Screen 7: Activity** | Deep entity inspection, metadata tabs, audit log. |
| **Form Edit** | `MDS-TMP-004` | **Screen 4: Item Edit** (`#/items/edit`) | Multi-field structured input, field validation, save bar. |
| **Settings Workspace**| `MDS-TMP-005` | **Screens 8–11: Settings Sub-screens** (`#/settings/*`) | Multi-tab preferences, themes, notifications, access control. |
| **AI Workspace** | `MDS-TMP-006` | **Screen 6: AI Workspace** (`#/ai-workspace`) | Prompt composition, streaming generation, review & sign-off. |

*Coverage: Exactly 6 of 6 canonical templates are fully utilized.*

---

## 8. Canonical Pattern Mapping (8/8 Covered)

| Canonical Pattern | Spec ID | Screen Where Exercised | Concrete UI Composition |
| :--- | :---: | :--- | :--- |
| **1. Form-Section** | `MDS-PAT-001` | `Item Edit`, `Settings General`, `Settings Access` | Grouped field container with title, description, and responsive grid. |
| **2. Search-Filter-Bar** | `MDS-PAT-002` | `Items List`, `Tasks` | Search input, filter dropdowns, and category filter chips (`Cluster`). |
| **3. Data-List-Card** | `MDS-PAT-003` | `Overview` (Task List), `Tasks`, `Activity` | Interactive entity card with title, badge, metadata, and status action. |
| **4. Empty-State** | `MDS-PAT-004` | `Items List` (0 results), `Tasks` (empty), `404 Item` | Centered icon, heading, descriptive text, and recovery action button. |
| **5. Confirmation-Dialog**| `MDS-PAT-005`| `Item Detail` (Delete), `Settings Access` (Danger) | `<mds-dialog>` modal with AF-002 Cancel-first focus safety. |
| **6. Page-Header** | `MDS-PAT-006` | All 11 Screens | Title, subtitle, breadcrumb trail, and primary action slot. |
| **7. AI-Input-Prompt** | `MDS-PAT-007` | `AI Workspace` | Textarea prompt input, model selector, token count, synthesize button. |
| **8. AI-Result-Review** | `MDS-PAT-008` | `AI Workspace` | Result card, confidence badge, metadata tag, approve/reject buttons. |

*Coverage: Exactly 8 of 8 canonical patterns are actively employed.*

---

## 9. Canonical Workflow Mapping (6/6 Covered)

| Canonical Workflow | Spec ID | Trigger Screen | Underlying State Machine Transitions |
| :--- | :---: | :--- | :--- |
| **1. Form Submission** | `MDS-WKF-001` | `Item Edit` | $\text{IDLE} \to \text{ACTIVE\_INPUT} \to \text{VALIDATING} \to \text{PROCESSING} \to \text{SUCCESS\_RESOLVED}$ |
| **2. Search & Discovery** | `MDS-WKF-002` | `Items List` | $\text{IDLE} \to \text{ACTIVE\_INPUT} \to \text{PROCESSING} \to \text{EMPTY} \lor \text{SUCCESS\_RESOLVED}$ |
| **3. Destructive Action** | `MDS-WKF-003` | `Item Detail` (Delete) | $\text{IDLE} \to \text{CONFIRMING (Cancel Focus)} \to \text{PROCESSING} \to \text{SUCCESS\_RESOLVED}$ |
| **4. Settings Update** | `MDS-WKF-004` | `Settings General` | $\text{IDLE} \to \text{ACTIVE\_INPUT} \to \text{PROCESSING (Optimistic)} \to \text{SUCCESS\_RESOLVED}$ |
| **5. AI Synthesis Review**| `MDS-WKF-005` | `AI Workspace` | $\text{IDLE} \to \text{PROCESSING} \to \text{STREAMING} \to \text{REVIEWING} \to \text{RESOLVED}$ |
| **6. Error Recovery** | `MDS-WKF-006` | `Item Edit` / `AI Workspace` | $\text{PROCESSING} \to \text{ERROR\_INTERCEPTED} \xrightarrow{\text{Fix / Retry}} \text{PROCESSING} \to \text{SUCCESS}$ |

*Coverage: Exactly 6 of 6 canonical workflows are natively supported.*

---

## 10. Experience State Taxonomy Mapping

The Reference Application intentionally models the 6 canonical experience state families:

```text
                                Experience States
  ┌───────────────┬───────────────┼───────────────┬───────────────┬───────────────┐
  ▼               ▼               ▼               ▼               ▼               ▼
1. Data        2. Access       3. Resource     4. Process      5. Recovery     6. Additional
- Loading      - No Access     - Not Found     - Processing    - Retry         - Offline
- Refreshing   - Forbidden     - Deleted       - Pending       - Undo          - Conflict
- Empty        - Auth Req      - Archived      - Completed     - Fix           - Dirty/Unsaved
- Partial                                      - Failed        - Restore
- Success
- Error
```

- **Simulation Triggers:** The application provides an unobtrusive "Simulation Bar" in the bottom footer allowing the tester to force specific states (e.g. `Simulate Network Error`, `Simulate Empty State`, `Simulate Permission Denied`) to observe graceful UI degradation and contextual recovery buttons.

---

## 11. Responsive Recomposition Strategy

Following the inviolable law: **"Recomposition over Shrinking"**, the layout adapts structurally across four standardized breakpoint classes:

| Viewport Class | Breakpoint Range | Navigation Layout | Content Layout | Form Layout | Table Behavior | Dialog Behavior |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- |
| **Mobile** | $320\text{px} - 767\text{px}$ | Top bar + slide-down navigation menu | Single-column linear stack | 1-column vertical fields | Horizontal swipe container (`tabindex="0"`) | Responsive bottom sheet (`<480px`) |
| **Tablet** | $768\text{px} - 1023\text{px}$ | Slim/iconized vertical navigation | Two-column responsive grid | 2-column compact grid | Full table with scroll container | Centered modal ($400\text{px}$) |
| **Desktop** | $1024\text{px} - 1439\text{px}$| Expanded vertical sidebar (260px) | Multi-column dashboard grid | 2-column standard grid | Full visible columns | Centered modal ($560\text{px}$) |
| **Wide** | $\ge 1440\text{px}$ | Persistent sidebar + container max 1440px | High-density multi-column | Multi-section horizontal | Full visible with inline actions | Centered modal ($720\text{px}$) |

---

## 12. RTL & Bidirectional Architecture

- **Root Directionality:** Controlled via `dir="rtl"` (Arabic default) and `dir="ltr"` (English).
- **Typography:** Cairo font universally applied across Arabic and Latin texts.
- **100% CSS Logical Properties:** Layout positioning relies solely on:
  - `margin-inline`, `margin-block`
  - `padding-inline`, `padding-block`
  - `inset-inline-start`, `inset-inline-end`, `inset-block-start`, `inset-block-end`
  - `border-inline-start`, `border-inline-end`
  - `text-align: start` and `text-align: end`
- **Zero Row-Reverse:** Zero functional `row-reverse` hacks (WCAG 2.4.3 focus order protection).
- **Icon Mirroring:** Directional navigation chevrons mirror via `.mds-icon--rtl-mirror`; status and static icons remain non-mirrored.

---

## 13. Multi-Dimensional Theme Architecture

The Reference Application strictly consumes the 4 thematic dimensions established in MDS Layer 02:

1. **Luminance Modes:** `light` (default), `dark` (`--mds-color-surface-canvas: #090D16`), `high-contrast` (2px black boundaries).
2. **Visual Presets:** `soft` (signature 10px radius, subtle shadows), `refined` (6px radius, flat elevation), `expressive` (vibrant accents).
3. **Density Tiers:** `comfortable` (40px control height, 16px gaps) vs `compact` (32px control height, 12px gaps).
4. **Deferred Tier:** `dense` (28px) remains strictly **DEFERRED** and is disabled in UI controls.

---

## 14. Accessibility Architecture (WCAG 2.1 AA/AAA)

1. **Semantic Landmarks:** `<header role="banner">`, `<nav aria-label="...">`, `<main id="main-content">`, `<aside role="complementary">`, `<footer role="contentinfo">`.
2. **Keyboard Focus:** High-visibility 2px solid focus ring (`var(--mds-color-focus-ring)`) with 2px offset on all interactive elements. Skip navigation link provided.
3. **Table Accessibility (AF-002):** Table scroll container declares `tabindex="0"`, `role="region"`, and an accessible label.
4. **Dialog Safety (AF-002):** Destructive confirmation modals land initial focus on the `Cancel` button. Focus is trapped using `FocusTrap`.
5. **AI Streaming Throttling (AF-001):** Streaming token generation does not overwhelm the screen reader rotor; final summary is announced via `aria-live="polite"`.
6. **Touch Ergonomics:** Minimum $44 \times 44\text{px}$ touch target hit area under `@media (pointer: coarse)` via `.mds-press-target`.

---

## 15. Data Strategy (Frontend Deterministic Store)

All application data is hosted in a clean, local, deterministic JSON fixture repository:
- `fixtures/items.json`: 15 realistic operational items (ID, Title, Category, Priority, Owner, Status, UpdatedDate).
- `fixtures/tasks.json`: 12 task cards with lifecycle states (`TODO`, `IN_PROGRESS`, `REVIEW`, `DONE`).
- `fixtures/activities.json`: 10 chronological system event entries with timestamps and avatars.
- `fixtures/ai_mock_corpus.json`: Deterministic AI generation chunks and review outputs.
- `fixtures/users.json`: 4 mock users representing the conceptual roles.

Zero backend servers, zero database connections, zero external REST APIs.

---

## 16. Application State Strategy (Vanilla Store)

- **Routing:** Handled via hash-based routing (`window.location.hash`).
- **Store Architecture:** A single-file observer store (`ReferenceStore`) managing:
  - `currentRoute`: Active screen identifier.
  - `activeRole`: Current user permission persona.
  - `entities`: Filtered/mutated collections of items and tasks.
  - `simulatedState`: Active forced experience state (Normal, Loading, Network Error, Empty).
- **Zero Frameworks:** Pure modern JavaScript. Zero state management libraries.

---

## 17. AI Strategy (Human-in-the-Loop)

The AI Workspace strictly adheres to the 5-stage human-in-the-loop workflow:
```text
1. IDLE: User inputs prompt instructions into AI-Input-Prompt.
    ↓
2. PROCESSING: System indicates generation via Spinner and aria-busy="true".
    ↓
3. STREAMING: Text chunks appear in UI; LiveRegion is throttled (AF-001).
    ↓
4. REVIEW: Generation completes; UI presents AI-Result-Review card with confidence score.
    ↓
5. DECISION: Human explicitly chooses:
   ├── [Approve & Apply] → Commits changes to workspace items.
   ├── [Reject & Discard] → Discards output without side-effects.
   └── [Refine & Retry] → Reopens prompt with previous parameters retained.
```

---

## 18. Application Navigation Strategy

Navigation is constructed strictly using MDS primitives and components:
- **Desktop ($\ge 1024\text{px}$):** Vertical navigation panel composed of `Container` + `Stack` + `Link` (`.mds-link--subtle`) + `Badge`.
- **Mobile ($< 768\text{px}$):** Header hamburger button triggers a compact navigation sheet composed via `<mds-dialog>` or top dropdown.
- **No Inventions:** Avoids creating an ad-hoc `<mds-navbar>` or `<mds-drawer>` component, honoring the "Compose over Invent" rule.

---

## 19. Governance Boundaries & The "No New Design System" Rule

The Reference Application is an unprivileged consumer:
- **Zero New Tokens:** Must not introduce any new CSS custom properties or token aliases.
- **Zero New Primitives:** Must not create new layout wrappers.
- **Zero Component Overrides:** Must not alter component padding, border-radius, or colors in custom CSS.
- **Any Gaps Discovered:** Must be logged in [`Phase-9.6-Architecture-Gaps.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/13-Implementation/Phase-9.6-Architecture-Gaps.md) rather than patched in code.

---

## 20. Complete Mapping Matrix

| Screen | Canonical Template | Canonical Patterns | Canonical Workflow | Core Components Composed | Experience States Exercised | Responsive Recomposition | RTL Behavior | Theme Support |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Overview** | Dashboard Overview (`MDS-TMP-001`) | `Page-Header`, `Data-List-Card` | Dashboard Monitoring | `Card`, `Button`, `Badge`, `Spinner`, `Skeleton`, `Table` | Loading, Populated, Partial, Error | 4-col $\to$ 2-col $\to$ 1-col stack | Symmetrical, Cairo, Logical gaps | Light, Dark, High-Contrast, Presets |
| **2. Items List** | List Management (`MDS-TMP-002`) | `Page-Header`, `Search-Filter-Bar`, `Empty-State` | Search & Discovery (`MDS-WKF-002`) | `Table`, `Input`, `Select`, `Button`, `IconButton`, `Badge` | Empty, Loading, Populated, Filtered | Full table $\to$ horizontal scroll (`tabindex="0"`) | Symmetrical inline padding, chevron flips | Light, Dark, High-Contrast, Presets |
| **3. Item Detail** | Detail Entity (`MDS-TMP-003`) | `Page-Header`, `Confirmation-Dialog` | Destructive Action (`MDS-WKF-003`) | `Tabs`, `Card`, `Badge`, `Button`, `IconButton`, `Dialog` | Populated, Not Found (404), Deleted | Two-pane split $\to$ stacked single column | Symmetrical tabs, logical border-inline | Light, Dark, High-Contrast, Presets |
| **4. Item Edit** | Form Edit (`MDS-TMP-004`) | `Page-Header`, `Form-Section` | Form Submission (`MDS-WKF-001`) | `Field`, `Input`, `Textarea`, `Select`, `Checkbox`, `Radio`, `Switch`, `Button` | Clean, Dirty (Unsaved), Validating, Error | 2-col field grid $\to$ 1-col vertical stack | Logical label alignment (`start`), RTL switch | Light, Dark, High-Contrast, Presets |
| **5. Tasks** | List Management (`MDS-TMP-002`) | `Page-Header`, `Data-List-Card`, `Empty-State` | Task Lifecycle Transition | `Tabs`, `Card`, `Badge`, `Button`, `Checkbox` | Empty task queue, In-progress, Completed | Column grid $\to$ vertical card list | Symmetrical tag layout, Arabic labels | Light, Dark, High-Contrast, Presets |
| **6. AI Workspace** | AI Workspace (`MDS-TMP-006`) | `Page-Header`, `AI-Input-Prompt`, `AI-Result-Review` | AI Synthesis Review (`MDS-WKF-005`) | `Field`, `Textarea`, `Select`, `Button`, `Card`, `Badge`, `Spinner`, `Alert` | Idle, Processing, Streaming, Review, Approved | Split canvas $\to$ stacked prompt/review cards | Symmetrical prompt layout, RTL live region | Light, Dark, High-Contrast, Presets |
| **7. Activity** | Detail Entity (`MDS-TMP-003`) | `Page-Header`, `Data-List-Card` | Audit Exploration | `Card`, `Badge`, `Text`, `Select` | Populated timeline, Empty history | Timeline width scales smoothly | Logical timeline border, right-aligned dates | Light, Dark, High-Contrast, Presets |
| **8. Settings Gen** | Settings Workspace (`MDS-TMP-005`) | `Page-Header`, `Form-Section` | Settings Update (`MDS-WKF-004`) | `Field`, `Input`, `Select`, `Button`, `Alert` | Unsaved, Saving (Optimistic), Saved | 2-col grid $\to$ 1-col stack | Logical text alignment, start padding | Light, Dark, High-Contrast, Presets |
| **9. Settings App** | Settings Workspace (`MDS-TMP-005`) | `Page-Header`, `Form-Section` | Live Theme Application | `Card`, `Radio`, `Button`, `Badge` | Dynamic theme change | Theme card grid $\to$ stacked radio cards | Dynamic LTR/RTL live inversion | Real-time token updates |
| **10. Settings Notif**| Settings Workspace (`MDS-TMP-005`)| `Page-Header`, `Form-Section` | Notification Preference | `Switch`, `Checkbox`, `Radio`, `Button` | Instant toggle updates | Setting rows stack cleanly | Logical switch translation inversion | Light, Dark, High-Contrast, Presets |
| **11. Settings Acc** | Settings Workspace (`MDS-TMP-005`) | `Page-Header`, `Form-Section`, `Confirmation-Dialog`| Role Management & Danger Zone | `Table`, `Select`, `Button`, `Dialog`, `Alert` | Permission Denied, Admin Authorized | Table horizontal scroll, dialog bottom-sheet | Logical table headers, Cancel-first focus | Light, Dark, High-Contrast, Presets |

---

## 21. Success Criteria (11 Dimensions)

1. **Compositional Integrity:** All 11 screens assemble naturally from the 19 core components and 18 primitives without requiring custom CSS overrides.
2. **100% Template Realization:** Exactly 6 of 6 canonical templates are rendered in real, functional contexts.
3. **100% Pattern Realization:** Exactly 8 of 8 canonical patterns are actively utilized.
4. **100% Workflow Realization:** All 6 canonical workflows execute deterministically from start to resolution.
5. **State Naturalness:** Experience states (empty, loading, partial, error) trigger and recover seamlessly.
6. **Responsive Recomposition:** Recomposition over shrinking verified across 320px, 768px, 1024px, and 1440px.
7. **Bilingual Symmetry:** Flawless RTL rendering under Cairo font with zero physical directional properties and zero row-reverse.
8. **Theme Agility:** Real-time toggling of Light, Dark, and High Contrast with Refined and Soft Modern presets without visual defects.
9. **Accessibility Preservation:** FocusTrap, 2px FocusRing, PressTarget 44px, Cancel-first dialog focus, and throttled LiveRegion function flawlessly during multi-component composition.
10. **Human-in-the-Loop AI:** The AI Workspace strictly adheres to non-autonomous human review and confirmation.
11. **Zero Governance Drift:** Exactly 0 new tokens, 0 new components, and 0 runtime mutations introduced.

---

## 22. Architectural Gaps & Deferred Capabilities

- **Architectural Gaps Logged:** 8 non-critical compositional gaps have been formally documented in [`Phase-9.6-Architecture-Gaps.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/13-Implementation/Phase-9.6-Architecture-Gaps.md). All 8 gaps are 100% resolvable via composition in Phase 9.6 without runtime changes.
- **Enterprise Systems Deferred:**
  - `DataGrid` (Complex inline editing, virtualized rows) $\to$ Replaced by canonical `Table`.
  - `RichTextEditor` $\to$ Replaced by canonical `Textarea` with softWrap.
  - `Calendar` & `DateRangePicker` $\to$ Replaced by native `<input type="date">` / `Select`.
  - `Combobox` / `CommandSystem` $\to$ Replaced by native `Select` / `Search-Filter-Bar`.
  - `Tree`, `VirtualizedList`, `FileUploadManager` $\to$ Strictly deferred to post-v1.0.
- **Dense Density Tier:** Strictly deferred and disabled in appearance settings.

---

## 23. Implementation Boundary & Strict Stop

In accordance with Phase 9.6 governance:
- **This concludes the Architecture Definition stage of Phase 9.6.**
- **Application implementation (HTML, CSS, JavaScript, fixtures) is STRICTLY NOT STARTED.**
- Execution is completely halted here to await the Lead Architect's review and authorization before any implementation work begins.
