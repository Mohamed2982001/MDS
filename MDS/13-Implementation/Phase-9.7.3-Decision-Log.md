# Master Design System (MDS) — Architecture Decision Log
## Phase 9.7.3: Static Validation Suite & Semantic CSS AST Scanner

**Status:** APPROVED & RATIFIED  
**Phase:** 9.7.3 — Static Validation Suite (Layers A, C, M) & Capability Dispatch Adapter  
**Date:** 2026-09-23  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Canonical Modules:**
- `MDS/10-Testing/static/css_scanner.py`
- `MDS/10-Testing/static/repo_validator.py`
- `MDS/10-Testing/static/governance_validator.py`
- `MDS/10-Testing/static/dispatch_adapter.py`
- `MDS/10-Testing/static/static_runner.py`
- `MDS/10-Testing/tests/test_css_scanner.py`
- `MDS/10-Testing/tests/test_repo_validator.py`
- `MDS/10-Testing/tests/test_dispatch_adapter.py`

---

## 1. Context & Architectural Mandate

Following the formal approval and locking of Phase 9.7.2, Phase 9.7.3 was authorized with a strict mandate:
> **Deliver the Static Validation Suite (Layers A, C, M) and resolve Finding F-04 via an execution dispatch adapter, maintaining canonical registry accounting (170 Unique, 167 Active, 3 Deferred) and zero modifications to locked runtime code.**

---

## 2. Ratified Decisions (ADR-049 through ADR-054)

### ADR-049: Semantic CSS AST Tokenizer (Scopes A, B, C, D)
- **Decision:** Replace naive regular expression stylesheet scanners with an AST-aware tokenizer (`css_scanner.py`) enforcing the four architectural scopes ratified in 9.7.1:
  - *Scope A (`MDS/02-Tokens/`):* Primitive hex colors and physical units allowed (`EXEMPT`).
  - *Scope B (`MDS/Runtime/`, `Playground/`, `Reference-Application/`):* Strict author CSS rules: zero raw hex colors (`#[0-9a-fA-F]{3,8}\b`), 100% CSS Logical Properties (`*-inline-start/end`, `*-block-start/end`), zero `row-reverse` (WCAG 2.4.3), parent-owned spacing on component base classes.
  - *Scope C (`MDS/Runtime/tokens/dist/`):* Compiled distributions in `@layer mds.tokens` allowed.
  - *Scope D (Structural Layout):* Whitelisted layout mechanics allowed (`0`, `1px solid ...`, `100%`, `flex`, `grid`, etc.).
- **Rationale:** Naive regex scanners falsely flag ID selectors (`#app`, `#overview`) or SVG fragments (`url(#clip)`) as hex colors.
- **Consequence:** 39 author CSS files scanned (975 rules, 3,430 declarations) with 0 violations and 0 false positives.

### ADR-050: Layer A Repository Integrity & Directory Layout Guard
- **Decision:** Codify and enforce the canonical 20-directory MDS architectural layout in `repo_validator.py`:
  `00-Research`, `01-Foundations`, `02-Tokens`, `03-Primitives`, `04-Components`, `05-Patterns`, `06-Workflows`, `07-Templates`, `08-Experience-States`, `09-Accessibility`, `10-Responsive`, `10-Testing`, `11-AI`, `12-Governance`, `13-Implementation`, `AGENT`, `Documentation`, `Playground`, `Reference-Application`, `Runtime`.
- **Rationale:** Prevents directory drift, accidental file pollution, and unauthorized top-level scratch files.
- **Consequence:** All 20 canonical directories verified present with zero stray files and zero npm dependencies.

### ADR-051: Capability Dispatch Adapter Contract (Resolution of Finding F-04)
- **Decision:** Implement `CapabilityDispatcher` (`dispatch_adapter.py`) bridging the machine-readable capability registry with physical execution targets:
  - Dispatches `standalone_test` capabilities directly to `unittest.TestCase` methods or runner classes.
  - Translates `harness_capability` logical identifiers (`MDSTestRunner.<ID>`) to the corresponding suite runner method in `run_tests.py` using `HARNESS_PREFIX_MAP`.
  - Strictly preserves `DEFERRED` capabilities, returning `ExecutionStatus.DEFERRED` with reason without executing or fabricating passes.
