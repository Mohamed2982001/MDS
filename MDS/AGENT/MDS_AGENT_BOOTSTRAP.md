<!-- Classification: CURRENT_SPECIFICATION -->
# Master Design System (MDS) — Agent Bootstrap & Handoff Contract

**Document Reference:** `MDS-BOOTSTRAP-1.0.0`  
**Version:** `1.0.0`  
**Phase:** 10.2 (MDS Agent Bootstrap & Handoff Contract)  
**Layer:** Layer 13 (Implementation, Tooling & Operationalization)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Status:** **RATIFIED OPERATIONAL CONTRACT**  
**Execution Context:** Microsoft Windows, Python 3.12.8 (Pure Standard Library)  

---

## 1. Scope, Mission & Architectural Context

### 1.1 Mission Statement
The **MDS Agent Bootstrap & Handoff Contract** (`MDS/AGENT/MDS_AGENT_BOOTSTRAP.md`) is the canonical, machine-readable onboarding contract that any downstream AI coding agent reads upon entering a repository. It translates the vast, multi-layered corpus of the Master Design System into deterministic operational rules, token resolution cascades, component contracts, accessibility invariants, state machines, and multi-agent handoff protocols.

### 1.2 Consumer-Facing Handoff Mandate
This document is strictly a **consumer-facing handoff contract**. It does not invent new design laws, redefine DSSE mathematical formulas, or supersede existing locked specifications. Instead, it serves as the operational gateway through which downstream AI agents consume and implement the ratified MDS estate across real-world web, mobile, and desktop applications.

```mermaid
graph TD
    MDS["MDS Master Architecture (Locked Core)"] --> BOOTSTRAP["MDS_AGENT_BOOTSTRAP.md (Phase 10.2 Contract)"]
    DSSE["DSSE Operational CLI (tools/dsse/)"] --> BOOTSTRAP
    
    BOOTSTRAP --> AGENT_A["AI Coding Agent A (Initiator)"]
    AGENT_A --> CONFIG["project_design_config.json (Project Decision)"]
    AGENT_A --> CODE["Downstream Application Implementation"]
    
    CONFIG --> AGENT_B["AI Coding Agent B (Successor)"]
    CODE --> AGENT_B
    AGENT_B --> VALIDATION["Local Conformance & Validation Engine"]
```

---

## 2. Five-Layer Authority Architecture

To prevent authority collapse where downstream agents conflate global standards with local choices, the architecture enforces a strict five-tier authority model:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ Layer A: MDS System Authority (Locked Global Core — Inviolable)        │
│   ├── Tokens, Foundations, Primitives, Components, Patterns, Workflows│
│   └── Accessibility Laws, Responsive Laws, RTL Laws, Governance FSM    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Layer B: DSSE Selection Authority (tools/dsse/ — Mathematical Core)    │
│   ├── 5-Pillar Decoupled Selection Model, Tri-State Hard Constraints   │
│   └── Decision Margin Δ, Epistemic Confidence, Tie-Break Cascade       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Layer C: Project Design Decision (project_design_config.json)          │
│   ├── Selected Design DNA, Active Personality, Theme, Density, Platform│
│   └── Formally Ratified Project Deviations (DEV-PROJ-xxx)              │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Layer D: Agent Implementation Contract (MDS_AGENT_BOOTSTRAP.md)        │
│   ├── Token Resolution Cascade, Component Reuse Rules, State Models    │
│   └── Agent Permission Tiers (SAFE, REVIEW REQUIRED, GOVERNANCE)       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Layer E: Validation Authority (Local Project & Central Orchestrator)   │
│   ├── DTCG Token Parsers, axe-core Accessibility Linter, Viewport Test │
│   └── Protected Core Immutability Verifier, Schema Validators          │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Canonical Authority Boundary Law
> **"DSSE owns selection and decision semantics. The Bootstrap Contract consumes the DSSE Decision Tuple and Exit Code. The Bootstrap Contract does not redefine DSSE."**

The Bootstrap Contract (Layer D) is strictly an operational consumer of the DSSE mathematical engine (Layer B). DSSE solely determines candidate scoring, margin classification, tie-break cascade resolution, Family C epistemic confidence tiering, and exit codes. The Bootstrap Contract does not recalculate scores or re-evaluate margins; its authority begins upon consuming the canonical DSSE decision tuple and exit code, governing the project configuration lock policy and downstream implementation authorization.

### 2.2 Hierarchy of Precedence & Conflict Resolution
When an agent encounters conflicting constraints during code generation, it must apply the following deterministic precedence cascade:
$$\mathbf{Layer\ A} \succ \mathbf{Approved\ Layer\ C\ Deviations} \succ \mathbf{Layer\ D\ Component\ Contracts} \succ \mathbf{Layer\ C\ Defaults} \succ \mathbf{Agent\ Heuristics}$$

*Rule of Precedence:* No project decision (Layer C) or agent heuristic (Layer D) may weaken or violate a Layer A Accessibility Law or System Invariant without an explicit, approved Deviation Record signed by the Lead Architect.

---

## 3. Project Startup Protocol & Downstream Lifecycle

