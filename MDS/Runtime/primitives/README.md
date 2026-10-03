# MDS Foundations & Primitives Runtime Engine

**Layer:** 13-Implementation / Foundations & Primitives  
**Phase:** 9.3 (Foundations & Primitives Runtime)  
**Status:** APPROVED & IMPLEMENTED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Specification:** [`MDS/13-Implementation/Phase-9.1-Implementation-Architecture.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/13-Implementation/Phase-9.1-Implementation-Architecture.md)  
**Runtime Dependencies:** Zero (Native Web Standards: CSS Cascade Layers, Custom Elements, Vanilla JS)

---

## 1. Architectural Mission & Strict Boundary

The **MDS Foundations & Primitives Runtime Engine** is the structural bedrock of the Master Design System. Positioned directly above the Token Runtime (`mds.tokens`), it establishes:
1. **Reset & Element Normalization** (`@layer mds.reset`)
2. **Global Typography, Cairo RTL Baseline & Universal Motion Safety** (`@layer mds.foundations`)
3. **18 Canonical Atomic Primitives** (`@layer mds.primitives`)

### Inviolable Boundary Rules:
- **Zero Component Inversion:** Core UI components (Buttons, Inputs, Dialogs, Cards, Tables, etc.) belong strictly to **Phase 9.4 (Core Component Runtime)** and are 100% excluded here.
- **Zero Value Invention:** Primitives never declare arbitrary hex colors, pixel margins, or magic numbers. All values are strictly bound to compiled CSS tokens via `var(--mds-*)`.
- **Parent-Owned Spacing Law:** Primitive elements NEVER declare external margins (`margin-top`, `margin-bottom`, etc.). Spacing is strictly owned and composed via Layout Primitives (`Stack`, `Inline`, `Grid`, `Cluster`).
- **100% CSS Logical Properties:** All spatial rules strictly use `inline` and `block` dimensions (`margin-inline`, `padding-inline`, `inset-inline-start`, `border-inline-start`, `text-align: start/end`). Physical directional properties (`left`, `right`, `margin-left`, `margin-right`, etc.) and `row-reverse` are strictly banned.
- **Internal Touch Target Rule:** 44×44px interaction hit target (`PressTarget`) enforced on touch devices via `@media (pointer: coarse)`.
- **AF-001 Streaming Speech Throttling:** Assistive speech synthesizer queue protection decoupled from high-frequency generative AI streaming tokens.

---

## 2. Canonical CSS Cascade Layer Order

Stylesheets are compiled into explicit native CSS Cascade Layers to guarantee deterministic specificity:

```css
@layer mds.reset, mds.tokens, mds.foundations, mds.primitives, mds.components, mds.patterns, mds.templates, mds.overrides;
```

### Hierarchy & Specificity Flow:
| Cascade Layer | File Source | Purpose |
| :--- | :--- | :--- |
| `mds.reset` | `MDS/Runtime/css/reset.css` | Box-sizing `border-box`, element normalization, responsive media. |
| `mds.tokens` | `MDS/Runtime/tokens/dist/tokens.css` | Compiled DTCG CSS custom properties across all 4 themes. |
| `mds.foundations` | `MDS/Runtime/css/foundations.css` | Cairo font, RTL leading boost (+0.15), selection highlight, universal motion safety. |
| `mds.primitives` | `MDS/Runtime/css/primitives.css` | 18 canonical layout, typography, surface, interaction, and icon primitives. |
| `mds.components` | *(Phase 9.4)* | Core interactive components (Button, Input, Card, Modal, etc.). |
| `mds.patterns` | *(Future)* | Multi-component compositions (FormGroup, SearchBar, etc.). |
| `mds.templates` | *(Future)* | Page-level templates and scaffold layouts. |
| `mds.overrides` | *(Application)* | Consumer project custom overrides and theme injections. |

---

## 3. Directory Structure

```text
MDS/Runtime/
├── css/
│   ├── mds-core.css                 # Master runtime entry point declaring canonical @layer order & imports
│   ├── reset.css                    # @layer mds.reset: Modern CSS reset and baseline normalization
│   ├── foundations.css              # @layer mds.foundations: Cairo font, RTL leading boost, reduced-motion
│   └── primitives.css               # @layer mds.primitives: Consolidated master primitive stylesheet
├── primitives/
│   ├── layout/
│   │   ├── container.css            # Standard (1152px), Wide (1440px), Fluid, responsive gutters
│   │   ├── stack.css                # 1D vertical flex, token gaps (xs-xl), dividers
│   │   ├── inline.css               # 1D horizontal flex, token gaps, wrap, responsive collapse
│   │   ├── grid.css                 # 12-column responsive fluid grid (4/8/12 cols), auto-fit tiles
│   │   └── cluster.css              # Multi-element wrapping flex layout
│   ├── typography/
│   │   └── typography.css           # Text (sizes, weights, soft-wrap), Heading 1-6, Label, Caption, HelperText, Numeric, Code
│   ├── surface/
│   │   └── surface.css              # Surface Depth Triad: Canvas, Surface, Raised L1, Floating L2, Overlay L3
│   ├── interaction/
│   │   ├── press-target.css         # 44×44px hit-box touch expansion (@media pointer: coarse)
│   │   ├── focus-ring.css           # 2px thick :focus-visible outline, interactive base
│   │   ├── visually-hidden.css      # Accessible clip rect & clip-path with focusable skip-link state
│   │   ├── reduced-motion.css       # Instant transition and motion collapse utilities
│   │   ├── focus-trap.js            # WAI-ARIA FocusTrap controller & <mds-focus-trap> Custom Element
│   │   └── live-region.js           # LiveRegion announcer & <mds-live-region> Custom Element (AF-001)
│   ├── icon/
│   │   └── icon.css                 # 24×24 box, 20×20 optical grid, sizes xs-xl, stroke weights, RTL scaleX(-1)
│   ├── tests/
│   │   ├── __init__.py              # Test package
│   │   └── test_primitives_runtime.py # 30 automated verification tests (100% passing)
│   └── README.md                    # This architecture document
```

---

## 4. The 18 Canonical Primitives

### 4.1 Layout Primitives (5)
1. **Container (`.mds-container`):**
   - `.mds-container--standard`: Maximum width `var(--mds-container-standard, 1152px)`.
   - `.mds-container--wide`: Maximum width `var(--mds-container-wide, 1440px)`.
   - `.mds-container--fluid`: Maximum width `100%`.
   - Responsive horizontal gutters: `16px` (mobile), `24px` (tablet), `32px` (desktop).
2. **Stack (`.mds-stack`):**
   - 1D vertical flex column layout.
   - Gap modifiers: `--gap-xs` (`4px`), `--gap-sm` (`8px`), `--gap-md` (`16px`), `--gap-lg` (`24px`), `--gap-xl` (`32px`).
   - Content divider support via `.mds-stack--divided`.
3. **Inline (`.mds-inline`):**
   - 1D horizontal flex row layout.
   - Gap modifiers: `--gap-xs` through `--gap-xl`.
   - Modifiers: `.mds-inline--wrap`, `.mds-inline--collapse-sm` (collapses to vertical stack on mobile `<768px`).
4. **Grid (`.mds-grid`):**
   - Responsive 12-column CSS Grid: 4 columns (mobile), 8 columns (tablet), 12 columns (desktop `1024px+`), 32px gutter (wide `1440px+`).
   - Column span modifiers: `.mds-grid__col--1` through `.mds-grid__col--12`.
   - Auto-fitting fluid tile layout: `.mds-grid--auto-tiles` (`repeat(auto-fit, minmax(280px, 1fr))`).
5. **Cluster (`.mds-cluster`):**
   - Multi-element horizontal wrapping flex layout for tags, badges, and chips.

### 4.2 Typography Primitives (7)
1. **Text (`.mds-text`):**
   - Size modifiers: `--size-xs` (`12px`) through `--size-4xl` (`36px`).
   - Weight modifiers: `--weight-regular` (`400`), `--weight-medium` (`500`), `--weight-semibold` (`600`), `--weight-bold` (`700`).
   - Soft-Wrap Invariant (`.mds-text--soft-wrap`): Strictly wraps descriptive text (`overflow-wrap: break-word; white-space: normal;`). No `text-overflow: ellipsis` on informational text.
2. **Heading (`.mds-heading`):**
   - Strict hierarchical levels `.mds-heading--1` through `.mds-heading--6` mapped to Cairo typography scale with tight line-height (`1.25`).
3. **Label (`.mds-label`):**
   - Form control label primitive (`14px`, medium weight `500`).
4. **Caption (`.mds-caption`):**
   - Secondary auxiliary caption text (`12px`, secondary text color).
5. **HelperText (`.mds-helper-text`):**
   - Guidance copy below form fields with semantic state variants (`.mds-helper-text--error`, `.mds-helper-text--success`).
6. **Numeric (`.mds-numeric`):**
   - Tabular numerals (`font-variant-numeric: tabular-nums`) for currency, telemetry, financial data, and countdowns.
7. **Code (`.mds-code`):**
   - Monospace snippet display using `var(--mds-font-family-mono)` (JetBrains Mono).

### 4.3 Surface Primitives (1 - Surface Depth Triad)
- **Canvas (`.mds-canvas`):** Base background plane (`var(--mds-color-surface-canvas)`).
- **Surface (`.mds-surface`):** Resting content surface (`var(--mds-color-surface-default)`), subtle border (`--mds-border-width-thin`), radius (`--mds-radius-md`).
- **Raised (`.mds-surface--raised`):** Elevation Level 1 (`--mds-elevation-level1`).
- **Floating (`.mds-surface--floating`):** Elevation Level 2 (`--mds-elevation-level2`), menus, popovers, autocomplete dropdowns (`z-index: 300`).
- **Overlay (`.mds-surface--overlay`):** Elevation Level 3 (`--mds-elevation-level3`), modal dialogs, flyouts, drawers (`z-index: 400`).

### 4.4 Interaction & Accessibility Primitives (4)
1. **PressTarget (`.mds-press-target`):**
   - Enforces the canonical MDS internal 44×44px hit-box requirement on touch devices via an invisible centered pseudo-element active only when `@media (pointer: coarse)`.
2. **FocusRing (`.mds-focus-ring`):**
   - Accessible keyboard indicator (`outline: var(--mds-border-width-thick) solid var(--mds-color-focus-ring)` with `outline-offset: 2px`).
   - Suppressed on mouse clicks via `:not(:focus-visible)`.
3. **VisuallyHidden (`.mds-visually-hidden`):**
   - Screen-reader accessible hiding (`clip: rect(0, 0, 0, 0); clip-path: inset(50%); width: 1px; height: 1px; margin: -1px;`).
   - Focusable variant (`.mds-visually-hidden--focusable:focus`) restores full visibility when navigated to via keyboard (skip links).
4. **ReducedMotion (`.mds-motion--instant`, `.mds-motion--collapse`):**
   - Instant duration override and complete transition/animation collapse under `@media (prefers-reduced-motion: reduce)`.
5. **FocusTrap (`FocusTrap` / `<mds-focus-trap>`):**
   - Component-agnostic keyboard containment controller and W3C Custom Element. Traps `Tab` and `Shift+Tab`, intercepts `Escape`, and restores previous focus upon deactivation.
6. **LiveRegion (`LiveRegion` / `<mds-live-region>`):**
   - AF-001 compliant speech buffer protection announcer. Implements dynamic queue throttling (`throttleMs=1000`) and decoupled streaming methods (`startStreaming`, `updateStreamingProgress`, `completeStreaming`).

### 4.5 Icon Primitive (1)
- **Icon (`.mds-icon`):**
  - Geometry: 24×24 bounding box with 20×20 optical grid.
  - Optical sizes: `.mds-icon--size-xs` (`14px`), `.mds-icon--size-sm` (`16px`), `.mds-icon--size-md` (`20px`), `.mds-icon--size-lg` (`24px`), `.mds-icon--size-xl` (`32px`).
  - Stroke taxonomy: `.mds-icon--stroke-regular` (`1.5px`), `.mds-icon--stroke-thick` (`2.0px`).
  - RTL Directional Mirroring: Strictly for directional icons (chevrons, arrows, send) via `.mds-icon--mirror-rtl` (`transform: scaleX(-1)` under `:lang(ar)` and `[dir="rtl"]`). Neutral icons remain unmirrored.

---

## 5. Verification & Testing

The primitives runtime engine is validated via an automated test suite executed with Python's standard library `unittest`:

```powershell
python "MDS/Runtime/primitives/tests/test_primitives_runtime.py"
```

### Test Coverage (30 Executable Tests):
- **Inventory Verification:** All 18 modular CSS and JS files exist.
- **Cascade Layer Hierarchy:** Canonical 8-layer ordering declared in `mds-core.css` and all stylesheets correctly wrapped.
- **Component Isolation:** 0 component classes found (`.mds-button`, `.mds-input`, `.mds-dialog`, etc.).
- **Logical Properties & RTL:** 0 physical `left`/`right`, `margin-left/right`, `padding-left/right`, `border-left/right`, and 0 `row-reverse`.
- **Token Consumption:** 0 raw hex colors (`#...`), 0 raw `rgb/hsl` calls, 100% token binding via `var(--mds-*)`.
- **Layout Invariants:** Standard container 1152px, Wide container 1440px, Fluid container 100%, 12-column grid.
- **Typography Invariants:** Soft-wrap preservation, 0 ellipsis on descriptive text, tabular numbers, monospace code.
- **Depth Triad Invariants:** Canvas, Surface, Raised, Floating, Overlay elevation levels.
- **Accessibility Invariants:** 44px touch target, 2px focus ring, accessible clip rect, reduced-motion overrides.
- **JavaScript Controllers:** FocusTrap containment/restoration and LiveRegion AF-001 streaming throttling.
- **Icon Taxonomy:** Optical scale xs-xl, stroke widths, RTL mirroring.
