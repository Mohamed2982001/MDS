<!-- Classification: CURRENT_SPECIFICATION -->
# Master Design System (MDS) — Architectural Decision Log
## Phase 10.4: MDS v1.0.0 Production Certification Gate

**Document Reference:** `MDS-DEC-10.4-REV7`  
**Phase:** 10.4 (MDS v1.0.0 Production Certification)  
**Layer:** Layer 13 (Implementation, Tooling & Operationalization)  
**Date:** 2026-10-02  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Status:** **ACTIVE & RATIFIED IN ARCHITECTURE STAGE (REV7 REMEDIATION)**  

---

## 1. Architectural Decision Index

| Decision ID | Title | Scope / Impact | Status |
| :--- | :--- | :--- | :--- |
| **ADR-301** | Certification Gate as Non-Development Phase | Scope boundary: Zero new features, pure evaluation | **APPROVED** |
| **ADR-302** | Sole Authority Model (Lead Architect Mohamed Khalid) | Governance: Sole sign-off authority | **APPROVED** |
| **ADR-303** | Thirteen Granular Certification Gates Architecture (A–L) | Quality: Split Gate F into F1 (Toolchain) and F2 (Browser) | **APPROVED** |
| **ADR-304** | Four-Tier Failure Severity Taxonomy | Risk: Blocker, Major, Minor, Advisory | **APPROVED** |
| **ADR-305** | Inviolable Zero-Waiver Domain & 5-State Evaluation Model | Governance: Mathematical consistency (PASS/FAIL/BLOCKED/NA/WAIVED) | **APPROVED** |
| **ADR-306** | Four-Tier Cryptographic Trust Chain Verification | Integrity: Pinned root anchor to 33 dist artifacts | **APPROVED** |
| **ADR-307** | Calibrated Performance Budget Classification | Performance: Mandatory $\le 1\text{MB}$ cap, Proposed component targets, Advisory gzip | **APPROVED** |
| **ADR-308** | Pure W3C Standards & Zero-NPM Web Runtime Enforcement | Architecture: Browser-native execution without Node | **APPROVED** |
| **ADR-309** | Standards Compatibility + Reference Browser Model (Option B) | Compatibility: Standards traceability (FF/Safari/Edge) + Chrome v153 live | **APPROVED** |
| **ADR-310** | Production Runtime Accessibility Protocol & WCAG Claim Boundary | Accessibility: 19 component specimens, 4-tier criteria classification, calibrated claim | **APPROVED** |
| **ADR-311** | Production Certificate Data Model & Evidence Binding | Release: Certificate Integrity Digest bound to Evidence Manifest SHA-256 | **APPROVED** |
| **ADR-312** | Four-Tier Asset Taxonomy (Subject vs Qualification vs Evidence vs Excluded) | Scope: Product = Runtime & dist; Tooling = Qualified; Specs = Evidence | **APPROVED** |
| **ADR-313** | Calibrated Clean Abort & Non-Destructive Rollback Protocol | Reliability: Sandbox lifecycle & zero-residue filesystem audits | **APPROVED** |
| **ADR-314** | Deterministic Evidence Capture Architecture & Measured Zero Sinks | Traceability: Structured logs & static regex scan for forbidden JS sinks | **APPROVED** |
| **ADR-315** | Strict Two-Stage Gate Model (Architecture Approval Prior to Execution) | Gate: Execution blocked until Architecture approval | **APPROVED** |
| **ADR-316** | Formal Waiver Record Schema & NOT_APPLICABLE Governance | Governance: Structured auditable waiver records & strict N/A determination rules | **APPROVED** |
| **ADR-317** | Release Integrity Set vs Production Artifact Set Partition | Integrity: 33 production artifacts declared; 35 release files in dist verified | **APPROVED** |
| **ADR-318** | Immutable Certification Evidence Manifest Architecture | Integrity: Canonical certification_evidence_manifest.json binding individual gate logs | **APPROVED** |
| **ADR-319** | Standalone Trusted Certification Seal & Integrity vs Authenticity Architecture | Governance/Integrity: External seal at evidence/certification/trusted_seal.json | **APPROVED** |
| **ADR-320** | Calibrated Gate G Scope & Illustrative Values Advisory | Quality/Governance: Automated verification scope != full WCAG; illustrative values advisory | **APPROVED** |

