# MDS CSS Architecture & Cascade Layering Specification

**Layer:** 13-Implementation  
**Target Specification:** [`MDS-Implementation-Architecture.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/13-Implementation/MDS-Implementation-Architecture.md)  
**Status:** APPROVED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Ratification Date:** 2026-09-20  
**Implementation Target:** Phase 9.2 (Token Runtime) through Phase 9.6 (Reference App)  

---

## 1. Architectural Mission

The **MDS CSS Architecture** defines the styling engine, specificity rules, layout mechanics, and internationalization standards governing all visual output in the web implementation.

The architecture enforces five inviolable laws:
1. **Cascade Layer Isolation:** Specificity wars are eliminated using native W3C CSS Cascade Layers (`@layer`).
2. **100% Token Consumption:** Zero raw hex values, pixel measurements, or magic numbers may exist in component stylesheets; all styling derives from `var(--mds-*)`.
3. **100% Logical Property Directionality:** All horizontal layout, margin, padding, border, and position rules must use CSS Logical Properties. Physical `left`/`right` and `row-reverse` are strictly forbidden.
4. **Accessible Focus & Touch Protection:** 2px high-visibility focus indicators (`:focus-visible`) and 44×44px minimum interactive hit areas (`PressTarget`).
5. **Reduced-Motion Universal Safety:** Instantaneous transition collapse under `prefers-reduced-motion: reduce`.

---

## 2. The CSS Cascade Layering Model (`@layer`)

MDS organizes all styles into eight strictly ordered cascade layers declared at the root of the stylesheet hierarchy:

```css
@layer mds.reset,
       mds.tokens,
       mds.foundations,
       mds.primitives,
       mds.components,
       mds.patterns,
       mds.templates,
       mds.overrides;
```

### Layer Hierarchy & Responsibilities:

```text
Layer Order          Role & Scope
──────────────────────────────────────────────────────────────────────────
1. mds.reset         Box-sizing, margin resets, baseline HTML element normalization.
2. mds.tokens        CSS custom properties compiled from DTCG tokens (base + themes).
3. mds.foundations   Global typography (Cairo), color defaults, surface luminance.
4. mds.primitives    5 Layout primitives (Container, Stack, Inline, Grid, Cluster) & Surfaces.
5. mds.components    19 Core Components (Button, Input, Badge, Card, Table, Dialog, etc.).
6. mds.patterns      8 Canonical composite patterns (Form-Section, Search-Filter-Bar, etc.).
7. mds.templates     6 Page layout templates (Dashboard, List, Detail, Form, Settings, AI).
8. mds.overrides     Consumer utility classes and application-specific contextual tweaks.
```

### Specificity Invariant:
Because layer order dictates precedence in modern CSS, a selector in `mds.components` with simple class specificity (`.mds-button`) will **always** override a selector in `mds.primitives` or `mds.reset` without requiring artificial selector escalation (e.g. `.parent .child.button`) or `!important`. Similarly, user overrides in `mds.overrides` effortlessly customize templates.

---

## 3. Directionality & Logical Properties Architecture

Arabic (RTL) is the primary baseline script of MDS, co-equal with Latin (LTR). 

### 3.1 Strict Logical Mapping Table

| Physical Property (FORBIDDEN) | CSS Logical Replacement (MANDATORY) | Architectural Justification |
| :--- | :--- | :--- |
| `margin-left`, `margin-right` | `margin-inline-start`, `margin-inline-end` | Automatically adjusts horizontal spacing across RTL/LTR |
| `padding-left`, `padding-right` | `padding-inline-start`, `padding-inline-end` | Natural content alignment without directional overrides |
| `left`, `right` (Positioning) | `inset-inline-start`, `inset-inline-end` | Pinning sidebars, drawers, badges symmetrically |
| `border-left`, `border-right` | `border-inline-start`, `border-inline-end` | Callout borders, table column borders invert cleanly |
| `text-align: left` / `right` | `text-align: start` / `end` | Text reads naturally from script origin |
| `float: left` / `right` | `float: inline-start` / `inline-end` | Avoids directional layout breakage |
| `flex-direction: row-reverse` | **STRICTLY PROHIBITED** | Inverting DOM visual flow breaks Tab navigation focus order (WCAG 2.4.3) |

### 3.2 Icon Mirroring Rules:
- **Directional Icons Mirror:** Navigation chevrons (`chevron-right` $\to$ `chevron-left`), forward/back arrows, send icons invert horizontally via `transform: scaleX(-1)` in RTL.
- **Static Icons Never Mirror:** Clock, search magnifying glass, document page, audio volume, and brand emblems remain un-mirrored to protect universal recognition.

---

## 4. Specificity & Selector Governance

To ensure deterministic maintainability and prevent style pollution:

1. **BEM-Inspired Semantic Naming:** All classes use the `.mds-[block]--[modifier]` prefix:
   - Block: `.mds-button`, `.mds-card`, `.mds-input`
   - Element: `.mds-button__icon`, `.mds-card__header`
   - Modifier: `.mds-button--primary`, `.mds-button--sm`, `.mds-input--error`
2. **Maximum Selector Depth $\le 2$ Classes:**
   - Allowed: `.mds-card .mds-card__header`
   - Forbidden: `.mds-page .mds-container .mds-card .mds-card__body .mds-button`
3. **Zero ID Selectors:** `#id` selectors are strictly banned for styling.
4. **Zero `!important` Usage:** Banned in all runtime component and pattern stylesheets.

---

## 5. Responsive & Container Grid Architecture

MDS responsive behavior follows the law of **"Recomposition, Not Shrinking"**:

### 5.1 Breakpoints:
```css
/* Mobile First Base: 320px - 767px */

/* Tablet Tier: 768px - 1023px */
@media (min-width: 768px) { ... }

/* Desktop Tier: 1024px - 1439px */
@media (min-width: 1024px) { ... }

/* Wide Screen Tier: >= 1440px */
@media (min-width: 1440px) { ... }
```

### 5.2 Container Constraints:
```css
@layer mds.primitives {
  .mds-container {
    width: 100%;
    margin-inline: auto;
    padding-inline: var(--mds-space-4); /* 16px mobile */
  }

  @media (min-width: 768px) {
    .mds-container {
      padding-inline: var(--mds-space-6); /* 24px tablet */
    }
  }

  /* Standard Application Container */
  .mds-container--standard {
    max-width: 1152px; /* container.lg - 65-75 chars line-length protection */
  }

  /* Wide Workspace Container */
  .mds-container--wide {
    max-width: 1440px; /* container.xl - data tables, dashboards, canvas */
  }
}
```
*Note: 1280px is strictly prohibited as a container max-width.*

---

## 6. Accessibility & Interaction State Styles

### 6.1 Unified Focus Ring Standard
All interactive elements implement an accessible, high-contrast 2px focus ring:

```css
@layer mds.foundations {
  :focus-visible {
    outline: var(--mds-border-width-focus, 2px) solid var(--mds-color-border-focus);
    outline-offset: 2px;
  }

  /* In high contrast mode, outline is guaranteed visible */
  [data-mode="high-contrast"] :focus-visible {
    outline: 2px solid var(--mds-color-border-focus);
    outline-offset: 3px;
  }
}
```

### 6.2 Reduced-Motion Safety Standard
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### 6.3 44×44px Interaction Target Enforcer (`PressTarget`)
Small controls expand their hit area transparently on touch devices:

```css
@media (pointer: coarse) {
  .mds-button--sm,
  .mds-icon-button--sm,
  .mds-checkbox,
  .mds-radio {
    position: relative;
  }

  .mds-button--sm::after,
  .mds-icon-button--sm::after,
  .mds-checkbox::after,
  .mds-radio::after {
    content: '';
    position: absolute;
    inset-inline-start: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    min-width: 44px;
    min-height: 44px;
    pointer-events: auto;
  }
}
```
