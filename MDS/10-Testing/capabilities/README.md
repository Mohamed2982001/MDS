# Master Design System (MDS) — Capability Registry Specification
**Phase 9.7.2: Unified Test Capability Registry & Architecture**
**Status:** Certified & Active
**Canonical File:** `MDS/10-Testing/capabilities/registry.json`
**Schema:** `MDS/10-Testing/capabilities/schema.json`

---

## 1. Architectural Purpose

The **MDS Capability Registry** serves as the immutable, machine-readable single source of truth for all verification and quality assurance capabilities across the Master Design System. 

Before Phase 9.7.2, test tracking was distributed across individual test suite runners, documentation matrices, and historical session logs. The Capability Registry unifies all 170 architectural verification invariants into a strictly typed, schema-validated JSON catalog that can be deterministically audited, queried, and orchestrated by CI/CD pipelines.

---

## 2. Capability Data Model

Every capability record in `registry.json` adheres to `schema.json` (Draft-07 JSON Schema) and provides the following canonical fields:

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `string` | Unique, immutable identifier matching `^MDS-[A-Z0-9]+-[0-9]{3}$` (e.g., `MDS-REF-001`, `MDS-TKN-003`). |
| `name` | `string` | Concise, human-readable capability title. |
| `description` | `string` | Exhaustive description of the architectural invariant verified. |
| `layer` | `string` (enum) | The system architecture layer under test (14 canonical layers). |
| `category` | `string` (enum) | Verification classification (8 canonical categories). |
| `execution` | `string` (enum) | Execution harness type (`PYTHON_UNIT`, `PYTHON_STATIC`, `AST_PARSER`, `BROWSER_AUTOMATION`, `DOC_SCANNER`, `COMPOSITE_HARNESS`). |
| `severity` | `string` (enum) | Failure severity and CI exit gate consequence (`BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `WARNING`, `INFO`). |
| `status` | `string` (enum) | Lifecycle status (`ACTIVE`, `QUARANTINED`, `DEFERRED`, `DISABLED`). |
| `owner` | `string` | Engineering domain team responsible for capability maintenance. |
| `runner` | `object` | Executable mapping containing `file` (relative path), `entrypoint`, and `type`. |
| `artifacts` | `string[]` | Diagnostic files, reports, or diffs generated upon execution. |
| `depends_on` | `string[]` | Prerequisite capability IDs that must pass before this test executes. |
| `wraps` | `string[]` | Sub-assertion capability IDs wrapped by this composite test (anti-double-counting). |
| `deferred_reason` | `string \| null` | Mandatory rationale if status is `DEFERRED`; null otherwise. |
| `quarantine_reason` | `string \| null` | Mandatory rationale and tracking ticket if status is `QUARANTINED`; null otherwise. |
| `disabled_reason` | `string \| null` | Mandatory rationale if status is `DISABLED`; null otherwise. |

---

## 3. Canonical Taxonomies

### 3.1 The 14 Canonical System Layers

The Master Design System defines 14 orthogonal verification layers:

1. **`A_REPOSITORY`**: Filesystem integrity, zero npm dependencies, repository structure.
2. **`B_TOKENS`**: W3C DTCG tokens, schema conformity, token counts, alias graphs, compilation.
3. **`C_CSS`**: CSS architecture, cascade layers (`@layer`), logical properties, zero raw hex, zero `row-reverse`.
4. **`D_COMPONENTS`**: Canonical 19 Custom Elements, modular controllers, 44px hit-box rule, focus rings.
5. **`E_PRIMITIVES`**: Layout primitives (Container, Stack, Inline, Grid, Cluster), depth triad, typography hierarchy.
6. **`F_PATTERNS_WORKFLOWS_TEMPLATES`**: Canonical 8 patterns, 6 workflows, 6 templates, FSM transitions, composition laws.
7. **`G_DSSE`**: Design System Selection Engine 5-pillar mathematical model and 8 calibration scenarios.
8. **`H_REFERENCE_APPLICATION`**: Reference App integration, 4 mock roles, AI human-in-the-loop FSM projection.
9. **`I_BROWSER`**: Headless browser lifecycle, CDP bridge, DOM rendering validation.
10. **`J_ACCESSIBILITY`**: WCAG 2.1 AA/AAA contracts, axe-core scans, screen reader live regions, focus trapping.
11. **`K_RESPONSIVE`**: Multi-viewport layout adaptation (320px, 768px, 1024px, 1440px), recomposition invariants.
12. **`L_VISUAL`**: Pixel-diff regression, multi-theme visual snapshots (Light, Dark, High Contrast).
13. **`M_GOVERNANCE`**: Architecture decision records, deprecation lifecycles, documentation consistency.
14. **`N_PHASE_GUARD`**: Strict phase gating, zero modifications to locked runtime assets.

### 3.2 The 8 Canonical Test Categories

1. **`STATIC`**: Source code analysis, AST parsing, token discovery, file presence checks.
2. **`UNIT`**: Deterministic functional logic, mathematical algorithms (DSSE), parser rules.
3. **`INTEGRATION`**: Cross-module contracts, Custom Element registration, CSS layer resolution.
4. **`BROWSER`**: Real DOM rendering, live event dispatching, browser subprocess execution.
5. **`ACCESSIBILITY`**: Automated WCAG audits, ARIA semantics, keyboard focus management.
6. **`RESPONSIVE`**: Viewport reconfiguration, fluid typography scaling, breakpoint enforcement.
7. **`VISUAL`**: Screenshot diffing, perceptual color comparison, layout stability.
8. **`GOVERNANCE`**: Policy enforcement, documentation sync, architecture review gates.

### 3.3 The 6 Severity Levels & CI Exit Gate Semantics

| Severity | Definition | CI Exit Code | Gate Consequence |
| :--- | :--- | :---: | :--- |
| **`BLOCKER`** | Catastrophic failure (broken parser, missing core file, circular dependency). | `1` | Pipeline aborts immediately. Zero code can merge. |
| **`CRITICAL`** | Severe architectural violation (WCAG failure, missing role, broken FSM guard). | `1` | Pipeline fails. Mandatory remediation required. |
| **`MAJOR`** | Quality violation (token leakage, physical property, missing CSS layer). | `1` | Pipeline fails unless explicitly exempted. |
| **`MINOR`** | Non-breaking quality deviation (documentation typo, deferred feature notice). | `0` | Pipeline passes with recorded warning. |
| **`WARNING`** | Deprecation notice or upcoming architectural shift. | `0` | Pipeline passes with advisory notice. |
| **`INFO`** | Telemetry, benchmarking metrics, and test execution statistics. | `0` | Informational only. |

### 3.4 The 4 Lifecycle Statuses

- **`ACTIVE`**: Fully implemented and executable in the current test runner.
- **`DEFERRED`**: Formally documented capability deferred to a designated future milestone (e.g. headless browser runner). Requires non-null `deferred_reason`.
- **`QUARANTINED`**: Flaky or unstable test temporarily isolated from blocking CI. Requires non-null `quarantine_reason`.
- **`DISABLED`**: Permanently retired or superseded capability. Requires non-null `disabled_reason`.

---

## 4. Test Accounting & Derivable Invariants

The registry enforces an exact, non-negotiable mathematical accounting invariant ratified during the Phase 9.6 Final Re-Audit:

$$\mathbf{167\ \text{Active Executable Assertions}} + \mathbf{3\ \text{Deferred Capabilities}} = \mathbf{170\ \text{Total Unique Capability IDs}}$$

$$\mathbf{37\ \text{Wrapped Assertions (DSSE Suite executed via Harness Composite)}}$$

### 4.1 Granular Breakdown by Source Suite

| Source Suite | Runner Path | Unique IDs | Active | Deferred |
| :--- | :--- | :---: | :---: | :---: |
| **Reference Application** | `MDS/Reference-Application/tests/test_reference_app.py` | 15 | 15 | 0 |
| **Playground Laboratory** | `MDS/Playground/tests/test_playground.py` | 13 | 13 | 0 |
| **Components Runtime** | `MDS/Runtime/components/tests/test_components_runtime.py` | 18 | 18 | 0 |
| **Primitives Runtime** | `MDS/Runtime/primitives/tests/test_primitives_runtime.py` | 30 | 30 | 0 |
| **Token Runtime** | `MDS/Runtime/tokens/tests/test_token_runtime.py` | 13 | 13 | 0 |
| **DSSE Mathematical Suite** | `MDS/10-Testing/test_dsse.py` | 37 | 37 | 0 |
| **Master Harness Non-DSSE** | `MDS/10-Testing/run_tests.py` | 44 | 41 | 3 |
| **Total** | — | **170** | **167** | **3** |

### 4.2 The 3 Deferred Capabilities

The following capabilities are formally registered as `DEFERRED` pending Phase 9.7 browser automation stages:
1. `MDS-A11Y-004`: Dynamic axe-core live injection in rendered DOM (Deferred to Stage 9.7.5).
2. `MDS-RWD-003`: Headless viewport resizing automation across 320px–1440px (Deferred to Stage 9.7.6).
3. `MDS-VIS-001`: Pixel-diff snapshot automation across themes and RTL (Deferred to Stage 9.7.7).

---

## 5. Registry Validation

The capability registry is programmatically guarded by `MDS/10-Testing/registry/validator.py`:

```bash
# Validate the canonical registry
python MDS/10-Testing/registry/validator.py

# Run registry validator unit tests (12 mandatory failure modes)
python MDS/10-Testing/tests/test_registry_validator.py
```
