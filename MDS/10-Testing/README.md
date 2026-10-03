# Master Design System (MDS) — Testing Layer (Layer 10)

Welcome to **Layer 10 (Testing & Regression Harness)** of the Master Design System (MDS).

This directory contains the master automated test architecture, coverage matrices, findings, governance rules, and the central executable regression harness governing the entire design system.

---

## 🚀 Quick Start: Running the Automated Test Suite

From the workspace root directory, execute:

```bash
python MDS/10-Testing/run_tests.py
```

### Expected Output
```text
--- [SUITE 1: Token & Schema Integrity] ---
[PASS]     MDS-TKN-001 (Tokens): Verified exactly 18 W3C DTCG token files exist
[PASS]     MDS-TKN-002 (Tokens): All DTCG token files parse with 100% valid JSON syntax
[PASS]     MDS-TKN-003 (Tokens): Canonical token registry invariant matches exactly 188 tokens
[PASS]     MDS-TKN-004 (Tokens): All alias references resolve with 100% clean graph linkage (0 broken)
[PASS]     MDS-TKN-005 (Tokens): Consumer stylesheets enforce 100% token usage (0 raw hex in primitives, patterns, workflows)
[PASS]     MDS-TKN-006 (Tokens): All 4 multi-dimensional theme overrides present and valid
...
=========================================================================
                 MDS AUTOMATED TEST SUITE EXECUTION REPORT               
=========================================================================
Total Tests Defined:        36
Total Tests Executed:       33
  [+] Passed:               33
  [-] Failed:               0
  [*] Not Executable:       3 (Deferred to headless browser CI)
-------------------------------------------------------------------------
OVERALL STATUS: SUCCESS — 100% of executable tests PASSED with ZERO failures.
```

### Exit Codes:
- `0`: All executable tests passed (Success).
- `1`: One or more tests failed (Quality gate blocked).

---

## 📁 Directory Structure

```text
MDS/10-Testing/
├── README.md                          # This entry guide and execution manual
├── MDS-Automated-Test-Architecture.md # Master testing pyramid and taxonomy
├── Test-Coverage-Matrix.md            # Detailed 36-test tracking matrix
├── Test-Findings.md                   # Execution results, env realities, and deferred tests
├── Test-Governance.md                 # PR gates, flakiness policy, and authoring rules
└── run_tests.py                       # Central automated test runner script
```

---

## 🔍 Key Architectural Invariants Enforced
1. **Tokens (188 Tokens):** Evaluates all 18 W3C DTCG files; verifies 0 broken aliases and 0 raw hex colors in consumer CSS.
2. **Primitives (Layout, Surface, A11y, Icon):** Validates parent-owned spacing, the Surface depth triad, 44px hit-boxes, and 4-tier RTL icon mirroring.
3. **Components (19 Core Components):** Enforces exact 19-component inventory and ensures all 9 complex enterprise systems remain strictly deferred.
4. **Patterns (8 Canonical Patterns):** Validates 8-stage Pattern Selection Engine and 10 composition laws.
5. **Workflows (6 Canonical Workflows):** Simulates universal 11-state FSM transitions and verifies the Security Triad.
6. **Accessibility & RTL:** Asserts zero `row-reverse` in CSS, 100% CSS logical properties, default RTL with Cairo font, and destructive dialog Cancel focus priority.
