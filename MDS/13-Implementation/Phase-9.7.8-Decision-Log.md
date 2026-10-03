# Master Design System (MDS) — Architecture Decision Log
## Phase 9.7.8: Governance & Cross-Document Consistency Engine (Architecture Stage — Final Remediation)

**Status:** ARCHITECTURE REMEDIATED — READY FOR FINAL INDEPENDENT AUDIT  
**Phase:** 9.7.8 (Governance & Cross-Document Consistency Engine — Layer M)  
**Date:** 2026-09-26  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Target Capability:** `MDS-GOV-001` (Layer M Unified Governance & Consistency Engine)  
**Execution Context:** Microsoft Windows, Google Chrome v153, Python 3.12.8 (Pure Standard Library)  
**Implementation Guard:** Phase 9.7.8 Implementation STRICTLY BLOCKED until authorized  

---

## 1. Context & Architectural Mandate

Following the second independent architecture audit of Phase 9.7.8, the architecture was approved in 5 findings (`G-003`, `G-004`, `G-006`, `G-007`, `G-008`), while 3 findings (`G-001`, `G-002`, `G-005`) required final micro-remediation:
1. **`G-001` (Coverage Accounting):** Replace abstract coverage guarantees with a formal typed bipartite coverage relation (`DIRECT_COVERAGE`, `WRAPPED_COVERAGE`, `INDIRECT_COVERAGE`, `UNCOVERED`, `DUPLICATE_COVERAGE`), explicitly mapping the 133 core capabilities and the 37 DSSE wrapped capabilities without false numerical equality.
2. **`G-002` (Explicit 16↔32 Anatomy Mapping Artifact):** Include the complete, physical 32-to-16 mapping table in the architecture specification, defining the exact relationship for every single canonical design facet.
3. **`G-005` (Performance Terminology):** Reclassify performance metrics from "SLA Performance Target" to "Performance Benchmark Target" (Warm $\le 500$ms, Cold $\le 1200$ms), explicitly stating that these are post-implementation measurement goals.

These decisions are formally codified in ADR-087 through ADR-101.

---

## 2. Ratified Architectural Decisions (ADR-087 through ADR-101)

### ADR-087: Five-Tier Authority Hierarchy
- **Decision:** Establish a strict 5-Tier Authority Hierarchy across all MDS documents, schemas, and source code:
  - **Tier 1:** Canonical Source of Truth (Authoritative Core).
  - **Tier 2:** Architectural Realization & Binding Contracts.
  - **Tier 3:** Derived Projections & Catalogs.
  - **Tier 4:** Operational Records & Historical Tracking.
  - **Tier 5:** Advisory Guidance & Prompts.
- **Cross-Tier Precedence Rule:** $\text{Tier 1} \succ \text{Tier 2} \succ \text{Tier 3} \succ \text{Tier 4} \succ \text{Tier 5}$. A lower tier document can never override or redefine an invariant from a higher tier.

---

### ADR-088: Zero-External-Dependency Pure Python AST Parsing Architecture
- **Decision:** The Governance Engine must be implemented entirely within the Python 3.12 standard library (`re`, `json`, `pathlib`, `ast`, `hashlib`, `dataclasses`, `enum`, `typing`, `argparse`). Zero external packages.

---

### ADR-089: Normalized Intermediate Representation & Knowledge Graph
- **Decision:** The engine ingests files into an in-memory directed Knowledge Graph (Normalized IR) decoupling file parsing from invariant rule evaluation.

---

### ADR-090: Read-Only Mandate & Complete Prohibition of Automatic Document Mutation
- **Decision:** The Governance Engine is **strictly read-only**. It shall NEVER automatically rewrite, reformat, or mutate any file. Output consists of structured diagnostic reports with exact line numbers and git diff proposals.

---

### ADR-091: Context-Aware Scoping & Dual-Mode Historical Validation
- **Decision:** Historical documents (`MDS/13-Implementation/Phase-*.md`, `docs/PROJECT_HISTORY.md`) are evaluated under a **Dual-Mode Validation Contract**:
  1. *Historical Semantic Mode (Exempt):* Historical token counts, intermediate capability statuses, and discarded exploratory options (e.g. 1280px containers) are permitted to diverge from current canonical state.
  2. *Structural Integrity Mode (Strictly Enforced):* Historical files must have valid Markdown syntax, zero broken intra-repo links (`[text](url)` must resolve on disk), valid metadata, and zero implementations of banned enterprise systems.

---

### ADR-092: Five-Tier Severity Classification Model & Exit Code Protocol
- **Decision:** Establish standardized severity levels: `BLOCKER` (Exit 2), `CRITICAL` (Exit 1), `MAJOR` (Exit 1 in `--strict`, 0 default), `MINOR` (Exit 0), `ADVISORY` (Exit 0).

---

