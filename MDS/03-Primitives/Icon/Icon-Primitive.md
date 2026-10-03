# MDS Primitive: Icon Contract
**Document Layer:** 03-Primitives / Icon  
**Status:** APPROVED (Phase 4 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Executive Summary & Vendor-Agnostic Philosophy

The **Icon Primitive** establishes a vendor-agnostic contract for rendering vector icons within MDS. It enforces optical weight consistency, standardized bounding boxes, accessible screen-reader semantics, and strict **RTL Mirroring Taxonomy** without locking the design system to a single icon library (works seamlessly with inline SVGs, Lucide, Heroicons, Material Symbols, or Flutter `IconData`).

---

## 2. Standardized Icon Sizing Scale

All icons are rendered on standardized square bounding boxes to preserve visual balance across interfaces:

| Token | Box Dimension | Optical Weight | Paired UI Context |
| :--- | :---: | :---: | :--- |
| `size.icon.xs` | **14px** | ~12px | Micro annotations, helper tooltips, inline status tags |
| `size.icon.sm` | **16px** | ~14px | Paired with `font.size.sm` (14px) inside compact controls |
| `size.icon.md` | **20px** | ~18px | **Standard Default:** Paired with standard 40px controls and navigation |
| `size.icon.lg` | **24px** | ~20px | Primary navigation sidebar, standalone toolbar action items |
| `size.icon.xl` | **32px** | ~28px | Empty state illustrations, feature announcement headers |

---

## 3. Normalized Icon API Contract

| Property | Type | Default | Values / Description | Token Mapping |
| :--- | :--- | :--- | :--- | :--- |
| `size` | `enum` | `'md'` | `'xs'` (14px), `'sm'` (16px), `'md'` (20px), `'lg'` (24px), `'xl'` (32px) | `size.icon.*` |
| `color` | `enum \| string` | `'currentColor'` | `'primary'`, `'secondary'`, `'brand'`, `'danger'`, `'success'`, `'currentColor'` | `color.text.*`, `color.action.*` |
| `mirrorRTL` | `boolean` | `false` | When true, mirrors icon horizontally (`scaleX(-1)`) in RTL viewports | — |
| `decorative` | `boolean` | `true` | When true, applies `aria-hidden="true"`; when false, requires `label` | — |
| `label` | `string` | `null` | Accessible screen-reader label for standalone standalone icons | — |
| `as` | `component` | SVG / IconData | Vector SVG component or icon renderer | — |

---

## 4. Strict RTL Mirroring Taxonomy

MDS categorizes all icons into a 4-tier behavioral taxonomy (established in `08-Iconography.md`):

```text
┌──────────────────────────────┬──────────────────────────────┐
│ TIER 1: DIRECTIONAL / FLOW   │ TIER 2: PROGRESS / PLAYBACK  │
│ [MUST MIRROR IN RTL]         │ [MUST MIRROR IN RTL]         │
│ • Arrow right/left           │ • Next / Previous step       │
│ • Chevron right/left         │ • Undo / Redo                │
│ • Back / Forward navigation  │ • History rewind / advance   │
├──────────────────────────────┼──────────────────────────────┤
│ TIER 3: PHYSICAL OBJECTS     │ TIER 4: MEDIA & SYMBOLS      │
│ [NEVER MIRROR IN RTL]        │ [NEVER MIRROR IN RTL]        │
│ • Magnifying glass (search)  │ • Play / Pause / Stop        │
│ • Trash can (delete)         │ • Clock (clockwise rotation) │
│ • Camera, Bell, Calendar     │ • Slash badges, Checkmarks   │
└──────────────────────────────┴──────────────────────────────┘
```

- In CSS, mirroring is applied via:
  ```css
  [dir="rtl"] .mds-icon--mirror-rtl {
    transform: scaleX(-1);
  }
  ```

---

## 5. Accessibility Contract

1. **Decorative Icons (`decorative={true}`):**
   - When paired with adjacent visible text (e.g. `<Inline><Icon as={SaveIcon} /><Text>Save</Text></Inline>`), the icon is purely decorative.
   - The primitive **must** output `aria-hidden="true"` so screen readers do not announce duplicate labels.
2. **Standalone Interactive Icons (`decorative={false}`):**
   - When an icon serves as an interactive button on its own (e.g. Close, Search), it **must** provide `label="Close dialog"` or contain an embedded `<VisuallyHidden>` text label.
   - It **must** be wrapped in a `<PressTarget>` to guarantee a $44 \times 44\text{px}$ hit area on touch interfaces.

---

## 6. Anti-Patterns (Forbidden Usage)

- ❌ Mirroring physical objects (e.g. flipping a magnifying glass in Arabic).
- ❌ Hardcoding pixel dimensions (e.g. `width: 17px; height: 17px;`).
- ❌ Standalone icon button with no accessible name.
- ❌ Interactive icon with no `PressTarget` wrapper (violating 44px hit-box rule).

---

## 7. AI Usage Rules

- **WHEN TO MIRROR:** Set `mirrorRTL={true}` ONLY on navigational arrows, back/forward buttons, and directional carets.
- **DECORATIVE RULE:** If text is next to the icon, always set `decorative={true}`.
- **STANDALONE RULE:** Never output an isolated `<Icon />` without an accessible `label` and a `<PressTarget>`.
