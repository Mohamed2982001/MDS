# Master Design System (MDS) — Automated Test Architecture & Regression Harness

## 1. Executive Summary & Vision

> *"A design system without regression protection is a design system that slowly drifts, degrades, and changes without knowing it. Automated testing in MDS is the mathematical guarantee that foundations, tokens, primitives, components, patterns, workflows, and accessibility contracts remain deterministic, inviolable, and uncorrupted over time."*

This document establishes the authoritative **Automated Test Architecture** for the Master Design System (MDS) under **Phase 8.1.2**. It formalizes the multi-tier testing pyramid, test classification, execution harnesses, and validation contracts governing every layer of the system.

---

## 2. Runtime Reality & Environment Assessment

In strict adherence to Section 3 of the Phase 8.1.2 mandate, the current host environment and repository structure have been inspected:

| Environmental Dimension | Detected Reality | Architectural Strategy |
| :--- | :--- | :--- |
| **Package Manager** | `npm` (11.9.0) available; root project currently unbundled (no root `package.json`). | Avoid creating competing ad-hoc npm structures; build lightweight, self-contained, native Python/Node test harness. |
| **Host Tooling** | `Python 3.12.10`, `Node.js v24.14.0`. | Use native Python 3.12 test runner (`MDS/10-Testing/run_tests.py`) with zero external package bloat for deterministic execution. |
| **Repository Structure** | W3C DTCG token repositories (`02-Tokens`), HTML5/CSS primitives & showcases (`03`, `05`, `06`), and exhaustive markdown architectural contracts (`01`–`09`). | Execute structural, token alias, CSS logical property, AST syntax, FSM, and invariant validation directly. |
| **Headless Browser Driver** | No active headless browser runner (Playwright / Puppeteer) installed or configured in root. | Mark live visual pixel diffing and headless browser DOM testing as `NOT_EXECUTABLE_IN_CURRENT_RUNTIME (Requires Headless Browser Driver)`. Never fabricate results. |
| **Assistive Technology** | NVDA / VoiceOver / TalkBack daemons not physically installed/running. | Retain Physical AT as `DEFERRED` per Phase 8.1.1. |

---

## 3. The MDS Testing Pyramid

Testing in MDS is strictly structured as an inverted-cost pyramid where contracts are proven at the lowest possible level:

```text
               ┌─────────────────────────────┐
               │    Visual Regression (VIS)   │  ◄── Snapshot diffing (Deferred to CI browser)
               ├─────────────────────────────┤
               │   Workflow & FSM Tests (WKF) │  ◄── State transitions, guards, recovery
               ├─────────────────────────────┤
               │    Pattern Tests (PAT)       │  ◄── Composition laws, parent-owned spacing
               ├─────────────────────────────┤
               │   Component Tests (CMP)      │  ◄── 19 core components, states, a11y roles
               ├─────────────────────────────┤
               │   Primitive Tests (PRI)      │  ◄── Hit-boxes (44px), containers, surface triad
               ├─────────────────────────────┤
               │  A11y & RTL Tests (A11Y/RTL) │  ◄── Zero row-reverse, logical properties
               ├─────────────────────────────┤
               │    Token Integrity (TKN)     │  ◄── DTCG schema, 188 tokens, 0 broken aliases
               ├─────────────────────────────┤
               │  Static / Schema Validation  │  ◄── Directory boundaries, 0 enterprise leaks
               └─────────────────────────────┘
```

### Core Testing Principle:
Never use an end-to-end or visual test for something that can be proven deterministically through token graph resolution, CSS AST validation, or state machine unit tests.

---

## 4. Test Suite Taxonomy & Grammars

Every automated test in MDS possesses a permanent, unique identifier conforming to the grammar:

$$\text{MDS-}[\text{LAYER/DOMAIN}]-\text{[001-999]}$$

