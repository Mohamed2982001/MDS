# Master Design System (MDS) — Layer M Governance Gaps & Remediation Analysis
## Phase 9.7.8: Independent Audit Findings Remediation (G-001 through G-008)

**Document Reference:** `MDS-GAP-9780`  
**Layer:** Layer M (Governance & Invariants)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Status:** ARCHITECTURAL AUDIT REMEDIATION BASELINE  
**Date:** 2026-09-26  

---

## 1. Executive Summary & Audit Remediation Status

Following the independent architecture audit of Phase 9.7.8, the initial specification was returned with status **`REQUIRES REMEDIATION`** due to 8 architectural findings (`G-001` through `G-008`).

This document records the exact root cause, architectural correction, and verification criteria for each finding, reconciling the Phase 9.7.8 architecture before implementation authorization.

---

## 2. Detailed Audit Remediation Records (G-001 through G-008)

### Finding G-001: INV-009 Test Accounting Model & Canonical Capability Coverage Matrix Artifact
- **Finding:** Initial wording incorrectly stated `170 capabilities = 48 master tests = 141 unit tests`, falsely implying numerical equality across three distinct tiers. Furthermore, the universal coverage guarantee ($\forall C \in \mathcal{C}, \text{Coverage}(C) \ge 1$) lacked a canonical line-by-line capability-to-test mapping artifact establishing deterministic coverage across tests and wrappers.
- **Root Cause:** Inappropriate mathematical notation treating separate dimensions (requirements, acceptance suites, and unit assertions) as equal quantities, combined with the lack of an explicit canonical mapping matrix.
- **Architectural Correction:**
  - Replaced the erroneous equation with the **Tri-Dimensional Traceability & Coverage Model** (ADR-095, ADR-101, ADR-102, and Architecture Section 3 `INV-009`).
  - Formalized the **Typed Bipartite Coverage Relation** $\mathcal{R} \subseteq \mathcal{C} \times \mathcal{T}$ between Declarative Capabilities ($\mathcal{C}$, $|\mathcal{C}|=170$) and Executable Tests ($\mathcal{T}$):
    - `DIRECT_COVERAGE(C, T)`: Test directly executes, names, or targets capability ID (170 direct relations across core and DSSE).
    - `WRAPPED_COVERAGE(C, T)`: Master Harness Test 48 (`run_tests.py::MDSTestRunner.MDS-DSS-004`) acts as an explicit **1-to-37 wrapper** covering all 37 DSSE mathematical capabilities:
      $$\forall c \in \{\text{MDS-DSS-001}, \dots, \text{MDS-DSS-037}\}, \quad (c, \text{WRAPPED\_COVERAGE}, \text{run\_tests.py::MDS-DSS-004}) \in \mathcal{R}$$
    - `INDIRECT_COVERAGE(C, T)`: 213 supporting relations across 15 subsystem unit test modules in `MDS/10-Testing/tests/`.
    - `DUPLICATE_COVERAGE(C)`: 167 capabilities verified by $\ge 2$ distinct tests across different tiers (healthy cross-layer redundancy).
    - `UNCOVERED(C)`: Mechanically evaluated as $\text{coverage}(C) = \emptyset$. Verified to evaluate to exactly 0 ($|\text{UNCOVERED}| = 0$).
  - **Mechanical Coverage Formulas:**
    - $\text{coverage}(C) \equiv \{ (C, \text{rel\_type}, T) \in \mathcal{R} \}$
    - $\text{UNCOVERED}(C) \iff \text{coverage}(C) = \emptyset$
    - $\text{DUPLICATE\_COVERAGE}(C) \iff |\text{coverage}(C)| > 1$
    - $\text{WRAPPED\_COVERAGE}(C, T) \iff T \text{ is explicitly declared as a wrapper for } C$
    - $\text{DIRECT\_COVERAGE}(C, T) \iff T \text{ directly targets or asserts } C$
    - $\text{INDIRECT\_COVERAGE}(C, T) \iff T \text{ validates a supporting subsystem required by } C$
  - **Handling of Invalid / Stale References:**
    - Invalid relation type $\to$ Governance `ERROR` (`CRITICAL`).
    - Missing test reference on disk $\to$ Governance `ERROR` (`CRITICAL`).
    - Unknown capability ID $\to$ Governance `ERROR` (`CRITICAL`).
    - Zero coverage ($|\text{coverage}(C)| = 0$) $\to$ `CRITICAL Blocker` (`BLOCKER`, Exit 2).
  - **Canonical Artifact Ratification:** Formally published and ratified [`Phase-9.7.8-Capability-Coverage-Matrix.md`](Phase-9.7.8-Capability-Coverage-Matrix.md) mapping all 170 individual capabilities line-by-line with their direct, wrapped, and indirect tests.
- **Verification:** Canonical artifact published; Architecture Section 3 updated; Decision Log updated with ADR-101 and ADR-102; zero uncovered capabilities.

---

