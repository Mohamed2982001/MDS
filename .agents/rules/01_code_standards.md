# Agent Rule: Code Standards & File Size Thresholds

## 1. File Size Guideline (500-Line Decomposition Threshold)
- **500 Lines as a Decomposition Heuristic:** 500 lines acts as a healthy warning threshold and trigger for modular decomposition, NOT an arbitrary knife that forces unnatural or fragmented splitting.
- **Natural Cohesion:** If a complex, coherent component or controller legitimately reaches ~520 lines, do not arbitrarily mutilate it into disjointed fragments just to satisfy a rigid counter.
- **Proactive Refactoring:** If any component, controller, widget, or service approaches 400+ lines, actively evaluate it for extractable sub-widgets, domain hooks, or composable utility modules to avoid God classes.
- **Composition Over Inheritance:** Always prefer small, focused, composable units over monolithic structures.

## 2. Token Discipline & Zero Arbitrary Values
- **Zero Raw Visual Values:** Never hardcode raw hex colors, raw pixel paddings, arbitrary border radii, or arbitrary z-index values in components.
- **Token Hierarchy:**
  1. Component Token (`component.button.primary.background`)
  2. Semantic Token (`color.action.primary`, `color.surface.default`)
  3. Primitive Token (`color.blue.500`, `space.16`, `radius.12`)
  4. If none exists, flag as `[TBD — requires design decision]`. Do NOT invent arbitrary values.
- **No In-line Magic Numbers:** All measurements, durations, and curves must reference MDS tokens.

## 3. Clean Architecture & Structure
- **Unidirectional Layer Dependencies:** Lower layers must NEVER depend on higher layers.
  - Allowed: `Template` -> `Pattern` -> `Component` -> `Primitive` -> `Token` -> `Foundation`.
  - Forbidden: `Component` importing from `Pattern`, or `Primitive` importing from `Component`.
- **Feature-First Organization:** When writing application modules, adhere to Clean Architecture with feature-first folder structures.
- **Strict Null Safety:** Sound null safety at all times. Avoid the `!` non-null assertion operator unless statically proven and strictly documented.

## 4. Documentation & Verification
- Keep all files cleanly typed (TypeScript / Dart strict analysis).
- No commented-out code in delivered solutions.
- Every architectural change must update the corresponding documentation and `docs/PROJECT_HISTORY.md`.
