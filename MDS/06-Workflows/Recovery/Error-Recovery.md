# MDS Workflow: Error Recovery & Resilience (MDS-WF-006)

## 1. Workflow Identification & Metadata
- **Workflow Name:** `Error-Recovery`
- **ID:** `MDS-WF-006`
- **Layer:** `06-Workflows`
- **Family:** `Recovery`
- **Verification Status:** `Manually Verified` (Testbed Sandbox) / `Automated Token/Style Integrity Check`

---

## 2. Purpose & Summary
The `Error-Recovery` workflow coordinates system resilience when an asynchronous operation, data fetch, or network transaction fails. Rather than presenting static, unhelpful dead-end screens, this workflow intercepts failures, diagnoses severity, preserves all client-side draft state, provides contextual and actionable remediation mechanisms (`Retry`, `Edit Details`, `Check Connection`, `Safe Exit`), and restores normal operational equilibrium.

---

## 3. User Intent
The user intends to understand what went wrong, preserve their current work, and execute an immediate recovery action to complete their task or safely exit without penalty.

---

## 4. Trigger
- System intercepts an unhandled exception, network timeout, `4xx/5xx` HTTP error, or WebSocket disconnection during an active workflow.

---

## 5. Preconditions
1. An active workflow was executing or fetching data.
2. A failure event occurred that cannot be silently resolved via automated background retries.

---

## 6. Actors & Roles
- **Primary Actor:** End User encountering an operational roadblock.
- **System Actor:** Global Exception Interceptor, Network Circuit Breaker, State Cache Manager, and Notification Service.

---

## 7. Entry State
- **State Identifier:** `ERROR_INTERCEPTED`
- The invoking UI enters error presentation mode.
- User input fields and draft state are locked and cached in memory.
- An actionable error banner or modal overlay mounts with descriptive feedback.

---

## 8. Sequential Steps (Happy Path)

```text
[1. FAILURE DETECTED] ──► [2. STATE PRESERVED] ──► [3. CONTEXTUAL DIAGNOSIS] ──► [4. REMEDIATION ACTION] ──► [5. RESTORATION]
  HTTP 503 / Timeout       Payload Cached in        Error Banner Rendered with    User Clicks "Retry Now";      Normal State Restored;
  Intercepted              Memory Buffer            Actionable Recovery Buttons   System Re-Dispatches Cached   Data Persisted Cleanly
```

1. **Step 1 — Interception:** Network request drops or times out. Global interceptor catches failure and creates an `ErrorIncident` record.
2. **Step 2 — Non-Destructive State Cache:** System caches in-flight payload and form fields in client state memory, preventing any input wiping.
3. **Step 3 — Contextual Diagnosis Display:** State machine mounts the appropriate recovery UI based on error classification:
   - *Transient / Network:* Inline dismissible alert banner with `"Retry"` button.
   - *Data Conflict:* Form section alert highlighting conflicting fields with `"Edit Details"` button.
   - *Catastrophic / Page-Level:* `Empty-State` pattern styled for system failure with `"Reload Page"` and `"Contact Support"` CTAs.
4. **Step 4 — User Remediation Trigger:** User evaluates diagnosis and clicks primary recovery action (e.g., `"Retry Submission"`).
5. **Step 5 — Re-Dispatch & Equilibrium:** State machine transitions back to `PROCESSING`. Cached payload is re-sent. Upon success (`200 OK`), state machine transitions to `SUCCESS_RESOLVED`, dismisses error banner, and returns to normal resting view.

---

## 9. Branches & Forks

```text
                     ┌──► [Branch A: Immediate Retry Succeeds] ──► Dismiss Banner, Commit Data
                     │
[Error Intercepted] ─┼──► [Branch B: Repeated Failure (Max 3)] ──► Escalate to Offline/Support Mode
                     │
                     ├──► [Branch C: User Edits Payload] ────────► Return to Form with Fields Intact
                     │
                     └──► [Branch D: User Aborts Flow] ──────────► Safe Rollback to Last Resting State
```

- **Branch A (Successful Retry):** Network re-established; operation completes cleanly.
- **Branch B (Exhausted Retries):** User retries 3 times without success. State machine escalates from inline banner to persistent diagnostic panel offering `"Download Offline Draft"` and `"Contact Support"`.
- **Branch C (Input Correction):** User chooses `"Edit Details"`. System focuses the specific erroneous field while keeping all other valid fields filled.
- **Branch D (Safe Exit):** User decides to abandon operation. System confirms rollback, releases network locks, and navigates safely back to dashboard.

---

## 10. Decision Points
- **Retry vs. Edit:** Deciding whether the issue is transient infrastructure (Retry) or invalid user data (Edit).
- **Abandon vs. Persist:** Deciding whether to keep trying or discard changes and exit.

