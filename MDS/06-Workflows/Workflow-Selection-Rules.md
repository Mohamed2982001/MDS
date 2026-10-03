# MDS Workflows — Selection Engine & Decision Rules

## 1. Executive Summary

This document formalizes the **Workflow Selection Engine (WSE)**, an 8-stage algorithmic methodology for choosing, scoping, and orchestrating the appropriate workflow archetype for any human-system task in the Master Design System (MDS). It also catalogs critical **Workflow Anti-Patterns** that must be actively avoided.

---

## 2. The 8-Stage Workflow Selection Engine (WSE)

When designing or implementing a user journey in MDS, engineers and designers must progress sequentially through the 8 stages of the WSE:

```text
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1: Identify Primary User Intent & Goal               │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 2: Assess Task Complexity & Step Sequence            │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 3: Classify Consequence & Reversibility Risk         │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 4: Evaluate Latency & Execution Dynamics             │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 5: Select Canonical Workflow Archetype               │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 6: Resolve Pattern Compositions (Layer 05)           │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 7: Bind Core Components & Primitives (Layers 04 & 03)│
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 8: Verify Accessibility, Recovery & Security Contracts│
└─────────────────────────────────────────────────────────────┘
```

---

### Detailed Stage Breakdown:

#### Stage 1: Identify Primary User Intent & Goal
- **Question:** What is the fundamental outcome the user intends to achieve?
- **Classifications:**
  - `CREATE / CAPTURE`: Entering structured information into the system.
  - `DISCOVER / LOCATE`: Searching, filtering, and identifying specific entities.
  - `MUTATE / CONFIGURE`: Altering operational parameters, preferences, or profile settings.
  - `DESTROY / TERMINATE`: Irrevocably deleting, archiving, or revoking entities.
  - `SYNTHESIZE / GENERATE`: Requesting AI generation, reasoning, or content transformation.
  - `RECOVER / REPAIR`: Remediating a system, network, or validation breakdown.

#### Stage 2: Assess Task Complexity & Step Sequence
- **Question:** Does the journey require a single interactive view, a sequential wizard, or branching paths?
  - *Single View:* Inline edits or single-form submissions.
  - *Sequential Flow:* Multi-step progression with dependency gates.
  - *Branching Journey:* Conditional forks based on user choices or runtime permissions.

#### Stage 3: Classify Consequence & Reversibility Risk
- **Question:** What are the operational consequences of this action?
  - *Low Risk / Reversible:* Filter changes, draft saving, view toggling.
  - *Medium Risk / Recoverable:* Profile edits, configuration updates with version rollback.
  - *High Risk / Irreversible:* Permanent deletion, financial transfers, security credential revocation. (Requires mandatory `Confirmation-Dialog` gate).

#### Stage 4: Evaluate Latency & Execution Dynamics
- **Question:** How does the system process the request?
  - *Immediate (<100ms):* Local client filtering or synchronous validation.
  - *Standard Async (100ms – 2s):* Standard network API dispatch (button spinner feedback).
  - *Extended Async (>2s):* Progress bar, polling, or asynchronous background job.
  - *Streaming / AI:* Real-time token streaming with cancel affordances.

#### Stage 5: Select Canonical Workflow Archetype
Map the findings from Stages 1–4 to one of the 6 canonical MDS workflows:
- **`Form-Submission`**: Creation, data capture, or transactional record updates.
- **`Search-Discovery`**: Locating entities via query inputs and multifaceted filters.
- **`Destructive-Action`**: High-consequence deletions or revocations.
- **`Settings-Update`**: Configuration changes with autosave or explicit batch commit.
- **`AI-Synthesis-Review`**: Generative AI tasks requiring prompt input and output inspection.
- **`Error-Recovery`**: Intercepting and resolving system or network failures.

#### Stage 6: Resolve Pattern Compositions (Layer 05)
Identify the exact Layer 05 patterns required:
- E.g., `Form-Section` for input grouping; `Confirmation-Dialog` for destruction; `Empty-State` for zero search results; `AI-Result-Review` for generated output.

