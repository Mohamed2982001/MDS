<!-- Classification: CURRENT_SPECIFICATION -->
# Master Design System (MDS) — Architecture Decision Log
## Phase 9.7.11: CI Pipeline & Artifact Dashboard — Final Architecture Micro-Remediation Pass #4

**Document Reference:** `MDS-DEC-9711-REV5`  
**Phase:** 9.7.11 (CI Pipeline & Artifact Dashboard)  
**Layer:** Layer M (Testing, Governance & Architectural Immutability)  
**Date:** 2026-10-01  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Status:** **ARCHITECTURE STAGE 1 — FINAL MICRO-REMEDIATION PASS #4 COMPLETE (Awaiting Final Independent Audit Gate)**  
**Execution Context:** Microsoft Windows, Google Chrome v153, Python 3.12.8 (Pure Standard Library)  
**Implementation Guard:** Phase 9.7.11 Implementation STRICTLY BLOCKED until authorized  

---

## 1. Context & Architectural Mandate

Following the formal **REV4 Independent Architecture Audit** conducted by Lead Architect Mohamed Khalid, the architecture of Phase 9.7.11 has been refined to resolve the final two architectural blockers:

1. **Trust Model Realignment & Layer Separation (ADR-151):**
   - *Audit Finding:* REV4 improperly grouped runner-local mechanisms (`$GITHUB_OUTPUT`, `$GITHUB_STEP_SUMMARY`) under the "Trust Anchor" concept. `$GITHUB_OUTPUT` is merely a runner-local file pipe for passing values between workflow steps; it does not constitute an immutable external record outside the runner workspace. Furthermore, calling standard provider records "cryptographic attestation" without cryptographic signing primitives is technically ungrounded.
   - *Resolution:* Formally decoupled the 4 architectural layers: (A) Runner-Local Transport/State, (B) Provider-Controlled Execution Record, (C) Cryptographically Authenticated Record, and (D) Root of Trust. Established the abstract `TrustedExecutionRecord` contract. Correctly designated provider-managed verification as "Provider-Controlled Trust Record". Reaffirmed that runner-local files never serve as the Root of Trust.
2. **Multi-Dimensional Authority Matrix (ADR-153):**
   - *Audit Finding:* REV4 modeled governance authority as a single linear hierarchy (`Baseline -> Historical Guard -> Governance -> Orchestrator -> Provenance Registry -> Dashboard`), inadvertently implying that the Orchestrator's execution authority is subordinate to Historical Guard, creating potential semantic collisions.
   - *Resolution:* Replaced the linear hierarchy with an orthogonal **Multi-Dimensional Authority Matrix**. Decoupled 6 distinct authority domains: (1) Specification Authority, (2) Historical Authority, (3) Governance Authority, (4) Execution Authority, (5) Reporting Metadata Authority, and (6) Presentation Authority. Enforced strict cross-domain invariants guaranteeing that neither Historical Guard nor Provenance Registry can alter the Orchestrator's sovereign Exit Code.

These decisions are formally codified in ADR-136 through ADR-153 below.

---

## 2. Ratified Architectural Decisions (ADR-136 through ADR-153)

### ADR-136: CI/Local Parity & Thin Provider Adapter Stance
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** The CI execution model shall be strictly a **Thin Consumer** of the canonical local validation entrypoint (`python MDS/10-Testing/run_all.py --ci`). CI runners MUST NOT implement independent validation steps, reimplement test discovery, or duplicate governance logic.
- **Rationale:** If validation logic diverges between local developer environments and CI runners, developers cannot reliably reproduce CI outcomes. By delegating all validation directly to `run_all.py`, local and CI environments maintain 100% semantic parity.
- **Boundary Contract:** The CI provider adapter is restricted to three operational duties:
  1. Detecting and normalizing runner environment metadata (commit SHA, branch, PR number, runner OS).
  2. Invoking `run_all.py` with the appropriate profile.
  3. Collecting output artifacts and publishing the step summary.

---