### Finding G-002: Component Anatomy Reconciliation & Physical Mapping Artifact
- **Finding:** The architecture referenced a 16-point component anatomy, while the broader MDS architecture also referenced a 32-point anatomy. In the second audit, the reviewer noted that while the reconciliation was conceptually sound, the complete 32-to-16 mapping table needed to be physically embedded within the architecture specification as a canonical governance artifact.
- **Root Cause:** Historical ambiguity between macro-design specification requirements and synthesized code implementation contracts, without an inlined physical artifact for automated verification.
- **Architectural Correction:**
  - Formally codified the **Design Standard vs Implementation Contract Reconciliation** (ADR-096 and Architecture Section 3 `INV-004`).
  - *Canonical Design Standard (32 Points):* Defines the macro-architectural requirements across design, accessibility, telemetry, and security (`MDS-Templates-Architecture.md` Section 4).
  - *Executable Implementation Contract (16 Points):* Synthesizes the 32 design facets into 16 concrete structural headings for component specs and custom element controllers.
  - *Physically Embedded Canonical Mapping Table:* Inlined the complete, exhaustive 32-to-16 anatomy mapping table into `Phase-9.7.8-Governance-Architecture.md` (Section 3 `INV-004`), detailing:
    - All 32 facets (01 Entity ID & Metadata through 32 Agent Selection Criteria).
    - The corresponding Implementation Contract Heading (1 through 16).
    - Mapping Type (1:1 Direct, Many:1 Clustered, Cross-Cutting).
    - Governance Validation Rules for each heading.
  - *Templates Layer 07:* Templates natively enforce the full 32-Point Template Anatomy Standard.
- **Verification:** Both standards preserved with complete physical mapping artifact embedded in Section 3; automated parser and AST rules defined.

---

### Finding G-003: Intra-Tier 1 Authority Precedence
- **Finding:** The 5-tier authority hierarchy lacked deterministic rules when two Tier 1 canonical documents conflict.
- **Root Cause:** Absence of ranking rules within Tier 1.
- **Architectural Correction:**
  - Codified a deterministic **Four-Rank Intra-Tier Precedence Order** (ADR-097 and Architecture Section 2.2):
    $$\text{Rank 1: Master Specification} \succ \text{Rank 2: Canonical Token Repository (DTCG)} \succ \text{Rank 3: Layer Specs (01–07)} \succ \text{Rank 4: Domain Engines (DSSE)}$$
  - Established concrete resolution rules: Master Spec overrides Layer specs on global invariants; DTCG overrides Component specs on raw token definitions; Layer umbrella specs override leaf specimen files.
  - Unresolved same-rank conflicts trigger a `CRITICAL` finding requiring an approved ADR.
- **Verification:** Precedence hierarchy and resolution protocol fully codified.

---

### Finding G-004: Knowledge Graph / Normalized IR Schema
- **Finding:** The term "Normalized Knowledge Graph (IR)" lacked an explicit, formal schema.
- **Root Cause:** High-level narrative description without typed data classes and edge taxonomies.
- **Architectural Correction:**
  - Defined explicit schema with **12 Node Types** (`DocumentNode`, `TokenNode`, `PrimitiveNode`, `ComponentNode`, `PatternNode`, `WorkflowNode`, `TemplateNode`, `FSMStateNode`, `CapabilityNode`, `DecisionNode`, `TestNode`, `RuntimeArtifactNode`) and **10 Edge Types** (`DEFINES`, `REFERENCES`, `IMPLEMENTS`, `DERIVES_FROM`, `VALIDATES`, `PROJECTS_TO`, `CONSUMES`, `CONFLICTS_WITH`, `SUPERSEDES`, `TRANSITIONS_TO`).
  - Specified mandatory node metadata: `canonical_id`, `concept_id`, `node_type`, `source_file`, `line_start`, `line_end`, `authority_tier`, `authority_rank`, `version`, `lifecycle_status`, `raw_evidence`, `attributes`.
- **Verification:** Schema formally codified in ADR-098 and Architecture Section 5.

---

### Finding G-005: Performance Target Qualification & Benchmark Envelope
- **Finding:** The statement "IR execution < 400ms" was phrased as an unverified invariant rather than a qualified target. In the second audit, the reviewer noted that the term "SLA Performance Target" should be replaced with "Performance Benchmark Target" and explicitly qualified as post-implementation measurement goals, not verified facts.
- **Root Cause:** Lack of an explicit benchmark envelope, inappropriate SLA terminology, and failure to designate the metric as an unverified post-implementation benchmark.
- **Architectural Correction:**
  - Reclassified performance criteria from "SLA Performance Target" to **"Performance Benchmark Target"** (ADR-100 and Architecture Section 8).
  - Explicitly documented that Warm Target ($\le 500\text{ ms}$) and Cold Target ($\le 1200\text{ ms}$) are **empirical measurement goals** to be verified after implementation, not verified facts or correctness invariants.
  - Defined the standardized benchmark envelope: Python 3.12 64-bit, x86_64 CPU (4+ physical cores), NVMe SSD, $\sim 150$ markdown files, warm OS disk cache.
  - Specified non-blocking behavior: execution exceeding benchmark thresholds logs an `ADVISORY` performance warning without failing the governance audit gate or breaking builds.
