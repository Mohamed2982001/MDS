# MDS Pattern: Confirmation-Dialog

**Document Layer:** 05-Patterns / Feedback  
**Status:** STABLE (Phase 6 Implementation)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-16  

---

## 1. Purpose
The **Confirmation-Dialog** pattern composes a focused modal overlay that captures user attention to explicitly confirm or cancel a high-risk, irreversible, or destructive operation (e.g. permanently deleting a database, removing team member access, revoking an API key).

---

## 2. User Intent
The user intends to execute a critical, potentially irreversible action, and the system prompts for explicit confirmation to prevent accidental catastrophic data loss or unwanted state mutation.

---

## 3. Problem Solved
Prevents accidental destruction of valuable records caused by single-click errors. Ensures that the consequence of the action is clearly stated and that cancellation is effortless and risk-free.

---

## 4. When to Use
- Any destructive operation (Delete, Destroy, Permanently Purge).
- High-impact irreversible configuration changes (e.g. changing subscription tier, resetting credentials).
- Leaving an uncompleted form with extensive unsaved changes.

---

## 5. When Not to Use
- For routine, non-destructive confirmations (e.g. "Item saved successfully"): Use `Alert` or toast.
- For trivial, low-risk actions: Prefer inline actions with an `Undo` toast.
- NEVER stack a Confirmation Dialog on top of another open modal dialog (anti-pattern).

---

## 6. Composition Architecture

