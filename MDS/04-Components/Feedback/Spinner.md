# MDS Component: Spinner

**Document Layer:** 04-Components / Feedback  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **Spinner** component provides an indeterminate, circular loading indicator to signal that a background operation, data fetch, or mutation is currently underway.

---

## 2. When to Use
- For short, indeterminate loading intervals (under 4 seconds).
- Inside `Button` during async form submissions (`loading={true}`).
- In small cards, inline data cells, or search inputs while querying.

---

## 3. When Not to Use
- When content structure is known and predictable: Use `Skeleton` instead to reserve layout space and reduce potential layout shift.
- When progress can be accurately measured: Use a progress bar instead.

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ Spinner (Circular SVG or CSS border-spinner)                │
│  ├── Outer track: subtle border (2px)                       │
│  └── Active head: brand arc rotating 360°                   │
│  └── VisuallyHidden: "Loading..." accessible name           │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Sizes

| Size | Diameter | Stroke Width | Primary Usage |
| :--- | :---: | :---: | :--- |
| `xs` | **14px** | 1.5px | Inline status badges |
| `sm` | **16px** | 2px | Inside 32px Button |
| `md` | **20px** | 2px | Inside 40px/48px Button |
| `lg` | **32px** | 3px | Section or modal loaders |
| `xl` | **48px** | 4px | Full-page initial data fetch |

---

## 6. Colors
- `brand` (Default): `color.brand.600` arc on subtle track.
- `inverse`: White arc for primary/destructive buttons.
- `neutral`: Muted slate arc for subtle loading indicators.

---

## 7. Accessibility & Reduced Motion
- Embeds `<VisuallyHidden>Loading, please wait...</VisuallyHidden>` and applies `aria-busy="true"`.
- **Vestibular Safety Invariant:** When `prefers-reduced-motion: reduce` is active, spinning rotation is halted; the spinner switches to a gentle, static pulsing opacity or a static "Loading..." text fallback.

---

## 8. Motion Specification
- Continuous 360° rotation: 800ms linear infinite.
- Active arc length: 25% of circumference (90° sweep).

---

## 9. Token Mapping Hierarchy
- Sizing maps to `size.icon.*` scale (`xs` 14px, `sm` 16px, `md` 20px, `xl` 32px).
- Color maps to `color.brand.600` or `color.text.inverse`.

---

## 10. AI Usage Rules
- **BUTTON INTEGRATION:** Do not write custom spinner markup inside buttons; pass `loading={true}` to `Button`.
