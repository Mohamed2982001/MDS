# MDS Component: Field

**Document Layer:** 04-Components / Inputs  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **Field** component is the architectural backbone of the MDS Form System. It coordinates the structural layout, labels, helper text, error messages, and ARIA relationships for all underlying input controls (`Input`, `Textarea`, `Select`, `Checkbox`, `Radio`, `Switch`).

---

## 2. When to Use
- To wrap any user input control in a form.
- To establish accessible associations (`htmlFor`, `aria-describedby`, `aria-invalid`) automatically.

---

## 3. When Not to Use
- Do not render raw `<Input>` components in forms without a `Field` wrapper, as doing so leads to missing labels and disconnected error states.

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ Field Container (Stack gap="xs")                            │
│                                                             │
│   Label Primitive (htmlFor="field-id")                      │
│     ├── Text Label                                          │
│     └── Required Indicator (*, aria-hidden="true")          │
│                                                             │
│   Control Slot (Input, Select, Textarea)                    │
│     ├── id="field-id"                                       │
│     ├── aria-describedby="field-help field-error"           │
│     └── aria-invalid="true | false"                         │
│                                                             │
│   HelperText Primitive (id="field-help")                    │
│     └── Contextual instructions / format requirements       │
│                                                             │
│   LiveRegion / Error Message (id="field-error", role="alert")│
│     └── Validation error message                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Variants & Layouts
- `vertical` (Default): Label placed above the control. Optimal for responsive screens and dense forms.
- `horizontal`: Label placed inline-start beside the control. Used in wide desktop settings or settings dashboards.
- `inline-reverse`: Used for `Checkbox` and `Switch` where control precedes the label.

---

## 6. Sizes
- Inherent to the control wrapped (`sm` 32px, `md` 40px, `lg` 48px).

---

## 7. States
- `default`: Resting form field.
- `disabled`: Mutes label and helper text opacity to match disabled control.
- `invalid`: Highlights field with semantic danger styling and connects error live region.
- `required`: Renders accessible required marker.

---

## 8. Slots
- `label`: Label text or custom label content.
- `children`: The actual interactive control (`Input`, `Select`, `Textarea`).
- `helperText`: Optional supportive guidance text.
- `errorMessage`: Error string displayed when validation fails.

---

## 9. Behavior & State Machine
- When `errorMessage` is provided, `Field` automatically marks the child control with `aria-invalid="true"` and appends the error element ID to `aria-describedby`.

---

## 10. Keyboard Interaction
- Clicking the label focuses the associated input control via native `htmlFor` $\to$ `id` mapping.

---

## 11. Accessibility Guarantees
- **WCAG SC 1.3.1 (Info and Relationships):** Label is programmatically linked to the input.
- **WCAG SC 3.3.1 (Error Identification):** Errors are explicitly connected via `aria-describedby` and announced via `role="alert"`.
- **WCAG SC 3.3.2 (Labels or Instructions):** Mandatory visible label or accessible label provided.

---

## 12. Responsive Behavior
- In `horizontal` layouts, `Field` automatically collapses to `vertical` on screens below 768px (`collapseBelow="md"`).

---

## 13. Motion & Transitions
- Error message expansion uses subtle 150ms slide-and-fade; collapses to 0ms when reduced motion is preferred.

---

## 14. Token Mapping Hierarchy
- Spacing: `space.block.xs` (4px between label and control, 4px between control and helper).
- Label Color: `color.text.primary`.
- Error Color: `color.feedback.danger` (`palette.red.600`).

---

## 15. Composition Rules
- Always compose multiple `Field` components inside a `Stack(gap="md")` to preserve uniform form spacing.

---

## 16. AI Usage Rules
- **MANDATORY FORM WRAPPER:** An AI agent must NEVER emit a naked `<Input>` or `<Select>` without wrapping it in a `<Field>`.
- **ERROR MESSAGES:** When a field is invalid, pass `errorMessage="..."` to the `Field` rather than building custom red text.
