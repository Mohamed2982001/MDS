# MDS Primitive: Cluster
**Document Layer:** 03-Primitives / Layout  
**Status:** APPROVED (Phase 4 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Purpose

The **Cluster** primitive manages collections of variable-width elements that flow horizontally and wrap naturally onto multiple lines. It provides identical, token-controlled horizontal and vertical gaps between wrapping items, eliminating legacy CSS margin hacks.

---

## 2. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ ┌─────────┐ ◄-gap-► ┌───────────────┐ ◄-gap-► ┌───────────┐ │
│ │ Tag 1   │         │ Filter Chip 2 │         │ Badge 3   │ │
│ └─────────┘         └───────────────┘         └───────────┘ │
│ ↕ gap (uniform)                                             │
│ ┌───────────────────────┐ ◄-gap-► ┌─────────┐               │
│ │ Longer Filter Item 4  │         │ Tag 5   │               │
│ └───────────────────────┘         └─────────┘               │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. API & Supported Properties

| Property | Type | Default | Values / Description | Token Mapping |
| :--- | :--- | :--- | :--- | :--- |
| `gap` | `enum` | `'sm'` | Uniform 2D gap: `'xs'` (4px), `'sm'` (8px), `'md'` (16px) | `space.scale.1`, `2`, `4` |
| `align` | `enum` | `'center'` | `'start'`, `'center'`, `'end'`, `'baseline'` | — |
| `justify` | `enum` | `'start'` | `'start'`, `'center'`, `'end'`, `'space-between'` | — |
| `as` | `string` | `'div'` | Semantic tag (`'div'`, `'ul'`, `'nav'`) | — |

---

## 4. Composition Rules

- **Children:** Badges, tags, filter chips, metadata pills, button groups.
- **Zero Child Margins:** Items must not apply `margin-right` or `margin-bottom`.
- **Contrast with `Inline`:** Use `Inline` when wrapping is forbidden or when horizontal/vertical gaps must differ; use `Cluster` when wrapping onto multiple lines is expected and normal.

---

## 5. Variants

1. **Tight Cluster (`gap="xs"` = 4px):** Micro status tags, inline keyword pills, rating stars.
2. **Standard Cluster (`gap="sm"` = 8px):** Category filters, search filter chips, product option badges.
3. **Action Cluster (`gap="md"` = 16px):** Dialog action button arrays, social share icon groups.

---

## 6. Responsive Behavior

- Elements wrap automatically when the container width shrinks.
- No media queries are needed: content responds purely to container boundaries.

---

## 7. RTL & Internationalization

- Natively flows from `inline-start` to `inline-end`:
  - In LTR: items fill from left to right, wrapping downwards.
  - In RTL: items fill from right to left, wrapping downwards.

---

## 8. Accessibility Guarantees

- Preserves sequential keyboard focus flow (`Tab`) across all wrapped items.
- When `as="ul"`, it provides valid list semantics for filter collections.

---

## 9. Tokens Consumed

- `space.scale.1` (4px tight gap)
- `space.scale.2` (8px standard tag gap)
- `space.scale.4` (16px action button gap)

---

## 10. Anti-Patterns (Forbidden Usage)

- ❌ Adding `margin-bottom: 8px; margin-right: 8px;` to child tags.
- ❌ Using negative margin wrappers on parents to cancel child margins.
- ❌ Using `Cluster` for full-page layout grids (use `Grid`).

---

## 11. AI Usage Rules

- **WHEN TO USE:** Whenever displaying a group of tags, chips, categories, badges, or button groups that may exceed one line.
- **WHEN NOT TO USE:** When items must stay strictly on a single non-wrapping row (use `Inline`).
