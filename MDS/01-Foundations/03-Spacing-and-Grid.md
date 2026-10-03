# MDS Foundation: Spacing & Grid Specification
**Foundational Layer:** 01-Foundations  
**Status:** APPROVED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Executive Summary: The 4px Base Grid

MDS uses an intentional **4px modular spacing grid** for all spatial dimensions, component padding, and layout gutters:
- Multiples of 4 create natural visual harmony and predictable alignment across mobile, tablet, and desktop viewports.
- **Scope Note:** The 4px grid applies specifically to **spacing and layout positioning tokens** (`space.*`). It does not restrict non-spacing dimensions (e.g., optical 1.5px border width or typographic line-height multipliers) from using precise optical values.

---

## 2. Calibrated Modular Spacing Scale

| Token | Pixels | Rem (16px base) | Primary Context & Application |
| :--- | :---: | :---: | :--- |
| `space.0`  | 0px  | 0.000rem | Boundary collapse, zero margin resets |
| `space.1`  | 4px  | 0.250rem | Micro gap: icon-to-label, badge internal padding |
| `space.2`  | 8px  | 0.500rem | Tight gap: list item vertical separation, chip padding |
| `space.3`  | 12px | 0.750rem | Compact padding: input field vertical padding, small card inset |
| `space.4`  | 16px | 1.000rem | **Baseline UI Standard:** Standard card body padding, form row spacing |
| `space.5`  | 20px | 1.250rem | Moderate padding: dialog headers, generous card padding |
| `space.6`  | 24px | 1.500rem | Medium layout spacing: modal interior padding, card grid gutter |
| `space.8`  | 32px | 2.000rem | Large container margin: section headers, page margins |
| `space.10` | 40px | 2.500rem | Prominent section break on tablet and desktop viewports |
| `space.12` | 48px | 3.000rem | Major layout block division |
| `space.16` | 64px | 4.000rem | Macro hero spacing, landing view transitions |

---

## 3. Parent-Owned Spacing Invariant

> **Architectural Law: Components NEVER declare external margins.**

- A `Button`, `Card`, or `Badge` must never contain hardcoded outer margins.
- Spacing between adjacent elements is **strictly owned by the parent layout container** (`Stack`, `Inline`, `Grid`, `Cluster`).
- This invariant guarantees that any component can be reused across dense tables, mobile lists, or sparse marketing hero banners without CSS margin conflicts.

---

## 4. 12-Column Responsive Layout Grid

| Breakpoint Tier | Min Viewport | Columns | Fluid Gutter | Page Margin |
| :--- | :---: | :---: | :---: | :---: |
| **Mobile (`sm`)**  | 320px  | 4  | 16px (`space.4`) | 16px (`space.4`) |
| **Tablet (`md`)**  | 768px  | 8  | 24px (`space.6`) | 24px (`space.6`) |
| **Desktop (`lg`)** | 1024px | 12 | 24px (`space.6`) | 32px (`space.8`) |
| **Wide (`xl`)**    | 1440px | 12 | 32px (`space.8`) | 48px (`space.12`) |

- **Container Max-Widths:** Standard application container max-width is constrained to **1152px** (`container.lg`) to maintain optimal text readability (65–75 characters per line). High-throughput data dashboards and wide workspaces may expand to **1440px** (`container.xl`).
