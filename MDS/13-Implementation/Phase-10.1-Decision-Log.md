<!-- Classification: CURRENT_SPECIFICATION -->
# Master Design System (MDS) — Architecture Decision Log
## Phase 10.1: DSSE Operational CLI Tooling (`mds-dsse`)

**Document Reference:** `MDS-DEC-10.1-REV1`  
**Phase:** 10.1 (DSSE Operational CLI Tooling)  
**Layer:** Layer 13 (Implementation, Tooling & Operationalization)  
**Date:** 2026-10-01  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Status:** **PHASE 10.1 IMPLEMENTATION COMPLETE — AWAITING INDEPENDENT IMPLEMENTATION AUDIT**  
**Execution Context:** Microsoft Windows, Google Chrome v153, Python 3.12.8 (Pure Standard Library)  

---

## 1. Context & Architectural Mandate

Following the formal seal and cryptographic lock of Phase 9.7 (spanning sub-phases 9.7.1 through 9.7.12), the Master Design System has entered **Phase 10: Operationalization, Agent Bootstrap & Production Certification**.

The canonical mathematical specification for the Design System Selection Engine (DSSE) was locked and approved under DSSE-ADR-001 in [`MDS/AGENT/DESIGN_SYSTEM_SELECTION_ENGINE.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/AGENT/DESIGN_SYSTEM_SELECTION_ENGINE.md) and verified in [`MDS/10-Testing/test_dsse.py`](file:///d:/Work/Dev/Master%20Design%20System/MDS/10-Testing/test_dsse.py). However, to be operational in real-world workflows, CI/CD pipelines, and autonomous agent handoffs, the mathematical engine required a concrete, standalone command-line interface utility (`mds-dsse`).

This Decision Log codifies Architectural Decision Records **ADR-164 through ADR-171**, ratifying the design, boundaries, algorithms, and governance of the DSSE operational toolset.

---

## 2. Ratified Architectural Decisions (ADR-164 through ADR-171)

### ADR-164: Standalone DSSE Operational CLI Architecture & Boundary Isolation
- **Status:** APPROVED & IMPLEMENTED
- **Decision:** The DSSE toolset is implemented as a standalone package located strictly in `tools/dsse/`. It comprises modular subsystems:
  - `cli.py`: Command routing and deterministic exit code dispatch.
  - `engine.py`: Pure 5-pillar decoupled mathematical evaluation core.
  - `analyzer.py`: Requirements inference and project profile generator.
  - `explainer.py`: Human-readable engineering audit trail and explanation formatter.
  - `validator.py`: Contract and JSON Schema validator (Draft 2020-12).
  - `catalog.py`: Candidate catalog provider and provenance resolver.
  - `default_catalog.json`: Canonical candidate benchmark dataset.
  - `schemas/`: Formal JSON schema specifications.
- **Boundary Contract:** `tools/dsse/` is completely decoupled from the 94 protected core files in `02-Tokens/`, `Runtime/`, `Playground/`, and `Reference-Application/`. Zero protected core files are modified.

---

### ADR-165: Mathematical Invariant Preservation (5-Pillar Decoupled Model)
- **Status:** APPROVED & IMPLEMENTED
- **Decision:** The operational CLI enforces the 5-pillar decoupled decision model ratified in DSSE-ADR-001:
  1. *Candidate Suitability ($0.0\% \dots 100.0\%$)*: Weighted normalized fit calculated strictly across active dimensions.
  2. *Hard Constraint Eligibility Gate*: Tri-state evaluation ($\text{PASS} \mid \text{FAIL} \mid \text{UNKNOWN}$).
  3. *Decision Margin ($\Delta$)*: Mathematical score separation between rank #1 and rank #2.
  4. *Conjunctive Epistemic Confidence*: $C_{\text{epistemic}} = C_{\text{req}} \times C_{\text{eval}} \times C_{\text{evid}}$.
  5. *Rule-Based Confidence Gating & Governance*: Family C deterministic tier assignment and human review triggers.
- **Core Axiom:** Candidate Suitability $\ne$ Epistemic Confidence. The engine strictly forbids collapsing these distinct dimensions into a single composite float.
- **Calibration Invariant:** All 8 historical calibration scenarios (Cases A through H) remain verified with 100% mathematical fidelity.

---

### ADR-166: Tri-State Hard Constraints as Pure Eligibility Gates
- **Status:** APPROVED & IMPLEMENTED
- **Decision:** Hard constraints are evaluated as discrete tri-state gates:
  - $\text{FAIL} \implies \mathbf{DISQUALIFIED}$: The candidate's selection score is forced immediately to $0.0\%$, and it is excluded from winning.
  - $\text{UNKNOWN} \implies \mathbf{MANDATORY\ HUMAN\ REVIEW}$: Candidate cannot be automatically cleared or recommended. Mandates human architect review.
  - $\text{PASS} \implies \mathbf{ELIGIBLE}$: Candidate proceeds to ranking based on its normalized selection score.
- **Rationale:** Hard constraints represent non-negotiable architectural boundaries (e.g. native compilation, accessibility compliance, Arabic RTL). They cannot be compensated by high scores on secondary dimensions.

---

### ADR-167: Deterministic 5-Step Tie-Break Cascade Protocol
- **Status:** APPROVED & IMPLEMENTED
- **Decision:** When top candidates fall within the Tie-Break Zone ($1.0\% < \Delta \le 3.0\%$), the engine executes this strict deterministic sequence:
  1. *Step 1 (Critical Dimensions Lead):* Compare scores restricted strictly to dimensions where $w(d) = 1.00$.
  2. *Step 2 (Primary Platform Fit):* Compare score on Dimension 1 (`Platform Fit`).
  3. *Step 3 (Accessibility & RTL Combined):* Compare unweighted sum of Dimension 3 (`Accessibility`) and Dimension 4 (`Localization & RTL`).
  4. *Step 4 (Developer Ecosystem Maturity):* Compare score on Dimension 12 (`Developer Ecosystem`).
  5. *Step 5 (Human Escalation):* If candidates remain within $\le 1.0\%$ after the cascade, trigger Mandatory Human Review.
- **Rationale:** Guarantees fully reproducible, deterministic tie-breaking without heuristic randomness or hidden biases.

---

### ADR-168: Rule-Based Epistemic Confidence Gating & Governance Triggers
- **Status:** APPROVED & IMPLEMENTED
- **Decision:** Epistemic confidence is classified into discrete tiers using Family C rule-based gating:
  - **`HIGH`:** $C_{\text{req}} \ge 0.85 \land C_{\text{eval}} = 1.00 \land C_{\text{evid}} \ge 0.75 \land \text{No Critical Information Gaps}$.
  - **`MEDIUM`:** $C_{\text{req}} \ge 0.60 \land C_{\text{evid}} \ge 0.50 \land \text{No Critical Information Gaps}$.
  - **`LOW`:** Otherwise ($C_{\text{req}} < 0.60 \lor C_{\text{evid}} < 0.50 \lor \text{critical dimension unrated/unverified}$).
- **Mandatory Human Review Triggers:**
  1. Any hard constraint is `UNKNOWN`.
  2. Decision margin $\Delta \le 1.0\%$ (Virtual Tie).
  3. Unresolved tie-break cascade.
  4. Epistemic Confidence Tier is `LOW`.
  5. Any `Critical` dimension ($w=1.00$) lacks verified evidence.
- **Non-Bypassable:** No command-line flag is permitted to suppress mandatory human review when mathematically triggered.

---

### ADR-169: Candidate Catalog Governance, Provenance & Evidence Tiers
- **Status:** APPROVED & IMPLEMENTED
- **Decision:** All candidate design system ratings in `default_catalog.json` must be grounded in explicit evidence:
  - Standard Discrete Evidence Taxonomy:
    - `CODE_AUDITED` ($1.00$): Backed by verified repository code, tokens, or automated tests.
    - `OFFICIAL_DOCS` ($0.75$): Backed by official vendor documentation or formal W3C specifications.
    - `COMMUNITY` ($0.50$): Backed by third-party benchmarks or ecosystem consensus.
    - `INFERRED` ($0.25$): AI agent inference or architectural extrapolation.
    - `UNKNOWN` ($0.00$): Missing or unverified data.
  - Every dimension rating in the catalog requires `score`, `evidenceTier`, `provenance`, and `notes`. Ungrounded score injection is rejected by schema validation.

---

### ADR-170: Pure Python 3.12 Standard-Library Portability Mandate
- **Status:** APPROVED & IMPLEMENTED
- **Decision:** The `tools/dsse/` package and CLI entrypoint are implemented exclusively using the Python 3.12+ standard library:
  - Standard modules: `argparse`, `dataclasses`, `json`, `pathlib`, `re`, `sys`, `hashlib`, `typing`, `unittest`.
  - Zero external dependencies: Zero `pip` packages, zero `npm` packages.
  - Cross-platform portability: Uses `pathlib.Path` uniformly, with UTF-8 console stream reconfigurers to prevent Windows charmap exceptions.

---

### ADR-171: Deterministic Exit-Code Contract & CI Pipeline Automation Semantics
- **Status:** APPROVED & IMPLEMENTED
- **Decision:** The CLI adheres to an unambiguous 5-tier exit code contract:
  - `Exit 0`: Complete & Decisive — Automated recommendation accepted, zero human review needed (or validation passed).
  - `Exit 1`: Complete with Human Review Required — Evaluation succeeded mathematically, but mandates human architect intervention per trigger matrix.
  - `Exit 2`: Contract Validation Error — Schema mismatch, invalid dimension identifier, out-of-range score, or illegal evidence tier.
  - `Exit 3`: Input / File Error — File not found, unparseable JSON syntax, or missing required CLI arguments.
  - `Exit 4`: Internal Engine Error — Unexpected I/O or runtime exception.
- **CI Parity:** Exit 1 is distinct from exit codes 2, 3, and 4. In automated continuous integration pipelines, Exit 1 halts automated promotion to request architect sign-off without treating the run as an engine crash.
