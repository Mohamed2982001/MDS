# MDS Pattern: Search-Filter-Bar

**Document Layer:** 05-Patterns / Search  
**Status:** STABLE (Phase 6 Implementation)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-16  

---

## 1. Purpose
The **Search-Filter-Bar** pattern provides an integrated query toolbar that combines full-text search, multi-faceted category filtering, active filter pill indicators, and an instant filter reset mechanism.

---

## 2. User Intent
The user intends to quickly locate, filter, or narrow down records within a large data collection (e.g., searching customers, filtering transactions by date and status).

---

## 3. Problem Solved
Prevents fragmented discovery UIs where search inputs and filter selectors are scattered across the screen. Unifies input, filter state display, and clear actions into a single coherent, responsive control strip.

---

## 4. When to Use
- Above data tables, card grids, directory listings, or product catalogs.
- When users need both keyword search and categorical filtering simultaneously.
- When active filters must be clearly visible and individually dismissible.

---

## 5. When Not to Use
- For simple site-wide navigation search in the top navbar: Use a standalone `Input` with an icon.
- For complex multi-predicate boolean query builders: Use advanced query workflow.
- Do NOT use with deferred `Combobox` or `DataGrid`.

---

## 6. Composition Architecture

```text
┌───────────────────────────────────────────────────────────────────────────┐
│ Search-Filter-Bar (Stack gap="xs")                                        │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ Toolbar Strip (Inline justify="space-between" align="center" gap="sm")│ │
│ │  ┌─────────────────────────────────┐ ┌──────────────┐ ┌─────────────┐│ │
│ │  │ Search Field (Input + 🔍 icon)   │ │ Filter Drop  │ │ Sort Drop   ││ │
│ │  │ (flex: 1, min-width: 200px)     │ │ (Select md)  │ │ (Select md) ││ │
│ │  └─────────────────────────────────┘ └──────────────┘ └─────────────┘│ │
│ └───────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│  Active Filters Row (Cluster gap="xs", align="center")                    │
│   ├── Filter Badge: "Status: Active" [✕]                                  │
│   ├── Filter Badge: "Role: Admin" [✕]                                     │
│   └── Clear All Button (Button variant="ghost", size="sm", "Clear All")   │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Required Components
- `Input` (Layer 04 Input Component — with prefix search icon)
- `Select` (Layer 04 Input Component — Native Select baseline for category filtering)
- `Badge` (Layer 04 Data Display Component — for removable active filter chips)
- `Inline` (Layer 03 Layout Primitive)
- `Stack` (Layer 03 Layout Primitive)
- `Cluster` (Layer 03 Layout Primitive — for wrapping active filter pills)

---

## 8. Optional Components
- `Button` (Layer 04 Actions Component — "Clear All" or "Filter" toggle)
- `IconButton` (Layer 04 Actions Component — for mobile filter drawer trigger)
- `Spinner` (Layer 04 Feedback Component — inside search input during debounced query)

---

## 9. Information Hierarchy
1. **Primary Input:** Full-text search input occupies leading prominent space.
2. **Secondary Controls:** Facet dropdowns (`Select`) sit immediately adjacent.
3. **Status Context:** Active filter pills sit directly underneath, confirming the active filter criteria.
4. **Reset Action:** "Clear All" link placed at the trailing edge of the active filter cluster.

---

## 10. Interaction Model
- Typing in the search input triggers an immediate debounced search (300ms).
- Selecting an option from a filter dropdown instantly adds an active filter badge to the cluster below.
- Clicking the [✕] on a filter badge removes that individual filter.
- Clicking "Clear All" clears all active filters and resets the search input.
- `Escape` key inside the search input clears the current search text.

---

## 11. Experience States
- **Resting / Empty:** Search input is blank; dropdowns show "All Categories"; no active filter pills.
- **Searching / Debouncing:** Search input displays a subtle `Spinner` in suffix slot.
- **Filtered Active:** Active filter pills are rendered in the cluster; result count updates.
- **No Results Found:** Interacts with downstream `Empty-State` pattern ("No results found matching your filters").

---

## 12. Responsive Behavior
- **Compact (<640px):**
  - Search input expands to 100% width.
  - Dropdowns stack vertically or collapse into a single "Filters" button opening a bottom modal sheet.
  - Active filter badges wrap onto multiple lines (`Cluster gap="xs"`).
- **Standard & Wide (>640px):**
  - Search input and dropdowns align inline on a single horizontal row (`Inline justify="space-between"`).

---

## 13. Accessibility (a11y)
> *Standards Scope:* Implemented accessibility behaviors were validated against selected WCAG success criteria where applicable. Comprehensive cross-platform assistive technology testing remains deferred to Phase 8.
- Search input has explicit accessible label (`aria-label="Search records"` or connected `Label`).
- Active filter badges have accessible removal labels (e.g. `aria-label="Remove filter: Status Active"`).
- Filter changes announce result updates to screen readers via a polite `LiveRegion` (e.g. "Showing 14 results").
- All interactive controls maintain $\ge 44 \times 44\text{px}$ touch targets where applicable via `PressTarget`. Static tags without click handlers are exempt.

---

## 14. RTL & Logical Progression
- Progresses along the inline axis: Search input sits at `inline-start` (right in RTL), dropdowns at `inline-end` (left in RTL).
- Search magnifying glass icon sits at `inline-start` within the input.
- No `row-reverse` is used; DOM tab sequence perfectly mirrors visual reading order.

---

## 15. Density Behavior
- **Comfortable:** Control heights `40px` (`size.control.md`), gap `space.3` (12px).
- **Compact:** Control heights `32px` (`size.control.sm`), gap `space.2` (8px).
- **Dense:** Technical dashboards only. Height `32px`, gap `space.2`. (0 unapproved 28px).

---

## 16. Motion & Animation
- Active filter pill insertion and removal uses 150ms fade-and-scale (`var(--mds-motion-fast)`).
- Collapses to 0s under `prefers-reduced-motion: reduce`.

---

## 17. Token Usage
- Search Input Background: `color.surface.default`
- Active Badge Tint: `color.brand.50` (Light) / `color.brand.900` (Dark)
- Active Badge Text: `color.brand.700`
- Border: `color.border.default`
- Spacing: `space.2` (Cluster gap), `space.3` (Toolbar gap)

---

## 18. Contextual Variants
- **Inline Filter Strip (Default):** Search and filter dropdowns share a single row.
- **Search-First Bar:** Search input dominates full width; filters sit on a separate secondary line.

---

## 19. Composition Rules
- Active filters must always be paired with a one-click "Clear All" action.
- Never wrap filter tags in a rigid single-line container that clips; always use `<Cluster>` with wrapping enabled.
- Do not build a custom Combobox dropdown; use the approved Native Select baseline.

---

## 20. Anti-Patterns & Prohibitions
- **NO HIDDEN ACTIVE FILTERS:** Never apply filters without visibly showing active badges to the user.
- **NO MISSING RESET:** Never omit the "Clear All" affordance when filters are active.
- **NO RAW MARGINS:** Use `<Inline>` and `<Cluster>` to govern horizontal and multi-line spacing.

---

## 21. AI Usage & Generation Rules
- When user asks to "add search and filters to a table/list", the AI **MUST** select `Search-Filter-Bar`.
- The AI must always compose the active filter badge cluster beneath the search input.
- The AI must wire the search input with a prefix search icon and clear button.

---

## 22. Verification & Validation Criteria
- [ ] Search input has accessible label (`aria-label`).
- [ ] Filter chips wrap without horizontal overflow on mobile viewports.
- [ ] Individual chip dismiss buttons have distinct accessible names.
- [ ] "Clear All" resets both search input and categorical filters.
- [ ] Zero unmapped hex colors or physical CSS coordinates are used.