### ADR-093: Phase 9.7.9 Boundary Interface (Current Consistency vs Historical Guard)
- **Decision:** Phase 9.7.8 validates current working tree consistency and exports `MDSGovernanceGraphSnapshot` (SHA-256). Phase 9.7.9 ingests this snapshot to verify historical phase immutability.

---

### ADR-094: Phase 9.7.10 Boundary Interface (Unified Orchestrator Integration)
- **Decision:** Expose a clean programmatic Python API (`GovernanceEngine.audit_all()`) and CLI (`governance_cli.py`) for direct invocation by `run_all.py`.

---

### ADR-095: Tri-Dimensional Test Architecture & Bipartite Coverage Model [G-001]
- **Decision:** Reject numerical equality across tiers ($170 \ne 48 \ne 141$) and formalize the **Typed Bipartite Coverage Relation** $\mathcal{R} \subseteq \mathcal{C} \times \mathcal{T}$ between Capabilities ($\mathcal{C}$, $|\mathcal{C}|=170$) and Executable Tests ($\mathcal{T}$):
  - **`DIRECT_COVERAGE`:** The test directly names or targets the capability in its runner definition (e.g. 47 direct Master Harness tests; unit tests targeting specific capability IDs).
  - **`WRAPPED_COVERAGE`:** A single composite test wraps and verifies multiple atomic capabilities. Master Harness Test 48 (`MDS-DSS-004`) wraps all 37 DSSE mathematical capabilities:
    $$\forall c \in \{\text{MDS-DSS-001}, \dots, \text{MDS-DSS-037}\}, \quad (c, \text{MDS-DSS-004}) \in \mathcal{R}_{\text{WRAPPED}}$$
  - **`INDIRECT_COVERAGE`:** Subsystem unit tests verifying underlying helpers, parsers, or mock classes supporting a capability.
  - **`DUPLICATE_COVERAGE`:** A capability covered by $\ge 2$ distinct tests across different tiers (e.g. Master Harness + Browser Live). Desirable cross-layer redundancy.
  - **`UNCOVERED`:** Any capability with degree 0 in $\mathcal{R}$. Emits a **`CRITICAL`** finding if $|\text{UNCOVERED}| > 0$.
- **Independence of Dimensions:**
  - $N_{\text{cap}} = 170$ (Declarative specifications in `registry.json`)
  - $N_{\text{master}} = 48$ ($47_{\text{direct}} + 1_{\text{wrapped}}$ integration suites in `run_tests.py`)
  - $N_{\text{unit}} = 141$ (Granular unit test methods in `tests/`)

---

### ADR-096: Component Anatomy Reconciliation & Physical Mapping Artifact [G-002]
- **Decision:** Formally reconcile the two anatomy definitions:
  - **Canonical Design Standard (32 Points):** The authoritative macro-architectural design standard, defining all 32 exhaustive facets of an enterprise UI component or template.
  - **Executable Implementation Contract (16 Points):** The synthesized delivery standard for component code and markdown specifications, clustering the 32 design facets into 16 concrete structural headings.
  - **Artifact Mandate:** The complete, exhaustive 32-to-16 mapping table must be physically embedded in `Phase-9.7.8-Governance-Architecture.md` as an authoritative governance artifact.
  - **Layer 07 Templates:** Canonical templates natively enforce the full 32-Point Template Anatomy Standard.

---

### ADR-097: Deterministic Intra-Tier 1 Authority Precedence [G-003]
- **Decision:** Establish a deterministic Four-Rank Intra-Tier Precedence Order within Tier 1:
  $$\text{Rank 1: Master Specification} \succ \text{Rank 2: Canonical Token Repository (DTCG)} \succ \text{Rank 3: Layer Specs (01–07)} \succ \text{Rank 4: Domain Engines (DSSE)}$$

---

### ADR-098: Knowledge Graph Schema & Semantic Identity Model [G-004, G-008]
- **Decision:** Formalize Knowledge Graph schema with 12 Node Types, 10 Edge Types, mandatory node metadata, and a Canonical Concept Dictionary (`ConceptDictionary`) with a 4-stage semantic normalization pipeline.

---

### ADR-099: Markdown Parser Contract [G-006]
- **Decision:** Specify 11 supported grammar structures, prohibit silent line drops, and define tri-state outcomes (`PARSE_SUCCESS`, `PARSE_PARTIAL`, `PARSE_FAILURE`).

---

### ADR-100: Performance Benchmark Target Qualification [G-005]
- **Decision:** Terminology corrected from "SLA Performance Target" to **"Performance Benchmark Target"**:
  - Warm Target: $\le 500\text{ ms}$ (Python 3.12, x86_64, NVMe SSD, warm OS cache).
  - Cold Target: $\le 1200\text{ ms}$ (clean cache first execution).
  - Explicit Status: These are post-implementation measurement targets, not verified facts. Slower runs emit `ADVISORY` warnings without failing the correctness gate.

---

