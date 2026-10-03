# MDS Workflow: Destructive Action (MDS-WF-003)

## 1. Workflow Identification & Metadata
- **Workflow Name:** `Destructive-Action`
- **ID:** `MDS-WF-003`
- **Layer:** `06-Workflows`
- **Family:** `Actions`
- **Verification Status:** `Manually Verified` (Testbed Sandbox) / `Automated Token/Style Integrity Check`

---

## 2. Purpose & Summary
The `Destructive-Action` workflow governs high-impact, irreversible operations (such as permanently deleting entities, revoking administrative privileges, or terminating subscriptions). It introduces intentional, calibrated UX friction to prevent accidental invocation, discloses non-recoverable consequences clearly, requires unambiguous user confirmation, and handles deletion execution and post-deletion recovery.

---

## 3. User Intent
The user intends to permanently remove, destroy, or revoke an existing system resource or permission.

---

## 4. Trigger
- User clicks a destructive action button or menu item styled with the danger token (`variant="danger"` / `color.feedback.error`).

---

## 5. Preconditions
1. The target entity exists and is in a deletable state.
2. The user has initiating privileges (client-side pre-check).

---

## 6. Actors & Roles
- **Primary Actor:** Authorized User or Administrator.
- **System Actor:** Client Confirmation Controller, Backend Authorization Policy Engine (`AuthZ`), and Deletion Service.

---

## 7. Entry State
- **State Identifier:** `IDLE_SELECTABLE`
- The entity is visible in a resting state (e.g., in a `Data-List-Card`).
- The trigger button is resting with red/danger accent styling.

---

## 8. Sequential Steps (Happy Path)

```text
[1. TRIGGER] ──► [2. CONFLICT/CONSEQUENCE] ──► [3. HIGH-FRICTION CONFIRM] ──► [4. EXECUTION] ──► [5. REMOVAL]
  Click Delete     Mount Confirmation Modal       Type Name / Check Box          Lock Dialog &       Entity Removed
  Button           Disclose Exact Loss Scope      Click Danger Confirm Button    Dispatch Delete     & Focus Reset
```

1. **Step 1 — Initiation:** User clicks "Delete Resource". The state machine transitions to `CONFIRMING`.
2. **Step 2 — Consequence Disclosure:** The `Confirmation-Dialog` pattern mounts as an accessible modal overlay. It clearly describes:
   - The exact name of the entity being destroyed.
   - The permanent consequences (e.g., *"This will permanently delete 14 sub-records and cannot be undone"*).
3. **Step 3 — High-Friction Challenge (If Critical):** For catastrophic actions, a challenge input requires the user to type the exact entity name (e.g., *"Type 'production-db' to confirm"*). The primary confirm button remains disabled until the string matches identically.
4. **Step 4 — Execution & Processing:** User clicks "Delete Permanently". The dialog locks; confirm button displays a loading spinner; `aria-busy="true"`. State machine transitions to `PROCESSING`.
5. **Step 5 — Removal & Focus Resolution:** Server returns `204 No Content / 200 OK`. State machine transitions to `SUCCESS_RESOLVED`. Dialog unmounts. Entity is removed from view. A toast notification confirms deletion. Focus returns safely to the parent container.

---

## 9. Branches & Forks

```text
                   ┌──► [Branch A: User Cancels / Escapes] ──► Close Modal, Restore Focus to Trigger
                   │
[Delete Trigger] ──┼──► [Branch B: AuthZ Forbidden 403] ─────► Keep Entity, Show "Permission Denied"
                   │
                   ├──► [Branch C: Deletion Timeout/5xx] ────► Keep Modal, Show Actionable Retry
                   │
                   └──► [Branch D: Deletion Success] ────────► Remove Entity, Show Undo Toast (If Soft)
```

- **Branch A (Cancellation):** User clicks "Cancel", clicks backdrop, or presses `Escape`. Dialog unmounts cleanly; no mutation occurs; focus is restored to the invoking button.
- **Branch B (Authorization Rejection 403):** Backend rejects deletion due to policy. Dialog unmounts; error alert informs user that administrative privileges are required.
- **Branch C (Network Error):** Dialog remains open; an inline error banner displays *"Deletion failed due to network timeout. Please retry"*; confirm button is re-enabled.
- **Branch D (Soft Delete with Undo):** If the system supports soft deletes, the success toast provides a 10-second `"Undo"` button before permanent purge.

---

## 10. Decision Points
- **Consequence Evaluation:** User reads warning text and decides whether to abort or proceed.
- **Challenge Verification:** User actively types confirmation string to prove conscious intent.

---

## 11. Patterns Used
- `Confirmation-Dialog` (`MDS/05-Patterns/Feedback/Confirmation-Dialog.md`): Modal dialog configured with `variant="danger"`.
- `Data-List-Card` (`MDS/05-Patterns/Data/Data-List-Card.md`): The entity card housing the initial delete trigger.

---

## 12. Components Used
- `Dialog` (Modal container, backdrop scrim, header, action footer)
- `Button` (Danger confirm button, secondary neutral cancel button)
- `Input` (Confirmation string verification input)
- `Badge` (Critical/irreversible warning badge)

