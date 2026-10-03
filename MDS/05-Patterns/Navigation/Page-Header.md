# MDS Pattern: Page-Header

**Document Layer:** 05-Patterns / Navigation  
**Status:** STABLE (Phase 6 Implementation)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-16  

---

## 1. Purpose
The **Page-Header** pattern establishes the primary semantic anchor and orientation strip at the top of a page, combining hierarchical breadcrumb navigation, the page H1/H2 title, contextual status badges, and top-level action buttons.

---

## 2. User Intent
The user intends to orient themselves within the product hierarchy (where am I?), identify the active entity or view, and quickly access the most important actions relevant to the current screen (e.g. "Create New", "Export", "Settings").

---

## 3. Problem Solved
Prevents inconsistent header arrangements across different views. Eliminates confusion regarding where primary page actions belong, how breadcrumbs relate to the page title, and where entity status should be displayed.

---

## 4. When to Use
- At the top of every distinct view, dashboard screen, or entity detail page.
- When a page requires breadcrumb orientation and primary contextual actions.
- When entity status (e.g., "Active", "Draft", "Archived") is an essential attribute.

---

## 5. When Not to Use
- Inside modal dialogs: Use modal dialog header.
- Inside small embedded cards: Use card header.
- As a substitute for top-level global navigation navbar.

---

## 6. Composition Architecture

