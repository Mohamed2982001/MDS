# MDS Primitives: Typography Suite
**Document Layer:** 03-Primitives / Typography  
**Status:** APPROVED (Phase 4 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Executive Summary & Multilingual Architecture

The **Typography Primitives** provide the semantic foundation for all text rendered within MDS. They enforce the approved **Cairo unified bilingual typographic strategy**, eliminate arbitrary font sizing, guarantee tabular alignment for numeric data, and strictly enforce the **No Text Truncation with Ellipsis on Descriptive Text** rule.

---

## 2. Taxonomy of Typography Primitives

```text
Typography Primitives
 ├── Text          (General body copy, paragraphs, spans)
 ├── Heading       (H1 to H6 semantic section titles)
 ├── Label         (Form field labels, metadata keys)
 ├── Caption       (Timestamps, footnotes, micro annotations)
 ├── HelperText    (Validation feedback & contextual field help)
 ├── Numeric       (Tabular numerals for money, counters, data tables)
 └── Code          (Monospace technical identifiers & code blocks)
```

---

## 3. Primitive Specifications

### 3.1 `Text` Primitive
- **Purpose:** Primary building block for body copy, paragraphs, and inline text.
- **Semantic HTML:** `<p>` (default for blocks) or `<span>` (for inline spans).
- **API & Props:**
  - `size`: `'xs'` (12px), `'sm'` (14px), `'base'` (16px default), `'lg'` (20px).
  - `weight`: `'regular'` (400 default), `'medium'` (500), `'semibold'` (600), `'bold'` (700).
  - `color`: `'primary'` (`color.text.primary`), `'secondary'` (`color.text.secondary`), `'inverse'` (`color.text.inverse`), `'brand'` (`color.brand.600`).
  - `lineHeight`: `'tight'` (1.25), `'normal'` (1.50 default), `'relaxed'` (1.75).
  - `softWrap`: `boolean` (default `true`).
  - `truncate`: `boolean` (default `false`). *Strict MDS Rule: Only permitted on isolated single-line URL paths or file names; never on functional or descriptive content.*

### 3.2 `Heading` Primitive
- **Purpose:** Semantic structural titles and section headers for document hierarchy.
- **Semantic HTML:** Renders semantic `<h1>`, `<h2>`, `<h3>`, `<h4>`, `<h5>`, or `<h6>` based on `level`.
- **API & Level Mapping:**
  - `level={1}`: `<h1>`, 48px (`font.size.4xl`), weight 700 (`bold`), line-height 1.25. (Hero page titles).
  - `level={2}`: `<h2>`, 36px (`font.size.3xl`), weight 700 (`bold`), line-height 1.25. (Major view headers).
  - `level={3}`: `<h3>`, 30px (`font.size.2xl`), weight 600 (`semibold`), line-height 1.25. (Dashboard widget headers).
  - `level={4}`: `<h4>`, 24px (`font.size.xl`), weight 600 (`semibold`), line-height 1.25. (Modal dialog titles).
  - `level={5}`: `<h5>`, 20px (`font.size.lg`), weight 600 (`semibold`), line-height 1.25. (Card titles).
  - `level={6}`: `<h6>`, 16px (`font.size.base`), weight 600 (`semibold`), line-height 1.25. (Form group subheads).
- **Arabic Contextual Leading (MDS Architectural Design Judgment):**
  - Calibrated as an **MDS Design Judgment** rather than an immutable mathematical fact: under Arabic script, multi-line `Heading` and `Text` primitives apply a **+0.15** contextual leading boost (e.g. `font.lineHeight.tight`: $1.25 \to 1.40$; `font.lineHeight.normal`: $1.50 \to 1.65$).
  - **Purpose:** Accommodates Cairo's extended ascender/descender metrics and full Arabic diacritic marks (tashkeel / harakat), preventing vertical clipping or glyph collisions.
  - **Scope Boundaries:** This boost applies strictly to structural reading text (`Heading`, `Text`). It is deliberately **NOT** applied to `<Numeric>` or `<Code>`, which maintain their standard line-heights to preserve tight baseline alignment and terminal code-grid cadence.

### 3.3 `Label` Primitive
- **Purpose:** Accessible form input labels and key metadata markers.
- **Semantic HTML:** `<label>` with required `htmlFor` prop, or `<span>` when used in metadata tables.
- **Tokens:** Fixed at 14px (`font.size.sm`), weight 500 (`font.weight.medium`), color `color.text.primary`.
- **Required Indicator:** Supports `required={true}` which renders an accessible asterisk with `aria-hidden="true"`.

### 3.4 `Caption` Primitive
- **Purpose:** De-emphasized micro copy, timestamps, image captions, and legal disclaimers.
- **Semantic HTML:** `<small>` or `<span>`.
- **Tokens:** Fixed at 12px (`font.size.xs`), weight 400 (`font.weight.regular`), color `color.text.secondary`.

### 3.5 `HelperText` Primitive
- **Purpose:** Form field guidance, validation errors, and success confirmation messages.
- **Semantic HTML:** `<span>` with `id` referenced by input's `aria-describedby`.
- **Status Variants:**
  - `'neutral'`: `color.text.secondary` (12px).
  - `'error'`: `color.feedback.danger` (`red.600`, 12px) with `role="alert"`.
  - `'success'`: `color.green.700` (12px accessible text pairing).

### 3.6 `Numeric` Primitive
- **Purpose:** Prevents horizontal layout jitter in updating numbers, currencies, timers, and data tables.
- **Styling Law:** Enforces `font-variant-numeric: tabular-nums` (`tnum`).
- **Font:** Inherits `font.family.primary` (`Cairo`) with tabular figures enabled, or uses `font.family.mono` (`JetBrains Mono`) for telemetry data.

### 3.7 `Code` Primitive
- **Purpose:** Technical identifiers, API endpoints, JSON payloads, and terminal commands.
- **Semantic HTML:** `<code>` (inline) or `<pre><code>` (block).
- **Tokens:** Fixed to `font.family.mono` (`JetBrains Mono`), 12px/14px, subtle surface fill (`neutral.100`), 1px subtle border (`neutral.200`), 4px corner radius (`radius.xs`).

---

## 4. RTL & Bilingual Invariants

- **Unified Font Family:** Cairo (`font.family.primary`) is applied globally to both Arabic and Latin strings, guaranteeing identical optical baselines.
- **Logical Alignment:** Text aligns to `inline-start` (right in Arabic, left in English) by default.
- **No Ellipsis Truncation Rule:** Descriptive Arabic and English text MUST wrap onto 2+ lines (`softWrap: true`). Truncating functional instructions with ellipsis (`...`) is strictly forbidden.
- **Mixed-Script & Baseline Integrity:** In mixed-language paragraphs (Arabic with inline Latin terms or technical tokens), the paragraph inherits the contextual Arabic leading boost (+0.15) to guarantee diacritic safety, while Latin glyphs align cleanly to Cairo's unified baseline.

---

## 5. Token Mapping Summary

| Primitive | Font Size | Font Weight | Line Height | Text Color |
| :--- | :--- | :--- | :--- | :--- |
| `Text (base)` | `font.size.base` (16px) | `font.weight.regular` (400) | `font.lineHeight.normal` (1.50) | `color.text.primary` |
| `Heading (H1)` | `font.size.4xl` (48px) | `font.weight.bold` (700) | `font.lineHeight.tight` (1.25) | `color.text.primary` |
| `Heading (H3)` | `font.size.2xl` (30px) | `font.weight.semibold` (600) | `font.lineHeight.tight` (1.25) | `color.text.primary` |
| `Label` | `font.size.sm` (14px) | `font.weight.medium` (500) | `font.lineHeight.normal` (1.50) | `color.text.primary` |
| `Caption` | `font.size.xs` (12px) | `font.weight.regular` (400) | `font.lineHeight.normal` (1.50) | `color.text.secondary` |
| `HelperText` | `font.size.xs` (12px) | `font.weight.regular` (400) | `font.lineHeight.normal` (1.50) | Contextual |
| `Code` | `font.size.sm` (14px) | `font.weight.regular` (400) | `font.lineHeight.normal` (1.50) | `font.family.mono` |

---

## 6. Anti-Patterns (Forbidden Usage)

- ❌ Hardcoding font sizes: `font-size: 15px;` or `font-size: 18px;`.
- ❌ Using `font-weight: 900` or arbitrary weights not in the 400/500/600/700 scale.
- ❌ Applying `text-overflow: ellipsis` to user instructional copy.
- ❌ Hardcoding `text-align: left` in multi-lingual apps.

---

## 7. AI Usage Rules

- **ALWAYS USE:** `Text`, `Heading`, `Label`, `Caption`, `HelperText`, `Numeric`, or `Code` for every rendered text string.
- **NEVER WRITE:** Naked `<span>` or `<p>` with raw inline styles.
- **DATA COLUMNS:** Always wrap numbers in `<Numeric>` to prevent layout shifting.