| Category Code | Layer / Domain | Scope | Executable in Current Runtime? |
| :--- | :--- | :--- | :---: |
| **`MDS-TKN-###`** | Tokens (Layer 02) | DTCG syntax, 188 tokens, alias resolution, themes, zero raw hex | **YES** (100% Executable) |
| **`MDS-PRI-###`** | Primitives (Layer 03) | Layout bounds, Surface triad, PressTarget 44px, FocusRing 2px | **YES** (Contract & CSS Executable) |
| **`MDS-CMP-###`** | Components (Layer 04) | 19 Core Components, 16-point anatomy, semantic roles, inputs | **YES** (Contract & Spec Executable) |
| **`MDS-PAT-###`** | Patterns (Layer 05) | 8 Core Patterns, 22-point anatomy, parent-owned spacing | **YES** (Contract & Showcase Executable) |
| **`MDS-WKF-###`** | Workflows (Layer 06) | 6 Canonical Workflows, 27-point anatomy, FSM transitions | **YES** (Contract & State Executable) |
| **`MDS-A11Y-###`** | Accessibility (09) | Roles, live regions, focus contracts, non-text contrast | **YES** (Static & Markup Executable) |
| **`MDS-RTL-###`** | Bidirectional (RTL) | Zero `row-reverse`, 100% CSS Logical Properties, DOM order | **YES** (100% Executable) |
| **`MDS-RWD-###`** | Responsive (RWD) | Breakpoints (320px–1440px), softWrap, overflow safety | **PARTIAL** (CSS Executable; Browser Deferred) |
| **`MDS-EXP-###`** | Experience States | Empty, Loading, Error, Success, Recovery contracts | **YES** (Contract Executable) |
| **`MDS-VIS-###`** | Visual Regression | Pixel-diffing across Light, Dark, High Contrast, RTL | **DEFERRED** (Requires Headless Browser Driver) |

---

## 5. Architectural Contract Verification Levels

### 5.1 Token Integrity Engine (`MDS-TKN-###`)
1. **DTCG Structure:** Evaluates all 18 `.tokens.json` files against standard W3C DTCG `$value` and `$type` syntax.
2. **Graph Traversal & Alias Resolution:** Resolves all `{alias}` references across Primitive $\to$ Semantic $\to$ Component $\to$ Theme tiers.
3. **Cycle Detection:** Ensures directed acyclic graph (DAG) invariants with depth $\le 3$ hops.
4. **Forbidden Literal Scanner:** Scans all codebase stylesheets (`.css`) to guarantee exactly **0 raw hex colors (`#[0-9a-fA-F]{3,6}`)**.

### 5.2 RTL & Logical Property Guard (`MDS-RTL-###`)
1. **Anti-Row-Reverse Invariant:** Verifies zero occurrences of `flex-direction: row-reverse` to protect WCAG SC 2.4.3 focus order.
2. **CSS Logical Properties:** Flags any physical directional spacing hacks (`margin-left`, `margin-right`, `padding-left`, `padding-right`, `left`, `right`).

### 5.3 Layer Boundary & Anti-Bloat Guard (`MDS-PRI-###`, `MDS-CMP-###`, `MDS-PAT-###`)
1. **Component Inventory Invariant:** Confirms exactly **19 Core Components** across 6 families.
2. **Pattern Inventory Invariant:** Confirms exactly **8 Canonical Patterns** across 6 families.
3. **Workflow Inventory Invariant:** Confirms exactly **6 Canonical Workflows**.
4. **Enterprise System Deferral Guard:** Confirms that the **9 complex enterprise systems** (`DataGrid`, `RichTextEditor`, `Calendar`, `DateRangePicker`, `CommandSystem`, `Tree`, `Combobox`, `VirtualizedList`, `FileUploadManager`) have zero unapproved implementations.

### 5.4 Finite State Machine Determinism (`MDS-WKF-###`)
1. **Transition Table Completeness:** Verifies that every canonical workflow implements explicit transitions across universal states (`IDLE`, `ACTIVE_INPUT`, `VALIDATING`, `CONFIRMING`, `PROCESSING`, `STREAMING`, `REVIEWING`, `SUCCESS_RESOLVED`, `ERROR_INTERCEPTED`, `FATAL_FAILURE`, `ABORTED_CANCEL`).
2. **Negative Transition Tests:** Proves that invalid state transitions (e.g., jumping from `IDLE` directly to `SUCCESS_RESOLVED` without validation or processing) are rejected by state guards.

---

## 6. The Central Regression Harness (`run_tests.py`)

MDS provides an automated, executable regression test suite runner located at:
`d:/Work/Dev/Master Design System/MDS/10-Testing/run_tests.py`

### Executable Test Pipeline:
```text
[1. Token & Schema Integrity] ──► [2. RTL & Logical Properties] ──► [3. Component Invariants] ──►
[4. Pattern Compositions]     ──► [5. Workflow FSM Engine]       ──► [6. Accessibility Contracts]
```

### Execution Command:
```bash
python "d:/Work/Dev/Master Design System/MDS/10-Testing/run_tests.py"
```

The runner produces deterministic, machine-readable test reports indicating passes, failures, and unsupported categories without fabrication.
