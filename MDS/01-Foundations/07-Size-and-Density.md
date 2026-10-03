# MDS Foundation: Size & Density Specification
**Foundational Layer:** 01-Foundations  
**Status:** APPROVED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Executive Summary & The MDS Touch Target Policy

MDS enforces a strict architectural boundary between visual rendering and physical touch ergonomics:

> **Visual Size $\neq$ Interaction Hit Area**

### Canonical MDS Touch Target Policy:
1. **Mandatory Minimum:** Any interactive component rendered on a touch-capable interface (mobile, tablet, kiosk) MUST provide a minimum physical hit area of **$44 \times 44\text{px}$** (satisfying WCAG 2.1/2.2 SC 2.5.5 and SC 2.5.8).
2. **Hit-Box Expansion Requirement:** Where a control's visual dimension is smaller than 44px (e.g. `size.control.sm` at 32px, `size.control.md` at 40px, or 20px standalone icons), the component implementation MUST expand its interactive target boundary to at least 44×44px using transparent hit-testing padding.
3. **Touch-First Primary Size:** `size.control.lg` (**48px**) is the primary touch-first visual height, naturally exceeding the 44px threshold without invisible padding.

---

## 2. Active Primitive Control Height Scale

| Token | Value (px) | Context & Target Device Usage |
| :--- | :---: | :--- |
| `size.control.sm` | **32px** | Compact density, dense table row actions, standalone filter chips |
| `size.control.md` | **40px** | **Default Soft Modern:** Standard desktop forms, buttons, inputs |
| `size.control.lg` | **48px** | Mobile-first primary actions, hero sign-up buttons, touch-first forms |

---

## 3. Active Primitive Icon Dimension Scale

All icons are drawn on standardized square bounding boxes to preserve optical weight parity:

| Token | Value (px) | Semantic Role & Hierarchy |
| :--- | :---: | :--- |
| `size.icon.xs` | 14px | Micro annotations, helper tooltips, inline status dots |
| `size.icon.sm` | 16px | Paired with `font.size.sm` (14px text) inside compact buttons and inputs |
| `size.icon.md` | 20px | **Standard UI Default:** Paired with standard 40px controls and navigation |
| `size.icon.lg` | 24px | Primary navigation sidebar icons, standalone action bar items |
| `size.icon.xl` | 32px | Feature headers, empty state illustrations, alert banners |

---

## 4. Density System Architecture

Density adjusts **information throughput and layout compacting**, independent of Mode (Light/Dark) or Visual Preset.

### 4.1 Comfortable (Default — Active)
- **Target Audience:** Consumer web, mobile apps, general SaaS dashboards.
- **Control Height:** 40px (`size.control.md`).
- **Base Spacing:** 16px (`space.4`) container padding.
- **Table Row Height:** 52px.

### 4.2 Compact (Enterprise — Active Scaffold)
- **Target Audience:** Administrative dashboards, CRM workflows, data-dense forms.
- **Control Height:** 32px (`size.control.sm`).
- **Base Spacing:** 12px (`space.3`) padding.
- **Table Row Height:** 40px.

### 4.3 Dense (High-Throughput — Deferred Proposal)
- **Status:** **Proposal 2: DEFERRED — FUTURE PHASE.** 28px (`size.control.xs`) is NOT an active primitive token in MDS. The active MDS control scale remains strictly 32px, 40px, and 48px.
- **Scope Restriction:** The 28px option remains deferred until actual dense desktop data-grid requirements are empirically validated in Phase 5. If reconsidered, it will be strictly restricted to pointer-driven desktop-only high-frequency environments and never permitted on touch interfaces.

---

## 5. Platform Implementation Guidance (Non-Normative)

- **Flutter:** Enforce minimum touch target using `BoxConstraints(minWidth: 44.0, minHeight: 44.0)` with `HitTestBehavior.opaque`.
- **Web / CSS:** Expand the interactive hit area on touch viewports using transparent pseudo-elements (e.g. `::after { content: ''; position: absolute; inset: -6px; }`).
