# MDS Pattern: Form-Section

**Document Layer:** 05-Patterns / Forms  
**Status:** STABLE (Phase 6 Implementation)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-16  

---

## 1. Purpose
The **Form-Section** pattern coordinates a thematic cluster of form inputs with a clear section header, descriptive contextual copy, inline error feedback, and an action footer. It breaks down complex data-entry workflows into digestible, scannable milestones.

---

## 2. User Intent
The user intends to create, configure, or update a coherent group of related business entities or personal preferences (e.g. Profile Information, Security Settings, Billing Address).

---

## 3. Problem Solved
Eliminates form fatigue and cognitive overload caused by unorganized walls of inputs. Ensures standardized vertical spacing, consistent label-to-control wiring, and clear visual separation between primary submission actions and secondary cancellation.

---

## 4. When to Use
- Any settings page, modal configuration form, or entity creation view containing 2 or more related fields.
- When grouping inputs that belong to a single domain context (e.g. Account Credentials).
- When forms require explicit batched submission rather than instant inline updates.

---

## 5. When Not to Use
- For isolated single-field interactions (e.g., standalone Search or Newsletter signup): Use `Field` directly.
- For instant independent on/off preferences: Use an unsubmitted settings list with `Switch`.
- For multi-step wizard sequences spanning separate screens: Use Layer 06 `Multi-Step-Workflow`.

---

## 6. Composition Architecture