---

## 2. Detailed Architectural Decisions

### ADR-301: Certification Gate as Non-Development Phase
* **Context:** Prior phases (9.1 through 10.3) developed, tested, and sealed all foundation tokens, components, operational tooling (DSSE, Agent Bootstrap, Compiler), and distribution artifacts. Phase 10.4 represents the final gateway to production release.
* **Decision:** Phase 10.4 is strictly classified as a **Certification Gate**, not a development phase. Zero new runtime features, widgets, design tokens, or utility classes may be added. If a defect is discovered during verification, it triggers formal defect remediation, not opportunistic feature expansion.
* **Consequences:** Eliminates scope creep and guarantees that the system released as MDS v1.0.0 is exactly what was specified and verified throughout prior phases.

---

### ADR-302: Sole Authority Model (Lead Architect Mohamed Khalid)
* **Context:** Release certification requires executive accountability and authoritative sign-off.
* **Decision:** Lead Architect **Mohamed Khalid** is designated as the **Sole Sign-off Authority** for MDS v1.0.0. No automated system, AI agent, CI pipeline, or delegate has the authority to declare the system certified for production or grant waivers.
* **Consequences:** Guarantees centralized architectural oversight and aligns with the Lead Architect's standards of senior engineering excellence.

---

### ADR-303: Thirteen Granular Certification Gates Architecture (A through L with F1 & F2 Split)
* **Context:** In REV2, Gate F possessed a dual severity (`BLOCKER (Tooling) / MAJOR (Browser)`), creating ambiguity in the gate matrix evaluation.
* **Decision:** Formally split Gate F into two distinct sub-gates:
  * **Gate F1 — Toolchain Runtime Compliance (Severity: BLOCKER):** Enforcing pure Python 3.12.x standard library runtime, zero third-party dependencies, and cross-platform line-ending normalization.
  * **Gate F2 — Standards Compatibility & Reference Browser Verification (Severity: MAJOR):** Enforcing W3C standards feature traceability across engines and automated headless execution on Chrome v153.
* **Consequences:** Eliminates dual-severity ambiguity and ensures each gate evaluates a single, clear responsibility.

---

### ADR-304: Four-Tier Failure Severity Taxonomy
* **Context:** Failures identified during certification may have differing impacts on release viability.
* **Decision:** Adopt a 4-tier failure classification:
  * `BLOCKER`: Direct violation of security, integrity, determinism, or test pass rate; release strictly forbidden.
  * `MAJOR`: Significant standard or accessibility deviation; release blocked unless explicitly waived.
  * `MINOR`: Non-critical cosmetic or documentation issue; release permitted with remediation scheduled for v1.0.1.
  * `ADVISORY`: Informational observation for future roadmap planning; release permitted.
* **Consequences:** Provides clear operational procedures for triage without compromising release standards.

---

### ADR-305: Inviolable Zero-Waiver Domain & 5-State Evaluation Model
* **Context:** Incorporating a waiver model requires mathematical integration into the certification formula without creating loopholes for critical gates.
* **Decision:**
  1. Define 5 explicit gate statuses: `PASS`, `FAIL`, `BLOCKED`, `NOT_APPLICABLE`, `WAIVED`.
  2. A waived gate remains explicitly `WAIVED` in all logs and certificates; it is **NEVER silently coerced or converted to `PASS`**.
  3. Establish an **Inviolable Zero-Waiver Domain** where waivers are strictly forbidden:
     * Gate A (Determinism & Reproducibility)
     * Gate B (Security, Root Trust Anchor, Zero-NPM)
     * Gate D (Artifact Cryptographic Integrity)
     * Gate F1 (Toolchain Python 3.12.x Runtime Contract)
     * Gate I-03 (Master Workspace Test Suite Pass Rate: 100% green / 0 failures)
  4. Only non-critical `MAJOR` or `MINOR` findings in specific waivable gates may receive an executive waiver, exclusively by Lead Architect Mohamed Khalid.
