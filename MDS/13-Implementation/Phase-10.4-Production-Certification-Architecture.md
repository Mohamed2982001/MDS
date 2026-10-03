<!-- Classification: CURRENT_SPECIFICATION -->
# Master Design System (MDS) — Architecture Specification
## Phase 10.4: MDS v1.0.0 Production Certification Gate

**Document Reference:** `MDS-ARCH-10.4-REV7`  
**Phase:** 10.4 (MDS v1.0.0 Production Certification)  
**Layer:** Layer 13 (Implementation, Tooling & Operationalization)  
**Date:** 2026-10-02  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Audit Stage:** Independent Architecture Audit Final Micro-Remediation Submission (REV7 Final)  
**Status:** **DRAFT (ARCHITECTURE STAGE REMEDIATION REV7) — AWAITING INDEPENDENT ARCHITECTURE AUDIT**  
**Execution Context:** Microsoft Windows, Google Chrome v153, Python 3.12.8 (Pure Standard Library)  
**Certification Guard:** MDS v1.0.0 Certification STRICTLY NOT GRANTED — Architecture Stage Only  

---

## 1. Executive Summary & Certification Mission

The **Master Design System (MDS)** represents an enterprise-grade, mathematically verified, standards-based design system and zero-runtime web architecture. Following the successful ratification, implementation, and cryptographic sealing of the **Design System Selection Engine (DSSE)** in **Phase 10.1**, the **Agent Bootstrap & Handoff Contract** in **Phase 10.2**, and the **Production Compiler & Zero-NPM Distribution Engine** in **Phase 10.3**, Phase 10.4 serves as the **Final Production Certification Gate** for **MDS v1.0.0**.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       MDS v1.0.0 RELEASE LIFECYCLE                          │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
           ┌───────────────────────────┴───────────────────────────┐
           ▼                                                       ▼
┌──────────────────────────────────────┐  ┌───────────────────────────────────┐
│     Phases 00–09: Design System      │  │  Phase 9.7: Master Validation,    │
│  Foundations, Tokens & Components    │  │  Governance & Historical Guards   │
└──────────────────┬───────────────────┘  └─────────────────┬─────────────────┘
                   │                                        │
                   └───────────────────┬────────────────────┘
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Phase 10.1: Design System Selection Engine (DSSE Operational Tooling)       │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Phase 10.2: MDS Agent Bootstrap & Handoff Contract (Autonomous AI Guard)    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Phase 10.3: Production Artifact Compilation & Zero-NPM Distribution Engine  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 10.4: MDS v1.0.0 PRODUCTION CERTIFICATION GATE (REV7)                 │
│ ├── Certified Subject: MDS Runtime, Production Tokens, and dist/ (33 files) │
│ ├── Release Integrity Set: Exactly 35 files (33 artifacts + 2 manifests)    │
│ ├── Evidence Integrity: Canonical certification_evidence_manifest.json      │
│ ├── Standalone Governance Seal: evidence/certification/trusted_seal.json    │
│ ├── Accessibility: Production Runtime Protocol across 19 Canonical Comps   │
│ ├── Browser Model: Standards Compatibility + Reference Browser (Chrome v153)│
│ └── Sole Sign-off Authority: Lead Architect Mohamed Khalid                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.1 Certification Mission
The mission of Phase 10.4 is **not development**, but **authoritative, multi-dimensional verification and formal certification**. It acts as the final inspection checkpoint that evaluates all deliverables, security guarantees, performance footprints, accessibility compliances, standards conformances, and cryptographic trust chains generated throughout the lifecycle of MDS.

Phase 10.4 establishes:
1. **The Production Certification Contract:** A formal, deterministic evaluation protocol consisting of 13 granular Production Certification Gates (Gates A through L, with Gate F formally split into F1 and F2).
2. **Integrity vs Authenticity Separation & Standalone Trusted Certification Seal (MAJOR-01 Remediation):** An architectural framework that explicitly separates cryptographic tamper-evidence (SHA-256 integrity hashes over artifacts, evidence manifest, and certificate payload) from governance authorization (the standalone **Trusted Certification Seal Record** located at `evidence/certification/trusted_certification_seal.json` authorized by Lead Architect Mohamed Khalid). Affirms that SHA-256 provides integrity binding rather than signer authenticity, and that no PKI or asymmetric digital signature is claimed.
3. **Canonical Evidence Manifest Naming (MINOR-01 Remediation):** Unification of all references under the single canonical path: `evidence/certification/certification_evidence_manifest.json`.
4. **Calibrated Production Runtime Accessibility Protocol (MINOR-01 Remediation):** An exhaustive verification protocol executed directly against standalone specimens of all 19 canonical MDS components, with pass criteria explicitly framed around automatable requirements within the defined protocol scope ($\text{Automated Verification} \ne \text{Full Universal WCAG Certification}$).
5. **Subject vs Dependency Qualification Separation:** An explicit separation clarifying that the **Certification Subject** is the shipped web product (MDS Runtime and the 33 production artifacts in `dist/`). Tooling engines (`tools/compiler/`, `tools/agent_bootstrap/`) undergo **Dependency Qualification** to prove deterministic, secure compilation, but are NOT shipped to end-users as runtime components.
6. **Exact Release Artifact Sets:** Rigorous distinction between the **Production Artifact Set** (33 compiled files declared in manifest) and the **Release Integrity Set** (35 physical files on disk in `dist/`, including `mds_dist_manifest.json` and `mds_dist_manifest.sha256`), verified bit-for-bit under Gate A.
7. **Standards Compatibility + Reference Browser Model:** W3C standards-based compatibility across all modern evergreen engines (Chrome, Firefox, Safari, Edge) coupled with live automated reference execution on the local engine (Google Chrome v153).

