# MDS Primitives Architecture Specification
**Document Layer:** 03-Primitives  
**Status:** APPROVED (Phase 4 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Primary Objective & Architectural Scope

The **MDS Primitive Layer (Layer 03)** transforms canonical Design Tokens into reusable, platform-agnostic structural and behavioral building blocks. Primitives form the foundational substrate upon which all user-facing Components (Layer 04) and UX Patterns (Layer 05) are built.

### The Unidirectional Hierarchy
```text
01 Foundations (Principles, Roles, Behavioral Invariants)
       ↓
02 Token Repository (Canonical W3C DTCG Tokens & Schemas)
       ↓
03 Core Primitives (Layout, Surfaces, Typography, A11y, Interaction)
       ↓
04 Components (Button, Input, Badge, Dialog, Table [Phase 5])
       ↓
05 Patterns (Data Table Toolbar, Form Section, Search+Filter [Phase 6])
```

### Invariant Layer Rules:
1. **Primitives Depend Strictly on Tokens:** A primitive must consume only Primitive (Layer 01) and Semantic (Layer 02) tokens. It must never hardcode raw hex values, arbitrary pixel dimensions, or standalone margins.
2. **Components Depend on Primitives:** User-facing components (`Button`, `Card`, `Dialog`) must be composed out of primitives (e.g. `Surface` + `PressTarget` + `FocusRing` + `Inline` + `Text`).
3. **Primitives Never Depend on Components:** A primitive must NEVER import or reference a component. Layer inversion is strictly prohibited.
4. **Zero User-Facing Chrome:** Primitives solve recurring structural, typographic, surface, and accessibility problems; they do not dictate visual component aesthetics (e.g. `Surface` provides the plane and shadow, but is not a "Card" component).

---

## 2. Core Architectural Invariants

### 2.1 Parent-Owned Spacing Invariant
> **Architectural Law: Primitives and Components NEVER declare external margins.**
- Spacing between adjacent elements is **strictly owned and managed by layout primitives** (`Stack`, `Inline`, `Grid`, `Cluster`).
- Child elements declare only internal padding (`padding.*`), never external margins (`margin.*`).
- This guarantees that any primitive or component can be dropped into dense data tables, modal dialogs, or marketing banners without layout side-effects or margin collapse issues.

### 2.2 Visual Size vs. Interaction Hit Target Invariant
> **Architectural Law: Visual Dimension $\neq$ Interaction Hit Area.**
- All interactive primitives and wrappers enforce the **Canonical MDS Touch Target Policy**: mandatory minimum **$44 \times 44\text{px}$** physical interaction area on all touch-capable viewports via invisible hit-box expansion (`PressTarget`).
- A visually compact 32px or 40px element safely preserves high information density without compromising physical accessibility.

### 2.3 Responsive Recomposition Invariant
> **Architectural Law: Recomposition over Shrinking.**
- Primitives respond to viewport constraints by changing their structural topology (e.g. `Inline` wrapping into `Stack`, 12-column `Grid` collapsing into single column, container gutters shifting from 32px to 16px).
- Elements are never arbitrarily shrunk down below legibility or touch thresholds.

### 2.4 Logical Directionality Invariant (RTL-First)
> **Architectural Law: Zero Physical Left/Right Assumptions.**
- All directional alignment, padding, and borders in layout and typography primitives utilize CSS Logical Properties (`inline-start`, `inline-end`, `block-start`, `block-end`) or platform-equivalent directional abstractions (Flutter `EdgeInsetsDirectional`, `Directionality`).
- Tested and verified across LTR, RTL, and mixed Arabic/Latin strings with zero manual layout flipping required.

---

## 3. Primitive Layer Directory Map

```text
MDS/03-Primitives/
├── MDS-Primitives-Architecture.md              # This core specification
├── Layout/
│   ├── Container.md                             # Viewport bounds & responsive gutters
│   ├── Stack.md                                 # 1D Vertical block layout & spacing
│   ├── Inline.md                                # 1D Horizontal inline layout & alignment
│   ├── Grid.md                                  # 12-column responsive fluid grid
│   └── Cluster.md                               # Multi-element wrapping group
├── Typography/
│   └── Typography-Primitives.md                 # Text, Heading, Label, Caption, HelperText, Numeric, Code
├── Surface/
│   └── Surface-Primitives.md                    # Canvas, Surface, Raised, Floating, Overlay
├── Interaction/
│   └── Interaction-Primitives.md                # PressTarget (44px), FocusRing (2px), Interactive
├── Accessibility/
│   └── Accessibility-Primitives.md              # VisuallyHidden, FocusTrap, LiveRegion, ReducedMotion
├── Icon/
│   └── Icon-Primitive.md                        # Optical sizing, 4-tier RTL mirroring contract
├── Primitive-Decision-Log.md                    # Architectural records for all primitive decisions
└── showcase/                                    # Executable validation sandbox (zero external dependencies)
    ├── tokens.css                               # Compiled CSS custom properties
    ├── primitives.css                           # Platform-agnostic CSS layout rules
    └── index.html                               # Standalone visual testbed
```

---

## 4. Universal Token Mapping Hierarchy

Before creating any property or style within a primitive, implementations must resolve values in this strict sequence:

$$\text{Component Token} \longrightarrow \text{Semantic Token} \longrightarrow \text{Primitive Token} \longrightarrow \text{STOP (No Unapproved Values)}$$

- **Bypassing is Forbidden:** Primitives must never bypass Semantic tokens to consume raw colors (e.g. must use `color.surface.default`, not `color.neutral.0`).
- **Magic Values are Forbidden:** Hardcoded numeric constants (e.g. `padding: 13px; font-size: 15px; border-radius: 9px;`) cause immediate build failure.

---

## 5. Interaction State Infrastructure

Interactive primitives establish standardized state hooks consumed downstream by Components:
- `default`: Resting state.
- `hover`: Pointer entry state (must never be the sole mechanism for disclosing critical information).
- `focus`: Keyboard navigation state (enforces `FocusRing` visibility).
- `pressed` / `active`: Immediate physical compression and darkened fill.
- `disabled`: Muted visual wash (`opacity.disabled = 0.38`), pointer events decoupled, `aria-disabled="true"`.
- `loading`: Visual busy state (`aria-busy="true"`), click propagation halted.
- `error` / `invalid`: High-contrast semantic danger border and assistive warning announcement.

---

## 6. AI Usage Contract & Guardrails

For all AI coding agents generating code within the MDS ecosystem:
1. **Search Order:** Always search for an existing primitive before writing custom HTML/CSS or Flutter widgets.
2. **Composition First:** If an existing primitive does not fulfill the layout exactly, compose existing primitives (`Stack` inside `Container`) rather than inventing a new layout primitive.
3. **No Margin Rule:** Never add `margin`, `marginTop`, or `margin-bottom` to a component. Wrap elements inside `Stack` or `Inline` with appropriate `gap`.
4. **Touch Target Rule:** Never create an interactive target smaller than 44×44px without wrapping it in `PressTarget`.
