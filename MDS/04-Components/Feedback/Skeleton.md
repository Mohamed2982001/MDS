# MDS Component: Skeleton

**Document Layer:** 04-Components / Feedback  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **Skeleton** component displays a temporary placeholder structure that reserves or approximates the expected content structure and can help reduce layout shifts when dimensions match the eventual content while data loads.

---

## 2. When to Use
- During initial page loading or view navigation when the expected layout structure is known (e.g. user profiles, card lists, tables).
- To preserve layout geometry during asynchronous data fetching.

---

## 3. When Not to Use
- For immediate instant micro-actions (e.g. button click): Use `Button(loading)` or `Spinner`.
- For unpredictable or dynamic freeform content.

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ Skeleton Placeholder (Surface + Subtle Shimmer Gradient)    │
│  ├── Shape: 'text', 'circular', 'rectangular'               │
│  ├── Background: neutral.100 (Light) / neutral.800 (Dark)   │
│  └── Shimmer: Linear gradient sweep                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Variants & Shapes
- `text`: Rounded pill mimicking text lines (height matches font line-height, width configurable, e.g. 60%, 80%, 100%).
- `circular`: Circle for avatars and user profile pictures (`radius.full`).
- `rectangular`: Rounded rectangle for cards, images, charts, and banner placeholders (`radius.md`).

---

## 6. Sizes
- `height`: Matches standard tokens or custom pixel values (`16px`, `24px`, `40px`, `120px`).
- `width`: Fluid (e.g. `100%`) or fixed width.

---

## 7. Accessibility & Reduced Motion
- Applies `aria-hidden="true"` to prevent screen readers from reading empty meaningless placeholder boxes.
- Parent container applies `aria-busy="true"`.
- **Reduced Motion Law:** Under `prefers-reduced-motion: reduce`, the sweeping shimmer gradient animation is completely disabled; the skeleton renders as a static muted placeholder.

---

## 8. Motion Specification
- Shimmer Sweep: Linear gradient translation across 1500ms cycle.
- Easing: Linear.

---

## 9. Token Mapping Hierarchy
- Base Color: `color.neutral.100` (Light) / `color.neutral.800` (Dark).
- Shimmer Highlight: `color.neutral.50` (Light) / `color.neutral.700` (Dark).
- Radius: `radius.xs` (text lines) / `radius.md` (cards) / `radius.full` (avatars).

---

## 10. Composition Rules
- Compose multiple `Skeleton` components inside `Stack` or `Inline` to recreate exact page card hierarchies.

---

## 11. AI Usage Rules
- **REPLACE EMPTY TEXT:** Never show blank cards or "Loading..." text when a structured card skeleton can be composed.