### ADR-137: Authoritative Manifest-First Artifact Model
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** Every CI execution shall produce a single, authoritative, cryptographically verified **Artifact Manifest** (`ci_artifact_manifest.json`) adhering to Layer-M Schema v1.0.0.
- **Rationale:** Disparate tool outputs (Axe raw JSON, visual diff PNGs, console logs, test runner outputs) must not be scattered or parsed ad-hoc by downstream consumers. The manifest acts as the definitive index and source of truth for the entire run.
- **Boundary Contract:** The manifest captures run context, phase context, orchestrator summary, subsystem results, raw findings, protected core integrity proofs, and the complete inventory of harvested artifacts.

---

### ADR-138: Run-Addressed Artifact Storage Architecture
- **Status:** APPROVED (Architecture Stage 1 - Micro-Remediation #1)
- **Decision:** Artifacts shall be organized into **Run-Addressed Storage** partitioned by run identifier:
  ```text
  MDS/10-Testing/artifacts/ci/
  ├── latest.json                                     <-- Logical JSON pointer (ADR-148)
  └── runs/
      └── {run_id}/                                   <-- Immutable run-addressed directory
          ├── ci_artifact_manifest.json               <-- Authoritative master manifest
          ├── ci_artifact_manifest.sha256             <-- External trusted digest sidecar (ADR-149)
          ├── step_summary.md                         <-- Markdown report
          ├── telemetry/
          ├── evidence/
          ├── logs/
          └── dashboard/
  ```
- **Integrity Rule:** While directory paths are run-addressed, every stored file is **cryptographically content-integrity protected**: the manifest records relative POSIX paths, byte sizes, MIME types, and NIST SHA-256 digests.
- **Terminology Rule:** This model is strictly termed **Run-Addressed Storage with Content-Integrity Verification**; it is NOT content-addressed storage (which addresses objects purely by hash).

---

### ADR-139: Honest Failure Preservation & Exit Code Integrity
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** The CI pipeline shall NEVER suppress, quarantine, or whitelist genuine validation failures to achieve an artificial green build. Specifically, known pre-existing Reference Application accessibility violations (`color-contrast` and `select-name`) MUST continue to trigger `Exit 1` in `--full` and `--ci` profiles.
- **Rationale:** Suppressing genuine failures introduces "false green" blindness and degrades engineering trust. The role of CI is truth verification.
- **Boundary Contract:** The pipeline verdict remains `FAIL (Exit 1)`. The CI job fails honestly until dedicated surface remediation occurs in future phases.

---

### ADR-140: Pure Static Dashboard Architecture & Dual Ingestion Protocol
- **Status:** APPROVED (Architecture Stage 1 - Micro-Remediation #1)
- **Decision:** The CI Artifact Dashboard shall be implemented as a **pure static HTML/CSS/JavaScript bundle** requiring zero runtime dependencies, zero Node.js tooling, zero server-side processes, and zero external network calls.
- **Dual Ingestion Protocol:**
  - **Local File Mode (`file:///`):** Ingestion is strictly driven by `manifest_data.js` via `window.__MDS_MANIFEST__`. Browser `fetch()` calls are **strictly prohibited** in `file://` mode to eliminate CORS/security failures across modern browsers.
  - **Hosted HTTP Mode (`http://` / `https://`):** Ingestion fetches `ci_artifact_manifest.json` dynamically via asynchronous relative `fetch('./ci_artifact_manifest.json')`.
- **Design System Mandate:** Styled exclusively with Master Design System tokens (Cairo typography via offline base64 data URIs, light/dark themes, CSS logical properties).

---

### ADR-141: Dashboard Security Boundary & CSP Specification
- **Status:** APPROVED (Architecture Stage 1 - Micro-Remediation #1)
- **Decision:** The dashboard security boundary is formally decoupled between hosted and local contexts:
  1. **Hosted HTTP Mode (Strict CSP Enforced):**
     `default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none';`
     `unsafe-inline` is **strictly forbidden** for scripts and styles in hosted mode.
  2. **Application-Layer DOM Sanitization (Universal Mandate):**
     Dynamic insertion of untrusted data (finding messages, commit metadata, file paths) MUST strictly use `textContent` or `document.createTextNode()`. The use of `innerHTML`, `outerHTML`, `document.write()`, and `eval()` is **strictly prohibited**.
  3. **Offline `file:///` Threat Model:** In `file://` mode where browser meta CSP support varies, security is 100% guaranteed by the universal DOM sanitization mandate and zero external resource loading.

---

### ADR-142: CI Exit Code Propagation & Non-Retriable Validation Failures
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** CI runners shall directly forward the orchestrator exit code:
  - `Exit 0`: Pipeline Passed (CI Job Succeeds).
  - `Exit 1`: Validation / Surface Failure (CI Job Fails). **Retries STRICTLY FORBIDDEN**.
  - `Exit 2`: Invariant / Structural / Fatal Failure (CI Job Fails). **Retries STRICTLY FORBIDDEN**.
- **Rationale:** Validation failures are deterministic design-system breaches; retrying them wastes computing resources and risks masking intermittent race conditions. Automatic retries are only permitted at the CI infrastructure level for runner startup crashes or lost agent connections prior to orchestrator launch.

---

### ADR-143: Secret Scrubbing & Untrusted PR Threat Model
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** The Artifact Collector and Telemetry Generator shall execute an automatic **Secret Redaction Pass** before writing any log, telemetry, or manifest to disk.
- **Redaction Rules:**
  - Any environment variable or configuration string matching patterns for keys, tokens, auth headers, passwords, or credentials (`*_KEY`, `*_TOKEN`, `*_SECRET`, `*_AUTH`, `*_PASS`, `*PRIVATE*`) is sanitized to `[REDACTED_MDS_SECRET]`.
  - Untrusted Pull Requests (from public forks) run under least-privilege tokens (`permissions: contents: read`) with zero write access to repository secrets or protected branches.

---

### ADR-144: CI Performance Overhead Decoupling Contract
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** CI telemetry must explicitly separate **Validation Execution Time** (governed by Orchestrator Layer-M contracts) from **CI Infrastructure Overhead** (runner provisioning, tool checkout, browser binary installation, artifact upload).
- **Canonical Metrics:**
  - `orchestrator_duration_ms`: Execution time of `run_all.py` (Benchmarked against Layer-M: Cold $\le 1200\text{ms}$ / Warm $\le 500\text{ms}$ advisory).
  - `ci_overhead_ms`: Delta between total runner time and orchestrator time (Target: $\le 2000\text{ms}$).

---

### ADR-145: Deterministic Historical Run Comparison Protocol
- **Status:** APPROVED (Architecture Stage 1)
- **Decision:** The dashboard shall support comparative analysis between the current run and previous baseline runs via a client-side comparison engine consuming past `ci_artifact_manifest.json` snapshots.
- **Comparison Dimensions:**
  - Overall status transition ($\text{PASS} \leftrightarrow \text{FAIL}$).
  - Subsystem duration deltas ($\Delta\text{ ms}$).
  - Finding diffing (New findings, resolved findings, persistent findings).
  - Visual baseline diff comparison (side-by-side raster comparison).
  - Assertion count drift ($\Delta\text{ assertions}$).

---

### ADR-146: Canonical Manifest Hashing Algorithm (Non-Circular)
- **Status:** APPROVED (Architecture Stage 1 - Micro-Remediation #1)
- **Decision:** The integrity digest of `ci_artifact_manifest.json` shall be computed using a strictly non-circular, deterministic canonicalization protocol:
  1. **Preparation:** Assemble the complete manifest dictionary with `"manifest_sha256": None`.
  2. **Canonical Serialization:** Serialize the dictionary to bytes using:
     ```python
     canonical_bytes = json.dumps(
         manifest_dict,
         ensure_ascii=False,
         sort_keys=True,
         separators=(",", ":")
     ).encode("utf-8")
     ```
  3. **Hash Generation:** Compute $\mathcal{H}_{\text{canon}} = \text{hashlib.sha256}(canonical\_bytes)\text{.hexdigest()}$.
  4. **Injection:** Assign `manifest_dict["manifest_sha256"] = ` $\mathcal{H}_{\text{canon}}$.
- **Scope of Guarantee:** Provides **Canonical Manifest Integrity Verification** (detects accidental corruption or serialization drift). Does NOT by itself establish authenticity against malicious tampering without an external trust anchor (ADR-149).

---

### ADR-147: Finding Provenance Authority & Comparison Architecture
- **Status:** APPROVED (Architecture Stage 1 - Micro-Remediation #1)
- **Decision:** The architectural boundaries governing finding semantics and provenance are formally partitioned:
  1. **Validation Authority (Orchestrator / Subsystems):** Subsystems (`SUB-01` to `SUB-15`) and the Orchestrator are the sole authorities for findings. Findings contain intrinsic properties: `severity`, `code`, `target`, `line`, `message`. The Orchestrator DOES NOT assign comparative provenance tags.
  2. **Pure Harvester (Artifact Collector):** The Artifact Collector extracts raw findings directly from `run_all_telemetry.json` without modifying, re-evaluating, or semantically tagging them. Zero validation logic exists in the Collector.
  3. **Derived Consumer (Historical Comparison Engine / Dashboard):** Comparative provenance (`PREEXISTING_SURFACE`, `REGRESSION`, `UNKNOWN`) is computed downstream by the **Historical Comparison Engine** by consuming declarative metadata from the Baseline Provenance Registry (ADR-150).
- **Rationale:** Preserves the core principle of Zero Validation Duplication while allowing rich triage visualization in reports and dashboards.

---

### ADR-148: `latest.json` Logical Pointer Governance
- **Status:** APPROVED (Architecture Stage 1 - Micro-Remediation #1)
- **Decision:** The pointer to the most recent run shall be a **Logical JSON Pointer** (`MDS/10-Testing/artifacts/ci/latest.json`), NOT an operating system filesystem symlink.
- **Schema:**
  ```json
  {
    "schema_version": "1.0.0",
    "pointer_updated_utc": "2026-09-28T13:30:00Z",
    "run_id": "20260928-133000-abc123",
    "manifest_relative_path": "runs/20260928-133000-abc123/ci_artifact_manifest.json",
    "manifest_sha256": "4a5b6c...64hex"
  }
  ```
- **Governance Rules:**
  - **Writer:** The Artifact Collector, executed after the run directory and canonical manifest are committed to disk.
  - **Immutability Boundary:** Run directories (`runs/{run_id}/`) are 100% immutable once written. `latest.json` is a mutable branch pointer.
  - **Non-Circular:** Located outside the run directory; not included inside the run manifest hash.
  - **Failure Semantics:** A failure writing `latest.json` is an **Infrastructure Warning**; it never alters the validation exit code.

---

### ADR-149: External Trusted Manifest Digest Sidecar & Authenticity Verification
- **Status:** APPROVED (Architecture Stage 1 - Micro-Remediation #2)
- **Decision:** To guarantee **Trusted Manifest Authenticity** and prevent undetected tampering where an attacker modifies both the payload and the internal `manifest_sha256`, every run shall establish an **External Trust Anchor**:
  1. **External Immutable Sidecar:** Alongside `ci_artifact_manifest.json`, the Artifact Collector writes an external digest file:
     `ci_artifact_manifest.sha256`
     Formatted according to POSIX `sha256sum` convention:
     ```text
     <64-hex SHA-256 digest>  ci_artifact_manifest.json
     ```
  2. **CI Runner Attestation:** The CI Provider Adapter captures the canonical digest and writes it to the CI provider's immutable run metadata (e.g. `$GITHUB_STEP_SUMMARY`, GitLab job artifact metadata, or an immutable CI pipeline log annotation).
  3. **Verification Sequence:**
     - **Phase 1 (Integrity):** Load `ci_artifact_manifest.json`, set `manifest_sha256 = null`, recompute canonical SHA-256 ($\mathcal{H}_{\text{canon}}$), and verify $\mathcal{H}_{\text{canon}} == \mathcal{H}_{\text{internal}}$. If mismatch $\to$ `ManifestIntegrityError` (`Exit 2`).
     - **Phase 2 (Authenticity):** Read external sidecar `ci_artifact_manifest.sha256` ($\mathcal{H}_{\text{trusted}}$). Verify $\mathcal{H}_{\text{canon}} == \mathcal{H}_{\text{trusted}}$. If mismatch $\to$ `ManifestAuthenticityError` (`Exit 2`).
  4. **Threat Model Separation:**
     - `manifest_sha256` inside the manifest: Protects against accidental transmission corruption, truncation, and serialization drift.
     - `ci_artifact_manifest.sha256` / CI Runner Attestation: Protects against intentional tampering and establishes provenance authenticity.

---

### ADR-150: Declarative Surface Provenance Registry & Metadata-Driven Comparison
- **Status:** APPROVED (Architecture Stage 1 - Micro-Remediation #2)
- **Decision:** Hardcoded domain rules for finding classification (e.g. `Reference-Application` + `color-contrast`) are strictly eliminated from the Historical Comparison Engine. Provenance classification shall be driven entirely by a declarative **Baseline Provenance Registry**:
  ```text
  MDS/10-Testing/baselines/provenance/surface_provenance_registry.json
  ```
- **Registry Schema (Schema v1.0.0):**
  ```json
  {
    "schema_version": "1.0.0",
    "registry_id": "MDS-SURFACE-PROVENANCE-v1",
    "authority_phase": "Phase-9.7.5",
    "provenance_rules": [
      {
        "rule_id": "PROV-A11Y-REF-001",
        "target_path": "MDS/Reference-Application/index.html",
        "violation_code": "color-contrast",
        "provenance": "PREEXISTING_SURFACE",
        "origin_phase": "Phase-9.7.5",
        "origin_test": "test_05_live_reference_app_accessibility_audit",
        "rationale": "Pre-existing design token contrast in Reference Application, codified in Phase 9.7.5"
      },
      {
        "rule_id": "PROV-A11Y-REF-002",
        "target_path": "MDS/Reference-Application/index.html",
        "violation_code": "select-name",
        "provenance": "PREEXISTING_SURFACE",
        "origin_phase": "Phase-9.7.5",
        "origin_test": "test_05_live_reference_app_accessibility_audit",
        "rationale": "Pre-existing unlabelled select element in Reference Application controls, codified in Phase 9.7.5"
      }
    ]
  }
  ```
- **Comparison Engine Lookup Protocol:**
  1. The Historical Comparison Engine loads the declarative registry dynamically.
  2. For each raw finding, the engine queries the registry by `(target_path, violation_code)`.
  3. If a match is found $\to$ assign `provenance = rule["provenance"]` (`PREEXISTING_SURFACE`).
  4. If finding is absent from registry and historical run baselines $\to$ assign `provenance = "REGRESSION"`.
  5. If registry is unavailable or finding cannot be reconciled $\to$ assign `provenance = "UNKNOWN"`.
- **Conservative Invariant:**
  - `UNKNOWN` is treated conservatively as potential defect in triage.
  - Derived provenance is metadata only; it **NEVER suppresses, alters, or overrides the authoritative Orchestrator exit code** (`Exit 1`).
  - Zero duplication: The registry is purely declarative metadata; zero validation logic is embedded in the comparison layer.

---

### ADR-151: Formal Trust Chain, Root of Trust & Multi-Tier Verification Semantics
- **Status:** APPROVED (Architecture Stage 1 - Pass #4 / REV5)
- **Decision:** To guarantee deterministic authenticity and eliminate runner-local trust ambiguities, the architecture codifies an explicit **Four-Tier Trust Hierarchy**:
  1. **Tier 4 — Root of Trust (External Execution Authority):** Anchored strictly in the **CI Provider's Protected Control Plane** (e.g., GitHub Actions Workflow Service, GitLab CI Pipeline Controller).
  2. **Tier 3 — Trust Anchor (Provider-Controlled Trust Record):** The authoritative execution record committed directly to the CI Provider's control plane via the provider adapter (e.g., GitHub Check Run Attestation or Provider Job Execution Record API). Represented by the abstract contract:
     ```python
     @dataclass(frozen=True)
     class TrustedExecutionRecord:
         run_id: str
         commit_identity: str
         manifest_digest: str  # Expected sha256
         provider_identity: str  # e.g., "github-actions"
         execution_identity: str  # e.g., check_run_id or job_id
         authenticity_status: str  # "RECORDED", "AUTHENTICATED", "UNVERIFIED"
     ```
     *Attestation Terminology:* Formally designated as a **"Provider-Controlled Trust Record"** unless an external cryptographic OIDC/Sigstore signing authority is configured.
  3. **Tier 2 — Runner-Local Transport & State:** `$GITHUB_OUTPUT`, `$GITHUB_STEP_SUMMARY`, and the local sidecar file `ci_artifact_manifest.sha256` reside within the runner workspace. They are strictly **transport/reporting mechanisms** and have **ZERO Root of Trust or Trust Anchor authority**.
  4. **Tier 1 — Canonical Artifact Integrity:** `manifest_sha256` inside `ci_artifact_manifest.json` provides deterministic internal payload integrity.
- **Ordered 3-Step Verification Protocol:**
  1. Step 1: Verify internal payload integrity (`manifest_sha256`).
  2. Step 2: Verify local sidecar digest (`ci_artifact_manifest.sha256`).
  3. Step 3: Verify provider control plane attestation (`TrustedExecutionRecord.manifest_digest`).
- **Multi-Tier Failure Semantics Matrix:**
  - Case A (Manifest Hash Mismatch): `ManifestIntegrityError` $\to$ `Exit 2` (Non-retriable).
  - Case B (Sidecar Hash Mismatch): `ManifestAuthenticityError` $\to$ `Exit 2` (Non-retriable).
  - Case C (Provider-Controlled Record Mismatch): `ManifestAuthenticityError` $\to$ `Exit 2` (Non-retriable).
  - Case D (Missing Sidecar in CI): `ManifestAuthenticityError` $\to$ `Exit 2` (Non-retriable).
  - Case D-Local (Missing Sidecar Local): Advisory Log $\to$ Integrity-Only Mode (Exit code preserved).
  - Case E (Missing CI Provider Record): `InfrastructureAttestationError` $\to$ Infrastructure Error / `Exit 2` (Max 1 retry).
  - Case F (Malformed Sidecar): `ManifestAuthenticityError` $\to$ `Exit 2` (Non-retriable).
  - Case G (Local Execution): Advisory Log $\to$ Integrity-Only Mode (Exit code preserved).
- **Rationale:** An attacker with filesystem write access to the runner workspace can overwrite both the manifest and the local sidecar. By anchoring authenticity in the provider control plane (outside filesystem reach), tampering is detected deterministically. Runner-local mechanisms (`$GITHUB_OUTPUT`) are untrusted file pipes and cannot serve as trust anchors.

---

### ADR-152: Deterministic Finding Provenance Precedence & Conflict Resolution Protocol
- **Status:** APPROVED (Architecture Stage 1 - Pass #4 / REV5)
- **Decision:** Downstream finding triage shall be governed by an explicit **5-Step Ordered Decision Algorithm** resolving all precedence edge cases deterministically:
  1. **Integrity & Schema Validation:** Validate `surface_provenance_registry.json`. Corrupt registry falls back to `UNKNOWN` (`Case H`). Missing registry falls back to historical baseline comparison (`Case G`).
  2. **Exact Identity Matching:** Findings are matched strictly against `(target_path, violation_code)`. No fuzzy, prefix, or partial matches are permitted (`Case I`).
  3. **Conflict Resolution Matrix:**
     - Case A: Registry matches + historical baseline agrees $\to$ `PREEXISTING_SURFACE` (High Confidence).
     - Case B: Registry matches + historical baseline conflicts $\to$ **`REGRESSION` (State: `PROVENANCE_CONFLICT`)**. Locked Historical Baseline Superiority takes precedence over registry claims.
     - Case C: Malformed registry rule $\to$ Rule discarded; finding falls back to `UNKNOWN`.
     - Case D: Unindexed finding in valid registry $\to$ Reconciled via historical baseline (`PREEXISTING_SURFACE` if present, `REGRESSION` if absent).
     - Case E: Finding present in baseline but unindexed in registry $\to$ `PREEXISTING_SURFACE`.
     - Case F: Finding absent in both registry and baseline $\to$ `REGRESSION`.
  4. **Reporting Metadata Invariant:** Provenance is strictly downstream triage metadata. It MUST NEVER suppress a finding, whitelist a finding, downgrade severity, or alter the Orchestrator exit code (`Exit 1` remains `Exit 1`).
- **Rationale:** Prevents ad-hoc or subjective triage, eliminates ambiguity when declarative records diverge, and guarantees that validation exit codes remain immutable.

---

### ADR-153: Multi-Dimensional Authority Matrix & Cross-Domain Invariants
- **Status:** APPROVED (Architecture Stage 1 - Pass #4 / REV5)
- **Decision:** The architecture replaces linear governance hierarchies with an orthogonal **Multi-Dimensional Authority Matrix** covering 6 decoupled operational domains:
  1. **Master Specification Authority:** Phase 9.7.8 & Core Design Specifications $\to$ Sole authority on canonical design tokens, contracts, and layer schemas.
  2. **Historical Authority:** Phase 9.7.9 Historical Guard (`MDS-ROOT-ANCHOR-v1`) $\to$ Sole authority on immutable past execution reality (42 sealed baselines). Cannot alter current run exit codes.
  3. **Governance Authority:** Phase 9.7.8 Governance Engine $\to$ Sole authority on modification authorization, exemption grants, and rule deprecation.
  4. **Execution Authority:** Phase 9.7.10 Orchestrator (`run_all.py`) $\to$ Sole sovereign authority over current run execution flow and Exit Codes (`Exit 0`, `Exit 1`, `Exit 2`). Cannot mutate historical baselines.
  5. **Reporting Metadata Authority:** Phase 9.7.11 Provenance Registry $\to$ Declarative classification index for downstream triage. Possesses zero authority to alter exit codes or historical reality.
  6. **Presentation Authority:** Phase 9.7.11 CI Dashboard $\to$ Pure visualization and navigation. Possesses zero authority over execution, exit codes, or governance verdicts.
- **Strict Cross-Domain Invariants:**
  - Historical Guard cannot modify the Orchestrator's current execution exit code.
  - Orchestrator cannot rewrite Historical Guard's locked historical baseline.
  - Provenance Registry cannot alter either historical truth or current execution exit codes.
  - CI Dashboard has zero decision-making or exit code authority.
  - Any discrepancy between Provenance Registry and Historical Baseline resolves strictly in favor of Historical Baseline (`Case B`).
  - Amending historical truth requires the Phase 9.7.9 Governance Amendment Protocol (ADR-113); modifying the declarative registry cannot amend historical records.
- **Rationale:** Linear authority chains blur the distinction between specification truth, historical truth, and execution authority. Decoupling into orthogonal domains prevents semantic collisions while enforcing strict immutability.

---

## 3. Decision Log Sign-off & Audit Readiness

- [x] ADR-136 through ADR-153 formally ratified and bounded under REV5 (Pass #4).
- [x] Complete Root of Trust (CI Provider Control Plane) and Provider-Controlled Trust Record chain established with `TrustedExecutionRecord` contract (ADR-151).
- [x] Runner-local transport mechanisms (`$GITHUB_OUTPUT`, `$GITHUB_STEP_SUMMARY`) explicitly isolated from Trust Anchor authority (ADR-151).
- [x] Multi-tier failure semantics matrix (Cases A through G) formalized (ADR-151).
- [x] Deterministic 5-step provenance decision algorithm and conflict matrix (Cases A through I) codified (ADR-152).
- [x] Orthogonal Multi-Dimensional Authority Matrix and cross-domain invariants ratified (ADR-153).
- [x] Provenance invariant guarantees zero mutation of orchestrator exit codes (Exit 1 preserved).
- [x] Test matrix expanded to 78 scenarios (`TEST-CI-01` through `TEST-CI-78`) covering all trust, precedence, and authority matrix invariants.
- [x] Zero validation duplication and zero implementation code boundary preserved.
- [x] Ready for final independent architecture gate.
