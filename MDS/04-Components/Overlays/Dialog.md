# MDS Component: Dialog (Modal)

**Document Layer:** 04-Components / Overlays  
**Status:** SPECIFIED (Phase 5 Architectural Specification)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-16  

> [!NOTE]
> **Implementation Scope Notice:** Dialog is specified but not implemented in the current Phase 5 implementation. Its complete interaction lifecycle, focus trap algorithm, and ARIA requirements are architecturally codified here for downstream implementation.

---

## 1. Purpose
The **Dialog** component renders a high-priority modal overlay that captures user focus to confirm critical decisions, display urgent notifications, or collect required task inputs before continuing.

---

## 2. When to Use
- To confirm destructive or irreversible actions (e.g. "Delete Project").
- For focused multi-step tasks that require completion before returning to the main workflow.
- For critical system interruption notices.

---

## 3. When Not to Use
- For simple informational hints: Use `Tooltip` or `Alert`.
- For non-modal secondary content: Use an inline collapsible section or drawer.

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ Backdrop Scrim (rgba(15, 23, 42, 0.6), blur 4px)            │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Dialog Window (FocusTrap + Surface.overlay + Elev.lvl3) │ │
│ │  ┌───────────────────────────────────────────────────┐  │ │
│ │  │ Header Slot (Inline: Title + Close IconButton)    │  │ │
│ │  ├───────────────────────────────────────────────────┤  │ │
│ │  │ Body Slot (Stack: Message / Form Fields)          │  │ │
│ │  ├───────────────────────────────────────────────────┤  │ │
│ │  │ Footer Slot (Inline: Cancel + Confirm Buttons)    │  │ │
│ │  └───────────────────────────────────────────────────┘  │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Sizes & Width Constraints
- `sm`: Max-width 400px (Confirmations).
- `md` (Default): Max-width 560px (Standard forms).
- `lg`: Max-width 720px (Complex multi-field dialogs).
- Fullscreen / Bottom Sheet on mobile viewports $< 480\text{px}`.

---

## 6. Focus & Interaction Lifecycle
1. **Trigger:** User clicks trigger button (e.g. "Delete").
2. **Mount & Inert:** Dialog renders; backdrop scrim activates; background document marked `inert` (or `aria-hidden="true"`).
3. **Focus Trap:** Focus automatically moves into the dialog (`FocusTrap` active).
4. **Interaction:** `Tab` loops strictly inside dialog elements; `Escape` key triggers dismissal.
5. **Unmount & Return:** On close, focus returns precisely to the trigger element that opened the dialog.

---

## 7. Slots
- `title`: Mandatory heading (renders semantic `<h2>` or `<h3>`).
- `children`: Body content (paragraphs, forms).
- `footer`: Action buttons (typically `[Cancel (secondary)]` + `[Confirm (primary or destructive)]`).

---

## 8. Accessibility Guarantees
- Container applies `role="dialog"`, `aria-modal="true"`, and `aria-labelledby="dialog-title"`.
- Focus is trapped strictly within the modal container.
- Close button embeds `<VisuallyHidden>Close dialog</VisuallyHidden>`.

---

## 9. Responsive Behavior ("Recomposition over Shrinking")
- On viewports $< 480\text{px}`:
  - Dialog window recomposes into a **Bottom Sheet** anchored to the viewport bottom.
  - Action footer buttons recompose from horizontal `Inline` to vertical full-width `Stack`.

---

## 10. Motion & Transitions
- Backdrop fade: 150ms (`motion.fast`).
- Dialog scale & slide: 250ms (`motion.normal`) with `motion.ease.enter`.
- Under `prefers-reduced-motion: reduce`, all transitions collapse to 0ms instant display.

---

## 11. Token Mapping Hierarchy
- Surface: `color.surface.overlay` (`color.neutral.0` / `neutral.900` in Dark Mode).
- Elevation: `elevation.level3` (12px/16px ambient shadow).
- Radius: `radius.lg` (14px).
- Backdrop: `rgba(15, 23, 42, 0.6)`.

---

## 12. Composition Rules
- Always compose `FocusTrap` primitive directly around dialog window interior.

---

## 13. AI Usage Rules
- **ALWAYS RETURN FOCUS:** An AI agent must ensure the trigger element ref is preserved to restore focus upon dialog close.
- **DESTRUCTIVE CONFIRMATIONS:** Use specific consequence language (e.g. "Permanently delete database?"), never generic "Are you sure?".
