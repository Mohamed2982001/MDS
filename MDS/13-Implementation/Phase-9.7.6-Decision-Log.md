# Master Design System (MDS) — Architecture Decision Log
## Phase 9.7.6: Responsive Viewport Automation (Architecture Stage — Remediated)

**Status:** ARCHITECTURE COMPLETE — READY FOR IMPLEMENTATION AUTHORIZATION  
**Phase:** 9.7.6 (Responsive Viewport Automation — Layer I)  
**Date:** 2026-09-24  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Target Capability:** `MDS-RWD-003` (Currently `DEFERRED` — Preserved during Architecture Phase)  
**Downstream Guard:** Phase 9.7.7 (Visual Regression Engine) STRICTLY BLOCKED  

---

## 1. Context & Architectural Mandate

Following the formal approval and locking of Phase 9.7.5 (Dynamic Accessibility Automation / axe-core Promotion), Phase 9.7.6 was authorized by Lead Architect Mohamed Khalid under strict **Architecture Phase Only** constraints. Following an independent architecture audit, four specific findings (`RWD-001` through `RWD-004`) were remediated to establish full contractual and mathematical rigor before implementation authorization.

---

## 2. Ratified Architectural Decisions (ADR-070 through ADR-077)

### ADR-070: Canonical 4-Tier Viewport Matrix (320, 768, 1024, 1440)
- **Decision:** Restrict canonical responsive testing strictly to the four foundational MDS viewport widths:
  1. `320px` — Mobile (`sm`) [1-column flow, bottom drawer, min 44px hit-box]
  2. `768px` — Tablet (`md`) [Dedicated master-detail / icon sidebar, 8-column grid]
  3. `1024px` — Desktop (`lg`) [Persistent sidebar, 12-column grid, max-width 1152px]
  4. `1440px` — Wide (`xl`) [Persistent sidebar, 12-column grid, max-width 1440px]
  Diagnostic widths (e.g. 480px, 1200px) are classified as non-canonical and prohibited from defining pass/fail contracts.
- **Rationale:** Aligns directly with `MDS/01-Foundations/03-Spacing-and-Grid.md` and `.agents/rules/03_responsive_and_devices.md`. Prevents arbitrary breakpoint proliferation.
- **Consequence:** Clean, predictable evaluation matrix across all components, patterns, and templates.

### ADR-071: Tri-Class Responsive Assertion Model (RWD-003)
- **Decision:** Partition all responsive assertions into three formal contractual classes:
  1. `HARD_CONTRACT`: Required by foundational documents or reference application architecture (e.g. 1152/1440px max-width, mobile drawer trigger presence, 44px touch-target minimum, zero horizontal overflow). Failure = immediate hard `FAIL`.
  2. `OBSERVABLE_BEHAVIOR`: Measurable responsive layout adaptations across viewports (e.g. grid column count transition, sidebar rail width collapse, table horizontal scroll container). Failure = `FAIL` when expectation violated.
  3. `INFORMATIONAL_MEASUREMENT`: Diagnostic telemetry collected for audit records (e.g. exact bounding box coordinates, computed style values, duration). **Never** determines PASS/FAIL.
- **Rationale:** Eliminates false-green passes (e.g. passing solely on `window.innerWidth == 320`) while preventing false failures from rigid over-specification of internal styles.
- **Consequence:** Senior-level test engineering rigor matching enterprise validation standards.

### ADR-072: Reusing Phase 9.7.4 CDP Browser Driver via `Emulation.setDeviceMetricsOverride`
- **Decision:** Utilize the existing standard-library `CDPBrowserDriver` (`MDS/10-Testing/browser/cdp_driver.py`) to manage viewports using Chrome DevTools Protocol `Emulation.setDeviceMetricsOverride`. Prohibit introducing Playwright, Puppeteer, Selenium, or npm packages.
- **Rationale:** Preserves the zero-dependency Python stdlib architecture established in Phase 9.7.4. CDP native device emulation allows exact pixel sizing, device scale factor configuration, and mobile touch emulation without resizing physical OS windows.
- **Consequence:** 100% hermetic, reproducible execution on any machine with Google Chrome or Chromium installed.

### ADR-073: Representative Coverage Strategy & 17-Run Deterministic Matrix (RWD-001, RWD-002)
- **Decision:** Adopt an explicit 17-run canonical execution matrix providing **representative responsive coverage across major responsive-sensitive template families**:
  - Dashboard Overview (`TMP-001` / `#/overview`): Multi-column KPI stats grid, page header, search bar, navigation.
  - List Management (`TMP-002` / `#/items`): Data tables, filter bar, pagination, action button clusters.
  - Form Edit (`TMP-004` / `#/items/edit`): Two-column form grid, stepper tabs, danger zone.
  - Remaining templates (`TMP-003`, `TMP-005`, `TMP-006`) and all 11 screens remain 100% verified by broader non-visual/reference validation suites.
  - Every run is an **independent, single-pass deterministic execution** with explicit route, viewport, theme, density, and direction definitions. Runs 13 and 14 evaluate LTR independently.
- **Rationale:** Eliminates a 528-run combinatorial explosion ($11\times 4\times 3\times 2\times 2$) while ensuring every critical responsive composition pattern is rigorously audited.
- **Consequence:** High-throughput execution ($\le 15$ seconds total) with zero ambiguity in run parameters.

### ADR-074: Bounded Layout Reflow Stabilization & Settlement Architecture
- **Decision:** Enforce a deterministic post-resize settlement algorithm before executing responsive assertions with a **hard bounded timeout**:
  1. Dispatch `Emulation.setDeviceMetricsOverride`.
  2. Wait for two consecutive animation frames (`window.requestAnimationFrame`).
  3. Wait for `document.fonts.ready` to settle typography bounding boxes.
  4. Poll root container geometry until horizontal variance $< 1.0$px across 50ms intervals.
  5. Maximum wait timeout: **1500ms**. If timeout occurs, report a deterministic failure diagnostic, never hang indefinitely.
