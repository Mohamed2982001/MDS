# MDS Component: IconButton

**Document Layer:** 04-Components / Actions  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **IconButton** provides a compact, icon-only trigger for common actions in tight spaces (e.g. toolbars, table row action menus, search clear buttons, dialog close triggers). It enforces mandatory non-visual labeling and minimum touch targets.

---

## 2. When to Use
- When space is constrained and the action icon is universally recognizable (e.g. "Close", "Search", "Edit", "Delete", "More options").
- In app headers, card corners, table row utility actions, and modal dismiss buttons.

---

## 3. When Not to Use
- When the icon meaning is ambiguous or culturally dependent (use a standard `Button` with visible text).
- For prominent primary call-to-actions on marketing or landing pages.

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ PressTarget (Invisible 44 × 44px hit-box on touch)          │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Interactive Square Surface (32 / 40 / 48px)             │ │
│ │  ┌───────────────────────────────────────────────────┐  │ │
│ │  │ Icon Primitive (16 / 20 / 24px)                   │  │ │
│ │  └───────────────────────────────────────────────────┘  │ │
│ │  ┌───────────────────────────────────────────────────┐  │ │
│ │  │ VisuallyHidden Primitive (Accessible Screen Name) │  │ │
│ │  └───────────────────────────────────────────────────┘  │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Variants & Intents
- `ghost` (Default): Transparent resting surface, subtle hover wash (`color.surface.raised`). Used for standard header and toolbar icons.
- `secondary`: Outlined border on white/default surface. Used when visual separation from the background is required.
- `destructive`: Crimson red hover and active states. Used for trash/delete icons.

---

## 6. Sizes

| Size | Visual Dimension | Icon Size | Corner Radius | Touch Hit-Box |
| :--- | :---: | :---: | :--- | :---: |
| `sm` | **32 × 32px** (`size.control.sm`) | 16px (`size.icon.sm`) | `radius.sm` (6px) | $\ge 44 \times 44\text{px}$ (`PressTarget`) |
| `md` | **40 × 40px** (`size.control.md`) | 20px (`size.icon.md`) | `radius.md` (10px) | $\ge 44 \times 44\text{px}$ (`PressTarget`) |
| `lg` | **48 × 48px** (`size.control.lg`) | 24px (`size.icon.lg`) | `radius.md` (10px) | Flush ($\ge 48 \times 48\text{px}$) |

---

## 7. States
- `default`, `hover`, `pressed`, `focus` (`FocusRing`), `disabled` (`opacity.disabled = 0.38`), `loading` (shows small Spinner).

---

## 8. Slots
- `icon`: Mandatory `Icon` primitive.
- `label`: **Mandatory string** rendered into `<VisuallyHidden>` and passed to `aria-label`.

---

## 9. Behavior & Interaction
- Clicking executes the associated callback.
- Touch events hit the expanded $44 \times 44\text{px}$ hit target without affecting desktop mouse precision.

---

## 10. Keyboard Interaction
- Standard button keyboard semantics: activated via `Enter` or `Space`, focused via `Tab`.

---

## 11. Accessibility Guarantees
- **Mandatory Accessible Name:** Component API requires `label: string`. Omitting `label` causes a TypeScript compilation error, preventing unlabelled button anti-patterns.
- **Screen Reader Discovery:** Renders `<VisuallyHidden>{label}</VisuallyHidden>` and sets `aria-label="{label}"`.
- **Focus Indicator:** 2px solid `brand.600` focus ring on `:focus-visible`.

---

## 12. Responsive Behavior
- Visual dimensions remain compact on mobile while `PressTarget` guarantees comfortable touch activation.

---

## 13. Motion & Transitions
- 150ms (`motion.fast`) standard background fade; collapses to 0ms on reduced-motion devices.

---

## 14. Token Mapping Hierarchy
- Dimensions map to `size.control.*` and `size.icon.*`.
- Radii map to `radius.sm` or `radius.md`.

---

## 15. Composition Rules
- Always compose `IconButton` inside `Inline(gap="xs")` when placing multiple utility buttons in a toolbar.

---

## 16. AI Usage Rules
- **NEVER OMIT LABEL:** Never generate an `IconButton` without a descriptive `label` (e.g. `label="Close dialog"`).
- **NEVER USE FOR EXPANSIVE TEXT:** Only single-action icon controls qualify as `IconButton`.
