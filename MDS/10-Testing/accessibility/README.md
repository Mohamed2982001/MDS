# MDS Dynamic Accessibility Automation Engine (Layer I)

**Package:** `MDS/10-Testing/accessibility`  
**Phase:** 9.7.5 — Dynamic Accessibility Automation / axe-core Promotion  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Promoted Capability:** `MDS-A11Y-004` (Promoted from `DEFERRED` $\to$ `ACTIVE`)  

---

## 1. Architectural Mission

The Dynamic Accessibility Automation Engine promotes capability `MDS-A11Y-004` from a deferred placeholder to a fully operational, live browser accessibility audit engine using **axe-core** inside the approved Browser Automation Runner Bridge (`MDS/10-Testing/browser`).

It enforces the inviolable **No False-Green Principle**:
- Successfully loading axe-core does **NOT** equal passing accessibility.
- A passing result (`PASS`) is issued **strictly and only** when axe-core executes against the live rendered DOM and discovers **0 violations exceeding the configured policy threshold**.
- Deliberately inaccessible elements (e.g. unlabeled inputs, missing image alt text, contrast breaches) produce deterministic failures (`FAIL`) with structured evidence.
- An environment missing axe-core or Chromium produces an explicit `DEFERRED` result, never a fabricated pass.

---

## 2. Directory Structure

```text
MDS/10-Testing/accessibility/
├── __init__.py                    # Public exports
├── vendor/                        # Pinned local axe-core artifact
│   ├── axe.min.js                 # axe-core v4.13.0 (580 KB, zero runtime npm)
│   └── axe_metadata.json          # Cryptographic SHA-256 hash & SRI integrity
├── fixtures/                      # Deterministic accessibility fixtures
│   ├── accessible_fixture.html    # 100% WCAG 2.1 AA compliant baseline (0 violations)
│   ├── inaccessible_fixture.html  # Deliberate critical/serious violations
│   └── incomplete_fixture.html    # Text over complex SVG gradient (requires manual review)
├── axe_loader.py                  # Hermetic discovery and SHA-256 integrity verification
├── accessibility_models.py        # Data classes (AccessibilityResult, Violation, Node, Policy)
├── axe_runner.py                  # Chrome DevTools Protocol (CDP) injection & evaluation
├── accessibility_dispatch.py      # Bridge connecting Registry and Master Test Harness
├── evidence.py                    # Structured evidence assembly and report formatting
└── README.md                      # Architectural specification (this file)
```

---

## 3. Pinned Artifact & Hermetic Sourcing Policy

The engine adheres strictly to zero-runtime-dependency standards:
- **Source:** Pinned official `axe-core@4.13.0` extracted into `vendor/axe.min.js`.
- **Integrity Check:** `AxeLoader` computes SHA-256 on discovery and verifies against `axe_metadata.json`:
  ```text
  SHA-256: c24f097bd2f451d4f933e8bc7d8d539f8672a2ebcb5cc9f9f3eec8ca9470a0c1
  ```
- **Hermetic Guarantee:** Zero network calls or external CDNs (`cdnjs`, `unpkg`) are permitted at runtime.

---

## 4. Evaluation Policy (`MDS-Standard-WCAG-AA`)

The default policy classifies axe violations according to WCAG 2.1 Level AA criteria:

| Severity Level | Policy Action | Default Threshold |
| :--- | :--- | :---: |
| **Critical** | Immediate `FAIL` | Max 0 allowed |
| **Serious** | Immediate `FAIL` | Max 0 allowed |
| **Moderate** | Immediate `FAIL` | Max 0 allowed |
| **Minor** | Recorded as Advisory Warning in Evidence | Allowed |
| **Incomplete** | Recorded as Manual Review items in Evidence | Allowed |

---

## 5. End-to-End Execution Flow

$$\text{registry.json} \to \text{CapabilityDispatcher} \to \text{BrowserCapabilityDispatcher} \to \text{AccessibilityDispatcher} \to \text{CDPBrowserDriver} \to \text{axe-core} \to \text{AccessibilityResult} \to \text{ExecutionResult}$$

---

## 6. Test Accounting Transition

| Dimension | Phase 9.7.4 | Phase 9.7.5 | Impact |
| :--- | :---: | :---: | :--- |
| **Total Defined IDs** | 170 | 170 | Invariant 100% Preserved |
| **Active Executable** | 167 | 168 | `MDS-A11Y-004` promoted to ACTIVE |
| **Deferred** | 3 | 2 | Only `MDS-RWD-003` & `MDS-VIS-001` remain deferred |
| **Wrapped Assertions**| 37 | 37 | Preserved |
| **Quarantined** | 0 | 0 | Clean |
| **Disabled** | 0 | 0 | Clean |
