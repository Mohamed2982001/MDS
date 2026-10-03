# MDS Workflows — Architectural Decision Log (WDR)

This document records the authoritative architectural decisions governing **Layer 06: Workflows** within the Master Design System (MDS).

---

## Decision Index

| ID | Title | Status | Date |
| :--- | :--- | :--- | :--- |
| **WDR-001** | Strict Separation Between Layer 05 (Patterns) and Layer 06 (Workflows) | `APPROVED` | Phase 7 |
| **WDR-002** | Adoption of the Mandatory 27-Point Workflow Anatomy Standard | `APPROVED` | Phase 7 |
| **WDR-003** | Platform-Agnostic Finite State Machine (FSM) Execution Model | `APPROVED` | Phase 7 |
| **WDR-004** | Invariant Scope Protection: Zero New Tokens, Components, or Patterns | `APPROVED` | Phase 7 |
| **WDR-005** | Continued Formal Deferral of 9 Enterprise Complex Systems | `APPROVED` | Phase 7 |
| **WDR-006** | Strict Demarcation of the Security Triad: Confirmation vs AuthN vs AuthZ | `APPROVED` | Phase 7 |
| **WDR-007** | Recovery-First Resilience and Non-Destructive State Preservation | `APPROVED` | Phase 7 |
| **WDR-008** | AI Streaming Cadence, Latency Feedback, and Citation Verification Standard | `APPROVED` | Phase 7 |
| **WDR-009** | Calibrated Verification Taxonomy and Accessibility Evidence Discipline | `APPROVED` | Phase 7 |
| **WDR-010** | Strict Token Cascading and Zero-Hex Styling Law in Workflow Showcases | `APPROVED` | Phase 7 |

---

### WDR-001: Strict Separation Between Layer 05 (Patterns) and Layer 06 (Workflows)

- **Status:** `APPROVED`
- **Context:** Design systems frequently blur the distinction between compound components, recurring design patterns, and end-to-end task workflows, leading to monolithic components with embedded business rules and brittle lifecycle bindings.
- **Decision:** Formally decouple Layer 05 (Patterns) from Layer 06 (Workflows). A **Pattern** is a spatial/structural composition answering *"How should this recurring UI problem be structured locally?"* (e.g., `Form-Section`, `Empty-State`, `Confirmation-Dialog`). A **Workflow** is a behavioral/temporal journey answering *"How does the user progress through a task from intent to outcome?"* (e.g., `Form-Submission`, `Destructive-Action`). Workflows orchestrate Patterns, Components, and Primitives over time without introducing new UI elements.
- **Consequences:** Clear architectural boundaries; zero component bloat in the workflow layer; high testability of state progressions independent of visual styling.

---

### WDR-002: Adoption of the Mandatory 27-Point Workflow Anatomy Standard

- **Status:** `APPROVED`
- **Context:** Workflow specifications without standardized documentation frameworks suffer from omitted edge cases (e.g., forgotten cancellation flows, unhandled network disconnects, missing accessibility focus contracts, or lack of RTL layout guidance).
- **Decision:** Mandate that all canonical MDS workflows adhere strictly to the **27-Point Workflow Anatomy Standard**:
  1. Workflow Name, 2. Purpose & Summary, 3. User Intent, 4. Trigger, 5. Preconditions, 6. Actors & Roles, 7. Entry State, 8. Sequential Steps, 9. Branches & Forks, 10. Decision Points, 11. Patterns Used, 12. Components Used, 13. Experience States, 14. Success Outcome, 15. Failure Outcomes, 16. Recovery Paths, 17. Cancellation & Exit, 18. Data & State Requirements, 19. Accessibility Contracts, 20. Responsive Behavior, 21. RTL Behavior, 22. Density Modes, 23. Motion & Transitions, 24. AI Guardrails & Cadence, 25. Validation Criteria, 26. Anti-Patterns & Misuse, 27. Governance & Lifecycle.
- **Consequences:** Eliminates architectural blind spots; ensures thorough evaluation of accessibility, responsiveness, recovery, and security for every documented journey.

---

### WDR-003: Platform-Agnostic Finite State Machine (FSM) Execution Model

- **Status:** `APPROVED`
- **Context:** Describing workflows purely through UI mockups or static diagrams leads to unhandled runtime transitions, race conditions, duplicate submissions, and inconsistent error recovery across web, mobile, and desktop.
- **Decision:** Model every workflow as a platform-agnostic Finite State Machine (FSM) with explicit states (`IDLE`, `ACTIVE`, `VALIDATING`, `PROCESSING`, `SUCCESS`, `ERROR`, `ABORTED`), deterministic transition events, guard conditions, and strict focus/payload contracts.
- **Consequences:** Engineering teams implementing MDS across Flutter, React, Next.js, or native platforms can bind state machines directly to their local state managers (`flutter_bloc`, XState, Redux) without ambiguity.

---

### WDR-004: Invariant Scope Protection: Zero New Tokens, Components, or Patterns

- **Status:** `APPROVED`
- **Context:** System layers often leak new styles, ad-hoc tokens, or specialized one-off components when orchestrating complex user journeys.
- **Decision:** Enforce absolute invariant scope for Phase 7:
  - New Foundations: **0**
  - New Primitives: **0**
  - New Core Components: **0** (19 Core Components maintained)
  - New Canonical Patterns: **0** (8 Core Patterns maintained)
  - New Design Tokens: **0** (188 total tokens, 47 component tokens strictly preserved)
- **Consequences:** Guarantees that Layer 06 remains a pure orchestration layer and preserves the approved token repository without regression or drift.

---

### WDR-005: Continued Formal Deferral of 9 Enterprise Complex Systems

