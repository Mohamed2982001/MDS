# MDS Primitives: Surface Suite
**Document Layer:** 03-Primitives / Surface  
**Status:** APPROVED (Phase 4 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Executive Summary & Surface Hierarchy

The **Surface Primitives** define the physical background planes, container groupings, and visual layering hierarchy across MDS interfaces. They enforce the **Depth Triad** (Surface Luminance > Subtle 1px Border > Soft Ambient Shadow) and strictly decouple surface fills from elevation z-planes:

```text
Canvas (Base Viewport Plane)
  ↓
Surface (Default Content & Card Plane)
  ↓
Raised (Elevated Control Panels & Cards)
  ↓
Floating (Dropdown Menus, Popovers, Autocomplete)
  ↓
Overlay (Modal Dialogs, Drawer Backdrops)
```

> [!IMPORTANT]
> **Architectural Boundary Law: Surface $\neq$ Elevation.**
> - A `Surface` defines the semantic background color, border separation, corner radius, and interior padding.
> - `Elevation` defines the multi-layer ambient shadow, z-index stack position, and Dark Mode luminance stepping.
> - They are composable: a `Surface` can receive an `elevation` prop, but elevation is never collapsed into raw CSS backgrounds.

---

## 2. Taxonomy of Surface Primitives

### 2.1 `Canvas` Primitive
- **Purpose:** The root background plane for the entire viewport/application window.
- **Tokens:** Fixed to `color.surface.canvas` (`neutral.50` in Light Mode, `neutral.950` in Dark Mode).
- **Elevation:** Level 0 (flush, zero shadow).
- **Radius:** None (`radius.none` = 0px).

### 2.2 `Surface` (Default) Primitive
- **Purpose:** The standard resting container plane for cards, content blocks, tables, and views.
- **Tokens:**
  - Background: `color.surface.default` (`neutral.0` in Light Mode, `neutral.900` in Dark Mode).
  - Border: 1px subtle border (`color.border.subtle` = `neutral.200` in Light Mode, `neutral.800` in Dark Mode).
  - Corner Radius: 10px default (`radius.md`).
- **Elevation:** Level 0 (Flat with border) or Level 1 (Raised with soft ambient shadow).

### 2.3 `Raised` Primitive
- **Purpose:** Elevated panels, control sidebars, raised active cards, and summary widgets.
- **Tokens:**
  - Background: `color.surface.raised` (`neutral.100` in Light Mode, `neutral.800` in Dark Mode).
  - Elevation: Level 1 (`elevation.level1`: `0 1px 3px rgba(15,23,42,0.06), 0 1px 2px rgba(15,23,42,0.04)`).
  - Border: Optional subtle 1px border.
  - Corner Radius: 10px (`radius.md`).

### 2.4 `Floating` Primitive
- **Purpose:** Detached, non-modal transient surfaces (dropdown menus, popover sheets, autocomplete lists, tooltips).
- **Tokens:**
  - Background: `color.surface.default` (Light: `#FFFFFF`, Dark: `#0F172A`).
  - Elevation: Level 2 (`elevation.level2`: `0 4px 6px -1px rgba(15,23,42,0.08), 0 2px 4px -2px rgba(15,23,42,0.04)`).
  - Layer (Z-Index): `layer.popover` (`z-index: 300`).
  - Corner Radius: 10px (`radius.md`) or 14px (`radius.lg`).
  - Border: 1px subtle border.

### 2.5 `Overlay` Primitive
- **Purpose:** Critical focal planes: modal dialogs, slide-in drawers, and sheet backdrops.
- **Tokens:**
  - Background: `color.surface.overlay` (Light: `#FFFFFF`, Dark: `#0F172A`).
  - Backdrop Scrim: `rgba(15, 23, 42, 0.40)` with subtle backdrop blur.
  - Elevation: Level 3 (`elevation.level3`: `0 12px 16px -4px rgba(15,23,42,0.12), 0 4px 6px -2px rgba(15,23,42,0.05)`).
  - Layer (Z-Index): `layer.modal` (`z-index: 400`).
  - Corner Radius: 14px (`radius.lg`) or 20px (`radius.xl`).

---

## 3. Normalized Surface API

| Property | Type | Default | Values / Description | Token Mapping |
| :--- | :--- | :--- | :--- | :--- |
| `elevation` | `enum` | `'level0'` | `'level0'` (Flat), `'level1'` (Raised), `'level2'` (Floating), `'level3'` (Overlay) | `elevation.level0`–`level3` |
| `border` | `enum \| boolean` | `'subtle'` | `false`, `'subtle'` (1px), `'default'` (1px), `'strong'` (1.5px) | `color.border.*`, `border.width.*` |
| `radius` | `enum` | `'md'` | `'none'` (0), `'sm'` (6px), `'md'` (10px default), `'lg'` (14px), `'xl'` (20px) | `radius.none` to `radius.xl` |
| `padding` | `enum` | `'md'` | `'none'`, `'xs'` (4px), `'sm'` (8px), `'md'` (16px), `'lg'` (24px), `'xl'` (32px) | `space.scale.*` |
| `as` | `string` | `'div'` | Semantic tag (`'div'`, `'article'`, `'aside'`, `'dialog'`) | — |

---

## 4. Dark Mode Stepping Validation

In Dark Mode, surfaces lighten progressively with elevation rather than relying exclusively on black shadows:
- **Canvas:** `neutral.950` (`#090D16`)
- **Default Surface:** `neutral.900` (`#0F172A`)
- **Raised Panel:** `neutral.800` (`#1E293B`)
- **Overlay Dialog:** `neutral.700` (`#334155`)

---

## 5. Concentricity Rule Integration

When surfaces are nested (e.g. an inset card inside a raised container with 16px padding):
$$R_{\text{inner}} \approx \max(0, R_{\text{outer}} - P)$$
Example: Outer container `radius="lg"` (14px) with 8px padding $\implies$ Inner surface `radius="sm"` (6px), maintaining optical geometric harmony.

---

## 6. Anti-Patterns (Forbidden Usage)

- ❌ Hardcoding `#FFFFFF` or `#F8FAFC` as CSS background.
- ❌ Using arbitrary multi-stop box shadows (`box-shadow: 0 10px 25px rgba(...)`).
- ❌ Hardcoding random corner radii (e.g. `border-radius: 8px;` instead of `radius.md` 10px).
- ❌ Collapsing surface and elevation into a single unconfigurable component.

---

## 7. AI Usage Rules

- **ALWAYS WRAP:** Every card, container panel, floating menu, or modal MUST be backed by a `Surface`, `Raised`, `Floating`, or `Overlay` primitive.
- **NEVER INVENT:** Do not add custom drop shadows. Always select an elevation tier (`level0` through `level3`).