When an AI coding agent enters a new or existing repository, it must strictly execute the following 12-step deterministic lifecycle:

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Lead Architect
    participant Agent as AI Coding Agent
    participant Boot as MDS_AGENT_BOOTSTRAP.md
    participant DSSE as DSSE CLI (tools/dsse/)
    participant Config as project_design_config.json
    participant Repo as Application Codebase
    participant Val as Validation Engine

    Agent->>Boot: 1. Ingest Bootstrap Contract
    Agent->>Repo: 2. Inspect Workspace (Tech stack, platform, requirements)
    Agent->>DSSE: 3. Run 'mds-dsse analyze' on PRD/prompts
    DSSE-->>Agent: Returns ProjectProfile JSON
    Agent->>DSSE: 4. Run 'mds-dsse evaluate' against Candidate Catalog
    alt DSSE Returns Exit Code 0 (Automated Decisive Clearance)
        DSSE-->>Agent: Exit 0 (Decisive Lead or Resolved Cascade; No Review Triggers)
        Agent->>Config: 5a. Automatically lock config (locked_by: "DSSE-AUTOMATED-CLEARANCE")
    else DSSE Returns Exit Code 1 (Human Review Mandatory)
        DSSE-->>Agent: Exit 1 (Virtual Tie / Low Conf / Unresolved Cascade / Unknown HC)
        Agent->>Dev: 5b. HALT: Present Decision Tuple & request Architect approval
        Dev-->>Agent: 5c. Ratifies candidate selection & signs governance lock
        Agent->>Config: 5d. Write approved lock (locked_by: "Lead Architect Mohamed Khalid")
    else DSSE Returns Exit Code 2 / 3 / 4 (Error / Tooling Abort)
        DSSE-->>Agent: Exit 2 / 3 / 4 (Tooling / Input / Fatal Error)
        Agent->>Dev: 5e. ABORT: Report error telemetry, zero implementation authorized
    end
    Agent->>Config: 6. Establish Project Design Configuration
    Agent->>Boot: 7. Query Token, Component & Pattern Subsets
    Agent->>Repo: 8. Synthesize UI Code & Styles
    Agent->>Val: 9. Execute Conformance Validation
    Val-->>Agent: Returns Verification Status
    Agent->>Repo: 10. Record .mds/agent_state.json & DESIGN_DECISIONS.md
    Agent->>Dev: 11. Present Verification Report & PR
    Agent->>Agent: 12. Enter Idle State (Ready for Next Task)
