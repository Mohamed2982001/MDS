# MDS Template: Dashboard-Overview (`MDS-TMP-001`)

**Document Layer:** 07-Templates / Overview  
**Status:** APPROVED (Phase 8.1.3 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-17  

---

## 1. Template ID
`MDS-TMP-001`

## 2. Name
Dashboard & Overview Template

## 3. Intent
To provide an executive, high-level operational overview summarizing key metrics, active telemetries, quick status indicators, and recent entity activity in a single cohesive viewport.

## 4. Problem Solved
Eliminates fragmented, ad-hoc dashboard layouts by establishing a standardized information hierarchy that balances high-density metric telemetry (KPI cards) with digestible operational activity feeds and rapid navigation shortcuts.

## 5. When to Use
- As the default landing view of an authenticated application, administrative portal, or SaaS workspace.
- For business intelligence portals, system telemetry monitors, and project portfolio summaries.
- When users need immediate situational awareness before diving into specific tasks or entities.

## 6. When Not to Use
- For managing large, filterable tabular collections of a single entity type: Use `List-Management` (`MDS-TMP-002`) instead.
- For deep inspection or editing of a single record: Use `Detail-Entity` (`MDS-TMP-003`) instead.
- For multi-step data entry tasks: Use `Form-Edit` (`MDS-TMP-004`) instead.

## 7. Page Regions
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Region 1: Global Navigation (App Shell Header)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 2: Page Header (Title, Date Filter, Status Badge, Primary Action)   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 3: Metric Summary Strip (4-Card Responsive KPI Grid)                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 4: Primary Content Grid (2:1 or 1:1 Split Layout)                    │
│ ┌─────────────────────────────────────────┐ ┌─────────────────────────────┐ │
│ │ Main Telemetry / Chart / Activity List  │ │ Secondary Quick Insights    │ │
│ │ (Wide Column)                           │ │ (Narrow Column)             │ │
│ └─────────────────────────────────────────┘ └─────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 5: System Status & Footer Meta                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 8. Region Hierarchy
`Global Navigation` $\to$ `Page Header` $\to$ `Metric Summary Strip` $\to$ `Primary Content Grid` $\to$ `Footer Meta`.

## 9. Pattern Composition
- **`Page-Header` (`MDS/05-Patterns/Navigation/Page-Header.md`):** Top orientation bar with breadcrumbs, H1 title, quick filter selector, and primary CTA.
- **`Data-List-Card` (`MDS/05-Patterns/Data/Data-List-Card.md`):** Renders recent activity items, alerts, and transaction previews.
- **`Empty-State` (`MDS/05-Patterns/Feedback/Empty-State.md`):** Renders when telemetry or activity widgets have zero data.
- **`Confirmation-Dialog` (`MDS/05-Patterns/Feedback/Confirmation-Dialog.md`):** Triggered when dismissing or resetting dashboard widgets.

## 10. Workflow Slots
- **`Search-Discovery` (`MDS/06-Workflows/Search/Search-Discovery.md`):** Filter and search within recent activity feeds.
- **`Destructive-Action` (`MDS/06-Workflows/Actions/Destructive-Action.md`):** For removing or resetting pinned dashboard metrics.
- **`Error-Recovery` (`MDS/06-Workflows/Recovery/Error-Recovery.md`):** Intercepts feed loading failures and provides contextual retry.

## 11. Component Dependencies
- `Button`, `IconButton` (Actions)
- `Card`, `Badge` (Data Display)
- `Skeleton`, `Spinner`, `Alert` (Feedback)
- `Select` (Date Range Picker trigger)
- `Surface`, `Stack`, `Inline`, `Grid`, `Container` (Primitives)

## 12. Content Slots
- `slot="header-actions"`: Time-range selector (e.g. "Last 30 Days"), Export button, Primary CTA.
- `slot="metric-cards"`: 3 to 4 KPI summary cards (Total Volume, Active Users, Revenue, Health).
- `slot="primary-workspace"`: Main telemetry graphs, tabular transaction previews, or active queues.
- `slot="secondary-panel"`: System announcements, audit log snippets, or quick task checklists.

## 13. Required vs Optional Regions
- **Required:** Page Header, Metric Summary Strip, Primary Content Workspace.
- **Optional:** Secondary Quick Insights panel (collapses if omitted), Date Range filter.

## 14. Responsive Composition
- **Compact (< 768px):** Metric Strip recomposes to a 1-column or 2x2 grid; Primary Content and Secondary Panel stack vertically; Page Header actions wrap or collapse into an icon menu.
- **Standard (768px – 1151px):** Metric Strip renders 2-column or 4-column compact; Primary Content and Secondary Panel display in a stacked or 50/50 arrangement.
- **Wide (1152px – 1439px):** Canonical 1152px container max-width; Metric Strip renders 4-column; Primary (66%) and Secondary (33%) side-by-side grid.
- **Full ($\ge$ 1440px):** 1440px wide container (`container.xl`); preserves side-by-side split without unreadable line lengths.

## 15. Mobile Composition
- Action buttons stack or pin to sticky bottom.
- Metric cards use compact padding (`space.3`) with minimum 44px tap areas for details.
- Tables or horizontal widgets inside slots enable swipe gestures or card transforms.

## 16. RTL Behavior
- Primary metric trend arrows (`↑`, `↓`) do NOT mirror (trend direction is universal).
- Inline layout flows right-to-left; primary metrics align to inline-start (`right` in RTL).
- Secondary panel sits on inline-end (`left` in RTL).
- Zero `row-reverse` hacks used.

## 17. Accessibility Structure
- `<main>` landmark wraps the entire dashboard workspace.
- `<h1>` is inside `Page-Header`.
- KPI cards structured as `<section>` or `<article>` with `<h2>` headings.
- Metric numbers use `font-variant-numeric: tabular-nums` for screen reader and visual alignment stability.

## 18. Experience States
- **`Default / Populated`:** Metric cards populated with delta percentages, activity stream active.
- **`Loading`:** Full-page geometric skeleton (4 KPI card skeletons + 2 content card skeletons).
- **`Empty`:** If workspace is brand new, replaces content grid with `Empty-State` ("No activity recorded yet").
- **`Partial`:** If 1 widget fails to load, displays an inline `Alert` within that widget while remaining cards function.
- **`Error`:** Top-level error banner with `Retry` action.
- **`No Access`:** Displays Permission Denied card with "Request dashboard access" CTA.

## 19. Loading Strategy
Geometric skeleton loading: renders four 120px tall card skeletons for the metric strip, followed by a 360px tall content skeleton. Eliminates Cumulative Layout Shift (CLS).

## 20. Error Strategy
Non-blocking widget error encapsulation: widget-level errors display an inline alert with a reload icon button; page-level network failure displays an overarching banner with non-destructive retry.

## 21. Empty Strategy
Embeds `Empty-State` pattern with visual illustration placeholder, title "No metrics available", explanatory text, and a CTA button "Connect Data Source" or "Invite Team".

## 22. Recovery Strategy
Network failure triggers `Error-Recovery` workflow; cached metric values remain visible with a "Stale data — Click to refresh" indicator.

## 23. Density Behavior
- **Comfortable:** Default for mobile/web; 24px gutters, 16px card padding.
- **Compact:** 16px gutters, 12px card padding, smaller numeric display font (`font.size.xl` vs `font.size.2xl`).

## 24. Theme/Mode Behavior
- **Light:** Surface Canvas `#F8FAFC`, Surface Default `#FFFFFF`, subtle 1px border `#E2E8F0`.
- **Dark:** Surface Canvas `#020617`, Surface Default `#0F172A`, Surface Raised `#1E293B`.
- **High Contrast:** Pure black/white background, 2px borders, ambient shadows suppressed.

## 25. AI Integration
Optional "AI Executive Summary" card at top of workspace: summarizes daily trends with thumbs feedback and citation links; conforms to human-in-the-loop inspection rules.

## 26. Navigation Context
Breadcrumb displays `Home > Dashboard`; header actions allow switching dashboard views.

## 27. Focus Management
Initial focus lands on the primary header action or main content container; keyboard `Tab` navigates sequentially through KPI card drilldowns, then through the main activity feed.

## 28. Motion Behavior
Metric cards enter with subtle 150ms fade; loading skeletons shimmer with natural 1.5s wave; collapses instantly to 0ms when `prefers-reduced-motion: reduce` is active.

## 29. Token Dependencies
`space.4`, `space.6`, `space.8`, `container.lg` (1152px), `container.xl` (1440px), `color.surface.*`, `color.border.*`, `elevation.level1`.

## 30. Anti-Patterns
- ❌ Do NOT turn Dashboard into an unscrollable single-screen fixed layout.
- ❌ Do NOT hide metric card titles or units to save space.
- ❌ Do NOT allow cards to stretch infinitely across a 4K display without max-width containment.

## 31. Validation Requirements
Must pass 7-Dimension validation; verified via `run_tests.py` and showcase sandbox.

## 32. Selection Criteria
Select when user intent is broad operational monitoring, high-level metrics review, or cross-system status orientation.
