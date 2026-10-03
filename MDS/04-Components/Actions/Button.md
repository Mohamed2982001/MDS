# MDS Component: Button

**Document Layer:** 04-Components / Actions  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **Button** is the primary interactive trigger for executing user actions, state changes, form submissions, and workflow steps. It acts as the reference component for MDS interaction lifecycles, states, and accessibility standards.

---

## 2. When to Use
- To trigger an action or business operation (e.g. "Save", "Submit", "Delete", "Add Item").
- To trigger dialogs, popovers, or modal sheets.
- For form action bars and toolbar controls.

---

## 3. When Not to Use
- **Do NOT use for page navigation:** Use `Link` instead when changing URLs or navigating between views.
- **Do NOT use for standalone icons without text:** Use `IconButton` instead to guarantee screen-reader labeling.
- **Do NOT use for mutually exclusive toggles:** Use `Radio` or `Tabs` instead.

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ Button Container (Interactive + PressTarget + FocusRing)    │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Inline Primitive (gap="xs", align="center")             │ │
│ │  ┌──────────────┐  ┌──────────────────┐  ┌────────────┐ │ │
│ │  │ Leading Icon │  │   Label (Text)   │  │TrailingIcon│ │ │
│ │  └──────────────┘  └──────────────────┘  └────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Variants & Intents

| Intent | Semantic Meaning | Visual Role | Token Consumption |
| :--- | :--- | :--- | :--- |
| `primary` | High-emphasis main action on a page or modal | Solid Royal Sapphire fill | `component.button.primary.*` |
| `secondary` | Medium-emphasis alternative action (e.g. "Cancel", "Back") | Outlined border on default surface | `component.button.secondary.*` |
| `ghost` | Low-emphasis subtle action inside cards or dense toolbars | Transparent surface, text-only until hover | `component.button.ghost.*` |
| `destructive` | High-risk, irreversible action (e.g. "Delete Account") | Solid Crimson Red fill | `component.button.destructive.*` |

---

## 6. Sizes

| Size | Visual Height | Horizontal Padding | Font Token | Icon Size | Touch Target |
| :--- | :---: | :---: | :--- | :--- | :---: |
| `sm` | **32px** (`size.control.sm`) | 12px (`space.3`) | `font.size.xs` (12px, weight 500) | 16px (`size.icon.sm`) | $\ge 44\text{px}$ via `PressTarget` |
| `md` | **40px** (`size.control.md`) | 16px (`space.4`) | `font.size.sm` (14px, weight 500) | 20px (`size.icon.md`) | $\ge 44\text{px}$ via `PressTarget` |
| `lg` | **48px** (`size.control.lg`) | 20px (`space.5`) | `font.size.base` (16px, weight 600) | 20px (`size.icon.md`) | Flush ($\ge 48\text{px}$) |

*Constraint:* The deferred 28px control height is strictly prohibited in this release.

---

## 7. States

1. **`default`:** Resting idle state.
2. **`hover`:** Pointer presence with subtle darkening of surface fill (`brand.700` or `neutral.100`).
3. **`pressed`:** Active click/tap compression with deeper tint (`brand.800` or `neutral.200`).
4. **`focus`:** Keyboard navigation focus boundary (`FocusRing`: 2px solid `brand.600` with 2px offset).
5. **`disabled`:** Non-interactive state (`opacity.disabled` = 0.38, `pointer-events: none`, `aria-disabled="true"`).
6. **`loading`:** Execution in progress. Replaces leading icon with `Spinner`, retains button width to prevent layout shift, and applies `aria-busy="true"`.

---

## 8. Slots
- `leadingIcon`: Optional leading icon (e.g. "+" for create).
- `children`: Mandatory visible button label (text).
- `trailingIcon`: Optional trailing icon (e.g. arrow for next step).

---

## 9. Behavior & Interaction
- **Click Propagation:** Click events propagate `onClick` callbacks. When `disabled={true}` or `loading={true}`, all click propagation is halted.
- **Loading State Stability:** When transitioning to `loading`, the button maintains its current computed width so adjacent layout does not collapse.

---

## 10. Keyboard Interaction
- **`Enter` Key:** Activates the button.
- **`Space` Key:** Activates the button on keydown / keyup.
- **`Tab` Key:** Navigates focus to the button. Visible focus indicator appears only during keyboard navigation (`:focus-visible`).

---

## 11. Accessibility Guarantees
- **Semantic Tag:** Renders native `<button type="button|submit|reset">`.
- **Accessible Name:** Computed directly from the text label.
- **Contrast Ratios:**
  - `primary` on white: > 4.5:1 (WCAG AA).
  - `destructive` on white: > 4.5:1 (WCAG AA).
  - `FocusRing`: $\ge 3:1$ against canvas and adjacent surface borders.
- **Touch Target:** Mandatory $44 \times 44\text{px}$ hit area on touch viewports enforced via `PressTarget`.

---

## 12. Responsive Behavior
- In narrow viewports, button labels never truncate with ellipsis (`softWrap: true` or responsive container wrapping).
- Action pairs (e.g. `[Cancel] [Confirm]`) inside modal dialogs recompose from horizontal `Inline` to vertical `Stack` on viewports $< 480\text{px}`.

---

## 13. Motion & Transitions
- Background and border transitions governed by `motion.fast` (**150ms**) and `motion.ease.standard` (`cubic-bezier(0.2, 0, 0, 1)`).
- When `prefers-reduced-motion` is active, transition duration collapses to **0ms** (`motion.instant`).

---

## 14. Token Mapping Hierarchy

$$\text{component.button.[intent].[state]} \longrightarrow \text{color.action.[intent].[state]} \longrightarrow \text{color.brand.* | color.neutral.*}$$

- Radius: `radius.md` (10px default; 6px in Refined preset).
- Height: `size.control.sm` (32px), `size.control.md` (40px), `size.control.lg` (48px).
- Font: `font.family.primary` (`Cairo`).

---

## 15. Composition Rules
- **Parent-Owned Spacing:** Never add margins to `Button`. Use `Inline(gap="sm")` for horizontal button pairs.
- **Icon Pairing:** Always use `Icon` primitive for leading/trailing glyphs to maintain optical weight parity.

---

## 16. AI Usage Rules
- **DO NOT USE FOR LINKS:** Never render `<Button onClick={() => router.push('/home')}>`. Use `<Link href="/home">`.
- **DO NOT INVENT VARIANTS:** Restrict strictly to `primary`, `secondary`, `ghost`, and `destructive`.
- **LOADING STATE:** When an async mutation occurs, pass `loading={true}` rather than rendering custom text or spinners.