```

### 3.1 Prohibited Shortcuts (Zero Tolerance)
1. **Bypassing DSSE:** An agent must never select a design system or CSS library without executing DSSE analysis.
2. **Implementing Before Locking Config:** Synthesizing UI components before `project_design_config.json` is formally locked and verified is strictly forbidden.
3. **Silent Deviation:** Modifying a component contract or hardcoding a raw style without a formal deviation entry triggers immediate validation rejection.

---

## 4. Canonical DSSE Consumption & Project Configuration Lock Policy

### 4.1 Strict Authority Demarcation
- **DSSE Engine / CLI Responsibility:** Evaluates candidates across the 5 pillars, calculates suitability scores, determines margin $\Delta$, executes the 5-step tie-break cascade, classifies Family C epistemic confidence ($C_{\text{epistemic}} = C_{\text{req}} \times C_{\text{eval}} \times C_{\text{evid}}$ into `HIGH`, `MEDIUM`, or `LOW`), evaluates tri-state hard constraints, detects review triggers, and outputs the canonical Decision Tuple and Exit Code (`0`, `1`, `2`, `3`, `4`).
- **Bootstrap Contract Responsibility:** Ingests the canonical DSSE output and enforces the project configuration lock policy. The Bootstrap Contract **does NOT calculate** $C_{\text{req}}$, $C_{\text{eval}}$, $C_{\text{evid}}$, or $C_{\text{epistemic}}$; it strictly consumes `confidence_tier`, `human_review_required`, `human_review_reasons`, `margin_classification`, the Decision Tuple, and the Exit Code.

### 4.2 Canonical Family C Epistemic Confidence Model
The confidence tier is evaluated via canonical Family C:
$$C_{\text{epistemic}} = C_{\text{req}} \times C_{\text{eval}} \times C_{\text{evid}}$$

Where:
- **`HIGH`:** No critical gaps AND $C_{\text{req}} \ge 0.85$ AND $C_{\text{eval}} = 1.00$ AND $C_{\text{evid}} \ge 0.75$.
- **`MEDIUM`:** No critical gaps AND $C_{\text{req}} \ge 0.60$ AND $C_{\text{eval}} \ge 0.85$ AND $C_{\text{evid}} \ge 0.50$.
- **`LOW`:** Failure of MEDIUM conditions OR presence of critical information deficits/gaps ($w=1.00$ unrated or lacking verified evidence).

*Authority Boundary Rule:* Bootstrap must **NOT** calculate individual confidence factors and must never reconstruct arbitrary scalar thresholds; it strictly consumes DSSE's canonical outputs.

### 4.3 Eight Canonical Architecture Validation Cases (Cases A through H)

> **Axiom on Calibration Scenarios:**  
> **Case A is strictly an illustrative decisive-clear-lead calibration case, not a universal definition of Exit 0 eligibility.** Case E demonstrates that an Epistemic Confidence Tier of `MEDIUM` produces Exit 0 when DSSE evaluates that no active review triggers exist. The sole universal criterion for Exit 0 eligibility is that canonical DSSE finishes evaluation, determines `human_review_required: false`, and emits Exit Code 0.

| Case | Scenario & Input Conditions | DSSE Margin Classification | DSSE Confidence Tier | DSSE Human Review Trigger Status | DSSE Exit Code | Bootstrap Lock Policy & Action |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **Case A** | **Decisive Clear Lead (Calibration Case):** $\Delta > 3.0\%$, Epistemic Confidence = `HIGH` (via Family C), Hard Constraints = `PASS`. | `Decisive Lead` | `HIGH` | `None (Clear)` | **Exit 0** | **Automated Lock Authorized:** Agent may set `locked: true`, compute `config_hash`, and record `locked_by: "DSSE-AUTOMATED-CLEARANCE"`. Code synthesis proceeds. |
| **Case B** | **Virtual Tie:** Decision margin $\Delta \le 1.0\%$ between top candidates. | `Virtual Tie` | Any | `Virtual Tie (Δ <= 1.0%)` | **Exit 1** | **Mandatory Human Review Gate:** Agent CANNOT lock config (`locked: false`). Agent halts, presents trade-offs, and awaits Lead Architect sign-off. |
| **Case C** | **Tie-Break Zone Resolved:** $1.0\% < \Delta \le 3.0\%$, resolved by deterministic cascade Steps 1–4; no other review triggers. | `Tie-Break Zone` | `HIGH` or `MEDIUM` | `None (Resolved by Cascade)` | **Exit 0** | **Automated Lock Authorized:** Bootstrap consumes resolved result. Agent may set `locked: true` (`"DSSE-AUTOMATED-CLEARANCE"`). No artificial human review. |
| **Case D** | **Tie-Break Zone Unresolved:** $1.0\% < \Delta \le 3.0\%$, reaching Step 5 (Human Escalation) without separation. | `Tie-Break Zone` | Any | `Unresolved Tie-Break Cascade` | **Exit 1** | **Mandatory Human Review Gate:** Agent CANNOT lock config (`locked: false`). Agent halts and awaits Lead Architect sign-off. |
| **Case E** | **Medium Confidence Clearance:** Epistemic Confidence = `MEDIUM` (satisfying canonical Family C MEDIUM conditions: no critical gaps, $C_{\text{req}} \ge 0.60, C_{\text{eval}} \ge 0.85$, and $C_{\text{evid}} \ge 0.50$) with NO unverified critical gaps or review triggers (e.g. Case D AI Workspace). | `Decisive Lead` | `MEDIUM` | `None (Clear)` | **Exit 0** | **Automated Lock Authorized:** `MEDIUM` confidence alone is NOT a review trigger. Bootstrap consumes Exit 0; agent may lock config automatically. |
| **Case F** | **Low Confidence Trigger:** Epistemic Confidence = `LOW` (classified by DSSE when Family C conditions are not met, or when a critical dimension $w=1.00$ lacks verified evidence). | Any | `LOW` | `Confidence Tier LOW / Information Deficit` | **Exit 1** | **Mandatory Human Review Gate:** Agent CANNOT lock config (`locked: false`). Agent halts, highlights information gaps, and awaits Architect sign-off. |
| **Case G** | **Hard Constraint Ambiguity:** Any candidate hard constraint verification state is `UNKNOWN`. | Any | Any | `Hard Constraint UNKNOWN` | **Exit 1** | **Mandatory Human Review Gate:** Agent CANNOT lock config (`locked: false`). Agent halts, flags unverified constraint, and awaits Architect sign-off. |
| **Case H** | **Tooling / Pipeline Errors:** CLI invalid arguments (`Exit 2`), missing input files (`Exit 3`), or fatal system error (`Exit 4`). | `N/A (CLI Tooling Outcome)` | `N/A` | `CLI Tooling / Pipeline Failure` | **Exit 2 / 3 / 4** | **Execution Aborted:** Zero implementation authorization. Configuration cannot be locked; agent reports error telemetry and halts. (Execution outcome, not a DSSE selection state). |

### 4.4 Lock Policy Mechanics

1. **Autonomous Lock on Exit 0:**
   - Upon receiving DSSE Exit Code 0, the project configuration is formally eligible for automated locking.
   - The agent sets `locked: true`, `locked_by: "DSSE-AUTOMATED-CLEARANCE"`, records the current ISO-8601 UTC timestamp in `lock_timestamp`, and computes the bit-exact SHA-256 canonical hash of the configuration payload into `config_hash`.
   - Governed implementation may proceed without artificial human pauses.
2. **Enforced Gate on Exit 1:**
   - Upon receiving DSSE Exit Code 1, the agent **MUST NOT** set `locked: true`.
   - `project_design_config.json` remains in draft state (`locked: false`).
   - The agent emits a structured decision summary presenting:
     - Winning candidate vs runner-up scores and active dimensions.
     - Decision margin $\Delta$ and classification.
     - Exact human review trigger reason(s) emitted by DSSE.
     - Candidate trade-offs and suggested next steps.
   - Governed code implementation is strictly blocked. Any attempt to generate UI code prior to human sign-off triggers immediate validation failure.
3. **Exit 2 / 3 / 4 Abort Behavior:**
   - Exit 2 (Validation Error), Exit 3 (Input Error), Exit 4 (Fatal System Error) indicate CLI tooling or system failure.
   - The configuration cannot be locked, and zero implementation authorization is granted.
4. **Human Review Approval State & Artifact:**
   When Lead Architect Mohamed Khalid reviews and approves the decision, the `governance_lock` is updated:
   ```json
   "governance_lock": {
     "locked": true,
     "locked_by": "Lead Architect Mohamed Khalid",
     "lock_timestamp": "2026-10-01T20:30:00Z",
     "review_resolution": "RATIFIED_CANDIDATE_MDS_FOR_FLUTTER_ECOSYSTEM",
     "config_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
   }
   ```
5. **Tamper Detection & Verification Invariants:**
   Downstream linters and the local validation engine strictly verify `governance_lock` prior to analyzing generated UI code:
   - `locked === false`: **UNLOCKED_DRAFT** $\implies$ Agent halts; code generation prohibited.
   - `locked === true` but `config_hash` does not match the canonical JSON hash of the configuration: **TAMPERED_CONFIG** $\implies$ Immediate Validation Failure (`Exit 2: CONTRACT_VIOLATION`).
   - DSSE output indicates an Exit 1 state (e.g. `human_review_required: true`) but `locked_by === "DSSE-AUTOMATED-CLEARANCE"`: **ILLEGAL_AUTO_LOCK_VIOLATION** $\implies$ Immediate Validation Failure (`Exit 2: CONTRACT_VIOLATION`).
   - `locked_by` is not `"DSSE-AUTOMATED-CLEARANCE"` or `"Lead Architect Mohamed Khalid"`: **UNAUTHORIZED_SIGNER_VIOLATION** $\implies$ Immediate Validation Failure (`Exit 2: CONTRACT_VIOLATION`).

---

## 5. Project Design Configuration Contract (`project_design_config.json`)

The single source of truth for a downstream project's design identity is `project_design_config.json`, validated against `schemas/project_design_config.schema.json` (Draft 2020-12).

### 5.1 Multi-Source Ownership & Immutability Matrix

| Configuration Property / Category | SOURCE | OWNER | MUTABILITY | APPROVAL_REQUIRED | Validation Invariant & Scope |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`schema_version`** | Layer A (MDS System Authority) | MDS Core Architecture | **IMMUTABLE** | Global MDS Governance RFC | Must match `"1.0.0"`. Project cannot redefine schema version. |
| **`project_name`** | Layer C (Project Context) | Project Developer | **CONFIGURABLE** | None (Informational) | Free-form string identifying project. |
| **`selected_design_system`** | Layer B (DSSE Selection) | DSSE Mathematical Engine | **IMMUTABLE** (Post-Evaluation) | Automated (Exit 0) / Architect (Exit 1) | Must equal winning candidate from `dsse_decision`. Cannot be arbitrarily edited. |
| **`dsse_decision.candidate_id`** | Layer B (DSSE Selection) | DSSE Mathematical Engine | **IMMUTABLE** | Automated (Exit 0) / Architect (Exit 1) | Evaluated identifier matching default or ratified catalog. |
| **`dsse_decision.selection_score`** | Layer B (DSSE Selection) | DSSE Mathematical Engine | **IMMUTABLE** | None (Mathematical Output) | Normalized suitability score ($0.0 \dots 100.0\%$). |
| **`dsse_decision.confidence_tier`** | Layer B (DSSE Selection) | DSSE Mathematical Engine | **IMMUTABLE** | None (Mathematical Output) | `HIGH`, `MEDIUM`, or `LOW` assigned via Family C rules. |
| **`dsse_decision.decision_margin_delta`** | Layer B (DSSE Selection) | DSSE Mathematical Engine | **IMMUTABLE** | None (Mathematical Output) | Score difference $\Delta$ between rank #1 and #2. |
| **`dsse_decision.margin_classification`** | Layer B (DSSE Selection) | DSSE Mathematical Engine | **IMMUTABLE** | None (Mathematical Output) | `"Decisive Lead"`, `"Tie-Break Zone"`, or `"Virtual Tie"`. |
| **`dsse_decision.human_review_required`** | Layer B (DSSE Selection) | DSSE Mathematical Engine | **IMMUTABLE** | None (Mathematical Output) | Boolean flag emitted directly by canonical DSSE engine. |
| **`dsse_decision.human_review_reasons`** | Layer B (DSSE Selection) | DSSE Mathematical Engine | **IMMUTABLE** | None (Mathematical Output) | Array of trigger justifications generated by DSSE. |
| **`dsse_decision.reproducibility_digest`** | Layer B (DSSE Selection) | DSSE Mathematical Engine | **IMMUTABLE** | None (Mathematical Output) | Bit-exact SHA-256 canonical hash of DSSE execution. |
| **`visual_personality`** | Layer C (Project Design Decision) | Project Lead / Developer | **CONFIGURABLE** | Architect Review on Change | Selected preset (`calm_editorial`, `expressive_brand`, etc.). |
| **`theme_mode`** | Layer C (Project Design Decision) | Project Lead / Developer | **CONFIGURABLE** | Autonomous within Presets | Active theme (`light`, `dark`, `system_adaptive`). |
| **`density_mode`** | Layer C (Project Design Decision) | Project Lead / Developer | **CONFIGURABLE** | Autonomous within Presets | Active spatial scale (`compact`, `regular`, `spacious`). |
| **`platform_targets`** | Layer C (Project Design Decision) | Project Lead / Developer | **CONFIGURABLE** | Architect Review if Hard Constraints Affected | Target stacks (`web`, `flutter_mobile`, `nextjs`). |
| **`directionality`** | Layer C (Project Design Decision) | Project Lead / Developer | **CONFIGURABLE** | Autonomous within Requirements | `ltr_only`, `rtl_only`, or `bidirectional_adaptive`. |
| **`accessibility_profile.target_level`** | Layer A / Layer C | MDS Authority / Project Lead | **RESTRICTED** | Architect Review if below AA | Minimum target level (`WCAG_2.1_AA` default). |
| **`accessibility_profile.min_touch_target_px`** | Layer A (MDS System Authority) | MDS Core Architecture | **IMMUTABLE** | Global MDS Governance RFC | Inviolable MDS law: **44px**. Cannot be lowered. |
| **`accessibility_profile.enforce_focus_rings`** | Layer A (MDS System Authority) | MDS Core Architecture | **IMMUTABLE** | Global MDS Governance RFC | Must be `true`. Focus ring enforcement cannot be disabled. |
| **`accessibility_profile.support_reduced_motion`** | Layer A (MDS System Authority) | MDS Core Architecture | **IMMUTABLE** | Global MDS Governance RFC | Must be `true`. Reduced motion handling cannot be disabled. |
| **`approved_deviations`** | Layer C / Human Authority | Lead Architect Mohamed Khalid | **APPEND-ONLY** | **MANDATORY EXPLICIT HUMAN SIGNATURE** | Array of formal Deviation Records (`DEV-PROJ-xxx`). |
| **`governance_lock.locked`** | Layer C / Human Authority | Governance Enforcement Engine | **BOOLEAN LOCK** | Automated (Exit 0) / Architect (Exit 1) | If `false`, downstream code synthesis is prohibited. |
| **`governance_lock.locked_by`** | Layer B / Human Authority | Locking Authority Entity | **IMMUTABLE** (Once Locked) | Must be `"DSSE-AUTOMATED-CLEARANCE"` or `"Lead Architect Mohamed Khalid"` | Identifies the authentic locking entity. |
| **`governance_lock.lock_timestamp`** | System Telemetry | Clock Provider | **IMMUTABLE** (Once Locked) | Automatic ISO-8601 Stamp | Exact timestamp when lock was ratified. |
| **`governance_lock.review_resolution`** | Human Authority | Lead Architect Mohamed Khalid | **REQUIRED ON EXIT 1** | Mandatory if Exit 1 was triggered | Explains human architectural rationale for Exit 1 resolution. |
| **`governance_lock.config_hash`** | Cryptographic Telemetry | Canonical Stream Hasher | **IMMUTABLE** (Once Locked) | Bit-exact Hash Match | SHA-256 digest of config content. Tampering forces Exit 2. |

### 5.2 Inviolable Non-Alternative Truth Law
`project_design_config.json` is strictly a **downstream project realization contract**.
1. It **MUST NOT** and **CANNOT** become an alternative source of truth for canonical MDS specifications (`MDS_MASTER_SPECIFICATION.md`).
2. It **MUST NOT** redefine DSSE candidate rating matrices or mathematical formulas.
3. It **MUST NOT** declare alternative token definitions or rename DTCG token paths.
4. It **MUST NOT** redefine component APIs or alter canonical component contracts.

---

## 6. Design DNA Model & Philosophy

The Master Design System embodies the core philosophical principle:
> **"Intentional + Refined + Adaptive"**  
> *Calm by default, expressive when needed.*

### 6.1 Three-Tier Cognitive-Perceptual Hierarchy

```text
┌────────────────────────────────────────────────────────────────────────┐
│ 01 في العقل (In the Mind) — Architectural Rigor & Invariants           │
│   ├── Token inheritance, mathematical scales, component contracts      │
│   ├── WCAG AA contrast, 44x44 touch targets, focus rings               │
│   └── 11-State universal interaction FSM, RTL logical properties       │
│   ==> 100% NON-NEGOTIABLE & UNIVERSAL ACROSS ALL PROJECTS              │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 02 في العين (In the Eye) — Harmonious Visual Presentation              │
│   ├── Curated HSL theme palettes, typography scale (Default: Cairo)    │
│   ├── Elevation shadows, border radii, spatial layout density          │
│   └── Smooth state transitions, responsive recomposition               │
│   ==> ADAPTIVE PER PROJECT PROFILE (Configured via Personality)        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 03 في الشخصية وقت الحاجة (In Personality When Needed) — Contextual Brand│
│   ├── Strategic micro-animations, expressive empty/success states      │
│   ├── Branded gradients, celebratory feedback, rich data graphics      │
│   └── Delightful moments of interactive polish                         │
│   ==> STRATEGIC & PURPOSEFUL (Never cluttering daily functional UI)    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Token Usage Contract & Zero-Tolerance Laws

