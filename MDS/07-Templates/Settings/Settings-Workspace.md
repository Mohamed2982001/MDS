# MDS Template: Settings-Workspace (`MDS-TMP-005`)

**Document Layer:** 07-Templates / Settings  
**Status:** APPROVED (Phase 8.1.3 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-17  

---

## 1. Template ID
`MDS-TMP-005`

## 2. Name
Settings & Preferences Workspace Template

## 3. Intent
To provide an authoritative, scalable master-detail environment for browsing application preferences, system configurations, security controls, and account settings organized via a persistent vertical category navigation rail.

## 4. Problem Solved
Prevents confusing, deeply nested settings pages by establishing a clear two-tier structure (Category Rail + Active Settings Section) supporting both Instant Autosave and Batched Form updates with unsaved changes protection.

## 5. When to Use
- For application configuration portals, user profile settings, organization preferences, and security/API management.
- When an application has multiple distinct categories of configuration (General, Security, Notifications, Billing, Team).

## 6. When Not to Use
- For linear multi-step wizards: Use `Form-Edit` (`MDS-TMP-004`) instead.
- For managing collections of business records: Use `List-Management` (`MDS-TMP-002`) instead.
- For deep inspection of single business records: Use `Detail-Entity` (`MDS-TMP-003`) instead.

## 7. Page Regions
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Region 1: Global Navigation (App Shell Header)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 2: Page Header (Title "Settings", Search Preferences Input)          │
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 3: Settings Master-Detail Layout (1:3 Column Ratio)                  │
│ ┌─────────────────────────────┐ ┌─────────────────────────────────────────┐ │
│ │ Category Navigation Rail    │ │ Active Preference Section Workspace     │ │
│ │ ├── Account / Profile       │ │ ├── Section Header (Title & Intro)      │ │
│ │ ├── Security & Auth         │ │ ├── Form-Section 1 (Toggles & Inputs)   │ │
│ │ ├── Notifications           │ │ ├── Form-Section 2 (Advanced Config)    │ │
│ │ ├── Billing & Plans         │ │ └── Save / Reset Action Bar (if batched)│ │
│ │ └── Danger Zone (Revoke)    │ │                                         │ │
│ └─────────────────────────────┘ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 8. Region Hierarchy
`Global Navigation` $\to$ `Page Header` $\to$ `Settings Master-Detail Layout` (Category Rail + Section Workspace) $\to$ `Action Bar`.

## 9. Pattern Composition
- **`Page-Header` (`MDS/05-Patterns/Navigation/Page-Header.md`):** Title, search settings shortcut, overall status indicators.
- **`Form-Section` (`MDS/05-Patterns/Forms/Form-Section.md`):** Structured preference groupings (e.g. "Password & Authentication", "Two-Factor Auth").
- **`Confirmation-Dialog` (`MDS/05-Patterns/Feedback/Confirmation-Dialog.md`):** For unsaved changes warnings or high-impact destructive settings (e.g. Delete Account).
- **`Empty-State` (`MDS/05-Patterns/Feedback/Empty-State.md`):** For empty configuration lists (e.g. "No API Keys generated yet").

## 10. Workflow Slots
- **`Settings-Update` (`MDS/06-Workflows/Settings/Settings-Update.md`):** Governs both Instant Autosave (optimistic toggle with green tick) and Batched Settings (dirty detection and save button).
- **`Destructive-Action` (`MDS/06-Workflows/Actions/Destructive-Action.md`):** For revoking keys, resetting configurations, or account termination.
- **`Error-Recovery` (`MDS/06-Workflows/Recovery/Error-Recovery.md`):** Handles background autosave failures with retry banner.

## 11. Component Dependencies
- `Button`, `Link` (Actions)
- `Switch`, `Checkbox`, `Radio`, `Input`, `Select`, `Field` (Inputs)
- `Badge`, `Card` (Data Display)
- `Alert`, `Spinner`, `Skeleton` (Feedback)
- `Surface`, `Stack`, `Inline`, `Grid`, `Container` (Primitives)

## 12. Content Slots
- `slot="category-nav"`: Navigation rail items with icons, titles, and optional count/status badges.
- `slot="section-header"`: Active category title, description, and documentation link.
- `slot="section-body"`: The preference fields and form sections.
- `slot="section-actions"`: Save/Cancel buttons (when operating in Batched mode).

## 13. Required vs Optional Regions
- **Required:** Page Header, Category Navigation Rail, Active Preference Section Workspace.
- **Optional:** Search Preferences input, Save/Cancel action bar (omitted in pure Instant Autosave mode).

## 14. Responsive Composition
- **Compact (< 768px):** Master-Detail recomposes into a drill-down navigation pattern: Category Rail is shown first as a full-width list; tapping a category navigates into that section's view with a prominent "Back to Settings" link.
- **Standard (768px – 1151px):** Category Rail displays in a compact 200px column; Section Workspace displays in remaining space.
- **Wide (1152px – 1439px):** Canonical 1152px container max-width; 240px Category Rail + 800px Section Workspace.
- **Full ($\ge$ 1440px):** 1440px wide container (`container.xl`); centered layout preserving optimal form field widths.

## 15. Mobile Composition
- Converts horizontal dual-pane to a 2-level drill-down stack.
- Switches and checkboxes feature minimum 44px hit-box touch expansion.
- Sticky action bar pinned to bottom if in batched edit mode.

## 16. RTL Behavior
- Category Navigation Rail sits on inline-start (`right` in RTL).
- Section Workspace sits on inline-end (`left` in RTL).
- Active category selection indicator renders on the inline-start edge.
- Zero `row-reverse` hacks used.

## 17. Accessibility Structure
- `<nav>` landmark with `aria-label="Settings Categories"` surrounds the rail.
- Active category item has `aria-current="page"`.
- `<main>` landmark surrounds the Active Preference Section Workspace.
- Form controls feature explicit `aria-describedby` linking to their explanation text.

## 18. Experience States
- **`Default / Populated`:** Active category loaded with current preference states.
- **`Saving (Autosave)`:** Subtle "Saving..." indicator in header; converts to "Saved" checkmark upon success.
- **`Dirty (Batched)`:** Unsaved changes bar appears at bottom with "Save changes" and "Discard".
- **`Error`:** Error alert in header: "Failed to save settings — Click to retry".
- **`No Access`:** If user lacks administrative permissions for a category (e.g. Billing), displays a restricted access card.

## 19. Loading Strategy
Category Rail renders instantly; Section Workspace displays a geometric skeleton with 3 toggle skeletons and 2 field skeletons. Zero layout shift.

## 20. Error Strategy
Background autosave failure displays an inline retry button next to the failed toggle; batched form failure retains all user inputs in memory.

## 21. Empty Strategy
For list-based preferences (e.g. "Authorized Devices"), renders `Empty-State` with a "Connect Device" button.

## 22. Recovery Strategy
Switching categories while batched changes are unsaved triggers a `Confirmation-Dialog` ("Discard unsaved changes?").

## 23. Density Behavior
- **Comfortable:** Standard toggle switches, 16px list item padding.
- **Compact:** 12px list item padding, compact switches, tighter vertical spacing.

## 24. Theme/Mode Behavior
- **Light:** Rail background `#F8FAFC`, active item background `#FFFFFF`, Section `#FFFFFF`.
- **Dark:** Rail background `#0B0F19`, active item `#1E293B`, Section `#0F172A`.
- **High Contrast:** 2px high-visibility focus borders and distinct category selection outlines.

## 25. AI Integration
Optional "AI Preference Optimizer" card: suggests optimal privacy or notification settings based on team usage patterns with explicit one-click apply and review.

## 26. Navigation Context
Breadcrumb: `Home > Settings > [Category Name]`.

## 27. Focus Management
Selecting a category moves focus to the category `<h1>` heading in the section workspace; keyboard arrow keys allow traversing the category rail.

## 28. Motion Behavior
Category transitions use a subtle 150ms cross-fade; autosave indicator fades in smoothly; collapses to 0ms in reduced motion mode.

## 29. Token Dependencies
`container.lg`, `container.xl`, `space.3`, `space.4`, `space.6`, `color.surface.*`, `color.action.*`.

## 30. Anti-Patterns
- ❌ Do NOT force users to scroll through one massive single-page list containing 50 settings.
- ❌ Do NOT discard unsaved changes silently when user clicks a different category.
- ❌ Do NOT mix instant autosave toggles and batched save buttons in the same section without clear visual separation.

## 31. Validation Requirements
Verified by `run_tests.py`, HTML showcase testbed, and 100% token usage.

## 32. Selection Criteria
Select when user intent is configuring preferences, security controls, notification rules, or administrative options organized into categories.
