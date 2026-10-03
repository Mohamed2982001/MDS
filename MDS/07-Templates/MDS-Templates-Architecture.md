# Master Design System (MDS) — Templates Architecture (Layer 07)

**Document Layer:** 07-Templates  
**Status:** APPROVED (Phase 8.1.3 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-17  

---

## 1. Executive Summary & Layer Mission

In the Master Design System (MDS), **Layer 07: Templates** defines the formal architectural contracts, region orchestrations, and responsive layout scaffolding governing how complete pages and full screens are structured across products.

While lower layers govern atomic aesthetics (Foundations & Tokens), structural components (Primitives & Components), localized compositions (Patterns), and multi-step task journeys (Workflows), **Templates provide the reusable, cohesive environments in which these layers come together**.

A Template is **NOT** a finished product page; it is a platform-agnostic, reusable information architecture that:
- Establishes macro visual and reading hierarchy.
- Allocates semantic layout regions and content slots.
- Orchestrates Layer 05 Patterns into spatial arrangements.
- Hosts Layer 06 Workflows in dedicated behavioral viewports.
- Controls page-level responsive recomposition across Compact, Standard, Wide, and Full screens.
- Standardizes page-level experience states (Loading skeletons, Empty views, Error recovery banners, Access boundaries).
- Remains completely independent of business-specific content, application routing, and database schema.

---

## 2. The Authoritative MDS Architectural Hierarchy

MDS enforces a strict, unidirectional, non-circular composition hierarchy. Each layer builds upon the layers directly beneath it and may never reach upward or bypass intermediate layers.

```text
┌─────────────────────────────────────────────────────────────┐
│ 01. Foundations       Typography, Color, Space, Elevation   │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 02. Tokens            Design tokens (188 canonical tokens)   │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 03. Primitives        Container, Stack, Grid, FocusRing     │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 04. Components        Button, Input, Badge, Dialog (19 Core)│
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 05. Patterns          FormSection, PageHeader, EmptyState   │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 06. Workflows         FormSubmission, ErrorRecovery (6 Core)│
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 07. Templates (THIS)  Page layout scaffolding & archetypes  │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 The Composition Law
$$\text{Foundations} \longrightarrow \text{Tokens} \longrightarrow \text{Primitives} \longrightarrow \text{Components} \longrightarrow \text{Patterns} \longrightarrow \text{Workflows} \longrightarrow \mathbf{\text{Templates}}$$

1. **Downstream Consumption Only:** Templates consume Workflows (Layer 06), Patterns (Layer 05), Components (Layer 04), Primitives (Layer 03), and Tokens (Layer 02).
2. **Zero Upstream Dependency:** Lower layers never know about or import from Layer 07 Templates.
3. **No Direct Raw Styling:** Templates define grid and flex relationships exclusively using MDS tokens (`space.*`, `container.*`). They never introduce raw pixel values, arbitrary margins, or unmapped hex colors.
4. **No Business Logic Coupling:** Templates declare slot contracts and injection points. They do not handle Redux/Bloc state, REST/GraphQL endpoints, or database entity structures.

---

## 3. Ontological Demarcation: What Templates ARE vs. ARE NOT

| Dimension | Layer 05: Pattern | Layer 06: Workflow | Layer 07: Template | Application Page |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Question** | *"How is this localized UI fragment composed?"* | *"How does the user progress through this multi-step task?"* | *"How is the entire screen/page structured and arranged?"* | *"What exact data and business logic does this app show?"* |
| **Scope** | Sub-page UI section (e.g. Header, Dialog) | Behavioral task flow over time (e.g. Submit, Recover) | Full viewport layout scaffold & regions | Production route in a specific product |
| **Data Binding** | Generic component props | Action payloads & validation results | Named slots (`slot="header"`, `slot="main"`) | Domain models (`Invoice`, `Patient`) |
| **State Ownership**| Local component state | Finite State Machine (FSM) states | Page-level Experience States (Loading, Error) | Global application/business store |
| **Reusability** | Universal | Universal | Universal across products | Specific to single product / domain |
| **Example** | `Page-Header` | `Destructive-Action` | `Detail-Entity Template` | `Stripe Invoice #1042 Screen` |

### 3.1 Templates ARE:
- Reusable structural page/screen compositions.
- Scaffolding that establishes reading order, landmarks, and spatial grouping.
- Orchestrators of Patterns (`Page-Header`, `Search-Filter-Bar`, `Data-List-Card`, `Empty-State`).
- Hosts for Workflows (`Form-Submission`, `Search-Discovery`, `Settings-Update`, `AI-Synthesis-Review`).
- Governors of responsive layout recomposition (Compact, Standard, Wide, Full).
- Frameworks for page-level experience state transitions (Loading skeleton $\to$ Populated $\to$ Error banner).
- 100% domain-neutral and business-agnostic.

### 3.2 Templates ARE NOT:
- Complete product screens (e.g., "Patient Electronic Health Record").
- Components, Patterns, or Workflows.
- Providers of arbitrary page copy, icons, or mock business data.
- State machines (state machines belong to Layer 06 Workflows).
- Application routing or URL navigation logic.
- Source of new design tokens or visual style variations.

---

## 4. The 32-Point Mandatory Template Anatomy Standard

To guarantee architectural consistency and eliminate ambiguous specifications, every canonical template must define all 32 points:

```text
┌─────────────────────────────────────────────────────────────┐
│                MDS TEMPLATE ANATOMY STANDARD                │
├─────────────────────────────────────────────────────────────┤
│ 01. Template ID              │ 17. Accessibility Structure  │
│ 02. Name                     │ 18. Experience States        │
│ 03. Intent                   │ 19. Loading Strategy         │
│ 04. Problem Solved           │ 20. Error Strategy           │
│ 05. When to Use              │ 21. Empty Strategy           │
│ 06. When Not to Use          │ 22. Recovery Strategy        │
│ 07. Page Regions             │ 23. Density Behavior         │
│ 08. Region Hierarchy         │ 24. Theme/Mode Behavior      │
│ 09. Pattern Composition      │ 25. AI Integration           │
│ 10. Workflow Slots           │ 26. Navigation Context       │
│ 11. Component Dependencies   │ 27. Focus Management         │
│ 12. Content Slots            │ 28. Motion Behavior          │
│ 13. Required vs Optional Reg │ 29. Token Dependencies       │
│ 14. Responsive Composition   │ 30. Anti-Patterns            │
│ 15. Mobile Composition       │ 31. Validation Requirements  │
│ 16. RTL Behavior             │ 32. Selection Criteria       │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Regional Vocabulary & Layout Scaffolding

MDS Templates standardize a universal vocabulary for page regions:

1. **`Global Navigation Region` (`<header>` / `<nav>`):** Top-level orientation bar across apps.
2. **`Context Navigation Rail / Sidebar` (`<aside>` / `<nav>`):** Contextual hierarchy (e.g. settings rail, category tree).
3. **`Page Header Region` (`<header>`):** Houses `Page-Header` pattern (Breadcrumbs, Title, Badges, Action group).
4. **`Filter & Controls Toolbar` (`<div>` / `<section>`):** Houses `Search-Filter-Bar` pattern and view switchers.
5. **`Primary Content Workspace` (`<main>`):** The central focus of user intent (grid, list, form, canvas).
6. **`Secondary Supporting Panel` (`<aside>`):** Contextual metadata, audit logs, quick summaries, or citations.
7. **`Footer & Sticky Action Bar` (`<footer>`):** Persistent primary actions, save/cancel triggers, and pagination.

---

## 6. Cross-Cutting Engineering Dimensions

### 6.1 Responsive Recomposition (Not Shrinking)
Templates enforce the core MDS principle: **Recomposition over Shrinking**.
- **Compact (< 768px / Mobile):** Multi-column grids collapse to a single ergonomic column; horizontal toolbars collapse to expandable drawers or bottom sheets; action bars become fixed/sticky bottom bars with $\ge 44\text{px}$ touch targets.
- **Standard (768px – 1151px / Tablet):** Dedicated master-detail views; 2-column forms; adaptive sidebar navigation.
- **Wide (1152px – 1439px / Standard Desktop):** Canonical 1152px container max-width; persistent sidebars; multi-pane workspaces.
- **Full ($\ge$ 1440px / Wide Screen):** 1440px wide container max-width (`container.xl`); max-width containment prevents unreadable line lengths.

### 6.2 Structural Accessibility (WCAG 2.1/2.2 AA)
- **Semantic Landmarks:** Every template enforces strictly one `<main>` landmark, explicit `<header>`, `<footer>`, `<nav>`, and `<aside>` roles.
- **Heading Hierarchy:** Standardizes `<h1>` in the Page Header region, `<h2>` for section boundaries, and `<h3>` for individual cards or widgets. Zero heading skips ($H1 \to H2 \to H3$).
- **Skip Navigation:** Every template reserves a top-level `Skip to main content` anchor link.
- **Focus Lifecycle:** Explicit initial focus placement upon page mount, predictable tab traversal, and restoration upon overlay dismissals.

### 6.3 Bidirectional RTL & Cairo Typographic Standard
- **Logical Flow:** Native inline progression (`inline-start` to `inline-end`); 100% CSS Logical Properties (`margin-inline`, `padding-inline`).
- **Anti-Row-Reverse:** Zero functional `flex-direction: row-reverse` to protect WCAG 2.4.3 focus order.
- **Cairo Font:** Universal typography using Cairo for Arabic and Latin scripts, with +0.15 context-aware leading boost for Arabic body copy.

### 6.4 Experience State Governance
Templates manage macro page-level states through standardized slots:
- **`Loading State`:** Full-page structural skeleton matching real content geometry.
- **`Empty State`:** Centralized `Empty-State` pattern with diagnostic copy and actionable recovery CTA.
- **`Error State`:** Top-level error banner or full-view error card with non-destructive retry affordance.
- **`Access State`:** Permission Denied or Authentication Required prompt with contextual recovery ("Sign in", "Request access").

---

## 7. Canonical Template Inventory (6 Core Templates)

Through rigorous candidate evaluation against reuse, orthogonal information architecture, and the anti-explosion mandate, MDS establishes exactly **6 Core Canonical Templates**:

| Template ID | Canonical Name | Category | Archetypal Purpose |
| :--- | :--- | :--- | :--- |
| **`MDS-TMP-001`** | **`Dashboard-Overview`** | Overview | High-level telemetry, KPI metrics, recent activity grids, and system status overview. |
| **`MDS-TMP-002`** | **`List-Management`** | Management | Tabular and card collection management, search/filter toolbar, bulk actions, and pagination. |
| **`MDS-TMP-003`** | **`Detail-Entity`** | Entity | Deep single-entity inspection and modification; dual-pane primary content and metadata sidebar. |
| **`MDS-TMP-004`** | **`Form-Edit`** | Forms | Focused task completion; constrained-width form sections, validation error mapping, sticky actions. |
| **`MDS-TMP-005`** | **`Settings-Workspace`** | Settings | Application and user configuration; master-detail category navigation and preference panels. |
| **`MDS-TMP-006`** | **`AI-Workspace`** | AI | Multi-pane generative interaction; prompt input, live canvas workspace, and citation review panel. |

---

## 8. Hard Invariant & Scope Boundary Mandate

To preserve system stability and prevent scope creep, Phase 8.1.3 operates under strictly monitored invariants:
1. **New Tokens:** Exactly **0** (188 canonical tokens preserved).
2. **New Primitives:** Exactly **0** (Layer 03 unchanged).
3. **New Core Components:** Exactly **0** (19 components preserved).
4. **New Core Patterns:** Exactly **0** (8 patterns preserved).
5. **New Workflows:** Exactly **0** (6 workflows preserved).
6. **Deferred Enterprise Systems:** All **9 complex enterprise systems** remain strictly deferred.
