# Master Design System (MDS) — Architecture Decision Log
## Phase 9.7.9: Historical Phase Guard (Architecture Stage 1 — Final Micro-Remediation #2)

**Document Reference:** `MDS-DEC-9790`  
**Phase:** 9.7.9 (Historical Phase Guard & Architectural Immutability Engine)  
**Date:** 2026-09-26  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Target Capabilities (Conceptual):**  
- `MDS-HST-001`: Historical Snapshot Baseline Verification  
- `MDS-HST-002`: Cumulative Hash Chain & Manifest Integrity  
- `MDS-HST-003`: Historical Amendment Authorization Verification  
**Execution Context:** Microsoft Windows, Google Chrome v153, Python 3.12.8 (Pure Standard Library)  
**Implementation Guard:** Phase 9.7.9 Implementation STRICTLY BLOCKED until authorized  

---

## 1. Context & Architectural Mandate

Following the final independent architecture audit pass, the architecture was approved across all boundary contracts, canonicalization, trust anchor structures, genesis scoping, classification precedence, and nine-state modeling. Three specific architectural details were designated for final micro-remediation (`G-001`, `G-004`, `G-005`), alongside an implementation safety clarification for `G-002`:
1. **`G-001` (Complete ADDED Detection):** Transition from filename-based matching (`Phase-*.md`) to a deterministic, classification- and manifest-scope-based detection rule.
2. **`G-004` (PROJECT_HISTORY.md Block Identity):** Define the exhaustive block identity specification, heading inclusion, date/phase attributes, duplicate prevention, and mutation behavior.
3. **`G-005` (Amendment State Resolution Model):** Formalize the Immutable Baseline + Amendment Overlay mechanical resolution model, chaining, retraction protocol, and linear acyclic hashing dependency DAG.
4. **`G-002` (Implementation Safety Note):** Clarify the linear bootstrap order between `trust_anchor.json`, `ROOT_TRUST_ANCHOR_FINGERPRINT`, and `master_historical_registry.json` to guarantee zero circular dependency.

These decisions are formally codified in ADR-104 through ADR-119 below.

---

## 2. Ratified Architectural Decisions (ADR-104 through ADR-119)

### ADR-104: Hybrid Versioned Manifest with Cumulative Digest Chain
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** Adopt **Option E (Hybrid Hierarchical Phase Manifests with Cumulative Digest Chain)**.
- **Rationale:** Self-contained, deterministically sorted JSON manifests per locked phase, cryptographically linked via a cumulative SHA-256 digest chain ($\text{digest}_N = \mathcal{H}(\text{digest}_{N-1} \parallel \text{manifest}_N)$). Delivers airtight tamper-evidence, zero external dependencies, human/AI readability in JSON format, zero branch merge friction, and deterministic verification.

---

### ADR-105: Architectural Separation of Boundary (Phase 9.7.8 vs Phase 9.7.9)
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** Establish an unyielding orthogonal boundary:
  - **Phase 9.7.8 (Spatial / Working Tree Consistency):** Validates the *active* state of the repository: cross-document semantic agreement, concept dictionary normalization, token tree syntax, authority precedence, intra-repository link resolution (INV-012), and capability test coverage (INV-009).
  - **Phase 9.7.9 (Temporal / Historical Immutability):** Validates the *invariance over time* of locked architectural milestones: detects unauthorized modification, deletion, addition, or relocation of historical phase records via canonical cryptographic hashing.
  - **Interaction Contract:** Phase 9.7.8 grants *semantic exemption* to historical files (ADR-091) while enforcing *structural link integrity* (ADR-103). Phase 9.7.9 enforces *bit-level content invariance* against ratified historical baselines. Phase 9.7.9 emits findings into the Governance findings pipeline under `INV-013: Unauthorized Historical Drift`.

---

