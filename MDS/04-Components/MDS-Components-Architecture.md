# MDS Components Architecture Specification

**Document Layer:** 04-Components  
**Status:** APPROVED (Phase 5 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-15  

---

## 1. Primary Objective & Scope

The **MDS Component Layer (Layer 04)** establishes the reusable, semantic, accessible, and user-facing building blocks of the Master Design System. Components translate Design Tokens (Layer 02) and Core Primitives (Layer 03) into recognizable UI controls without duplicating layout or accessibility infrastructure.

### Unidirectional Layer Hierarchy
```text
01 Foundations (Principles, Roles, Behavioral Invariants)
       ↓
02 Token Repository (Canonical W3C DTCG Tokens & Schemas)
       ↓
03 Core Primitives (Layout, Surfaces, Typography, A11y, Interaction)
       ↓
04 Components (Button, Input, Badge, Dialog, Table, Tabs, etc.)
       ↓
05 Patterns (Toolbar, FormSection, SearchFilter, EmptyRecovery)
       ↓
06 Workflows & 07 Templates
```

### Invariant Layer Rules:
1. **Components Depend on Primitives & Tokens:** A Component must strictly compose Layer 03 Primitives (`Surface`, `Stack`, `Inline`, `PressTarget`, `FocusRing`, `VisuallyHidden`) and consume Layer 02 Tokens (Component or Semantic).
2. **Primitives Never Depend on Components:** Layer inversion is strictly forbidden. A primitive must NEVER import or reference a component.
3. **Zero Widget Bloat:** Components represent recurring, high-leverage user interface patterns. Premature enterprise systems (e.g. `DataGrid`, `RichTextEditor`, `Calendar`, `CommandPalette`) are deferred until justified by concrete application requirements.

---

## 2. Core Architectural Invariants

### 2.1 Parent-Owned Spacing Invariant (Zero External Margins)
> **Architectural Law: Components NEVER declare external margins.**
- A Component (`Button`, `Input`, `Card`, `Badge`) specifies internal padding (`padding.*`), but never external margins (`margin-top`, `margin-bottom`, `margin-inline`).
- Spacing between adjacent components is strictly owned and governed by layout primitives (`Stack`, `Inline`, `Grid`, `Cluster`).
- This guarantees composability in modal footers, dense data tables, card bodies, and toolbars without layout side-effects or margin collapse.

### 2.2 Visual Dimension vs. Interaction Hit Target Invariant
> **Architectural Law: Visual Dimension $\neq$ Interaction Hit Area.**
- All interactive controls enforce the **Canonical MDS Touch Target Policy**: mandatory minimum **$44 \times 44\text{px}$** physical interaction area on all touch-capable viewports via invisible hit-box expansion (`PressTarget`).
- A visually compact 32px or 40px control preserves high desktop information density while guaranteeing physical touch accessibility on mobile.

### 2.3 Composition Over Variant Explosion
> **Architectural Law: Compose existing primitives rather than inventing specialized variants.**
- Rather than creating `ButtonWithIcon`, `ButtonWithBadge`, or `IconButton`, MDS composes:
  $$\text{Button} + \text{Icon} + \text{Inline}$$
- Rather than creating specialized inputs (`InputWithHelper`, `InputWithError`), MDS establishes the centralized **Field Architecture**:
  $$\text{Field} = \text{Stack} + \text{Label} + \text{Control (Input/Select)} + \text{HelperText} + \text{LiveRegion (Alert)}$$

### 2.4 Logical Directionality & Focus Order Invariant (PDR-009)
> **Architectural Law: Native inline axis progression; zero `row-reverse` in RTL.**
- Layout within and between components flows along the logical inline axis (`inline-start` $\to$ `inline-end`).
- Under LTR, `inline-start` is physically on the left. Under RTL, `inline-start` is physically on the right.
- `flex-direction: row-reverse` is strictly forbidden to prevent inversion of keyboard `Tab` traversal order relative to visual reading sequence (satisfying **WCAG 2.1/2.2 SC 2.4.3 Focus Order**).

---

## 3. Centralized Form Architecture

Forms are treated as an integrated semantic system rather than disconnected inputs. The `Field` primitive wrapper centralizes accessibility and feedback relationships:

```text
┌─────────────────────────────────────────────────────────────┐
│ Field Container (Stack gap="xs")                            │
│                                                             │
│   Label Primitive (htmlFor="field-id")                      │
│     ├── Text: "User Email"                                  │
│     └── Required Asterisk (aria-hidden="true")              │
│                                                             │
│   Control Slot (Input, Select, Textarea)                    │
│     ├── id="field-id"                                       │
│     ├── aria-describedby="field-help field-error"           │
│     ├── aria-invalid="true | false"                         │
│     └── aria-required="true | false"                        │
│                                                             │
│   HelperText Primitive (id="field-help")                    │
│     └── "We'll never share your email with third parties."  │
│                                                             │
│   LiveRegion / Error Alert (id="field-error", role="alert") │
│     └── "Please enter a valid email address."               │
└─────────────────────────────────────────────────────────────┘
```

This prevents repeating ARIA wiring, error styling, and label associations across every individual input component.

---

## 4. Component Taxonomy & Inventory

| Family | Implemented Core Components | Primary Primitives Composed |
| :--- | :--- | :--- |
| **Actions** | `Button`, `IconButton`, `Link` | `Interactive`, `PressTarget`, `FocusRing`, `Inline`, `Text`, `Icon` |
| **Inputs** | `Field`, `Input`, `Textarea`, `Checkbox`, `Radio`, `Switch`, `Select` | `Stack`, `Inline`, `Label`, `HelperText`, `LiveRegion`, `PressTarget` |
| **Feedback** | `Alert`, `Spinner`, `Skeleton` | `Surface`, `Inline`, `Text`, `Icon`, `ReducedMotion` |
| **Data Display** | `Badge`, `Card`, `Table` | `Surface`, `Stack`, `Inline`, `Text`, `Numeric`, `Elevation` |
| **Navigation** | `Tabs` | `Inline`, `Interactive`, `FocusRing`, `Text`, `Surface` |
| **Overlays** | `Dialog`, `Tooltip` | `FocusTrap`, `Surface (Overlay/Floating)`, `Elevation`, `VisuallyHidden` |

---

## 5. Mandatory 16-Point Component Anatomy Standard

Every core component specification in Layer 04 strictly documents:
1. **Purpose:** Semantic role and user goal.
2. **When to Use:** Prescriptive usage triggers.
3. **When Not to Use:** Explicit anti-patterns and redirecting to better alternatives.
4. **Anatomy:** Structural composition diagram.
5. **Variants & Intents:** Meaningful visual/semantic variations.
6. **Sizes:** Approved scale (32px `sm`, 40px `md`, 48px `lg`; zero 28px).
7. **States:** Visual states (default, hover, pressed, focus, disabled) & Experience states (loading, error, empty).
8. **Slots:** Composition points (leading/trailing icons, content body, trigger, dismiss action).
9. **Behavior:** Interaction lifecycle, event propagation, dismissal rules.
10. **Keyboard Interaction:** WAI-ARIA APG compliant key bindings (`Enter`, `Space`, `Tab`, `ArrowKeys`, `Escape`).
11. **Accessibility Guarantees:** Contrast ratios, accessible names, hit-targets, screen-reader semantics.
12. **Responsive Behavior:** Recomposition over shrinking (collapsing, scrolling, stacking).
13. **Motion & Transitions:** Duration, easing curve, and 0ms vestibular collapse.
14. **Token Mapping:** Strict Component $\to$ Semantic $\to$ Primitive resolution.
15. **Composition Rules:** Rules for nesting within other primitives/components.
16. **AI Usage Rules:** Heuristic selection laws for LLM/AI code generation agents.

---

## 6. Component Governance & Lifecycle

Components progress through disciplined lifecycle stages:
```text
Proposed ──► Reviewed ──► Approved ──► Beta ──► Stable ──► Deprecated ──► Removed
```
- **Phase 5 Delivery Status:** All Core Components delivered in Phase 5 enter the repository as **`Approved (Phase 5 Delivery)`**.
- **Promotion to Stable:** Occurs after automated test coverage, cross-browser visual verification, and end-to-end accessibility testing in concrete application environments.

---

## 7. AI Agent Usage Contract

When generating UI code using MDS:
1. **Intent-Driven Selection:** Select components based on user intent and semantic meaning, never visual mimicry.
   - For page navigation: use `Link`, NOT `Button`.
   - For state mutation/actions: use `Button`, NOT `Link`.
   - For mutually exclusive options: use `Radio`, NOT `Checkbox`.
   - For binary immediate toggles: use `Switch`, NOT `Checkbox`.
2. **Composition First:** If an icon button is required, compose `IconButton` with `VisuallyHidden` label rather than creating custom CSS.
3. **Form Integrity:** Always wrap inputs in `Field` to ensure accessible label association and error announcements.
4. **No Naked HTML:** Never output unstyled `<button>`, `<input>`, or `<table>`. Always map to MDS components.
