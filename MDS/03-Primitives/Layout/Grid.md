# MDS Primitive: Grid
**Document Layer:** 03-Primitives / Layout  
**Status:** APPROVED (Phase 4 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Purpose

The **Grid** primitive manages two-dimensional responsive layouts. It provides both the canonical **12-column responsive layout grid** and **content-driven auto-fit grids**, enforcing uniform gutters and parent-owned spacing across complex dashboards, forms, and card directories.

---

## 2. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ ┌─────────┐   gutter   ┌─────────┐   gutter   ┌─────────┐   │
│ │ Col 1   │ ◄────────► │ Col 2   │ ◄────────► │ Col 3   │   │
│ └─────────┘            └─────────┘            └─────────┘   │
│ ↕ row gap (space.block.*)                                   │
│ ┌─────────┐            ┌─────────┐            ┌─────────┐   │
│ │ Col 4   │            │ Col 5   │            │ Col 6   │   │
│ └─────────┘            └─────────┘            └─────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. API & Supported Properties

| Property | Type | Default | Values / Description | Token Mapping |
| :--- | :--- | :--- | :--- | :--- |
| `columns` | `number \| object` | `12` | 1–12, or responsive map (`{ sm: 1, md: 2, lg: 3, xl: 4 }`) | — |
| `minItemWidth` | `string` | `null` | Creates auto-fitting grid (e.g. `'280px'`) using `repeat(auto-fit, minmax(...))` | — |
| `gutter` | `enum` | `'responsive'` | Fluid: Mobile (16px), Tablet (24px), Desktop (24px), Wide (32px) | `space.scale.4`, `6`, `8` |
| `rowGap` | `enum` | `'md'` | `'xs'` (4px), `'sm'` (8px), `'md'` (16px), `'lg'` (24px), `'xl'` (32px) | `space.block.*` |
| `as` | `string` | `'div'` | Semantic tag (`'div'`, `'section'`, `'ul'`, `'ol'`) | — |

---

## 4. Composition Rules

- **Children:** `GridItem` wrappers (supporting `colSpan` and `rowSpan`) or direct component tiles (`Card`, `Surface`).
- **Zero Child Margins:** Spacing between grid cells is strictly governed by `gutter` and `rowGap`.
- **Nesting:** Complex dashboard sections combine `Container` $\to$ `Stack` $\to$ `Grid`.

---

## 5. Variants

1. **12-Column Layout Grid (`columns={12}`):** Page-level layouts where items span variable columns (e.g. main content `colSpan={8}`, sidebar `colSpan={4}`).
2. **Auto-Fitting Tile Grid (`minItemWidth="280px"`):** Content-driven grid that automatically wraps cards into fewer or more columns based on available space without brittle media queries.
3. **Uniform Feature Grid (`columns={{ sm: 1, md: 2, lg: 3 }}`):** Equal-width feature columns.

---

## 6. Responsive Behavior

Adheres strictly to the **MDS 12-Column Responsive Standard**:

| Viewport Tier | Min Width | Default Grid Columns | Fluid Gutter |
| :--- | :---: | :---: | :---: |
| **Mobile (`sm`)** | 320px | 4 columns | 16px (`space.scale.4`) |
| **Tablet (`md`)** | 768px | 8 columns | 24px (`space.scale.6`) |
| **Desktop (`lg`)** | 1024px | 12 columns | 24px (`space.scale.6`) |
| **Wide (`xl`)** | 1440px | 12 columns | 32px (`space.scale.8`) |

---

## 7. RTL & Internationalization

- Built on CSS Grid, which natively mirrors column ordering under `dir="rtl"`.
- Column 1 starts at the inline-start edge (right in Arabic, left in English).

---

## 8. Accessibility Guarantees

- **Tab Navigation Flow:** Guarantees that keyboard focus sequentially traverses across rows (row-major) matching visual reading direction.
- Does not use visual reordering (`order` property) that contradicts the DOM tree.

---

## 9. Tokens Consumed

- `space.scale.4` (16px mobile gutter)
- `space.scale.6` (24px tablet/desktop gutter)
- `space.scale.8` (32px wide desktop gutter)
- `space.block.*` (row gaps)

---

## 10. Anti-Patterns (Forbidden Usage)

- ❌ Hardcoding fixed column pixel widths (`grid-template-columns: 300px 300px;`).
- ❌ Using CSS floats or table tags for layout.
- ❌ Applying outer margins on grid items to compensate for missing gutters.

---

## 11. AI Usage Rules

- **WHEN TO USE:** Whenever items form a 2-dimensional grid, dashboard widget collection, or 12-column page layout.
- **WHEN NOT TO USE:** For simple 1-dimensional vertical lists (use `Stack`) or single horizontal rows (use `Inline`).
- **AUTO-FIT RULE:** For card collections, prefer `minItemWidth="280px"` over static breakpoint tables for smoother responsive behavior.
