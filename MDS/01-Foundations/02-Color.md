# MDS Foundation: Color System Specification
**Foundational Layer:** 01-Foundations  
**Status:** APPROVED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Aesthetic Rationale: Chromatic Slate & Royal Sapphire

MDS rejects sterile achromatic grays and oversaturated palette schemes in favor of an intentional **Chromatic Slate & Royal Sapphire** pairing:
- **Chromatic Slate Neutrals:** Cool slate-blue undertone (Hue range 210°–222°, nominal 215°–220°, saturation 16%–47%). Adds depth, prevents eye fatigue, and feels premium in both light and dark modes.
- **Royal Sapphire Brand Blue:** Primary action anchor `#2563EB` (`brand.600`), balancing vitality with high WCAG legibility.

---

## 2. Calibrated Primitive Color Scales

### 2.1 Brand Scale (Royal Sapphire)
- `brand.50`: `#EFF6FF` — Lightest active wash and selection background
- `brand.100`: `#DBEAFE` — Highlight fill for chips and active navigation
- `brand.200`: `#BFDBFE` — Subtle brand boundary outline
- `brand.300`: `#93C5FD` — Progress track fill and secondary accents
- `brand.400`: `#60A5FA` — Dark mode secondary brand accent
- `brand.500`: `#3B82F6` — Vibrant interactive blue
- `brand.600`: **`#2563EB`** — **Primary Brand Anchor:** Resting button fill (WCAG AA **5.17:1** against `#FFFFFF`)
- `brand.700`: **`#1D4ED8`** — **Primary Hover State:** (WCAG AA **6.70:1** against `#FFFFFF`)
- `brand.800`: **`#1E40AF`** — **Primary Active/Pressed State:** (WCAG AAA **8.72:1** against `#FFFFFF`)
- `brand.900`: `#1E3A8A` — Midnight blue for high-contrast headers
- `brand.950`: `#172554` — Deepest brand night tint

### 2.2 Neutral Scale (Chromatic Slate)
- `neutral.0`: `#FFFFFF` — Pure white anchor for canvas and inverted text
- `neutral.50`: `#F8FAFC` — Chromatic canvas backdrop and alternate table rows
- `neutral.100`: `#F1F5F9` — Inactive control backgrounds and surface fills
- `neutral.200`: `#E2E8F0` — Subtle interior dividers and table row borders
- `neutral.300`: `#CBD5E1` — Resting form field borders and card outlines
- `neutral.400`: `#94A3B8` — Disabled text and non-interactive icon glyphs
- `neutral.500`: `#64748B` — Secondary labels and captions (WCAG AA **4.76:1** against `#FFFFFF`)
- `neutral.600`: `#475569` — Emphasized secondary text on light surfaces
- `neutral.700`: `#334155` — Dark mode overlay surface and prominent text
- `neutral.800`: `#1E293B` — Dark mode elevated cards and container fill
- `neutral.900`: `#0F172A` — Primary dark neutral for body text (WCAG AAA **17.85:1** against `#FFFFFF`)
- `neutral.950`: `#090D16` — Deepest dark mode canvas backdrop
- `neutral.1000`: `#000000` — Pure black anchor for High Contrast Mode

---

## 3. Semantic Feedback Scales & Alert Usage

Status colors communicate state clearly without relying solely on color (paired with icons and text labels):

| Domain | Base 600 Token | Hex Code | Alert Banner Text Pairing (Accessible AA) |
| :--- | :--- | :---: | :--- |
| **Success** | `palette.green.600` | `#059669` | Use `green.700` (`#047857`, **5.21:1**) on `green.50` (`#ECFDF5`) |
| **Warning** | `palette.amber.600` | `#D97706` | Use `amber.700` (`#B45309`, **4.84:1**) on `amber.50` (`#FFFBEB`) |
| **Danger**  | `palette.red.600`   | `#DC2626` | Resting action button with white text achieves **4.83:1** (AA Pass) |
| **Info**    | `palette.blue.600`  | `#0284C7` | Use `blue.700` (`#0369A1`, **5.57:1**) on `blue.50` (`#F0F9FF`) |

> **Contrast Rule for Feedback:** Mid-tone 600-series feedback colors are calibrated as accent strokes, icons, and indicator marks. For readable text inside alert banners, pair light `.50` backgrounds with darker `.700` or `.800` text to guarantee WCAG AA ($\ge 4.5:1$).

---

## 4. Non-Text Contrast (WCAG 2.1 SC 1.4.11)

- **Interior Dividers (`border.subtle` `#E2E8F0` = 1.23:1):** Intentionally subtle for visual grouping without visual noise (exempt from SC 1.4.11 as non-interactive boundaries).
- **Control Outlines (`border.default` `#CBD5E1` = 1.48:1):** Supported by container fill; active interaction states reach high-contrast thresholds.
- **Focus Rings (`focus.ring` `#2563EB` = 5.17:1 on white):** Massively exceeds the 3.0:1 requirement.
- **High Contrast Mode (`neutral.1000` `#000000` = 21:1):** Guarantees maximum boundary visibility.

---

## 5. Data Visualization Palette & Multi-Dimensional Encoding

The calibrated 8-color series provides distinct hues with $\ge 3:1$ contrast against light canvas:
1. Sapphire: `#2563EB` (5.17:1)
2. Emerald: `#059669` (3.77:1)
3. Amber: `#D97706` (3.19:1)
4. Violet: `#7C3AED` (5.70:1)
5. Crimson: `#DC2626` (4.83:1)
6. Cerulean: `#0284C7` (4.10:1)
7. Coral: `#EA580C` (3.56:1)
8. Slate: `#475569` (7.58:1)

### Accessible Chart Design Standards:
- Never rely solely on color hue to convey data series.
- Use **redundant encodings**: line dash patterns (`dashed`, `dotted`, `solid`), data point markers (`circle`, `square`, `triangle`), and direct text labeling.