### 7.1 Four-Step Token Search Cascade
For any visual property (color, font-size, line-height, spacing, border-radius, shadow, duration), the downstream agent must resolve tokens strictly in this order:

$$\mathbf{Step\ 1:\ Component\ Token} \longrightarrow \mathbf{Step\ 2:\ Semantic\ Token} \longrightarrow \mathbf{Step\ 3:\ Primitive\ Token} \longrightarrow \mathbf{Step\ 4:\ Propose\ Token\ RFC}$$

1. **Component Token (Highest Specificity):** E.g., `--mds-comp-button-bg-primary`, `mds.comp.button.padding.x`.
2. **Semantic Token (System Meaning):** E.g., `--mds-color-surface-brand`, `--mds-space-inset-md`, `--mds-radius-control`.
3. **Primitive Token (Raw Scale):** E.g., `--mds-primitive-color-blue-600`, `--mds-primitive-space-16`.
4. **Propose Token RFC (Missing Scale):** If no token covers the semantic requirement, the agent must document a formal proposal in `docs/DESIGN_DECISIONS.md` before introducing any new CSS variable.

### 7.2 Zero-Tolerance Styling Laws
- 🚫 **No Magic Values:** Hardcoded numbers (`padding: 13px;`, `color: #1a73e8;`, `border-radius: 7px;`) are strictly prohibited in application stylesheets.
- 🚫 **No Page-Level Mutation:** Agents must not redefine `--mds-*` tokens locally within a specific page or component block to change colors for one screen.
- 🚫 **No Raw Color Application:** Primitive color tokens (`--mds-primitive-color-*`) must never be applied directly to UI elements; they must be wrapped in semantic tokens.

