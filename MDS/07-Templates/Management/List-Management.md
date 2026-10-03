# MDS Template: List-Management (`MDS-TMP-002`)

**Document Layer:** 07-Templates / Management  
**Status:** APPROVED (Phase 8.1.3 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-17  

---

## 1. Template ID
`MDS-TMP-002`

## 2. Name
List & Collection Management Template

## 3. Intent
To provide an authoritative, scalable layout for browsing, filtering, sorting, paginating, and executing bulk actions across a collection of homogeneous data entities.

## 4. Problem Solved
Standardizes entity collection views across applications, replacing disparate table headers, mismatched search bars, and inconsistent pagination with a unified, accessible, responsive collection management scaffold.

## 5. When to Use
- For any entity index view (Users, Orders, Invoices, Products, Projects, Audit Records).
- For global search results and faceted discovery views (subsuming Candidate 7).
- When users need to query, inspect, batch-select, or export multiple records.

## 6. When Not to Use
- For high-level executive KPI metrics: Use `Dashboard-Overview` (`MDS-TMP-001`) instead.
- For deep inspection or editing of a single entity: Use `Detail-Entity` (`MDS-TMP-003`) instead.
- For creating a new entity via a form: Use `Form-Edit` (`MDS-TMP-004`) instead.

## 7. Page Regions
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Region 1: Global Navigation (App Shell Header)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 2: Page Header (Title, Total Record Count, Primary Action "Create") │
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 3: Filter & Search Toolbar (Search Input, Filter Pills, Bulk Actions)│
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 4: Primary Collection Canvas (Table or Responsive Card Grid)         │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ Homogeneous Entity Rows / Cards (Checkboxes, Columns, Context Actions)  │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 5: Pagination & Summary Footer (Showing 1-25 of 1,240 | Prev/Next)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 8. Region Hierarchy
`Global Navigation` $\to$ `Page Header` $\to$ `Filter & Search Toolbar` $\to$ `Primary Collection Canvas` $\to$ `Pagination Footer`.

## 9. Pattern Composition
- **`Page-Header` (`MDS/05-Patterns/Navigation/Page-Header.md`):** Title, entity count badge, export button, primary "Add Entity" button.
- **`Search-Filter-Bar` (`MDS/05-Patterns/Search/Search-Filter-Bar.md`):** Instant search input, faceted filter dropdowns, active filter pills, and "Clear Filters" action.
- **`Data-List-Card` (`MDS/05-Patterns/Data/Data-List-Card.md`):** Alternative card rendering for entity collections on mobile or tile view.
- **`Empty-State` (`MDS/05-Patterns/Feedback/Empty-State.md`):** Renders when collection has 0 items or when filters yield 0 results.
- **`Confirmation-Dialog` (`MDS/05-Patterns/Feedback/Confirmation-Dialog.md`):** For batch deletion or archiving of selected entities.

## 10. Workflow Slots
- **`Search-Discovery` (`MDS/06-Workflows/Search/Search-Discovery.md`):** Debounced search, faceted filter execution, and active query states.
- **`Destructive-Action` (`MDS/06-Workflows/Actions/Destructive-Action.md`):** Single or bulk entity deletion with safety confirmation.
- **`Error-Recovery` (`MDS/06-Workflows/Recovery/Error-Recovery.md`):** Intercepts network failure during pagination/filter requests with retry.

## 11. Component Dependencies
- `Button`, `IconButton`, `Link` (Actions)
- `Input`, `Checkbox`, `Select` (Inputs)
- `Table`, `Badge`, `Card` (Data Display)
- `Skeleton`, `Spinner`, `Alert` (Feedback)
- `Surface`, `Stack`, `Inline`, `Container` (Primitives)

## 12. Content Slots
- `slot="header-actions"`: Primary CTA ("Create User"), Secondary Action ("Export CSV").
- `slot="toolbar-filters"`: Custom domain filter dropdowns (Status, Date, Role).
- `slot="collection-view"`: Table component or Data-List-Card grid.
- `slot="footer-pagination"`: Pagination controls and total record indicators.

## 13. Required vs Optional Regions
- **Required:** Page Header, Filter & Search Toolbar, Primary Collection Canvas, Pagination Footer.
- **Optional:** Bulk Action Bar (appears dynamically upon item selection).

## 14. Responsive Composition
- **Compact (< 768px):** Search-Filter-Bar collapses search input to full width; filter pills move into an off-canvas filter sheet; Table view automatically recomposes into vertical `Data-List-Card` stack; pagination simplifies to "Previous / Next" buttons with $\ge 44\text{px}$ touch targets.
- **Standard (768px – 1151px):** Table renders horizontally scrollable container with visual fade indicator; search toolbar renders inline.
- **Wide (1152px – 1439px):** Canonical 1152px container max-width; full multi-column table or 3-column card grid.
- **Full ($\ge$ 1440px):** 1440px wide container (`container.xl`); maximum information throughput with comfortable spacing.

## 15. Mobile Composition
- Converts table rows to `Data-List-Card` instances to avoid unusable horizontal squishing.
- Batch action floating bar docks cleanly at the bottom edge above navigation bars.
- Touch target sizes strictly adhere to the $44 \times 44\text{px}$ minimum rule.

## 16. RTL Behavior
- Search input icon sits at inline-start (`right` in RTL).
- Filter dropdowns and column sorting arrows align naturally with text direction.
- Checkbox selection column sits on inline-start; action menu button sits on inline-end.
- Zero `row-reverse` hacks used.

## 17. Accessibility Structure
- `<main>` landmark encompasses the collection management workspace.
- The Table container has `tabindex="0"`, `role="region"`, and `aria-label="[Entity Name] List"` to allow keyboard scrolling.
- Table headers include `aria-sort="ascending"` / `"descending"` for active sort columns.
- Active search count updates are announced via polite live region (`aria-live="polite"`).

## 18. Experience States
- **`Default / Populated`:** Populated table/cards with active records and pagination.
- **`Loading`:** Full table skeleton with 5 animated placeholder rows.
- **`Empty (Zero Data)`:** No entities exist yet $\to$ `Empty-State` with "Create First [Entity]" CTA.
- **`Empty (Filtered)`:** Query returned 0 matches $\to$ `Empty-State` with "Clear all filters" CTA.
- **`Partial`:** Stale data banner if offline, showing cached results.
- **`Error`:** Error card in place of table with "Failed to load entities — Retry" button.
- **`No Access`:** Permission Denied card with "Request access to this collection" CTA.

## 19. Loading Strategy
Renders a 5-row table skeleton or 6-card grid skeleton matching row height (52px) and column widths. Eliminates layout shift.

## 20. Error Strategy
Network failure during pagination preserves the previous valid page in memory while displaying an inline `Alert` with retry trigger at the top of the collection canvas.

## 21. Empty Strategy
Differentiates between **Zero Data** (onboarding empty state with illustration and create CTA) and **Filtered Empty** (search empty state with "Clear Filters" action).

## 22. Recovery Strategy
Failed delete action rolls back optimistic UI removal and shows error toast; network drop allows user to retry without losing search input text.

## 23. Density Behavior
- **Comfortable:** 56px table row height, 16px padding, standard badge sizes.
- **Compact:** 44px table row height, 12px padding, compact typography (`font.size.sm`).

## 24. Theme/Mode Behavior
- **Light:** Canvas `#F8FAFC`, Table header `#F1F5F9`, alternating row hover `#F8FAFC`.
- **Dark:** Canvas `#020617`, Table header `#0F172A`, row hover `#1E293B`.
- **High Contrast:** 1px solid borders between rows, clear selection checkboxes.

## 25. AI Integration
Optional AI search assistance in the toolbar: natural language query parser with badge indicating "AI-Assisted Filter"; citations available in item detail.

## 26. Navigation Context
Breadcrumb: `Home > [Entity Collection]`. Clicking a row/card navigates to `Detail-Entity` (`MDS-TMP-003`).

## 27. Focus Management
Upon completing search query, focus remains in the search input; upon row deletion via dialog, focus restores to the next adjacent row's action button.

## 28. Motion Behavior
Row deletion uses 150ms fade-out; filter tag dismissals use smooth scale; collapses to 0ms when reduced motion is requested.

## 29. Token Dependencies
`color.surface.*`, `color.border.*`, `space.3`, `space.4`, `space.6`, `container.lg`, `container.xl`.

## 30. Anti-Patterns
- ❌ Do NOT hide pagination controls when multiple pages exist.
- ❌ Do NOT remove column headers on desktop to save space.
- ❌ Do NOT force mobile viewports to horizontally scroll a 10-column table; recompose to cards.

## 31. Validation Requirements
Verified by `run_tests.py`, HTML showcase testbed, and 100% token usage.

## 32. Selection Criteria
Select when user intent is querying, browsing, inspecting, or performing batch actions on an entity collection.