### ADR-106: Exact Canonical Stream Hashing & Cross-Platform Normalization
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** All content hashing must operate on the **Exact Canonical Stream**:
  1. **Binary Ingestion:** Read raw bytes via `Path.read_bytes()`.
  2. **BOM Handling:** If the leading 3 bytes match `0xEF, 0xBB, 0xBF` (UTF-8 BOM), strip from stream for hashing (emits `ADVISORY`).
  3. **Strict UTF-8 Decoding:** Stream must be valid UTF-8. Non-UTF-8 bytes trigger a `DECODE_ERROR` (`BLOCKER`).
  4. **Line-Ending Normalization:** All `\r\n` (CRLF) and standalone `\r` (CR) sequences are deterministically converted to `\n` (LF).
  5. **Trailing Line Invariance:** Trailing newlines and internal whitespace are preserved exactly as written; no body trimming is applied.
  6. **Cryptographic Algorithm:** Standard NIST SHA-256 (`hashlib.sha256()`).

---

### ADR-107: Nine-State Historical Immutability Model & Severity Mapping
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** Establish a formal **Nine-State Immutability Classification Model** with deterministic severity and exit code semantics:
  1. `UNCHANGED`: File on disk matches baseline canonical hash. $\to$ `PASS` (Exit 0).
  2. `MODIFIED`: File on disk differs from baseline hash, no authorized amendment record. $\to$ `CRITICAL` (Exit 1).
  3. `ADDED`: Unrecognized file detected in governed historical scope. $\to$ `CRITICAL` if historical record/decision/gate; `MAJOR` if unknown file in historical directory.
  4. `DELETED`: File present in baseline manifest is missing from disk. $\to$ `BLOCKER` (Exit 2).
  5. `MOVED`: File canonical hash matches baseline, but relative path has changed across directories. $\to$ `CRITICAL` (Exit 1).
  6. `RENAMED`: File canonical hash matches baseline in same directory, but filename has changed. $\to$ `CRITICAL` (Exit 1).
  7. `AUTHORIZED_AMENDMENT`: File hash differs from baseline, BUT a valid ratified amendment record exists in the append-only ledger referencing prior hash, new hash, ADR, and Lead Architect signature. $\to$ `PASS (AUDITED AMENDMENT)` (Exit 0).
  8. `UNKNOWN_BASELINE`: Verification requested for a phase without a ratified baseline manifest. $\to$ `CRITICAL` (Exit 1).
  9. `UNVERIFIABLE`: File unreadable due to filesystem permissions, encoding errors, or ambiguous multi-candidate matching. $\to$ `BLOCKER` (Exit 2).

---

### ADR-108: Baseline Authority & Anti-Poisoning Architecture
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:**
  1. **Lead Architect Exclusivity:** A baseline manifest can ONLY be created or ratified upon explicit instruction and sign-off by the Lead Architect (Mohamed Khalid) during formal phase lock.
  2. **Prohibition of Automated Baseline Generation:** Baseline creation logic is strictly decoupled from automated test execution (`run_tests.py`, pre-commit hooks, CI). The CI environment is strictly read-only (`--verify-only`).
  3. **Manifest Storage Location:** Baselines are stored in `MDS/10-Testing/baselines/historical/phase_<id>_manifest.json`.
  4. **Cumulative Master Ledger:** A top-level ledger (`master_historical_registry.json`) records the sequence of locked phases, their individual manifest SHA-256 digests, and the cumulative digest chain. Tampering with any manifest breaks the chain.

---

### ADR-109: Formal Amendment Authorization Protocol & Append-Only Ledger
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** An amendment is legitimate **if and only if** an explicit, ratified amendment record exists in the append-only ledger (`MDS/10-Testing/baselines/historical/amendments_ledger.json`).
  - Required Fields: `amendment_id`, `target_file`, `prior_canonical_hash`, `new_canonical_hash`, `authorizing_adr`, `authorized_by`, `authorized_at`, `justification`, `amendment_type`.
  - Invariant: `AUTHORIZED_AMENDMENT` requires both hash match AND ledger verification. A changed hash without an amendment record is treated as `UNAUTHORIZED_MODIFICATION` (`CRITICAL`).

---