* **Consequences:** Resolves the mathematical contradiction, maintains total transparency, and strictly prevents bypassing core integrity rules.

---

### ADR-306: Four-Tier Cryptographic Trust Chain Verification
* **Context:** The production package must be cryptographically provable from the Root Trust Anchor down to individual output files.
* **Decision:** Validate the complete 4-tier cryptographic chain:
  $$\text{Root Trust Anchor} \rightarrow \text{Source Trust Binding} \rightarrow \text{Canonical Source Manifest} \rightarrow \text{61 Sources} \rightarrow \text{Dist Manifest} \rightarrow \text{33 Dist Artifacts}$$
* **Consequences:** Provides mathematical proof that the distributed code originates exclusively from approved, tamper-free source files.

---

### ADR-307: Calibrated Performance Budget Classification
* **Context:** Performance limits must be categorized to distinguish mandatory gating criteria from directional engineering targets.
* **Decision:** Clearly classify all performance and size budgets into three distinct tiers:
  1. **MANDATORY (Gating):**
     * Total Uncompressed Distribution Package: $\le 1,000,000$ bytes (976.5 KB) across all 33 files in `dist/`. (Current measured baseline: 920,872 bytes with 79,128 bytes headroom).
     * Core CSS Bundle (`dist/bundles/mds.all.css`): $\le 300,000$ bytes.
     * Core JS Bundle (`dist/bundles/mds.all.js`): $\le 120,000$ bytes.
     * Core ESM JS Bundle (`dist/bundles/mds.all.esm.js`): $\le 120,000$ bytes.
  2. **PROPOSED (Non-Gating Targets):**
     * Single Component CSS Target: $< 25,000$ bytes per component file.
     * Single Component JS Target: $< 35,000$ bytes per component file.
  3. **ADVISORY (Informational Benchmark):**
     * Total Estimated Gzip Transfer Footprint: $< 150,000$ bytes (~118.5 KB estimated).
* **Consequences:** Eliminates terminology contradiction and establishes an enforceable, realistic budget contract.

---

### ADR-308: Pure W3C Standards & Zero-NPM Web Runtime Enforcement
* **Context:** Design systems often introduce heavy build dependencies or framework lock-ins.
* **Decision:** Strictly enforce the Zero-NPM mandate. MDS runtime code must execute directly in the browser via standard W3C primitives: CSS Cascade Layers (`@layer`), CSS Custom Properties (`--mds-*`), Web Components Custom Elements (`customElements.define`), and native ECMAScript Modules (`import`/`export`).
* **Consequences:** Consumers can adopt MDS without `npm`, Node.js, or complex build toolchains.

---

### ADR-309: Standards Compatibility + Reference Browser Model (Option B)
* **Context:** In REV2, Gate F claimed multi-browser coverage (Chrome, Firefox, Safari, Edge) while executing live tests solely on Google Chrome v153.
* **Decision:** Formally adopt **Option B: Standards Compatibility + Reference Browser Verification**:
  1. **Google Chrome / Chromium:** Formally certified via live automated headless execution on Chrome v153 on the host platform.
  2. **Mozilla Firefox, Apple Safari, Microsoft Edge:** Formally certified via **Standards-Mapped Feature Traceability**. Static inspection verifies 100% adherence to standard W3C specifications natively supported by these engines (CSS Layers, Container Queries, `:has()`, Custom Elements, ES Modules). No unexecuted live browser lab claims are made.
* **Consequences:** Restores complete technical truthfulness to browser claims and aligns with the standalone environment's actual execution capabilities.

---

