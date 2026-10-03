# MDS Layer 08 — Experience States (Canonical Pointer)

## Architectural Role & Scope
Layer 08 governs the systemic state lifecycle, error boundaries, empty state affordances, and contextual recovery patterns across the Master Design System (MDS). In MDS, experience states are cross-cutting invariants that apply to every screen, container, and interactive component.

## Core Architectural Invariants
1. **Mandatory Universal States:** Every relevant screen or data container must define explicit `Loading`, `Empty`, `Partial`, `Success`, and `Error` states.
2. **Contextual Recovery Pairing:** Recovery actions must semantically match the failure root cause (e.g. Network $\to$ Retry, Validation $\to$ Fix, Auth Expiry $\to$ Sign in, Conflict $\to$ Resolve, Deletion $\to$ Restore/Undo). Generic "Retry" CTAs on non-network errors are prohibited.
3. **Non-Color-Only Communication (WCAG 1.4.1):** State transitions and error indicators must combine iconography, explicit text, or structural styling alongside color tokens.

## Canonical Sources of Truth
To prevent fractured definitions, Layer 08 specifications are codified in the following authoritative files:

1. **Systemic Experience State Agent Rules:**
   - [`.agents/rules/02_experience_states.md`](file:///d:/Work/Dev/Master%20Design%20System/.agents/rules/02_experience_states.md) — Comprehensive rules for Data, Access, Resource, Process, and Resilience states.
2. **Deterministic FSM State Transitions:**
   - [`MDS/06-Workflows/Workflow-State-Model.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/06-Workflows/Workflow-State-Model.md) — Universal 11-State Finite State Machine topology and operational state lifecycles.
3. **Feedback Patterns & Contextual Guidance:**
   - [`MDS/05-Patterns/Feedback/Empty-State.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/05-Patterns/Feedback/Empty-State.md)
   - [`MDS/05-Patterns/Feedback/Confirmation-Dialog.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/05-Patterns/Feedback/Confirmation-Dialog.md)
   - [`MDS/04-Components/Feedback/Alert.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/04-Components/Feedback/Alert.md)
4. **Master Specification Summary:**
   - [`MDS/MDS_MASTER_SPECIFICATION.md` (Section 13)](file:///d:/Work/Dev/Master%20Design%20System/MDS/MDS_MASTER_SPECIFICATION.md#13-experience-states-invariants-layer-08)
