# MDS Pattern: Empty-State

**Document Layer:** 05-Patterns / Feedback  
**Status:** STABLE (Phase 6 Implementation)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-16  

---

## 1. Purpose
The **Empty-State** pattern provides an empathetic, informative, and actionable placeholder when a container, table, or page has no content to display. It guides the user on why the screen is empty and offers clear recovery steps.

---

## 2. User Intent
The user intends to understand why no data is visible (e.g., first-time user onboarding, filtered search returned zero results, items cleared) and how to proceed without feeling stuck or suspecting a system malfunction.

---

## 3. Problem Solved
Eliminates confusion and abandonment caused by blank screens or uninformative "No data" text. Transforms a zero-data state into an engaging onboarding or filter-reset opportunity.

---

## 4. When to Use
- First-time user experience (onboarding) when an account has no created projects or records.
- When an active search or filter combination yields zero matches.
- When an inbox, cart, or task list has been completely cleared.
- Error states where data failed to load and user action is required to retry.

---

## 5. When Not to Use
- During asynchronous initial data loading: Use `Skeleton` placeholders or `Spinner`.
- For inline form validation feedback: Use `Field` helper/error text.
- For short transient notifications: Use `Alert`.

---

## 6. Composition Architecture

```text
┌───────────────────────────────────────────────────────────────────────────┐
│ Empty-State Container (Surface.default or Card, padding.8, align="center")│
│                                                                           │
│  Stack (align="center", gap="md", max-width="440px")                      │
│   ├── Visual Anchor Slot (Icon / Illustration, size="48px" to "64px")     │
│   │    └── Muted brand icon / empty box glyph in neutral.400              │
│   │                                                                       │
│   ├── Text Group (Stack align="center", gap="xs")                         │
│   │    ├── Heading H3 (font.size.lg, font.weight.semibold)                │
│   │    │    "No projects found"                                           │
│   │    └── Description (font.size.sm, color="text.secondary", wrap=true)  │
│   │         "You haven't created any projects yet, or your active         │
│   │          filters didn't return any matches."                          │
│   │                                                                       │
│   └── Action Bar (Inline justify="center", gap="sm")                      │
│        ├── Secondary Action (Optional): Button("Reset Filters", secondary)│
│        └── Primary Action: Button("Create First Project", primary)        │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Required Components
- `Stack` (Layer 03 Layout Primitive — centered alignment)
- `Heading` (Layer 03 Typography Primitive — H3 or H4)
- `Text` (Layer 03 Typography Primitive — descriptive body copy)
- `Button` (Layer 04 Actions Component — primary call to action)
- `Icon` (Layer 03 Primitive — semantic visual anchor)

---

## 8. Optional Components
- `Button` (Secondary Action — for "Clear Filters" or "Read Docs")
- `Card` (Layer 04 Data Display Component — when embedded within a section or dashboard tile)
- `Link` (Layer 04 Actions Component — for external documentation links)

---

## 9. Information Hierarchy
1. **Visual Cue:** Centered muted icon or illustration signals the nature of the zero state.
2. **Clear Diagnosis:** Bold, concise title states the reality ("No projects found").
3. **Contextual Explanation:** 1–2 sentences explaining why and what can be done.
4. **Primary Recovery Action:** Highly prominent primary button offering the solution.

---

## 10. Interaction Model
- Clicking the Primary CTA immediately opens the creation modal/flow.
- Clicking the Secondary CTA resets active filters or navigates to help.
- Tab sequence moves logically: `Visual Icon (if interactive)` $\to$ `Secondary Action` $\to$ `Primary Action`.

---

## 11. Experience States
- **Onboarding Empty:** Focuses on creation ("Create your first invoice").
- **Filter Empty:** Focuses on clearing filters ("Clear all filters to see results").
- **Cleared / Success Empty:** Celebratory ("Inbox zero — you're all caught up!").
- **Permission Empty:** Explains access limitations ("You don't have access to this team").

---

## 12. Responsive Behavior
- **Compact (<640px):**
  - Action buttons stack vertically with full width (`width: 100%`).
  - Container padding reduces to `space.6` (24px).
  - Max text width set to 100%.
- **Standard & Wide (>640px):**
  - Action buttons align horizontally inline.
  - Text container constrained to max 440px to ensure optimal reading line length.

---

## 13. Accessibility (a11y)
> *Standards Scope:* Implemented accessibility behaviors were validated against selected WCAG success criteria where applicable. Comprehensive cross-platform assistive technology testing remains deferred to Phase 8.
- The entire empty state container has `role="region"` with `aria-labelledby="empty-title-id"`.
- If the icon is decorative, it must have `aria-hidden="true"`.
- Interactive action buttons retain minimum $\ge 44 \times 44\text{px}$ touch targets where applicable via `PressTarget`.
- Title text satisfies $\ge 4.5:1$ contrast against surface background.

---

## 14. RTL & Logical Progression
- Content is horizontally centered along the inline axis.
- Action buttons follow logical inline reading order (`inline-start` $\to$ `inline-end`).
- Any directional icons (e.g. arrow CTA) flip appropriately in RTL viewports.

---

## 15. Density Behavior
- **Comfortable:** Container padding `space.8` (32px), icon `64px`, gap `space.4`.
- **Compact:** Container padding `space.6` (24px), icon `48px`, gap `space.3`.
- **Dense:** Embedded in table/card tiles. Padding `space.4` (16px), icon `32px`.

---

## 16. Motion & Animation
- Entrance fade-in uses 250ms (`var(--mds-motion-normal)`) with `var(--mds-motion-ease-standard)`.
- Collapses to 0s under `prefers-reduced-motion: reduce`.

---

## 17. Token Usage
- Title Color: `color.text.primary`
- Description Color: `color.text.secondary`
- Icon Color: `color.neutral.400`
- Background: `color.surface.default` (Canvas-embedded) or `color.surface.raised` (Card-embedded)
- Button Token: `component.button.primary.background.default`

---

## 18. Contextual Variants
- **Full-Page Empty State:** Dominates viewport; used for empty section roots.
- **Embedded Tile Empty State:** Contained inside a card, tabpanel, or table container.
- **Search Zero-Result State:** Specifically tuned for query failure with filter reset action.

---

## 19. Composition Rules
- Every empty state MUST include at least one action button. Zero-action empty states are strictly forbidden.
- Explanatory copy must never be truncated; allow natural 2+ line wrapping.

---

## 20. Anti-Patterns & Prohibitions
- **NO DEAD ENDS:** Never display an empty state without an actionable button.
- **NO BLAME LANGUAGE:** Avoid accusatory phrasing like "You entered an invalid query". Use "No items match your search criteria".
- **NO RAW INVENTIONS:** Do not create custom icon circle containers with hardcoded pixel shadows.

---

## 21. AI Usage & Generation Rules
- When the query or dataset returns length 0, the AI **MUST** render `Empty-State`.
- The AI must provide both a descriptive title and a primary recovery action.
- The AI must center-align the stack elements.

---

## 22. Verification & Validation Criteria
- [ ] Title has semantic heading element (`h3` or `h4`).
- [ ] Primary recovery button is present and clearly visible.
- [ ] Decorative icon has `aria-hidden="true"`.
- [ ] Text wrapping enabled without ellipsis.
- [ ] 0 raw hex colors or physical coordinates.
