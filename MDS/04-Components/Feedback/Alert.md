# MDS Component: Alert

**Document Layer:** 04-Components / Feedback  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **Alert** component displays prominent, contextual feedback messages at the page or section level to inform users about system status, successful actions, warnings, or critical errors.

---

## 2. When to Use
- To notify users of important outcomes (e.g. "Order placed successfully", "Payment failed", "Profile updated").
- To display persistent system warnings (e.g. "Maintenance scheduled in 10 minutes").

---

## 3. When Not to Use
- For field-level form validation errors: Use `Field`'s `errorMessage` instead.
- For transient toast notifications that disappear automatically: Use toast notifications (Phase 5.5).

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ Alert Box (Surface + 1px Border + Radius.md + Padding.4)    │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Inline Primitive (gap="md", align="start")              │ │
│ │  ┌──────────────┐  ┌──────────────────────────────────┐ │ │
│ │  │ Status Icon  │  │ Stack Primitive (gap="xs")       │ │ │
│ │  │ (20 × 20px)  │  │  ├── Title (Heading 6 / Bold)    │ │ │
│ │  │              │  │  └── Description (Text / softWrap)│ │
│ │  └──────────────┘  └──────────────────────────────────┘ │ │
│ │  ┌──────────────┐                                       │ │
│ │  │ Close Button │                                       │ │
│ │  │ (IconButton) │                                       │ │
│ │  └──────────────┘                                       │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Variants & Semantic Intents

| Intent | Icon | Background Fill | Border Color | Text & Icon Color | WCAG Contrast |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `info` | ℹ️ Info circle | `color.palette.blue.50` | `color.palette.blue.200` | `color.palette.blue.600` | $\ge 4.5:1$ (AA) |
| `success` | ✓ Check circle | `color.palette.green.50` | `color.palette.green.200` | `color.palette.green.600` | $\ge 4.5:1$ (AA) |
| `warning` | ⚠️ Alert triangle | `color.palette.amber.50` | `color.palette.amber.200` | `color.palette.amber.600` | $\ge 4.5:1$ (AA) |
| `danger` | ✕ Alert octagon | `color.palette.red.50` | `color.palette.red.200` | `color.palette.red.600` | $\ge 4.5:1$ (AA) |

---

## 6. Sizes
- Inherent layout padding: 16px (`space.4`).

---

## 7. States
- `visible`: Resting display state.
- `dismissed`: Removed from DOM upon clicking dismiss button.

---

## 8. Slots
- `title`: Optional bold headline.
- `children`: Mandatory detailed descriptive text (`softWrap: true`).
- `action`: Optional inline recovery button (e.g. "Retry", "View Details").
- `onDismiss`: Optional callback enabling the dismiss icon button.

---

## 9. Behavior & Dismissal
- When dismissed, `Alert` smoothly unmounts without abrupt layout collapse.

---

## 10. Keyboard Interaction
- If `onDismiss` is present, `Tab` focuses the close `IconButton`. `Enter` or `Space` activates dismissal.

---

## 11. Accessibility Guarantees
- Container applies `role="alert"` for critical `danger` alerts, or `role="status"` for `info`/`success` notices.
- Does not steal keyboard focus from current user flow.
- Close button embeds `<VisuallyHidden>Dismiss alert</VisuallyHidden>`.

---

## 12. Responsive & RTL Behavior
- In RTL, status icon sits at `inline-start` (right) and dismiss button sits at `inline-end` (left).
- Descriptive text wraps naturally across multiple lines (`softWrap: true`).

---

## 13. Motion & Transitions
- Fade and collapse transition: 250ms (`motion.normal`). Collapses to 0ms when reduced motion is preferred.

---

## 14. Token Mapping Hierarchy
- Uses semantic feedback palette (`palette.[color].50` bg, `palette.[color].200` border, `palette.[color].600` text).
- Radius: `radius.md` (10px default).

---

## 15. Composition Rules
- Place at top of page body or within modal content headers.

---

## 16. AI Usage Rules
- **CRITICAL ERRORS:** Use `intent="danger"` and `role="alert"` for unrecoverable API or validation errors.
- **NO ELLIPSIS:** Never truncate alert message body copy.
