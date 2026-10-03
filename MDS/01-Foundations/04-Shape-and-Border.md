# MDS Foundation: Shape, Radius & Border Specification
**Foundational Layer:** 01-Foundations  
**Status:** APPROVED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Aesthetic Rationale: "Refined Softness"

MDS adopts an intentional **Refined Softness** aesthetic:
- It rejects **Brutalist Sharpness** (0px corners everywhere feel aggressive and dated).
- It rejects **Bubble Softness** (24px+ giant radii on standard buttons feel toy-like and waste critical UI space).
- Instead, MDS uses disciplined, subtle curvatures that soften boundaries while maintaining architectural rigor.

---

## 2. Calibrated Radius Scale

| Token | Value (px) | Usage & Contextual Assignment |
| :--- | :---: | :--- |
| `radius.none` | 0px  | Sharp geometric containers, full-bleed header bars, table cells |
| `radius.xs`   | 4px  | Micro chips, nested sub-tags, status indicator dots |
| `radius.sm`   | 6px  | Compact buttons, small badges, Refined Minimal preset controls |
| `radius.md`   | 10px | **Soft Modern Default:** Standard buttons, form fields, card containers |
| `radius.lg`   | 14px | Elevated cards, dropdown menus, context popovers |
| `radius.xl`   | 20px | Modal dialogs, floating action sheets, side panels |
| `radius.full` | 9999px| Fully rounded pills, avatar circles, toggle switches |

---

## 3. Contextual Concentricity for Nested Surfaces

To maintain visual geometric harmony, nested rounded surfaces (such as an inner image preview or highlighted panel nested within a card) should maintain coherent curvature with the parent container:

$$R_{\text{inner}} \approx \max(0, R_{\text{outer}} - \text{Padding})$$

```
┌──────────────────────────────────────────────┐  R_outer = 14px (radius.lg)
│   Padding = 8px                              │
│   ┌──────────────────────────────────────┐   │
│   │                                      │   │  R_inner = 14px - 8px = 6px (radius.sm)
│   └──────────────────────────────────────┘   │
└──────────────────────────────────────────────┘
```

> **Contextual Application:** Concentricity is a geometric design guideline for nested surface fills and structural containers. It does not apply to small standalone interactive elements (e.g. icon buttons or action chips) positioned inside a card, which follow their own component size tokens.

---

## 4. Border Architecture & Width Hierarchy

| Token | Value (px) | Semantic Role & Platform Characteristic |
| :--- | :---: | :--- |
| `border.width.thin`    | 1px   | Standard container boundaries, table row dividers, resting card perimeters |
| `border.width.regular` | 1.5px | **Optical Treatment:** Standard interactive input borders on high-DPI displays |
| `border.width.thick`   | 2px   | High Contrast Mode default, accessibility focus indicator rings |

### 1.5px Optical Precision Note:
`border.width.regular` (1.5px) is an optical treatment calibrated for modern high-density screens (retina displays, high-DPI mobile screens) to provide crisp interactive definition without the heaviness of 2px. On standard 1x displays, platform rendering pipelines snap seamlessly to device boundaries.

### Semantic Border Roles:
- **`color.border.subtle` (neutral.200 Light / neutral.800 Dark):** Table dividers, passive cards.
- **`color.border.default` (neutral.300 Light / neutral.700 Dark):** Standard input fields, resting cards.
- **`color.focus.ring` (brand.600 Light / neutral.1000 High Contrast):** Keyboard navigation focus rings.