- **Rationale:** Asynchronous layout reflow and font loading in Chromium can cause transient subpixel shifts. Bounding the timeout prevents hanging CI processes.
- **Consequence:** Fast, reliable, flake-free layout measurement.

### ADR-075: Hermetic State Isolation & Clean Session Lifecycles
- **Decision:** Provide strict state isolation between viewport test runs. For each viewport evaluation:
  - Reset single-page application hash route and modal dialogs.
  - Reset theme, density, and direction controls to expected baseline.
  - Clear ephemeral session storage / simulation states.
  - Call `Emulation.clearDeviceMetricsOverride` upon step completion.
  - Isolate multi-screen sweeps in disposable `BrowserSession` instances.
- **Rationale:** Prevents state pollution (e.g. an unclosed mobile drawer from 320px persisting into a 1024px desktop evaluation).
- **Consequence:** Every test run is independently reproducible in isolation.

### ADR-076: Capability Accounting & Status Preservation (`MDS-RWD-003`)
- **Decision:** Preserve capability `MDS-RWD-003` with status `DEFERRED` in `MDS/10-Testing/capabilities/registry.json` throughout Phase 9.7.6 Architecture:
  - `unique_defined_ids`: 170
  - `active_executable_assertions`: 168
  - `deferred_capabilities`: 2 (`MDS-RWD-003`, `MDS-VIS-001`)
  - Promotion to `ACTIVE` will occur strictly upon implementation completion, live browser verification, and independent audit clearance.
- **Rationale:** Strict adherence to the MDS phase-gate lifecycle: Architecture $\to$ Audit $\to$ Authorization $\to$ Implementation $\to$ Audit $\to$ Lock.
- **Consequence:** Zero premature registry pollution; 100% accounting integrity maintained.

### ADR-077: Decoupling CSS Viewport from Browser Window & Device Emulation (RWD-004)
- **Decision:** Explicitly decouple and classify responsive testing dimensions:
  1. CSS Viewport (`width` × `height` in CSS px): Primary MDS Design Contract under test.
  2. Browser Window Dimensions (`--window-size=1440,900`): Outer host OS process container.
  3. CDP Emulation (`Emulation.setDeviceMetricsOverride`): Automation mechanism.
  4. `deviceScaleFactor` (2.0 on Mobile/Tablet, 1.0 on Desktop): Test-environment parameter simulating high-DPI retina rendering; not an MDS design token.
  5. Mobile Emulation Mode (`mobile: true` on Mobile/Tablet, `false` on Desktop): Input & UA characteristic simulation (touch events, coarse pointer).
- **Rationale:** Prevents confusion between test infrastructure simulation parameters and design system token contracts. PASS/FAIL criteria evaluate CSS viewport layout reflow, not emulation flags.
- **Consequence:** Complete clarity between what is being tested (CSS layout contracts) and how it is simulated (CDP emulation parameters).

### ADR-077: Canonical Route & Theme Reconciliation (Audit Finding 1 & 2)
- **Decision:** Reconcile route and theme references to match the locked, approved Reference Application reality:
  1. Route for Item Edit: Canonical route is `#/items/edit` (matching `Reference-Application/app.js` line 154, 229, 303, 569). Eliminate stale architecture artifact `#/item/edit/item-101`.
  2. Mode for High Contrast: Canonical semantic mode name is `High Contrast` (MDS token mode standard). Implementation DOM/CSS attribute identifier is `high-contrast` (`data-theme="high-contrast"`).
- **Rationale:** Ensures architecture documentation is authoritative without modifying a single byte of the protected Reference Application code.
- **Consequence:** 100% alignment across Reference Application, Matrix configuration, Evidence serialization, and Architecture documentation.

---

## 3. Architecture Sign-off Matrix

| Review Criterion | Standard Mandate | Remediated Architecture Compliance |
| :--- | :--- | :--- |
| **RWD-001: Coverage Claim** | No misleading 100% template claim | Accurately defined as representative coverage of major responsive template families |
| **RWD-002: Deterministic Matrix** | Fully defined, unambiguous 17 runs | Every run explicitly defines route, viewport, theme, density, direction, session isolation |
| **RWD-003: Assertion Classes** | Hard Contract vs Observable vs Info | Formally partitioned into `HARD_CONTRACT`, `OBSERVABLE_BEHAVIOR`, `INFORMATIONAL_MEASUREMENT` |
| **RWD-004: Emulation vs Viewport**| Decouple CSS viewport from emulation | Explicitly separated; CSS viewport is the contract, emulation parameters are test settings |
| **Stabilization Timeout** | Bounded wait, no infinite hangs | Hard timeout at 1500ms; returns deterministic timeout failure diagnostic |
| **Browser Runner** | Zero npm dependencies, stdlib CDP | Reuses Phase 9.7.4 `CDPBrowserDriver` via `Emulation.setDeviceMetricsOverride` |
| **Protected Core** | 0 files / 0 bytes modified | Runtime, Playground, Reference App, Tokens completely frozen |
| **Accounting Invariant** | 170 Unique = 168 Active + 2 Deferred | 100% preserved; `MDS-RWD-003` remains DEFERRED until implementation |

---

## 4. Next Step Gate

```text
========================================================================
  PHASE 9.7.6 ARCHITECTURE COMPLETE — READY FOR IMPLEMENTATION AUTHORIZATION
  Implementation:               STRICTLY BLOCKED until authorized
  Phase 9.7.7 Visual Engine:   STRICTLY BLOCKED
========================================================================
```
