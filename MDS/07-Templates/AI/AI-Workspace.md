# MDS Template: AI-Workspace (`MDS-TMP-006`)

**Document Layer:** 07-Templates / AI  
**Status:** APPROVED (Phase 8.1.3 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-17  

---

## 1. Template ID
`MDS-TMP-006`

## 2. Name
Generative AI Workspace & Studio Template

## 3. Intent
To provide a dedicated, high-performance multi-pane environment for conversational, generative, and assistive AI workflows, balancing prompt composition, real-time streaming canvas, and side-by-side human review.

## 4. Problem Solved
Eliminates congested conversational UIs that squeeze prompts, generated artifacts, and verification citations into a narrow chatbot column. Establishes an expansive studio layout designed for serious generative tasks (code synthesis, research analysis, document generation) with strict human-in-the-loop oversight.

## 5. When to Use
- For AI-assisted research studios, generative code tools, automated report builders, and conversational copilot workspaces.
- When an AI interaction produces multi-paragraph text, code snippets, structured tables, or generative artifacts requiring side-by-side review.
- When source citations, confidence scores, and feedback mechanisms are required.

## 6. When Not to Use
- For standard CRUD data entry forms: Use `Form-Edit` (`MDS-TMP-004`) instead.
- For single-entity property views: Use `Detail-Entity` (`MDS-TMP-003`) instead.
- For traditional dashboards without interactive AI generation: Use `Dashboard-Overview` (`MDS-TMP-001`) instead.

## 7. Page Regions
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Region 1: AI Studio Header (Model Selector, Token Counter, Clear Session)   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 2: Multi-Pane Studio Workspace (3-Column Layout)                     │
│ ┌─────────────────────────┐ ┌─────────────────────────┐ ┌─────────────────┐ │
│ │ Prompt & History Panel  │ │ Generative Canvas       │ │ Citations &     │ │
│ │ ├── Prompt Input Box    │ │ ├── Active Generation   │ │ Review Drawer   │ │
│ │ ├── Suggestion Chips    │ │ ├── Streaming Cursor    │ │ ├── Sources     │ │
│ │ └── Session Threads     │ │ └── Stop / Regenerate   │ │ └── Thumbs/Diff │ │
│ └─────────────────────────┘ └─────────────────────────┘ └─────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 3: Human Verification Bar (Reject / Edit / Accept & Persist)         │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 8. Region Hierarchy
`AI Studio Header` $\to$ `Multi-Pane Studio Workspace` (Prompt Panel + Generative Canvas + Review Drawer) $\to$ `Human Verification Bar`.

## 9. Pattern Composition
- **`Page-Header` (`MDS/05-Patterns/Navigation/Page-Header.md`):** Model selection dropdown, active token budget indicator, session clear action.
- **`AI-Input-Prompt` (`MDS/05-Patterns/AI/AI-Input-Prompt.md`):** Multi-line auto-expanding textarea, suggestion pills, model parameters button, submit trigger.
- **`AI-Result-Review` (`MDS/05-Patterns/AI/AI-Result-Review.md`):** Generative output presentation, confidence badge, source citations list, copy action, feedback thumbs.
- **`Empty-State` (`MDS/05-Patterns/Feedback/Empty-State.md`):** Initial zero-prompt canvas with starter prompt templates.
- **`Confirmation-Dialog` (`MDS/05-Patterns/Feedback/Confirmation-Dialog.md`):** For session reset or discarding unpersisted generative artifacts.

## 10. Workflow Slots
- **`AI-Synthesis-Review` (`MDS/06-Workflows/AI/AI-Synthesis-Review.md`):** Manages prompt dispatch, real-time streaming, stop generation guarantee, human review, and explicit persistence.
- **`Error-Recovery` (`MDS/06-Workflows/Recovery/Error-Recovery.md`):** Intercepts API rate limits or model timeouts with non-destructive prompt recovery.

## 11. Component Dependencies
- `Button`, `IconButton` (Actions)
- `Textarea`, `Select`, `Badge` (Inputs & Data Display)
- `Card`, `Skeleton`, `Alert`, `Spinner` (Feedback)
- `Surface`, `Stack`, `Inline`, `Grid`, `Container` (Primitives)

## 12. Content Slots
- `slot="model-parameters"`: Model picker (e.g. "Gemini Pro", "Claude 3.5 Sonnet") and temperature/mode controls.
- `slot="prompt-panel"`: houses `AI-Input-Prompt` and history list.
- `slot="canvas-workspace"`: houses the live generated document, code editor, or artifact preview.
- `slot="citations-review"`: houses source citations, confidence indicators, and quality feedback.
- `slot="human-verification"`: "Accept & Apply", "Request Revisions", "Discard".

## 13. Required vs Optional Regions
- **Required:** AI Studio Header, Prompt Input Region, Generative Canvas, Human Verification Bar.
- **Optional:** Citations & Review Drawer (collapses into toggle icon on narrow viewports).

## 14. Responsive Composition
- **Compact (< 768px):** 3-pane layout recomposes into a focused single-view layout: Generative Canvas fills the viewport; Prompt Input docks into a persistent bottom bar; Citations and Review metadata move into a swipeable bottom sheet.
- **Standard (768px – 1151px):** 2-pane layout (Prompt Input on side or bottom, Generative Canvas in center, Citations toggleable via slide-over panel).
- **Wide (1152px – 1439px):** Canonical 1152px max-width; full 3-pane studio layout (25% Prompt, 50% Canvas, 25% Citations).
- **Full ($\ge$ 1440px):** 1440px wide container (`container.xl`); generous side panels and spacious central generative canvas.

## 15. Mobile Composition
- Prompt bar stays docked at the bottom with keyboard-safe viewports.
- Stop Generation button is large and prominent during active streaming.
- Generated code or rich cards are horizontally swipeable within their container.

## 16. RTL Behavior
- Studio prompt panel aligns to inline-start (`right` in RTL).
- Citations panel aligns to inline-end (`left` in RTL).
- Generated code blocks remain strictly LTR (`dir="ltr"`) with monospace Cairo / JetBrains Mono.
- Zero `row-reverse` hacks used.

## 17. Accessibility Structure
- `<main>` landmark encompasses the Generative Canvas.
- AI streaming live region speech decoupling (Finding `AF-001`): rapid token stream is NOT announced word-by-word to avoid screen reader speech buffer flooding. A polite live region announces generation start and completion.
- Stop generation button features explicit `aria-label="Stop AI generation"`.

## 18. Experience States
- **`Idle / Empty`:** Canvas displays `Empty-State` with sample prompt cards.
- **`Composing Prompt`:** User typing; suggestion pills active.
- **`Generating / Streaming`:** Visual cursor pulse; Stop button active; canvas actively rendering tokens.
- **`Reviewing`:** Generation complete; human verification bar active; citations inspectable.
- **`Error / Rate Limited`:** Alert card: "Model capacity reached — Click to retry"; prompt preserved in memory.

## 19. Loading Strategy
Initial load renders an empty studio skeleton; active generation uses a pulsing cursor line and subtle shimmer; avoids blank screens.

## 20. Error Strategy
Model timeout or content policy flag displays an inline warning banner; the user's prompt is NEVER cleared from the textarea.

## 21. Empty Strategy
Embeds `Empty-State` pattern with generative icon, "Start your generation", and 3 clickable prompt starter cards ("Analyze dataset", "Draft architecture", "Generate code").

## 22. Recovery Strategy
Failed generations offer a one-click "Regenerate" button; previous generation attempts are archived in the session history rail.

## 23. Density Behavior
- **Comfortable:** Standard line-height (1.6) in canvas, 16px prompt padding.
- **Compact:** High-density code view with 13px JetBrains Mono typography and 12px panel padding.

## 24. Theme/Mode Behavior
- **Light:** Studio Canvas `#F8FAFC`, Editor `#FFFFFF`, Subtle border `#E2E8F0`.
- **Dark:** Studio Canvas `#020617`, Editor `#0F172A`, Border `#1E293B`.
- **High Contrast:** Clear 2px boundary separating prompt panel from canvas.

## 25. AI Integration
The foundational purpose of this template. Built specifically to house the `AI-Synthesis-Review` workflow and enforce the MDS principle: **AI outputs never auto-persist without explicit human confirmation**.

## 26. Navigation Context
Header displays active model badge, session title, and session history switcher.

## 27. Focus Management
When generation completes, focus moves smoothly to the Human Verification Bar or first citation link; Escape key dismisses the citation drawer.

## 28. Motion Behavior
Streaming text renders with subtle 50ms token fade; cursor blinks with 800ms ease; collapses to 0ms when reduced motion is requested.

## 29. Token Dependencies
`container.lg`, `container.xl`, `space.3`, `space.4`, `space.6`, `color.surface.*`, `color.brand.*`.

## 30. Anti-Patterns
- ❌ Do NOT auto-save AI outputs without explicit user approval.
- ❌ Do NOT flood screen readers with every token in the live stream (violates AF-001).
- ❌ Do NOT clear the user's prompt text if generation encounters an error.

## 31. Validation Requirements
Verified by `run_tests.py`, HTML showcase testbed, and 100% token usage.

## 32. Selection Criteria
Select when user intent involves conversational, generative, or assistive AI interaction requiring side-by-side prompt composition, canvas artifact rendering, and citation review.