### 1.2 Strict Scope Creep Prohibition & Inviolable Boundaries
Certification is strictly retrospective and evaluative:
* **Zero Feature Additions:** No new runtime widgets, styles, design tokens, or utility classes may be added under the guise of certification.
* **Zero Tooling Rewrites:** Tooling engines (`tools/agent_bootstrap/`, `tools/compiler/`, `MDS/10-Testing/`) are evaluated in their locked state.
* **Defect Remediation Protocol:** If a verification gate fails during certification execution, the failure constitutes an architectural defect requiring formal root-cause analysis, isolated remediation, and re-audit—never an ad-hoc or opportunistic workaround.
* **Architecture-First Enforcement:** Execution of certification verification commands is strictly prohibited until this Architecture Specification (REV7) receives explicit, written approval from Lead Architect Mohamed Khalid.

### 1.3 Illustrative Architecture Values Advisory
All SHA-256 hashes, file byte sizes, IDs, and timestamps appearing in JSON schema examples and architectural diagrams throughout this specification are **illustrative example values** provided strictly for structural clarity during the Architecture Stage. They do **not** represent production execution evidence, which will be generated exclusively upon explicit authorization during the Certification Execution Stage.

---

## 2. Refined Asset Taxonomy: Subject vs Qualification vs Evidence