---

## 8. Component Implementation Contract (19 Canonical Components)

```text
┌────────────────────────────────────────────────────────────────────────┐
│ 19 CANONICAL MDS COMPONENTS (MANDATORY REUSE)                          │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ 1. Button         │ 8. Radio          │ 15. Card                       │
│ 2. IconButton     │ 9. Switch         │ 16. Table                      │
│ 3. Link           │ 10. Select        │ 17. Tabs                       │
│ 4. Field          │ 11. Alert         │ 18. Dialog                     │
│ 5. Input          │ 12. Spinner       │ 19. Tooltip                    │
│ 6. Textarea       │ 13. Skeleton      │                                │
│ 7. Checkbox       │ 14. Badge         │                                │
└───────────────────┴───────────────────┴────────────────────────────────┘
```

### 8.1 Reuse & Composition Rules
1. **Mandatory Reuse:** When a standard control is needed (e.g. form inputs, modals, alerts), the agent must instantiate the canonical component. Re-implementing a bespoke button or input with raw divs is a critical violation.
2. **Composed Patterns:** Canonical components should be composed together (e.g., `Field` + `Input` + `Tooltip` + `Badge`).
3. **Deferred Enterprise Components:** Specialized enterprise components (`Data Grid`, `Tree View`, `Date Picker`, `Rich Text Editor`, `Command Palette`) are formally designated as deferred enterprise specifications. When required, the agent must build them adhering to MDS tokens, keyboard navigation, and the 11-state interaction FSM.