### ADR-310: Production Runtime Accessibility Protocol & WCAG Claim Boundary (MAJOR-02 Remediation)
* **Context:** Excluding the Reference Application from certification leaves Gate G without an explicit evidence base unless a dedicated protocol is defined for the production runtime components.
* **Decision:**
  1. Establish a **Production Runtime Accessibility Certification Protocol** executed directly on standalone specimens of all 19 canonical components loaded with production CSS and JS from `dist/`.
  2. Classify all WCAG 2.1 AA criteria into four explicit tiers: `AUTOMATED_VERIFIED` (Gating), `MANUAL_REQUIRED` (Non-gating/Advisory), `NOT_AUTOMATABLE` (Advisory), and `NOT_APPLICABLE`.
  3. **Claim Boundary:** Prohibit claiming "universal WCAG 2.1 AA compliance" without human assistive tech audition. The certificate explicitly claims compliance for **all automatable WCAG 2.1 AA technical contracts** (Contrast, ARIA semantics, focus management, reduced motion).
  4. If Gate G is granted an executive waiver, the certificate must explicitly state that compliance was not fully demonstrated for the waived scope.
* **Consequences:** Provides an objective, airtight verification protocol for runtime UI accessibility without relying on excluded demonstration apps.

---

### ADR-311: Production Certificate Data Model & Evidence Binding (MAJOR-01 Remediation)
* **Context:** A production certificate must be immutably linked to the exact evidence artifacts that justified release.
* **Decision:**
  1. Define the cryptographic integrity mechanism as a **Certificate Integrity Digest** (`certificate_integrity_digest`) computed via SHA-256 over RFC 8785 canonical JSON payload.
  2. Embed `evidence_manifest_binding` (`evidence_manifest_id` and `evidence_manifest_sha256`) directly into the certificate payload.
  3. Define the governance approval mechanism as a separate **Lead Architect Authorization Record** (`architect_authorization_record`) containing Mohamed Khalid's formal decision, timestamp, and attestation statement.
  4. Explicitly declare field `"cryptographic_signer_authenticity_claimed": false` in the certificate schema, confirming that no asymmetric PKI / private key infrastructure is claimed.
* **Consequences:** Creates an unbreakable cryptographic link between the release certificate and the underlying test evidence.

---

### ADR-312: Refined Four-Tier Asset Taxonomy: Subject vs Qualification vs Evidence
* **Context:** Conflating the shipped web product with its qualification tooling or evidence creates confusion regarding what end-users consume.
* **Decision:** Formally categorize all repository assets into four distinct tiers:
  1. **Tier 1: Certification Subject (The Shipped Web Product):** MDS Production Runtime (`MDS/Runtime/`), 18 DTCG Tokens (`MDS/02-Tokens/`), and Production Distribution Package (`dist/` — 33 production artifacts).
  2. **Tier 2: Certification Dependency Qualification:** Host Python 3.12.x stdlib runtime, compiler toolchain (`tools/compiler/`), and bootstrap engine (`tools/agent_bootstrap/`). Qualified to ensure deterministic builds, but NOT shipped as end-user web runtime components.
  3. **Tier 3: Certification Evidence Sources:** Layers 00–13 specifications, Historical Guard (53 sealed docs, 12 manifests), DSSE records, test suite (119 tests), and verification scanners.
  4. **Tier 4: Excluded Artifacts:** MDS Playground (`MDS/Playground/`), MDS Reference Application (`MDS/Reference-Application/`), and ephemeral test fixtures.
* **Consequences:** Establishes unambiguous clarity regarding what is certified versus what serves as supporting evidence, qualified dependencies, or excluded scaffolding.

---

### ADR-313: Calibrated Clean Abort & Non-Destructive Rollback Protocol
* **Context:** Gate K in REV1 required tighter definition regarding sandbox scope and cleanup evidence.
* **Decision:**
  1. Define sandboxes as temporary build directories (`temp_build_*`, staging scratch folders) created during verification.
  2. Enforce sandbox lifecycle management via Python `tempfile.TemporaryDirectory` context managers ensuring guaranteed purge upon exit.
  3. Implement a directory residue audit comparing workspace state before and after execution to confirm exactly zero orphan folders or dangling `.tmp` files.
