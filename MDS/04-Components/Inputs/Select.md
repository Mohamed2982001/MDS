# MDS Component: Select

**Document Layer:** 04-Components / Inputs  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **Select** component allows users to choose one option from a list of predefined values displayed in a dropdown menu.

---

## 2. When to Use
- When users must choose a single option from a list of more than 5 items (e.g. Country, Timezone, Category).
- When screen space is constrained and all options cannot be shown simultaneously.

---

## 3. When Not to Use
- When options are 5 or fewer and space permits: Use `Radio` for better visual scanning.
- For freeform text entry with suggestions: Use autocomplete (deferred per Section 34).

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ Select Container (Border + Radius + Surface)                │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Inline Primitive (justify="space-between")              │ │
│ │  ┌──────────────────────────────────┐  ┌──────────────┐ │ │
│ │  │ Selected Value / Placeholder     │  │ Chevron Icon │ │ │
│ │  │ (Text: font.size.sm)             │  │   ▼ icon     │ │ │
│ │  └──────────────────────────────────┘  └──────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Variants & Sizes

| Size | Control Height | Padding Inline | Chevron Size | Touch Target |
| :--- | :---: | :---: | :--- | :---: |
| `sm` | **32px** (`size.control.sm`) | 12px (`space.3`) | 16px | $\ge 44\text{px}$ (`PressTarget`) |
| `md` | **40px** (`size.control.md`) | 16px (`space.4`) | 20px | $\ge 44\text{px}$ (`PressTarget`) |
| `lg` | **48px** (`size.control.lg`) | 16px (`space.4`) | 20px | Flush ($\ge 48\text{px}$) |

---

## 6. States
- `default`: Resting border outline.
- `hover`: Border slightly darkened (`neutral.400`).
- `focus` / `open`: `FocusRing` active, chevron rotates 180°.
- `invalid`: Danger border (`feedback.danger`).
- `disabled`: Muted non-interactive background (`opacity.disabled = 0.38`).

---

## 7. Slots
- `placeholder`: Initial hint text before selection is made.
- `options`: List of `{ value, label, disabled? }`.

---

## 8. Implementation Tiers & State Machine
- **Core Baseline Tier (Native Select):** Implemented core baseline. Uses `<select class="mds-input mds-select">`. Provides 100% native mobile picker integration (iOS Wheel, Android Drawer), native assistive technology announcements, zero layout clipping, and zero custom JavaScript state overhead.
- **Enhanced Tier (Custom Listbox):** Architectural specification only for future implementation (not implemented in Phase 5). Defines custom dropdown surface using `role="combobox"`, `aria-expanded`, and `role="listbox"` when rich option content (avatars, icons, badges) is explicitly required.

---

## 9. Keyboard Interaction
- **Native Select:** Handled entirely by browser standard keyboard ergonomics (`Alt+Down`, `Space`, arrow keys, typeahead).
- **Custom Listbox Tier:**
  - `Space` or `Enter` opens the dropdown listbox.
  - `Down Arrow` / `Up Arrow` navigates through options.
  - `Enter` commits the highlighted option and closes the dropdown.
  - `Escape` dismisses the dropdown without changing selection.

---

## 10. Accessibility Guarantees
- **Baseline Tier:** Native `<select>` guarantees full platform-level accessibility and screen-reader form controls.
- **Custom Tier:** Explicit WAI-ARIA Combobox 1.2 pattern (`role="combobox"`, `aria-expanded`, `aria-controls`, `role="listbox"`, `role="option"`, `aria-selected`).
- Accessible label connected via `Field`'s `Label` (`for`/`id` association).

---

## 11. Responsive & RTL Behavior
- In RTL, chevron icon sits at `inline-end` (left) and selected text aligns to `inline-start` (right).

---

## 12. Motion & Transitions
- Chevron rotation uses 150ms (`motion.fast`) with `motion.ease.standard`.

---

## 13. Token Mapping Hierarchy
- Background: `component.input.background.default`.
- Border: `component.input.border.default`.
- Focus: `component.input.border.focus`.
- Radius: `component.input.radius` (`radius.md`).

---

## 14. Composition Rules
- Always compose inside `Field` for form label and error wiring.

---

## 15. AI Usage Rules
- **FEW OPTIONS:** If options $\le 4$, prefer `Radio` over `Select`.
