# MDS Primitive: Inline
**Document Layer:** 03-Primitives / Layout  
**Status:** APPROVED (Phase 4 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Purpose

The **Inline** primitive manages one-dimensional horizontal layout. It distributes items side-by-side with uniform horizontal gaps, enforcing the **Parent-Owned Spacing Invariant** without child margins, and follows the document's logical inline axis (`inline-start` to `inline-end`), allowing items to flow naturally along the reading direction under both LTR and RTL without altering DOM sequence or keyboard focus order.

---

## 2. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ ┌─────────┐   gap (space.inline.*)   ┌─────────┐   gap      │
│ │ Child A │ ◄──────────────────────► │ Child B │ ◄────────► │
│ └─────────┘                          └─────────┘            │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. API & Supported Properties

| Property | Type | Default | Values / Description | Token Mapping |
| :--- | :--- | :--- | :--- | :--- |
| `gap` | `enum` | `'md'` | `'xs'` (4px), `'sm'` (8px), `'md'` (16px), `'lg'` (24px) | `space.inline.xs` to `space.inline.lg` |
| `align` | `enum` | `'center'` | `'start'`, `'center'`, `'end'`, `'baseline'`, `'stretch'` | — |
| `justify` | `enum` | `'start'` | `'start'`, `'center'`, `'end'`, `'space-between'`, `'space-around'` | — |
| `wrap` | `boolean` | `false` | When true, items wrap to the next line (consider `Cluster` if 2D gaps needed) | — |
| `collapseBelow`| `enum` | `null` | `'sm'`, `'md'`, `'lg'` (recomposes from horizontal row into vertical `Stack`) | — |
| `as` | `string` | `'div'` | Semantic tag (`'div'`, `'nav'`, `'header'`, `'footer'`) | — |

---

## 4. Composition Rules

- **Children:** Icons paired with labels, action button pairs, card headers (title + icon), pagination controls.
- **Zero Child Margins:** Children must NOT apply physical `margin-left` or `margin-right`.
- **Vertical Alignment Parity:** Default `align="center"` ensures icons and text align optically without line-height jitter.

---

## 5. Variants

1. **Tight Inline (`gap="xs"`):** Icon + text label pairing, status indicator dot + label.
2. **Standard Inline (`gap="sm"` or `"md"`):** Button groups, card action footers, breadcrumb navigation.
3. **Justified Split Inline (`justify="space-between"`):** Modal header (title on start, close button on end), card headers.
4. **Baseline Inline (`align="baseline"`):** Metric values paired with secondary currency or percent symbols.

---

## 6. Responsive Behavior: "Recomposition over Shrinking"

- Through `collapseBelow="sm"` or `"md"`, `Inline` automatically shifts from a horizontal row (`flex-direction: row`) to a vertical `Stack` (`flex-direction: column`) on constrained screens, rather than shrinking button labels or truncating action text.

---

## 7. RTL & Internationalization Architecture

### 7.1 Logical Axis Progression vs. DOM Order Invariants
- `Inline` relies entirely on native document directionality (`dir="rtl"` vs `dir="ltr"`).
- In CSS Flexbox (`flex-direction: row`), items progress along the **inline axis** (`inline-start` $\to$ `inline-end`):
  - In **LTR**, `inline-start` is physically on the left, advancing rightward.
  - In **RTL**, `inline-start` is physically on the right, advancing leftward.
- **The DOM Order Invariant:** The sequence of child elements in the DOM tree remains completely identical in both LTR and RTL. There is zero DOM reordering.

### 7.2 Why `flex-direction: row-reverse` is Strictly Forbidden
- Using `row-reverse` in RTL is an anti-pattern. It visually reverses elements while leaving DOM order unchanged, creating a catastrophic divergence between **visual reading order** and **keyboard focus traversal order**.
- This directly violates **WCAG 2.1/2.2 SC 2.4.3 (Focus Order)**: a user pressing `Tab` would experience focus jumping backwards across the visual row.
- `Inline` strictly maintains `flex-direction: row` and allows the browser's native directionality engine to handle inline-axis progression.

### 7.3 Conceptual Directionality Scenarios

1. **Scenario A: Action Button `[Icon] [Label]`**
   - **LTR:** Visual order is `[Icon]` (left) $\to$ `[Label]` (right). DOM order is `Child 1: Icon`, `Child 2: Label`.
   - **RTL:** Visual order is `[Icon]` (right) $\to$ `[Label]` (left). DOM order is `Child 1: Icon`, `Child 2: Label`.
   - **Result:** The icon naturally leads the label along the reading vector in both writing systems without DOM mutations.

2. **Scenario B: Navigation / Continuation `[Label] [Arrow]`**
   - **LTR:** Visual order is `[Label]` (left) $\to$ `[Arrow →]` (right). DOM order is `Child 1: Label`, `Child 2: Arrow`.
   - **RTL:** Visual order is `[Label]` (right) $\to$ `[Arrow ←]` (left). DOM order is `Child 1: Label`, `Child 2: Arrow`.
   - **Result:** The directional icon (`Tier 1 Directional`) mirrors per the MDS Icon Contract, pointing in the forward reading direction (`←` in RTL), following the label.

3. **Scenario C: Mixed Arabic & Latin Text**
   - Mixed-script strings maintain strict bidirectional isolation (`unicode-bidi: isolate` / `<bdi>`).
   - The primary `Inline` container flows from `inline-start` (right in Arabic). When a Latin brand or code token is encountered, the Latin segment reads LTR internally without disrupting the horizontal inline flow of surrounding elements.

4. **Scenario D: Mixed Numeric + Arabic + Latin (Data & Financial Badges)**
   - Numerals within currency blocks or counters retain standard mathematical left-to-right digit sequence (e.g. `1,450.50 EGP`), while the parent `Inline` items progress along the RTL inline axis.
   - Using `<Numeric>` with `tnum` guarantees stable glyph widths and prevents layout shifts.

---

## 8. Accessibility Guarantees

- When wrapping interactive elements, `Inline` preserves natural focus traversal order (`Tab` moves sequentially in reading direction).
- When configured with `as="nav"`, it exposes proper ARIA navigation landmark semantics.

---

## 9. Tokens Consumed

- `space.inline.xs` (`space.scale.1` = 4px)
- `space.inline.sm` (`space.scale.2` = 8px)
- `space.inline.md` (`space.scale.4` = 16px)
- `space.inline.lg` (`space.scale.6` = 24px)

---

## 10. Anti-Patterns (Forbidden Usage)

- ❌ Using physical margins: `margin-right: 8px;` (breaks in RTL interfaces).
- ❌ Using `Inline` for multi-row chip/tag clouds that need 2D vertical wrap spacing (use `Cluster`).
- ❌ Forcing elements to stay horizontal on 320px mobile screens until text clips (use `collapseBelow="sm"`).

---

## 11. AI Usage Rules

- **WHEN TO USE:** For horizontal element placement where elements belong to the same logical row (e.g., Icon + Label, Confirm + Cancel buttons, Header title + Action).
- **WHEN NOT TO USE:** For wrapping tags (use `Cluster`), 12-column layouts (use `Grid`), or vertical lists (use `Stack`).
- **NEVER OUTPUT:** `margin-left` or `margin-right`. Always wrap elements in `Inline(gap="...")`.
