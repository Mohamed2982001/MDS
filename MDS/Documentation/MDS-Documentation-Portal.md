# Master Design System (MDS) — Documentation Portal & Unified Catalog

**Document Layer:** Documentation (Portal Layer)  
**Status:** APPROVED (Phase 8.1.4 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-20  

---

## 1. Executive Summary & Portal Mission

The **MDS Documentation Portal** serves as the interactive, unified documentation layer, visual catalog, and developer/designer showcase for the **Master Design System (MDS)**.

While earlier phases established the foundations, design tokens, layout primitives, atomic components, structural patterns, multi-step workflows, full-page templates, accessibility audits, and automated test harnesses across separate markdown specifications, **the Documentation Portal unites all 14 layers into an accessible, navigable, and search-driven single pane of glass**.

### Key Personas Served:
1. **Developers:** Instant copy-paste token references, component APIs, state contracts, keyboard accessibility guidance, and FSM transition schemas.
2. **Product Designers:** Direct visual showcase of chromatic slate palettes, Cairo typography hierarchy, surface depth triads, spacing rules, and responsive recomposition blueprints.
3. **AI Coding Agents:** Structured, machine-readable index (`Documentation-Index.json`) enabling zero-guesswork exploration of reusable assets, source paths, and verification states.

---

## 2. The Source-of-Truth Hierarchy (NON-NEGOTIABLE)

The Documentation Portal is strictly a **CONSUMER** of the Master Design System. It must **NEVER** become the source of truth, and must **NEVER** duplicate token values or invent undocumented component variants.

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Structured Token Repository (MDS/02-Tokens/**/*.json)   │ ◄── Canonical Token Truth
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Canonical MDS Specifications (MDS/**/*.md)               │ ◄── Canonical Architectural Truth
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Existing Showcase & Validation Artifacts                 │ ◄── Runtime Evidence Truth
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Documentation Portal (MDS/Documentation/)                │ ◄── READ-ONLY CONSUMER & VISUALIZER
└─────────────────────────────────────────────────────────────┘
```

### Inviolable Rules:
- **No Manual Duplication:** If a design token is displayed, it is derived directly from `MDS/02-Tokens/`.
- **No Specification Rewriting:** If a component, pattern, workflow, or template is documented, it links to its canonical markdown file.
- **Zero Hidden Abstractions:** The portal does not invent new components, new tokens, or new layout rules.

---

## 3. Information Architecture (14 Architectural Domains)

The portal organizes the entire design system into 14 distinct top-level sections:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       MDS DOCUMENTATION PORTAL IA                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ 01. Overview          MDS DNA, Soft Modern personality, Core Philosophy    │
│ 02. Foundations       Typography, Color, Spacing, Shape, Elevation, Motion │
│ 03. Tokens            DTCG 3-Tier Model, 188 Tokens, Theme/Density Axes    │
│ 04. Primitives        Layout (5), Surface (Triad), A11y (4), Icon Contract │
│ 05. Components        19 Core Components across 6 Families (16-Pt Anatomy) │
│ 06. Patterns          8 Canonical Patterns (22-Pt Anatomy, 10 Laws)        │
│ 07. Workflows         6 Canonical Workflows (27-Pt Anatomy, 11-State FSM)  │
│ 08. Templates         6 Canonical Templates (32-Pt Anatomy, 10 Laws)       │
│ 09. Experience States Universal State Model (Loading, Empty, Error, etc.)  │
│ 10. Accessibility     AT Audit, 7-Facet Law, 33-Test Matrix, AF Findings   │
│ 11. Responsive        Breakpoints (320px–1440px), Recomposition Philosophy │
│ 12. AI Layer          AI Synthesis Review, Human-in-the-Loop, Agent Rules  │
│ 13. Governance        8-Stage Lifecycle, 4 Governance Laws, ADR Log        │
│ 14. Testing           Pyramid, Regression Harness (run_tests.py), 40 Tests │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Key Portal Features & Capabilities

### 4.1 Token Explorer
- Reads directly from `MDS/02-Tokens/**/*.tokens.json`.
- Displays token identifier, layer (Primitive, Semantic, Component), resolved value, alias reference, description, and source file.
- Visualizes the 3-tier reference chain:
  $$\text{Component Token} \longrightarrow \text{Semantic Token} \longrightarrow \text{Primitive Token}$$
- Provides interactive color swatches, copy-to-clipboard actions, and theme override previews (Light, Dark, High Contrast).

### 4.2 Component Catalog (19 Core Components)
- Exhaustive catalog of all 19 approved components grouped by family:
  - **Actions (3):** `Button`, `IconButton`, `Link`
  - **Inputs (7):** `Field`, `Input`, `Textarea`, `Checkbox`, `Radio`, `Switch`, `Select`
  - **Feedback (3):** `Alert`, `Spinner`, `Skeleton`
  - **Data Display (3):** `Badge`, `Card`, `Table`
  - **Navigation (1):** `Tabs`
  - **Overlays (2):** `Dialog`, `Tooltip`
- Displays explicit verification state:
  - `Implemented` (in showcase/sandboxes)
  - `Specified` (`Dialog`, `Tooltip` specifications per Phase 5)
  - `Manually Verified`
  - `Automated Verified` (via `run_tests.py`)
  - `Deferred` (the 9 enterprise systems)

### 4.3 Pattern & Workflow Catalogs
- **8 Canonical Patterns:** `Page-Header`, `Search-Filter-Bar`, `Data-List-Card`, `Form-Section`, `Empty-State`, `Confirmation-Dialog`, `AI-Input-Prompt`, `AI-Result-Review`.
- **6 Canonical Workflows:** `Form-Submission`, `Search-Discovery`, `Destructive-Action`, `Settings-Update`, `AI-Synthesis-Review`, `Error-Recovery`.
- Includes interactive FSM state visualizer displaying transitions across universal operational states (`IDLE` $\to$ `VALIDATING` $\to$ `PROCESSING` $\to$ `SUCCESS`).

### 4.4 Template Catalog
- **6 Canonical Page Templates:** `Dashboard-Overview` (`MDS-TMP-001`), `List-Management` (`MDS-TMP-002`), `Detail-Entity` (`MDS-TMP-003`), `Form-Edit` (`MDS-TMP-004`), `Settings-Workspace` (`MDS-TMP-005`), `AI-Workspace` (`MDS-TMP-006`).
- Exposes regional layout blueprints, pattern compositions, hosted workflow slots, and responsive reflow behaviors.

### 4.5 Global Instant Search & Multi-Faceted Filtering
- Instant, deterministic in-browser search across titles, keywords, layer codes, component IDs, and descriptions.
- Multi-faceted filter engine supporting:
  - By Layer: Foundations, Tokens, Primitives, Components, Patterns, Workflows, Templates
  - By Verification Status: Implemented, Specified, Verified, Deferred
  - By Feature Tag: RTL, A11y, Responsive, AI, Form, Data

### 4.6 Deep Linking & Hash Routing
- Predictable hash-based navigation allowing direct deep-linking without server routing:
  - `#/overview`
  - `#/tokens`
  - `#/components` (and `#/components/button`, `#/components/input`, etc.)
  - `#/patterns`
  - `#/workflows`
  - `#/templates`
  - `#/accessibility`
  - `#/testing`

### 4.7 Bidirectional RTL & Theming Support
- Defaults to Arabic RTL (`dir="rtl"`) with the canonical **Cairo** typeface.
- Provides instant LTR / RTL toggle (`dir="ltr"` / `dir="rtl"`).
- Supports instant theme switching across **Light Mode**, **Dark Mode**, and **High Contrast Mode** using MDS semantic tokens.

### 4.8 Machine-Readable Documentation Index (`Documentation-Index.json`)
- Derived, structured JSON catalog located at `MDS/Documentation/Documentation-Index.json`.
- Provides an automated lookup table for AI coding agents to answer:
  - *"What components exist in MDS?"*
  - *"Which patterns solve search and filtering?"*
  - *"What are the token aliases for brand blue?"*
  - *"Where is the canonical specification located?"*
  without scanning every markdown file in the repository.

---

## 5. Portal Governance & Maintenance

- **Regeneration & Sync:** When a component or token is modified in the canonical source files, `Documentation-Index.json` and the portal reflect the update.
- **Zero Scope Creep:** The portal strictly respects the **0 New Tokens / 0 New Components / 0 Lower-Layer Regressions** mandate.
- **Verification Status Honesty:** The portal never claims physical screen reader verification (NVDA/VoiceOver) or automated browser visual diffing, maintaining their formal status as `DEFERRED TO QA LAB` and `DEFERRED TO CI`.