* **Consequences:** Guarantees repository cleanliness and zero corrupted releases.

---

### ADR-314: Deterministic Evidence Capture Architecture & Measured Zero Sinks
* **Context:** Claims of "zero unsafe JS sinks" must be measurable, and evidence must be systematically archived.
* **Decision:**
  1. Implement an automated static regex scanner verifying zero occurrences of forbidden tokens: `\beval\s*\(`, `\bnew\s+Function\s*\(`, `\bdocument\.write\s*\(`, `\binnerHTML\s*=`, `\bouterHTML\s*=`, `\bjavascript:`.
  2. Stream all verification logs into `evidence/certification/` with ISO-8601 timestamps and individual SHA-256 digests.
* **Consequences:** Provides concrete, measurable evidence for security and code quality claims.

---

### ADR-315: Strict Two-Stage Gate Model (Architecture Approval Prior to Execution)
* **Context:** Premature execution of certification commands violates architectural governance.
* **Decision:** Phase 10.4 is explicitly split into two stages:
  1. **Architecture Stage (Current):** Full architectural specification, decision log, and matrix design. Zero implementation, zero execution, zero certificate issuance.
  2. **Certification Execution Stage:** Triggered ONLY after explicit written authorization from Lead Architect Mohamed Khalid.
* **Consequences:** Preserves strict governance and guarantees that all verification activities proceed according to an approved plan.

---

### ADR-316: Formal Structured Waiver Record & NOT_APPLICABLE Governance
* **Context:** Waivers and N/A determinations must be formally governed to prevent undocumented bypasses and contradictory examples.
* **Decision:**
  1. **Structured Waiver Record:** Every waiver must be recorded with: `waiver_id`, `gate_id`, `reason`, `risk`, `required_evidence`, `authorized_by` ("Mohamed Khalid"), `authorized_at`, `release_version` ("1.0.0"), `scope`, and `review_or_expiry_condition`.
  2. **Synthetic Example:** Illustrate the schema strictly using `WVR-EXAMPLE-001` marked `EXAMPLE_ONLY_NOT_VALID_FOR_RELEASE`. Zero actual waivers exist in the Architecture Stage.
  3. **Waiver Lifecycle:** Waivers apply strictly to v1.0.0 and mandate re-review in v1.0.1.
  4. **NOT_APPLICABLE Governance:** An N/A status requires a documented applicability determination approved exclusively by Mohamed Khalid. N/A is strictly forbidden on any gate in the Zero-Waiver Domain (A, B, D, F1, I-03).
* **Consequences:** Eliminates loopholes and ensures every exception is tracked with full architectural transparency.

---

### ADR-317: Release Integrity Set vs Production Artifact Set Partition
* **Context:** In REV3, Gate A referred to 33 files, whereas the actual output directory `dist/` contains 33 production artifacts plus `mds_dist_manifest.json` and `mds_dist_manifest.sha256` (35 files total).
* **Decision:**
  1. Define **Production Artifact Set (33 Files):** The 33 compiled distribution files declared within `mds_dist_manifest.json`.
  2. Define **Release Integrity Set (35 Files):** The complete set of 35 files on disk in `dist/` (33 production artifacts + `mds_dist_manifest.json` + `mds_dist_manifest.sha256`).
  3. Gate A verifies that all **35 release files** are 100% bit-for-bit identical across dual isolated builds.
  4. Gate D verifies that the 33 production artifacts match the manifest declarations, exactly 35 release files exist on disk, and `mds_dist_manifest.sha256` matches `SHA-256(mds_dist_manifest.json)`.
* **Consequences:** Aligns certification criteria with the true physical distribution package emitted by the Phase 10.3 compiler engine.

---

