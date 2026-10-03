# MDS Component: Badge & Status

**Document Layer:** 04-Components / Data Display  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **Badge** component displays compact, non-interactive status tags, categories, counts, or metadata markers.

---

## 2. When to Use
- To display state markers (e.g. "Active", "Pending", "Failed", "Completed").
- For category tags and project labels.
- For numerical notification counts or version labels (e.g. "v2.1", "12").

---

## 3. When Not to Use
- For interactive clickable filter tags: Use `Chip` or `Button(intent="ghost")` instead.
- For prominent alert messages: Use `Alert` instead.

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ Badge Pill (Radius.full, Padding 2px 8px, 1px subtle border)│
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Inline Primitive (gap="xs", align="center")             │ │
│ │  ┌──────────────┐  ┌──────────────────────────────────┐ │ │
│ │  │ Optional Dot │  │ Label Text                       │ │ │
│ │  │   or Icon    │  │ (font.size.xs: 12px, weight 500) │ │ │
│ │  └──────────────┘  └──────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Variants & Semantic Intents

| Intent | Background | Border | Text & Dot Color | Typical Usage |
| :--- | :--- | :--- | :--- | :--- |
| `neutral` | `color.neutral.100` | `color.neutral.200` | `color.neutral.700` | Inactive, draft, metadata |
| `brand` | `color.brand.50` | `color.brand.200` | `color.brand.700` | In progress, featured, primary |
| `success` | `color.palette.green.50` | `color.palette.green.200` | `color.palette.green.600` | Active, published, paid, online |
| `warning` | `color.palette.amber.50` | `color.palette.amber.200` | `color.palette.amber.600` | Pending, review required |
| `danger` | `color.palette.red.50` | `color.palette.red.200` | `color.palette.red.600` | Failed, expired, rejected |

---

## 6. Sizes
- `sm`: 18px height (2px padding block, 6px padding inline, 11px text).
- `md` (Default): 22px height (2px padding block, 8px padding inline, 12px text).

---

## 7. States
- Non-interactive by default. If wrapped with an action, inherits interactive focus ring.

---

## 8. Slots
- `dot`: Optional 6px circular status dot on leading edge.
- `icon`: Optional leading icon (14px).
- `children`: Label text or count string.

---

## 9. Accessibility Guarantees
- Contrast ratio between badge text and background exceeds 4.5:1 (WCAG AA).
- Color is not the sole conveyor of meaning: status intent is always paired with explicit text (e.g. "Active", "Offline").

---

## 10. Responsive & RTL Behavior
- Aligns along the logical inline axis (`inline-start` dot/icon $\to$ `inline-end` text).

---

## 11. Token Mapping Hierarchy
- Background: `component.badge.[intent].background`.
- Border: `component.badge.[intent].border`.
- Text: `component.badge.[intent].foreground`.
- Radius: `radius.full`.

---

## 12. Composition Rules
- Compose lists of badges using `Cluster(gap="xs")` to allow seamless multi-row wrapping.

---

## 13. AI Usage Rules
- **NEVER USE FOR PRIMARY BUTTONS:** Badges are display tags, not action triggers.
- **NO RAW COLORS:** Always use semantic intents (`brand`, `success`, etc.), never arbitrary hex tints.
