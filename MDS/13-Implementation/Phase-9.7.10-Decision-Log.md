<!-- Classification: CURRENT_SPECIFICATION -->
# Master Design System (MDS) — Architecture Decision Log
## Phase 9.7.10: Unified Local Orchestrator CLI (`run_all.py`) — Final Micro-Remediation Pass #3

**Document Reference:** `MDS-DEC-9710-REV3`  
**Phase:** 9.7.10 (Unified Local Orchestrator CLI & Master Validation Pipeline)  
**Layer:** Layer M (Testing, Governance & Architectural Immutability)  
**Date:** 2026-09-27  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Status:** **ARCHITECTURE STAGE 1 — FINAL MICRO-REMEDIATION COMPLETE (Awaiting Final Implementation Authorization)**  
**Execution Context:** Microsoft Windows, Google Chrome v153, Python 3.12.8 (Pure Standard Library)  
**Implementation Guard:** Phase 9.7.10 Implementation STRICTLY BLOCKED until authorized  

---

## 1. Context & Architectural Mandate

Following the formal **Independent Architecture Audit #2 Final Review** conducted by Lead Architect Mohamed Khalid, the architecture of Phase 9.7.10 was refined to address the four final architectural requirements:

1. **Status/Severity 20-Combination Cardinality (ADR-125 & ADR-126):** Corrected cardinality to $5 \times 4 = 20$ theoretical combinations. Statically classified every permutation into `VALID`, `INVALID`, or `UNREACHABLE` with discrete handling and exit codes.
2. **Deterministic Enforcement of Illegal CACHED States (ADR-125 & ADR-126):** Updated `resolve_final_exit_code()` with an unbypassable Step 0 invariant check: any occurrence of `CACHED + CRITICAL` or `CACHED + BLOCKER` is treated as a fatal architectural violation, yielding `BLOCKER` and `Exit 2`.
3. **Formal Governance Contract for `ACTIVE_PHASE.json` (ADR-135):** Codified a tamper-proof governance contract including strict schema validation, deterministic transition graph ($\text{Phase 9.7.9 LOCKED} \to \text{Phase 9.7.10 ACTIVE} \to \text{Phase 9.7.10 SEALED} \to \text{Phase 9.7.11 ACTIVE}$), previous-phase prerequisite verification against `master_historical_registry.json`, authorization metadata, and immediate rejection of arbitrary prefix injection with `BLOCKER` (`Exit 2`), strictly preserving locked Phase 9.7.9 files.
4. **Deterministic `--ci` Preset Override & Conflict Semantics (ADR-127 & ADR-132):** Defined `--ci` as a syntactic preset expander with deterministic augmentation rules (`--strict-environment` and `--subsystem` augment; `--fast` and `--core` conflict and abort with `Exit 2`; relaxation flags do not exist).
5. **Expanded 44-Scenario Test Matrix (ADR-134):** Expanded the pre-implementation test matrix from 35 to 44 scenarios (`TEST-ORC-01` through `TEST-ORC-44`) covering all 20 normalization permutations, illegal cached state rejections, governance violations, and `--ci` override semantics.

These decisions are formally codified in ADR-120 through ADR-135 below.

---

## 2. Ratified Architectural Decisions (ADR-120 through ADR-135)

### ADR-120: Pure Orchestration Stance & Subsystem Autonomy
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** `run_all.py` is strictly a **Pure Orchestrator**. It MUST NOT re-implement or duplicate the validation logic of any subsystem.
- **Rationale:** Subsystems (Historical Guard, Governance Engine, Axe Runner, Visual Comparator, etc.) are autonomous, mature, and independently tested. The orchestrator's sole responsibility is discovery, scheduling, dispatching, de-duplication, and uniform telemetry aggregation.
- **Boundary Contract:** Modifying a rule or invariant occurs exclusively within that subsystem's domain. The orchestrator merely consumes its standardized interface.

---

