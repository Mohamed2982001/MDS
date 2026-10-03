# MDS Component: Tooltip

**Document Layer:** 04-Components / Overlays  
**Status:** SPECIFIED (Phase 5 Architectural Specification)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-16  

> [!NOTE]
> **Implementation Scope Notice:** Tooltip is specified but not implemented in the current Phase 5 implementation. Its micro-copy constraint, non-essential status, and assistive technology relationship (`aria-describedby`) are architecturally codified here for downstream implementation.

---

## 1. Purpose
The **Tooltip** component provides brief, non-essential contextual micro-copy that appears when a user hovers over or focuses an interactive element.

---

## 2. When to Use
- To clarify the secondary function of an icon button (e.g. "Edit settings", "Bookmark").
- To provide keyboard shortcut hints (e.g. "Search (Ctrl+K)").

---

## 3. When Not to Use
- **NEVER PUT ESSENTIAL INFORMATION IN TOOLTIPS:** Form validation instructions, legal notices, or critical instructions must be visible in the page body, not hidden behind a hover state.
- **NEVER PUT INTERACTIVE ELEMENTS IN TOOLTIPS:** If a tooltip needs buttons or links, use a `Popover` or `Dialog` instead.

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ Tooltip Surface (Surface.floating + Radius.xs + Elev.lvl2)  │
│  ├── Text: Caption (font.size.xs: 12px)                     │
│  └── Optional Keyboard Shortcut Tag                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Positions
- `top` (Default), `bottom`, `start` (`inline-start`), `end` (`inline-end`).
- Automatically flips if close to viewport boundaries.

---

## 6. Delay & Dismissal Laws
- Display Delay: **300ms** intentional hover delay to prevent flashing while moving mouse across the screen.
- Dismissal: Instantly hides when the trigger loses focus or the pointer leaves, or when `Escape` is pressed.

---

## 7. Keyboard & Touch Interaction
- **Keyboard:** Visible instantly when trigger receives keyboard focus (`:focus-visible`).
- **Touch Viewports:** Tapping the element shows the tooltip briefly, or long-pressing reveals it without navigating.
- **Escape Key:** Pressing `Escape` closes the tooltip without moving focus away from the trigger element.

---

## 8. Accessibility Guarantees
- Trigger applies `aria-describedby="tooltip-id"`.
- Tooltip container applies `role="tooltip"` with matching `id`.
- Does NOT steal keyboard focus.

---

## 9. Motion & Transitions
- 150ms (`motion.fast`) subtle scale (0.95 $\to$ 1.0) and opacity fade.
- Collapses to 0ms on reduced motion.

---

## 10. Token Mapping Hierarchy
- Surface: `color.surface.raised` or dark contrast fill (`color.neutral.900`).
- Text: `color.text.inverse` (white on dark) or `color.text.primary`.
- Radius: `radius.xs` (4px).
- Elevation: `elevation.level2`.

---

## 11. AI Usage Rules
- **NEVER HIDE CRITICAL DATA:** If information is required to complete a task, place it as visible helper text, never in a tooltip.