---

## 11. Patterns Used
- `Empty-State` (`MDS/05-Patterns/Feedback/Empty-State.md`): Used for full-page or section-level catastrophic breakdowns.
- `Confirmation-Dialog` (`MDS/05-Patterns/Feedback/Confirmation-Dialog.md`): Used when aborting an error flow with unsaved offline data.

---

## 12. Components Used
- `Button` (Retry, Edit Details, Reload, Contact Support)
- `Badge` (Error status tag, offline indicator)
- `Dialog` (Catastrophic error modal or exit confirmation)

---

## 13. Experience States
- **Loading State:** Operation actively re-trying with animated spinner; `aria-busy="true"`.
- **Error State:** High-contrast error banner or card with prominent tokenized danger accents.
- **Success State:** Successful resolution banner; checkmark icon; normal view restoration.

---

## 14. Success Outcome
- Operational failure successfully remediated.
- Zero loss of user time or typed information.
- Complete transparency regarding system status.

---

## 15. Failure Outcomes
- **Permanent Outage:** User given offline export of their form data or clear escalation path to technical support.

---

## 16. Recovery Paths
- **One-Click Retry:** Immediately re-dispatches identical payload without retyping.
- **Payload Editing:** Returns focus directly to the erroneous field for correction.
- **Draft Export:** In critical enterprise contexts, allows saving JSON draft locally.
- **Safe Rollback:** Gracefully exits without corrupting existing database records.

---

## 17. Cancellation & Exit Affordances
- Prominent `"Cancel"` or `"Dismiss"` action on all error banners.
- Clear `"Back to Safety"` CTA on full-page error screens.

---

## 18. Data & State Requirements
```typescript
interface ErrorRecoveryState {
  incidentId: string;
  errorCode: string;
  errorMessage: string;
  isRetryable: boolean;
  retryAttempt: number;
  maxRetryAttempts: number;
  cachedPayload: any;
  status: 'INTERCEPTED' | 'RETRYING' | 'RESOLVED' | 'ESCALATED' | 'ABORTED';
}
```

---

## 19. Accessibility Contracts
- **Live Announcement:** Error appearance announced immediately via `aria-live="assertive"` and `role="alert"`.
- **Focus Progression:** Focus is moved programmatically to the primary recovery action (`"Retry"` button) or the error banner container.
- **Dismissible:** Banners can be dismissed via keyboard `Escape` or accessible close button.
- **WCAG Standard:** Implemented accessibility behaviors were validated against selected WCAG success criteria where applicable. Comprehensive cross-platform assistive technology testing remains deferred to Phase 8.

---

## 20. Responsive Behavior
- **Mobile (320px – 767px):** Error banners span 100% width; buttons stack vertically with full touch hit area (minimum 44×44px). Interactive controls preserve the MDS minimum interaction target where applicable.
- **Tablet & Desktop (768px – 1440px):** Actionable buttons align inline within the banner.
- **Overflow:** The current sandbox was checked at the defined MDS responsive modes and showed no observed horizontal overflow for the included Workflow examples.

---

## 21. RTL Behavior
- Error icon aligns at `inline-start`.
- Action buttons align at `inline-end`.
- RTL structural and logical-property checks passed in the current sandbox. Broader language/content localization testing remains outside this closure pass.

---

## 22. Density Modes
- Banners maintain adequate padding (`var(--mds-space-3)`) in both default and compact modes to ensure legibility during critical errors.

---

## 23. Motion & Transitions
- Error banner slide-down: `motion.duration.fast` (150ms) with `motion.easing.standard`.
- Retry button spinner transition: `motion.duration.fast` (150ms).
- Reduced Motion: Transitions disabled when `prefers-reduced-motion: reduce` is active.

---

## 24. AI Behavior & Guardrails
- *AI Guidance:* If an AI operation fails (e.g., token context window exceeded, content filter triggered), the error message must explain the exact reason in plain human language, not raw stack traces, and offer prompt shortening suggestions.

---

## 25. Validation Criteria
- [x] In-flight user payload is preserved during network drop.
- [x] Retry button re-dispatches cached payload without requiring user re-entry.
- [x] Focus moves to the error container or primary recovery CTA.
- [x] Zero raw hex colors; 100% token-driven styling.

---

## 26. Anti-Patterns & Misuse
- ❌ **The Dead-End Error:** Displaying "Something went wrong" with no buttons or next steps.
- ❌ **The Amnesiac Crash:** Resetting the application to the login screen and wiping all form data.
- ❌ **The Cryptic Code:** Displaying `Error 0x80070002` to end users without plain-language explanation.

---

## 27. Governance & Lifecycle
- **Version:** `1.0.0`
- **Scope Invariant:** 0 new components, 0 new tokens, 0 deferred enterprise systems.
