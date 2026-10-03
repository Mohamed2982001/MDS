# MDS Primitive: Container
**Document Layer:** 03-Primitives / Layout  
**Status:** APPROVED (Phase 4 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Purpose

The **Container** primitive establishes the outer horizontal boundaries of the page or viewport region. It centers content horizontally and provides responsive, fluid padding to prevent content from touching the screen edges while constraining reading line lengths.

---

## 2. Anatomy

```text
┌───────────────────────────────────────────────────────────────┐
│ Viewport Canvas                                               │
│   ← padding.inline → ┌───────────────────────┐ ← padding.inline →
│                      │ Container Max-Width   │                │
│                      │ (Centered Content)    │                │
│                      └───────────────────────┘                │
└───────────────────────────────────────────────────────────────┘
```

---

## 3. API & Supported Properties

| Property | Type | Default | Values / Description | Token Mapping |
| :--- | :--- | :--- | :--- | :--- |
| `size` | `enum` | `'standard'` | `'standard'` (1152px), `'wide'` (1440px), `'full'` (100%) | `container.lg`, `container.xl` |
| `padding` | `boolean \| enum` | `true` | Responsive gutters: Mobile (16px), Tablet (24px), Desktop (32px) | `space.4`, `space.6`, `space.8` |
| `center` | `boolean` | `true` | Automatically centers horizontally via auto inline margins | — |
| `as` | `string` | `'div'` | Semantic tag (`'div'`, `'main'`, `'section'`, `'article'`) | — |

---

## 4. Composition Rules

- **Top-Level Root Container:** Nest page-level layout primitives (`Stack`, `Grid`) directly inside `Container`.
- **Nesting Boundary:** Never nest a `Container` directly inside another `Container` unless creating an intentionally constrained nested column.
- **Parent-Owned Spacing:** `Container` owns the outer horizontal page gutter; children inside must not apply outer negative margins (unless intentionally using a `Bleed` pattern).

---

## 5. Variants

1. **Standard (`size="standard"`):** Constrained to **1152px** (`container.lg`). Default for forms, articles, marketing pages, and general SaaS workflows to preserve 65–75 CPL readability.
2. **Wide (`size="wide"`):** Constrained to **1440px** (`container.xl`). For high-throughput analytics dashboards, data grids, and multi-column workspaces.
3. **Full (`size="full"`):** 100% width with fluid responsive edge padding preserved.

---

## 6. Responsive Behavior

| Viewport Tier | Min Width | Max Container Width | Horizontal Gutter |
| :--- | :---: | :---: | :---: |
| **Mobile (`sm`)** | 320px | 100% | 16px (`space.4`) |
| **Tablet (`md`)** | 768px | 100% | 24px (`space.6`) |
| **Desktop (`lg`)** | 1024px | 1152px (`container.lg`) | 32px (`space.8`) |
| **Wide (`xl`)** | 1440px | 1440px (`container.xl`) | 48px (`space.12`) |

---

## 7. RTL & Internationalization

- Uses `margin-inline: auto` for centering.
- Uses `padding-inline: var(--gutter)` for fluid edge gutters, guaranteeing identical optical symmetry in both LTR and RTL layouts.

---

## 8. Accessibility Guarantees

- When configured with `as="main"`, it provides landmark role `<main>` for assistive screen readers.
- Prevents horizontal layout overflow and unconstrained stretching, which disorients users with low vision or cognitive impairments.

---

## 9. Token Consumed

- `space.scale.4` (16px mobile gutter)
- `space.scale.6` (24px tablet gutter)
- `space.scale.8` (32px desktop gutter)
- `space.scale.12` (48px wide page gutter)

---

## 10. Anti-Patterns (Forbidden Usage)

- ❌ Hardcoding pixel widths: `width: 1200px;` (violates approved 1152px standard).
- ❌ Zero gutters on mobile: Removing padding causing text to clip the screen edge.
- ❌ Adding vertical margins to `Container`: Spacing between sections must be managed by page-level `Stack`.

---

## 11. AI Usage Rules

- **WHEN TO USE:** Every application view, marketing page, or full-width section header MUST wrap its content in `Container`.
- **WHEN NOT TO USE:** Inside small isolated components like buttons, dropdown popovers, or modal sheets.
- **EXISTING ALTERNATIVES:** If unconstrained horizontal bleed is required, use `size="full"` instead of removing `Container`.
