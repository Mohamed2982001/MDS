# MDS Workflow: Settings & Preferences Update (MDS-WF-004)

## 1. Workflow Identification & Metadata
- **Workflow Name:** `Settings-Update`
- **ID:** `MDS-WF-004`
- **Layer:** `06-Workflows`
- **Family:** `Settings`
- **Verification Status:** `Manually Verified` (Testbed Sandbox) / `Automated Token/Style Integrity Check`

---

## 2. Purpose & Summary
The `Settings-Update` workflow governs how users view, modify, validate, and persist configuration preferences, account settings, and application options. It supports two primary mutation modes—**Instant Persistence (Inline Autosave)** for low-risk toggles and **Batched Persistence (Explicit Save)** for complex configurations—while managing dirty state detection and unsaved changes warnings.

---

## 3. User Intent
The user intends to change system behavior, visual preferences (e.g., theme, density), notification rules, or profile parameters.

---

## 4. Trigger
- User modifies an inline toggle/switch or select menu.
- User edits text fields and clicks the primary `"Save Preferences"` button in a batched settings view.

---

## 5. Preconditions
1. User has session privileges to update settings.
2. Current configuration is loaded and bound to form controls.

---

## 6. Actors & Roles
- **Primary Actor:** End User or System Operator.
- **System Actor:** Client Configuration Manager, Autosave Controller, and Backend Preferences Service.

---

## 7. Entry State
- **State Identifier:** `IDLE_LOADED`
- Settings views populated with current active system values.
- `isDirty = false`.
- If batched mode: "Save Changes" button is disabled or in resting state.

---

## 8. Sequential Steps (Happy Path)

### Mode 1: Instant Persistence (Inline Autosave)
```text
[1. TOGGLE OPTION] ──► [2. OPTIMISTIC UPDATE] ──► [3. BACKGROUND SYNC] ──► [4. TOAST / STATUS TICK]
  User Flips Switch      UI Changes Instantly      API Call Dispatched      "Settings Saved" Feedback
```
1. User flips a switch (e.g., Dark Mode or Email Alerts).
2. UI updates immediately (optimistic transition).
3. State machine enters background `PROCESSING`. A subtle inline status reads *"Saving..."*.
4. Backend confirms; status updates to *"Saved"* with a subtle checkmark for 2 seconds.

### Mode 2: Batched Persistence (Explicit Save)
```text
[1. MUTATE FIELDS] ──► [2. DIRTY STATE ACTIVE] ──► [3. CLICK SAVE] ──► [4. VALIDATE & DISPATCH] ──► [5. SAVED CLEAN]
  Edit Multiple          "Save Changes" Button       User Commits        Loading Spinner;             isDirty = false;
  Inputs                 Enables; Floating Bar       Form                API Confirms Update          Success Toast Shown
```
1. User modifies multiple fields across a settings section.
2. System sets `isDirty = true`. The "Save Changes" button enables; an optional floating sticky action bar appears.
3. User clicks "Save Changes". State machine transitions to `VALIDATING` $\to$ `PROCESSING`.
4. API confirms persistence. State machine transitions to `SUCCESS_RESOLVED`.
5. `isDirty` resets to `false`. Success toast notification is displayed.

---

## 9. Branches & Forks

```text
                     ┌──► [Branch A: Autosave Sync Failure] ──► Revert Switch & Show Error Toast
                     │
[Settings Mutation] ─┼──► [Branch B: Unsaved Navigation] ─────► Guard Modal: "Discard or Save Changes?"
                     │
                     └──► [Branch C: Validation Rejection] ───► Highlight Invalid Settings Input
```

- **Branch A (Autosave Failure):** If an inline autosave network call fails, revert the toggle back to its prior state and display an error alert with a `"Retry"` action.
- **Branch B (Unsaved Navigation Guard):** If user attempts to leave the view while `isDirty == true`, an exit confirmation dialog interrupts navigation: *"You have unsaved changes. Discard or Save?"*.
- **Branch C (Field Validation Failure):** If a setting input violates format rules, block the batched save and highlight the field with tokenized error styling.

---

## 10. Decision Points
- **Unsaved Changes Guard:** User chooses whether to discard edits, continue editing, or save immediately before leaving.
- **Reset to Defaults:** User chooses whether to restore system factory defaults.

---

## 11. Patterns Used
- `Form-Section` (`MDS/05-Patterns/Forms/Form-Section.md`): Used to divide settings into logical subsections (e.g., "Account", "Security", "Notifications").
- `Page-Header` (`MDS/05-Patterns/Navigation/Page-Header.md`): Provides page context and category breadcrumbs.
- `Data-List-Card` (`MDS/05-Patterns/Data/Data-List-Card.md`): Houses individual configurable options.