#### Stage 7: Bind Core Components & Primitives (Layers 04 & 03)
Bind the approved 19 Core Components (`Button`, `Input`, `Badge`, `Dialog`) and Layout Primitives (`Stack`, `Container`, `Grid`).

#### Stage 8: Verify Accessibility, Recovery & Security Contracts
Audit the workflow against focus restoration, ARIA live announcements, touch targets, non-destructive state preservation, and security triad separation.

---

## 3. Workflow Selection Matrix

| Intent Category | Risk Level | Execution Latency | Canonical Workflow | Key Patterns Used |
| :--- | :--- | :--- | :--- | :--- |
| Create Record | Low / Medium | 200ms – 1s | **Form-Submission** | `Form-Section`, `Page-Header` |
| Find Entity | Low | < 300ms | **Search-Discovery** | `Search-Filter-Bar`, `Empty-State` |
| Delete Resource | High | 500ms – 2s | **Destructive-Action** | `Confirmation-Dialog`, `Data-List-Card` |
| Change Config | Low / Medium | Instant / Batch | **Settings-Update** | `Form-Section`, `Data-List-Card` |
| Generate Content | Medium | 1s – 10s (Streaming) | **AI-Synthesis-Review** | `AI-Input-Prompt`, `AI-Result-Review` |
| Fix Failure | Variable | Network dependent | **Error-Recovery** | `Empty-State`, `Confirmation-Dialog` |

---

## 4. Critical Workflow Anti-Patterns

```text
┌─────────────────────────────────────────────────────────────┐
│                 WORKFLOW ANTI-PATTERNS                      │
├──────────────────────────┬──────────────────────────────────┤
│ ❌ The Amnesiac Error    │ ❌ The Premature Submitter       │
│ ❌ The Dead-End Despair  │ ❌ The Trapped User              │
│ ❌ The Invisible Stream  │ ❌ The False Authorization       │
│ ❌ The Phantom Action    │ ❌ The Infinite Spinner          │
└──────────────────────────┴──────────────────────────────────┘
```

### 1. The Amnesiac Error
- **Description:** Wiping user form data upon a network error or server validation rejection.
- **Correction:** In-progress form state must always remain preserved in client memory so the user can easily rectify errors without retyping.

### 2. The Premature Submitter
- **Description:** Submitting payloads to the server without client-side schema validation, resulting in unnecessary network trips and delayed error feedback.
- **Correction:** Validate required constraints, regex masks, and value boundaries client-side in the `VALIDATING` state before dispatching.

### 3. The Dead-End Despair
- **Description:** Showing an error banner or screen with no interactive buttons or actionable recovery paths.
- **Correction:** Every error state must provide clear recovery options: `Retry`, `Check Connection`, `Edit Details`, or `Go Back`.

### 4. The Trapped User
- **Description:** Modal dialogs or multi-step wizards that remove escape hatches, disable closing on `Escape` key, or provide no `Cancel` button.
- **Correction:** Always provide accessible exit affordances and prompt for confirmation only if unsaved changes exist (`isDirty`).

### 5. The Invisible Stream
- **Description:** Generating AI outputs without streaming cadence, typing indicators, or a `Stop Generating` control.
- **Correction:** Utilize dedicated AI Experience States with real-time text expansion and an immediate abort button.

### 6. The False Authorization
- **Description:** Treating a client-side confirmation dialog as an authorization mechanism.
- **Correction:** A confirmation dialog only verifies human intent. Real security authorization (`AuthZ`) must always be evaluated server-side.

### 7. The Phantom Action
- **Description:** Applying optimistic UI updates without maintaining rollback capabilities if the server rejects the action.
- **Correction:** When using optimistic updates, cache the previous state and provide automatic rollback with an actionable toast alert on failure.

### 8. The Infinite Spinner
- **Description:** Locking a button or view into a loading spinner indefinitely when a request times out or silently drops.
- **Correction:** Enforce strict client-side timeout thresholds (e.g., 15s) that automatically transition the state machine to `ERROR_INTERCEPTED`.
