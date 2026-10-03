# MDS Foundation: Typography Specification
**Foundational Layer:** 01-Foundations  
**Status:** APPROVED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Multilingual Typography Strategy

Arabic and Latin scripts are treated with equal visual priority in MDS. Rather than treating Arabic as a secondary localized fallback, MDS adopts a **unified bilingual typographic strategy**:

- **Primary Multilingual Typeface:** **Cairo** (Google Fonts).
  - *Design Judgment:* Cairo was selected as the unified primary typeface for both Arabic and Latin to promote stylistic harmony, shared geometric proportions, and visual coherence across bilingual interfaces, avoiding the visual dissonance of uncoordinated dual-font fallbacks.
  - *Contextual Leading:* Because Arabic script features extended vertical strokes, high ascenders, and diacritics (harakat), Arabic typography requires an intentional **+0.15 line-height increase** over Latin baselines to prevent glyph collision.
- **Monospace Typeface:** **JetBrains Mono** for developer consoles, code blocks, JSON schemas, and tabular telemetry.

---

## 2. Calibrated Typographic Scale

MDS adopts a **Discretized Typographic Scale** optimized for UI pixel-snapping, readability, and visual hierarchy, loosely structured around a Minor Third interval stepping (1.200–1.250) from a 16px baseline:

| Token | Pixels | Rem (16px base) | Semantic Role & Hierarchy |
| :--- | :---: | :---: | :--- |
| `font.size.xs`  | 12px | 0.750rem | Captions, metadata timestamps, fine print, tags |
| `font.size.sm`  | 14px | 0.875rem | Form input labels, helper text, dense table data |
| `font.size.base`| 16px | 1.000rem | **Standard Body Copy:** Articles, reading text, primary inputs |
| `font.size.lg`  | 20px | 1.250rem | Card headings, section sub-titles, large callouts |
| `font.size.xl`  | 24px | 1.500rem | Page subsection titles, modal dialog headers |
| `font.size.2xl` | 30px | 1.875rem | Major dashboard view titles, primary page headers |
| `font.size.3xl` | 36px | 2.250rem | Display metrics, marketing headers, featured stats |
| `font.size.4xl` | 48px | 3.000rem | High-impact hero display text, showcase banners |

---

## 3. Font Weights & Semantic Roles

| Token | Numeric | Role & Usage |
| :--- | :---: | :--- |
| `font.weight.regular`  | 400 | Long-form body copy, descriptive paragraphs |
| `font.weight.medium`   | 500 | Interactive buttons, input text, table headers |
| `font.weight.semibold` | 600 | Section headings, highlighted cards, emphasized alerts |
| `font.weight.bold`     | 700 | Primary view titles, hero display copy, KPI stat values |

---

## 4. Context-Aware Line Heights

Vertical rhythm adapts dynamically between Latin and Arabic scripts:

| Token | Latin Multiplier | Arabic Context Multiplier | Recommended Usage |
| :--- | :---: | :---: | :--- |
| `font.lineHeight.tight`   | **1.25** | **1.35–1.40** | Display titles, short multi-line headings |
| `font.lineHeight.normal`  | **1.50** | **1.65**      | Standard body copy, articles, form controls |
| `font.lineHeight.relaxed` | **1.75** | **1.85**      | Extended long-form editorial and legal text |

---

## 5. Tabular Numerals & Data Alignment

To prevent horizontal jitter when numeric values update dynamically (e.g. counters, financial tables, system telemetry), MDS specifies:
- **Tabular Figures (`tnum`):** Required for data tables, currency amounts, timestamps, and live progress counters (`font-variant-numeric: tabular-nums`).
- **Proportional Figures:** Default for general narrative copy and paragraph text.
