# Agent Rule: Responsive Philosophy & Device Strategy

## 1. Core Philosophy: Recomposition, Not Shrinking
- Responsive design in MDS is **recomposition of layout hierarchy**, not simply scaling or shrinking desktop elements with `width: 100%`.
- Reorganization of layout must preserve:
  - Visual hierarchy
  - Information density
  - Ergonomics and touch targets

## 2. Dedicated Tablet & iPad Support
- **First-Class Tablet Experience:** Tablets and iPads must NOT simply receive a stretched mobile layout or an unconstrained desktop view.
- **Dedicated Tablet Layouts:**
  - Leverage Split-Screen / Master-Detail patterns (navigation list on the left/start, detailed workspace on the right/end).
  - Use adaptive multi-pane views and popovers instead of full-screen page transitions.
  - Optimize for both Portrait and Landscape orientations.
## 3. Form Factor Considerations
1. **Mobile (< 768px):**
   - Single-column flow, bottom sheets for overlays, bottom navigation or drawer, minimum 44×44px interactive touch targets (MDS internal design-system rule; stricter than applicable WCAG AA 2.5.8 minimum, aligned with AAA 2.5.5).
2. **Tablet (768px – 1023px):**
   - Dedicated master-detail / dual-pane layouts, contextual sidebars, adaptable dialogs. Never stretch mobile layouts or squash desktop layouts.
3. **Desktop (1024px – 1439px):**
   - Multi-column layouts, persistent sidebars, rich data tables, hover and tooltips enabled. Standard container max-width: **1152px** (`container.lg`).
4. **Wide Screens (≥ 1440px):**
   - Wide container max-width containment: **1440px** (`container.xl`) to protect line-length legibility. (1280px is strictly forbidden).

## 4. Typography & Interaction Rules
- **No Text Truncation with Ellipsis on Descriptive Text:** Use `softWrap: true` and allow 2+ lines with proper leading.
- **Pointer vs. Touch:** Never rely solely on hover interactions. Always provide tap/click parity.