- **Status:** `APPROVED`
- **Context:** Workflows often interface with advanced enterprise data manipulation (e.g., bulk editing in grids, rich text authoring, complex scheduling).
- **Decision:** Reaffirm the strict deferral of the 9 complex enterprise systems:
  1. `DataGrid`
  2. `RichTextEditor`
  3. `Calendar`
  4. `DateRangePicker`
  5. `CommandSystem`
  6. `Tree`
  7. `Combobox`
  8. `VirtualizedList`
  9. `FileUploadManager`
  Workflows in Phase 7 must utilize standard input controls, lists, and basic cards without assuming the presence of these deferred systems.
- **Consequences:** Prevents unapproved architectural scope inflation prior to dedicated enterprise design validation passes.

---

### WDR-006: Strict Demarcation of the Security Triad: Confirmation vs. AuthN vs. AuthZ

- **Status:** `APPROVED`
- **Context:** Destructive action and settings workflows frequently confuse user intention confirmation with identity verification and authorization checks, creating security vulnerabilities or flawed UX assumptions.
- **Decision:** Explicitly codify the separation of the Security Triad:
  - **User Confirmation:** A client-side UX mechanism designed to verify explicit human intent and prevent accidental triggers (e.g., typing a resource name into an input, clicking a high-friction modal confirmation).
  - **Authentication (AuthN):** The cryptographic verification of user identity (e.g., password, WebAuthn, MFA, biometric token), governed strictly by identity providers.
  - **Authorization (AuthZ):** The server-side policy evaluation verifying whether the authenticated user possesses privileges to mutate the entity (e.g., RBAC, ABAC), evaluated strictly by the backend.
  MDS Workflows design and specify User Confirmation and error feedback from AuthN/AuthZ rejections, but NEVER implement auth logic or store credentials.
- **Consequences:** Clean separation of concerns; zero architectural or legal exposure regarding security protocol implementation in the design system.

---

### WDR-007: Recovery-First Resilience and Non-Destructive State Preservation

- **Status:** `APPROVED`
- **Context:** Poorly architected workflows discard user input when a network error occurs, or trap users in unrecoverable dead-end error screens.
- **Decision:** Mandate a "Recovery-First" law across all MDS Workflows:
  1. User input must be preserved in client-side state during failures, validation errors, and modal dismissals.
  2. Every error state must provide an actionable, contextual remediation pathway (e.g., `Retry`, `Edit Details`, `Save Draft`, or `Discard Changes`).
  3. No error screen may ever terminate without an explicit escape hatch returning the user to the last safe resting state.
- **Consequences:** Superior user trust and resilience; zero unforced user data loss during intermittent network or validation failures.

---

### WDR-008: AI Streaming Cadence, Latency Feedback, and Citation Verification Standard

- **Status:** `APPROVED`
- **Context:** AI generation introduces non-deterministic latency, hallucinations, partial streaming, and trust deficits. Standard form workflows fail when applied directly to generative AI workflows.
- **Decision:** Establish dedicated UX contracts for AI workflows:
  1. **Latency Feedback:** Differentiate between "Prompt Received", "Reasoning / Processing", and "Streaming Output".
  2. **Human-in-the-Loop:** All AI synthesis workflows must conclude with an explicit human review step (`Accept`, `Edit`, `Regenerate`, `Reject`) before persisting changes to the core system state.
  3. **Traceability:** Outputs containing synthesized assertions must present inspectable source references or citations.
- **Consequences:** Predictable, transparent AI interactions that elevate user control and prevent automated persistence of unverified model outputs.

---

### WDR-009: Calibrated Verification Taxonomy and Accessibility Evidence Discipline

- **Status:** `APPROVED`
- **Context:** Overstating automated test coverage as "full UX verification" or claiming absolute universal WCAG compliance leads to compliance risk and architectural dishonesty.
- **Decision:** Enforce calibrated terminology across all Layer 06 specifications and verification artifacts:
  - Automated test runs verifying token linkage and CSS syntax are strictly designated as **Automated Token/Style Integrity Check**.
  - Interactive flows validated in the testbed are designated as **Manually Verified**.
  - Accessibility statements must state: *"Implemented accessibility behaviors were validated against selected WCAG success criteria where applicable. Comprehensive cross-platform assistive technology testing remains deferred to Phase 8."*
  - Touch target documentation must state: *"Interactive controls preserve the MDS minimum interaction target where applicable."*
  - Viewport & RTL claims must state: *"The current sandbox was checked at the defined MDS responsive modes and showed no observed horizontal overflow for the included Workflow examples."* and *"RTL structural and logical-property checks passed in the current sandbox. Broader language/content localization testing remains outside this closure pass."*
- **Consequences:** Precise, truthful, and defensible architectural documentation.

---

### WDR-010: Strict Token Cascading and Zero-Hex Styling Law in Workflow Showcases

- **Status:** `APPROVED`
- **Context:** Showcase prototypes frequently introduce hardcoded hex colors, arbitrary padding, and ad-hoc CSS overrides that break design token governance.
- **Decision:** All CSS supporting Layer 06 showcases must strictly reference existing MDS tokens via CSS custom properties (`var(--mds-...)`).
  - Raw hex codes (`#xxxxxx`) are strictly forbidden.
  - Hardcoded non-token pixel dimensions for spacing, typography, and elevations are strictly forbidden.
  - RTL styling must strictly utilize CSS Logical Properties (`margin-inline`, `padding-inline`, `inset-inline-start`, etc.) without `row-reverse` or physical directional hacks.
- **Consequences:** 100% token fidelity; theme-switchable showcases (Light/Dark); flawless RTL support by design.