### ADR-110: Historical Document Classification Hierarchy
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** Align with existing MDS Authority Tiers (ADR-087) and define 8 concrete classifications:
  1. `HISTORICAL_PHASE_RECORD`: Locked phase audits, execution reports, reconciliations, remediation reports, and phase architectures (Tier 4 Operational).
  2. `HISTORICAL_DECISION_LOG`: Ratified decision logs containing historical ADRs/PDRs/CDRs/IDRs (Tier 4 Operational).
  3. `HISTORICAL_GATE_REPORT`: Ratified calibration gate reports and audit sign-offs (Tier 4 Operational).
  4. `HISTORICAL_BLOCK_LEDGER`: Phase-partitioned block-anchored changelog (`docs/PROJECT_HISTORY.md`).
  5. `CURRENT_SPECIFICATION`: Active Tier 1 & Tier 2 specifications defining current system truth. Guarded by Phase 9.7.8 semantic governance; NOT frozen as historical records.
  6. `CURRENT_IMPLEMENTATION_RECORD`: Active runtime code (`Runtime/`, `Playground/`, `Reference-Application/`). Guarded by unit/integration tests.
  7. `ADVISORY_GUIDANCE`: Layer pointer READMEs, agent guidelines, research notes (Tier 5 Advisory).
  8. `GENERATED_ARTIFACT`: Test outputs, visual diffs, compiled CSS, coverage telemetry. Strictly excluded from historical baseline.
  9. `UNKNOWN`: Unclassified documents. Emits `MAJOR` finding if detected in historical directories.

---

### ADR-111: Conceptual Capability Registry Allocations (`MDS-HST-###`)
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** Allocate three conceptual capabilities under Layer M (Testing & Governance):
  - `MDS-HST-001`: Historical Snapshot Baseline Verification (verifies locked phase records against canonical SHA-256 manifests).
  - `MDS-HST-002`: Cumulative Hash Chain & Manifest Integrity (verifies baseline manifests are un-poisoned, chained, and syntactically valid).
  - `MDS-HST-003`: Historical Amendment Authorization Verification (verifies that any modified historical document possesses a valid, ratified amendment record).
  - **Constraint:** `registry.json` shall NOT be modified during Architecture Stage 1. Registration is deferred to the authorized implementation phase.

---

### ADR-112: Pre-Implementation Test Architecture & 20-Scenario Coverage Matrix
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** Design a 20-scenario test suite in `test_historical_guard.py` covering all failure modes, edge cases, cross-platform behaviors, block hashing, and ambiguation protocols before code is written.

---

### ADR-113: Advisory Performance Benchmark Target Qualification
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** Establish **Advisory Performance Benchmark Targets**:
  - Warm Cache Target: $\le 100\text{ ms}$ for complete scan of ~50 historical records.
  - Cold Cache Target: $\le 300\text{ ms}$ for first execution.
  - Telemetry is explicitly classified as `Advisory Benchmark Target`. Slower executions on low-resource hardware emit advisory notifications and do not fail the correctness gate.

---