- **Verification:** Benchmark envelope, non-blocking status, and post-implementation measurement designation documented in Architecture Section 8 and ADR-100.

---

### Finding G-006: Markdown Parser Contract
- **Finding:** The zero-dependency Markdown parser lacked an explicit grammar support list and error state protocol.
- **Root Cause:** Abstract description of the parser without specifying grammar coverage.
- **Architectural Correction:**
  - Defined explicit grammar coverage across 11 structures (headings, paragraphs, lists, tables, links, reference links, code fences, inline code, blockquotes, HTML custom tags, escaped characters).
  - Codified the tri-state outcome protocol: `PARSE_SUCCESS`, `PARSE_PARTIAL` (non-fatal anomalies logged in telemetry), and `PARSE_FAILURE` (`BLOCKER`).
  - Prohibited silent failures: all unparsed or malformed lines must appear in parser telemetry.
- **Verification:** Contract codified in ADR-099 and Architecture Section 4.

---

### Finding G-007: Historical Document Scope
- **Finding:** Historical documents were described as completely exempt, which would allow broken links and structural rot to pass unnoticed.
- **Root Cause:** Conflating semantic exemption (historical counts) with structural integrity.
- **Architectural Correction:**
  - Codified the **Dual-Mode Historical Validation Contract** (ADR-091 and Architecture Section 7):
    1. *Historical Semantic Mode (Exempt):* Historical counts, intermediate test passes, and exploratory discarded options (e.g. 1280px containers) are permitted to diverge from current state.
    2. *Structural Integrity Mode (Strictly Enforced):* Historical files must have valid Markdown syntax, zero broken internal links (`[text](url)` must resolve on disk), valid metadata, and zero implementations of banned enterprise systems.
- **Verification:** Dual-mode boundary codified; structural validation remains active.

---

### Finding G-008: Semantic Identity & Conflict Model
- **Finding:** The engine lacked a formal model to recognize when differently worded phrases refer to the same concept (e.g. "standard container" vs "container max-width").
- **Root Cause:** Implicit reliance on naive string equality.
- **Architectural Correction:**
  - Established the **Canonical Concept Dictionary (`ConceptDictionary`)** defining standardized Concept IDs (e.g. `CONTAINER.MAX_WIDTH.DEFAULT`), aliases, and canonical values (ADR-098 and Architecture Section 6).
  - Defined a 4-stage Semantic Normalization Pipeline: Lexical Normalization $\to$ Concept Matching $\to$ Value Extraction $\to$ Contradiction Evaluation.
- **Verification:** Concept dictionary schema and normalization pipeline codified.

---

## 3. Real-World Document Drift Identified in Current Repository

During this architectural audit, three concrete document drift points were cataloged in the repository:

1. **`Documentation-Index.json` Stale Invariants Block:** Records Phase 8.1.4 counts (`tests_defined: 44, tests_passed: 41, tests_deferred: 3`) instead of post-Phase 9.7.7 state (`170 capabilities, 48 harness tests, 0 deferred`). To be synchronized in Phase 9.7.8 implementation.
2. **`docs/ROADMAP.md` Frozen Status:** Shows Phase 9.7 as "Pending Kickoff" (dated 2026-09-22) rather than reflecting the completion and lock of Phases 9.7.1 through 9.7.7.
3. **`docs/PROJECT_HISTORY.md` and `docs/AI_MEMORY.md`:** Stop at Phase 9.6; need updating to reflect the headless browser bridge, axe-core v4.13.0, 17 responsive runs, and 12 canonical visual baselines.

---

## 4. Implementation Phasing & Readiness Gate

When Phase 9.7.8 Implementation is authorized by the Lead Architect, development will proceed in 4 surgical batches:

```text
Batch 1: Core Standard-Library Parsers
         ├── md_scanner.py (Markdown AST Lexer & Link Extractor)
         ├── dtcg_parser.py (W3C DTCG Token Tree & Alias Analyzer)
         └── python_ast_extractor.py (Safe AST Inspector for Python Tests)

Batch 2: Knowledge Graph (Normalized IR) & Engine Core
         ├── knowledge_graph.py (12 Node Types, 10 Edge Types Data Classes)
         ├── concept_dictionary.py (Semantic Concept IDs & Aliases)
         └── engine.py (Graph Builder, Rule Dispatcher, Dual-Mode Scope Filter)

Batch 3: Invariant Rules (INV-001 through INV-012)
         ├── rules_inventory.py (INV-001, INV-003, INV-005, INV-007)
         ├── rules_contracts.py (INV-002, INV-004, INV-006, INV-008)
         └── rules_integration.py (INV-009, INV-010, INV-011, INV-012)

Batch 4: Telemetry, CLI, and Registry Integration
         ├── reporters.py (JSON Schema Serializer, ANSI Terminal Dashboard)
         ├── governance_cli.py (Deterministic CLI Entrypoint)
         └── MDS/10-Testing/tests/test_governance_engine.py (15 Dedicated Tests)
```

---

*Gaps & Remediation Analysis complete for Phase 9.7.8 Independent Re-Audit.*