---

## 9. Pattern, Workflow, and Template Consumption

Downstream agents must prioritize established structural assets over ad-hoc page creation:

$$\mathbf{Templates\ (6)} \succ \mathbf{Workflows\ (6)} \succ \mathbf{Patterns\ (8)} \succ \mathbf{Custom\ Composition}$$

### 9.1 Asset Inventory Roster
* **6 Canonical Templates:**
  1. `Dashboard Overview`: Multi-card analytical summary with filter bar and activity stream.
  2. `Entity Data Table`: Paginated, sortable tabular view with batch actions and search.
  3. `Document / Detail View`: Two-column layout with header metadata and contextual sidebar.
  4. `Settings Layout`: Tabbed configuration page with section cards and sticky save bar.
  5. `Form Submission Page`: Linear structured multi-field form with sticky footer.
  6. `Authentication Screen`: Centered, distraction-free card layout supporting multi-step auth.
* **6 Canonical Workflows:**
  1. `Auth & Onboarding`: Sign-in, sign-up, password recovery, session renewal.
  2. `Multi-Step Wizard`: Linear stepped processes with state persistence and validation guards.
  3. `CRUD Entity Management`: Create, view, update, and soft-delete operations.
  4. `Async Task Processing`: Long-running jobs with progress feedback, polling, and toasts.
  5. `Account Settings`: Profile, security, notification, and organization management.
  6. `Bulk Operations`: Multi-select, batch status change, and destructive confirmation.
* **8 Canonical Patterns:**
  1. `Empty State`, 2. `Confirmation Dialog`, 3. `Filter Bar`, 4. `Form Layout`, 5. `Stat Card`, 6. `Action Toolbar`, 7. `Search with Autocomplete`, 8. `Details Header`.

---

## 10. Accessibility Invariants & Touch Target Decoupling

Accessibility is a system property verified on every generated screen:

1. **Semantic HTML First:** Always utilize `<button>`, `<input>`, `<dialog>`, `<table>`, `<nav>`, `<main>`, `<aside>`. Never use `<div onclick="...">`.
2. **Keyboard Navigation:** Full support for `Tab`, `Shift+Tab`, `Enter`, `Space`, `Escape`, and `Arrow` keys.
3. **Visible Focus Rings:** All focusable elements must display a high-contrast focus ring (minimum 3:1 contrast ratio against both component background and adjacent canvas).
4. **44x44 Touch Target Rule:**
   > **Architectural Boundary:** The 44x44 CSS px touch target is an **internal MDS design rule** enforced across all interactive components to ensure ergonomic mobile and touch usability. It is strictly an MDS system invariant and must **never** be cited as an authoritative claim of WCAG compliance.
5. **Color Independence:** Error and status messages must never rely on color alone; always pair color with text or iconography.
6. **Motion Sensitivity:** Respect `prefers-reduced-motion: reduce` by replacing spatial animations with subtle opacity fades.

---

## 11. Responsive Architecture Law ("Recomposition, Not Shrinking")

Downstream agents must never implement responsive layouts by simply scaling down desktop elements or squeezing multi-column layouts until they break.

### 11.1 The Recomposition Cognitive Chain
$$\mathbf{Available\ Space} \longrightarrow \mathbf{User\ Task} \longrightarrow \mathbf{Essential\ Information} \longrightarrow \mathbf{Compress/Move/Hide} \longrightarrow \mathbf{Recompose}$$

### 11.2 Breakpoint & Container Standards
- **Breakpoints:**
  - `320px`: Mobile Small (Single column, full-width touch targets, collapsed navigation).
  - `768px`: Tablet (Two-column layout, adaptive sidebars, expanded toolbars).
  - `1024px`: Desktop / Laptop (Full navigation drawer, multi-column data views).
  - `1440px`: Desktop Wide (High-density dashboard, multi-pane split views).
- **Container Max-Widths:**
  - Standard Content: `1152px` (Centered, optimized reading measure).
  - Wide Content / Dashboards: `1440px`.

---

## 12. RTL & Bi-Directionality Contract

RTL is a first-class architectural citizen across all MDS implementations:

1. **Mandatory Logical CSS Properties:**
   - Use `margin-inline-start`, `margin-inline-end`, `padding-inline-start`, `padding-inline-end`.
   - Use `inset-inline-start`, `inset-inline-end` instead of `left` / `right`.
   - Use `text-align: start` instead of `text-align: left`.
2. **Mirroring Taxonomy:**
   - *Mirrored:* Navigation chevrons, back/forward buttons, breadcrumb separators, progress indicators.
   - *Unmirrored:* Media playback controls (play, pause, seek), clocks, telephone numbers, technical codes, brand logos.
3. **Arabic-First Typography:**
   - When Arabic is targeted, the global default font is **`Cairo`** (Google Fonts).
   - Layouts must budget for **20% to 30% text length expansion** compared to English.
   - 🚫 **No Ellipsis Truncation:** Never truncate descriptive, informational, or functional text with `text-overflow: ellipsis`. Allow text to wrap cleanly (`soft-wrap: true`).

---

## 13. State & Interaction Models

### 13.1 Universal 11-State Interaction FSM
Every complex view, form, or interactive widget must map cleanly to the 11-state MDS Finite State Machine:

```text
[IDLE] ───► [ACTIVE_INPUT] ───► [VALIDATING] ───► [CONFIRMING]
                                                       │
  ┌────────────────────────────────────────────────────┘
  ▼
[PROCESSING] ───► [STREAMING] ───► [REVIEWING] ───► [SUCCESS_RESOLVED]
      │
      ├───────► [ERROR_INTERCEPTED] ───► (Retry)
      │
      ├───────► [FATAL_FAILURE] ───────► (Terminal Recovery)
      │
      └───────► [ABORTED_CANCEL] ──────► [IDLE]
```

