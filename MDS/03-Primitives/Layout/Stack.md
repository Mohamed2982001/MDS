# MDS Primitive: Stack
**Document Layer:** 03-Primitives / Layout  
**Status:** APPROVED (Phase 4 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Purpose

The **Stack** primitive manages one-dimensional vertical layout. It enforces the **Parent-Owned Spacing Invariant** by distributing uniform vertical gaps between stacked children without requiring children to declare individual outer margins.

---

## 2. Anatomy

```text
┌──────────────────────────────────────┐
│ Child Element A                      │
├──────────────────────────────────────┤
│ ↕ gap (space.block.*)                │
├──────────────────────────────────────┤
│ Child Element B                      │
├──────────────────────────────────────┤
│ ↕ gap (space.block.*)                │
├──────────────────────────────────────┤
│ Child Element C                      │
└──────────────────────────────────────┘
```

---

## 3. API & Supported Properties

| Property | Type | Default | Values / Description | Token Mapping |
| :--- | :--- | :--- | :--- | :--- |
| `gap` | `enum` | `'md'` | `'xs'` (4px), `'sm'` (8px), `'md'` (16px), `'lg'` (32px), `'xl'` (48px) | `space.block.xs` to `space.block.lg` |
| `align` | `enum` | `'stretch'` | `'stretch'`, `'start'`, `'center'`, `'end'` | — |
| `justify` | `enum` | `'start'` | `'start'`, `'center'`, `'end'`, `'space-between'` | — |
| `dividers` | `boolean` | `false` | Inserts subtle 1px divider border between adjacent items | `color.border.subtle` |
| `as` | `string` | `'div'` | Semantic tag (`'div'`, `'section'`, `'form'`, `'ul'`) | — |

---

## 4. Composition Rules

- **Children:** Any primitive or component can be a child of `Stack`.
- **Zero Child Margins:** Children placed within `Stack` must NOT have outer top or bottom margins.
- **Nesting:** `Stack` primitives nest cleanly inside other `Stack` or `Inline` primitives to form complex 2D UI without custom grid hacks.

---

## 5. Variants

1. **Tight Stack (`gap="xs"` or `"sm"`):** Form label + input field, header title + subtitle, badge + count.
2. **Standard Stack (`gap="md"`):** Vertical card feed, form fields in a section, list of options.
3. **Generous Section Stack (`gap="lg"` or `"xl"`):** Spacing between major page sections or modal headers, bodies, and footers.
4. **Centered Stack (`align="center" justify="center"`):** Replaces the need for a separate `Center` primitive.

---

## 6. Responsive Behavior

`gap` accepts responsive breakpoint objects:
- `gap={{ sm: 'sm', lg: 'md' }}` allows vertical gaps to automatically expand on desktop and compact on mobile.

---

## 7. RTL & Internationalization

- Vertical flow direction is naturally script-agnostic.
- Alignment properties (`align="start"`, `align="end"`) map strictly to logical inline alignment (`align-items: flex-start` aligning to inline-start: left in LTR, right in RTL).

---

## 8. Accessibility Guarantees

- **DOM Reading Order:** Enforces DOM order matching visual layout, critical for screen reader navigational order and sequential keyboard focus (`Tab`).
- When `as="ul"`, it cleanly structures lists of interactive items without breaking list semantics.

---

## 9. Tokens Consumed

- `space.block.xs` (`space.scale.1` = 4px)
- `space.block.sm` (`space.scale.2` = 8px)
- `space.block.md` (`space.scale.4` = 16px)
- `space.block.lg` (`space.scale.8` = 32px)
- `color.border.subtle` (Divider fill)

---

## 10. Anti-Patterns (Forbidden Usage)

- ❌ Adding `margin-bottom: 16px;` to a child element inside `Stack`.
- ❌ Using `<br>` or empty `<div>` tags to force vertical spacing.
- ❌ Using `Stack` when elements should sit horizontally (use `Inline`).

---

## 11. AI Usage Rules

- **WHEN TO USE:** Whenever two or more elements are placed vertically above/below each other.
- **WHEN NOT TO USE:** For horizontal rows (use `Inline`), wrapping chip lists (use `Cluster`), or multi-column grids (use `Grid`).
- **RULE:** Never output `margin-top` or `margin-bottom` in component CSS. Always place elements in a `Stack(gap="...")`.