To prevent conflating the shippable product with its qualification tooling, evidence sources, or development scaffolding, all repository assets are partitioned into four explicit tiers:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                   REFINED FOUR-TIER ASSET TAXONOMY                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ TIER 1: CERTIFICATION SUBJECT (The Shipped Web Product)                     │
│ ├── 1. MDS Production Design System Runtime (MDS/Runtime/css/)              │
│ ├── 2. MDS Core Primitives (MDS/Runtime/primitives/ — CSS & JS behaviors)  │
│ ├── 3. MDS Accessible UI Components (MDS/Runtime/components/ — Web Comps)   │
│ ├── 4. Canonical Production Tokens (MDS/02-Tokens/ — 18 DTCG JSON files)    │
│ └── 5. Production Distribution Artifacts (dist/ — Exactly 33 artifacts)     │
├─────────────────────────────────────────────────────────────────────────────┤
│ TIER 2: CERTIFICATION DEPENDENCY QUALIFICATION (Operational Toolchains)     │
│ ├── 1. Host Tooling Runtime Contract: Python 3.12.x Standard Library        │
│ ├── 2. Standalone Compiler Engine (tools/compiler/ — Build & Packaging)     │
│ └── 3. Agent Bootstrap Contract Engine (tools/agent_bootstrap/ — Governance)│
│ * NOTE: Tooling is qualified to guarantee deterministic builds, NOT shipped │
│         to end-users as part of the MDS Web Runtime product.                │
├─────────────────────────────────────────────────────────────────────────────┤
│ TIER 3: CERTIFICATION EVIDENCE SOURCES (Authoritative Verification Inputs)  │
│ ├── 1. Canonical Specifications (Layers 00–13 — Documentation Baselines)    │
│ ├── 2. Historical Phase Guard (12 manifests, 53 sealed phase records)       │
│ ├── 3. DSSE Engine Decision Records (Phase 10.1 decision & scoring baselines│
│ ├── 4. Master Workspace Test Suite (119 automated test fixtures)            │
│ ├── 5. Cryptographic Trust Anchors (trust_anchor.json, source_trust_binding)│
│ └── 6. Certification Evidence Manifest & Individual Gate Evidence Logs      │
├─────────────────────────────────────────────────────────────────────────────┤
│ TIER 4: EXCLUDED ARTIFACTS (Non-Production Development Harnesses)           │
│ ├── 1. MDS Playground (MDS/Playground/ — Developer testing sandbox)         │
│ ├── 2. MDS Reference Application (MDS/Reference-Application/ — Dev prototype│
│ └── 3. Unit Test Mock Fixtures & Scratch Directories (Ephemeral test data)  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Production Artifact Set vs Release Integrity Set

To eliminate any ambiguity between the artifacts declared in the distribution manifest and the complete physical file set emitted into `dist/`, MDS v1.0.0 establishes the following formal definitions:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DISTRIBUTION FILE SET PARTITION                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  RELEASE INTEGRITY SET (35 Files on disk in dist/)                          │
│  │                                                                          │
│  ├── 1. PRODUCTION ARTIFACT SET (33 Files declared in mds_dist_manifest.json│
│  │   ├── Archives (2 files): mds-v1.0.0-dist.tar.gz, mds-v1.0.0-dist.zip    │
│  │   ├── Bundles (3 files): mds.all.css, mds.all.esm.js, mds.all.js         │
│  │   ├── Components (19 files): css/components/*.css                        │
│  │   ├── Modular Layer CSS (3 files): mds.components, primitives, tokens    │
│  │   ├── Modular Layer JS (2 files): mds.components.js, mds.primitives.js   │
│  │   ├── Tokens (3 files): tokens.css, tokens.d.ts, tokens.json             │
│  │   └── Types (1 file): types/components.d.ts                              │
│  │                                                                          │
│  └── 2. DISTRIBUTION INTEGRITY METADATA (2 Files securing the release)      │
│      ├── mds_dist_manifest.json (Cryptographic inventory & build identity) │
│      └── mds_dist_manifest.sha256 (Companion SHA-256 digest of manifest)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Gating Rules for the 35 Release Files
1. **Gate A (Determinism):** Every dual compilation run must produce all **35 release files** in `dist/` with 100% bit-for-bit identical SHA-256 hashes across isolated runs, identical $I_{build}$, identical `mds_dist_manifest.json`, and identical `mds_dist_manifest.sha256`.
2. **Gate D (Artifact Integrity):** Verifies that exactly 33 production artifacts are declared in `mds_dist_manifest.json`, all 33 match their declared digests, exactly 35 release files exist in `dist/` with zero extraneous files, and companion `mds_dist_manifest.sha256` matches `SHA-256(mds_dist_manifest.json)`.
3. **Gate J (BOM):** Catalogs both the 33 production artifacts and the 2 integrity metadata files.

---

## 4. Integrity vs Authenticity & Standalone Trusted Certification Seal (MAJOR-01 & MINOR-01 Remediation)

To maintain absolute technical precision, the certification architecture explicitly demarcates **Cryptographic Integrity** from **Governance Authenticity & Trust**.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                 INTEGRITY VS AUTHENTICITY ARCHITECTURE (REV7)               │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. CRYPTOGRAPHIC INTEGRITY (Tamper-Evidence via SHA-256)                    │
│    Individual Gate Logs (evidence/certification/GATE_*.log)                 │
│         ↓ (Hashed: SHA-256)                                                 │
│    Canonical Evidence Manifest (evidence/certification/certification_evidence_manifest.json)│
│         ↓ (Hashed: evidence_manifest_sha256 via RFC 8785)                   │
│    Production Certificate (evidence/certification/MDS_v1.0.0_PRODUCTION_CERTIFICATE.json)│
│         ↓ (Hashed: certificate_integrity_digest via RFC 8785)               │
│    Guarantees: Any byte alteration breaks the cryptographic hash chain.     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. GOVERNANCE AUTHENTICITY & TRUST (Authoritative Human Sealing)            │
│    Certificate Integrity Digest + Evidence Manifest SHA-256                 │
│         ↓ (Bound into Standalone Governance Artifact)                       │
│    Standalone Trusted Seal: evidence/certification/trusted_certification_seal.json│
│         ↓ (Authorized exclusively by)                                       │
│    Lead Architect Mohamed Khalid (Senior Full Stack & Flutter Developer)    │
│    Guarantees: Release legitimacy is established through explicit human     │
│    architectural sign-off, completely external to the certificate file.     │
│    Affirms: "cryptographic_signer_authenticity_claimed": false (No PKI).   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.1 Four Distinct Verification Dimensions
1. **Artifact Integrity:** The 35 release files in `dist/` match their declared cryptographic digests.
2. **Evidence Integrity:** The 13 individual gate evidence logs match the digests recorded in `evidence/certification/certification_evidence_manifest.json`.
3. **Certificate Integrity:** The certificate payload matches `certificate_integrity_digest` computed via RFC 8785 canonicalization.
4. **Governance Authorization:** The standalone **Trusted Certification Seal Record** (`evidence/certification/trusted_certification_seal.json`) explicitly binds the release to the authority of Lead Architect Mohamed Khalid with status `SEALED_APPROVED`.

### 4.2 Canonical Evidence Manifest Schema (`evidence/certification/certification_evidence_manifest.json`)
The canonical file path is strictly pinned across the entire repository to:
`evidence/certification/certification_evidence_manifest.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "evidence_manifest_id": "MDS-EVID-v1.0.0-9a8b7c6d5e4f3a2b",
  "release_identity": "MDS-v1.0.0-RELEASE",
  "build_identity": "426b8bf473112cf5a46f7535e85d821efab7a5b2b6603b39ec7f52840fb9f526",
  "source_identity": "34cd5128a6258cdfb09bed3f0002eaf9910610bc8ebf3fda16034cef6a815a73",
  "timestamp": "2026-10-02T22:00:00Z",
  "gate_evidence_map": {
    "Gate_A": {
      "log_file": "evidence/certification/GATE_A_determinism_multi_build.log",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "byte_size": 12450
    },
    "Gate_B": {
      "log_file": "evidence/certification/GATE_B_security_trust_chain.log",
      "sha256": "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
      "byte_size": 8920
    },
    "Gate_C": {
      "log_file": "evidence/certification/GATE_C_standards_zero_npm.log",
      "sha256": "ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d",
      "byte_size": 6540
    },
    "Gate_D": {
      "log_file": "evidence/certification/GATE_D_artifact_integrity.log",
      "sha256": "c8ad4dd08922fe5ad7773b26d16f846ab507968311f47e81cafba4ce4dfaa6f9",
      "byte_size": 15800
    },
    "Gate_E": {
      "log_file": "evidence/certification/GATE_E_size_performance_budgets.log",
      "sha256": "7d48eb77e3a1eae39f4fa577bc5de9f1d6eb505ed0e26047bc72c5facd8c8a51",
      "byte_size": 7430
    },
    "Gate_F1": {
      "log_file": "evidence/certification/GATE_F1_toolchain_runtime.log",
      "sha256": "d1df7c4562b1134d9d063fba0f73fd1c29ba4f2abdfea18324ba807df5577692",
      "byte_size": 5120
    },
    "Gate_F2": {
      "log_file": "evidence/certification/GATE_F2_browser_compatibility.log",
      "sha256": "876cd0e22ee947db0e9b53da8c5d50e04c28e7fc316add6ff7eca95050ce87f8",
      "byte_size": 11200
    },
    "Gate_G": {
      "log_file": "evidence/certification/GATE_G_accessibility_wcag.log",
      "sha256": "99efe99e4ca77d29f57f01890b2e1a582133817c4114239059ed61033cb27e39",
      "byte_size": 24500
    },
    "Gate_H": {
      "log_file": "evidence/certification/GATE_H_responsive_rtl.log",
      "sha256": "f01009093c162eea772cc1218a9db159858e2637563d3ab50c07c602814e57aa",
      "byte_size": 9340
    },
    "Gate_I": {
      "log_file": "evidence/certification/GATE_I_versioning_governance.log",
      "sha256": "c3aaa81caf4a48fa3a4b0d1ca7e543c1617d5761db7015618399e8bfbd363628",
      "byte_size": 18200
    },
    "Gate_J": {
      "log_file": "evidence/certification/GATE_J_release_bom.log",
      "sha256": "8381d511b302bf76fc259165d77c55fff70f968284496e0f7e6a166f3249aa35",
      "byte_size": 14100
    },
    "Gate_K": {
      "log_file": "evidence/certification/GATE_K_rollback_recovery.log",
      "sha256": "20c240e650a447299690d0e2f65c65a0dbed2acc4aba9de9997c4a093f2ed114",
      "byte_size": 6800
    },
    "Gate_L": {
      "log_file": "evidence/certification/GATE_L_sign_off_attestation.log",
      "sha256": "bc77421d30408375ad4c197cfa2db12dbaa18b395bd06928da64bbc3f41c5744",
      "byte_size": 4300
    }
  }
}
```

### 4.3 Standalone Trusted Certification Seal Record Schema (`evidence/certification/trusted_certification_seal.json`)
To guarantee that human governance authorization remains independent of and external to the certificate file itself, the **Trusted Certification Seal Record** is persisted as a dedicated, standalone governance artifact at:
`evidence/certification/trusted_certification_seal.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "seal_id": "MDS-SEAL-v1.0.0-PROD",
  "certificate_id": "MDS-CERT-v1.0.0-426b8bf473112cf5",
  "release_identity": "MDS-v1.0.0-RELEASE",
  "build_identity": "426b8bf473112cf5a46f7535e85d821efab7a5b2b6603b39ec7f52840fb9f526",
  "evidence_manifest_sha256": "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
  "certificate_integrity_digest": "c8ad4dd08922fe5ad7773b26d16f846ab507968311f47e81cafba4ce4dfaa6f9",
  "authorized_by": "Mohamed Khalid",
  "architect_title": "Senior Full Stack & Flutter Developer",
  "authorized_at": "2026-10-02T22:30:00Z",
  "seal_status": "SEALED_APPROVED",
  "governance_classification": "GOVERNANCE_AUTHORIZATION_RECORD",
  "cryptographic_signer_authenticity_claimed": false
}
```

> [!IMPORTANT]
> **Definitive Architectural Boundary:**  
> The Trusted Certification Seal Record is a **governance authorization artifact**, not a cryptographic digital signature and does not provide cryptographic signer authenticity. Release legitimacy is established through explicit human architectural sign-off, completely external to the certificate payload.

---

## 5. Production Runtime Accessibility Certification Protocol

Because the Reference Application and Playground are excluded from the Certification Subject, Gate G must evaluate the **actual in-scope production components** via standalone component specimens.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│             PRODUCTION RUNTIME ACCESSIBILITY PROTOCOL (GATE G)              │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Target Scope: All 19 Canonical MDS Components                            │
│    alert, badge, button, card, checkbox, dialog, field, icon-button, input, │
│    link, radio, select, skeleton, spinner, switch, table, tabs, textarea,   │
│    tooltip. (Specimens rendered directly from dist/ CSS & JS).              │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. Multi-Dimensional Verification Matrix:                                   │
│    ├── A. Semantic Structure & ARIA: Standard roles, states, accessible name│
│    ├── B. Color Contrast: Token contrast computation (>= 4.5:1 / 3:1)       │
│    ├── C. Keyboard & Focus Trap: Tab, Arrows, Enter, Esc, focus restoration │
│    ├── D. Live Announcements: aria-live polite/assertive in alert/regions   │
│    ├── E. Motion Sensitivity: prefers-reduced-motion CSS override rules     │
│    └── F. Interaction Targets: 44x44px minimum touch target enforcement     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. Strict Classification of WCAG 2.1 AA Criteria:                           │
│    ├── AUTOMATED_VERIFIED: Fully proven via automated headless DOM tests    │
│    ├── MANUAL_REQUIRED: Requires human screen reader audition               │
│    ├── NOT_AUTOMATABLE: Contextual copywriting / cognitive readability      │
│    └── NOT_APPLICABLE: Media / audio / video criteria not relevant to UI lib│
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. Calibrated Claim Boundary:                                               │
│    Certificate claims compliance ONLY for AUTOMATED_VERIFIED criteria;      │
│    prohibits claiming full universal WCAG 2.1 AA without manual audition.   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.1 Component Coverage & Specimen Registry (19 Components)
Every canonical MDS component is verified using a standalone HTML specimen loaded with `dist/bundles/mds.all.css` and `dist/bundles/mds.all.esm.js`:

| Component Name | File Targets | Primary Accessibility Contracts Evaluated |
| :--- | :--- | :--- |
| **`alert`** | `css/components/alert.css` | `role="alert"`, `aria-live="assertive"`, high-contrast borders |
| **`badge`** | `css/components/badge.css` | Semantic span, contrast $\ge 4.5:1$, aria-hidden icons |
| **`button`** | `css/components/button.css` | Native `<button>`, visible `:focus-visible`, 44px press target |
| **`card`** | `css/components/card.css` | Semantic container, surface contrast, keyboard boundary |
| **`checkbox`** | `css/components/checkbox.css`| Native input / `role="checkbox"`, `aria-checked`, keyboard Space |
| **`dialog`** | `css/components/dialog.css`, `js/mds.components.js` | `role="dialog"`, `aria-modal="true"`, focus trap, Escape dismissal, focus restore |
| **`field`** | `css/components/field.css` | `<label for="...">`, `aria-describedby` helper/error association |
| **`icon-button`** | `css/components/icon-button.css` | Mandatory `aria-label`, 44x44px target, `:focus-visible` ring |
| **`input`** | `css/components/input.css` | Accessible name, `aria-invalid`, autocomplete, clear focus outline |
| **`link`** | `css/components/link.css` | Native `<a>`, distinguishable from text, contrast $\ge 4.5:1$ |
| **`radio`** | `css/components/radio.css` | `role="radiogroup"`, Arrow key roving navigation, `aria-checked` |
| **`select`** | `css/components/select.css` | Native `<select>` or listbox ARIA pattern, keyboard navigation |
| **`skeleton`** | `css/components/skeleton.css`| `aria-busy="true"`, `aria-hidden="true"`, reduced-motion pulse halt |
| **`spinner`** | `css/components/spinner.css` | `role="status"`, `aria-label="Loading"`, motion sensitivity |
| **`switch`** | `css/components/switch.css`, `js/mds.components.js` | `role="switch"`, `aria-checked="true|false"`, Space key toggle |
| **`table`** | `css/components/table.css` | `<th scope="col|row">`, `<caption>`, responsive container wrap |
| **`tabs`** | `css/components/tabs.css`, `js/mds.components.js` | `role="tablist"`, `role="tab"`, `role="tabpanel"`, Arrow navigation |
| **`textarea`** | `css/components/textarea.css`| Label association, resize constraints, visible focus ring |
| **`tooltip`** | `css/components/tooltip.css`, `js/mds.components.js` | `role="tooltip"`, `aria-describedby`, Escape dismiss, hover/focus trigger |

### 5.2 Four-Tier WCAG 2.1 AA Criteria Classification

| Classification Tier | Definition | Scope in Phase 10.4 | Verification Method |
| :--- | :--- | :--- | :--- |
| **`AUTOMATED_VERIFIED`** | Objectively measurable technical criteria (Contrast, ARIA attributes, keyboard traps, focus rings, reduced motion). | **GATING (Gate G)** | Headless Chrome DOM execution + static AST inspection. |
| **`MANUAL_REQUIRED`** | Criteria requiring human assistive technology testing (Screen reader announcement flow, pronunciation, cognitive clarity). | **NON-GATING (Advisory)**| Documented as requiring application-level testing with NVDA / VoiceOver. |
| **`NOT_AUTOMATABLE`** | Subjective or contextual criteria (Meaningful image alt text, plain language readability). | **NON-GATING (Advisory)**| Governed by authoring guidelines in Layer 08; not mechanically verifiable in component library. |
| **`NOT_APPLICABLE`** | Media, audio, video, or full-page specific criteria (Captions, audio descriptions, bypass blocks). | **NOT APPLICABLE** | Formally documented as N/A to a UI component distribution. |

### 5.3 Calibrated WCAG Claim Boundary
The production certificate **strictly limits its claim** to the verified evidence:
* **Permitted Claim:** `"MDS v1.0.0 Production Component UI satisfies all automatable WCAG 2.1 AA technical contracts (Color Contrast, ARIA Semantics, Keyboard Focus Management, and Reduced Motion) across all 19 canonical components."`
* **Prohibited Claim:** Stating that MDS v1.0.0 provides "complete universal WCAG 2.1 AA compliance" without human assistive tech audition.

---

## 6. Standards Compatibility & Reference Browser Model (Option B)

| Browser Engine / Family | Minimum Supported Version | Verification Method | Live Execution Status | Official Certification Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **Google Chrome / Chromium** | **Chrome $\ge 115$** | Automated headless DOM execution in Chrome v153 | **LIVE EXECUTED (Local)** | **LIVE CERTIFIED** |
| **Mozilla Firefox (Gecko)** | **Firefox $\ge 115$** | W3C Static AST & Feature Support Traceability | **NOT LIVE EXECUTED** | **STANDARDS-COMPATIBLE VERIFIED** |
| **Apple Safari (WebKit)** | **Safari $\ge 16.4$** | W3C Static AST & Feature Support Traceability | **NOT LIVE EXECUTED** | **STANDARDS-COMPATIBLE VERIFIED** |
| **Microsoft Edge (Chromium)**| **Edge $\ge 115$** | Chromium Engine Alignment + Static AST Traceability | **NOT LIVE EXECUTED** | **STANDARDS-COMPATIBLE VERIFIED** |

---

## 7. Formal Waiver Record & Accessibility Claim Calibration

### 7.1 Synthetic Waiver Record Schema Example
```json
{
  "waiver_id": "WVR-EXAMPLE-001",
  "gate_id": "Gate_E_04",
  "status": "EXAMPLE_ONLY_NOT_VALID_FOR_RELEASE",
  "reason": "Synthetic Schema Example: A hypothetical non-gating modular component CSS budget exception.",
  "risk": "Illustrative Risk Assessment: Modular file variance does not impact core bundle or total package cap.",
  "required_evidence": "evidence/certification/GATE_E_size_performance_budgets.log",
  "authorized_by": "Mohamed Khalid",
  "authorized_at": "2026-10-02T00:00:00Z",
  "release_version": "1.0.0",
  "scope": "dist/css/components/example.css",
  "review_or_expiry_condition": "Valid for v1.0.0 release only; mandatory review and refactoring in v1.0.1 maintenance release."
}
```
* **Governance Invariant:** ZERO actual waivers exist or are granted during the Architecture Stage.

### 7.2 Accessibility Claim Calibration
If Gate G is granted an executive waiver by Lead Architect Mohamed Khalid, the production certificate **strictly forbids** claiming full WCAG 2.1 AA compliance. It must explicitly record:
1. `Gate_G.status = "WAIVED"`.
2. Formal waiver record and scope.
3. Explicit certification limitation statement:
   `"Gate G was granted an executive waiver; therefore WCAG 2.1 AA compliance was not fully demonstrated for the waived scope."`
A waived accessibility gate is **never silently represented as a full PASS**.

### 7.3 Inviolable Zero-Waiver Domain
Waivers and N/A determinations are **strictly forbidden** for:
$$\text{ZeroWaiverDomain} = \{\text{Gate A}, \text{Gate B}, \text{Gate D}, \text{Gate F1}, \text{Gate I-03 (Master Workspace Test Suite 100\% Green)}\}$$

---

## 8. The 13 Granular Certification Gates

| Gate ID | Domain | Requirement Description | Pass Criteria | Severity | Release Impact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Gate A** | Determinism | Bit-for-bit reproducible dual compile ($T_{epoch}=1790812800$) | All **35 release files** match identical SHA-256; $I_{build}$ matches | **BLOCKER** | Non-Waivable |
| **Gate B** | Security | Zero-NPM, 4-tier trust chain, measured zero unsafe JS sinks, Core intact | Trust chain valid; zero forbidden sinks; 94/94 core intact | **BLOCKER** | Non-Waivable |
| **Gate C** | Standards | Pure W3C standards: CSS Cascade Layers, Custom Properties, Custom Elements, ESM | 100% adherence to standard primitives; zero polyfills | **MAJOR** | Waivable |
| **Gate D** | Artifacts | Exactly 33 production artifacts declared; 35 release files in `dist/` | 33 declared artifacts match; 35 files present; verify CLI exit 0 | **BLOCKER** | Non-Waivable |
| **Gate E** | Budgets | **MANDATORY:** Total package $\le 1\text{MB}$, Core CSS $\le 300\text{KB}$, Core JS $\le 120\text{KB}$ | Physical byte sizes $\le$ mandatory limits (Current: 920,872 bytes) | **MAJOR** | Waivable |
| **Gate F1**| Toolchain | Pure Python 3.12.x stdlib contract + CRLF/LF stream normalization | Zero third-party imports; canonical hashing invariant verified | **BLOCKER** | Non-Waivable |
| **Gate F2**| Browser | Standards compatibility mapping + Chrome v153 live headless execution | W3C traceability complete; Chrome headless DOM execution clean | **MAJOR** | Waivable |
| **Gate G** | Accessibility | Production Runtime Accessibility Protocol across all 19 canonical components | Automated accessibility criteria mapped to applicable WCAG 2.1 AA requirements are satisfied across all 19 canonical component specimens, within the automated verification scope defined by the Production Runtime Accessibility Protocol | **MAJOR** | Waivable |
| **Gate H** | Responsive & RTL | CSS Logical Properties exclusively, `softWrap: true` (no ellipsis), compact mode | Zero physical left/right; bidirectional flip verified; text wraps | **MAJOR** | Waivable |
| **Gate I** | Versioning | SemVer 1.0.0 locked across manifests; monotonic phase; 119/119 tests green | 100% version alignment; phase valid; 119/119 tests pass | **BLOCKER** | Non-Waivable |
| **Gate J** | BOM | 6-Tier Release Bill of Materials: 61 sources, 33 non-sources, 35 release files | Complete inventory accounted for; dev fixtures isolated | **BLOCKER** | Non-Waivable |
| **Gate K** | Recovery | Atomic release evaluation; temporary sandbox cleanup with zero orphan residue | Evaluation halts on failure; zero residual temp files/folders | **BLOCKER** | Non-Waivable |
| **Gate L** | Sign-off | All Gates evaluate to PASS, N/A, or approved WAIVED; Mohamed Khalid sign-off | Zero Blockers, Zero unapproved Majors; formal written attestation | **BLOCKER** | Non-Waivable |

---

## 9. Production Certificate Data Model & Trusted Certification Seal (MAJOR-01 Remediation)

The production certificate embeds the cryptographic evidence manifest binding and references the standalone **Trusted Certification Seal Record**.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "MDSProductionCertificate",
  "type": "object",
  "required": [
    "schema_version",
    "certificate_id",
    "release_id",
    "package_name",
    "version",
    "certification_timestamp",
    "certification_subject_summary",
    "release_file_summary",
    "root_trust_anchor",
    "identity_contract",
    "evidence_manifest_binding",
    "gate_evaluations",
    "waiver_records",
    "not_applicable_determinations",
    "verdict",
    "certificate_integrity_digest",
    "trusted_certification_seal_path",
    "trusted_certification_seal_id"
  ],
  "properties": {
    "schema_version": { "type": "string", "const": "1.0.0" },
    "certificate_id": { "type": "string", "pattern": "^MDS-CERT-v1\\.0\\.0-[0-9a-f]{16}$" },
    "release_id": { "type": "string", "const": "MDS-v1.0.0-RELEASE" },
    "package_name": { "type": "string", "const": "master-design-system" },
    "version": { "type": "string", "const": "1.0.0" },
    "certification_timestamp": { "type": "string", "format": "date-time" },
    "certification_subject_summary": {
      "type": "object",
      "required": ["subject_scope", "runtime_files_count", "compiled_distribution_artifacts_count", "excluded_harnesses"],
      "properties": {
        "subject_scope": { "type": "string", "const": "MDS v1.0.0 Production Design System Runtime & Distribution Package" },
        "runtime_files_count": { "type": "integer", "const": 61 },
        "compiled_distribution_artifacts_count": { "type": "integer", "const": 33 },
        "excluded_harnesses": {
          "type": "array",
          "items": { "type": "string" },
          "default": ["MDS/Playground/", "MDS/Reference-Application/", "MDS/10-Testing/fixtures/"]
        }
      }
    },
    "release_file_summary": {
      "type": "object",
      "required": ["production_artifacts_count", "integrity_metadata_files_count", "total_release_files_count", "total_artifact_bytes"],
      "properties": {
        "production_artifacts_count": { "type": "integer", "const": 33 },
        "integrity_metadata_files_count": { "type": "integer", "const": 2 },
        "total_release_files_count": { "type": "integer", "const": 35 },
        "total_artifact_bytes": { "type": "integer" }
      }
    },
    "root_trust_anchor": {
      "type": "object",
      "required": ["anchor_id", "fingerprint"],
      "properties": {
        "anchor_id": { "type": "string", "const": "MDS-ROOT-ANCHOR-v1" },
        "fingerprint": { "type": "string", "const": "20c240e650a447299690d0e2f65c65a0dbed2acc4aba9de9997c4a093f2ed114" }
      }
    },
    "identity_contract": {
      "type": "object",
      "required": ["source_identity", "compiler_identity", "config_identity", "environment_identity", "build_epoch", "build_identity"],
      "properties": {
        "source_identity": { "type": "string", "pattern": "^[0-9a-f]{64}$" },
        "compiler_identity": { "type": "string", "pattern": "^[0-9a-f]{64}$" },
        "config_identity": { "type": "string", "pattern": "^[0-9a-f]{64}$" },
        "environment_identity": { "type": "string", "pattern": "^[0-9a-f]{64}$" },
        "build_epoch": { "type": "integer" },
        "build_identity": { "type": "string", "pattern": "^[0-9a-f]{64}$" }
      }
    },
    "evidence_manifest_binding": {
      "type": "object",
      "required": ["evidence_manifest_path", "evidence_manifest_id", "evidence_manifest_sha256", "total_evidence_files_count"],
      "properties": {
        "evidence_manifest_path": { "type": "string", "const": "evidence/certification/certification_evidence_manifest.json" },
        "evidence_manifest_id": { "type": "string", "pattern": "^MDS-EVID-v1\\.0\\.0-[0-9a-f]{16}$" },
        "evidence_manifest_sha256": { "type": "string", "pattern": "^[0-9a-f]{64}$" },
        "total_evidence_files_count": { "type": "integer", "const": 13 }
      }
    },
    "gate_evaluations": {
      "type": "object",
      "required": ["Gate_A", "Gate_B", "Gate_C", "Gate_D", "Gate_E", "Gate_F1", "Gate_F2", "Gate_G", "Gate_H", "Gate_I", "Gate_J", "Gate_K", "Gate_L"],
      "additionalProperties": {
        "type": "object",
        "required": ["name", "status", "blockers", "majors", "minors", "evidence_digest"],
        "properties": {
          "name": { "type": "string" },
          "status": { "type": "string", "enum": ["PASS", "FAIL", "BLOCKED", "NOT_APPLICABLE", "WAIVED"] },
          "blockers": { "type": "integer", "minimum": 0 },
          "majors": { "type": "integer", "minimum": 0 },
          "minors": { "type": "integer", "minimum": 0 },
          "evidence_digest": { "type": "string", "pattern": "^[0-9a-f]{64}$" }
        }
      }
    },
    "waiver_records": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "waiver_id",
          "gate_id",
          "reason",
          "risk",
          "required_evidence",
          "authorized_by",
          "authorized_at",
          "release_version",
          "scope",
          "review_or_expiry_condition"
        ],
        "properties": {
          "waiver_id": { "type": "string", "pattern": "^WVR-[0-9A-Z-]+$" },
          "gate_id": { "type": "string" },
          "reason": { "type": "string" },
          "risk": { "type": "string" },
          "required_evidence": { "type": "string" },
          "authorized_by": { "type": "string", "const": "Mohamed Khalid" },
          "authorized_at": { "type": "string", "format": "date-time" },
          "release_version": { "type": "string", "const": "1.0.0" },
          "scope": { "type": "string" },
          "review_or_expiry_condition": { "type": "string" }
        }
      }
    },
    "not_applicable_determinations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["determination_id", "gate_id", "rationale", "authorized_by", "authorized_at"],
        "properties": {
          "determination_id": { "type": "string", "pattern": "^NA-[0-9A-Z-]+$" },
          "gate_id": { "type": "string" },
          "rationale": { "type": "string" },
          "authorized_by": { "type": "string", "const": "Mohamed Khalid" },
          "authorized_at": { "type": "string", "format": "date-time" }
        }
      }
    },
    "verdict": {
      "type": "object",
      "required": ["status", "total_blockers", "total_majors", "total_minors", "total_waived", "total_na", "certification_decision"],
      "properties": {
        "status": { "type": "string", "enum": ["CERTIFIED", "REJECTED"] },
        "total_blockers": { "type": "integer", "const": 0 },
        "total_majors": { "type": "integer", "const": 0 },
        "total_minors": { "type": "integer" },
        "total_waived": { "type": "integer" },
        "total_na": { "type": "integer" },
        "certification_decision": { "type": "string" }
      }
    },
    "certificate_integrity_digest": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$",
      "description": "Deterministic SHA-256 hash over canonical JSON payload (RFC 8785) excluding this certificate_integrity_digest field."
    },
    "trusted_certification_seal_path": {
      "type": "string",
      "const": "evidence/certification/trusted_certification_seal.json",
      "description": "Relative filesystem path to the external standalone governance authorization seal."
    },
    "trusted_certification_seal_id": {
      "type": "string",
      "const": "MDS-SEAL-v1.0.0-PROD",
      "description": "Identifier of the external standalone governance seal authorizing this release."
    }
  }
}
```

---

## 10. Final Decision Calculus (Boolean Evaluation)

The release certification decision is governed by a formal Boolean calculus incorporating all 13 gates, the waiver records, the N/A determinations, the immutable evidence manifest, and the Trusted Certification Seal:

$$\text{ReleaseCertified} \iff \left(\bigwedge_{g \in \text{Gates}} \text{ValidGateState}(g)\right) \land (\text{Count}(\text{BLOCKER}) = 0) \land (\text{Count}(\text{Unapproved MAJOR}) = 0) \land \text{EvidenceManifestBound} \land \text{CertificationSealRatified}$$

Where:
1. **Valid Gate State:**
   $$\text{ValidGateState}(g) \iff \text{Status}(g) \in \{\text{PASS}, \text{NOT\_APPLICABLE}, \text{WAIVED}\}$$
2. **Strict Waiver Validity:**
   $$\text{Status}(g) = \text{WAIVED} \implies (g \notin \text{ZeroWaiverDomain}) \land \text{AuthorizedWaiver}(\text{Mohamed Khalid}, g) \land \text{ValidWaiverRecord}(g)$$
   Where:
   $$\text{ZeroWaiverDomain} = \{\text{Gate A}, \text{Gate B}, \text{Gate D}, \text{Gate F1}, \text{Gate I-03 (Master Workspace Test Suite 100\% Green)}\}$$
3. **Strict NOT_APPLICABLE Validity:**
   $$\text{Status}(g) = \text{NOT\_APPLICABLE} \implies (g \notin \text{ZeroWaiverDomain}) \land \text{DocumentedDetermination}(\text{Mohamed Khalid}, g)$$
4. **Immutable Evidence Binding:**
   $$\text{EvidenceManifestBound} \iff \mathcal{H}(\text{CanonicalEvidenceManifest}) \equiv \text{Certificate}.\text{evidence\_manifest\_sha256}$$
5. **Certification Seal Ratification:**
   $$\text{CertificationSealRatified} \iff (\text{Seal}.\text{seal\_id} \equiv \text{Certificate}.\text{trusted\_certification\_seal\_id}) \land (\text{Seal}.\text{certificate\_integrity\_digest} \equiv \text{Certificate}.\text{certificate\_integrity\_digest}) \land (\text{Seal}.\text{evidence\_manifest\_sha256} \equiv \text{Certificate}.\text{evidence\_manifest\_sha256}) \land (\text{Seal}.\text{authorized\_by} \equiv \text{"Mohamed Khalid"}) \land (\text{Seal}.\text{seal\_status} \equiv \text{SEALED\_APPROVED})$$

---

## 11. Implementation & Scope Boundaries for Phase 10.4

### 11.1 Strictly Forbidden in Phase 10.4
* Creating or editing files in `MDS/Runtime/` (Protected Core).
* Creating or editing token definitions in `MDS/02-Tokens/` (Protected Core).
* Modifying historical documentation or manifests in `MDS/13-Implementation/` (Phases 9.1–10.3).
* Adding Node.js, npm, or Python third-party dependencies.
* Claiming production certification before architecture approval and execution verification.
* Marking Phase 10.4 as `SEALED` during the architecture stage.

### 11.2 Authorized in Phase 10.4 Architecture Stage
* Authoring `Phase-10.4-Production-Certification-Architecture.md` (this document).
* Authoring `Phase-10.4-Decision-Log.md`.
* Generating the Brain summary artifact for Lead Architect review.
* Running read-only verification commands to inspect existing baselines.

---

## 12. Formal Sign-off & Executive Authority

### 12.1 Attestation Protocol
Formal certification of MDS v1.0.0 requires the personal, explicit review and written attestation of Lead Architect **Mohamed Khalid**.

### 12.2 Attestation Template
```text
================================================================================
          MASTER DESIGN SYSTEM (MDS) v1.0.0 — PRODUCTION CERTIFICATE
================================================================================
I, Mohamed Khalid, Lead Architect (Senior Full Stack & Flutter Developer),
hereby attest that Master Design System (MDS) v1.0.0 has undergone exhaustive,
independent production certification across all 13 mandatory certification gates.

I confirm that:
1. Determinism: All 35 release files are bit-for-bit reproducible across environments.
2. Security: The system is 100% Zero-NPM with an unbroken 4-tier trust chain.
3. Quality: Master test suite (119/119) and historical guards (53/53) are green.
4. Standards: Architecture conforms natively to W3C standards and automatable WCAG 2.1 AA.
5. Scope: Certification strictly applies to MDS Runtime & Distribution Package.
6. Evidence: The release is immutably bound to Certification Evidence Manifest SHA-256.
7. Seal: The Trusted Certification Seal Record is formally ratified.
8. Browser: Standards compatibility mapped; reference execution verified on Chrome.

STATUS: APPROVED & CERTIFIED FOR PRODUCTION
DATE: [Pending Execution Stage]
LEAD ARCHITECT: Mohamed Khalid
================================================================================
```

---

## 13. Exit Criteria for Phase 10.4 Architecture Stage

The Architecture Stage of Phase 10.4 will be formally complete and eligible for transition to Certification Execution when:
1. This Architecture Specification (`MDS-ARCH-10.4-REV7`) is submitted and reviewed.
2. The Decision Log (`Phase-10.4-Decision-Log.md`) records all updated architectural decisions (ADR-301 through ADR-320).
3. The brain summary report is generated.
4. Master test suite (119/119) and Protected Core integrity (94/94) are verified intact.
5. **Lead Architect Mohamed Khalid grants explicit, written ARCHITECTURE APPROVAL.**