---

## 13. Experience States
- **Idle State:** Target entity in resting list view with delete trigger.
- **Loading State:** Modal locked with processing spinner inside danger button.
- **Error State:** Red alert banner inside modal indicating deletion failure.
- **Success State:** Entity cleanly unmounted with success toast confirmation.

---

## 14. Success Outcome
- Entity permanently deleted or soft-deleted according to system policy.
- Zero unintended side effects.
- User informed via tokenized success notification.

---

## 15. Failure Outcomes
- **Permission Rejection:** Unauthorized users cannot delete.
- **Server Breakdown:** Target resource remains completely intact; zero partial or corrupted state.

---

## 16. Recovery Paths
- **Immediate Cancel:** Closes modal instantly; leaves entity 100% untouched.
- **Server Retry:** Click `"Retry"` on the error banner without closing modal.
- **Undo Toast:** For soft-deletable entities, a temporary undo action restores the record.

---

## 17. Cancellation & Exit Affordances
- Prominent secondary `"Cancel"` button.
- Top-corner accessible `"Close"` button (`aria-label="Close dialog"`).
- Keyboard `Escape` key immediately closes the dialog.
- Clicking backdrop scrim closes the dialog (unless high-friction string challenge is active).

---

## 18. Data & State Requirements
```typescript
interface DestructiveActionState {
  targetEntityId: string;
  targetEntityName: string;
  confirmationChallengeText: string;
  userEnteredChallenge: string;
  isConfirmed: boolean;
  isDeleting: boolean;
  error: string | null;
}
```

---

## 19. Accessibility Contracts
- **Focus Trap:** When `Confirmation-Dialog` opens, focus is programmatically trapped within the modal container. Initial focus is placed on the **Cancel** button (never on the destructive confirm button, preventing accidental spacebar activation).
- **Focus Restoration:** When the dialog closes (via Cancel or Escape), focus is returned precisely to the trigger button that launched the modal.
- **Role:** `role="alertdialog"` with `aria-modal="true"`, `aria-labelledby="dialog-title"`, and `aria-describedby="dialog-description"`.
- **WCAG Standard:** Implemented accessibility behaviors were validated against selected WCAG success criteria where applicable. Comprehensive cross-platform assistive technology testing remains deferred to Phase 8.

---

## 20. Responsive Behavior
- **Mobile (320px – 767px):** Dialog converts to bottom sheet or full-width modal (margins 16px). Cancel and Delete buttons stack vertically with Cancel on top to prioritize safety. Interactive controls preserve the MDS minimum interaction target where applicable.
- **Tablet & Desktop (768px – 1440px):** Centered modal (max-width 480px) with backdrop scrim. Cancel and Delete buttons align inline-end.
- **Overflow:** The current sandbox was checked at the defined MDS responsive modes and showed no observed horizontal overflow for the included Workflow examples.

---

## 21. RTL Behavior
- Modal layout and buttons mirror cleanly using CSS Logical Properties.
- In RTL, `"Cancel"` and `"Delete"` maintain logical ordering (`start` to `end`).
- RTL structural and logical-property checks passed in the current sandbox. Broader language/content localization testing remains outside this closure pass.

---

## 22. Density Modes
- Modals maintain comfortable touch padding across density themes to prevent accidental mis-clicks.

---

## 23. Motion & Transitions
- Modal backdrop fade-in: `motion.duration.fast` (150ms) with `motion.easing.standard`.
- Modal scale-in: `motion.duration.moderate` (250ms) with `motion.easing.standard`.
- Reduced Motion: Transitions disabled when `prefers-reduced-motion: reduce` is active.

---

## 24. AI Behavior & Guardrails
- *Rule:* **AI models may NEVER trigger a Destructive Action autonomously.**
- *Guardrail:* Any AI-suggested deletion must be presented to a human operator who must execute this manual destructive action workflow explicitly.

---

## 25. Validation Criteria
- [x] Initial focus is placed on the Cancel button, never the Delete button.
- [x] Focus trap keeps keyboard navigation inside the modal.
- [x] Pressing `Escape` cancels the flow and restores focus to trigger.
- [x] Danger token colors (`color.feedback.error`) used for destructive accents (0 raw hex).
- [x] Security Triad documented: Confirmation $\ne$ Authentication $\ne$ Authorization.

---

## 26. Anti-Patterns & Misuse
- ❌ **The Hair-Trigger Deletion:** Deleting a resource immediately on a single click without confirmation.
- ❌ **The Focused Destroyer:** Opening a destructive modal and defaulting keyboard focus onto the "Delete" button.
- ❌ **The Amnesiac Dismissal:** Leaving keyboard focus stranded in the document body after modal closes.

---

## 27. Governance & Lifecycle
- **Version:** `1.0.0`
- **Security Mandate:** Strict decoupling of UI confirmation from AuthN/AuthZ.
- **Scope Invariant:** 0 new components, 0 new tokens, 0 deferred enterprise systems.
