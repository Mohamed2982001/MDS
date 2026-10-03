# MDS Workflows — Composition & Orchestration Rules

## 1. Executive Summary

This document establishes the **10 Inviolable Workflow Orchestration Laws** governing **Layer 06: Workflows** within the Master Design System (MDS). Any user journey, multi-step flow, or interaction progression that violates any of these laws is considered non-compliant and cannot be approved.

---

## 2. The 10 Inviolable Workflow Orchestration Laws

```text
┌────────────────────────────────────────────────────────────────────────┐
│               THE 10 INVIOLABLE WORKFLOW ORCHESTRATION LAWS            │
├─────────┬──────────────────────────────────────────────────────────────┤
│ LAW 01  │ Unidirectional Layer Resolution                              │
│ LAW 02  │ Zero Direct Visual Inventing & Token Invariance              │
│ LAW 03  │ Non-Destructive State Preservation                           │
│ LAW 04  │ Mandatory Contextual Recovery Affordance                     │
│ LAW 05  │ Deterministic Focus Progression & Restoration                │
│ LAW 06  │ Safe Cancellation & State Rollback Guarantee                 │
│ LAW 07  │ Strict Security Triad Demarcation (Confirm ≠ AuthN ≠ AuthZ)  │
│ LAW 08  │ Mandatory Human-in-the-Loop for AI Generation                │
│ LAW 09  │ Bidirectional & Responsive Flow Equivalence                  │
│ LAW 10  │ Absolute Zero-Bloat & Enterprise System Deferral             │
└─────────┴──────────────────────────────────────────────────────────────┘
```

---

### LAW 01: Unidirectional Layer Resolution
- **Rule:** Workflows must resolve downwards through canonical MDS layers:
  $$\text{Workflows (06)} \longrightarrow \text{Patterns (05)} \longrightarrow \text{Components (04)} \longrightarrow \text{Primitives (03)} \longrightarrow \text{Tokens (02)}$$
- **Mandate:** Workflows compose existing Patterns and Components. They may never reach upward into Templates (07) or bypass intermediate layers to invent private UI structures.
- **Violation:** Declaring a custom ad-hoc layout container directly in a workflow instead of using `Stack`, `Container`, or `Form-Section`.

---

### LAW 02: Zero Direct Visual Inventing & Token Invariance
- **Rule:** Workflows introduce **zero new visual tokens, zero new color literals, and zero custom CSS dimensions**.
- **Mandate:** All visual properties (padding, colors, borders, shadows, transitions) utilized across workflow states must resolve strictly to existing MDS design tokens.
- **Violation:** Using `#ef4444` or `padding: 17px` anywhere in workflow mockups, CSS, or code.

---

### LAW 03: Non-Destructive State Preservation
- **Rule:** A user's input data is sacred. A workflow must **never wipe, reset, or discard user inputs** due to an intermittent network error, server rejection, validation failure, or modal prompt dismissal.
- **Mandate:** In-progress form buffers must be preserved in client-side memory throughout error recovery cycles until the user explicitly commands a reset or reaches a successful terminal state.
- **Violation:** Clearing password/email fields or form state when an API returns `500 Internal Server Error`.

---

### LAW 04: Mandatory Contextual Recovery Affordance
- **Rule:** There are **no dead-end error states** in MDS.
- **Mandate:** Every error state displayed during a workflow must provide at least one actionable, contextual recovery path (e.g., `Retry Submission`, `Edit Details`, `Check Connection`, or `Contact Support`).
- **Violation:** Displaying a generic "An error occurred" screen with no buttons or exit affordances.

---

### LAW 05: Deterministic Focus Progression & Restoration
- **Rule:** Focus management across workflow states must follow an explicit, predictable contract.
- **Mandate:**
  1. Upon entering a workflow or opening a modal, focus moves to the first actionable control or container.
  2. Upon a validation failure, focus moves immediately to the first invalid input field, and the error is announced via `aria-describedby` or `role="alert"`.
  3. Upon dismissing or cancelling a workflow, focus must return precisely to the invoking trigger button that initiated the sequence.
- **Violation:** Leaving focus stranded on a removed DOM node or resetting focus to `document.body`.

---

### LAW 06: Safe Cancellation & State Rollback Guarantee
- **Rule:** Every workflow step must provide an unambiguous, accessible cancellation mechanism (e.g., `Cancel`, `Close`, `Back`, or `Escape` key handler).
- **Mandate:**
  - If no changes were made (`!isDirty`), cancellation immediately restores the clean resting state.
  - If unsaved changes exist (`isDirty`), the system must prompt the user to confirm discarding changes before destroying data.
- **Violation:** Closing a multi-step form on outside click without prompting when 10 fields have been populated.

---

### LAW 07: Strict Security Triad Demarcation (Confirm ≠ AuthN ≠ AuthZ)
- **Rule:** Workflows must cleanly decouple user intent confirmation from identity verification and access permissions.
- **Mandate:**
  - **User Confirmation:** Verifies conscious human consent via UI friction (e.g., confirmation dialog, typing entity name). Managed within Layer 06.
  - **Authentication (AuthN):** Handled by cryptographic identity providers (OAuth, SAML, WebAuthn). Workflows only receive success/failure tokens.
  - **Authorization (AuthZ):** Evaluated by backend policy engines. Workflows handle `403 Forbidden` states gracefully without claiming to enforce authorization client-side.
- **Violation:** Storing user passwords in client state or claiming a confirmation dialog "authorizes" an action.

---

### LAW 08: Mandatory Human-in-the-Loop for AI Generation
- **Rule:** Generative AI outputs are probabilistic and cannot be committed directly to system state without explicit human verification.
- **Mandate:**
  - All AI synthesis workflows must present a mandatory review step (`Accept`, `Edit`, `Regenerate`, `Reject`).
  - Streaming generation must display real-time cadence indicators and allow immediate cancellation.
  - Citations or source references must be inspectable before committing generated text.
- **Violation:** Automatically persisting AI-generated content to a database without user inspection and explicit sign-off.

---

### LAW 09: Bidirectional & Responsive Flow Equivalence
- **Rule:** A workflow must be functionally and structurally identical regardless of writing direction (LTR vs. RTL) or viewport size (320px mobile to 1440px desktop).
- **Mandate:**
  - Layouts must rely exclusively on CSS Logical Properties (`inline`, `block`, `start`, `end`).
  - Physical direction hacks (`row-reverse`, `float: right`, hardcoded `left`/`right`) are strictly prohibited.
  - Touch targets must preserve the MDS minimum interaction target (44×44px hit area) across mobile viewports.
- **Violation:** Hardcoding `margin-left: 16px` or altering step sequence order between Arabic and English.

---

### LAW 10: Absolute Zero-Bloat & Enterprise System Deferral
- **Rule:** Workflows must operate within the approved design system boundaries and never introduce unapproved enterprise components.
- **Mandate:**
  - The 9 complex enterprise systems (`DataGrid`, `RichTextEditor`, `Calendar`, `DateRangePicker`, `CommandSystem`, `Tree`, `Combobox`, `VirtualizedList`, `FileUploadManager`) remain strictly **DEFERRED**.
  - All Phase 7 workflows must compose using the approved 19 Core Components and 8 Core Patterns.
- **Violation:** Introducing an inline rich-text wysiwyg editor or a virtualized infinite table into a workflow specification.
