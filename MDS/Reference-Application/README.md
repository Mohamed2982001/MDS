# MDS Workspace — Reference Application

**Application:** MDS Workspace  
**Layer:** 13-Implementation (Phase 9.6)  
**Status:** **READY FOR FINAL AUDIT**  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Standard:** 100% Pure Modern Web Standards, Zero NPM Runtime Dependencies  

---

## 1. Executive Summary & Architectural Mission

**MDS Workspace** is the official Reference Application for the **Master Design System (MDS)**. It proves that the complete compositional chain:

$$\text{Tokens} \to \text{Primitives} \to \text{Components} \to \text{Patterns} \to \text{Workflows} \to \text{Templates} \to \text{Application}$$

is 100% operational, cohesive, and resilient across multi-screen enterprise scenarios without requiring the application to invent its own design system, patch component CSS, or introduce external frameworks.

---

## 2. Directory Structure & File Topology

```text
MDS/Reference-Application/
├── index.html                   # Master application shell, semantic landmarks, header toolbar
├── app.css                      # Application stylesheet strictly in @layer mds.overrides
├── app.js                       # Vanilla ES Module controller, router, reactive store, mock actions
├── README.md                    # Operational manual and architectural documentation
├── fixtures/
│   └── workspace_data.json      # Deterministic fixtures (items, tasks, users, activities, AI corpus, settings)
└── tests/
    ├── __init__.py
    └── test_reference_app.py    # 15-test automated verification suite
```

---

## 3. How to Run Locally

Because the application uses native ECMAScript Modules (`import ... from "../Runtime/..."`) and fetches `workspace_data.json`, browsers enforce CORS origin security on `file://` URLs. The application must be served over HTTP:

### Using Python (Native):
```powershell
# From the workspace root:
python -m http.server 8000
```
Then navigate to:
```text
http://localhost:8000/MDS/Reference-Application/
```

### Using Node.js / npx (Alternative):
```powershell
npx serve .
```

---

## 4. Information Architecture & Canonical Screens

The application realizes all **6 canonical templates** across **11 distinct screens**:

1. **Screen 1: Overview (`#/overview`):** Dashboard Overview Template (`MDS-TMP-001`). KPI Metric Cards, Priority Tasks list (`Data-List-Card`), recent activity feed.
2. **Screen 2: Items List (`#/items`):** List Management Template (`MDS-TMP-002`). Tabbed record management (All, Favorites, Archived), Search-Filter Bar (`MDS-PAT-002`), Table with focusable container (`AF-002`), Composed Pager.
3. **Screen 3: Item Detail (`#/items/detail`):** Detail Entity Template (`MDS-TMP-003`). Breadcrumbs trail, two-column split, tabbed metadata, safe Destructive Confirmation modal with Cancel-first initial focus (`AF-002`).
4. **Screen 4: Item Edit (`#/items/edit`):** Form Edit Template (`MDS-TMP-004`). Form Sections (`MDS-PAT-001`), labeled fields, dirty state warning, optimistic save bar.
5. **Screen 5: Tasks (`#/tasks`):** Workflow Task Engine. Status filter tabs, task lifecycle cards, status advancement triggers (`TODO` $\to$ `IN_PROGRESS` $\to$ `REVIEW` $\to$ `DONE`).
6. **Screen 6: AI Workspace (`#/ai-workspace`):** AI Workspace Template (`MDS-TMP-006`). 5-stage Human-in-the-Loop generator with throttled `LiveRegion` (`AF-001`), streaming output, and `AI-Result-Review` approval/rejection card.
7. **Screen 7: Activity (`#/activity`):** Audit Trail (`MDS-TMP-003` variant). Chronological event stream with tabular-nums timestamps, actor avatars, and event tags.
8. **Screen 8: Settings — General (`#/settings/general`):** Settings Workspace (`MDS-TMP-005`). Workspace name, timezone, auto-save toggles.
9. **Screen 9: Settings — Appearance (`#/settings/appearance`):** Settings Workspace. Real-time dynamic switcher for Light/Dark/High-Contrast, Soft/Refined/Expressive presets, Comfortable/Compact density, and LTR/RTL.
10. **Screen 10: Settings — Notifications (`#/settings/notifications`):** Settings Workspace. Communication channel switches and frequency selectors.
11. **Screen 11: Settings — Access & Security (`#/settings/access`):** Settings Workspace. User role table and Danger Zone panel with destructive delete dialog.

---

## 5. Mock Roles & Permissions Simulation

The top toolbar includes an active **Role Switcher**:
- **Administrator:** Unrestricted master authority; can delete items and workspace.
- **Manager:** Can edit items, advance tasks, and manage operational records.
- **Reviewer:** Dedicated authority over AI-generated outputs (`Approve & Apply`).
- **User:** Read-only access; attempting a destructive delete simulates a **`Permission Denied`** state.

---

## 6. Experience States Tester (Simulation Bar)

The bottom sticky toolbar enables testers to force system-wide experience states on demand:
- **Normal:** Standard populated state.
- **Loading:** Renders skeleton loaders across the dashboard.
- **Empty:** Simulates 0 records found with an accessible `Empty-State` pattern and reset trigger.
- **Error:** Simulates a network failure banner with an interactive `Retry` recovery action.

---

## 7. Responsive Recomposition Strategy

- **Desktop ($\ge 1024\text{px}$):** Persistent 260px vertical sidebar, multi-column dashboard grids, expanded search bars.
- **Tablet ($768\text{px} - 1023\text{px}$):** Slim/compact 72px iconized sidebar, two-column form collapse, table horizontal scroll with focus ring.
- **Mobile ($< 768\text{px}$):** Collapsed sidebar accessible via header menu toggle button, single-column stacked forms, full-width action buttons, dialogs converted to bottom sheets.

---

## 8. Inviolable Architectural Invariants

- **Zero Runtime Mutations:** Operates strictly as a consumer of `MDS/Runtime/`.
- **Zero NPM Dependencies:** Pure HTML5, CSS Custom Properties, ES Modules, Custom Elements.
- **100% CSS Logical Properties:** Zero physical `left`/`right`/`margin-left/right` properties.
- **Zero Functional `row-reverse`:** Enforces WCAG 2.4.3 focus order protection.
- **Zero Hardcoded Hex Colors:** 100% bound to `var(--mds-*)`.
- **Dense Density Tier Deferred:** Formally disabled in settings.
