# MDS Component: Radio & RadioGroup

**Document Layer:** 04-Components / Inputs  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **Radio** and **RadioGroup** components allow users to select exactly one option from a list of two or more mutually exclusive choices.

---

## 2. When to Use
- When only a single choice can be active from a set of options.
- When all available options should be visible simultaneously (if options exceed 6, consider `Select`).

---

## 3. When Not to Use
- When multiple options can be chosen simultaneously: Use `Checkbox`.
- For instant independent on/off settings: Use `Switch`.

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ RadioGroup (role="radiogroup", Stack gap="sm")              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ PressTarget (44 × 44px)                                 │ │
│ │  Inline Primitive (gap="sm", align="center")            │ │
│ │   ┌──────────────┐  ┌─────────────────────────────────┐ │ │
│ │   │ Radio Circle │  │ Option Label                    │ │ │
│ │   │ (20 × 20px)  │  │ (Description beneath if needed) │ │ │
│ │   │  ● dot icon  │  │                                 │ │ │
│ │   └──────────────┘  └─────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Variants & States
- **Selection States:**
  - `unselected`: 20px circular ring with 1.5px subtle border.
  - `selected`: Brand blue border and outer ring with 8px solid inner dot.
- **Interactive States:** `default`, `hover`, `focus` (`FocusRing`), `disabled` (`opacity.disabled = 0.38`).

---

## 6. Sizes
- Outer Circle: **20 × 20px** (`size.icon.md`).
- Inner Dot: **8 × 8px**.
- Touch Hit-Box: $\ge \mathbf{44 \times 44px}$ (`PressTarget`).

---

## 7. Slots
- `label`: Option title.
- `description`: Optional subtext explaining the consequence of this choice.

---

## 8. Behavior & State Machine
- Selecting a radio option automatically unselects all other radio options within the parent `RadioGroup`.

---

## 9. Keyboard Interaction & Implementation Models
- **Native Web Baseline (Standard):** Using `<input type="radio" name="...">` leverages native browser keyboard handling. The browser engine natively manages mutual exclusivity and roving arrow-key focus traversal without client-side JavaScript overhead.
- **Custom WAI-ARIA Roving Tabindex Pattern (Headless / Cross-Platform):**
  - Container maintains `role="radiogroup"`.
  - Selected item receives `tabindex="0"`, all other items receive `tabindex="-1"`.
  - `Tab` moves focus into the selected radio item in the group (or the first item if none selected).
  - `Up Arrow` / `Left Arrow`: Selects and moves focus to the previous radio item (wraps around in headless pattern).
  - `Down Arrow` / `Right Arrow`: Selects and moves focus to the next radio item (wraps around in headless pattern).
  - `Space`: Selects the currently focused radio item if not already selected.

---

## 10. Accessibility Guarantees
- Container has `role="radiogroup"` and an accessible label (`aria-labelledby` linking to group title).
- Children have `role="radio"` with `aria-checked="true | false"`.

---

## 11. Responsive & RTL Behavior
- Aligns logically along the inline axis (`inline-start` circle $\to$ `inline-end` label). Arrow key navigation follows reading direction.

---

## 12. Motion & Transitions
- Inner dot scale and opacity transition uses 150ms (`motion.fast`).

---

## 13. Token Mapping Hierarchy
- Selected Ring: `color.action.primary.default` (`brand.600`).
- Radius: `radius.full` (circular).

---

## 14. Composition Rules
- Always group multiple `Radio` components inside a `RadioGroup` wrapped in a `Field`.

---

## 15. AI Usage Rules
- **NEVER ISOLATE RADIOS:** Radios must always belong to a `RadioGroup` sharing the same `name`.
