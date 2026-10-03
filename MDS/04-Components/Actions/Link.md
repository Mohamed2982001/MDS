# MDS Component: Link

**Document Layer:** 04-Components / Actions  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **Link** component enables accessible textual navigation between internal application routes or external URLs.

---

## 2. When to Use
- To navigate to another page, view, or external website.
- For inline hypertext references within paragraphs or cards.

---

## 3. When Not to Use
- **Do NOT use for state mutation or business operations:** (e.g. saving, deleting, opening modals). Use `Button` instead.
- If an action triggers a backend API call without changing routes, it is a `Button`, not a `Link`.

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ <a> Anchor Element (Inline text or standalone link)         │
│  ┌──────────────────┐  ┌──────────────────────────────────┐ │
│  │   Link Text      │  │ External Icon (rel="noreferrer") │ │
│  └──────────────────┘  └──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Variants & Intents
- `inline` (Default): Embedded within running text; underlined on hover (or persistent underline in high contrast) to distinguish from surrounding body text without relying solely on color.
- `standalone`: Independent navigation links in headers, footers, or sidebars; includes optional leading or trailing arrow icons.
- `muted`: Secondary gray navigation links (`color.text.secondary`) for footer legal items.

---

## 6. Sizes
- Matches the typography scale: `sm` (14px), `base` (16px default), `lg` (20px).

---

## 7. States
- `default`: High-contrast brand or primary text color.
- `hover`: Text decoration underline + brand color shift (`brand.700`).
- `focus`: 2px high-visibility `FocusRing` (`:focus-visible`).
- `visited`: Subtle color shift where route history is semantically useful.

---

## 8. Slots
- `children`: Mandatory text content.
- `external`: Boolean. When true, appends an external link icon and sets `target="_blank"` with `rel="noopener noreferrer"`.

---

## 9. Behavior & Interaction
- Left-click triggers route change.
- `Ctrl+Click` / `Cmd+Click` opens in a new tab natively.

---

## 10. Keyboard Interaction
- `Tab` moves focus to the link.
- `Enter` activates the link.

---

## 11. Accessibility Guarantees
- Renders native `<a href="...">`.
- External links include screen-reader notice: `<VisuallyHidden>(opens in a new window)</VisuallyHidden>`.
- Satisfies WCAG 1.4.1 (Use of Color): Links do not rely solely on color to convey affordance; they use underlined styling on hover/focus.

---

## 12. Responsive Behavior
- Inline links wrap naturally with parent text without clipping.

---

## 13. Motion & Transitions
- Instant or subtle 150ms color transition.

---

## 14. Token Mapping Hierarchy
- Color: `color.brand.600` (hover `color.brand.700`), or `color.text.primary`.
- Focus Ring: `color.focus.ring`.

---

## 15. Composition Rules
- Use inside `Text` or `Paragraph` for inline citations.
- Use inside `Inline` or `Stack` for breadcrumb or navigation lists.

---

## 16. AI Usage Rules
- **NEVER RENDER DEAD LINKS:** An `href` must always be provided. Never use `href="#"` or `href="javascript:void(0)"`. If no URL exists, use `Button(intent="ghost")`.