```text
┌───────────────────────────────────────────────────────────────────────────┐
│ Form-Section (Surface.raised / Card, border, radius.lg, padding.6)        │
│                                                                           │
│  Section Header (Stack gap="xs")                                          │
│   ├── Heading H3 (font.size.lg, font.weight.semibold)                     │
│   └── Description (Text.secondary, font.size.sm, softWrap: true)          │
│                                                                           │
│  Divider / Visual Boundary (border.subtle)                                │
│                                                                           │
│  Fields Body (Stack gap="md" or Grid columns="2" gap="md")                │
│   ├── Field 1 (Label + Input + HelperText)                                │
│   ├── Field 2 (Label + Select + HelperText)                               │
│   └── Field 3 (Label + Textarea + HelperText)                             │
│                                                                           │
│  Form Action Bar (Inline justify="flex-end" gap="sm")                     │
│   ├── Secondary Action: Button(variant="secondary", "Cancel")             │
│   └── Primary Action:   Button(variant="primary",   "Save Changes")       │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Required Components
- `Stack` (Layer 03 Layout Primitive)
- `Inline` (Layer 03 Layout Primitive)
- `Heading` (Layer 03 Typography Primitive — H3)
- `Text` / `Caption` (Layer 03 Typography Primitive)
- `Field` (Layer 04 Input Component — coordinates Label, Control, and Error)
- `Button` (Layer 04 Actions Component — Primary and Secondary intents)

---

## 8. Optional Components
- `Alert` (Layer 04 Feedback Component — for section-level form submission errors)
- `Badge` (Layer 04 Data Display Component — for "Optional" or "Beta" indicators in the header)
- `Grid` (Layer 03 Layout Primitive — for multi-column desktop layouts)
- `Spinner` (Layer 04 Feedback Component — embedded inside the primary button during submission)

---

## 9. Information Hierarchy
1. **Primary Focus:** Section Title (H3) and introductory explanation orient the user.
2. **Secondary Focus:** Individual form fields arranged logically from top to bottom (or 2-column inline).
3. **Tertiary Focus:** Helper text beneath fields providing formatting guidance.
4. **Action Commitment:** Action bar anchored at the bottom-trailing edge.

---

## 10. Interaction Model
- `Tab` moves focus sequentially through interactive fields in DOM order.
- `Enter` within a single-line input triggers form submission if valid, or moves to next field.
- Validation triggers:
  - Format checks run on `blur` (`onBlur`).
  - Active error states clear as the user types (`onChange`).
- Submitting triggers a loading state on the primary button (`Button(loading=true)`), disabling all inputs.

---

## 11. Experience States
- **Default / Resting:** Inputs show empty or prefilled values with subtle resting borders.
- **Active / Focused:** Active control highlights with `color.border.focus` and `FocusRing`.
- **Loading / Submitting:** Primary button displays `Spinner`; inputs render disabled background (`opacity.disabled`).
- **Validation Error:** Field border shifts to `color.feedback.danger`; error message announced via `role="alert"`.
- **Success Confirmation:** Form displays a temporary success `Alert` banner or toasts confirmation.

---

## 12. Responsive Behavior
- **Compact (<640px):**
  - All multi-column grids collapse to a single vertical column (`Stack gap="md"`).
  - The Form Action Bar stacks vertically (`Stack gap="sm"`): Primary Button and Secondary Button both expand to full width (`width: 100%`) without altering DOM order.
- **Standard (640–1024px):**
  - 2-column grid for paired inputs (e.g., First Name / Last Name; City / State).
  - Action bar aligns inline to the trailing edge.
- **Wide (>1024px):**
  - Max section width constrained to `container.md` or `container.lg` to maintain comfortable line length.

---

## 13. Accessibility (a11y)
> *Standards Scope:* Implemented accessibility behaviors were validated against selected WCAG success criteria where applicable. Comprehensive cross-platform assistive technology testing remains deferred to Phase 8.
- **Landmark & Grouping:** The entire pattern is wrapped in `<form aria-labelledby="section-title-id">` or `<fieldset>`.
- **Label Associations:** Every field has an explicit programmatic connection (`htmlFor="input-id"`).
- **Error Live Region:** Form-level errors render in an `Alert` with `role="alert"` and `aria-live="assertive"`.
- **Touch Targets:** All interactive controls maintain $\ge 44 \times 44\text{px}$ hit areas where applicable via `PressTarget`. Static visual elements are exempt.

---

## 14. RTL & Logical Progression
- **Flow:** Layout progresses strictly along the inline axis (`inline-start` $\to$ `inline-end`).
- **No Row-Reverse:** Zero `row-reverse` is permitted. Under RTL, labels and inputs naturally align to the physical right.
- **Action Placement:** In RTL, primary button remains at the trailing edge (physical left).

---

## 15. Density Behavior
- **Comfortable (Default):** Section padding `space.6` (24px), field gap `space.4` (16px), controls `40px` (`md`).
- **Compact:** Section padding `space.4` (16px), field gap `space.3` (12px), controls `32px` (`sm`).
- **Dense:** Technical dashboards only. Padding `space.3` (12px), controls `32px` (`sm`). (0 unapproved 28px).

---

## 16. Motion & Animation
- Error message expansion uses 150ms (`var(--mds-motion-fast)`) with `var(--mds-motion-ease-standard)`.
- Transitions collapse to 0s under `@media (prefers-reduced-motion: reduce)`.

---

## 17. Token Usage
- Background: `color.surface.raised` (Surface Card)
- Border: `color.border.default`
- Section Title: `font.size.lg`, `color.text.primary`
- Description: `font.size.sm`, `color.text.secondary`
- Padding: `space.6` (Comfortable), `space.4` (Compact)
- Gap: `space.4` (Fields), `space.3` (Actions)

---

## 18. Contextual Variants
- **Stacked Variant (Default):** Header sits above fields; full-width card layout.
- **Split Variant (Settings Page):** Header and description sit in the leading column (1/3 width); fields and actions sit in the trailing column (2/3 width) on desktop viewports.

---

## 19. Composition Rules
- Never inject external margins; all spacing is owned by `Stack` and `Grid`.
- Primary CTA must always have clear visual priority over the secondary action.
- Destructive actions (e.g., "Delete Account") must never share the standard action bar; they require a dedicated Danger Zone section with `Confirmation-Dialog`.

---

## 20. Anti-Patterns & Prohibitions
- **NO ISOLATED INPUTS:** Never place an `<input>` without an accompanying `Label` and `HelperText` slot.
- **NO MULTI-PRIMARY ACTIONS:** Never place two primary buttons in the same action bar.
- **NO TRUNCATED LABELS:** Labels must always wrap cleanly without ellipsis.

---

## 21. AI Usage & Generation Rules
- When the user asks to "build a settings form" or "create a profile editor", the AI **MUST** select the `Form-Section` pattern.
- The AI must wrap all inputs inside `Field` components.
- The AI must generate both `Primary` (submit) and `Secondary` (cancel) actions in the footer.
- The AI must not invent custom CSS classes for spacing; it must strictly emit MDS Primitives (`Stack`, `Inline`, `Grid`).

---

## 22. Verification & Validation Criteria
- [ ] Section title has proper semantic heading tag (`h2` or `h3`).
- [ ] All inputs are linked to labels via `id`/`htmlFor`.
- [ ] Error messages have `role="alert"`.
- [ ] Primary button displays loading spinner during asynchronous submission.
- [ ] 2-column layouts collapse to single-column on viewports $<640\text{px}$.
- [ ] Zero unmapped hex colors or physical CSS margins are present.
