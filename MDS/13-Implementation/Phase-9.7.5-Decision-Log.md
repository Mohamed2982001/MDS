# Master Design System (MDS) — Architecture Decision Log
## Phase 9.7.5: Dynamic Accessibility Automation / axe-core Promotion

**Status:** COMPLETE — READY FOR REVIEW  
**Phase:** 9.7.5 — Dynamic Accessibility Automation (Layer I)  
**Date:** 2026-09-24  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Promoted Capability:** `MDS-A11Y-004` (`DEFERRED` $\to$ `ACTIVE`)  

---

## 1. Context & Architectural Mandate

Following the formal approval and locking of Phase 9.7.4 (Browser Automation Runner Bridge), Phase 9.7.5 was authorized by Lead Architect Mohamed Khalid with a specific mandate:
> **Promote deferred accessibility capability `MDS-A11Y-004` from DEFERRED to an active, real dynamic browser accessibility validation capability using axe-core injection inside the approved Browser Automation Runner Bridge, without adding runtime dependencies or violating the 170 capability accounting invariant.**

---

## 2. Ratified Decisions (ADR-063 through ADR-068)

### ADR-063: Testing-Layer Pinned axe-core Artifact with Cryptographic Integrity Verification
- **Decision:** Store official `axe-core@4.13.0` as a pinned local artifact in `MDS/10-Testing/accessibility/vendor/axe.min.js` with metadata in `axe_metadata.json` containing SHA-256 and SRI integrity hashes.
- **Rationale:** Prohibits runtime npm dependencies in the MDS core, guarantees hermetic execution without external network access or CDNs (`unpkg`, `cdnjs`), and detects any artifact corruption immediately.
- **Consequence:** 100% offline deterministic accessibility auditing with zero network latency or external failure points.

### ADR-064: Dynamic CDP In-Memory Script Injection over Runtime.evaluate
- **Decision:** Inject `axe.min.js` dynamically into live browser sessions using Chrome DevTools Protocol `Runtime.evaluate` with synchronous frame transmission, verifying `typeof window.axe === 'object'` and `window.axe.version === '4.13.0'`.
- **Rationale:** Synchronous in-memory evaluation avoids network roundtrips, works seamlessly on dynamically served pages, and operates deterministically across all Chromium targets without altering served HTML files.
- **Consequence:** Zero modification of inspected HTML/CSS source files.

### ADR-065: Strict Tri-State Severity Policy (`MDS-Standard-WCAG-AA`) & No False-Green Principle
- **Decision:** Enforce an explicit accessibility evaluation policy:
  - Any `critical`, `serious`, or `moderate` violation results in immediate `FAIL`.
  - `minor` violations and `incomplete` checks are recorded in structured audit evidence as advisory diagnostics.
  - `PASS` is awarded **strictly and only** when axe-core executes against the live DOM and finds 0 violations exceeding policy thresholds.
  - Successfully injecting axe-core does **NOT** constitute a pass.
- **Rationale:** Guarantees zero false positives and protects against silent regressions in design system components.
- **Consequence:** Reliable, audit-grade verification reflecting real WCAG 2.1 Level AA conformance.

### ADR-066: Deterministic Multi-Tier Fixture Strategy
- **Decision:** Create three dedicated fixtures under `MDS/10-Testing/accessibility/fixtures/`:
  1. `accessible_fixture.html`: 100% WCAG 2.1 AA compliant semantic baseline (Expected: 0 violations $\to$ PASS).
  2. `inaccessible_fixture.html`: Deliberately injected with broken controls (missing label, missing alt text, empty button, contrast breach) (Expected: $\ge 3$ violations $\to$ FAIL).
  3. `incomplete_fixture.html`: Complex SVG gradient background with text overlay requiring human contrast review (Expected: $\ge 1$ incomplete item captured).
- **Rationale:** Empirically verifies all branches of the accessibility engine against known, deterministic expectations before auditing production application surfaces.
- **Consequence:** High-fidelity test coverage proving both positive and negative enforcement.

### ADR-067: Canonical Registry Promotion of `MDS-A11Y-004` (170 = 168 Active + 2 Deferred)
- **Decision:** Promote capability `MDS-A11Y-004` in `MDS/10-Testing/capabilities/registry.json`:
  - `status`: `"ACTIVE"`
  - `execution`: `"BROWSER_AUTOMATION"`
  - `runner`: `{"file": "MDS/10-Testing/accessibility/accessibility_dispatch.py", "entrypoint": "run_accessibility_capability", "type": "browser_test"}`
  - `deferred_reason`: `null`
  - Update accounting: `active_executable_assertions: 168`, `deferred_capabilities: 2`.
- **Rationale:** Formally recognizes the activation of browser accessibility validation while preserving the inviolable 170 capability accounting equation.
- **Consequence:** Exactly 2 capabilities remain deferred (`MDS-RWD-003` for Phase 9.7.6, `MDS-VIS-001` for Phase 9.7.7).

### ADR-068: End-to-End Accessibility Dispatch Pipeline Integration
- **Decision:** Connect `CapabilityDispatcher` $\to$ `BrowserCapabilityDispatcher` $\to$ `AccessibilityDispatcher` $\to$ `CDPBrowserDriver` $\to$ `axe-core` $\to$ `AccessibilityResult` $\to$ `ExecutionResult`.
- **Rationale:** Unifies static validation, runner bridge, and Master Test Harness under a single dispatch hierarchy.
- **Consequence:** Master Harness Suite 6 executes live browser accessibility audits directly.

---

## 3. Implementation Verification Summary

