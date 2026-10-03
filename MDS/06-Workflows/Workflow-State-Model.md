# MDS Workflows — Finite State Machine (FSM) Model

## 1. Architectural Philosophy

In the Master Design System (MDS), a Workflow is formalized as a **Deterministic Finite State Machine (FSM)**. Workflows are never defined as loose sequences of UI screens or ad-hoc event handlers; instead, they are platform-agnostic behavioral engines with explicit states, deterministic transitions, rigorous guards, and standardized state preservation rules.

This model enables seamless implementation across diverse engineering stacks—whether using `flutter_bloc` / Cubits in Flutter, XState or Redux in Next.js/React, or native mobile architecture—without semantic divergence.

---

## 2. Universal Workflow State Topology

All MDS Workflows operate within a canonical state topology:

```text
                           ┌──────────────────┐
                           │       IDLE       │
                           └────────┬─────────┘
                                    │ TRIGGER / START
                                    ▼
                           ┌──────────────────┐
                     ┌────►│  ACTIVE_INPUT    │◄─────────────────┐
                     │     └────────┬─────────┘                  │
                     │              │ SUBMIT / PROCEED           │
                     │              ▼                            │
                     │     ┌──────────────────┐                  │
(Validation Failure) │     │    VALIDATING    │                  │
                     └─────┤                  ├──────┐           │
                           └────────┬─────────┘      │           │
                                    │ (Valid)        │ (Require  │
                                    ▼                │  Confirm) │
                           ┌──────────────────┐      │           │
                           │    PROCESSING    │◄─────┘           │
                           │  (or STREAMING)  │                  │
                           └────────┬─────────┘                  │
                                    │                            │
                 ┌──────────────────┴──────────────────┐         │
                 ▼                                     ▼         │
        ┌──────────────────┐                  ┌──────────────────┴┐
        │ SUCCESS_RESOLVED │                  │ ERROR_INTERCEPTED │
        └────────┬─────────┘                  └────────┬──────────┘
                 │                                     │
                 ▼                                     ▼
        ┌──────────────────┐                  ┌──────────────────┐
        │  TERMINAL_EXIT   │                  │  ABORTED_CANCEL  │
        └──────────────────┘                  └──────────────────┘
```

---

## 3. Canonical State Definitions

| State Name | Classification | Description | UI Manifestation | Focus Anchor |
| :--- | :--- | :--- | :--- | :--- |
| `IDLE` | Resting | Initial quiescent state before user initiates action. | Resting button, search bar, or entry card. | Natural tab order |
| `ACTIVE_INPUT` | Interactive | User is actively inputting data, selecting options, or searching. | Editable inputs, active filters, draft state. | Current active field |
| `VALIDATING` | Synchronous / Transient | Synchronous or client-side check verifying data integrity. | Inline validation spinners or indicators. | First invalid control |
| `CONFIRMING` | Modal / High-Friction | User is presented with consequences of a critical/destructive action. | `Confirmation-Dialog` overlay. | Primary dialog action |
| `PROCESSING` | Asynchronous | Network dispatch, backend persistence, or long-running computation. | Button spinner, loading overlay, progress bar. | Aria-busy container |
| `STREAMING` | Progressive | Progressive delivery of AI tokens or chunked data payloads. | Streaming cursor, real-time text expansion. | Live region container |
| `REVIEWING` | Interactive | User inspects generated output or aggregated batch results. | `AI-Result-Review` pattern, summary panel. | Review container header |
| `SUCCESS_RESOLVED` | Positive Terminal | Task successfully accomplished. Permanent state mutation confirmed. | Toast alert, success banner, checkmark badge. | Success message / Exit CTA |
| `ERROR_INTERCEPTED` | Recoverable Negative | Operational, network, or server validation failure occurred. | Alert banner, inline field errors, retry button. | Error banner / Retry CTA |
| `FATAL_FAILURE` | Critical Negative | Unrecoverable error (e.g., session expired, entity deleted by peer). | Critical Empty-State or modal roadblock. | Primary recovery action |
| `ABORTED_CANCEL` | Neutral Terminal | User intentionally dismissed or cancelled workflow; clean rollback. | Returned to `IDLE` or previous resting view. | Invoking trigger button |

---

## 4. State Transition Matrix & Event Signatures