### 13.2 Eight Experience-State Families
Agents must handle all 8 foundational state families:
1. `Data States`: Empty, Partial, Populated, Overflown.
2. `Access States`: Unauthorized, Forbidden, Session Expired.
3. `Resource States`: Not Found, Deleted, Rate Limited.
4. `Process States`: Loading, Submitting, Stepping, Queued.
5. `Recovery States`: Offline, Reconnecting, Syncing.
6. `Conflict States`: Version Mismatch, Concurrent Edit.
7. `Unsaved Changes`: Dirty Form, Discard Confirmation.
8. `Fatal Failure`: Network Severed, System Crash.

---

## 14. AI UX Contract & Human-in-the-Loop Protocol

AI experiences within MDS follow strict cognitive and safety guidelines:

1. **Seven AI States:** `Idle`, `Thinking`, `Working`, `Streaming`, `Completed`, `Needs Review`, `Error`.
2. **Human-in-the-Loop Law:**
   > When an AI model generates content requiring verification (e.g. data synthesis, code generation, critical operations), the UI must transition to **`Needs Review`**. The generated output **cannot** silently mutate the production database without an explicit, verifiable human confirmation action (`Confirm / Accept / Reject`).
3. **Canonical AI Composite Patterns:**
   - `AI-Input-Prompt`: Context-aware prompt bar with token budget indicator.
   - `AI-Result-Review`: Side-by-side or inline diff comparison showing model confidence.
   - `AI-Synthesis-Review`: Aggregated multi-source review card with citation badges.
   - `AI-Workspace`: Integrated split-pane canvas for continuous human-AI co-creation.

---

## 15. Validation Architecture & Local Conformance Engine

Downstream agents must validate their code locally before declaring tasks complete:

```mermaid
graph LR
    CODE["Generated Code"] --> V1["DTCG Token Check"]
    CODE --> V2["HTML & Component Contract Check"]
    CODE --> V3["axe-core Accessibility Audit"]
    CODE --> V4["RTL Logical Property Scanner"]
    CODE --> V5["Viewport Recomposition Test"]
    
    V1 & V2 & V3 & V4 & V5 --> VERDICT{"All Invariants Satisfied?"}
    VERDICT -- Yes --> REPORT["Generate Conformance Report (PASS)"]
    VERDICT -- No --> REMEDIATION["Agent Auto-Remediation Loop"]
```

### 15.1 Conformance Checklist
- [ ] Zero magic numbers in CSS.
- [ ] 100% semantic HTML elements.
- [ ] Minimum 4.5:1 text contrast / 3:1 UI contrast.
- [ ] Visible focus ring on every interactive control.
- [ ] Logical CSS properties for all directional spacing.
- [ ] Cairo font applied for Arabic layouts.
- [ ] 11-state FSM adhered to for complex forms.

---

## 16. Project Deviation Schema & Validation Suppression

When a real-world project has an authentic need to deviate from an MDS rule, the agent must document it using the formal **Deviation Record Schema**:

```json
{
  "deviation_id": "DEV-PROJ-001",
  "affected_mds_rule": "MDS-RULE-TOK-004",
  "reason_and_rationale": "High-density flight management radar requires 24px micro-buttons.",
  "project_context": "RadarView/AirTrafficControlGrid",
  "evidence_and_benchmarks": "EUROCONTROL Human Factors Standard HFS-2024",
  "impact_assessment": "Restricted exclusively to RadarView; standard views retain 44x44 targets.",
  "approval_status": "APPROVED",
  "approved_by": "Lead Architect Mohamed Khalid",
  "timestamp": "2026-10-01T20:00:00Z",
  "lifecycle": "permanent",
  "validation_suppression": {
    "rule_code": "TOUCH_TARGET_44",
    "target_selector": ".radar-grid-cell__button",
    "scope_file": "src/views/RadarView.vue"
  }
}
```

*Triaging Rule:*
- **Bug:** Unintended implementation error $\implies$ Fix it immediately.
- **Project Deviation:** Legitimate, domain-specific exception $\implies$ Submit formal Deviation Record for Architect approval.
- **MDS System RFC:** Fundamental improvement to MDS itself $\implies$ Escalate to Core MDS Architecture repository.

---

## 17. Tri-Level Agent Permission Model