### ADR-114: Complete Scope-Based ADDED Detection & Disambiguation Algorithm [G-001]
- **Status:** APPROVED (Architecture Stage 1 Final Remediation)
- **Context:** Previous detection relied on filename pattern matching (`Phase-*.md`). This was insufficient because historical scope includes decision logs and gate reports, and unknown files in historical directories must be strictly classified.
- **Decision:** Define a deterministic, **Scope- and Classification-Based ADDED Algorithm**:
  1. **Governed Historical Scope Definition:** A file $f$ falls within Governed Historical Scope if:
     - It resides in `MDS/13-Implementation/` (excluding recognized current specs), OR
     - It is classified as `HISTORICAL_PHASE_RECORD`, `HISTORICAL_DECISION_LOG`, or `HISTORICAL_GATE_REPORT` under the 4-rank precedence engine (ADR-119).
  2. **Disambiguation Pipeline:**
     - *Stage 1 (Exact Normalized Path Match):* If path $P$ exists in both baseline and disk, compare $\mathcal{H}(P_{\text{disk}})$ and $\mathcal{H}(P_{\text{base}})$. If equal $\implies \mathtt{UNCHANGED}$.
     - *Stage 2 (Unmatched Partitioning):* Unmatched disk files ($U_{\text{disk}}$) and missing baseline records ($U_{\text{base}}$) are collected.
     - *Stage 3 (Candidate Matching by Canonical Hash):* For each $f \in U_{\text{disk}}$, find all $b \in U_{\text{base}}$ where $\mathcal{H}(f) = \mathcal{H}(b)$, forming candidate set $\mathcal{C}(f)$.
     - *Stage 4 (Classification-Based Disambiguation):*
       - **Unique Match ($|\mathcal{C}(f)| = 1$):**
         - If $\text{parent}(f) = \text{parent}(b) \land \text{name}(f) \ne \text{name}(b) \implies \mathtt{RENAMED}$ (`CRITICAL`).
         - If $\text{parent}(f) \ne \text{parent}(b) \implies \mathtt{MOVED}$ (`CRITICAL`).
       - **Multiple Matches ($|\mathcal{C}(f)| > 1$):** Duplicate content files. Silent inference is strictly prohibited $\to \mathtt{UNVERIFIABLE (AMBIGUOUS\_MATCH)}$ (`BLOCKER`, Exit Code 2).
       - **Zero Matches ($|\mathcal{C}(f)| = 0$):**
         - If $f$ is within Governed Historical Scope:
           - If classified as `HISTORICAL_PHASE_RECORD`, `HISTORICAL_DECISION_LOG`, or `HISTORICAL_GATE_REPORT` $\implies \mathtt{ADDED}$ (`CRITICAL`, Exit Code 1).
           - If unclassified or non-conforming file in historical directory $\implies \mathtt{UNKNOWN}$ (`MAJOR`, Exit Code 1 in strict mode, non-blocking default).
         - If $f$ is outside historical scope (e.g. `Runtime/`, `04-Components/specifications/`) $\implies$ Ignored by Historical Guard (governed by Phase 9.7.8).
         - Generated artifacts (`artifacts/`) $\implies$ Ignored.
  3. *Stage 5 (Residual Missing Records):* Any $b \in U_{\text{base}}$ with no disk file and no candidate match is classified as $\mathtt{DELETED}$ (`BLOCKER`, Exit Code 2).

---

### ADR-115: Root Trust Anchor Specification & Anti-Tampering Chain of Custody [G-002]
- **Status:** APPROVED (Architecture Stage 1 Final Remediation)
- **Context:** A cumulative hash chain guarantees internal consistency, but cannot prove authenticity against a malicious actor who rewrites both the registry and all manifests. A formal Root Trust Anchor must be established with an explicit bootstrap protocol.
- **Decision:**
  1. **Root Trust Anchor Specification:** Codified in:
     `MDS/10-Testing/baselines/historical/trust_anchor.json`
  2. **Anchor Content:**
     - `genesis_phase_id`: `"Phase-9.1"`
     - `genesis_manifest_digest`: SHA-256 digest of Phase 9.1 baseline manifest.
     - `trust_anchor_id`: Unique identifier (`MDS-ROOT-ANCHOR-v1`).
     - `ratified_at`: ISO 8601 UTC timestamp.
     - `lead_architect_signature`: Verifiable signature block for Mohamed Khalid.
  3. **Linear Bootstrap Protocol (Zero Circularity):**
     - *Step 1 (Generate Genesis Baseline & Registry):* The initial Phase 9.1 through 9.7.8 manifests are ingested. The cumulative chain is computed in `master_historical_registry.json`.
     - *Step 2 (Generate `trust_anchor.json`):* `trust_anchor.json` is created recording the immutable genesis manifest digest and signature.
     - *Step 3 (Pin `ROOT_TRUST_ANCHOR_FINGERPRINT` in Engine):* The canonical SHA-256 digest of `trust_anchor.json` is computed and hard-coded into the engine code as:
       `ROOT_TRUST_ANCHOR_FINGERPRINT = "<canonical_sha256>"`
  4. **Runtime Verification:**
     - Engine asserts: $\text{SHA256}(\mathtt{trust\_anchor.json}) \equiv \mathtt{ROOT\_TRUST\_ANCHOR\_FINGERPRINT}$.
     - Failure triggers an immediate system halt: $\mathtt{BLOCKER (TRUST\_ANCHOR\_VIOLATION)}$.
  5. **Replacement Policy:** Trust Anchor replacement requires an explicit, ratified ADR approved by Mohamed Khalid.

