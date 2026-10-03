# MDS Primitives: Accessibility Suite
**Document Layer:** 03-Primitives / Accessibility  
**Status:** APPROVED (Phase 4 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Executive Summary & Philosophy

The **Accessibility Primitives** provide reusable, platform-agnostic infrastructure designed to support inclusive interaction, keyboard operability, screen reader assistive semantics, vestibular protection, and alignment with **WCAG 2.1/2.2 AA** guidelines (while exceeding target size minimums via the internal 44×44px MDS touch policy).

```text
Accessibility Primitives
 ├── VisuallyHidden (Screen-reader-only accessible labels and descriptions)
 ├── FocusTrap      (Keyboard focus loop constraint for modals and drawers)
 ├── LiveRegion     (ARIA live announcements for dynamic async updates)
 └── ReducedMotion  (Vestibular protection collapsing motion to 0ms)
```

---

## 2. Primitive Specifications

### 2.1 `VisuallyHidden` Primitive
- **Purpose:** Hides content visually while keeping it fully discoverable and readable by screen readers. Used for icon-only button labels, screen-reader table headers, and status descriptions.
- **Implementation Mechanism (CSS clip pattern):**
  ```css
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
  ```
- **Semantic Tag:** `<span>` by default.
- **Anti-Pattern Guard:** NEVER use `display: none;` or `visibility: hidden;` for accessible names, as both completely remove the element from the accessibility tree.

### 2.2 `FocusTrap` Primitive
- **Purpose:** Restricts keyboard `Tab` navigation strictly within an active modal container (dialog, slide-over drawer), preventing focus from escaping into the inert background document.
- **Focus Lifecycle Management:**
  1. **Activation:** On mount, automatically moves focus to the first focusable child element (or a specific `initialFocus` element).
  2. **Loop Constraint:** When `Tab` is pressed on the last focusable element, wraps focus back to the first focusable element. When `Shift+Tab` is pressed on the first element, wraps to the last.
  3. **Escape Key Handling:** Listens for the `Escape` key to trigger the container's dismissal callback.
  4. **Restoration:** On unmount, restores focus precisely back to the trigger element that launched the modal.

### 2.3 `LiveRegion` Primitive
- **Purpose:** Announces dynamic status messages, asynchronous completion, validation errors, and AI streaming tokens to screen reader users without stealing focus.
- **API & Modes:**
  - `mode="polite"` (Default): Screen reader waits until the user finishes their current task before announcing. Ideal for search results count, background saves, and status changes.
  - `mode="assertive"`: Screen reader interrupts current speech immediately. Reserved strictly for critical errors, system disconnections, or time-sensitive alerts.
- **Attributes Applied:** `aria-live="polite|assertive"`, `aria-atomic="true"`, `role="status|alert"`.

### 2.4 `ReducedMotion` Primitive / Hook
- **Purpose:** Safeguards users with vestibular disorders by detecting the operating system's reduced-motion preference (`prefers-reduced-motion: reduce`).
- **Behavior:**
  - When reduced motion is requested, all MDS transition durations automatically collapse to `motion.duration.instant` (**0ms**).
  - Replaces sliding and scaling transitions with instantaneous state switches or gentle 0ms opacity reveals.

---

## 3. Normalized Accessibility API

| Primitive | Key Properties | Default | Role / Output |
| :--- | :--- | :--- | :--- |
| `VisuallyHidden` | `as`, `children` | `'span'` | Accessible screen-reader text |
| `FocusTrap` | `active`, `initialFocus`, `returnFocus` | `true` | Traps keyboard focus loop |
| `LiveRegion` | `mode`, `atomic` | `'polite'`, `true` | Dynamic ARIA announcements |
| `ReducedMotion` | `children`, `fallback` | — | Overrides animation durations to 0ms |

---

## 4. MDS Rules vs. Platform Implementation Scope

| Accessibility Requirement | MDS Architectural Rule | Platform Implementation |
| :--- | :--- | :--- |
| **Touch Target Area** | Mandatory min 44×44px hit boundary on touch (MDS rule; exceeds WCAG 2.2 AA 2.5.8 24×24px, aligns with AAA 2.5.5) | `PressTarget` expands `::after` hit area (Web) / `BoxConstraints` (Flutter) |
| **Non-Text Contrast** | Focus ring $\ge 3:1$ contrast against surface (WCAG 2.1 AA SC 1.4.11) | 2px solid `color.brand.600` (`#2563EB`) with 2px offset |
| **Text Contrast** | WCAG AA ($4.5:1$ body, $3:1$ large) | Validated via `02-Color.md` and automated contrast tests |
| **Screen Reader Labels** | Icon buttons require non-visual text | Mandate `VisuallyHidden` child or `aria-label` |
| **Reduced Motion** | Zero spatial translation animations | CSS media query `@media (prefers-reduced-motion: reduce)` |

---

## 5. Anti-Patterns (Forbidden Usage)

- ❌ Using `display: none` for accessible screen-reader labels.
- ❌ Building modal overlays without a `FocusTrap` (allows tab navigation into invisible background content).
- ❌ Using `mode="assertive"` on normal background data refreshes (disorients blind users).
- ❌ Ignoring `prefers-reduced-motion` and forcing long animations.

---

## 6. AI Usage Rules

- **ICON BUTTONS:** Whenever generating an icon-only button, an AI agent MUST include `<VisuallyHidden>Label text</VisuallyHidden>`.
- **MODAL DIALOGS:** Every modal dialog or sheet MUST wrap its interior in `<FocusTrap>`.
- **ASYNC ACTIONS:** Wrap dynamic status notices (e.g. "Draft saved") in `<LiveRegion mode="polite">`.
