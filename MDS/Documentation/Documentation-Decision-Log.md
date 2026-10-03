# Master Design System (MDS) — Documentation Portal Decision Log

**Document Layer:** Documentation (Portal Layer)  
**Status:** APPROVED (Phase 8.1.4 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-20  

---

## 1. Overview & Decision Methodology

This Decision Log captures key architectural, technical, and structural decisions made during the design and delivery of the **MDS Documentation Portal (Phase 8.1.4)**. 

Each decision follows the standard Architecture Decision Record (ADR) format:
- **Context & Problem Statement**
- **Decision & Rationale**
- **Evidence & Constraints**
- **Consequences (Positive & Negative)**

---

## 2. Architecture Decision Records (DDR-001 through DDR-010)

### DDR-001: Zero-Dependency Static Web Portal vs. Heavyweight Frameworks
- **Context:** The MDS repository is an unbundled, specification-first design system without an existing `package.json` or build toolchain in the workspace root. We needed an interactive documentation portal. Options included Docusaurus, Storybook, Next.js, Vite, or a native vanilla web app.
- **Decision:** Build a high-performance, zero-dependency static web application (`index.html`, `documentation.css`, `documentation.js`).
- **Rationale:** 
  1. Prevents introducing hundreds of megabytes of `node_modules` and complex node build scripts into a pure architecture repository.
  2. Runs instantly in any standard browser via double-click (`file:///`) or static file server (`http-server`, `python -m http.server`).
  3. Eliminates maintenance debt, dependency security vulnerabilities, and build configuration breakage.
- **Consequences:** (+) Zero build time, instant preview, 100% portable. (-) Must author router and state logic in vanilla modern JavaScript without JSX/TypeScript transpilation at runtime.

---

### DDR-002: Strict Source-of-Truth Hierarchy & Read-Only Consumer Stance
- **Context:** Documentation portals frequently drift from reality when maintainers manually re-enter token hex codes, component API tables, and state lists into documentation markup.
- **Decision:** Enforce that the Documentation Portal is strictly a **READ-ONLY CONSUMER** of the Master Design System. The canonical sources of truth remain:
  1. `MDS/02-Tokens/**/*.tokens.json` (Tokens)
  2. `MDS/**/*.md` (Architecture, Components, Patterns, Workflows, Templates)
  3. `MDS/10-Testing/run_tests.py` (Automated Verification)
- **Rationale:** Prevents divergence. If a token or component changes, it must be changed in the canonical source file first. The portal merely visualizes it.
- **Consequences:** (+) Zero token drift, single authoritative source. (-) Requires syncing `Documentation-Index.json` whenever underlying specs evolve.

---

### DDR-003: Deterministic Client-Side Hash-Based Routing
- **Context:** Users and AI agents need to deep-link directly to specific components (`#/components/button`), tokens (`#/tokens/color-brand-primary`), or workflows (`#/workflows/destructive-action`) without requiring server-side URL rewrite rules (e.g. Apache `.htaccess` or Nginx `try_files`).
- **Decision:** Implement a deterministic client-side hash router listening to `window.addEventListener('hashchange')`.
- **Rationale:** Hash-based routing (`#/path`) works uniformly across all hosting environments, including static file systems (`file://`), GitHub Pages, S3/CloudFront, and local testing servers, with zero server configuration.
- **Consequences:** (+) Universal compatibility, bookmarkable URLs, browser back/forward history support. (-) URLs contain `#` symbol.

---

### DDR-004: Unified Machine-Readable Index (`Documentation-Index.json`)
- **Context:** AI coding agents and automated scripts frequently need to query design system assets without parsing dozens of markdown files, which consumes excessive tokens and context window space.
- **Decision:** Compile a single structured JSON index (`MDS/Documentation/Documentation-Index.json`) cataloging all 14 layers, 188 tokens, 19 components, 8 patterns, 6 workflows, 6 templates, and test suites.
- **Rationale:** Provides both the client-side search engine and AI subagents with an instant, structured lookup table containing titles, IDs, categories, file paths, keywords, and verification statuses.
- **Consequences:** (+) Instant client-side search indexation, subagent efficiency, machine-verifiable consistency. (-) Index file must be updated during major system updates.

---

### DDR-005: 100% Token-Driven Styling & Strict Zero Raw Hex Rule
- **Context:** Many design system documentation sites violate their own rules by using ad-hoc colors, hardcoded hex values, or off-brand utility classes in their documentation stylesheets.
- **Decision:** Enforce that `MDS/Documentation/showcase/documentation.css` strictly consumes MDS design tokens (`var(--mds-*)`). Raw hex colors (`#[0-9a-fA-F]{3,6}`) are strictly forbidden and validated by `run_tests.py`.
- **Rationale:** The documentation portal must be the ultimate living proof that the Master Design System tokens are fully sufficient to build complex, responsive, accessible web applications.
- **Consequences:** (+) Guarantees token completeness; enforces dogfooding. (-) Developers cannot take quick styling shortcuts with arbitrary hex colors.

---

### DDR-006: Bidirectional RTL First & Cairo Typography Default
- **Context:** Global developer guidelines require Cairo as the primary font and first-class Arabic/RTL support. Web applications often treat RTL as an afterthought by using `flex-direction: row-reverse` which causes focus order inversion.
- **Decision:** 
  1. Default root document to Arabic RTL (`<html lang="ar" dir="rtl">`).
  2. Enforce Cairo font across all headings, body text, and interactive controls.
  3. Prohibit `flex-direction: row-reverse`; rely 100% on native CSS logical properties (`margin-inline`, `padding-inline`, `border-inline-start`, `inset-inline-start`).
  4. Provide an instant runtime toggle between RTL and LTR.
- **Rationale:** Guarantees perfect bidirectional layout mirroring without DOM reordering or accessibility focus bugs.
- **Consequences:** (+) Flawless Arabic and English rendering, full accessibility compliance. (-) Requires diligent use of CSS logical properties.

---

### DDR-007: Explicit Multi-Level Verification Status Taxonomies
- **Context:** Design systems often mislead developers by labeling components or patterns as "100% verified" when accessibility tests were only static lint checks, or when screen reader tests have not been executed on physical devices.
- **Decision:** Establish explicit, non-conflated status indicators across all portal cards:
  - `Implemented`
  - `Specified` (e.g., Dialog, Tooltip)
  - `Manually Verified` (Patterns, Workflows, Templates)
  - `Automated Verified` (Python regression harness tests)
  - `Deferred to QA Lab` (Physical AT screen readers)
  - `Deferred to CI` (Headless browser visual regression)
  - `Deferred Enterprise` (The 9 deferred complex systems)
- **Rationale:** Preserves unshakeable trust and technical honesty with senior engineers and auditing teams.
- **Consequences:** (+) Complete transparency; no fake pass claims. (-) UI must render distinct badges for each taxonomy.

---

### DDR-008: Scope Boundary & Invariant Preservation
- **Context:** During documentation portal implementation, there is a temptation to "fix" or add missing tokens, invent new convenience components, or begin early implementation of deferred enterprise systems (e.g. `DataGrid`).
- **Decision:** Strictly enforce the invariant boundaries:
  - 0 New Foundations
  - 0 New Primitives
  - 0 New Components (Exactly 19 core components)
  - 0 New Patterns (Exactly 8 canonical patterns)
  - 0 New Workflows (Exactly 6 canonical workflows)
  - 0 New Templates (Exactly 6 page templates)
  - 0 New Tokens (Exactly 188 registered tokens, 47 component tokens)
  - 9 Enterprise Systems remain 100% deferred to Phase 9.
- **Rationale:** Protects architectural discipline and prevents scope creep.
- **Consequences:** (+) Strict adherence to project constraints; stability. (-) Portal will showcase deferred systems as roadmap placeholders only.

---

### DDR-009: Interactive Token Swatches with Clipboard Utility & Accessibility Contrast Check
- **Context:** Developers need quick access to CSS variable names and values when implementing UI, while designers need to verify WCAG contrast ratios against various surface backgrounds.
- **Decision:** The Token Explorer provides interactive swatches with one-click copy to clipboard (`navigator.clipboard.writeText`) and contrast ratio badges for text and background color pairs.
- **Rationale:** Increases developer velocity and guarantees visual adherence to WCAG AA contrast standards (4.5:1 for body text, 3:1 for large text/icons).
- **Consequences:** (+) High developer satisfaction and instant feedback. (-) Requires clipboard API permissions in modern browsers.

---

### DDR-010: FSM State Visualizer for Workflows & Templates
- **Context:** Workflows and templates in MDS have multi-step state machines (`IDLE`, `VALIDATING`, `PROCESSING`, `SUCCESS`, `ERROR`, `RETRYING`). Pure text descriptions fail to communicate state transitions dynamically.
- **Decision:** Build an interactive client-side state machine visualizer in the Workflow and Template catalogs.
- **Rationale:** Allows engineers to simulate step progressions, trigger simulated errors, and observe how rollback and recovery mechanisms behave without coupling to a specific backend or frontend framework.
- **Consequences:** (+) Intuitive mental model of system state. (-) Lightweight state machine simulator required in `documentation.js`.
