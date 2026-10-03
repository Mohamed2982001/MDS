# MDS Component: Textarea

**Document Layer:** 04-Components / Inputs  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **Textarea** component provides a multi-line plain text editing field for long-form content, comments, descriptions, and notes.

---

## 2. When to Use
- For multi-line text input (e.g. bio, message, feedback, notes).
- When content exceeds 60 characters or requires line breaks.

---

## 3. When Not to Use
- For single-line inputs (use `Input`).
- For rich-text formatted editing (bold, italic, lists) — rich text editor is deferred per Section 34.

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ Textarea Container (Border + Radius + Surface)              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ <textarea> element                                      │ │
│ │ (softWrap: true, minHeight: 80px, auto-resize option)   │ │
│ └─────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Character Counter (Caption, right-aligned)              │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Variants & Behavior
- `resizable`: Vertical-only resize allowed (`resize: vertical`). Horizontal resize is strictly disabled to prevent breaking page layouts.
- `autoResize`: Dynamically grows with content length up to a specified maximum height.

---

## 6. Sizes
- `minRows`: Default 3 rows (approx. 80px height).
- `maxRows`: Optional ceiling before enabling internal scrolling.

---

## 7. States
- `default`, `hover`, `focus` (`FocusRing`), `invalid` (danger border), `disabled` (muted background).

---

## 8. Slots
- `children`: Value string.
- `counter`: Optional character count display (e.g. "120 / 500").

---

## 9. Behavior & Soft-Wrap Rule
- Enforces `softWrap: true` (`white-space: pre-wrap; word-break: break-word`). Text wraps seamlessly without horizontal scrolling or text clipping.

---

## 10. Keyboard Interaction
- `Enter` inserts a new line.
- `Ctrl+Enter` / `Cmd+Enter` can trigger form submission if configured.
- `Tab` moves focus to the next form control.

---

## 11. Accessibility Guarantees
- Semantic `<textarea>` element.
- Accessible name provided via `Field`'s `Label`.
- Character counter linked via `aria-describedby`.

---

## 12. Responsive Behavior
- Expands to 100% width of parent container.

---

## 13. Motion & Transitions
- 150ms focus ring and height transition.

---

## 14. Token Mapping Hierarchy
- Surface: `component.input.background.default`.
- Border: `component.input.border.default`.
- Focus: `component.input.border.focus`.
- Radius: `component.input.radius` (`radius.md`).

---

## 15. Composition Rules
- Always compose inside `Field` for consistent form semantics.

---

## 16. AI Usage Rules
- **NO HORIZONTAL RESIZE:** Never set `resize: both` or `resize: horizontal`. Always enforce `resize: vertical` or `resize: none`.
