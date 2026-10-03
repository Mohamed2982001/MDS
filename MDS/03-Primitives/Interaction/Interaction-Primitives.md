# MDS Primitives: Interaction Suite
**Document Layer:** 03-Primitives / Interaction  
**Status:** APPROVED (Phase 4 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Executive Summary & Philosophy

The **Interaction Primitives** provide the structural infrastructure for user input, focus, and event handling. They implement the **Canonical MDS Touch Target Policy** (44×44px minimum target for touch contexts), provide visible focus indicators, and establish predictable interaction state lifecycles without prematurely implementing concrete components.

```text
Interaction Primitives
 ├── PressTarget   (Enforces 44×44px hit-box expansion on touch viewports)
 ├── FocusRing     (2px high-visibility focus indicator on :focus-visible)
 └── Interactive   (Base state machine: hover, focus, pressed, disabled, loading)
```

---

## 2. Primitive Specifications

### 2.1 `PressTarget` Primitive (Touch Target Enforcer)
- **Purpose:** Decouples physical interaction hit area from visual component dimensions.
- **Canonical Policy (MDS Design Rule):** Any interactive control rendered on a touch-capable interface MUST provide an interactive bounding box of at least **$44 \times 44\text{px}$**.

> [!NOTE]
> **WCAG Benchmark & Standards Calibration:**
> - **MDS Internal Rule:** MDS establishes the 44×44px minimum touch target as a core design-system invariant across mobile and touch viewports.
> - **WCAG SC 2.5.5 (Target Size - Enhanced, Level AAA):** Aligns with the 44×44 CSS pixel recommendation.
> - **WCAG SC 2.5.8 (Target Size - Minimum, Level AA):** Requires a 24×24 CSS pixel target (with spacing exceptions). MDS deliberately exceeds this AA threshold for superior ergonomic reliability.
> - **Compliance Boundary:** Physical hit area dimension alone does *not* establish overall WCAG accessibility compliance; accessible naming, color contrast, keyboard interoperability, and state announcements remain mandatory independent requirements.

- **Behavior:**
  - When the visual element is $44\text{px}$ or larger (e.g. `size.control.lg` = 48px), `PressTarget` renders flush without expansion.
  - When the visual element is smaller than $44\text{px}$ (e.g. `size.control.sm` = 32px, or a 20px icon), `PressTarget` expands an invisible transparent hit area using pseudo-elements (`::after`) or Flutter `BoxConstraints(minWidth: 44, minHeight: 44)` with `HitTestBehavior.opaque`.

- **Hit-Area Overlap & Safety Invariants:**
  - **No Target Collisions:** When `PressTarget` expands an invisible hit area via `::after`, adjacent controls must not occlude each other. Layout containers (`Inline`, `Stack`) must enforce a minimum spacing gap of at least `space.2` (8px) between interactive siblings.
  - **Pointer Precision:** Expanded hit targets are restricted to touch contexts (`@media (pointer: coarse)`); precision mouse/trackpad environments retain native boundary bounds to prevent accidental clicks.
  - **Keyboard Integrity:** Keyboard focus indicators (`FocusRing`) bind strictly to the visual component boundary, ensuring focus rings remain sharp and unclipped.
  - **DOM Semantics:** The visible control remains the authoritative semantic target in the accessibility tree (`<button>`, `<a>`, `<input>`).

- **API:**
  - `minTarget`: `number` (default `44`).
  - `targetPlatform`: `'auto'` (detects touch capability), `'touch'` (always active), `'pointer'` (disabled for precision desktop).

```text
┌──────────────────────────────────────────────┐
│ Invisible Hit Target Boundary (44 × 44px)    │
│       ┌──────────────────────────────┐       │
│       │ Compact Visual Button (32px) │       │
│       └──────────────────────────────┘       │
└──────────────────────────────────────────────┘
```

### 2.2 `FocusRing` Primitive (Accessible Focus Indicator)
- **Purpose:** Provides a high-visibility, WCAG-compliant keyboard focus boundary without relying on ugly default browser focus outlines.
- **Activation Law:** Strictly visible on `:focus-visible` (keyboard navigation / `Tab` key) and **never** on pointer click/touch taps.
- **Tokens & Geometry:**
  - Width: **2px** (`border.width.thick`).
  - Offset: **2px** gap (`outline-offset: 2px`) separating ring from component border.
  - Color:
    - Light / Dark Mode: `color.brand.600` (`#2563EB`, achieves >3:1 contrast against white and dark backgrounds).
    - High Contrast Mode: `#000000` (Light) / `#FFFFFF` (Dark) for maximum contrast.
  - Corner Radius: Follows parent component radius + 2px offset for perfect concentricity.

### 2.3 `Interactive` Primitive (State Lifecycle Wrapper)
- **Purpose:** Low-level event and state manager providing keyboard accessibility, click propagation rules, and state tokens for unstyled elements.
- **Supported States:**
  - `isHovered`: Pointer presence.
  - `isFocused`: Keyboard focus (`FocusRing` applied).
  - `isPressed`: Active click/touch compression.
  - `isDisabled`: Pointer events disconnected (`pointer-events: none`), opacity collapsed to 0.38 (`opacity.disabled`), `aria-disabled="true"`.
  - `isLoading`: Interaction locked, `aria-busy="true"`.
- **Keyboard Handling:**
  - Automatically handles `Enter` and `Space` keydown events for non-native `<button>` elements, triggering onClick callbacks.

---

## 3. Normalized Interaction API

| Property | Type | Default | Values / Description | Token Mapping |
| :--- | :--- | :--- | :--- | :--- |
| `disabled` | `boolean` | `false` | Sets `aria-disabled="true"`, mutes visual fill | `opacity.disabled` (0.38) |
| `loading` | `boolean` | `false` | Sets `aria-busy="true"`, halts click propagation | — |
| `focusRing` | `boolean` | `true` | Enables high-visibility 2px focus outline | `border.width.thick`, `brand.600` |
| `touchTarget`| `boolean` | `true` | Enforces 44×44px hit boundary on touch screens | `size.target.touch` (44px) |
| `onClick` | `function` | `null` | Callback executed on click, touch, or Enter/Space key | — |

---

## 4. Accessibility Guarantees

1. **No Hover Dependency:** No action, tooltip, or navigation can depend solely on hover. Hover feedback is purely visual confirmation.
2. **Accessible Names:** Any interactive wrapper that does not contain visible text MUST mandate an `aria-label` or embed a `VisuallyHidden` primitive.
3. **Contrast Compliance:** The 2px `FocusRing` satisfies WCAG 2.1 SC 1.4.11 (Non-Text Contrast) with $\ge 3:1$ ratio against surrounding surfaces.

---

## 5. Anti-Patterns (Forbidden Usage)

- ❌ Setting `outline: none;` without providing `FocusRing`.
- ❌ Creating clickable icon buttons with a 24×24px hit area on mobile.
- ❌ Relying on `:hover` to reveal critical actions without keyboard/touch equivalents.
- ❌ Using `opacity: 0.5` instead of `opacity.disabled` (0.38).

---

## 6. AI Usage Rules

- **ALWAYS ENFORCE:** Every interactive element smaller than 44px on mobile must be wrapped in `PressTarget`.
- **FOCUS REQUIREMENT:** Never remove focus outlines. Always attach `FocusRing`.
- **NO COMPONENTS YET:** Use `Interactive` and `PressTarget` to define interaction infrastructure; do not build full `Button` components.