### ADR-121: Four-Tier Phased Execution Pipeline (DAG Topology)
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** Structure execution as a directed acyclic graph (DAG) across 4 sequential stages with explicit dependency ordering:
  - **Stage 0: Preflight & Environment Verification:** Python version (3.12+), workspace root validation, OS detection, `ACTIVE_PHASE.json` governance verification, Chrome/Chromium discovery, protected core preflight cryptographic snapshot.
  - **Stage 1: Core Immutability & Structural Governance (Fast, File-based):**
    - Step 1.1: Historical Phase Guard (`SUB-01` with verified active phase prefix injection)
    - Step 1.2: Repository Structure Validator (`SUB-04`)
    - Step 1.3: Capability Registry Validator (`SUB-03`)
    - Step 1.4: Governance Engine (`SUB-02` - INV-001 through INV-012)
  - **Stage 2: Static Token & Semantic Code Quality:**
    - Step 2.1: Design Token DTCG Parser & Schema Check (`SUB-05`)
    - Step 2.2: CSS Architecture Scanner (`SUB-06` - 0 raw hex, 100% logical props, 0 row-reverse)
    - Step 2.3: DSSE Mathematical Harness (`SUB-07` - 37 assertions across 9 domains)
  - **Stage 3: Component, Primitive & Workflow Unit Invariants:**
    - Step 3.1: Component & Primitive Contract Assertions (`SUB-08`, `SUB-09`)
    - Step 3.2: Patterns, Templates & Workflow FSM (`SUB-10`, `SUB-11`)
    - Step 3.3: Granular Unit Test Discovery (`tests/test_*.py` de-duplicated)
  - **Stage 4: Dynamic & Live Browser Invariants (Profile-gated):**
    - Step 4.1: Local Mock HTTP Server Startup (`SUB-12`)
    - Step 4.2: Headless CDP Browser Session Launch (`SUB-12`)
    - Step 4.3: Accessibility Live Audits (`SUB-13` - Axe-core injection)
    - Step 4.4: Responsive Viewport Resizing Matrix (`SUB-14`)
    - Step 4.5: Visual Regression Snapshot Comparison (`SUB-15`)
- **Failure Propagation:** If Stage 1 fails with a `BLOCKER` (e.g. Trust Anchor violation), downstream execution halts immediately.

---