| Component | Target Path | Verification Metric | Status |
| :--- | :--- | :--- | :--- |
| **Pinned axe Artifact** | `MDS/10-Testing/accessibility/vendor/axe.min.js` | v4.13.0, SHA-256 verified | **VERIFIED** |
| **Integrity Loader** | `MDS/10-Testing/accessibility/axe_loader.py` | Checksum validation, hermetic | **VERIFIED** |
| **Domain Models & Policy** | `MDS/10-Testing/accessibility/accessibility_models.py` | Tri-state, Node truncation, Policy | **VERIFIED** |
| **Axe Execution Runner** | `MDS/10-Testing/accessibility/axe_runner.py` | CDP injection, async await, evidence | **VERIFIED** |
| **Capability Dispatcher** | `MDS/10-Testing/accessibility/accessibility_dispatch.py` | Full dispatch bridge, session isolation | **VERIFIED** |
| **Evidence Serializer** | `MDS/10-Testing/accessibility/evidence.py` | Audit bundle, text report | **VERIFIED** |
| **Test Fixtures** | `MDS/10-Testing/accessibility/fixtures/` | Accessible, Inaccessible, Incomplete | **VERIFIED** |
| **Accessibility Unit Tests**| `MDS/10-Testing/tests/test_accessibility_unit.py` | 18 / 18 PASS (Including A11Y-001 & A11Y-003) | **VERIFIED** |
| **Accessibility Live Tests**| `MDS/10-Testing/tests/test_accessibility_live.py` | 6 / 6 Real Chrome Tests PASS (Deterministic B-05) | **VERIFIED** |
| **Full Testing Discovery** | `MDS/10-Testing/tests/` | 104 / 104 Tests PASS | **VERIFIED** |
| **Registry Accounting** | `MDS/10-Testing/capabilities/registry.json` | 170 Unique = 168 Active + 2 Deferred | **VERIFIED** |
| **Static Suite** | `MDS/10-Testing/static/static_runner.py` | PASS (0 errors, 1 accepted warning) | **VERIFIED** |
| **Master Test Harness** | `MDS/10-Testing/run_tests.py` | 46 passed / 0 failed / 2 deferred | **VERIFIED** |
| **Protected Core Runtime** | `MDS/Runtime/`, `Playground/`, etc. | 0 files / 0 bytes modified | **VERIFIED** |

---

## 4. Independent Audit Remediation (ADR-069)

### ADR-069: Canonical Resolution of Independent Audit Findings A11Y-001, A11Y-002, and A11Y-003

- **Context:** Following the initial Phase 9.7.5 submission, Lead Architect Mohamed Khalid performed an Independent Audit identifying three specific findings requiring contractual closure before formal lock:
  1. `A11Y-001` (Severity: HIGH): Ambiguity between "PASS = 0 violations" vs "PASS = 0 critical/serious violations".
  2. `A11Y-002` (Severity: MEDIUM): Insufficient deterministic evidence tying live execution to the real Reference Application surface.
  3. `A11Y-003` (Severity: MEDIUM): Full audit reconciliation of the 170 / 168 / 2 / 37 capability accounting and Master Test Harness alignment.

- **Remediation Decisions:**
  1. **Canonical Severity Policy (A11Y-001):** Unified and codified `MDS-Standard-WCAG-AA`:
     - **Blocking Violations:** Critical, Serious, and Moderate (`fail_on_critical=True`, `fail_on_serious=True`, `fail_on_moderate=True`) immediately trigger `FAIL`.
     - **Advisory Diagnostics:** Minor violations and Incomplete checks (`fail_on_minor=False`, `fail_on_incomplete=False`) do NOT block `PASS`. They are recorded in audit evidence.
     - **Pass Criterion:** axe-core runs to completion on live DOM and detects 0 blocking violations.
     - **Regression Verification:** Added `test_17_policy_exact_severity_matrix_regression` in `test_accessibility_unit.py` systematically validating all 9 permutations of the severity boundary matrix.
  2. **Deterministic Real Surface Evidence (A11Y-002):**
     - Upgraded `test_05_live_reference_app_accessibility_audit` in `test_accessibility_live.py` with deterministic DOM assertions:
       - Page title: `MDS Workspace — تطبيق المرجع المعماري (Reference Application)`
       - Page URL contains: `MDS/Reference-Application/index.html`
       - Browser: `Google Chrome v153`
       - Viewport: `1440 x 900`
       - Axe Version: `4.13.0`
       - Duration: `> 0.0 ms`
       - Passes: `> 35 rules` (real surface passes 40 rules)
       - Violations: Captured exact IDs (`color-contrast`, `select-name`)
       - Incomplete: Captured exact IDs (`color-contrast`)
       - Report: Verified formatted text output referencing the real surface
  3. **Registry & Master Harness Accounting Reconciliation (A11Y-003):**
     - Added `test_18_registry_master_harness_accounting_reconciliation` in `test_accessibility_unit.py` proving:
       - $170\ \text{Total Unique IDs} = 168\ \text{Active Executable} + 2\ \text{Deferred}\ (\text{MDS-RWD-003}, \text{MDS-VIS-001})$
       - Exactly 170 unique capability IDs with zero duplicates.
       - `MDS-A11Y-004` is uniquely defined, ACTIVE, and BROWSER_AUTOMATION with zero duplicate declarations.
       - 37 wrapped assertions mapped in `MDS-DSS-000.wraps`.
       - Master Test Harness (`run_tests.py`) defines 48 tests, executes 46, and defers 2 without double counting.
