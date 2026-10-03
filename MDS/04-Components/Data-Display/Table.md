# MDS Component: Table

**Document Layer:** 04-Components / Data Display  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **Table** component organizes and displays structured datasets across rows and columns, providing clear visual alignment, row separation, sorting indicators, and tabular numeric alignment.

---

## 2. When to Use
- To display tabular datasets (e.g. transactions, user lists, orders, financial metrics).
- When data items share the same attribute schema.

---

## 3. When Not to Use
- For general page layouts: Use `Grid` instead.
- For complex enterprise spreadsheets (in-cell editing, cell formulas, column freeze): Use a specialized DataGrid (deferred per Section 11 & 34).

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ Table Container (Horizontal Scroll Containment + Border)    │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ <table> Element                                         │ │
│ │  ┌───────────────────────────────────────────────────┐  │ │
│ │  │ <thead> (Column Headers, th, align="start")       │  │ │
│ │  ├───────────────────────────────────────────────────┤  │ │
│ │  │ <tbody>                                           │  │ │
│ │  │  ├── <tr> Row 1 (td cells, divider border.subtle) │  │ │
│ │  │  ├── <tr> Row 2 (alternate row zebra shading)     │  │ │
│ │  │  └── <tr> Row 3 (Numeric columns: tnum right-align)│ │
│ │  └───────────────────────────────────────────────────┘  │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Variants & Features
- `striped`: Alternates background shading on even rows (`color.surface.canvas`) for dense scanability.
- `bordered`: Includes vertical column dividers in addition to horizontal row dividers.
- `compact`: Reduces row vertical padding (8px instead of 12px) for high-density data views.

---

## 6. Sizing & Cell Padding
- Standard Density: 12px padding block, 16px padding inline.
- Compact Density: 8px padding block, 12px padding inline.

---

## 7. Column Alignment Laws
- **Text Columns:** Aligns to `inline-start` (right in Arabic, left in English).
- **Numeric Columns:** Strictly right-aligned (`text-align: end`), with `font-variant-numeric: tabular-nums` (`tnum`) to ensure decimal points and digits align vertically.
- **Status / Action Columns:** Center-aligned or `inline-end`.

---

## 8. Slots & Composition
- `columns`: Header definitions (`key`, `label`, `align`, `sortable`).
- `data`: Array of row records.
- `emptyState`: Custom component rendered when data array is empty.

---

## 9. Accessibility Guarantees
- Semantic HTML: `<table>`, `<thead>`, `<tbody>`, `<th> scope="col"`, `<td>`.
- Accessible Name: Wrapped with `aria-label` or `<caption>`.
- Sortable headers expose `aria-sort="ascending | descending | none"`.

---

## 10. Responsive Behavior ("Recomposition over Truncation")
- Table container provides smooth horizontal scrolling (`overflow-x: auto`) with visual scroll fade indicators on mobile viewports.
- Cell text never truncates with ellipsis; columns wrap or table scrolls cleanly.

---

## 11. Token Mapping Hierarchy
- Surface: `color.surface.default`.
- Header Fill: `color.surface.raised`.
- Dividers: `color.border.subtle` (1px).
- Numeric Figures: `font-variant-numeric: tabular-nums`.

---

## 12. AI Usage Rules
- **NEVER HARDCODE COLUMN WIDTHS IN PIXELS:** Allow table columns to size naturally or use relative percentages.
- **NUMERIC COLUMNS:** Always right-align numeric data columns and wrap cells in `<Numeric>`.
