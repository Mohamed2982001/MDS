# MDS Pattern: Data-List-Card

**Document Layer:** 05-Patterns / Data  
**Status:** STABLE (Phase 6 Implementation)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-16  

---

## 1. Purpose
The **Data-List-Card** pattern displays an individual entity record within a collection, organizing its title, status badge, key metadata pairs, and contextual actions into a responsive, highly scannable card format.

---

## 2. User Intent
The user intends to quickly scan, review, and take direct action on specific items in a business list or catalog (e.g. project list, order history, team members, customer accounts).

---

## 3. Problem Solved
Solves the mobile usability issues of wide tabular displays. On smaller viewports or in content-rich dashboards, horizontal tables break and cause awkward horizontal scrolling; `Data-List-Card` packages essential entity metrics into an adaptive vertical card surface.

---

## 4. When to Use
- Browsing entity lists where each item has 3 to 6 key metadata attributes.
- Mobile and tablet views of data collections.
- Dashboard overview widgets where full data tables are too dense or visually rigid.

---

## 5. When Not to Use
- For dense tabular data requiring cross-row numerical comparison: Use `Table`.
- Do NOT use for virtualized infinite lists (deferred per Section 34).
- For pure text paragraphs without metadata: Use a standard article or card layout.

---

## 6. Composition Architecture