---

## 12. Components Used
- `Button` (Save Changes, Discard, Reset to Default)
- `Input` (Text settings, URLs, API keys)
- `Badge` (Status tags, beta features)
- `Dialog` (Unsaved changes guard modal)

---

## 13. Experience States
- **Idle State:** Settings options rendered with current configuration.
- **Loading State:** Background sync in progress; subtle spinner or "Saving..." indicator.
- **Error State:** Field error border or toast indicating persistence failure.
- **Success State:** Temporary "Saved" badge or toast notification.

---

## 14. Success Outcome
- Preferences persisted to client cache and remote backend.
- UI reflects updated behavior immediately.
- `isDirty` returned to `false`.

---

## 15. Failure Outcomes
- **Sync Failure:** Optimistic change reverted; user informed via non-intrusive alert.
- **Validation Failure:** Clear explanation of invalid settings constraints.

---

## 16. Recovery Paths
- **Autosave Retry:** Click `"Retry"` toast to re-dispatch the failed preference change.
- **Discard Edits:** Click `"Discard Changes"` to roll back inputs to original baseline.
- **Reset Defaults:** Option to revert section to default system configuration.

---

## 17. Cancellation & Exit Affordances
- **Discard Button:** Reverts all dirty fields to `initialValues`.
- **Navigation Guard:** Prevents accidental data loss when switching tabs or closing window.

---

## 18. Data & State Requirements
```typescript
interface SettingsUpdateState {
  initialConfig: Record<string, any>;
  currentConfig: Record<string, any>;
  isDirty: boolean;
  isSaving: boolean;
  lastSavedAt: number | null;
  saveMode: 'instant' | 'batched';
  syncError: string | null;
}
```

---

## 19. Accessibility Contracts
- **Live Status:** "Saving..." and "Saved" status updates are announced via `aria-live="polite"`.
- **Switch Controls:** Toggles use native role or `role="switch"` with `aria-checked="true|false"`.
- **Guard Dialog:** Focus trapped when unsaved changes modal is displayed; returns to active field upon cancel.
- **WCAG Standard:** Implemented accessibility behaviors were validated against selected WCAG success criteria where applicable. Comprehensive cross-platform assistive technology testing remains deferred to Phase 8.

---

## 20. Responsive Behavior
- **Mobile (320px – 767px):** Settings options stack vertically. Sticky bottom bar houses "Save Changes" and "Discard" buttons. Interactive controls preserve the MDS minimum interaction target where applicable.
- **Tablet & Desktop (768px – 1440px):** Multi-column settings sections; actions align inline-end.
- **Overflow:** The current sandbox was checked at the defined MDS responsive modes and showed no observed horizontal overflow for the included Workflow examples.

---

## 21. RTL Behavior
- Toggle switches, labels, and helper text mirror cleanly across the inline axis.
- In RTL, switches sit at the inline-end, labels at inline-start.
- RTL structural and logical-property checks passed in the current sandbox. Broader language/content localization testing remains outside this closure pass.

---

## 22. Density Modes
- **Default Mode:** Toggle row min-height 48px; padding 16px.
- **Compact Mode:** Toggle row min-height 36px; padding 8px.

---

## 23. Motion & Transitions
- Switch thumb slide: `motion.duration.fast` (150ms) with `motion.easing.standard`.
- Sticky action bar slide-up: `motion.duration.moderate` (250ms) with `motion.easing.standard`.
- Reduced Motion: Transitions disabled when `prefers-reduced-motion: reduce` is active.

---

## 24. AI Behavior & Guardrails
- *AI Guidance:* If an AI recommendation engine proposes optimized settings, each recommendation is flagged with a `"Recommended by AI"` badge and requires explicit user opt-in before saving.

---

## 25. Validation Criteria
- [x] Mutating fields enables Save button and updates `isDirty` flag.
- [x] Leaving dirty view triggers unsaved changes confirmation modal.
- [x] Failed autosave reverts toggle state and notifies user.
- [x] Zero raw hex colors; 100% token-driven styling.

---

## 26. Anti-Patterns & Misuse
- ❌ **The Silent Reversion:** Silently snapping a toggle back without telling the user the network request failed.
- ❌ **The Unsaved Trap:** Allowing a user to navigate away and losing 20 edited settings without a confirmation prompt.
- ❌ **The Indecisive UI:** Mixing instant autosave and batched save buttons within the exact same section.

---

## 27. Governance & Lifecycle
- **Version:** `1.0.0`
- **Scope Invariant:** 0 new components, 0 new tokens, 0 deferred enterprise systems.