- **Rationale:** Formally resolves Finding F-04 from the Phase 9.7.2 Independent Audit without modifying the Master Harness or runtime core.
- **Consequence:** 100% of Active Capabilities (167 / 167) successfully resolve to callable runners.

### ADR-052: Layer M Cross-Layer Governance & Anti-Leak Protection
- **Decision:** Implement `GovernanceValidator` (`governance_validator.py`) programmatically enforcing:
  - Exact token count: 188 registered DTCG tokens across 18 files.
  - Exact component count: 19 core canonical components.
  - Exact composition counts: 8 Patterns, 6 Workflows, 6 Templates.
  - 9 Deferred Enterprise Systems Guard: 0 unapproved implementations in active tiers.
  - Deferred Capabilities Guard: Exactly 3 deferred capabilities registered.
- **Rationale:** Guarantees automated detection of specification drift or unapproved scope creep.
- **Consequence:** All governance metrics verified at 100% compliance.

### ADR-053: Strict Runtime Isolation & Non-Pollution Invariant
- **Decision:** Phase 9.7.3 must author code exclusively within `MDS/10-Testing/static/`, `MDS/10-Testing/tests/`, and `MDS/13-Implementation/`.
- **Rationale:** Protected core runtime and reference application must remain locked and untouched.
- **Consequence:** Exactly 0 files and 0 bytes modified in `MDS/Runtime/`, `MDS/Playground/`, `MDS/Reference-Application/`, `MDS/02-Tokens/`.

### ADR-054: Warning Reconciliation & Composition Inventory Validation
- **Decision:** Surgically update `governance_validator.py` (`Rule M-03`) to validate canonical composition inventory specifications (`05-Patterns/`, `06-Workflows/`, `07-Templates/`) via exact relative paths matching Master Harness specifications `MDS-PAT-001`, `MDS-WKF-001`, and `MDS-TMP-001`, eliminating false-positive warning `[M-03]`. Formally classify and document the remaining intra-doc link warning as canonical advisory `WARN-A03-DOC-LINKS` (Severity `MINOR` / `WARNING` under Section 5 Failure Severity Matrix).
- **Rationale:** Shallow directory globbing in `governance_validator.py` failed to inspect category subdirectories where specifications reside. In contrast, intra-doc links in early historical research READMEs and locked runtime READMEs cannot be rewritten without violating the runtime freeze or fabricating historical records.
- **Consequence:** `Total Errors: 0`, `Total Warnings: 1` (`WARN-A03-DOC-LINKS`), 100% genuine zero-error static validation pass.

---

## 3. Implementation Verification Summary

| Component | Target Path | Verification Metric | Status |
| :--- | :--- | :--- | :---: |
| **CSS AST Scanner** | `MDS/10-Testing/static/css_scanner.py` | 39 CSS files / 3,430 decls / 0 violations | **VERIFIED** |
| **Repo Validator** | `MDS/10-Testing/static/repo_validator.py` | 20 canonical dirs / 0 stray / 0 npm | **VERIFIED** |
| **Governance Validator** | `MDS/10-Testing/static/governance_validator.py` | 188 tokens / 19 comps / 0 leaks / 3 def | **VERIFIED** |
| **Dispatch Adapter** | `MDS/10-Testing/static/dispatch_adapter.py` | 167/167 active resolved / F-04 resolved | **VERIFIED** |
| **Static Runner CLI** | `MDS/10-Testing/static/static_runner.py` | Unified runner passing in 278 ms | **VERIFIED** |
| **CSS Unit Tests** | `MDS/10-Testing/tests/test_css_scanner.py` | 10 / 10 Tests Passing | **VERIFIED** |
| **Repo Unit Tests** | `MDS/10-Testing/tests/test_repo_validator.py` | 5 / 5 Tests Passing | **VERIFIED** |
| **Dispatch Unit Tests** | `MDS/10-Testing/tests/test_dispatch_adapter.py` | 6 / 6 Tests Passing | **VERIFIED** |
| **Registry Validator** | `MDS/10-Testing/tests/test_registry_validator.py` | 18 / 18 Tests Passing (Phase 9.7.2 baseline) | **VERIFIED** |
| **Master Harness** | `MDS/10-Testing/run_tests.py` | 45 passed / 0 failed / 3 deferred | **VERIFIED** |
| **Runtime Isolation** | `MDS/Runtime/`, `Playground/`, etc. | 0 files / 0 bytes modified | **VERIFIED** |
