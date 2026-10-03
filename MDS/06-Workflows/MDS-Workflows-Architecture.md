# Master Design System (MDS) — Workflows Architecture (Layer 06)

## 1. Executive Summary & Layer Purpose

In the Master Design System (MDS), **Layer 06: Workflows** defines the formal architectural contracts and behavioral models governing how a user progresses through a multi-step task, decision sequence, or systemic journey from initial intent to final outcome.

While lower layers govern aesthetics, primitives, individual controls, and localized UI compositions, **Workflows orchestrate end-to-end human and system behaviors over time**. A workflow is not a single visual component or a static page layout; it is a platform-agnostic state machine that synchronizes user intent, sequential tasks, conditional branches, decision points, feedback loops, error interception, and recovery affordances.

---

## 2. The Authoritative MDS Architectural Hierarchy

MDS enforces a strict, unidirectional, non-circular composition hierarchy. Each layer builds upon the layers directly beneath it and may never reach upward or bypass intermediate layers.

```text
┌─────────────────────────────────────────────────────────────┐
│ 01. Foundations       Typography, Color, Space, Elevation   │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 02. Tokens            Design tokens (188 canonical tokens)   │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 03. Primitives        Container, Stack, Grid, FocusRing     │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 04. Components        Button, Input, Badge, Dialog (19 Core)│
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 05. Patterns          FormSection, PageHeader, EmptyState   │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 06. Workflows (THIS)  End-to-end task flows & state machines │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 07. Templates         Full-page layouts & composite views   │
└─────────────────────────────────────────────────────────────┘
```

### Layer Hierarchy Rules:
1. **Downstream Consumption Only:** Workflows consume Patterns (Layer 05), Components (Layer 04), Primitives (Layer 03), and Tokens (Layer 02).
2. **Zero Upstream Dependency:** Workflows do not know about or depend on Templates (Layer 07).
3. **No Direct Raw Styling:** Workflows do not declare new raw CSS values, hex codes, or arbitrary dimensions. All styling resolves strictly through MDS tokens.
4. **No Direct Backend Coupling:** Workflows govern client UX contracts and interaction state machines. They define payload expectations and state transitions, never database queries, network protocols, or server-side implementations.

---

## 3. The Ontological Boundary: Pattern vs. Workflow

A fundamental failure mode in design system architecture is conflating Patterns with Workflows. MDS maintains a strict boundary:

| Dimension | Layer 05: Pattern | Layer 06: Workflow |
| :--- | :--- | :--- |
| **Primary Question** | *"How should this recurring UX structure be composed?"* | *"How does the user progress through a task from intent to outcome?"* |
| **Nature** | Structural & Spatial Composition | Behavioral Progression & State Machine |
| **Temporal Dimension** | Static or Locally Interactive | Temporal, Sequential, Multi-step |
| **Scope** | Localized UI fragment (e.g., Form Section, Header, Dialog) | Cross-surface journey (e.g., Submission, Recovery, Destruction) |
| **Lifecycle** | Mounted / Rendered within a view | Initialized $\to$ In-Progress $\to$ Resolved / Aborted |
| **Branching** | Static variants | Dynamic conditional forks & decision trees |
| **Recovery** | Local validation state | Cross-step error interception & rollback paths |
| **Example** | `Confirmation-Dialog` | `Destructive-Action Workflow` |
| **Example** | `Form-Section` | `Form-Submission Workflow` |
| **Example** | `Empty-State` | `Search-Discovery Workflow` |

---

## 4. Hard Scope Boundaries & Invariants

To guarantee architectural stability and prevent system bloat, Phase 7 operates under strict, non-negotiable invariants:

1. **Zero New Foundations:** 0 additions or changes to typography, color ramps, elevations, or spacing grids.
2. **Zero New Primitives:** 0 additions to Layer 03.
3. **Zero New Core Components:** 0 additions to Layer 04. The 19 Core Components remain unchanged.
4. **Zero New Patterns:** 0 additions to Layer 05. The 8 canonical patterns remain stable.
5. **Zero New Tokens:** Exactly 0 new design tokens. The total token count remains invariant at **188 total tokens** (including 47 component tokens).
6. **Zero Leaks of Deferred Enterprise Systems:** The 9 complex enterprise systems remain strictly **DEFERRED**:
   - `DataGrid`
   - `RichTextEditor`
   - `Calendar`
   - `DateRangePicker`
   - `CommandSystem`
   - `Tree`
   - `Combobox`
   - `VirtualizedList`
   - `FileUploadManager`
7. **Security Triad Distinction:** Workflows strictly distinguish:
   $$\text{User Confirmation} \ne \text{Authentication} \ne \text{Authorization}$$
   - *Confirmation:* Verifying explicit human intent (Layer 06 UX concern).
   - *Authentication:* Verifying subject identity (external security provider concern).
   - *Authorization:* Verifying permissions and capabilities (external policy enforcement concern).
8. **Calibrated Verification Taxonomy:**
   - Documentation of implementation status is strictly demarcated across: `Specified`, `Implemented`, `Manually Verified`, and `Automated Token/Style Integrity Check`.

---

## 5. The Mandatory 27-Point Workflow Anatomy Standard

Every canonical workflow in MDS must be documented against the standardized **27-Point Workflow Anatomy**. No workflow specification is valid without addressing all 27 dimensions:

```text
┌──────────────────────────────────────────────────────────┐
│              27-POINT WORKFLOW ANATOMY                   │
├──────────────────────────┬───────────────────────────────┤
│ 01. Workflow Name        │ 15. Failure Outcomes          │
│ 02. Purpose & Summary    │ 16. Recovery Paths            │
│ 03. User Intent          │ 17. Cancellation & Exit       │
│ 04. Trigger              │ 18. Data & State Requirements │
│ 05. Preconditions        │ 19. Accessibility Contracts   │
│ 06. Actors & Roles       │ 20. Responsive Behavior       │
│ 07. Entry State          │ 21. RTL Behavior              │
│ 08. Sequential Steps     │ 22. Density Modes             │
│ 09. Branches & Forks     │ 23. Motion & Transitions      │
│ 10. Decision Points      │ 24. AI Guardrails & Cadence   │
│ 11. Patterns Used        │ 25. Validation Criteria       │
│ 12. Components Used      │ 26. Anti-Patterns & Misuse    │
│ 13. Experience States    │ 27. Governance & Lifecycle    │
│ 14. Success Outcome      │                               │
└──────────────────────────┴───────────────────────────────┘
```

### Detailed Breakdown of the 27 Dimensions:
1. **Workflow Name:** Authoritative identifier (`MDS-WF-XXX`).
2. **Purpose & Summary:** High-level architectural objective and business outcome.
3. **User Intent:** The primary goal the human actor is attempting to achieve.
4. **Trigger:** Explicit user action or system event that initiates the workflow.
5. **Preconditions:** System or session conditions that must evaluate to `true` before entry.
6. **Actors & Roles:** Intended human operators and their contextual permissions.
7. **Entry State:** The clean, initial state of the workflow upon activation.
8. **Sequential Steps:** Linear progression of tasks, inputs, and feedback states.
9. **Branches & Forks:** Conditional divergent paths based on runtime data or user choices.
10. **Decision Points:** Explicit moments requiring human evaluation or critical branching.
11. **Patterns Used:** Formal inventory of Layer 05 patterns orchestrated.
12. **Components Used:** Formal inventory of Layer 04 components utilized.
13. **Experience States:** Concrete mapping to MDS Experience States (`Idle`, `Loading`, `Empty`, `Error`, `Success`).
14. **Success Outcome:** Definitive terminal state signifying successful task completion.
15. **Failure Outcomes:** Catalog of terminal or non-terminal failure states.
16. **Recovery Paths:** Actionable avenues allowing the user to remediate failure without data loss.
17. **Cancellation & Exit:** Safe, low-consequence escape hatches and state rollback.
18. **Data & State Requirements:** Client-side state schema and persistence contracts.
19. **Accessibility Contracts:** Focus order, screen reader announcements, ARIA live regions, and keyboard traps.
20. **Responsive Behavior:** Viewport adaptation across Mobile (320px), Tablet (768px), Desktop (1024px), and Wide (1440px).
21. **RTL Behavior:** Logical reading order, bidirectional navigation, and spatial symmetry.
22. **Density Modes:** Rendering adaptations for `default` and `compact` density themes.
23. **Motion & Transitions:** Duration, easing, and reduced-motion fallbacks for state changes.
24. **AI Guardrails & Cadence:** Latency indicators, streaming updates, citation inspection, and confidence boundaries.
25. **Validation Criteria:** Concrete behavioral criteria for pass/fail audits.
26. **Anti-Patterns & Misuse:** Common architectural and UX errors to avoid.
27. **Governance & Lifecycle:** Deprecation policy, breaking change thresholds, and review gates.

---

## 6. The Canonical Phase 7 Workflow Portfolio

Phase 7 establishes six canonical workflows covering foundational interaction paradigms:

```text
MDS/06-Workflows/
├── Forms/
│   └── Form-Submission.md          # Input → Validation → Processing → Success/Recovery
├── Search/
│   └── Search-Discovery.md         # Query → Filter → Results → Empty/Refine
├── Actions/
│   └── Destructive-Action.md       # Trigger → Consequence → High-Friction Confirm → Execution
├── Settings/
│   └── Settings-Update.md          # Section Nav → Mutation → Inline/Batch Persist → Feedback
├── AI/
│   └── AI-Synthesis-Review.md      # Prompt → Stream → Inspect → Feedback/Citation → Accept
└── Recovery/
    └── Error-Recovery.md           # Intercept → Diagnose → Contextual Remediation → Resolution
```

---

## 7. State Machine Execution Philosophy

All MDS Workflows adhere to a deterministic, finite state machine (FSM) execution model:

```text
[IDLE / UNINITIALIZED]
         │
         ▼ (Trigger)
    [ACTIVE STEP] ◄────────────────────────┐
         │                                 │
         ├─── (Invalid / Transient Error) ─┤ (Inline Fix)
         │                                 │
         ▼ (Proceed)                       │
   [PROCESSING] ───────────────────────────┤ (Retry)
         │                                 │
         ├─── (Fatal Error) ───────────────┘ (Fallback Recovery)
         │
         ▼ (Resolution)
     [SUCCESS] ───► [TERMINAL EXIT]
```

### Key FSM Principles:
- **No Orphan States:** Every state has at least one valid transition to a subsequent state or a safe cancellation exit.
- **State Preservation on Interruption:** User inputs must never be cleared upon failure or cancellation dialogs.
- **Predictable Focus Management:** Focus must move deliberately to new interaction contexts and return safely upon dismissal.