| Source State | Event Trigger | Guard Conditions | Target State | Action / Side-Effect |
| :--- | :--- | :--- | :--- | :--- |
| `IDLE` | `WORKFLOW_START` | User has interaction permission | `ACTIVE_INPUT` | Mount workflow context; focus first field |
| `ACTIVE_INPUT` | `FIELD_MUTATE` | Input conforms to character bounds | `ACTIVE_INPUT` | Update client buffer; clear previous field error |
| `ACTIVE_INPUT` | `REQUEST_SUBMIT` | Form is dirty; fields populated | `VALIDATING` | Run client-side schema validation |
| `VALIDATING` | `VALIDATION_PASS` | All required constraints satisfied | `PROCESSING` (or `CONFIRMING`) | Dispatch payload or open confirmation modal |
| `VALIDATING` | `VALIDATION_FAIL` | One or more constraints violated | `ACTIVE_INPUT` | Highlight invalid fields; announce first error |
| `CONFIRMING` | `CONFIRM_COMMIT` | Confirmation challenge satisfied | `PROCESSING` | Lock dialog; dispatch destructive payload |
| `CONFIRMING` | `CONFIRM_CANCEL` | None | `ACTIVE_INPUT` (or `IDLE`) | Close dialog; return focus to trigger control |
| `PROCESSING` | `DISPATCH_SUCCESS` | Status == 200/201/204 | `SUCCESS_RESOLVED` | Announce success; emit completion event |
| `PROCESSING` | `DISPATCH_ERROR` | Error is transient / network / 4xx | `ERROR_INTERCEPTED` | Preserve form state; mount recovery alert |
| `PROCESSING` | `DISPATCH_FATAL` | Status == 401/403/410/500 fatal | `FATAL_FAILURE` | Lock form; present session recovery options |
| `STREAMING` | `CHUNK_ARRIVE` | Payload contains valid delta | `STREAMING` | Append delta to buffer; throttle DOM repaint |
| `STREAMING` | `STREAM_END` | Stream closure token received | `REVIEWING` | Stop stream indicator; present review actions |
| `STREAMING` | `STREAM_ABORT` | User clicked Stop Generating | `REVIEWING` | Terminate stream; present partial draft review |
| `ERROR_INTERCEPTED` | `RETRY_DISPATCH` | Network re-established / payload intact | `PROCESSING` | Re-dispatch cached payload without data loss |
| `ERROR_INTERCEPTED` | `EDIT_PAYLOAD` | None | `ACTIVE_INPUT` | Focus erroneous field; keep valid data intact |
| `ANY_ACTIVE_STATE`| `USER_CANCEL` | No irreversible side-effect underway | `ABORTED_CANCEL` | Check dirty state; prompt if unsaved; exit |

---

## 5. Guard Conditions & Invariants

All transitions must respect strict Boolean guards before firing:

1. **`canSubmit(state)`**:
   - Evaluates to `true` ONLY when all required fields contain valid values, no validation errors exist, and the form is not already in `PROCESSING`.
2. **`isSafeToCancel(state)`**:
   - If form state is clean (`!isDirty`), transition to `ABORTED_CANCEL` immediately.
   - If form state is dirty (`isDirty`), interrupt transition and prompt user with a lightweight confirmation before discarding changes.
3. **`isRecoverable(error)`**:
   - Differentiates between transient failures (network timeouts, rate limits, field validation) and fatal failures (missing permissions, corrupted entity). Transient failures route to `ERROR_INTERCEPTED`; fatal failures route to `FATAL_FAILURE`.
4. **`requiresConfirmation(action)`**:
   - If action is destructive, irreversible, or high-impact, transition MUST pass through `CONFIRMING` before reaching `PROCESSING`.

---

## 6. State Context (Memory Payload) Schema

The client-side state machine maintains a typed context payload throughout execution:

```typescript
interface MDSWorkflowContext<TPayload, TResult> {
  // Identification
  workflowId: string;
  instanceId: string;
  
  // Lifecycle
  status: 'IDLE' | 'ACTIVE_INPUT' | 'VALIDATING' | 'CONFIRMING' | 
          'PROCESSING' | 'STREAMING' | 'REVIEWING' | 'SUCCESS_RESOLVED' | 
          'ERROR_INTERCEPTED' | 'FATAL_FAILURE' | 'ABORTED_CANCEL';
  
  // Data State
  initialValues: Readonly<TPayload>;
  currentValues: TPayload;
  isDirty: boolean;
  
  // Validation State
  errors: Record<string, string>;
  touchedFields: Set<string>;
  
  // Execution & Recovery State
  retryCount: number;
  maxRetries: number;
  lastError: {
    code: string;
    message: string;
    isRecoverable: boolean;
    timestamp: number;
  } | null;
  
  // Output Result
  result: TResult | null;
  
  // Accessibility Focus Anchor
  lastFocusedElementId: string | null;
}
```

---

## 7. Mapping to Experience States (Layer 08)

MDS Workflows coordinate directly with the five canonical Experience States:

| Workflow State | MDS Experience State | Visual / Interaction Manifestation |
| :--- | :--- | :--- |
| `IDLE` | **Idle / Resting** | Standard resting surface, default inputs, interactive triggers. |
| `PROCESSING` / `STREAMING` | **Loading State** | Skeleton loaders, button spinners, streaming text, `aria-busy="true"`. |
| `ACTIVE_INPUT` (No Data) | **Empty State** | Prompts to begin search, filter bar initial empty list state. |
| `ERROR_INTERCEPTED` | **Error State** | Alert banners, inline input error borders, recovery actions. |
| `SUCCESS_RESOLVED` | **Success State** | Confirmation banner, success badge, checkmark animation. |