### ADR-122: Canonical Subsystem Registry & Dependency Closure Contract
- **Status:** APPROVED (Architecture Stage 1 Remediation Pass #2)
- **Decision:** The orchestrator operates on a compile-time static `ORCHESTRATOR_SUBSYSTEM_REGISTRY` covering all 15 validation subsystems. Open-ended runtime heuristic discovery is strictly prohibited.
- **Dependency Closure Specification:**
  - Targeted execution resolves the **Target Execution Closure**:
    $$\mathcal{C}(\text{target}) = \text{MandatorySafetyGates} \cup \text{TransitiveClosure}(\text{target}) \cup \{\text{target}\}$$
  - Direct dependencies are declared in `SubsystemDefinition.dependencies`.
  - Transitive dependencies are computed recursively: $\text{TransitiveClosure}(S) = \bigcup_{d \in S.\text{deps}} (\{d\} \cup \text{TransitiveClosure}(d))$.
  - DAG topological sort via Kahn's algorithm with **strict alphabetical tie-breaking** for equal-depth sibling nodes (e.g. `SUB-03` before `SUB-04`).
  - **Duplicate Dependency Collapsing:** Every subsystem in $\mathcal{C}(\text{target})$ executes exactly once.
  - **Cycle Detection:** Any cyclic dependency in the registry graph raises fatal `ORCHESTRATOR_DEPENDENCY_CYCLE` (`Exit 2`).
  - **Invalid Dependency Detection:** Dependencies referencing unregistered IDs raise fatal `ORCHESTRATOR_INVALID_DEPENDENCY` (`Exit 2`).

---

### ADR-123: Five-Tuple Composite Assertion De-Duplication Identity
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** De-duplication MUST NOT rely on naked `assertion_id`. All caching requires a **5-Tuple Composite Identity**:
  $$\mathcal{K}_{\text{assertion}} = (\text{assertion\_id}, \text{subsystem\_id}, \text{execution\_context}, \text{input\_fingerprint}, \text{validator\_version})$$
- **Components:**
  - `assertion_id`: Unique identifier (e.g. `MDS-TKN-001`, `INV-008`, `TEST-HST-01`).
  - `subsystem_id`: Canonical subsystem (`SUB-01` to `SUB-15`).
  - `execution_context`: `STATIC_FILE_SYNTAX` | `AST_GRAPH_ANALYSIS` | `RUNTIME_DOM_EVALUATION` | `HEADLESS_CDP_VIEWPORT`.
  - `input_fingerprint`: SHA-256 digest of target input file/data stream.
  - `validator_version`: Stable version of validator logic.
- **Legal Invariant for `CACHED`:** Downstream test assertions resolve to `CACHED` if and only if an upstream test with identical $\mathcal{K}_{\text{assertion}}$ passed, the input fingerprint is unmutated, the execution context matches, and no upstream blocker/critical finding occurred on the target.

---

### ADR-124: Safe Targeted Subsystem Execution & Unbypassable Gates
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** The `--subsystem <NAME>` flag provides safe targeted execution without creating an escape hatch that bypasses safety gates.
- **Unbypassable Mandatory Safety Gates:**
  1. **Stage 0 Preflight:** Always executed (Python 3.12, workspace root, `ACTIVE_PHASE.json` check, protected core preflight snapshot).
  2. **Stage 1 Core Safety Gates:** Always executed regardless of target:
     - `SUB-01` Historical Phase Guard (Trust Anchor & Cumulative Chain)
     - `SUB-04` Repository Structure Validator
     - `SUB-03` Capability Registry Validator
     - `SUB-02` Governance Engine
  3. **Direct and Transitive Dependencies:** The full dependency closure $\mathcal{C}(\text{target})$ is executed.
  4. **Postflight Core Snapshot:** Always executed before emitting final verdict.
- **Allowed Bypasses:** Only non-dependent peer subsystems (e.g. `--subsystem visual` bypasses CSS scanner, DSSE suite, and workflow FSM).
- **Forbidden Bypasses:** Skipping Stage 0, Stage 1 Core Gates, or Protected Core audits is architecturally prohibited and rejected with `Exit 2`.

---

### ADR-125: Orthogonal Separation of Execution Status and Finding Severity
- **Status:** APPROVED (Architecture Stage 1 Remediation Pass #2)
- **Decision:** Decouple operational status from diagnostic severity into two orthogonal enums:
  1. **`ExecutionStatus` (5 values):** `PASS`, `FAIL`, `DEFERRED`, `SKIPPED`, `CACHED`.
  2. **`FindingSeverity` (4 values):** `INFO`, `WARN`, `CRITICAL`, `BLOCKER`.
- **Cardinality Invariant:** The complete theoretical state space consists of exactly $5 \times 4 = 20$ combinations.

---

### ADR-126: Canonical Status & Severity Normalization Algorithm & Invariant Enforcement
- **Status:** APPROVED (Architecture Stage 1 Remediation Pass #3)
- **Decision:** Replace partial exit-code tables with a single canonical resolution algorithm enforcing all 20 combinations:
  $$\text{ResultSet} \xrightarrow{\text{Step 0: Invariant Validation}} \xrightarrow{\text{Step 1: Aggregate}} \text{HighestEffectiveSeverity} \xrightarrow{\text{Step 2: Policy/Profile}} \text{FinalExitCode}$$
  - **Step 0 (Invariant Validation):** If any result has `ExecutionStatus.CACHED` while carrying findings with `CRITICAL` or `BLOCKER` severity, an architectural invariant violation is flagged $\to$ promoted to `BLOCKER` $\to$ **Exit 2**.
  - **Step 1:** Compute $\text{MaxSeverity} = \max(\{f.\text{severity} \mid f \in \text{findings}\} \cup \{\mathtt{INFO}\})$.
  - **Step 2:** If `ExecutionStatus.FAIL` is present, promote effective severity to at least `CRITICAL`.
  - **Step 3:** If $\text{MaxSeverity} == \mathtt{BLOCKER} \implies \text{Exit 2}$.
  - **Step 4:** If $\text{MaxSeverity} == \mathtt{CRITICAL} \implies \text{Exit 1}$.
  - **Step 5:** If $\text{MaxSeverity} == \mathtt{WARN}$:
    - If `--strict` $\implies \text{Exit 1}$.
    - Else if `DEFERRED` present and `--strict-environment` $\implies \text{Exit 1}$.
    - Else $\implies \text{Exit 0}$.
  - **Step 6:** If $\text{MaxSeverity} \in \{\mathtt{INFO}, \text{None}\}$:
    - If `DEFERRED` present and `--strict-environment` $\implies \text{Exit 1}$.
    - Else $\implies \text{Exit 0}$.
- **20-Combination Classification:**
  - 18 combinations are `VALID`.
  - 2 combinations (`CACHED + CRITICAL`, `CACHED + BLOCKER`) are `INVALID` and strictly enforced to yield `Exit 2`.

---

### ADR-127: Five-Tier Policy Precedence Model & `--ci` Preset Override Semantics
- **Status:** APPROVED (Architecture Stage 1 Remediation Pass #3)
- **Decision:** Enforce a strict 5-layer precedence hierarchy for all CLI flags:
  $$\text{Execution Profile} \to \text{Target Selection} \to \text{Strictness/Environment Policy} \to \text{Failure Policy} \to \text{Isolation Policy}$$
- **`--ci` Preset Expansion Model:**
  `--ci` is a syntactic preset expander that expands to defaults: `--full` + `--isolate` + `--fail-fast` + `--strict`.
- **Override & Conflict Rules:**
  - **Augmentations allowed:** `--strict-environment` (escalates missing Chrome to Exit 1) and `--subsystem <NAME>` (narrows scope to $\mathcal{C}(\text{target})$).
  - **Redundant flags accepted:** `--ci --full`, `--ci --strict`, `--ci --fail-fast`, `--ci --isolate`.
  - **Conflicting base profiles REJECTED with Exit 2:** `--ci --fast` and `--ci --core` raise `ORCHESTRATOR_CLI_CONFLICT` (`Exit 2`).
  - **No Relaxation Flags:** No `--no-isolate` or `--no-strict` flags exist in MDS CLI.

---

### ADR-128: Process Isolation Contract (`--isolate`)
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** Define the complete IPC protocol for subprocess isolation:
  - **Process Boundary:** Spawned via `sys.executable -m MDS.10-Testing.orchestrator.worker`.
  - **Input Contract:** Passed via stdin as single-line UTF-8 JSON containing target subsystem ID, configuration, and workspace root.
  - **Output Contract:** Worker writes strictly serialized JSON telemetry to stdout on completion.
  - **Stream Ownership:** Worker captures subsystem stdout/stderr; only clean JSON is written to stdout channel; raw stderr is redirected to `artifacts/traces/<SUB_ID>.log`.
  - **Timeouts:** 15s (Stage 1), 30s (Stages 2/3), 90s (Stage 4). Timeout triggers `SIGTERM` $\to$ `SIGKILL` and logs `BLOCKER` finding (`SUBPROCESS_TIMEOUT`).
  - **Crash Handling:** Non-zero worker exit or uncaught exception caught by orchestrator and converted to `BLOCKER` finding and `Exit 2`.
  - **Signals:** Orchestrator catches `SIGINT` (Ctrl+C) and terminates all child workers cleanly.

---

### ADR-129: Protected Core Post-State Cryptographic Snapshot Contract
- **Status:** APPROVED (Architecture Stage 1 Remediation Pass #2)
- **Decision:** Replace superficial timestamp/filesystem checks with cryptographic **Preflight and Postflight SHA-256 Snapshots**:
  - **Scope:** `MDS/02-Tokens/`, `MDS/Runtime/`, `MDS/Playground/`, `MDS/Reference-Application/`.
  - **Snapshot Tuple:** Every file is mapped to $\mathcal{S}(p_{\text{rel}}) = (\text{byte\_size}, \text{sha256\_digest})$.
  - **Preflight Snapshot:** Generated in Stage 0 before any test execution.
  - **Postflight Snapshot:** Generated after all stages conclude, before emitting final report.
  - **Post-State Guarantee:**
    - Any added file $\to$ `PROTECTED_CORE_ADDED` (`BLOCKER`, Exit 2).
    - Any deleted file $\to$ `PROTECTED_CORE_DELETED` (`BLOCKER`, Exit 2).
    - Any modified file ($\text{size}$ or $\text{sha256}$ mismatch) $\to$ `PROTECTED_CORE_MODIFIED` (`BLOCKER`, Exit 2).
  - **Transient Mutation Non-Claim (Honest Boundary):**
    - Pre/post snapshot guarantees **Post-State Final Integrity**.
    - It does NOT claim to detect transient mutations that are modified and then restored exactly during execution.
    - Low-level OS filesystem write-monitoring is explicitly **OUT OF SCOPE**.

---

### ADR-130: Dual Reporting Contract (Executive Terminal Dashboard & Unified JSON Telemetry)
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** Adopt the standard Layer-M dual reporting contract:
  1. **Executive Terminal Dashboard (`ConsoleReporter`):**
     - ANSI-colorized executive summary with subsystem cards.
     - Consolidated findings table grouped by subsystem and severity.
     - Final verdict box: `PASS`, `FAIL`, or `BLOCKER`.
  2. **Unified JSON Telemetry (`run_all_telemetry.json`):**
     - Exported to `MDS/10-Testing/artifacts/run_all_telemetry.json`.
     - Standardized Layer-M schema including environment, performance contracts, stage summaries, accounting, and structured findings list.

---

### ADR-131: Cross-Phase Performance Contract Preservation
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** The orchestrator telemetry explicitly preserves and displays both performance contract tiers established in Phase 9.7.8 and Phase 9.7.9:
  - **Global Layer-M Canonical Performance Contract (ADR-100):** Warm $\le 500\text{ ms}$, Cold $\le 1200\text{ ms}$ (Advisory / Non-gating). Evaluated against Stage 1 & 2 in-memory governance/static validation.
  - **Phase 9.7.9 Local Advisory Benchmark Target (ADR-113):** Warm $\le 100\text{ ms}$, Cold $\le 300\text{ ms}$ (Advisory / Non-gating). Evaluated specifically against Step 1.1 Historical Phase Guard execution.
  - **Non-Contradiction Invariant:** The orchestrator never conflates the local target with the global contract.

---

### ADR-132: Execution Profiles & Tiered Invocation
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** Support standardized execution profiles: `--fast`, `--core` (default), `--full`, `--ci`, `--subsystem <NAME>`, `--strict`, `--strict-environment`, `--fail-fast`, `--isolate`.

---

### ADR-133: Sealed Phase Immutability & Anti-Regression Guard
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** The orchestrator incorporates Historical Phase Guard as Step 1.1 in Stage 1.
- If any historical phase baseline (Phases 9.1 through 9.7.9) detects drift, unauthorized additions, or manifest corruptions, the orchestrator reports `CRITICAL` / `BLOCKER` and refuses to proceed with downstream feature tests.

---

### ADR-134: Phase 9.7.10 Pre-Implementation 44-Scenario Test Matrix Expansion
- **Status:** APPROVED (Architecture Stage 1 Remediation Pass #3)
- **Decision:** Expand the pre-implementation test matrix from 35 to 44 scenarios (`TEST-ORC-01` to `TEST-ORC-44`) to provide 100% executable coverage for all micro-remediations:
  - Complete 20-combination status/severity normalization (`TEST-ORC-29`).
  - Illegal cached state rejection: `CACHED + CRITICAL` $\to$ `BLOCKER` / Exit 2 (`TEST-ORC-36`).
  - Illegal cached state rejection: `CACHED + BLOCKER` $\to$ `BLOCKER` / Exit 2 (`TEST-ORC-37`).
  - `ACTIVE_PHASE.json` schema validation failure (`TEST-ORC-38`).
  - Unauthorized phase prefix injection rejection (`TEST-ORC-39`).
  - Invalid non-sequential phase jump rejection (`TEST-ORC-40`).
  - Valid phase activation protocol execution (`TEST-ORC-41`).
  - Valid sealing transition in descriptor (`TEST-ORC-42`).
  - `--ci` preset expansion with `--strict-environment` (`TEST-ORC-43`).
  - `--ci` mutually exclusive profile conflict (`--ci --fast`) rejection (`TEST-ORC-44`).

---

### ADR-135: Workspace Phase Transition Governance Contract & Historical Guard Boundary
- **Status:** APPROVED (Architecture Stage 1 Remediation Pass #3)
- **Decision:** Codify a formal, deterministic phase transition governance contract without modifying locked Phase 9.7.9 files:
  - **Governance Anchor:** `MDS/13-Implementation/ACTIVE_PHASE.json` specifies the active phase descriptor matching strict JSON schema.
  - **Monotonic Progression Guard:** Progression must follow the strict graph:
    $$\text{Phase 9.7.9 LOCKED} \to \text{Phase 9.7.10 ACTIVE} \to \text{Phase 9.7.10 SEALED} \to \text{Phase 9.7.11 ACTIVE}$$
  - **Previous-Phase Check:** `previous_phase_id` in `ACTIVE_PHASE.json` MUST match the latest sealed phase in `master_historical_registry.json`. Arbitrary phase jumps (e.g. 9.7.9 to 9.7.11 skipping 9.7.10) raise fatal `BLOCKER` (`ORCHESTRATOR_PHASE_GOVERNANCE_VIOLATION`, `Exit 2`).
  - **Prefix Restriction:** `active_prefixes` must contain strictly `[active_phase_id]`. Arbitrary prefix injection is forbidden and rejected with `Exit 2`.
  - **Dynamic Engine Prefix Injection:** In Stage 0, the orchestrator sets `HistoricalGuardEngine.ACTIVE_PHASE_PREFIXES = tuple(active_prefixes)` at runtime before calling `verify_all()`.
  - **Boundary Invariant:** All locked historical phase files (Phases 9.1 through 9.7.9) remain 100% untouched and byte-identical on disk.

---

*Decision Log ratified for Phase 9.7.10 Architecture Stage 1 Final Micro-Remediation Review.*
