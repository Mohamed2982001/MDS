# Master Design System (MDS) — Reference Runtime Laboratory

**Architecture Layer:** Layer 13 / Phase 9.5 (Reference Runtime Laboratory)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Current Milestone:** Phase 9.5 (Interactive Playground)  
**Governance:** Strict Shared-Core Consumer (`MDS/Runtime/` is immutable)

---

## 🏛️ Purpose & Philosophy

> *"Build the laboratory, not another system."*

The MDS Interactive Playground is **NOT** a new design system, **NOT** a marketing showcase, **NOT** a replacement for the Documentation Portal, and **NOT** a full product dashboard. 

It is a **Reference Runtime Laboratory** designed to:
1. Exercise, test, and inspect all **19 Canonical Core Components** in real-time.
2. Verify CSS Cascade Layer discipline (`@layer mds.reset, mds.tokens, mds.foundations, mds.primitives, mds.components, mds.overrides`).
3. Demonstrate multi-dimensional theme switching (`light`, `dark`, `high-contrast`) and visual presets (`soft`, `refined`, `expressive`).
4. Validate spatial density transitions (`comfortable` 40px vs `compact` 32px), with `dense` (28px) visibly enforced as `[Deferred]`.
5. Verify bidirectional consistency (RTL default with Arabic Cairo typography and LTR symmetry).
6. Simulate universal interaction state machine transitions (FSM: `IDLE` through `ERROR_INTERCEPTED`).
7. Provide an interactive **Token Inspector** querying compiled DTCG tokens directly.
8. Validate **Accessibility Invariants** (FocusTrap, PressTarget >= 44x44px, 2px FocusRing, LiveRegion decoupling).

---

## ⚙️ Architecture & Zero-Dependency Law

- **Zero npm/pip runtime dependencies:** Pure Modern Web Standards (HTML5, Native CSS Cascade Layers, CSS Custom Properties, Vanilla JavaScript ES Modules, Custom Elements).
- **Direct Runtime Consumption:**
  - Stylesheet: `../Runtime/css/mds-core.css`
  - Interactive Controllers: `../Runtime/components/components.js` (`<mds-switch>`, `<mds-tabs>`, `<mds-dialog>`, `<mds-tooltip>`)
  - Tokens: `../Runtime/tokens/dist/tokens.json` & `tokens.css`
- **Zero Runtime Mutation:** The playground never alters, patches, or overrides core runtime files.

---

## 📂 Directory Structure

```text
MDS/Playground/
├── index.html                   # Master application shell, 11 sections, semantic landmarks
├── playground.css               # Shell layout, specimen cards, laboratory styling (@layer mds.overrides)
├── playground.js                # Shell controller, router, live controls, FSM lab, Token Inspector
├── fixtures/
│   └── sample_data.json         # Mock data for Table and card specimens
├── tests/
│   ├── __init__.py
│   └── test_playground.py       # Automated verification suite (13 tests)
└── README.md                    # Operational guide and architecture
```

---

## 🚀 How to Run & Inspect

Because the playground utilizes native JavaScript ES Modules (`import ... from "../Runtime/..."`) and fetches `tokens.json`, it must be served via any standard HTTP file server (to satisfy browser CORS / module origin security).

### Method 1: Python Standard Library (Zero dependencies)
```bash
cd "D:\Work\Dev\Master Design System\MDS"
python -m http.server 8000
```
Open in browser:
👉 `http://localhost:8000/Playground/index.html`

### Method 2: Node npx (Zero install)
```bash
npx serve "D:\Work\Dev\Master Design System\MDS" -p 8000
```

---

## 🧪 Automated Testing

Execute the automated playground laboratory verification suite:
```bash
python "MDS/Playground/tests/test_playground.py"
```

The test suite validates:
- [x] File inventory and absence of node_modules/package.json
- [x] Runtime import linkage (`mds-core.css`, `components.js`)
- [x] Default Arabic RTL and Cairo typography
- [x] All 11 architectural sections present
- [x] All 19 canonical components represented in specimens
- [x] Zero leaks of banned deferred enterprise systems
- [x] Dense tier disabled and labeled `[Deferred]`
- [x] 100% CSS Logical Properties (0 physical left/right)
- [x] Zero functional `row-reverse`
- [x] Zero raw hex colors in `playground.css`
- [x] Sample fixtures integrity

---

## 🔒 Governance & Next Phase Gate

- **Phase 9.5 Status:** READY FOR FINAL AUDIT & LOCK.
- **Phase 9.6 Gate:** Strict Stop Condition — Phase 9.6 (Reference Application) MUST NOT begin until Phase 9.5 is formally approved and locked by the lead architect.
