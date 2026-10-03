# Master Design System (MDS) — Documentation Portal Architecture

**Document Layer:** Documentation (Portal Layer)  
**Status:** APPROVED (Phase 8.1.4 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-20  

---

## 1. Architectural Mission & Philosophy

The **MDS Documentation Portal** is designed as a high-performance, zero-dependency, single-pane-of-glass web application that unifies and visualizes all 14 layers of the Master Design System.

### Core Architectural Axioms:
1. **Consumer-Only Stance:** The portal is strictly a read-only consumer of design tokens and specifications. It never acts as the source of truth, never duplicates token definitions manually, and never invents undocumented components or variations.
2. **Zero-Dependency Static Delivery:** Operates natively in any modern browser without requiring node build steps (`npm run build`), heavyweight documentation generators (Docusaurus, Storybook), or external runtime dependencies.
3. **Deterministic Hash Routing:** Client-side hash routing (`#/<domain>/<item>`) guarantees deep-linkability, bookmarking, and instant navigation without server-side rewrite rules.
4. **Token-Driven CSS:** 100% styled via MDS semantic and component tokens (`var(--mds-*)`). Zero raw hex colors (`#[0-9a-fA-F]{3,6}`) and 100% CSS logical properties.
5. **Bidirectional & Typography Integrity:** Native Cairo typography with RTL default (`dir="rtl"`), supporting zero-layout-flip LTR toggling.

---

## 2. Source-of-Truth Hierarchy & Ingestion Flow

The portal runtime and index ingestion strictly respect the MDS authority hierarchy:

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Structured Token Repository (MDS/02-Tokens/**/*.json)   │ ◄── Canonical Token Truth
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Canonical Specifications (MDS/**/*.md)                   │ ◄── Canonical Architectural Truth
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Automated Test Suite (MDS/10-Testing/run_tests.py)       │ ◄── Automated Regression Truth
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Machine Index (Documentation-Index.json)                 │ ◄── Derived Machine-Readable Catalog
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Documentation Portal Web App (showcase/index.html)       │ ◄── Interactive Consumer UI
└─────────────────────────────────────────────────────────────┘
```

### Ingestion Contract:
- `Documentation-Index.json` is a deterministic projection of canonical Markdown specifications and token JSON files.
- The portal client (`documentation.js`) ingests `Documentation-Index.json` to build its search index, category navigation, token tree, and component cards.

---

## 3. Application Shell & Layout System

The portal UI consists of four unified architectural regions:

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                             TOPBAR SHELL                                 │
│  [Logo / Brand]    [Global Search: Cmd+K]    [Theme] [Density] [Dir RTL] │
├─────────────────┬────────────────────────────────────────────────────────┤
│                 │                                                        │
│  NAVIGATION     │                  MAIN STAGE SHELL                      │
│  SIDEBAR        │                                                        │
│                 │  ┌──────────────────────────────────────────────────┐  │
│  • Overview     │  │ Breadcrumb & Page Header                         │  │
│  • Foundations  │  ├──────────────────────────────────────────────────┤  │
│  • Tokens       │  │                                                  │  │
│  • Primitives   │  │ Dynamic Section Content                          │  │
│  • Components   │  │ (Interactive Showcases, Token Grids,             │  │
│  • Patterns     │  │  Anatomy Tables, FSM State Visualizers)          │  │
│  • Workflows    │  │                                                  │  │
│  • Templates    │  │                                                  │  │
│  • A11y & Tests │  └──────────────────────────────────────────────────┘  │
│                 │                                                        │
├─────────────────┴────────────────────────────────────────────────────────┤
│                            FOOTER SHELL                                  │
│  MDS Phase 8.1.4 Unified Catalog • 188 Tokens • 19 Components • Cairo    │
└──────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Topbar Shell
- **Brand Identity:** MDS Monogram + Version Badge (`v1.0.0 Phase 8.1.4`).
- **Global Search Trigger:** Instant input box with keyboard shortcut hint (`Ctrl+K` / `Cmd+K`).
- **Density Toggle:** Switches between `Default` (44px touch targets) and `Compact` (36px desktop data density) by toggling `data-density="compact"`.
- **Theme Switcher:** Toggles between `light`, `dark`, and `high-contrast` on the root document element.
- **Direction Toggle:** Switches between Arabic (`dir="rtl"`) and English (`dir="ltr"`).

### 3.2 Navigation Sidebar
- Groups all 14 layers into 5 logical categories:
  1. **Core Architecture:** Overview, Foundations, Tokens, Primitives.
  2. **Atomic System:** 19 Components (grouped by Actions, Inputs, Feedback, Data Display, Navigation, Overlays).
  3. **Compositions:** 8 Canonical Patterns, 6 Canonical Workflows, 6 Page Templates.
  4. **Quality & Compliance:** Accessibility Matrix, Responsive Breakpoints, Universal Experience States.
  5. **Operations:** Governance & ADRs, Automated Test Suite (44 Tests).
- Active navigation item auto-highlights based on the current hash route.

### 3.3 Main Stage Shell
- Render target for dynamically routed content.
- Houses interactive sandboxes, live code snippets, copyable token identifiers, anatomy diagrams, and state transitions.

---

## 4. Client Router & Hash State Engine

The portal uses a lightweight, vanilla JavaScript hash router (`documentation.js`):

### Route Map:
| Hash Route | Target View | Content Rendered |
| :--- | :--- | :--- |
| `#/` or `#/overview` | Overview View | MDS Mission, Soft Modern DNA, 14-Layer Hierarchy, Scope Metrics |
| `#/foundations` | Foundations View | Color Palettes, Typography Scale, Spacing Grid, Elevation, Motion |
| `#/tokens` | Token Explorer | 188 Tokens interactive grid, DTCG 3-Tier chain viewer, search & copy |
| `#/primitives` | Primitives View | 5 Layout Primitives, Surface Triad, 4 A11y Primitives, Icon contract |
| `#/components` | Component Catalog | 19 Components catalog, 6 families, verification badges, specifications |
| `#/components/:id` | Component Detail | 16-point anatomy, token bindings, accessibility rules, interactive demo |
| `#/patterns` | Pattern Catalog | 8 Canonical Patterns, 22-point anatomy, composition rules, selection matrix |
| `#/workflows` | Workflow Catalog | 6 Canonical Workflows, 11-State FSM, security triad, recovery patterns |
| `#/templates` | Template Catalog | 6 Page Templates, responsive blueprints, pattern slot bindings |
| `#/states` | Experience States | Universal 11-state model, transitions, fallback and recovery contracts |
| `#/accessibility` | Accessibility View | 33-Audit Matrix, 7-Facet Law, AF Findings, Deferred Physical Status |
| `#/responsive` | Responsive View | 5 Breakpoints (320px–1440px), Recomposition rules, Mobile-first |
| `#/ai` | AI Integration | Synthesis Review pattern, Human-in-the-loop, Agent coding rules |
| `#/governance` | Governance View | 8-Stage Lifecycle, 4 Governance Laws, ADR Decision Logs |
| `#/testing` | Test Suite View | 44 Test Cases Matrix, Automated Test Suite runner, Coverage status |

---

## 5. Token Explorer Architecture

The Token Explorer bridges raw JSON definitions to human and agent understanding:
1. **JSON Stream Ingestion:** Ingests tokens from `02-Tokens/Primitive/*.tokens.json`, `Semantic/*.tokens.json`, and `Component/*.tokens.json`.
2. **Reference Resolution:** Traces aliases such as `{color.brand.primary}` $\to$ `{color.blue.600}` $\to$ `#1e40af` (in documentation viewer metadata).
3. **Interactive Swatch Rendering:**
   - Color swatches with contrast ratio calculation against surface backgrounds.
   - Spacing swatches with visual box dimension previews.
   - Typography previews displaying Cairo weight, font size, and line height.
   - Radius swatches showcasing shape geometry (`rounded-sm` through `rounded-full`).
4. **Copy-on-Click:** Single click copies the CSS variable (`var(--mds-color-brand-primary)`) to the clipboard with visual toast feedback.

---

## 6. Global Search & Multi-Faceted Filter Pipeline

The search pipeline runs client-side with sub-millisecond execution:

```text
[User Query String] ──► [Tokenizer / Normalizer] ──► [Index Matcher]
                                                            │
                                                            ▼
                                                [Filter Evaluator]
                                                • Layer Filter
                                                • Status Filter
                                                • Tag Filter
                                                            │
                                                            ▼
                                                [Ranked Result Set]
                                                • Exact Title Matches
                                                • Keyword Matches
                                                • Token Name Matches
                                                • Content Description Matches
```

- **Query Normalization:** Trims whitespace, strips Arabic diacritics (tashkeel), converts Latin to lowercase.
- **Score Ranking:** Direct ID/Title match (weight 10) > Keyword match (weight 5) > Description match (weight 2).
- **Live Search Overlay:** Shows top 8 matches with layer badge, item title, preview snippet, and direct deep-link.

---

## 7. CSS Architecture & Token Invariant Rules

The documentation portal CSS (`documentation.css`) adheres to strict quality invariants:

1. **Zero Raw Hex Colors:** Every color is expressed via `var(--mds-*)`.
2. **100% CSS Logical Properties:**
   - `margin-inline-start` / `margin-inline-end` instead of `left` / `right`.
   - `padding-inline`, `padding-block` instead of directional padding.
   - `border-inline-start` instead of `border-left`.
   - `inset-inline-start`, `inset-inline-end` instead of `left` / `right`.
3. **Zero `flex-direction: row-reverse`:** Directional reflow is handled automatically by the browser's native Bidi engine when `dir="rtl"` is set on `<html>`.
4. **Container Queries & Mobile Reflow:** Layout adjusts smoothly from 320px mobile viewport to 1440px desktop ultrawide displays.

---

## 8. Verification Status Taxonomies

To preserve 100% honesty across all layers, the portal displays explicit, non-conflated status indicators:

| Status Badge | Semantic Definition | Entities Tagged |
| :--- | :--- | :--- |
| `Implemented` | Fully coded in CSS/HTML and verified in sandboxes | 17 Components, All Foundations, Layout Primitives |
| `Specified` | Fully designed and specified; production DOM pending | Dialog, Tooltip (Per Phase 5 Scope Boundary) |
| `Manually Verified` | UX and visual composition verified via interactive walk | 8 Patterns, 6 Workflows, 6 Templates |
| `Automated Verified` | Verified by Python regression harness (`run_tests.py`) | 41 Automated Test Cases across 12 Test Suites |
| `Deferred to QA Lab` | Requires physical hardware & screen readers | Physical AT Testing (NVDA, VoiceOver, TalkBack) |
| `Deferred to CI` | Requires headless browser automation & visual diffing | Playwright / Puppeteer visual regression |
| `Deferred Enterprise` | Out of scope for Core v1.0.0; reserved for Phase 9 | DataGrid, RichTextEditor, Calendar, Combobox, etc. (9 Systems) |

---

## 9. Machine-Readable Documentation Index Specification

The portal includes `MDS/Documentation/Documentation-Index.json` to empower AI coding assistants:
- **Schema:**
  - `version`: System version string.
  - `generated`: Generation timestamp.
  - `invariants`: Formal token counts, component counts, pattern counts, workflow counts, template counts.
  - `layers`: Map of 14 layer descriptors containing canonical file paths and summary descriptions.
  - `catalog`: Flat, searchable array of all design system entities (Tokens, Primitives, Components, Patterns, Workflows, Templates).
  - `deferred`: Explicit listing of deferred systems and tests.
- **Agent Usage:** Coding agents can read this single JSON file to discover available components, token names, and source files without traversing dozens of directories.
