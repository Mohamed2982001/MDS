# MDS Component: Card

**Document Layer:** 04-Components / Data Display  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **Card** component groups related content, media, actions, and metadata into a visually distinct, structured surface plane.

---

## 2. When to Use
- To display discrete content items in a grid or dashboard (e.g. project cards, product summaries, analytics widgets).
- To visually partition complex view sections.

---

## 3. When Not to Use
- For simple horizontal divider lists: Use `Stack(dividers=true)`.
- For full-page modal dialogs: Use `Dialog`.

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ Card (Surface + Radius.md + Depth Triad + Padding)          │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Header Slot (Inline: Title + Icon / Action)             │ │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ Body Slot (Stack: Paragraphs, Media, Data metrics)      │ │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ Footer Slot (Inline: Action Buttons, Timestamps)        │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Variants & Depth Levels
- `flat` (Default): Resting plane on canvas, subtle 1px border (`border.subtle`), zero shadow (`elevation.level0`).
- `raised`: Resting elevated surface, subtle 1px border + soft ambient shadow (`elevation.level1`).
- `interactive`: Flat or raised card that responds to hover and click (elevates to `elevation.level2`, darkens border, handles keyboard `Enter`).

---

## 6. Sizes & Padding
- `sm`: 12px padding (`space.3`).
- `md` (Default): 16px padding (`space.4`).
- `lg`: 24px padding (`space.6`).

---

## 7. States
- Resting, hover (interactive cards), focus (`FocusRing` around card boundary on `:focus-visible`).

---

## 8. Slots
- `header`: Title, subtitle, and optional header action button.
- `children`: Primary body content.
- `footer`: Action buttons or metadata footer.

---

## 9. Accessibility Guarantees
- If interactive, applies `role="region"` or `role="button"` with keyboard activation.
- Does not trap keyboard focus.

---

## 10. Responsive Behavior
- Width is fluid (100% of parent grid cell or container column).
- In multi-column grids, card headers and footers adapt seamlessly across mobile (single column) and desktop (3–4 columns).

---

## 11. Motion & Transitions
- Elevation lift on hover: 150ms (`motion.fast`) with standard deceleration curve.

---

## 12. Token Mapping Hierarchy
- Surface: `color.surface.default` (Light) / `color.neutral.900` (Dark).
- Border: `color.border.default`.
- Radius: `radius.md` (10px default; 6px in Refined preset).
- Elevation: `elevation.level1` or `level0`.

---

## 13. Composition Rules
- Compose cards inside a 12-column `Grid` or `Grid(autoTiles=true)`.

---

## 14. AI Usage Rules
- **ZERO EXTERNAL MARGINS:** Never add margins to a `Card`. Use `Grid(gap="md")` or `Stack(gap="md")` to space multiple cards.