### ADR-101: Tri-Dimensional Governance Reporting Protocol [G-001]
- **Decision:** Governance telemetry and terminal dashboards must report the three testing tiers independently:
  ```text
  Capabilities Inventory : 170 Total (133 Core + 37 DSSE) | 170 Active | 0 Deferred | 0 Uncovered
  Master Harness Suites  : 48 Defined | 48 Executed | 48 Passed (1 wrapper = 37 capabilities)
  Unit Discovery Battery : 141 Defined | 141 Executed | 141 Passed
  Coverage Verification  : 100% of capabilities mapped (170 direct, 37 wrapped, 213 indirect, 167 duplicate, 0 uncovered)
  ```
- **Rationale:** Ensures complete transparency without false equivalence.

---

### ADR-102: Canonical Capability Coverage Relation Matrix Artifact & Deterministic Accounting [G-001]
- **Decision:** Ratify `MDS/13-Implementation/Phase-9.7.8-Capability-Coverage-Matrix.md` as the authoritative canonical artifact mapping all 170 capabilities deterministically to their test relations.
- **Formal Computation Model:**
  $$\text{coverage}(C) \equiv \{ (C, \text{rel\_type}, T) \in \mathcal{R} \}$$
  $$\text{UNCOVERED}(C) \iff \text{coverage}(C) = \emptyset$$
  $$\text{DUPLICATE\_COVERAGE}(C) \iff |\text{coverage}(C)| > 1$$
  $$\text{WRAPPED\_COVERAGE}(C, T) \iff T \text{ is explicitly declared as a wrapper for } C$$
  $$\text{DIRECT\_COVERAGE}(C, T) \iff T \text{ directly targets or asserts } C$$
  $$\text{INDIRECT\_COVERAGE}(C, T) \iff T \text{ validates a supporting subsystem required by } C$$
- **Error Handling Protocol:**
  - Invalid relation type $\to$ Governance `ERROR` (`CRITICAL`).
  - Missing test reference on disk $\to$ Governance `ERROR` (`CRITICAL`).
  - Unknown capability ID $\to$ Governance `ERROR` (`CRITICAL`).
  - Zero coverage ($|\text{coverage}(C)| = 0$) $\to$ `CRITICAL Blocker` (Exit 2).
- **Ground Truth Statistics:**
  - Total Capabilities: 170 (133 Core Systemic + 37 DSSE Mathematical)
  - Direct Relations: 170
  - Wrapped Relations: 37 (Suite 13 Test 4: `run_tests.py::MDSTestRunner.MDS-DSS-004` wrapping `MDS-DSS-001` through `037`)
  - Indirect Supporting Relations: 213 (across 15 subsystem unit test modules)
  - Duplicate-covered Capabilities: 167 (healthy defense-in-depth)
  - Single-covered Capabilities: 3 (`MDS-EXP-001`, `002`, `003` direct in master runner)
  - Uncovered Capabilities: 0 ($|\text{UNCOVERED}| = 0$)

---

### ADR-103: Resolution of INV-012 Link Scope, Document Tier Attribution, and Link Ledger
- **Context:** Independent Implementation Audit identified ambiguity regarding the structural validation boundary of historical documents and README/advisory pointers under Invariant INV-012.
- **Architectural Decision:**
  1. **Strict Structural Validation Invariant:** Strict structural validation (valid Markdown, valid metadata, zero broken intra-repository links) applies uniformly to all documents across `MDS/` and `docs/`. Historical documents (Tier 4) are semantically exempt from obsolete counts, statuses, and discarded decisions, but are NOT exempt from structural link integrity.
  2. **Empirical Fact Finding:** An exhaustive audit verified that Tier 4 Historical phase documents contain **exactly 0 broken links**. All 9 broken links across the repository reside in active documents:
     - 8 links in **Tier 5 Advisory Guidance (Layer Pointer READMEs)** (`00-Research`, `08-Experience-States`, `11-AI`, `12-Governance`).
     - 1 link in **Tier 2 Architectural Realization (Runtime Spec Header)** (`Runtime/primitives/README.md`).
  3. **Mechanical Ledger & Attribution:** The 9 findings are attributed to concrete historical causes (typographical singular/plural mismatch, pre-standardization provisional names, or legacy phase prefixes). Every finding is mechanically tagged with `source_file`, `target`, `classification`, `validation_mode`, `severity`, and `reason`.
  4. **Quality Gate & Severity Contract:**
     - In **Standard Mode**, these 9 findings are classified as `MAJOR` (tracked structural defects; non-blocking, Exit Code 0).
     - In **Strict Mode (`--strict`)**, any `MAJOR` finding triggers Exit Code 1 (blocking).
     - Findings must never be suppressed, quarantined, or downgraded to obtain an artificial PASS.
  5. **Advisory Performance Classification:** Performance telemetry thresholds (Warm $\le 500$ms, Cold $\le 1200$ms) are strictly **Advisory Benchmark Targets**, not mandatory architectural quality gates.

---

*Decision Log ratified for Phase 9.7.8 Architecture Final Independent Audit.*

