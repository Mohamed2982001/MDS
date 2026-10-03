# Master Design System (MDS) — Architecture Decision Log
## Phase 9.7.2: Unified Test Capability Registry & Architecture Decisions

**Status:** APPROVED & RATIFIED
**Phase:** 9.7.2 — Unified Test Capability Registry & Implementation
**Date:** 2026-09-22
**Lead Architect:** Mohamed Khalid
**Canonical Artifacts:**
- `MDS/10-Testing/capabilities/registry.json`
- `MDS/10-Testing/capabilities/schema.json`
- `MDS/10-Testing/capabilities/README.md`
- `MDS/10-Testing/registry/validator.py`
- `MDS/10-Testing/tests/test_registry_validator.py`

---

## 1. Context & Architectural Mandate

In Phase 9.7.1, the validation architecture was formally ratified (`ARCHITECTURE READY FOR IMPLEMENTATION`), establishing four critical hardening items:
1. Orthogonal Array Testing Strategy (OATS) for 12 targeted visual regression baselines.
2. Decoupled Universal 11-State FSM from the Reference App's 5-state operational projection.
3. 4 CSS scan scopes with AST parsing semantics.
4. Concrete technical contract for headless browser automation via CDP over WebSocket/IPC.

Phase 9.7.2 was authorized with a strict and singular mandate:
> **Build the Unified Test Capability Registry & Implementation without touching runtime code, and without prematurely implementing browser automation drivers.**

The registry serves as the machine-readable single source of truth for all testing capabilities across the repository.

---

## 2. Ratified Decisions (ADR-041 through ADR-047)

### ADR-041: Canonical Capability JSON Schema (`schema.json`)
- **Decision:** Formalize capability definitions using Draft-07 JSON Schema. Every capability must provide: `id`, `name`, `description`, `layer`, `category`, `execution`, `severity`, `status`, `owner`, `runner`, `artifacts`, `depends_on`, `wraps`, `deferred_reason`, `quarantine_reason`, `disabled_reason`.
- **Rationale:** Prevents ad-hoc test descriptions and guarantees that CI orchestrators, static checkers, and human auditors inspect identical metadata contracts.
- **Consequence:** `registry.json` validates with zero errors under standard `jsonschema` validators.

### ADR-042: 14 Canonical Layers and 8 Testing Categories
- **Decision:** Standardize on exactly 14 architectural layers (`A_REPOSITORY` through `N_PHASE_GUARD`) and 8 categories (`STATIC`, `UNIT`, `INTEGRATION`, `BROWSER`, `ACCESSIBILITY`, `RESPONSIVE`, `VISUAL`, `GOVERNANCE`).
- **Rationale:** Ensures complete vertical and horizontal coverage across all design system tiers, from DTCG tokens to composite application workflows and phase guards.
- **Consequence:** Eliminates arbitrary layer taxonomy drift across test suites.

### ADR-043: Mathematical Invariant & Derivable Test Accounting
- **Decision:** Enforce the exact Phase 9.6 baseline accounting invariant:
  $$\mathbf{167\ \text{Active Executable Assertions}} + \mathbf{3\ \text{Deferred Capabilities}} = \mathbf{170\ \text{Total Unique Defined IDs}}$$
  $$\mathbf{37\ \text{Wrapped Assertions (DSSE Suite executed in Harness Composite)}}$$
- **Rationale:** Eliminates double-counting ambiguity and prevents discrepancy between standalone test runners and composite harness executions.
- **Consequence:** Numbers are not hardcoded assertions of truth; they are dynamically derived and verified by `validator.py`.

