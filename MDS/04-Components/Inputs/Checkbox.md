# MDS Component: Checkbox

**Document Layer:** 04-Components / Inputs  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **Checkbox** component allows users to select one or multiple items from a list, or to toggle a single independent binary preference.

---

## 2. When to Use
- When users can select zero, one, or multiple options from a group.
- For terms and conditions agreement agreements.
- For multi-select table rows with an "indeterminate" select-all header state.

---

## 3. When Not to Use
- For mutually exclusive options where only one can be chosen: Use `Radio` instead.
- For immediate instant binary settings (e.g. "Dark Mode", "Airplane Mode"): Use `Switch` instead.

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ PressTarget (44 × 44px hit-box on touch)                    │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Inline Primitive (gap="sm", align="center")             │ │
│ │  ┌──────────────┐  ┌──────────────────────────────────┐ │ │
│ │  │ Checkbox Box │  │ Label Text                       │ │ │
│ │  │ (20 × 20px)  │  │                                  │ │ │
│ │  │  ✓ or - icon │  │                                  │ │ │
│ │  └──────────────┘  └──────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Variants & States
- **Selection States:**
  - `unchecked`: Empty box with 1.5px subtle border.
  - `checked`: Solid brand blue fill (`brand.600`) with white checkmark icon.
  - `indeterminate`: Solid brand blue fill with white horizontal minus/dash icon (for parent select-all states).
- **Interactive States:** `default`, `hover`, `focus` (`FocusRing`), `disabled` (`opacity.disabled = 0.38`), `invalid` (danger border).

---

## 6. Sizes
- Visual Box: **20 × 20px** (`size.icon.md`).
- Touch Hit-Box: $\ge \mathbf{44 \times 44px}$ enforced via `PressTarget`.
- Corner Radius: `radius.xs` (4px).

---

## 7. Slots
- `label`: Associated label text.
- `description`: Optional supporting explanation beneath label.

---

## 8. Behavior & State Transitions
- Clicking the box or label toggles between checked and unchecked.
- Indeterminate state clears upon user interaction, transitioning to checked or unchecked.

---

## 9. Keyboard Interaction
- `Tab` moves focus to the checkbox.
- `Space` key toggles selection state.

---

## 10. Accessibility Guarantees
- Native `<input type="checkbox">` visually hidden or custom rendered with `role="checkbox"`.
- Uses `aria-checked="true | false | mixed"` (where `mixed` represents indeterminate).
- Focus ring rendered on `:focus-visible`.

---

## 11. Responsive & RTL Behavior
- In RTL, the checkbox box sits at `inline-start` (right) followed by the label (left) via native Flexbox flow.

---

## 12. Motion & Transitions
- Checkmark scale and opacity transition uses 150ms (`motion.fast`).

---

## 13. Token Mapping Hierarchy
- Active Fill: `color.action.primary.default` (`brand.600`).
- Border: `color.border.default`.
- Radius: `radius.xs` (4px).

---

## 14. Composition Rules
- Compose lists of checkboxes inside `Stack(gap="sm")`.

---

## 15. AI Usage Rules
- **DO NOT USE FOR MUTUALLY EXCLUSIVE OPTIONS:** If selecting one option unchecks another, use `Radio`.
