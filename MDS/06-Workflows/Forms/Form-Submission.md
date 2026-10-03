# MDS Workflow: Form-Submission (MDS-WF-001)

## 1. Workflow Identification & Metadata
- **Workflow Name:** `Form-Submission`
- **ID:** `MDS-WF-001`
- **Layer:** `06-Workflows`
- **Family:** `Forms`
- **Verification Status:** `Manually Verified` (Testbed Sandbox) / `Automated Token/Style Integrity Check`

---

## 2. Purpose & Summary
The `Form-Submission` workflow coordinates structured data entry, client-side constraint validation, asynchronous submission dispatch, server feedback processing, and post-submission resolution. It ensures zero user data loss during failures, provides immediate validation feedback, and maintains an accessible, deterministic focus journey.

---

## 3. User Intent
The user intends to create, capture, or update a business entity (e.g., user account, project, billing profile) by providing structured values through form controls and submitting them for persistence.

---

## 4. Trigger
- **Explicit Trigger:** The user clicks or presses the primary `Submit` button (`Button` component with `variant="primary"`).
- **Keyboard Trigger:** The user presses `Enter` while focused on a single-line input field within an active form context.

---

## 5. Preconditions
1. The user has active session privileges to write/create the entity.
2. The form container and initial field controls are mounted and hydrated in the DOM.
3. Network connection is initialized.

---

## 6. Actors & Roles
- **Primary Actor:** End User (Standard, Admin, or Anonymous depending on context).
- **System Actor:** Client-side Form State Machine, Validation Engine, and Backend API Dispatcher.

---

## 7. Entry State
- **State Identifier:** `IDLE_UNTOUCHED`
- Form fields contain default empty strings or initial pre-populated values.
- No field errors are displayed.
- The submit button is rendered in its default resting state (`disabled=false` or evaluated via initial dirty check).
- `isDirty = false`.

---

## 8. Sequential Steps (Happy Path)

```text
[1. ENTRY] ──► [2. INPUT] ──► [3. CLIENT VALIDATE] ──► [4. ASYNC SUBMISSION] ──► [5. SUCCESS RESOLUTION]
  Mount Form     Populate        Validate Against        Lock Controls &          Display Success Toast
  & Focus        Fields          Schema Constraints      Show Loading Spinner     & Redirect / Reset
```

1. **Step 1 — Entry & Focus:** User enters view. Focus is set automatically on the first interactive input field (or remains in standard document order if view was not user-initiated).
2. **Step 2 — Data Input:** User enters data across fields. On `blur` or `change`, touched fields update client buffer.
3. **Step 3 — Submit Request & Validation:** User triggers `Submit`. The client state machine transitions to `VALIDATING` and checks all fields against schema rules.
4. **Step 4 — Processing & Dispatch:** If validation passes, form transitions to `PROCESSING`. Submit button renders an inline loading spinner; fields become read-only/disabled; payload is dispatched via network.
5. **Step 5 — Resolution:** Backend returns `200/201 Success`. State machine transitions to `SUCCESS_RESOLVED`. A success alert is displayed, and form either resets cleanly or navigates to the newly created entity.

---

## 9. Branches & Forks

```text
                    ┌──► [Branch A: Client Validation Error] ──► Focus First Invalid Field
                    │
[Submit Request] ───┼──► [Branch B: Network / Server 5xx] ────► Error-Recovery Banner (Keep Form Data)
                    │
                    ├──► [Branch C: Conflict 409 / 422] ──────► Highlight Conflicting Fields
                    │
                    └──► [Branch D: Happy Path 200/201] ──────► Success Resolution
```

- **Branch A (Client Validation Failure):** If required fields are missing or format is invalid, transition back to `ACTIVE_INPUT` immediately. Set focus to the first invalid field and announce error via `aria-describedby`.
- **Branch B (Network Failure):** If request times out or returns `500 Internal Server Error`, transition to `ERROR_INTERCEPTED`. Preserve all field values in client memory. Display an alert banner with a `Retry` action.
- **Branch C (Field-Specific Server Error 422):** Map backend validation errors back to specific field components. Focus the primary field with the server rejection message.

---

## 10. Decision Points
- **Submit Decision:** User decides whether to commit the form or abort.
- **Unsaved Changes Exit Decision:** If the user attempts to navigate away while `isDirty == true`, an exit-confirmation modal prompts the user to either discard changes or stay.
- **Retry Decision:** Following a server failure, user decides whether to retry immediately or modify input fields.

---

## 11. Patterns Used
- `Form-Section` (`MDS/05-Patterns/Forms/Form-Section.md`): Used to group related form controls with clear section titles and descriptive subtitles.
- `Page-Header` (`MDS/05-Patterns/Navigation/Page-Header.md`): Provides workflow context, title, and primary back/cancel navigation.

---

## 12. Components Used
- `Button` (Primary submit, secondary cancel, retry action)
- `Input` (Text, email, number fields)
- `Badge` (Optional/required indicator)
- `Dialog` (Unsaved changes confirmation if navigated away while dirty)

---

