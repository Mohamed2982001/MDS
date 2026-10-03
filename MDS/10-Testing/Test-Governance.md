# Master Design System (MDS) — Test Governance & Quality Gates

**Document Layer:** 10-Testing / Governance  
**Status:** APPROVED (Phase 8.1.2 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-17  

---

## 1. Governance Vision & Inviolable Principles

The Master Design System (MDS) regression harness is designed to be the mathematical bedrock of design integrity. Every automated test must be deterministic, transparent, and reproducible.

### The 4 Governance Laws:
1. **The Zero-Fabrication Mandate:** If an environmental prerequisite (e.g. headless browser, physical screen reader) is unavailable, the test must be explicitly marked as `DEFERRED` or `NOT_EXECUTABLE`. Fabricating passes or mocking external realities is strictly prohibited.
2. **The Zero-Raw-Hex Invariant:** No consumer stylesheet (`primitives.css`, `patterns.css`, `workflows.css`, or downstream product styles) may declare hardcoded hex colors (`#hex`). Every color must reference an approved W3C DTCG CSS custom property.
3. **The Anti-Bloat Guard:** Any pull request attempting to add unapproved components, tokens, or complex enterprise systems without an approved Architectural Decision Record (ADR) will fail the CI gate immediately.
4. **The Zero Flakiness Mandate:** Tests that rely on arbitrary network requests, timers, or non-deterministic layout calculations are forbidden.

---

## 2. Test ID Grammar & Naming Conventions

All tests added to the MDS regression harness must follow the standardized grammar:

$$\text{MDS-}[\text{DOMAIN}]-\text{[001-999]}$$

### Approved Domain Codes:
- `MDS-TKN`: Token schema, DTCG syntax, alias resolution, and theme overrides.
- `MDS-PRI`: Primitives structural bounds, touch targets, and surface depth triad.
- `MDS-CMP`: Core component inventory, semantic roles, and accessibility contracts.
- `MDS-PAT`: Pattern composition laws, layout parent-ownership, and selection rules.
- `MDS-WKF`: Workflow FSM state transitions, negative transition guards, and security triad.
- `MDS-A11Y`: Accessibility contrast, keyboard focus flow, and live region semantics.
- `MDS-RTL`: Bidirectional invariants, anti-`row-reverse` enforcement, and CSS logical properties.
- `MDS-RWD`: Responsive container bounds, soft-wrap invariants, and viewport reflow.
- `MDS-EXP`: Core experience states (Empty, Error, Loading, Partial, Recovery) and contextual recovery.
- `MDS-VIS`: Visual regression snapshot diffing across theme axes.

---

## 3. Pull Request (PR) Quality Gates

Every code modification submitted to MDS must pass through the **4-Tier Quality Gate** before merge:

```text
┌─────────────────────────────────────────────────────────────┐
│                      MDS PR GATES                           │
│                                                             │
│  [Gate 1: Static AST & Syntax Verification]                 │
│   ├── Valid JSON on all 18 DTCG token files                 │
│   └── Clean Markdown syntax across architecture docs        │
│                                                             │
│  [Gate 2: Token Graph Integrity]                            │
│   ├── 0 broken or dangling alias references                 │
│   ├── Exactly 188 registered tokens                         │
│   └── 0 raw hex colors in consumer CSS                      │
│                                                             │
│  [Gate 3: Scope & Invariant Guard]                          │
│   ├── Exactly 19 Core Components                            │
│   ├── Exactly 8 Canonical Patterns                          │
│   ├── Exactly 6 Canonical Workflows                         │
│   └── 0 leaks of 9 deferred enterprise systems              │
│                                                             │
│  [Gate 4: Automated Regression Suite Execution]             │
│   └── 100% pass on executable tests in run_tests.py         │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Flaky Test Policy & Resolution Workflow

A flaky test is defined as any test that fails intermittently without source code changes.

1. **Immediate Quarantine:** Any test exhibiting flakiness must be immediately quarantined into a dedicated triage suite and excluded from blocking developer local builds.
2. **Root Cause Analysis:** Flaky tests must be diagnosed within 48 hours to determine whether the cause is timing, rendering race conditions, or environment variance.
3. **Determinism or Removal:** If a test cannot be made 100% deterministic (e.g. through explicit state machine transition validation instead of arbitrary timeouts), it must be rewritten or deferred to specialized browser integration pipelines.

---

## 5. Test Maintenance & Authoring Rules

When contributing a new test to `MDS/10-Testing/run_tests.py`:
- Use native Python standard library modules (`json`, `re`, `pathlib`, `sys`).
- Ensure Windows console encoding compatibility (`sys.stdout.reconfigure(encoding="utf-8")`).
- Keep test execution synchronous, deterministic, and fast (entire suite execution must complete in $< 2$ seconds).
- Document every new test in the [Test-Coverage-Matrix.md](file:///d:/Work/Dev/Master%20Design%20System/MDS/10-Testing/Test-Coverage-Matrix.md).