```text
┌───────────────────────────────────────────────────────────────────────────┐
│ Page-Header (Stack gap="xs", padding-block="space.4")                      │
│                                                                           │
│  Breadcrumb Trail (Inline gap="2xs", align="center")                      │
│   ├── Link(variant="muted", "Projects") /                                 │
│   ├── Link(variant="muted", "Falcon-9") /                                 │
│   └── Text(color="text.secondary", "Deployments")                         │
│                                                                           │
│  Title & Actions Strip (Inline justify="space-between" align="center")    │
│   ├── Leading Title Group (Inline gap="sm" align="center")                │
│   │    ├── Heading H1 (font.size.2xl, font.weight.bold, softWrap: true)   │
│   │    │    "Production Deployments"                                      │
│   │    └── Badge (variant="brand", "v2.4.0 Active")                       │
│   │                                                                       │
│   └── Trailing Action Group (Inline gap="xs" align="center")              │
│        ├── Secondary Action: Button(variant="secondary", "Export CSV")    │
│        └── Primary Action:   Button(variant="primary",   "+ New Deploy")  │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Required Components
- `Heading` (Layer 03 Typography Primitive — H1)
- `Button` (Layer 04 Actions Component — primary page action)
- `Inline` (Layer 03 Layout Primitive)
- `Stack` (Layer 03 Layout Primitive)

---

## 8. Optional Components
- `Link` (Layer 04 Actions Component — breadcrumb hierarchy items)
- `Badge` (Layer 04 Data Display Component — entity status pill)
- `IconButton` (Layer 04 Actions Component — back arrow button or settings gear)
- `Tabs` (Layer 04 Navigation Component — sub-view tab navigation anchored below title)

---

## 9. Information Hierarchy
1. **Breadcrumbs:** Muted contextual trail establishes parent hierarchy.
2. **Page Title (H1):** Primary visual focal point confirming current location.
3. **Status Badge:** Contextual modifier immediately adjacent to title.
4. **Action Group:** Anchored at trailing edge for immediate execution.

---

## 10. Interaction Model
- Clicking breadcrumb links navigates up the information architecture.
- Clicking the primary action triggers the main page workflow (e.g. opens modal or navigates to create form).
- Action buttons maintain standard hover, active, and focus states.

---

## 11. Experience States
- **Standard Viewing:** Title, badge, and actions displayed normally.
- **Loading State:** Breadcrumbs and title render `Skeleton` shimmers while data resolves.
- **Read-Only / No Permission:** Primary create action is disabled or hidden with explanatory tooltip.

---

## 12. Responsive Behavior
- **Compact (<640px):**
  - Breadcrumb trail collapses to show only the immediate parent back link (`← Projects`).
  - Title & Actions strip switches to vertical stack: Title + Badge on top, Action buttons full-width beneath.
  - Heading reduces font size gracefully from `2xl` to `xl`.
- **Standard & Wide (>640px):**
  - Full breadcrumb trail visible.
  - Title and Actions align on a single horizontal row (`Inline justify="space-between"`).

---

## 13. Accessibility (a11y)
> *Standards Scope:* Implemented accessibility behaviors were validated against selected WCAG success criteria where applicable. Comprehensive cross-platform assistive technology testing remains deferred to Phase 8.
- The entire page header is wrapped in `<header role="banner">` or `<div role="region" aria-label="Page header">`.
- Breadcrumb navigation is wrapped in `<nav aria-label="Breadcrumb">` with `<ol>` and `aria-current="page"` on the active leaf item.
- Heading has explicit level `<h1>` (exactly one H1 per page).
- Interactive action buttons maintain minimum $\ge 44 \times 44\text{px}$ touch targets where applicable via `PressTarget`. Static title and breadcrumb text are exempt.

---

## 14. RTL & Logical Progression
- Progresses along the inline axis.
- Title and breadcrumbs align to `inline-start` (right in RTL).
- Action buttons align to `inline-end` (left in RTL).
- Breadcrumb separator slashes or chevrons flip logically.
- Zero `row-reverse` is permitted.

---

## 15. Density Behavior
- **Comfortable:** Vertical padding `space.6` (24px), title `font.size.2xl`, action button `40px` (`md`).
- **Compact:** Vertical padding `space.4` (16px), title `font.size.xl`, action button `32px` (`sm`).
- **Dense:** Dashboards only. Vertical padding `space.3` (12px), title `font.size.lg`.

---

## 16. Motion & Animation
- Tab indicator sliding (if tabs present) uses 250ms (`var(--mds-motion-normal)`).
- Collapses to 0s under `prefers-reduced-motion: reduce`.

---

## 17. Token Usage
- Title: `font.size.2xl`, `font.weight.bold`, `color.text.primary`
- Breadcrumb Link: `font.size.sm`, `color.text.secondary`
- Action Button: `component.button.primary.background.default`
- Padding Block: `space.4` to `space.6`

---

## 18. Contextual Variants
- **Entity Detail Header:** Includes back button, entity title, status badge, and action menu.
- **Dashboard Section Header:** Title + date picker / filter trigger.
- **Tabbed Page Header:** Page header with integrated `Tabs` line indicator anchored directly beneath title.

---

## 19. Composition Rules
- Exactly ONE `<h1>` tag must be present in the Page-Header.
- Never place more than 2 visible buttons in the trailing action group; collapse additional actions into an overflow menu (`IconButton` with `...`).

---

## 20. Anti-Patterns & Prohibitions
- **NO MULTIPLE H1s:** Never render multiple H1 elements on the same page.
- **NO TRUNCATED PAGE TITLES:** The title must be allowed to wrap to 2 lines on small screens without truncation.
- **NO FLOATING ACTIONS:** Actions must be grouped cleanly with `<Inline gap="xs">`.

---

## 21. AI Usage & Generation Rules
- When the user asks to "build a dashboard page" or "create an entity view", the AI **MUST** place `Page-Header` at the top of the layout.
- The AI must wrap the title in `<h1>`.
- The AI must place the primary action at the trailing edge.

---

## 22. Verification & Validation Criteria
- [ ] Title has semantic `<h1>` tag.
- [ ] Breadcrumb nav has `<nav aria-label="Breadcrumb">` and `aria-current="page"`.
- [ ] Responsive stack collapses cleanly on viewports $<640\text{px}$.
- [ ] Touch hit area $\ge 44 \times 44\text{px}$ on all buttons.
- [ ] 0 raw hex colors or physical coordinates.