## 13. Experience States
- **Idle State:** Form rendered with empty inputs and clear labels.
- **Loading State:** Processing submission; submit button shows spinner; inputs disabled; `aria-busy="true"`.
- **Error State:** Alert banner at top of form; red tokenized border on invalid inputs; descriptive error text beneath fields.
- **Success State:** Form replaced by success confirmation card or notification toast.

---

## 14. Success Outcome
- Entity persisted to system.
- User notified via token-driven success feedback (`variant="success"`).
- State machine reaches terminal clean state (`isDirty = false`). Focus returned to page root or navigation destination.

---

## 15. Failure Outcomes
- **Client Constraint Failure:** Form blocked locally; 0 network trips.
- **Transient Network Drop:** Payload cached; retryable banner shown.
- **Unauthorized 401/403:** Form state frozen; user prompted to re-authenticate without losing input data.

---

## 16. Recovery Paths
- **Inline Fix:** User corrects invalid input in field; error clears dynamically on subsequent blur/change.
- **Network Retry:** User clicks `Retry` on error banner; state machine re-dispatches cached payload directly to `PROCESSING`.
- **Draft Preservation:** Form preserves user data in client state even if submission fails 10 times in a row.

---

## 17. Cancellation & Exit Affordances
- **Secondary Cancel Button:** Positioned adjacent to Submit button.
- **Clean Exit:** If `!isDirty`, clicking Cancel navigates back immediately.
- **Dirty Exit:** If `isDirty`, clicking Cancel invokes `Confirmation-Dialog` with message: *"You have unsaved changes. Discard changes?"*.

---

## 18. Data & State Requirements
```typescript
interface FormSubmissionState {
  values: Record<string, any>;
  errors: Record<string, string>;
  touched: Record<string, boolean>;
  isSubmitting: boolean;
  isValidating: boolean;
  submitCount: number;
  lastError: string | null;
}
```

---

## 19. Accessibility Contracts
- **Focus Order:** Natural tab order across all inputs ending with Cancel and Submit buttons.
- **Error Announcement:** Invalid fields linked to error messages via `aria-describedby="field-error-id"`. The first invalid field receives programmatic focus upon submit validation failure.
- **Processing Status:** Submit button receives `aria-busy="true"` and announces "Submitting..." via `aria-live="polite"`.
- **WCAG Standard:** Implemented accessibility behaviors were validated against selected WCAG success criteria where applicable. Comprehensive cross-platform assistive technology testing remains deferred to Phase 8.

---

## 20. Responsive Behavior
- **Mobile (320px – 767px):** Form fields stack in single vertical column (100% width). Submit and Cancel buttons stack vertically with full width; primary action on top. Interactive controls preserve the MDS minimum interaction target where applicable.
- **Tablet (768px – 1023px):** Multi-column grid for short paired fields (e.g., First Name, Last Name). Buttons align to inline-end.
- **Desktop (1024px – 1440px):** Form constrained to maximum width (`var(--mds-container-max-width, 1152px)`). Clean horizontal button cluster.
- **Overflow:** The current sandbox was checked at the defined MDS responsive modes and showed no observed horizontal overflow for the included Workflow examples.

---

## 21. RTL Behavior
- Uses CSS Logical Properties throughout (`margin-inline-start`, `padding-inline`, `text-align: start`).
- In RTL (Arabic / `dir="rtl"`), form labels and inputs align to the right naturally.
- Button clusters reverse reading order logically (`Cancel` then `Submit` from right to left).
- RTL structural and logical-property checks passed in the current sandbox. Broader language/content localization testing remains outside this closure pass.

---

## 22. Density Modes
- **Default Mode:** Input height 40px, field gap 16px (`var(--mds-space-4)`).
- **Compact Mode:** Input height 32px, field gap 8px (`var(--mds-space-2)`).

---

## 23. Motion & Transitions
- Validation error appearance: `motion.duration.fast` (150ms) with `motion.easing.standard`.
- Submit button spinner fade-in: `motion.duration.fast` (150ms).
- Reduced Motion: Transitions disabled (`transition: none`) when `prefers-reduced-motion: reduce` is active.

---

## 24. AI Behavior & Guardrails
- *Classification:* Deterministic Form Workflow.
- *AI Guidance:* If an AI assistant pre-populates form fields (e.g., autofill from document), all AI-suggested fields must display an informational badge (`Suggested by AI`) and require explicit human review before submission.

---

## 25. Validation Criteria
- [x] Input values are never cleared upon validation or network failure.
- [x] Submit button enters loading state and disables double-clicks while processing.
- [x] Focus jumps to the first invalid field upon validation failure.
- [x] Zero raw hex colors; 100% token-driven styles.
- [x] 44×44px touch targets preserved on mobile interactive controls.

---

## 26. Anti-Patterns & Misuse
- ❌ **The Amnesiac Form:** Wiping input fields after an API error.
- ❌ **The Premature Submitter:** Sending empty or invalid payloads to the server without client validation.
- ❌ **The Silent Blocker:** Disabling the Submit button with zero explanation as to why the form is invalid.

---

## 27. Governance & Lifecycle
- **Version:** `1.0.0`
- **Deprecation Policy:** Canonical workflow; non-deprecating.
- **Scope Invariant:** Employs 0 new components, 0 new tokens, and 0 deferred enterprise systems.
