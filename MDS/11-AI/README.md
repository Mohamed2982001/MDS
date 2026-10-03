# MDS Layer 11 — AI Integration & Agentic Experience Layer (Canonical Pointer)

## Architectural Role & Scope
Layer 11 governs human-in-the-loop generative interfaces, contextual prompt affordances, token-by-token streaming lifecycles, and machine-readable agent governance throughout the Master Design System (MDS).

## Core Architectural Invariants
1. **Human-in-the-Loop & Explicit Confirmation:** AI generative proposals must never auto-persist destructive changes without explicit human user review and consent.
2. **AF-001 Streaming Decoupling Standard:** Progressive token streaming visually must decouple from screen reader live regions. Live region announcements must be throttled or triggered only upon terminal token completion to prevent auditory cognitive overload.
3. **Security Triad Decoupling:** In AI interactions: $\text{User Confirmation} \ne \text{Authentication} \ne \text{Authorization}$.

## Canonical Sources of Truth
AI-native patterns, workflows, templates, and agent guidelines are codified in:

1. **AI Composite Patterns:**
   - [`MDS/05-Patterns/AI/AI-Input-Prompt.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/05-Patterns/AI/AI-Input-Prompt.md) — Multi-modal input, token meter, context attachments.
   - [`MDS/05-Patterns/AI/AI-Result-Review.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/05-Patterns/AI/AI-Result-Review.md) — Progressive streaming container with AF-001 decoupling.
2. **AI Workflows:**
   - [`MDS/06-Workflows/AI/AI-Synthesis-Review.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/06-Workflows/AI/AI-Synthesis-Review.md) — Generative flow, diff inspection, non-auto-persist.
3. **AI Page Templates:**
   - [`MDS/07-Templates/AI/AI-Workspace.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/07-Templates/AI/AI-Workspace.md) — Dual-pane conversational and canvas workspace.
4. **AI Agent Rules & Selection Engines:**
   - [`MDS/AGENT/MDS_AGENT_RULES.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/AGENT/MDS_AGENT_RULES.md)
   - [`MDS/AGENT/DESIGN_SYSTEM_SELECTION_ENGINE.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/AGENT/DESIGN_SYSTEM_SELECTION_ENGINE.md)
   - [`MDS/AGENT/DSSE-Mathematical-Decision-Proposal.md` (DSSE-ADR-001 Decision Record)](file:///d:/Work/Dev/Master%20Design%20System/MDS/AGENT/DSSE-Mathematical-Decision-Proposal.md)
5. **Accessibility Architectural Findings:**
   - [`MDS/09-Accessibility/Accessibility-Findings.md` (Finding AF-001)](file:///d:/Work/Dev/Master%20Design%20System/MDS/09-Accessibility/Accessibility-Findings.md)
