# MDS Foundation: Elevation & Depth Specification
**Foundational Layer:** 01-Foundations  
**Status:** APPROVED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Executive Summary & Depth Philosophy

In **MDS**, elevation communicates **structural hierarchy and z-axis focus**, never superficial decoration.

### The Depth Triad:
When lifting an element in the z-axis, MDS applies three layers of differentiation in order of importance:
1. **Surface Luminance Difference:** The elevated surface shifts in tone relative to the canvas.
2. **Structural Border Outline:** A 1px subtle border ensures edge clarity.
3. **Multi-Layer Ambient Shadow:** A dual-layer physical shadow mimics soft, natural ambient occlusion.

> **Rule:** Excessive drop shadows, colored glows, and intense blurred halos are strictly rejected.

---

## 2. Platform-Agnostic Shadow Hierarchy (Light Mode)

Each elevation level defines a physical dual-layer shadow configuration (an ambient contact shadow + a directional elevation shadow):

| Level | Token | Layer 1 (Ambient Contact) | Layer 2 (Directional Elevation) | Role & Assigned Components |
| :---: | :--- | :--- | :--- | :--- |
| **0** | `elevation.level0` | Flush surface (Zero shadow) | Flush surface (Zero shadow) | Canvas, base layouts, flush list items |
| **1** | `elevation.level1` | `Y: 1px, Blur: 3px, Alpha: 6%` | `Y: 1px, Blur: 2px, Spread: -1px, Alpha: 4%` | Standard cards, statistics panels, data tables |
| **2** | `elevation.level2` | `Y: 4px, Blur: 6px, Spread: -1px, Alpha: 8%` | `Y: 2px, Blur: 4px, Spread: -2px, Alpha: 4%` | Select dropdowns, autocomplete menus, popovers |
| **3** | `elevation.level3` | `Y: 12px, Blur: 16px, Spread: -4px, Alpha: 12%` | `Y: 4px, Blur: 6px, Spread: -2px, Alpha: 5%` | Modal dialogs, command palettes, slide-in drawers |

*Base Shadow Color: Tinted with neutral slate (`rgba(15, 23, 42, ...)`).*

---

## 3. Elevation vs. Layer Stacking Order Disambiguation

MDS establishes an explicit architectural separation between visual depth and stacking order:
- **Elevation (`elevation.*`):** Optical perceived depth rendered via shadows and surface luminance shifts.
- **Layer Stacking Order (`layer.*`):** Platform z-index coordinates governing DOM/render-tree stacking planes (`base: 0`, `raised: 10`, `dropdown: 100`, `overlay: 1000`, `toast: 2000`).
- *Principle:* An element with `elevation.level2` (e.g. a hovering card) does NOT necessarily acquire `layer.dropdown` unless it is a floating popup detached from document flow.

---

## 4. Dark Mode Elevation Strategy (Luminance Stepping)

In Dark Mode, dark drop shadows become visually imperceptible against dark canvases (`#090D16` / `#0F172A`). MDS communicates elevation by progressively **lightening surface tones**:

```
[Level 3 Overlay:  #334155 (neutral.700)]   <-- Modal Dialogs & Drawers
       ▲
[Level 2 Floating: #1E293B (neutral.800)]   <-- Popovers & Menus
       ▲
[Level 1 Raised:   #0F172A (neutral.900)]   <-- Cards & Panels
       ▲
[Level 0 Canvas:   #090D16 (neutral.950)]   <-- Background Canvas
```

Coupled with a `1px` subtle border (`#334155`), elements maintain crisp edge definition without muddy shadows.
