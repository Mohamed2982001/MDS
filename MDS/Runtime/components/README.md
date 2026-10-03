# MDS Component Runtime Engine (Layer 04)

**Architecture Layer:** Layer 13 (Implementation / Core Components)  
**Status:** DELIVERED & APPROVED (Phase 9.4 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Standard:** Modern Web Standards (HTML5 / CSS Custom Properties / W3C Custom Elements)  

---

## 1. Overview & Architecture

The **MDS Component Runtime Engine** provides the production-grade, framework-agnostic implementation of the 19 Canonical Core Components defined in `MDS/04-Components/`. It translates Design Tokens (`MDS/02-Tokens/`) and Core Primitives (`MDS/Runtime/primitives/`) into accessible, robust, user-facing UI controls without external npm or runtime dependencies.

### Unidirectional Layer Progression
```text
01 Foundations (Principles, Roles, Behavioral Invariants)
       ↓
02 Token Repository (188 Canonical DTCG Tokens & Themes)
       ↓
03 Core Primitives (Layout, Surfaces, Typography, A11y, Interaction)
       ↓
04 Core Components (19 Canonical Components in @layer mds.components)
```

---

## 2. The 19 Canonical Components (5 Batches)

| Batch | Component | Directory | Modular CSS | Controller | Primary Primitives Composed |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Batch 1: Core Interaction** | `Button` | `button/` | `button.css` | Native `<button>` | `PressTarget`, `FocusRing`, `Text`, `Spinner` |
| | `IconButton` | `icon-button/` | `icon-button.css` | Native `<button>` | `PressTarget`, `FocusRing`, `Icon`, `VisuallyHidden` |
| | `Link` | `link/` | `link.css` | Native `<a>` | `FocusRing`, `Text` |
| **Batch 2: Form Infrastructure** | `Field` | `field/` | `field.css` | CSS Grid / Flex | `Stack`, `Label`, `HelperText`, `LiveRegion` |
| | `Input` | `input/` | `input.css` | Native `<input>` | `PressTarget`, `FocusRing`, `Text`, `Icon` |
| | `Textarea` | `textarea/` | `textarea.css` | Native `<textarea>` | `PressTarget`, `FocusRing`, `Numeric` |
| | `Checkbox` | `checkbox/` | `checkbox.css` | Native checkbox | `PressTarget`, `FocusRing`, `Icon` |
| | `Radio` | `radio/` | `radio.css` | Native radio | `PressTarget`, `FocusRing`, `Stack` |
| | `Switch` | `switch/` | `switch.css` | `switch.js` (`<mds-switch>`) | `PressTarget`, `FocusRing` |
| | `Select` | `select/` | `select.css` | Native `<select>` | `PressTarget`, `FocusRing`, `Icon` |
| **Batch 3: Feedback / Status** | `Alert` | `alert/` | `alert.css` | Container | `Surface`, `Icon`, `Text`, `IconButton` |
| | `Spinner` | `spinner/` | `spinner.css` | CSS animation | `ReducedMotion`, `VisuallyHidden` |
| | `Skeleton` | `skeleton/` | `skeleton.css` | CSS shimmer | `Surface`, `ReducedMotion` |
| | `Badge` | `badge/` | `badge.css` | Inline pill | `Surface`, `Text`, `Icon` |
| **Batch 4: Content / Data** | `Card` | `card/` | `card.css` | Container | `Surface`, `Elevation`, `Stack`, `Inline` |
| | `Table` | `table/` | `table.css` | AF-002 Container | `Surface`, `FocusRing`, `Numeric` |
| **Batch 5: Navigation / Overlay**| `Tabs` | `tabs/` | `tabs.css` | `tabs.js` (`<mds-tabs>`) | `FocusRing`, `Surface`, `PressTarget` |
| | `Dialog` | `dialog/` | `dialog.css` | `dialog.js` (`<mds-dialog>`) | `FocusTrap`, `Surface.overlay`, `Elevation` |
| | `Tooltip` | `tooltip/` | `tooltip.css` | `tooltip.js` (`<mds-tooltip>`)| `Surface.floating`, `Elevation` |

---

## 3. Inviolable Architectural Laws Codified

1. **Parent-Owned Spacing Law (Zero External Margins):**
   - Components declare internal padding (`padding.*`), but never external margins (`margin: 0`).
   - Spacing between adjacent components is strictly governed by layout primitives (`Stack`, `Inline`, `Grid`, `Cluster`).
2. **100% CSS Logical Properties:**
   - Zero physical `left`, `right`, `margin-left/right`, `padding-left/right`, or `border-left/right`.
   - All spatial dimensions use `*-inline-start`, `*-inline-end`, `*-block-start`, and `*-block-end`.
3. **PDR-009 / RTL Focus Order Protection:**
   - Zero `row-reverse` in CSS.
   - Logical inline progression preserves keyboard `Tab` traversal alignment with visual reading vector.
4. **Canonical Touch Targets (PressTarget 44px):**
   - Interactive controls guarantee minimum $44 \times 44\text{px}$ physical interaction area on touch viewports (`@media (pointer: coarse)`).
5. **High-Visibility Focus Indicators:**
   - 2px solid `var(--mds-color-focus-ring)` outline on `:focus-visible` with 2px offset.
6. **100% Design Token Consumption:**
   - 0 raw hex/rgb/hsl color magic numbers.
   - Bound directly to Layer 02 Component and Semantic Tokens.
7. **Accessibility Findings Codified:**
   - **AF-002 (Table):** Scrollable container with `tabindex="0"` and `role="region"` for keyboard panning.
   - **AF-002 (Dialog):** Destructive confirmation initial focus safety lands on Cancel button.
   - **AF-003 (Dialog):** Full inertness support and focus restoration on unmount.

---

## 4. Usage & Imports

### Consolidated CSS Import
```css
/* Inside application master stylesheet */
@import "path/to/MDS/Runtime/css/mds-core.css";
/* Or direct component runtime import */
@import "path/to/MDS/Runtime/components/components.css" layer(mds.components);
```

### Interactive Web Components Registration
```javascript
// Import all registered custom elements
import "./path/to/MDS/Runtime/components/components.js";

// Or import modular elements
import { MdsSwitch } from "./path/to/MDS/Runtime/components/switch/switch.js";
import { MdsTabs } from "./path/to/MDS/Runtime/components/tabs/tabs.js";
import { MdsDialog } from "./path/to/MDS/Runtime/components/dialog/dialog.js";
import { MdsTooltip } from "./path/to/MDS/Runtime/components/tooltip/tooltip.js";
```

---

## 5. Verification & Test Suite

Run the automated test suite:
```bash
python MDS/Runtime/components/tests/test_components_runtime.py
```
Asserts:
- 19/19 canonical components present
- 0/10 banned enterprise components
- 100% CSS Cascade Layering (`@layer mds.components`)
- 100% Parent-Owned Spacing Law compliance
- 100% CSS Logical Properties compliance
- 100% Design Token consumption (0 hardcoded colors)
- 44px Touch Targets & 2px Focus Rings
- Accessibility Findings AF-002 / AF-003
- Vestibular Reduced Motion Safety