```text
┌───────────────────────────────────────────────────────────────────────────┐
│ Backdrop Scrim (Surface.overlay, rgba(0,0,0,0.5), FocusTrap active)       │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │ Dialog Container (Surface.raised, elevation.level3, radius.lg)      │  │
│  │  max-width: 480px, padding: space.6                                 │  │
│  │                                                                     │  │
│  │   Header Strip (Inline gap="sm" align="flex-start")                 │  │
│  │    ├── Warning / Destructive Icon (Icon ⚠️ in palette.red.600)      │  │
│  │    └── Title Group (Stack gap="2xs")                                │  │
│  │         ├── Heading H3: "Delete Project Forever?"                   │  │
│  │         └── Caption: "Action cannot be undone"                      │  │
│  │                                                                     │  │
│  │   Body Copy (Text font.size.sm, color="text.secondary", wrap=true)  │  │
│  │    "This will permanently delete the project 'Falcon-9' and all     │  │
│  │     associated deployment configurations. All 14 team members       │  │
│  │     will lose access immediately."                                  │  │
│  │                                                                     │  │
│  │   Action Footer (Inline justify="flex-end" gap="sm")                │  │
│  │    ├── Cancel:  Button(variant="secondary", "Keep Project")         │  │
│  │    └── Confirm: Button(variant="destructive", "Permanently Delete") │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Required Components
- `Dialog` (Layer 04 Overlays Component — surface, backdrop, focus trap, Escape dismissal)
- `Heading` (Layer 03 Typography Primitive — H3 dialog title)
- `Text` (Layer 03 Typography Primitive — consequence body copy)
- `Button` (Layer 04 Actions Component — Destructive Confirm & Secondary Cancel)
- `Icon` (Layer 03 Primitive — warning or alert glyph)
- `Inline` & `Stack` (Layer 03 Layout Primitives)

---

## 8. Optional Components
- `Input` (Layer 04 Input Component — for explicit "Type entity name to confirm" friction gate)
- `Spinner` (Layer 04 Feedback Component — inside the confirm button during execution)

---

## 9. Information Hierarchy
1. **Prominent Alert:** Warning icon and clear, explicit question ("Delete Project Forever?").
2. **Consequence Statement:** Clear description detailing exactly what will be destroyed or lost.
3. **Primary Escape Route:** Prominent "Cancel" button giving the user a safe way out.
4. **Destructive Execution:** Distinct red destructive button confirming intent.

---

## 10. Interaction Model
- Dialog opens with focus trapped inside the modal container.
- Initial focus is placed on the **Cancel** button (NOT the destructive confirm button) to prevent accidental Enter-key triggers.
- `Escape` key immediately dismisses the dialog without taking action.
- Clicking the backdrop scrim dismisses the dialog.
- Clicking Confirm shifts button into loading state (`Button(loading=true)`), executes mutation, closes modal on success, and shifts focus back to the originating trigger button.

---

## 11. Experience States
- **Resting Confirmation:** Standard modal presentation.
- **Typing Verification:** If typed confirmation is required, confirm button remains disabled until input matches exact entity name.
- **Executing / Loading:** Confirm button displays `Spinner`; Cancel button is disabled; backdrop prevents clicks.
- **Error State:** If mutation fails, dialog displays an inline `Alert(danger)` banner without dismissing the dialog.

---

## 12. Responsive Behavior
- **Compact (<640px):**
  - Dialog aligns to bottom of screen as a mobile action sheet or stays centered with 16px margins (`calc(100% - 32px)`).
  - Actions stack vertically: Destructive Confirm on top, Cancel full-width underneath.
- **Standard & Wide (>640px):**
  - Centered horizontally and vertically in viewport (`max-width: 480px`).
  - Actions align inline at the trailing edge.

---

## 13. Accessibility (a11y)
> *Standards Scope:* Implemented accessibility behaviors were validated against selected WCAG success criteria where applicable. Comprehensive cross-platform assistive technology testing remains deferred to Phase 8.
- Dialog container has `role="alertdialog"` (due to high urgency and destructive consequence).
- `aria-modal="true"`.
- Linked via `aria-labelledby="dialog-title-id"` and `aria-describedby="dialog-desc-id"`.
- Strict Focus Trap: `Tab` cycles strictly within Cancel and Confirm buttons.
- Focus restoration: Focus returns to the trigger button that launched the dialog upon dismissal.
- Action buttons preserve minimum $\ge 44 \times 44\text{px}$ touch targets where applicable via `PressTarget`.

---

## 14. RTL & Logical Progression
- Layout flows along the inline axis.
- Warning icon sits at `inline-start`.
- Actions align to `inline-end`; Cancel sits at `inline-start` relative to Destructive Confirm.
- Zero `row-reverse` is permitted.

---

## 15. Density Behavior
- **Comfortable (Default):** Modal padding `space.6` (24px), title `font.size.lg`, gap `space.4`.
- **Compact:** Modal padding `space.4` (16px), gap `space.3`.
- Density does not compress touch targets below $\ge 44 \times 44\text{px}$.

---

## 16. Motion & Animation
- Backdrop fade-in and dialog scale-up (0.95 $\to$ 1.0) uses 250ms (`var(--mds-motion-normal)`) with `var(--mds-motion-ease-standard)`.
- Collapses to instant 0s under `prefers-reduced-motion: reduce`.

---

## 17. Token Usage
- Scrim: `color.surface.overlay`
- Surface: `color.surface.raised`
- Border: `color.border.default`
- Shadow: `elevation.level3`
- Destructive Button: `component.button.destructive.background.default`
- Warning Icon: `color.palette.red.600`
- Radius: `radius.lg`

---

## 18. Contextual Variants
- **Simple Binary Confirmation:** Title + Description + Cancel + Destructive Confirm.
- **High-Friction Typed Confirmation:** Includes an `Input` requiring exact name entry before confirm enables.

---

## 19. Composition Rules
- Initial focus must NEVER be placed on the destructive action; always land on Cancel.
- Must use `variant="destructive"` for destructive actions, never a standard primary brand blue.
- Never spawn a dialog from inside another dialog.

---

## 20. Anti-Patterns & Prohibitions
- **NO NESTED MODALS:** Never open a confirmation dialog on top of an existing modal.
- **NO VAGUE COPY:** Never say "Are you sure?". Always specify the item and consequence (e.g. "Permanently delete Falcon-9?").
- **NO TRAPPED FOCUS ESCAPE:** Never allow Tab to leak behind the modal backdrop.

---

## 21. AI Usage & Generation Rules
- When user asks to "confirm delete", the AI **MUST** select `Confirmation-Dialog`.
- The AI must configure the confirm button with `variant="destructive"`.
- The AI must explicitly specify `role="alertdialog"` and wire initial focus to Cancel.

---

## 22. Verification & Validation Criteria
- [ ] Container has `role="alertdialog"` and `aria-modal="true"`.
- [ ] Focus traps within modal; `Escape` key dismisses cleanly.
- [ ] Initial focus defaults to Cancel button.
- [ ] Confirm button uses `variant="destructive"`.
- [ ] Focus restores to trigger element upon closing.
- [ ] 0 raw hex colors or physical coordinates.
