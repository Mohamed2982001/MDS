# MDS Implementation Decision Log — Phase 9.7: Validation & CI Automation
**Document Reference:** `MDS-IDR-9701`  
**Layer:** 13-Implementation  
**Target Specification:** [`Phase-9.7-Validation-Architecture.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/13-Implementation/Phase-9.7-Validation-Architecture.md)  
**Lead Architect & Owner:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Status:** ARCHITECTURE READY FOR REVIEW  
**Date:** 2026-09-22  

---

## 1. Executive Summary & Principles

Phase 9.7 transforms the verification of the Master Design System (MDS) from localized, semi-manual inspection scripts into a continuous, repeatable, automated validation architecture. In keeping with the architectural foundation established in IDR-001 through IDR-010, every engineering decision for Phase 9.7 is evaluated under strict criteria:
1. **Zero Runtime Pollution:** The Core Runtime (`MDS/Runtime/`) remains strictly zero-dependency and 100% downstream-isolated. No testing harness, node module, or runner artifact may leak into production packages.
2. **Deterministic Reproducibility:** Every test must produce an identical verdict regardless of whether it is executed on Windows, Linux, macOS, or a headless CI container.
3. **Zero False-Green & Zero Fabrication:** Tests must never pass by default when environments or dependencies are absent. Every skipped or deferred capability must be explicitly tracked as `DEFERRED` or `QUARANTINED`.
4. **Anti-Double-Counting:** Standalone unit tests, wrapped harness assertions, and deferred capabilities must be reconciled with mathematical precision.

---

## 2. Implementation Decision Records (IDR-011 through IDR-022)

---

### IDR-011: Browser Automation Driver — Lightweight Headless Runner Architecture

- **Context:** The three deferred capabilities from Phases 9.5 and 9.6 (`MDS-A11Y-004`, `MDS-RWD-003`, `MDS-VIS-001`) require a headless browser environment to render DOM trees, execute dynamic JavaScript, measure physical bounding rects, and capture pixel-accurate raster snapshots. We must select a browser automation approach that fulfills these requirements without burdening the repository with heavy dependencies.
- **Options Evaluated:**
  - *Option A: Global Heavyweight Playwright (`@playwright/test` via npm).* Standard enterprise choice; supports multi-browser (Chromium, Firefox, WebKit); features built-in test runner and trace viewer. Disadvantages: Heavy npm dependency footprint (~300MB+), download of 3 separate browser binaries, risk of competing with existing Python test runner.
  - *Option B: Standalone Node.js Puppeteer (`puppeteer-core` with system Chromium / Chrome).* Minimalist Node script connecting to already installed Google Chrome or Microsoft Edge via Chrome DevTools Protocol (CDP); or downloading a pinned headless Chromium shell. Disadvantages: Requires Node.js orchestration alongside Python runner.
  - *Option C: Python-Playwright (`playwright` Python package).* Single language stack unifying with Python 3.12 runner; direct programmatic API for viewport resizing, screenshots, and evaluation. Disadvantages: Requires `pip install playwright` and browser binary installation in CI/local dev.
  - *Option D: Native Chrome DevTools Protocol (CDP) via Headless Chrome Subprocess + WebSocket (Zero External Package).* Spawns system `chrome.exe` / `google-chrome` in `--headless=new` with remote debugging port; communicates over native WebSocket/HTTP using standard library (`urllib` / `json`). Disadvantages: High maintenance burden for custom CDP wire protocol client.
- **Evidence:**
  - Host environment inspection reveals `Python 3.12.10`, `Node.js v24.14.0`, and `npm 11.9.0` installed.
  - `Google Chrome` (`C:\Program Files\Google\Chrome\Application\chrome.exe`) and `Microsoft Edge` (`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`) are natively present on the developer host.
  - CI environments (e.g. GitHub Actions `ubuntu-latest`) provide native Chromium, Node, and Python out of the box.
- **Inference:** A dedicated, isolated Node.js test script located inside `MDS/10-Testing/browser/` using standard headless automation (either `playwright` or `puppeteer-core`) or an isolated Python driver provides maximum reliability. To avoid forcing npm dependencies onto consumer projects, all browser automation dependencies must be strictly sandboxed inside `MDS/10-Testing/` and executed via an orchestrated subprocess from the master Python runner.
- **Decision:** **Adopt an Isolated Subprocess Automation Architecture**. The primary entrypoint remains `python MDS/10-Testing/run_all.py`. For browser-dependent layers (Layers I, J, K, L), the runner delegates to an isolated automation bridge (`MDS/10-Testing/browser/`) powered by Playwright / Puppeteer. If no browser driver is detected in the environment, the runner gracefully marks browser assertions as `DEFERRED (Requires Headless Browser Driver)` with zero false greens, rather than throwing uncaught fatal crashes.

---

### IDR-012: Dependency Isolation & Boundary Policy — Sandboxed Testing Tier

- **Context:** MDS maintains a strict zero-dependency invariant for `MDS/Runtime/`, `MDS/Playground/`, and `MDS/Reference-Application/`. Phase 9.7 requires development dependencies (axe-core, image diffing, browser automation). We must define an inviolable boundary preventing test dependencies from polluting the runtime.
- **Evidence:** Throughout Phases 9.1 to 9.6, `package.json` was kept completely absent from root and runtime to guarantee platform neutrality across Flutter, Laravel, React, and vanilla web consumers.
- **Inference:** If a `package.json` is created at the repository root, developers and automated consumers might assume MDS is an npm-only package, conflicting with the platform-neutral design system baseline.
- **Decision:** **Enforce Sandboxed Testing Dependencies**. 
  - Any Node-based or Python-based test utilities must reside exclusively in `MDS/10-Testing/` (e.g., `MDS/10-Testing/package.json` or `MDS/10-Testing/requirements-dev.txt`).
  - The root directory and `MDS/Runtime/` shall contain zero package manifests and zero `node_modules`.
  - Continuous integration workflows install test dependencies strictly within the `MDS/10-Testing/` sub-context.

---

### IDR-013: Test Classification Taxonomy & Schema

- **Context:** Testing capabilities across tokens, primitives, components, workflows, templates, and browser validations currently use heterogeneous naming and reporting. A unified taxonomy is required.
- **Evidence:** Master test suite currently tracks 44 master capability IDs (`MDS-TOK-*`, `MDS-CMP-*`, `MDS-A11Y-*`, etc.) and 126 standalone Python unit assertions.
- **Decision:** Ratify an **8-Category Test Taxonomy** where every validation rule implements a canonical schema:
  1. `STATIC` (Layer A & Layer M: Repository, syntax, and governance integrity)
  2. `UNIT` (Layer B & Layer G: Token resolution, DSSE mathematics)
  3. `INTEGRATION` (Layer C, D, E, F: CSS cascade layers, components, primitives, patterns)
  4. `BROWSER` (Layer H & Layer I: Live DOM mounting, custom element lifecycle, router)
  5. `ACCESSIBILITY` (Layer J: axe-core automated audits, ARIA landmarks, FocusTrap)
  6. `RESPONSIVE` (Layer K: 320px–1440px viewport overflow, drawer recomposition)
  7. `VISUAL` (Layer L: Pixel diff snapshot comparison across themes/RTL)
  8. `GOVERNANCE` (Layer M & Layer N: Inventory invariants, roadmap drift, phase lock protection)
  
  **Canonical Schema for every Test Capability:**
  ```json
  {
    "id": "MDS-A11Y-004",
    "name": "Dynamic axe-core live DOM injection audit",
    "layer": "ACCESSIBILITY",
    "owner": "MDS Core Architecture",
    "executionMethod": "BROWSER_AUTOMATION",
    "failureSeverity": "CRITICAL",
    "status": "ACTIVE",
    "artifact": "artifacts/a11y/axe-violations.json"
  }
  ```

---

### IDR-014: Failure Classification & CI Gate Severity Policy

- **Context:** Not all test failures carry identical architectural implications. A typo in documentation should not be treated the same as a token cycle, broken custom element, or WCAG AA contrast failure.
- **Decision:** Establish a **6-Tier Failure Severity Model** with deterministic CI gating:
  - `BLOCKER`: Core runtime syntax error, token DAG cycle, broken component registration, or runtime directory mutation. $\to$ **CI FAILS IMMEDIATELY (Exit 1)**.
  - `CRITICAL`: Critical accessibility violation (axe-core critical/serious), broken state transition in FSM, or missing canonical component. $\to$ **CI FAILS (Exit 1)**.
  - `MAJOR`: Visual regression $\Delta > 0.1\%$ outside approved baseline, horizontal scroll overflow on mobile, or invalid logical CSS property. $\to$ **CI FAILS unless quarantined (Exit 1)**.
  - `MINOR`: axe-core moderate violation, documentation count mismatch, or deprecated token usage. $\to$ **CI PASSES with Warning Log (Exit 0)**.
  - `WARNING`: Performance hint, spatial density observation, or non-blocking styling advisory. $\to$ **CI PASSES (Exit 0)**.
  - `INFO`: Execution duration, token count summary, or baseline inventory log. $\to$ **CI PASSES (Exit 0)**.

---

### IDR-015: Dynamic Accessibility (axe-core) Promotion Strategy (`MDS-A11Y-004`)

- **Context:** Capability `MDS-A11Y-004` has been deferred since Phase 8.1.1 awaiting a headless browser runner. We must promote it to an active automated test without over-promising complete accessibility compliance.
- **Evidence:** Automated tools (such as Deque `axe-core`) reliably capture ~30–40% of WCAG violations (contrast, missing labels, ARIA roles, duplicate IDs), but cannot detect physical screen reader mispronunciations, confusing tab order, or cognitive clarity.
- **Decision:**
  1. Promote `MDS-A11Y-004` to an **Automated Dynamic Accessibility Audit**.
  2. The browser runner injects the official `axe-core` script (`v4.10+`) into rendered pages (`MDS/Playground/` specimens and `MDS/Reference-Application/` screens).
  3. Fail the CI on any violations classified by axe-core as `critical` or `serious`.
  4. Formally maintain physical screen reader testing (NVDA, VoiceOver, TalkBack) as **Level 5 — Manual Assistive Technology Testing**, documented separately and never simulated headlessly.

---

### IDR-016: Responsive Automation Strategy (`MDS-RWD-003`)

- **Context:** Capability `MDS-RWD-003` was deferred awaiting automated viewport resizing.
- **Evidence:** In Phase 9.6 live verification, we proved that at 320px viewport, the Reference Application cleanly recomposes navigation from desktop sidebar to `<mds-dialog id="dialog-mobile-nav">`.
- **Decision:**
  1. Promote `MDS-RWD-003` to an automated **Multi-Viewport Invariant Suite**.
  2. The runner programmatically renders the application across four canonical viewports:
     - `320px × 640px` (Mobile Compact — Primary Reflow Boundary)
     - `768px × 1024px` (Tablet / Portrait Viewport)
     - `1024px × 768px` (Desktop Small / Landscape)
     - `1440px × 900px` (Desktop Wide / Standard Workspace)
  3. **Automated Assertions at every viewport:**
     - Horizontal Overflow Guard: `document.documentElement.scrollWidth <= window.innerWidth` (strictly no horizontal scrollbars on body).
     - Component Reflow Guard: Tables must be wrapped in scrollable containers (`overflow-x: auto`), never expanding the document root.
     - Mobile Drawer Trigger Guard: At $\le 768\text{px}$, `#btn-mobile-nav` must be visible and have physical dimensions $\ge 44 \times 44\text{px}$.

---

### IDR-017: Visual Regression & Pixel Diffing Strategy (`MDS-VIS-001`)

- **Context:** Capability `MDS-VIS-001` was deferred awaiting a visual snapshot engine. A naive visual regression suite checking every permutation ($3\text{ themes} \times 3\text{ presets} \times 2\text{ densities} \times 2\text{ directions} \times 4\text{ viewports} \times 11\text{ screens} = 1584\text{ snapshots}$) would produce massive CI flakiness, excessive disk usage, and unmaintainable diffs.
- **Decision:**
  1. Promote `MDS-VIS-001` to a **Targeted Canonical Visual Baseline Engine**.
  2. Select a representative matrix of **12 High-Value Reference Snapshots**:
     - *Overview Dashboard:* Light / Soft / Comfortable / RTL (1440px)
     - *Overview Dashboard:* Dark / Refined / Comfortable / RTL (1440px)
     - *Overview Dashboard:* High-Contrast / Expressive / Compact / RTL (1440px)
     - *Overview Dashboard:* Light / Soft / Comfortable / LTR (1440px)
     - *Overview Dashboard Mobile:* Light / Soft / Comfortable / RTL (320px)
     - *Item Master List:* Light / Refined / Comfortable / RTL (1024px)
     - *Item Edit Stepper (Step 1):* Light / Soft / Comfortable / RTL (768px)
     - *Item Edit Stepper (Step 2 Unlocked):* Light / Soft / Comfortable / RTL (768px)
     - *AI Workspace (Reviewing State):* Dark / Expressive / Comfortable / RTL (1440px)
     - *Settings Access Matrix:* Light / Refined / Compact / RTL (1440px)
     - *Interactive Playground Button Specimen:* Light / Soft / RTL (768px)
     - *Interactive Playground Dialog Specimen:* Dark / Soft / RTL (768px)
  3. **Anti-Flakiness Controls:**
     - Await `document.fonts.ready` prior to snapshot capture to guarantee Cairo font rasterization.
     - Force `prefers-reduced-motion: reduce` and disable CSS transitions during capture.
     - Pixel comparison uses pixelmatch/Pillow with strict $\Delta < 0.1\%$ threshold.
  4. Intentional baseline updates require explicit flag: `python MDS/10-Testing/run_all.py --update-baselines`.

---

### IDR-018: Test Accounting Reconciliation & Anti-Double-Counting Mandate

- **Context:** In Phase 9.6, a discrepancy occurred due to counting wrapped test executions twice. Phase 9.7 must codify an inviolable accounting formula.
- **Decision:** Every execution of the test suite must strictly report:
  $$\text{Unique Defined Capability IDs} = \text{Executable Assertions Passed} + \text{Executable Assertions Failed} + \text{Deferred Capabilities}$$
  - Standalone tests executed within a parent capability (e.g. the 37 DSSE assertions within `MDS-DSS-004`) must be explicitly classified as **Sub-Assertions (Wrapped)** and never added to the top-level unique capability count.
  - The test harness outputs a structured machine-readable JSON summary (`test-summary.json`) verifying this equation on every run.

---

### IDR-019: Flakiness Mitigation & Quarantine Strategy

- **Context:** Browser and network automation can intermittently fail due to timing, font rendering jitter, or CPU throttling, leading to "flaky" CI pipelines that erode developer trust.
- **Decision:** Establish a formal **Quarantine Lifecycle**:
  - `ACTIVE`: Standard test executed on every CI and local run.
  - `QUARANTINED`: A test exhibiting intermittent flakiness may be placed in quarantine for a maximum of 14 days with an associated tracking ticket and designated owner. It executes during CI, but a failure outputs a `WARNING` rather than failing the build.
  - `DEFERRED`: Capability requiring external infrastructure (e.g., physical screen readers) not present in standard CI.
  - `DISABLED`: Permanently deprecated test awaiting architectural removal.
  - **No Silent Skips:** Any test bypassed without an explicit `QUARANTINED` or `DEFERRED` declaration causes the CI gate to fail immediately.

---

### IDR-020: Zero False-Green Mandate & Unified Orchestrator Architecture

- **Context:** The current repository requires executing separate test scripts (`run_tests.py`, `test_reference_app.py`, `test_playground.py`, etc.).
- **Decision:** Build a single canonical entrypoint:
  ```bash
  python MDS/10-Testing/run_all.py
  ```
  - The orchestrator executes validation layers in strict dependency order:
    1. Static & Integrity (Layers A, M)
    2. Tokens & Compile (Layer B)
    3. CSS & Runtime Architecture (Layers C, E)
    4. Component & Pattern Contracts (Layers D, F)
    5. DSSE Mathematical Verification (Layer G)
    6. Reference Application Unit (Layer H)
    7. Browser Automation (Layers I, J, K, L)
    8. Governance & Historical Phase Invariants (Layer N)
  - Supports ergonomic flags:
    - `--fast`: Runs Layers A through H (zero browser dependency, sub-second execution).
    - `--browser`: Runs browser, accessibility, responsive, and visual layers.
    - `--full`: Complete regression run including all executable layers.
    - `--json`: Outputs structured JSON report to `MDS/10-Testing/artifacts/reports/`.

---

### IDR-021: Static CSS Semantic Parsing vs Naive Regex Validation

- **Context:** CSS validation (Layer C) must verify zero raw hex colors, 100% logical properties, and zero `row-reverse`. Naive regular expressions produce false positives on strings like `#ref-app-main` (an element ID) or URLs in comments.
- **Evidence:** Previous regex scripts required complex lookaround assertions (`(?<![\w-])#[0-9a-fA-F]{3,8}\b`) and comment stripping to avoid flagging valid selectors.
- **Decision:** Implement **CSS AST Tokenizer / Semantic Scanner** in Python:
  - Strips CSS comments cleanly.
  - Distinguishes CSS Selectors (`#my-id`) from CSS Property Values (`#fff`).
  - Flags raw hex colors only when found in property value positions (`color`, `background`, `border`, etc.).
  - Accurately identifies physical property keys (`margin-left`, `padding-right`, `left`, `right`) while ignoring custom property names that contain those substrings (e.g. `--mds-custom-left-offset` if any existed).

---

### IDR-022: Historical Phase Regression Protection (Phase Guard)

- **Context:** Future modifications to MDS must never silently break contracts established in locked phases (Phase 9.1 through 9.6).
- **Decision:** Implement a dedicated **Phase Regression Guard (Layer N)**:
  - Cryptographic checksum / timestamp / structural check of `MDS/Runtime/` to detect unauthorized modifications.
  - Contract check verifying that `MDS/Playground/` remains isolated from `MDS/Runtime/`.
  - Contract check verifying that `MDS/Reference-Application/` remains a pure downstream consumer.
  - Any regression in Phase 9.2 through 9.6 immediately halts the validation suite with a `BLOCKER` violation.

---

## 3. Phase 9.7.1 Architecture Hardening

Following the independent review of the Phase 9.7.1 Architecture Gate by Lead Architect Mohamed Khalid, four foundational architectural dimensions were identified as requiring rigorous hardening prior to implementation authorization:

---

### Hardening Item 1: Visual Regression Strategy — Targeted Orthogonal Baseline Matrix

- **Issue Identified:** The initial architecture proposed a "12-baseline pixel comparison" while simultaneously declaring four visual axes: Modes (3: Light, Dark, High-Contrast) $\times$ Presets (3: Soft Modern, Refined Minimal, Expressive) $\times$ Directions (2: LTR, RTL) $\times$ Viewports (4: 320, 768, 1024, 1440). A naive Cartesian product across these axes yields $3 \times 3 \times 2 \times 4 = 72$ combinations per view (and $72 \times 11 = 792$ across all screens). The decision to select 12 baselines was not formally justified against the full Cartesian space.
- **Decision:** Ratify an **Orthogonal Array Testing Strategy (OATS)** utilizing a deterministic **12-Baseline Targeted Matrix**. Do NOT expand to 72 or 792 image snapshots.
- **Rationale & Mathematical Justification:**
  1. *Combinatorial Inefficiency & Flakiness:* Capturing 72–792 full-page raster snapshots introduces severe CI latency (~5–10 minutes in image processing), massive disk bloat in git/artifact storage (~200MB+ per build), and high susceptibility to non-deterministic antialiasing/GPU jitter across CI runners.
  2. *Orthogonal Coverage Law:* The visual axes in MDS are largely orthogonal:
     - The *Preset* axis controls component radii (`border-radius`) and surface shadows (`box-shadow`), which are invariant to viewport width.
     - The *Mode* axis controls color tokens (`--mds-color-*`), which are invariant to layout reflow.
     - The *Direction* axis controls inline inversion (`dir="rtl"` vs `dir="ltr"`), which operates at the layout engine level.
     - The *Viewport* axis controls responsive breakpoints (`@media` queries and container queries).
  3. Testing every preset across all 4 viewports in both directions is redundant because preset tokens do not change responsive breakpoint behavior.
- **The Canonical 12-Baseline Candidate Registry:**
  | Baseline ID | Screen Target | Mode | Preset | Density | Direction | Viewport | Target Verification Intent |
  | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
  | `BL-01` | Dashboard Overview | Light | Soft Modern | Comfortable | RTL | `1440×900` | Default enterprise reference baseline (KPIs, Charts, Grid) |
  | `BL-02` | Dashboard Overview | Dark | Refined Minimal | Comfortable | RTL | `1440×900` | Dark surface luminance contrast, slate borders, refined radii |
  | `BL-03` | Dashboard Overview | High-Contrast | Expressive | Compact | RTL | `1440×900` | WCAG AAA high-contrast borders, dense layout, expressive accent |
  | `BL-04` | Dashboard Overview | Light | Soft Modern | Comfortable | LTR | `1440×900` | Full LTR bidirectional layout inversion (sidebar on left, metrics start) |
  | `BL-05` | Dashboard Overview | Light | Soft Modern | Comfortable | RTL | `320×640` | Extreme mobile reflow, hidden desktop sidebar, visible hamburger button |
  | `BL-06` | Item Master List | Light | Refined Minimal | Comfortable | RTL | `1024×768` | Data grid table layout, regional horizontal scroll, search filter pattern |
  | `BL-07` | Multi-Step Item Edit | Light | Soft Modern | Comfortable | RTL | `768×1024` | Stepper Step 1 active, Step 2 locked (`aria-disabled="true"`), form inputs |
  | `BL-08` | Multi-Step Item Edit | Light | Soft Modern | Comfortable | RTL | `768×1024` | Stepper Step 2 unlocked, Step 1 validated, badge update |
  | `BL-09` | AI Workspace | Dark | Expressive | Comfortable | RTL | `1440×900` | AI human-in-the-loop canvas in `REVIEWING` state with action buttons |
  | `BL-10` | Settings & Access Matrix | Light | Refined Minimal | Compact | RTL | `1440×900` | User permissions data grid, dense padding, Danger Zone card |
  | `BL-11` | Playground Specimen Lab | Light | Soft Modern | Comfortable | RTL | `768×1024` | Component isolated specimens: Button variants, sizes, and states |
  | `BL-12` | Playground Specimen Lab | Dark | Soft Modern | Comfortable | RTL | `768×1024` | Component isolated specimens: Dialog Modal overlay surface depth |
- **Coverage of Remaining Combinations via Non-Visual Automation:**
  - *Layer H (Reference App Behavioral Tests):* Programmatically verifies all 11 screens across all 4 roles and 5 simulation states via DOM state assertions.
  - *Layer K (Responsive Viewports):* Evaluates all 11 screens at 320, 768, 1024, and 1440px via `scrollWidth <= clientWidth` and computed bounding rects (44 programmatic checks).
  - *Layer C (CSS Token Conformance):* Verifies token consumption across all themes without requiring raster image diffs.
- **Baseline Addition & Update Workflow:**
  - Baselines are tracked via `MDS/10-Testing/baselines/visual-manifest.json`.
  - Adding a new baseline requires adding a manifest entry specifying route, theme, viewport, and target selector.
  - Updating baselines is strictly gated: `python MDS/10-Testing/run_all.py --update-baselines` overwrites golden images only when authorized.
- **Implementation Consequence:** High CI speed (< 15 seconds for visual diffing), zero flakiness, deterministic pixel thresholding ($\Delta < 0.1\%$).

---

### Hardening Item 2: FSM Terminology & Architectural Separation

- **Issue Identified:** The draft architecture described the Reference Application as having "5 FSM stages". This risked conflating the application-specific workflow with the canonical MDS Universal FSM, creating the false perception that MDS reduced its state taxonomy from 11 states to 5.
- **Decision:** Formally codify the strict architectural separation between the **Universal MDS FSM (11 States)** and the **AI Workspace Lifecycle Projection (5 States)**.
- **Rationale & Architectural Hierarchy:**
  1. *Universal MDS FSM (Canonical Baseline Layer 06):* Governs all canonical workflows across the design system, codified in `06-Workflows/` and validated by `MDS-WKF-002`:
     $$\{ \text{IDLE}, \text{ACTIVE\_INPUT}, \text{VALIDATING}, \text{CONFIRMING}, \text{PROCESSING}, \text{STREAMING}, \text{REVIEWING}, \text{SUCCESS\_RESOLVED}, \text{ERROR\_INTERCEPTED}, \text{FATAL\_FAILURE}, \text{ABORTED\_CANCEL} \}$$
     All 11 states remain mathematically inviolable and canonical across MDS.
  2. *AI Workspace Lifecycle Projection:* Represents an **operational workflow projection/subset** tailored specifically for the generative AI human-in-the-loop interaction pattern:
     $$\text{IDLE} \xrightarrow{\text{Synthesize}} \text{PROCESSING} \to \text{STREAMING} \to \text{REVIEWING} \xrightarrow{\text{Approve}} \text{SUCCESS\_RESOLVED}$$
     Transitions on `Reject` or `Retry` route back to `IDLE`.
- **Validation Engine Rules:**
  - *Layer F (Workflow Validation):* Validates that all 6 canonical workflows implement the 11-state Universal FSM topology, guard contracts, and non-destructive retry mechanics.
  - *Layer H (Reference App Validation):* Validates that the Reference Application implements the 5-state operational projection, asserting that no unauthorized state enums (such as an independent `APPROVED` state) exist.
- **Implementation Consequence:** Zero architectural ambiguity. The Universal FSM remains 11 states; the application workflow is validated as an authorized subset projection.

---

### Hardening Item 3: CSS Validation Scope, Scan Boundaries & Semantic AST Tokenizer

- **Issue Identified:** Applying a blanket rule like "zero hex everywhere" creates catastrophic false positives against `MDS/02-Tokens/` (where primitive hex values legitimately originate) and generated distribution artifacts (`tokens.css`, where resolved values are output).
- **Decision:** Establish **Four Explicit Validation Scopes** with calibrated rules, replacing crude regex searches with a **Semantic CSS AST Tokenizer/Scanner**:
  - **Scope A: Design Token Source (`MDS/02-Tokens/`):**
    - *Classification:* Authoritative primitive definition source.
    - *Rules:* `RAW_HEX_ALLOWED`, `RAW_PX_ALLOWED`. Primitive token values (e.g. `"#0F172A"`, `"16px"`) are legitimate and necessary.
  - **Scope B: Author Runtime & Application Stylesheets (`MDS/Runtime/`, `MDS/Playground/`, `MDS/Reference-Application/`):**
    - *Classification:* Consumer and component stylesheets.
    - *Rules:* `RAW_VISUAL_LITERAL_FORBIDDEN`. Any raw hex (`#[0-9a-fA-F]{3,8}`), hardcoded RGB/HSL, unauthorized pixel font size, or pixel spacing in property values triggers a **BLOCKER** failure.
    - *Logical Properties:* `margin-left/right`, `padding-left/right`, `border-left/right`, `left`, `right` are strictly **FORBIDDEN**. Enforces `*-inline-start/end` and `*-block-start/end`.
    - *Anti-Row-Reverse:* `flex-direction: row-reverse` is strictly **FORBIDDEN**.
  - **Scope C: Generated Token Distribution Artifacts (`MDS/Runtime/tokens/tokens.css`):**
    - *Classification:* Compiled distribution output from `compile_tokens.py`.
    - *Rules:* `GENERATED_RESOLVED_VALUES_ALLOWED`. The scanner recognizes `@layer mds.tokens` as generated distribution where resolved hex literals are legitimate CSS custom property definitions.
  - **Scope D: Structural CSS Values Classification:**
    - *Classification:* Non-design layout mechanics.
    - *Rules:* Explicitly allow structural values:
      - `0` / `0px` (Reset, zero margin/padding)
      - `1px solid ...` (Divider border thickness when paired with token color)
      - `100%`, `100vw`, `100vh`, `auto` (Container sizing)
      - `transparent`, `currentColor`, `inherit` (CSS system keywords)
      - `none`, `block`, `flex`, `grid`, `inline-flex` (Display mechanics)
      - `z-index: 1`, `z-index: 10`, `z-index: 100` (Bounded elevation integers)
- **Design of Semantic CSS AST Tokenizer/Scanner (`css_validator.py`):**
  1. Strips CSS comments (`/* ... */`) before scanning.
  2. Parses text into Rules and Declarations: `selector { property: value; }`.
  3. Ignores Selectors when checking for hex (allowing `#overview`, `#ref-app-main`, `#modal-delete`).
  4. Scans only Declaration Values for forbidden color patterns.
  5. Scans Declaration Properties for physical directional keys, ignoring custom property names (`--mds-*`).
- **Implementation Consequence:** Zero false positives. Clean separation between token sources, compiled distribution, and author stylesheets.

---

### Hardening Item 4: Browser Automation Technical Contract & Concrete Execution Bridge

- **Issue Identified:** Labeling the browser layer a "Lightweight Headless Subprocess Bridge" without specifying the concrete control protocol, lifecycle, process supervision, and failure fallbacks creates high implementation risk, especially given the zero-runtime-dependency constraint.
- **Decision:** Document the **Concrete Technical Contract** for the browser automation bridge (`MDS/10-Testing/browser/`).
- **Concrete Technical Architecture:**
  1. *Subprocess Supervisor:*
     - Python orchestrator (`run_all.py`) launches the browser runner via `subprocess.Popen([sys.executable, 'MDS/10-Testing/browser/runner.py', ...])` or Node.js bridge.
     - Enforces a 60-second watchdog timeout per test suite; forcefully terminates orphan browser processes on SIGINT/timeout.
  2. *Browser Backend Selection & Discovery:*
     - The bridge searches for system-installed Chromium-based executables in order:
       1. `C:\Program Files\Google\Chrome\Application\chrome.exe` (Chrome on Windows)
       2. `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` (Edge on Windows)
       3. `/usr/bin/google-chrome` or `/usr/bin/chromium-browser` (Linux CI)
       4. `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` (macOS)
     - Runs in `--headless=new --disable-gpu --no-sandbox --remote-debugging-port=0` mode.
  3. *Control Protocol & IPC:*
     - The Python runner communicates with the browser via Chrome DevTools Protocol (CDP) WebSocket commands or via a lightweight, isolated Node.js script inside `MDS/10-Testing/browser/`.
     - Standard Actions Supported:
       - `launch()`: Starts browser, attaches CDP session.
       - `navigate(url)`: Loads URL, awaits `document.readyState === 'complete'`.
       - `set_viewport(w, h)`: Sends `Emulation.setDeviceMetricsOverride`.
       - `click(selector)`: Locates element, computes client rect, dispatches pointer events.
       - `type_text(selector, text)`: Focuses element, sets value, dispatches `input` and `change`.
       - `wait_for(selector, timeout)`: Polls DOM until element appears or timeout fires.
       - `screenshot(path, selector)`: Sends `Page.captureScreenshot`, saves PNG to disk.
       - `evaluate(script)`: Sends `Runtime.evaluate`, returns serialized JSON payload.
       - `get_console_logs()`: Collects `Log.entryAdded` and `Runtime.consoleAPICalled`.
       - `close()`: Sends `Browser.close`, kills process tree cleanly.
  4. *Dynamic axe-core Script Injection (`MDS-A11Y-004`):*
     - The bridge reads `MDS/10-Testing/vendor/axe-core/axe.min.js`.
     - Injects into page via `Runtime.evaluate({ expression: axe_script })`.
     - Executes `axe.run()` and extracts structured JSON violations.
     - Filters violations into `critical`, `serious`, `moderate`, `minor`.
  5. *Graceful Fallback & Zero False-Green Behavior:*
     - If no browser executable is discovered on the host system:
       - The runner logs: `[DEFERRED] Headless browser driver unavailable (Google Chrome/Chromium not detected on system).`
       - Layers I, J, K, L are marked `DEFERRED` in `test-summary.json`.
       - The suite exits with code 0 (or warning) without throwing an uncaught fatal exception and without marking tests as PASS.
  6. *Extensibility:*
     - The runner defines an abstract base class `BrowserDriverBase`. Replacing CDP with Playwright or WebDriver in the future requires zero changes to the test suites or assertion logic.
- **Implementation Consequence:** Robust, production-grade browser execution with zero external npm bloat in the repository root, leveraging the host's existing Chrome/Edge installation.

---

*Phase 9.7.1 Architecture Hardening codified and ratified on 2026-09-22.*

