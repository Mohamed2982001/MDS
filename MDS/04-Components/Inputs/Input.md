# MDS Component: Input

**Document Layer:** 04-Components / Inputs  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **Input** component is the primary control for capturing single-line text, numbers, emails, passwords, and search queries.

---

## 2. When to Use
- For single-line text entry in forms, filters, and modals.
- For search bars and numeric inputs.

---

## 3. When Not to Use
- For multi-line text: Use `Textarea` instead.
- For predefined selectable options: Use `Select` or `Radio` instead.

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ Input Container (Border + Radius + Surface)                 │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Inline Primitive (gap="xs", align="center")             │ │
│ │  ┌──────────────┐  ┌──────────────────┐  ┌────────────┐ │ │
│ │  │ Prefix Icon  │  │  <input> Element │  │SuffixAction│ │ │
│ │  └──────────────┘  └──────────────────┘  └────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Variants & Types
- Types: `text`, `email`, `password`, `number`, `search`, `tel`, `url`.
- Visual Variants: Standard boxed input (subtle border, white/dark surface).

---

## 6. Sizes

| Size | Control Height | Padding Inline | Font Size | Icon Size | Touch Target |
| :--- | :---: | :---: | :--- | :--- | :---: |
| `sm` | **32px** (`size.control.sm`) | 12px (`space.3`) | 12px (`font.size.xs`) | 16px | $\ge 44\text{px}$ (`PressTarget`) |
| `md` | **40px** (`size.control.md`) | 16px (`space.4`) | 14px (`font.size.sm`) | 20px | $\ge 44\text{px}$ (`PressTarget`) |
| `lg` | **48px** (`size.control.lg`) | 16px (`space.4`) | 16px (`font.size.base`) | 20px | Flush ($\ge 48\text{px}$) |

---

## 7. States
- `default`: Resting border (`component.input.border.default`).
- `hover`: Slightly darkened border (`color.neutral.400`).
- `focus`: Active focus outline (`FocusRing` / `component.input.border.focus`).
- `invalid`: High-contrast danger border (`component.input.border.invalid`).
- `disabled`: Non-interactive muted fill (`component.input.background.disabled`).
- `readOnly`: Text selectable but not editable; no focus ring or hover border.

---

## 8. Slots
- `prefix`: Leading icon or symbol (e.g. search magnifying glass, currency symbol).
- `suffix`: Trailing icon, clear button, or password visibility toggle.

---

## 9. Behavior & Interaction
- Clicking inside the box places focus and selects caret position.
- Suffix action buttons (e.g. password reveal) trigger their action without submitting parent forms (`type="button"`).

---

## 10. Keyboard Interaction
- `Tab` moves focus into the input.
- Typing modifies value.
- `Enter` inside form submits the form unless prevented.

---

## 11. Accessibility Guarantees
- Native `<input>` with full keyboard navigation.
- Accessible name provided via wrapping `Field` or explicit `aria-label`.
- Suffix buttons embed `VisuallyHidden` text labels.

---

## 12. Responsive Behavior
- Width defaults to `100%` of parent container, adapting fluidly across mobile and desktop.

---

## 13. Motion & Transitions
- Focus border and ring transitions use 150ms (`motion.fast`).

---

## 14. Token Mapping Hierarchy
- Background: `component.input.background.default` (`color.surface.default`).
- Border: `component.input.border.default` (`color.border.default`).
- Focus: `component.input.border.focus` (`color.brand.600`).
- Radius: `component.input.radius` (`radius.md`).

---

## 15. Composition Rules
- Always compose inside `Field` for form layout and validation.

---

## 16. AI Usage Rules
- **SEARCH FIELDS:** Use `type="search"` and prefix with Search `Icon`.
- **NUMERIC DATA:** For currency or numbers, pass `inputMode="decimal"` or `type="number"`.