```text
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 1: SAFE (Autonomous Agent Execution Permitted)                    │
│   ├── Ingesting existing tokens and CSS variables                      │
│   ├── Instantiating and composing 19 canonical components              │
│   ├── Implementing approved patterns, workflows, and templates         │
│   ├── Writing unit tests, component tests, and local stories           │
│   └── Running validation suites and generating reports                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 2: REVIEW REQUIRED (Human Architect Sign-Off Required)            │
│   ├── Proposing a new semantic or component token                      │
│   ├── Introducing a new custom component (not in 19 canonical list)    │
│   ├── Submitting a Project Deviation Record (DEV-PROJ-xxx)             │
│   ├── Altering project_design_config.json parameters                   │
│   └── Resolving a DSSE Human Review Gate (Exit 1)                      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 3: SYSTEM GOVERNANCE (Strictly Prohibited for Downstream Agents)  │
│   ├── Modifying canonical MDS specifications in MDS/                   │
│   ├── Modifying Protected Core files (02-Tokens/, Runtime/, etc.)      │
│   ├── Altering DSSE mathematical algorithms or candidate baselines     │
│   └── Bypassing or disabling validation safety gates                   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 18. Stateless Multi-Agent Handoff & Continuity Contract

To guarantee that "Agent B" can seamlessly resume work initiated by "Agent A" without access to conversational chat history, three synchronized disk artifacts must be maintained:

1. **`project_design_config.json`**: Captures active design system, theme, density, platform, and approved deviations.
2. **`docs/DESIGN_DECISIONS.md`**: Human-readable append-only log explaining *why* decisions were made.
3. **`.mds/agent_state.json`**: Machine-readable operational ledger containing:
   - `last_active_agent_id`
   - `last_updated_timestamp`
   - `implemented_components_manifest`
   - `active_validation_status`
   - `pending_review_gates`

*Handoff Protocol:* Agent B executes `cat .mds/agent_state.json` $\to$ verifies `project_design_config.json` $\to$ runs local validation $\to$ proceeds with implementation in perfect context.

---

## 19. AI-Readability & Machine-Enforceable Guardrails

| Ambiguous Prose (Banned) | Machine-Enforceable Rule (Mandatory) |
| :--- | :--- |
| *"Make the buttons look modern and clean."* | `button { height: var(--mds-comp-button-h-md); border-radius: var(--mds-radius-control); background: var(--mds-color-interactive-primary); }` |
| *"Ensure the page is accessible."* | `Run axe-core with zero CRITICAL/SERIOUS violations; visible focus ring >= 3:1; touch target >= 44x44px.` |
| *"Adapt the layout for mobile screens."* | `At viewport < 768px: recompose grid to single column; stack action toolbars; ensure font-size >= 16px to prevent iOS auto-zoom.` |
| *"Support Arabic if needed."* | `Use logical CSS properties; set font-family: Cairo; direction: rtl; allocate +25% horizontal container expansion.` |

---

## 20. Five-Tier Source Provenance & Security Trust Hierarchy

1. **Tier 1 (Root Authority):** Canonical MDS specifications (`MDS/` locked specs, `MDS_AGENT_BOOTSTRAP.md`, `ACTIVE_PHASE.json`).
2. **Tier 2 (Governed Derived Artifacts):** Formal JSON schemas, compiled token DTCG dictionaries, and verified test suites.
3. **Tier 3 (Project Design Contract):** `project_design_config.json` signed by Lead Architect.
4. **Tier 4 (Generated Telemetry & Reports):** Orchestrator test output, axe-core audit reports, DSSE evaluation output.
5. **Tier 5 (Agent Interpretation & Chat Prompts):** Lowest authority; cannot contradict or weaken Tiers 1-3.

---

## 21. Versioning & Upstream Compatibility Model

All bootstrap artifacts enforce Semantic Versioning (`MAJOR.MINOR.PATCH`):
- `bootstrap_contract_version`: `1.0.0`
- `mds_system_version`: `1.0.0`
- `dsse_engine_version`: `1.0.0`
- `project_design_config_schema`: `1.0.0`

### 21.1 Migration & Upstream Compatibility
If `project_design_config.json` was generated against an older MDS release (e.g. `0.9.x` vs `1.0.0`), the agent must execute a non-destructive schema migration pass, preserving all approved deviations while updating token reference pointers.

---

## 22. Failure & Recovery Behavior

When an agent encounters unresolvable conflicts or validation failures, it must adhere to deterministic recovery pathways:
1. **Validation Failure (Exit 1):** The agent enters auto-remediation mode, parsing the finding diagnostic code (e.g. `COLOR_CONTRAST_DEFICIT`), adjusting the semantic token pointer to a higher-contrast token, and re-running validation.
2. **Missing Token:** The agent checks semantic fallbacks; if none exist, it logs an RFC proposal in `docs/DESIGN_DECISIONS.md` and pauses for human review.
3. **Ambiguous Requirements:** When requirements lack platform or density targets, the agent must fall back to the safe baseline: `Web`, `Regular Density`, `System-Adaptive Theme`, and `Level AA Accessibility`.

---

## 23. Artifact Lifecycle & Status Transitions

Every design artifact produced within a downstream project transitions through five deterministic states:

$$\mathbf{DRAFT} \longrightarrow \mathbf{IN\_REVIEW} \longrightarrow \mathbf{APPROVED} \longrightarrow \mathbf{LOCKED} \longrightarrow \mathbf{DEPRECATED}$$

- **DRAFT:** Work in progress by AI Coding Agent.
- **IN_REVIEW:** Waiting for Lead Architect sign-off (Exit 1 gate).
- **APPROVED:** Ratified by Architect.
- **LOCKED:** Cryptographically hashed and committed to version control.
- **DEPRECATED:** Replaced by a superseded revision.

---

## 24. Canonical Phase 10 Roadmap Realignment

1. **Phase 10.1: DSSE Operational CLI (`mds-dsse`)** — *LOCKED & APPROVED*  
   Autonomous mathematical selection engine, CLI commands (`analyze`, `evaluate`, `explain`, `validate`), exit codes 0–4 verified.
2. **Phase 10.2: MDS Agent Bootstrap & Handoff Contract (`MDS_AGENT_BOOTSTRAP.md`)** — *CURRENT (IN_PROGRESS)*  
   Canonical onboarding contract, five-layer authority model, project design configuration schema, and multi-agent handoff ledger.
3. **Phase 10.3: Production Artifact Compilation & Zero-NPM Distribution** — *UPCOMING DIRECT DEPENDENT*  
   Automated compilation, bundling, minification, tree-shaking, and standalone packaging of production runtime CSS/JS assets, design tokens, and components for zero-NPM standalone deployment and CDN distribution.
4. **Phase 10.4: MDS v1.0.0 Production Certification** — *FINAL GATE*  
   Systemic end-to-end production readiness audit, performance benchmarks, and formal v1.0.0 release certification.

---

## 25. Contract Sign-Off

The **MDS Agent Bootstrap & Handoff Contract** is ratified, immutable, and authoritative for all downstream coding agents.

**Mohamed Khalid**, Lead Architect (Senior Full Stack & Flutter Developer)