### ADR-044: Status Lifecycle Gating & Explicit Rationale Mandate
- **Decision:** Strictly enforce the 4 canonical lifecycle statuses: `ACTIVE`, `DEFERRED`, `QUARANTINED`, `DISABLED`. Every non-ACTIVE capability MUST provide a non-empty rationale string (`deferred_reason`, `quarantine_reason`, `disabled_reason`).
- **Rationale:** Prevents silent test skipping or unmonitored quarantine rotting.
- **Consequence:** The 3 deferred capabilities (`MDS-A11Y-004`, `MDS-RWD-003`, `MDS-VIS-001`) are explicitly documented with their designated future milestones (Stages 9.7.5, 9.7.6, 9.7.7).

### ADR-045: Dependency Graph (DAG) with Cycle Detection
- **Decision:** Implement Directed Acyclic Graph (DAG) validation on capability `depends_on` relationships using Depth-First Search (DFS) with 3-color state tracking.
- **Rationale:** Prevents circular prerequisites that would deadlock or crash execution pipelines.
- **Consequence:** Self-dependencies (`A -> A`) and multi-node cycles (`A -> B -> A`) are caught deterministically with exact cycle paths reported.

### ADR-046: Anti-Double-Counting `wraps` Model with Referential Integrity
- **Decision:** Capabilities that execute sub-suites (such as master harness composites) must declare the wrapped capability IDs in their `wraps` array. The validator verifies referential integrity: wrapped IDs must exist in the registry and self-wrapping is forbidden.
- **Rationale:** Guarantees transparent accounting when composite runners aggregate individual unit assertions.
- **Consequence:** Full distinction between standalone capabilities and composite executions.

### ADR-047: Strict Core Isolation Invariant
- **Decision:** Phase 9.7.2 must not modify any files in `MDS/Runtime/`, `MDS/Playground/`, `MDS/Reference-Application/`, or `MDS/02-Tokens/`.
- **Rationale:** Core runtime and reference application are locked and approved under Phase 9.5 and 9.6. Testing tooling must remain downstream.
- **Consequence:** Exactly 0 files and 0 bytes were modified in protected runtime directories.

### ADR-048: Explicit Wrap Graph & Playground Entrypoint Alignment (Remediation)
- **Decision:** (1) Designate Master Harness composite DSSE runner as `MDS-DSS-000` with explicit `wraps: ["MDS-DSS-001", ..., "MDS-DSS-037"]`. (2) Align all 13 `MDS-PLG-*` capability entrypoints to exact `test_playground.py` method names. (3) Derive `wrapped_assertions` strictly from capability `wraps` arrays without metadata fallback.
- **Rationale:** Resolves Findings F-01, F-02, and F-03 from the Phase 9.7.2 Independent Audit. Eliminates ID collision on `MDS-DSS-004`, prevents `AttributeError` on playground test execution, and enforces strict dynamic derivation of wrapped assertions count.
- **Consequence:** 100% graph integrity, 0 ID collisions, and strict accounting verification with 18 / 18 validator tests passing.

---

## 3. Implementation Verification Summary

| Component | Target Path | Verification Metric | Status |
| :--- | :--- | :--- | :---: |
| **JSON Schema** | `MDS/10-Testing/capabilities/schema.json` | Valid Draft-07 JSON Schema | **VERIFIED** |
| **Capability Registry** | `MDS/10-Testing/capabilities/registry.json` | 170 Unique IDs / 167 Active / 3 Deferred / 37 Wrapped | **VERIFIED** |
| **Registry Documentation**| `MDS/10-Testing/capabilities/README.md` | Full Layer, Category, Accounting Guide | **VERIFIED** |
| **Registry Validator** | `MDS/10-Testing/registry/validator.py` | Standalone CLI + Programmatic API + Strict Wraps Derivation | **VERIFIED** |
| **Validator Unit Tests** | `MDS/10-Testing/tests/test_registry_validator.py` | 18 / 18 Tests Passing (All Failure Modes + Wraps Integrity) | **VERIFIED** |
| **Runtime Isolation** | `MDS/Runtime/`, `MDS/Playground/`, etc. | 0 Files / 0 Bytes Modified | **VERIFIED** |