### ADR-318: Immutable Certification Evidence Manifest Architecture (MAJOR-01 Remediation)
* **Context:** A production certificate must prove which exact evidence logs justified its release decision. If evidence logs can be silently altered, certification integrity is lost.
* **Decision:**
  1. Define the single canonical manifest path: `evidence/certification/certification_evidence_manifest.json` cataloging every gate evidence artifact (`GATE_*.log`) with its relative path, byte size, and SHA-256 hash.
  2. Compute `evidence_manifest_sha256` over the canonical serialization (RFC 8785) of the manifest.
  3. Embed `evidence_manifest_path`, `evidence_manifest_id`, and `evidence_manifest_sha256` directly into `MDS_v1.0.0_PRODUCTION_CERTIFICATE.json`.
  4. Any modification to any evidence log invalidates `evidence_manifest_sha256`, immediately breaking the certificate integrity digest.
* **Consequences:** Guarantees cryptographic immutability across the entire certification evidence trail.

---

### ADR-319: Standalone Trusted Certification Seal & Integrity vs Authenticity Architecture (REV7 Remediation)
* **Context:** In REV6, the Trusted Certification Seal was embedded inside the certificate while being excluded from the certificate integrity digest, meaning an actor with filesystem write permissions could theoretically modify the seal and recalculate the file. Lead Architect Mohamed Khalid required decoupling the seal into an external, standalone governance artifact to establish true separation between cryptographic tamper-evidence and human architectural sign-off.
* **Decision:**
  1. Formally delineate between **Cryptographic Integrity** (SHA-256 tamper-evidence cascading across logs, manifest, and certificate payload) and **Governance Authenticity & Trust** (human architectural ratification).
  2. Implement the **Trusted Certification Seal Record** as a dedicated, standalone governance artifact located at:
     `evidence/certification/trusted_certification_seal.json`.
  3. The standalone seal explicitly records: `seal_id` (`MDS-SEAL-v1.0.0-PROD`), `certificate_id`, `release_identity`, `build_identity`, `evidence_manifest_sha256`, `certificate_integrity_digest`, `authorized_by` ("Mohamed Khalid"), `architect_title` ("Senior Full Stack & Flutter Developer"), `authorized_at`, `seal_status` (`SEALED_APPROVED`), `governance_classification` (`GOVERNANCE_AUTHORIZATION_RECORD`), and `"cryptographic_signer_authenticity_claimed": false`.
  4. The production certificate (`evidence/certification/MDS_v1.0.0_PRODUCTION_CERTIFICATE.json`) references the standalone seal via `trusted_certification_seal_path` and `trusted_certification_seal_id`.
  5. The `certificate_integrity_digest` is computed over the canonical JSON certificate payload (RFC 8785) excluding only the digest field itself, eliminating any awkward exclusions of embedded governance objects.
  6. The seal explicitly affirms: "The Trusted Certification Seal Record is a governance authorization artifact, not a cryptographic digital signature and does not provide cryptographic signer authenticity."
* **Consequences:** Provides absolute architectural separation between cryptographic integrity and human governance authorization.

---

### ADR-320: Calibrated Gate G Scope & Illustrative Values Advisory (REV7 Remediation)
* **Context:** In REV6, Gate G pass criteria stated "Automated WCAG 2.1 AA criteria satisfied on all 19 component specimens", which could be misinterpreted as certifying the 19 components as universally WCAG 2.1 AA compliant. Furthermore, architectural examples contained realistic hash values that must not be mistaken for production evidence.
* **Decision:**
  1. Refine the pass criteria for Gate G to explicitly state:
     `"Automated accessibility criteria mapped to applicable WCAG 2.1 AA requirements are satisfied across all 19 canonical component specimens, within the automated verification scope defined by the Production Runtime Accessibility Protocol."`
  2. Codify the explicit architectural declaration:
     $$\text{Automated Verification} \ne \text{Full Universal WCAG Certification}$$
  3. Formally declare that all SHA-256 hashes, file sizes, and timestamps appearing in schema definitions and examples throughout the Architecture Stage are illustrative example values, not production execution evidence.
* **Consequences:** Eliminates any risk of over-claiming accessibility guarantees and maintains strict technical truthfulness across all documentation.