---

### ADR-116: Hybrid Genesis Batch Ingestion & Sequential Baseline Generation Scope [G-003]
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** Adopt **Option C (Hybrid Genesis Batch Ingestion with Phase-Partitioned Lineage)**:
  1. **Genesis Ingestion Scope:** Upon Phase 9.7.9 Implementation Authorization, the engine executes a single-run **Genesis Ingestion** that processes all 42 pre-existing historical phase documents across locked Phases 9.1 through 9.7.8.
  2. **Phase-Partitioned Lineage:** Chronologically partitions documents into **8 discrete phase baseline manifests**:
     - `phase_9.1_manifest.json` through `phase_9.7.8_manifest.json`.
  3. **Cumulative Digest Initialization:** Seeded with $\text{digest}_0 = \mathtt{"0" * 64}$ and chained sequentially across the 8 phases in `master_historical_registry.json`. Future phases append one phase manifest at a time upon formal phase lock.

---

### ADR-117: Phase-Partitioned Block Hashing Architecture for PROJECT_HISTORY.md [G-004]
- **Status:** APPROVED (Architecture Stage 1 Final Remediation)
- **Context:** `docs/PROJECT_HISTORY.md` is an append-only document growing with each phase. The block identity, demarcation, and mutation rules must be completely machine-deterministic.
- **Decision:** Adopt **Option B (Phase-Partitioned Block-Anchored Ledger)** with rigorous block identity rules:
  1. **Canonical Block Demarcation:** Demarcated by standard Markdown H2 headings:
     `^## \[([0-9]{4}-[0-9]{2}-[0-9]{2})\] — (.+)$`
     A block extends from its H2 heading line up to (but not including) the next `^## ` line or EOF.
  2. **Canonical Block ID:** Composite identifier `BLOCK:<date>:<phase_slug>` (e.g. `BLOCK:2026-09-26:phase-9.7.8`).
  3. **Heading Inclusion:** The H2 heading line is an integral part of the canonical block byte stream.
  4. **Date & Phase Attributes:** Date and Phase label are required components of the block identity.
  5. **Mutation Behavior Rules:**
     - *Heading or Body Text Edit:* Altering any text within the block alters its hash $\to \mathtt{HISTORICAL\_BLOCK\_MUTATION}$ (`CRITICAL`).
     - *Date or Phase Label Alteration:* Changes the block ID. The original block is reported missing $\to \mathtt{HISTORICAL\_BLOCK\_DELETED}$ (`BLOCKER`), and a new unrecognized block is reported $\to \mathtt{HISTORICAL\_BLOCK\_ADDED}$ (`CRITICAL`).
     - *Duplicate Block IDs:* If two blocks produce identical block IDs $\implies \mathtt{BLOCKER (DUPLICATE\_BLOCK\_ID)}$.
     - *Block Reordering:* Comparing the sequence of block IDs against `master_historical_registry.json`. Any permutation $\implies \mathtt{BLOCKER (HISTORICAL\_BLOCK\_REORDERING)}$.
     - *Block Split / Merge:* Dividing or merging locked blocks produces hash mismatches and deleted/added block IDs $\implies \mathtt{BLOCKER}$.
     - *Active Trailing Sections:* Blocks corresponding to un-locked/in-progress phases are marked `ACTIVE_CHANGELOG_SECTION` and exempted from immutability checks until that phase is locked.

---

