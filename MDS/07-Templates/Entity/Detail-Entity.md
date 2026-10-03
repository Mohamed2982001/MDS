# MDS Template: Detail-Entity (`MDS-TMP-003`)

**Document Layer:** 07-Templates / Entity  
**Status:** APPROVED (Phase 8.1.3 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-17  

---

## 1. Template ID
`MDS-TMP-003`

## 2. Name
Detail & Entity Management Template

## 3. Intent
To provide an authoritative, deep single-entity inspection, review, and modification environment organized into a dual-pane information architecture (Primary Content + Supporting Metadata Panel).

## 4. Problem Solved
Eliminates scattered, inconsistent detail pages where metadata, activity history, and core properties compete for attention. Standardizes visual hierarchy across entity views (Profiles, Invoices, Contracts, Devices, Cases).

## 5. When to Use
- For single-record inspection views (e.g. Order #1234, User Profile, Invoice Details).
- For approval and review tasks (subsuming Candidate 8: Review / Approval).
- When an entity requires both comprehensive attributes and contextual metadata (audit trail, timestamps, assigned owners, related items).

## 6. When Not to Use
- For multi-record collections: Use `List-Management` (`MDS-TMP-002`) instead.
- For high-level executive dashboards: Use `Dashboard-Overview` (`MDS-TMP-001`) instead.
- For multi-step wizard creation: Use `Form-Edit` (`MDS-TMP-004`) instead.

## 7. Page Regions
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Region 1: Global Navigation (App Shell Header)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 2: Page Header (Back Link, Entity Title, Status Badge, Action Group) │
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 3: Dual-Pane Workspace (2:1 Column Ratio)                            │
│ ┌─────────────────────────────────────────┐ ┌─────────────────────────────┐ │
│ │ Primary Content Area                    │ │ Secondary Metadata Panel    │ │
│ │ ├── Entity Overview / Key Properties    │ │ ├── Quick Summary Card      │ │
│ │ ├── Tabs (Details, Activity, Sub-items) │ │ ├── Audit Log / Timestamps  │ │
│ │ └── Tab Content Workspace               │ │ └── Danger / Archive Zone   │ │
│ └─────────────────────────────────────────┘ └─────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 4: Sticky Footer Action Rail (Save / Cancel / Approve / Reject)     │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 8. Region Hierarchy
`Global Navigation` $\to$ `Page Header` $\to$ `Dual-Pane Workspace` (Primary Area + Secondary Panel) $\to$ `Footer Action Rail`.

## 9. Pattern Composition
- **`Page-Header` (`MDS/05-Patterns/Navigation/Page-Header.md`):** Back navigation link, entity H1 title, status badge, primary action buttons ("Edit", "Approve", "Download").
- **`Form-Section` (`MDS/05-Patterns/Forms/Form-Section.md`):** Grouped entity property sections within tab panes.
- **`Data-List-Card` (`MDS/05-Patterns/Data/Data-List-Card.md`):** Renders related sub-entities, line items, or attachments.
- **`Confirmation-Dialog` (`MDS/05-Patterns/Feedback/Confirmation-Dialog.md`):** Triggered for destructive actions (Delete, Archive, Revoke) or high-impact approvals.
- **`Empty-State` (`MDS/05-Patterns/Feedback/Empty-State.md`):** Renders inside empty tabs (e.g. "No attachments uploaded yet").

## 10. Workflow Slots
- **`Settings-Update` (`MDS/06-Workflows/Settings/Settings-Update.md`):** Inline attribute edits with optimistic autosave or batched submission.
- **`Destructive-Action` (`MDS/06-Workflows/Actions/Destructive-Action.md`):** Archiving or permanently deleting the entity.
- **`Error-Recovery` (`MDS/06-Workflows/Recovery/Error-Recovery.md`):** Handles failure when updating attributes or loading entity details.

## 11. Component Dependencies
- `Button`, `IconButton`, `Link` (Actions)
- `Tabs`, `Badge`, `Card`, `Table` (Data Display & Nav)
- `Field`, `Input`, `Textarea`, `Switch` (Inputs)
- `Alert`, `Skeleton`, `Spinner` (Feedback)
- `Surface`, `Stack`, `Inline`, `Grid`, `Container` (Primitives)

## 12. Content Slots
- `slot="header-status"`: Primary entity status badge (`success`, `warning`, `danger`, `neutral`).
- `slot="primary-tabs"`: Navigation tabs (`Details`, `History`, `Attachments`, `Notes`).
- `slot="tab-content"`: The active tab's property forms or child entity lists.
- `slot="sidebar-metadata"`: Entity attributes (ID, Created Date, Last Modified, Owner, Tags).
- `slot="footer-actions"`: Contextual actions (Save, Cancel, Approve, Reject).

## 13. Required vs Optional Regions
- **Required:** Page Header with Back Link, Primary Content Area, Secondary Metadata Panel.
- **Optional:** Tabs (if entity has minimal fields), Sticky Footer Action Rail.

## 14. Responsive Composition
- **Compact (< 768px):** Dual-pane collapses into a single vertical column; Secondary Metadata Panel moves below Primary Content or into a bottom sheet; Action buttons pin to a sticky bottom rail ($\ge 44\text{px}$ touch targets).
- **Standard (768px – 1151px):** Primary and Secondary panels render in an adaptive master-detail 60/40 or stacked tabbed layout.
- **Wide (1152px – 1439px):** Canonical 1152px container max-width; 66/33 dual-pane side-by-side split.
- **Full ($\ge$ 1440px):** 1440px wide container (`container.xl`); primary and secondary panels scale proportionally while maintaining optimal reading line lengths.

## 15. Mobile Composition
- Back button is prominent at top-left/top-right.
- Status badge stays visible next to the title.
- Actions dock into a persistent sticky bottom bar with safe-area padding.

## 16. RTL Behavior
- Primary content column aligns to inline-start (`right` in RTL).
- Secondary metadata sidebar aligns to inline-end (`left` in RTL).
- Back chevron mirrors (`←` becomes `→`).
- Zero `row-reverse` hacks used.

## 17. Accessibility Structure
- `<main>` landmark encompasses the entity workspace.
- `<aside>` landmark identifies the Secondary Metadata Panel.
- `<nav>` landmark surrounds the tab strip with WAI-ARIA roving tabindex keyboard navigation.
- Initial focus lands on the H1 title or active tab panel.

## 18. Experience States
- **`Default / Populated`:** Entity loaded with active metadata and tabs.
- **`Loading`:** Full dual-pane geometric skeleton (header skeleton, 2-column body skeleton).
- **`Not Found (404)`:** Resource deleted or missing $\to$ `Empty-State` with "Entity not found — Return to list" CTA.
- **`No Access / Permission Denied`:** Informative card with "Request access to this entity" CTA.
- **`Archived / Deleted Banner`:** Prominent read-only banner with "Restore" recovery trigger.
- **`Error`:** Full-page error card with retry button.

## 19. Loading Strategy
Renders an exact geometric skeleton: Page header skeleton (48px height), Primary panel card skeleton (320px height), Sidebar metadata skeleton (240px height). Zero layout shift.

## 20. Error Strategy
Field-level inline errors map to specific `Field` components; entity loading failure shows overarching error card with retry.

## 21. Empty Strategy
Empty tabs (e.g. zero attachments) render the `Empty-State` pattern with upload button; does NOT display a blank white area.

## 22. Recovery Strategy
Archived entities offer single-click undo restoration; failed attribute updates roll back cleanly and alert the user without data loss.

## 23. Density Behavior
- **Comfortable:** Standard padding (`space.6`), 14px body text, 24px grid gutters.
- **Compact:** Reduced padding (`space.4`), 12px metadata text, 16px grid gutters.

## 24. Theme/Mode Behavior
- **Light:** Canvas `#F8FAFC`, Surface `#FFFFFF`, Border `#E2E8F0`.
- **Dark:** Canvas `#020617`, Surface `#0F172A`, Raised `#1E293B`.
- **High Contrast:** Pure black/white contrast, distinct 2px borders separating panels.

## 25. AI Integration
Optional "AI Entity Insights" widget in the secondary panel: generates automated audit summaries or anomaly detection tags with human review controls.

## 26. Navigation Context
Breadcrumb: `Home > [Collection Name] > [Entity Identifier]`. Back link returns to `List-Management` (`MDS-TMP-002`).

## 27. Focus Management
Tab strip supports Left/Right arrow key navigation; opening confirmation dialog traps focus inside; closing restores focus to trigger.

## 28. Motion Behavior
Tab switching uses 150ms cross-fade; drawer open uses 250ms slide; collapses to 0ms in reduced motion mode.

## 29. Token Dependencies
`container.lg`, `container.xl`, `space.4`, `space.6`, `color.surface.*`, `color.border.*`.

## 30. Anti-Patterns
- ❌ Do NOT hide the entity status badge or primary ID.
- ❌ Do NOT place destructive actions in the same visual grouping as primary approval actions without clear visual hierarchy separation.
- ❌ Do NOT stretch text inputs full-width across 1440px displays.

## 31. Validation Requirements
Verified by `run_tests.py`, HTML showcase testbed, and 100% token usage.

## 32. Selection Criteria
Select when user intent is deep inspection, modification, or approval of a single identifiable business record.
