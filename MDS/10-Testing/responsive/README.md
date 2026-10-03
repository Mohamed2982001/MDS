# MDS Responsive Viewport Automation Engine (Layer K)

**Phase 9.7.6: Responsive Viewport Automation Engine**  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Promoted Capability:** `MDS-RWD-003` (`DEFERRED` $\to$ `ACTIVE`)

---

## 1. Overview & Purpose

The Responsive Viewport Automation Engine delivers automated multi-viewport testing across Google Chrome using the standard-library Chrome DevTools Protocol (`CDPBrowserDriver`) established in Phase 9.7.4.

It enforces the foundational responsive law:
$$\textbf{Recomposition, Not Shrinking}$$

---

## 2. Canonical Viewports

Defined strictly in `03-Spacing-and-Grid.md` and ratified under ADR-074:

| Tier | Width | Height | Scale Factor | Mobile Emulation | Intent |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Mobile** | `320px` | `640px` | `2.0` | `true` | Compact single-column touch ergonomics |
| **Tablet** | `768px` | `1024px` | `2.0` | `true` | Collapsed 72px icon rail with touch ergonomics |
| **Desktop**| `1024px`| `768px` | `1.0` | `false` | Multi-column workspace with expanded navigation |
| **Wide**   | `1440px`| `900px` | `1.0` | `false` | High-throughput data layout with bounded container |

*Constraint:* Non-canonical breakpoints (e.g. `1280px`) are strictly forbidden.

---

## 3. Canonical 17-Run Deterministic Execution Matrix

The matrix executes **exactly 17 isolated runs**:
- **Tier 1 (Runs 1–12):** Canonical Recomposition Sweep across 3 archetype screens (`Overview`, `Items List`, `Item Edit`) $\times$ 4 viewports (`320px`, `768px`, `1024px`, `1440px`) in RTL, Light, Comfortable.
- **Tier 2 (Runs 13–17):** Orthogonal Invariant Checks:
  - `RWD-RUN-013`: Mobile LTR symmetry (start-aligned nav toggle)
  - `RWD-RUN-014`: Tablet LTR symmetry (left-anchored 72px icon rail)
  - `RWD-RUN-015`: Mobile Compact density touch target invariant ($\ge 44\times 44$px preserved)
  - `RWD-RUN-016`: Desktop Compact density table row compacting
  - `RWD-RUN-017`: Mobile High Contrast theme borders and reflow stability

---

## 4. Tri-Class Assertion Model

Every assertion evaluated against live DOM is partitioned into:
1. **`HARD_CONTRACT`**: Non-negotiable structural contracts (e.g. zero horizontal blowout, container $\le 1440$px, mobile trigger visible at 320px, $\ge 44\times 44$px touch targets). Failure = **`FAIL`**.
2. **`OBSERVABLE_BEHAVIOR`**: Measurable layout recomposition (e.g. stats grid 1/2/4 columns, form grid 1/2 columns, 72px tablet rail). Failure = **`FAIL`**.
3. **`INFORMATIONAL_MEASUREMENT`**: Telemetry and diagnostic data. Never determines PASS/FAIL.

---

## 5. Hardened Layout Reflow Settlement

Before evaluating assertions, each viewport change awaits layout settlement:
- $2\times$ `requestAnimationFrame` for CSS reflow
- `document.fonts.ready` for typography metrics
- Bounded 1500ms timeout with 50ms polling interval.
