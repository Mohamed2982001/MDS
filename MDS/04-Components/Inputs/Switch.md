# MDS Component: Switch

**Document Layer:** 04-Components / Inputs  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **Switch** component provides a binary toggle control for instantly turning a preference or feature on or off without requiring a "Save" or "Submit" step.

---

## 2. When to Use
- For immediate instant settings (e.g. "Push Notifications", "Auto-Save", "Airplane Mode").
- In settings screens and preference panels.

---

## 3. When Not to Use
- Inside forms that require explicit submission via a "Submit" button: Use `Checkbox` instead.
- For non-binary choices: Use `Radio` or `Select`.

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ PressTarget (44 × 44px hit-box on touch)                    │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Inline Primitive (gap="sm", align="center")             │ │
│ │  ┌──────────────────────────────────┐  ┌──────────────┐ │ │
│ │  │ Label Text                       │  │ Track (Pill) │ │ │
│ │  │                                  │  │  ┌─────────┐ │ │ │
│ │  │                                  │  │  │ Thumb ○ │ │ │ │
│ │  │                                  │  │  └─────────┘ │ │ │
│ │  └──────────────────────────────────┘  └──────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Variants & States
- **Track States:**
  - `off`: Neutral track fill (`neutral.300` / `neutral.700` in dark mode) with thumb on `inline-start`.
  - `on`: Solid brand blue fill (`brand.600`) with thumb translated to `inline-end`.
- **Interactive States:** `default`, `hover`, `focus` (`FocusRing`), `disabled` (`opacity.disabled = 0.38`).

---

## 6. Sizes
- Track: **40px width × 24px height**.
- Thumb: **18 × 18px white circle**.
- Touch Target: $\ge \mathbf{44 \times 44px}$ (`PressTarget`).

---

## 7. Slots
- `label`: Associated setting name.
- `description`: Optional supporting context beneath label.

---

## 8. Behavior & State Machine
- Clicking the track, thumb, or label toggles the state immediately and fires the `onChange` event.

---

## 9. Keyboard Interaction
- `Tab` moves focus to the switch track.
- `Space` or `Enter` toggles the switch.

---

## 10. Accessibility Guarantees
- Semantic ARIA role: `role="switch"`.
- Sets `aria-checked="true | false"`.
- Focus ring rendered cleanly on track boundary during keyboard navigation.

---

## 11. Responsive & RTL Behavior
- Under RTL, the thumb translates from right (`inline-start` = off) to left (`inline-end` = on).

---

## 12. Motion & Transitions
- Thumb horizontal translation and track background-color interpolation are strictly bound to approved motion tokens:
  - Duration: `var(--mds-motion-normal)` (`motion.duration.normal` = 250ms).
  - Easing curve: `var(--mds-motion-ease-standard)` (`motion.ease.standard` = cubic-bezier(0.2, 0, 0, 1)).
  - Zero raw literals are permitted.
  - Collapses to 0ms when `prefers-reduced-motion: reduce` is active.

---

## 13. Token Mapping Hierarchy
- Active Track: `color.action.primary.default` (`brand.600`).
- Inactive Track: `color.neutral.300`.
- Thumb: `color.neutral.0` (White).
- Radius: `radius.full`.

---

## 14. Composition Rules
- Use inside `Inline(justify="space-between")` for settings list rows.

---

## 15. AI Usage Rules
- **INSTANT VS FORM SUBMIT:** Only use `Switch` if the action takes effect immediately without a submit button.
