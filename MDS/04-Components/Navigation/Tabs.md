# MDS Component: Tabs

**Document Layer:** 04-Components / Navigation  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Purpose
The **Tabs** component organizes content into distinct view panels, allowing users to switch between related context views in place without leaving the page.

---

## 2. When to Use
- To partition complex pages or settings into related sub-views (e.g. "General", "Security", "Notifications").
- To offer alternate views of the same dataset (e.g. "Chart View" vs "Table View").

---

## 3. When Not to Use
- For step-by-step wizard progression: Use a `Stepper` instead.
- For primary site-wide URL navigation: Use primary navigation links instead.

---

## 4. Anatomy

```text
┌─────────────────────────────────────────────────────────────┐
│ Tabs Container                                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ TabList (role="tablist", Inline gap="md", border-bottom)│ │
│ │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │ │
│ │  │ Tab 1 (Active│  │ Tab 2        │  │ Tab 3        │   │ │
│ │  │ 2px blue line│  │              │  │              │   │ │
│ │  └──────────────┘  └──────────────┘  └──────────────┘   │ │
│ └─────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ TabPanel (role="tabpanel", active view content)         │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Variants
- `line` (Default): Subtle bottom hairline divider with a 2px Royal Sapphire indicator line under the active tab.
- `pill` / `contained`: Tabs styled as rounded pill buttons inside a subtle gray container track (`color.surface.raised`).

---

## 6. Sizes & Control Heights
- Standard tab control height: **40px** (`size.control.md`).
- Minimum touch hit-box: $\ge \mathbf{44 \times 44px}$ (`PressTarget`).

---

## 7. States
- `default`: Neutral text (`color.text.secondary`).
- `hover`: Text darkens to primary (`color.text.primary`).
- `active` / `selected`: High-contrast brand blue text (`color.brand.600`) + 2px active indicator line.
- `focus`: 2px `FocusRing` on `:focus-visible`.
- `disabled`: Non-interactive muted text.

---

## 8. Slots & Composition
- `tabs`: Array of `{ id, label, icon?, count? }`.
- `children`: Corresponding `TabPanel` views.

---

## 9. Keyboard Interaction (WAI-ARIA APG Tabs Pattern)
- `Left Arrow` / `Right Arrow`: Moves focus and activates the previous/next tab along reading direction (automatically inverting direction in RTL).
- `Home` / `End`: Moves focus to first/last tab.
- `Tab`: Moves focus out of the `tablist` and into the active `tabpanel`.

---

## 10. Accessibility Guarantees
- Container has `role="tablist"`.
- Buttons have `role="tab"`, `aria-selected="true | false"`, and `aria-controls="panel-id"`.
- Content has `role="tabpanel"` and `aria-labelledby="tab-id"`.

---

## 11. Responsive & RTL Behavior
- In RTL, `Left Arrow` moves forward and `Right Arrow` moves backward along the native reading vector.
- On small mobile screens, the `TabList` allows horizontal swipe-scrolling without clipping tab text.

---

## 12. Motion & Transitions
- Active indicator sliding transition: 200ms (`motion.normal`) with `motion.ease.standard`. Collapses to 0ms on reduced motion.

---

## 13. Token Mapping Hierarchy
- Active Indicator: `color.action.primary.default` (`brand.600`).
- Border: `color.border.subtle` (1px).
- Indicator Thickness: `border.width.thick` (2px).

---

## 14. Composition Rules
- Never add external margins to tabs. Use `Stack` to separate `TabList` from `TabPanel`.

---

## 15. AI Usage Rules
- **ROVING ARROWS:** Always implement horizontal arrow-key navigation for tabs.