```text
┌───────────────────────────────────────────────────────────────────────────┐
│ Data-List-Card (Surface.raised, border, radius.md, padding.4)             │
│                                                                           │
│  Card Header (Inline justify="space-between" align="center")              │
│   ├── Heading H4 / Title (Text font.weight.semibold, softWrap: true)      │
│   └── Badge (Status intent: 'success', 'warning', 'neutral', 'brand')     │
│                                                                           │
│  Card Body / Metadata Cluster (Grid columns="2" or Cluster gap="sm")      │
│   ├── Key-Value Pair 1: [Label: "Client"] [Text: "Acme Corp"]             │
│   ├── Key-Value Pair 2: [Label: "Due Date"] [Numeric: "2026-10-15"]       │
│   └── Key-Value Pair 3: [Label: "Amount"] [Numeric: "$12,450.00" (tnum)]  │
│                                                                           │
│  Card Footer (Inline justify="space-between" align="center" gap="sm")     │
│   ├── Timestamp / Secondary Info (Caption color="text.secondary")         │
│   └── Action Group (Inline gap="xs")                                      │
│        ├── Secondary Action: Button(variant="ghost", size="sm", "View")   │
│        └── Primary Action:   Button(variant="secondary", size="sm", "Edit")
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Required Components
- `Card` (Layer 04 Data Display Component — Surface + Depth Triad)
- `Badge` (Layer 04 Data Display Component — status indicator)
- `Text` / `Heading` (Layer 03 Typography Primitives)
- `Button` (Layer 04 Actions Component — contextual card actions)
- `Inline` (Layer 03 Layout Primitive)
- `Stack` (Layer 03 Layout Primitive)

---

## 8. Optional Components
- `IconButton` (Layer 04 Actions Component — for kebab action menu `...`)
- `Checkbox` (Layer 04 Input Component — for bulk multi-selection mode)
- `Skeleton` (Layer 04 Feedback Component — for card loading placeholder)

---

## 9. Information Hierarchy
1. **Primary Eye Anchor:** Entity Title and Status Badge in the header.
2. **Supporting Data:** Key metadata attributes in the central grid.
3. **Context & Actions:** Timestamp and action buttons anchored in the footer.

---

## 10. Interaction Model
- The whole card may be clickable (`cursor: pointer`), or actions may be contained strictly within the footer buttons.
- Hover state subtly elevates card shadow (`elevation.level1` to `elevation.level2`) and highlights border.
- Focus ring highlights cleanly on card boundary if the card itself is an interactive link/button.

---

## 11. Experience States
- **Resting:** Standard card border and surface background.
- **Hover:** Elevated surface with subtle border transition (150ms).
- **Selected (Bulk Mode):** Active brand border highlight (`color.border.focus`) with checked checkbox.
- **Loading:** Entire card renders a matching `Skeleton` shimmer layout.
- **Disabled / Archived:** Card content dims with `opacity.disabled = 0.38`.

---

## 12. Responsive Behavior
- **Compact (<640px):**
  - Card takes 100% viewport width.
  - Metadata cluster stacks vertically or uses a 1-column layout.
  - Action buttons expand or align to full width in footer.
- **Standard & Wide (>640px):**
  - Cards can be arranged in a 2 or 3-column responsive grid (`Grid columns="repeat(auto-fill, minmax(280px, 1fr))"`).

---

## 13. Accessibility (a11y)
> *Standards Scope:* Implemented accessibility behaviors were validated against selected WCAG success criteria where applicable. Comprehensive cross-platform assistive technology testing remains deferred to Phase 8.
- If the card is clickable, it must not contain nested interactive buttons (to prevent invalid nested interactive controls). Instead, use a stretched link or keep actions distinct in the footer.
- Status badge must have high contrast text ($\ge 4.5:1$).
- Interactive action buttons maintain minimum $\ge 44 \times 44\text{px}$ touch targets where applicable via `PressTarget`. Static data labels are exempt.

---

## 14. RTL & Logical Progression
- Progresses along the inline axis: Entity title aligns to `inline-start` (right in RTL), status badge aligns to `inline-end` (left in RTL).
- Numeric values maintain standard LTR numeral formatting with `font-variant-numeric: tabular-nums`.

---

## 15. Density Behavior
- **Comfortable:** Card padding `space.4` (16px), gap `space.3` (12px).
- **Compact:** Card padding `space.3` (12px), gap `space.2` (8px).
- **Dense:** Card padding `space.2` (8px), gap `space.1` (4px).

---

## 16. Motion & Animation
- Card hover elevation uses 150ms (`var(--mds-motion-fast)`) with `var(--mds-motion-ease-standard)`.
- Collapses to 0ms under `prefers-reduced-motion: reduce`.

---

## 17. Token Usage
- Surface: `color.surface.raised`
- Border: `color.border.default`
- Hover Border: `color.neutral.400`
- Shadow: `elevation.level1` (Resting), `elevation.level2` (Hover)
- Title: `font.size.base`, `font.weight.semibold`
- Radius: `radius.md`

---

## 18. Contextual Variants
- **Simple Entity Card:** Title + Badge + Single Action.
- **Detailed Metric Card:** Includes multiple key-value pairs and progress indicator.
- **Selectable Bulk Card:** Includes leading checkbox for bulk actions.

---

## 19. Composition Rules
- Never use external margins; spacing between cards in a list is owned by the parent `<Stack>` or `<Grid>`.
- Card must clearly distinguish resting vs interactive hover states.

---

## 20. Anti-Patterns & Prohibitions
- **NO NESTED CLICKS:** Never put a `<button>` inside an `<a>` that wraps the whole card.
- **NO OVERCROWDED METADATA:** Do not place more than 6 metadata items in a single card; use a detail modal or full page view instead.

---

## 21. AI Usage & Generation Rules
- When user asks to "display records on mobile" or "create an entity card list", the AI **MUST** select `Data-List-Card`.
- The AI must place the status badge in the header alongside the title.
- The AI must use `Card` as the outer surface wrapper.

---

## 22. Verification & Validation Criteria
- [ ] Card uses `Surface.raised` and `elevation.level1`.
- [ ] Status badge uses approved semantic intent tokens.
- [ ] Tab navigation traverses header $\to$ metadata $\to$ footer actions sequentially.
- [ ] Touch hit area $\ge 44 \times 44\text{px}$ on all buttons.
- [ ] 0 raw hex colors or physical CSS coordinates.