### ADR-118: Immutable Baseline + Amendment Overlay Resolution Model & Acyclic DAG [G-005]
- **Status:** APPROVED (Architecture Stage 1 Final Remediation)
- **Context:** Define how an authorized amendment changes the expected historical state without rewriting historical manifests, and eliminate circular hash dependencies between manifest, registry, and amendment ledger.
- **Decision:** Adopt **Model A (Immutable Baseline + Amendment Overlay)**:
  1. **Permanence of Baseline Manifests:**
     - The original baseline manifest (`phase_9.7.8_manifest.json`) is **NEVER mutated**. It permanently records the original locked hash: $H_{\text{base}} = H_1$.
  2. **Amendment Ledger as Authoritative Expected-State Overlay:**
     - `amendments_ledger.json` records:
       `prior_canonical_hash = H1`, `new_canonical_hash = H2`, `authorizing_adr = ADR-103`.
     - The Expected Hash $H_{\text{expected}}$ for any file $F$ is resolved mechanically:
       $$\text{If no active amendment} \implies H_{\text{expected}} = H_{\text{base}}$$
       $$\text{If amendment chain exists: } H_1 \xrightarrow{\text{AMD-01}} H_2 \dots \xrightarrow{\text{AMD-K}} H_K \implies H_{\text{expected}} = H_K$$
  3. **Verification Resolution Logic:**
     - Given current disk hash $H_{\text{disk}}$:
       - If $H_{\text{disk}} == H_{\text{expected}} \land H_{\text{expected}} \ne H_{\text{base}} \implies \mathtt{AUTHORIZED\_AMENDMENT}$ (`PASS`).
       - If $H_{\text{disk}} == H_{\text{base}} \land H_{\text{expected}} \ne H_{\text{base}} \implies \mathtt{AMENDMENT\_DIVERGENCE}$ (`CRITICAL`, file reverted while amendment was ratified).
       - If $H_{\text{disk}} \ne H_{\text{expected}} \land H_{\text{disk}} \ne H_{\text{base}} \implies \mathtt{MODIFIED}$ (`CRITICAL`, unauthorized mutation).
  4. **Multiple Amendments Chaining:** Each subsequent amendment must declare `prior_canonical_hash` equal to the preceding amendment's `new_canonical_hash`. Non-matching prior hash $\implies \mathtt{BLOCKER (BROKEN\_AMENDMENT\_CHAIN)}$.
  5. **Amendment Retraction:** Retraction is achieved by appending a new record of type `RETRACTED_ERRATUM` declaring `prior_canonical_hash = H2` and `new_canonical_hash = H1`. Ledger history is never rewritten.
  6. **Linear Acyclic Hashing Dependency DAG (Zero Circularity):**
     - *Level 0:* Documents on Disk.
     - *Level 1:* `Phase Manifests` (`phase_X_manifest.json`). Hashes Level 0 files and previous manifest digest.
     - *Level 2:* `Amendments Ledger` (`amendments_ledger.json`). Internal hash chain referencing document hashes.
     - *Level 3:* `Master Historical Registry` (`master_historical_registry.json`). Hashes cumulative manifest digest + ledger digest.
     - *Level 4:* `Root Trust Anchor` (`trust_anchor.json`). Verifies Genesis digest.
     - Circular dependency is mathematically impossible.

---

### ADR-119: Four-Rank Canonical Classification Precedence Engine [G-006]
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** Enforce a deterministic **Four-Rank Classification Precedence Hierarchy**:
  1. **Rank 1: Explicit Manifest Roster (Highest Precedence):** If a document's relative path or canonical hash is recorded in any ratified baseline manifest, its classification is immutable and fixed by that manifest.
  2. **Rank 2: Explicit Metadata Header:** Document YAML frontmatter or Markdown header:
     `Classification: HISTORICAL_PHASE_RECORD | HISTORICAL_DECISION_LOG | CURRENT_SPECIFICATION`
  3. **Rank 3: Canonical Path Pattern Rules:** Strict folder/pattern mapping.
  4. **Rank 4: Fallback / Unknown:** Any unclassified file in `MDS/13-Implementation/` is classified as `UNKNOWN` $\to$ triggers `MAJOR` finding.

---

*Decision Log ratified for Phase 9.7.9 Final Micro-Remediation #2.*
