# MDS Agent Rules & AI Implementation Guardrails

This document establishes the binding operational rules for any AI agent interacting with, extending, or implementing components within the **Master Design System (MDS)** repository.

---

## 1. AI Authority Levels

Every action taken by an AI agent falls under a defined authority tier. Higher levels require explicit human approval and documented architectural justification.

| Level | Classification | Scope of Authority | Human Approval Required? |
| :---: | :--- | :--- | :---: |
| **Level 1** | **Use Existing System** | Direct consumption of existing tokens, primitives, and components. | No (Standard task) |
| **Level 2** | **Compose Existing** | Combining existing primitives and components into new patterns or templates. | No (Standard task) |
| **Level 3** | **Propose Extension** | Proposing a new component token, component variant, or primitive extension. | **Yes** (Must propose spec first) |
| **Level 4** | **Propose Modification** | Proposing a change to an existing component API, token value, or semantic definition. | **Yes** (Requires review) |
| **Level 5** | **Propose Architecture Change** | Modifying layer hierarchy, adding foundational systems, or changing core philosophy. | **Mandatory Explicit Signoff** |

*Rule: An AI agent must NEVER silently modify foundations or tokens at Levels 3, 4, or 5.*

---

## 2. The Existing-First Search Hierarchy

Before proposing or generating any new visual element or component code, the AI agent MUST search through existing assets in this strict order:

```
1. Search Existing Component
      └── Does a component already solve this intent?
2. Search Existing Variant
      └── Does the component have a variant or slot that satisfies this?
3. Search Existing Pattern
      └── Is there a documented pattern combining existing parts?
4. Search Existing Composition
      └── Can this be built cleanly by composing primitives?
5. Search Existing Token
      └── Can semantic or primitive tokens express the need?
6. Propose New Architecture / Extension
      └── Only when steps 1–5 are exhausted.
```

---

## 3. Strict Prohibitions & Hard Guardrails

1. **Zero Raw Visual Inventions:**
   - Prohibited: `radius="13px"`, `background="#123456"`, `padding="17px"`.
   - Permitted: `variant="primary"`, `size="md"`, `radius="md"`, `color="color.surface.raised"`.
2. **Zero Premature Component Implementation:**
   - Do NOT write UI component code until the component specification has been authored and approved according to the 16-point anatomy standard.
3. **No Unidirectional Layer Inversions:**
   - Primitives must never import from components. Components must never import from patterns or templates.
4. **File Length Discipline (500-Line Decomposition Threshold):**
   - 500 lines acts as a **decomposition warning threshold**, not an arbitrary truncation guillotine.
   - If a cohesive component legitimately requires ~520 lines, do not arbitrarily mutilate it into fragmented pieces.
   - However, components approaching 400+ lines must be actively evaluated for extractable sub-widgets, hooks, or utility abstractions to prevent God-classes.
5. **Universal RTL & Typographic Strategy:**
   - Never use physical left/right CSS margins or paddings. Use logical properties (`inline-start`, `inline-end`).
   - Arabic typography is first-class; primary font family is canonical **Cairo** (Google Fonts) for Arabic + Latin, and **JetBrains Mono** for code and tabular telemetry data. All components must support dynamic leading adjustments (+0.15 context-aware leading) for Arabic scripts.
6. **Mandatory Experience States & Contextual Recovery:**
   - Every relevant screen or data container must define appropriate Loading, Empty, Error, and Recovery behavior.
   - Recovery actions must be contextual to the specific failure or state (e.g. Network failure → Retry, Invalid input → Fix, Permission denied → Request access / appropriate next action, Authentication expired → Sign in, Conflict → Review/resolve, Deleted resource → Restore/navigate away, Recoverable operation → Undo).
   - Do NOT force a generic "Retry" CTA on every error.

---

## 4. Handling `[TBD — requires design decision]` Markers

Where tokens, scales, or breakpoint values are marked with `[TBD — requires design decision]`:
- The agent must preserve the marker.
- The agent must NOT guess, invent, or substitute arbitrary numeric values.
- When tasked with resolving a TBD, the agent must present options with mathematical/aesthetic justifications for human architect approval.
