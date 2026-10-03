# MDS Playground & Reference Implementation Architecture

**Layer:** 13-Implementation  
**Target Specification:** [`MDS-Implementation-Architecture.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/13-Implementation/MDS-Implementation-Architecture.md)  
**Status:** APPROVED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Ratification Date:** 2026-09-20  
**Target Consumer:** Phase 9.5 (Playground) & Phase 9.6 (Reference App)  

---

## 1. Architectural Mission & Decoupling Law

Phase 9 delivers two distinct public consumer applications:
1. **The Interactive Playground (Phase 9.5):** An interactive component laboratory, token explorer, and state simulator.
2. **The Reference Application (Phase 9.6):** A full-featured enterprise SaaS application implementing all 6 canonical page templates and 6 canonical workflows.

### 1.1 The Inviolable Shared-Core Law
> **The Playground and Reference Application must consume the IDENTICAL Runtime Core. There shall be ZERO playground-only component implementations.**

```text
                     MDS Runtime Core (Phase 9.2 - 9.4)
            ┌────────────────────────┴────────────────────────┐
            ▼                                                 ▼
   Interactive Playground                            Reference Application
        (Phase 9.5)                                       (Phase 9.6)
   - Component Inspector                             - Dashboard Overview Template
   - Token & Color Swatches                          - List Management Template
   - State Machine Simulator                         - Detail Entity Template
   - Variant Matrix Viewer                           - Form Edit Template
   - Code Copy Generator                             - Settings Workspace Template
                                                     - AI Workspace Template
```

---

## 2. Interactive Playground Architecture (Phase 9.5)

### 2.1 Purpose & Target Personas
- **Designers:** Inspect token color swatches, typographic scales, spacing rhythms, and visual presets.
- **Engineers:** Test interactive component states, inspect HTML/DOM anatomy, copy ready-to-use HTML/CSS snippets.
- **AI Coding Agents:** Read deterministic component examples, explore token mappings, and verify composition rules.

### 2.2 Shell Topology & Screen Layout
The Playground web application shell (`MDS/Playground/index.html`) is structured into four functional zones:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. GLOBAL TOOLBAR: Theme (Light/Dark/HC) | Preset | Density | RTL/LTR | Search│
├──────────────┬──────────────────────────────────────────────┬───────────────┤
│ 2. CATALOG   │ 3. COMPONENT STAGE                           │ 4. CONTROLLER │
│    SIDEBAR   │    - Live interactive component canvas       │    PANEL      │
│              │    - Multi-viewport resize handles           │               │
│ - Foundatns  │    - Arabic / English bilingual preview      │ - Variants    │
│ - Tokens     │    - Experience State Switcher               │ - Sizes       │
│ - Primitives │                                              │ - States      │
│ - Components │ ──────────────────────────────────────────── │ - Props       │
│ - Patterns   │ 5. CODE INSPECTOR                            │ - Slots       │
│ - Workflows  │    - Semantic HTML snippet                   │               │
│ - Templates  │    - Token bindings used                     │               │
└──────────────┴──────────────────────────────────────────────┴───────────────┘
```

### 2.3 Interactive Controller Capabilities:
- **Live State Switcher:** Force component into `Default`, `Hover`, `Pressed`, `Focus`, `Disabled`, `Loading`, `Selected`, `Error`, or `Success`.
- **Variant Selector:** Switch between `Primary`, `Secondary`, `Outline`, `Ghost`, `Danger`.
- **Size Selector:** Switch between 32px (`sm`), 40px (`md`), 48px (`lg`).
- **Slot Toggle:** Enable/disable Prefix Icon, Suffix Icon, or Trailing Badges.
- **Instant Code Generator:** Emits semantic, clean HTML markup reflecting the active inspector configuration with one-click copy.

---

## 3. Reference Implementation Architecture (Phase 9.6)

### 3.1 Purpose & Scope
The Reference Application (`MDS/Reference-Application/index.html`) proves that MDS scales effortlessly into a complex, cohesive, multi-screen enterprise product. It integrates all 6 canonical page templates and orchestrates all 6 canonical workflows.

### 3.2 Canonical Screen Inventory (6 Templates Realized):

1. **Screen 1: Dashboard Overview (`MDS-TMP-001`)**
   - *Archetype:* Executive summary workspace with high information density.
   - *Composition:* Page-Header, 4 KPI Metric Cards, Activity Feed List, and Quick Action Buttons.
   - *Experience States:* Populated metrics vs Skeleton loading state.
2. **Screen 2: List Management (`MDS-TMP-002`)**
   - *Archetype:* High-throughput record management.
   - *Composition:* Search-Filter-Bar, Data Table with sticky header, Checkbox selection, and Bulk Action Toolbar.
   - *Workflow:* Executes the **Search & Discovery Workflow** (`MDS-WKF-002`).
   - *Experience States:* Populated records vs Empty search results (`Empty-State` pattern).
3. **Screen 3: Detail Entity (`MDS-TMP-003`)**
   - *Archetype:* Deep inspection of a single record.
   - *Composition:* Two-column master-detail layout, tabbed navigation (`Tabs`), metadata sidebar, and audit timeline.
   - *Workflow:* Executes the **Destructive Action Workflow** (`MDS-WKF-003`) with safe confirmation modal.
4. **Screen 4: Form Edit (`MDS-TMP-004`)**
   - *Archetype:* Structured data entry and entity modification.
   - *Composition:* Form-Section patterns, labeled fields, validation banners, and sticky action bar.
   - *Workflow:* Executes the **Form Submission Workflow** (`MDS-WKF-001`) with inline validation and recovery.
5. **Screen 5: Settings Workspace (`MDS-TMP-005`)**
   - *Archetype:* System configuration and user preferences.
   - *Composition:* Vertical navigation tabs, toggle cards (`Switch`), and danger zone with confirmation.
   - *Workflow:* Executes the **Settings Update Workflow** (`MDS-WKF-004`) with optimistic save and toast feedback.
6. **Screen 6: AI Workspace (`MDS-TMP-006`)**
   - *Archetype:* AI-native split-pane conversational canvas.
   - *Composition:* AI-Input-Prompt with token counter, streaming response simulator, and AI-Result-Review card.
   - *Workflow:* Executes the **AI Synthesis Review Workflow** (`MDS-WKF-005`) adhering to finding AF-001 live region speech throttling.

---

## 4. Universal Navigation & Routing

Both the Playground and Reference Application utilize **zero-dependency URL hash routing** (`window.location.hash`):
- `#/components/button` $\to$ Playground Button inspector.
- `#/templates/dashboard` $\to$ Reference Dashboard screen.
- `#/templates/ai-workspace` $\to$ Reference AI screen.

This enables deep-linking, browser history navigation (Back/Forward buttons), and instantaneous offline loading without requiring server-side routing configuration.
