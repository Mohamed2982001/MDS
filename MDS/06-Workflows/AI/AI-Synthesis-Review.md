# MDS Workflow: AI Synthesis & Review (MDS-WF-005)

## 1. Workflow Identification & Metadata
- **Workflow Name:** `AI-Synthesis-Review`
- **ID:** `MDS-WF-005`
- **Layer:** `06-Workflows`
- **Family:** `AI`
- **Verification Status:** `Manually Verified` (Testbed Sandbox) / `Automated Token/Style Integrity Check`

---

## 2. Purpose & Summary
The `AI-Synthesis-Review` workflow governs generative AI interactions from prompt formulation and parameter configuration through progressive token streaming to human-in-the-loop inspection, source citation verification, and explicit persistence sign-off. It enforces strict human agency over probabilistic model outputs and provides full control over streaming latency and cancellation.

---

## 3. User Intent
The user intends to formulate an instruction, prompt, or synthesis request for an AI model, observe the generation, review the output for factual and contextual accuracy, and decide whether to accept, edit, regenerate, or discard the result.

---

## 4. Trigger
- User enters a prompt in the `AI-Input-Prompt` pattern and clicks `"Generate"` (or presses `Cmd/Ctrl + Enter`).

---

## 5. Preconditions
1. AI service connection is authenticated and active.
2. The user has quota / permission to invoke the AI model.

---

## 6. Actors & Roles
- **Primary Actor:** Human Operator / Reviewer.
- **System Actor:** Prompt Controller, Streaming SSE/WebSocket Client, LLM Service, and Citation Parser.

---

## 7. Entry State
- **State Identifier:** `IDLE_PROMPT_READY`
- Prompt textarea is empty or populated with an editable starter template.
- Review panel is unmounted or in resting empty state.
- Generate button is enabled when prompt text exceeds minimum length.

---

## 8. Sequential Steps (Happy Path)

```text
[1. FORMULATE] ──► [2. STREAMING CADENCE] ──► [3. STREAM COMPLETE] ──► [4. INSPECT/CITATIONS] ──► [5. ACCEPT & COMMIT]
  Enter Prompt       Tokens Stream in Real-      Review Container       Human Checks Sources       Click "Accept";
  & Click Generate   Time; "Stop" Button Active  Locks Draft Output     & Edits Text               Persist to System
```

1. **Step 1 — Prompt Formulation:** User inputs prompt and optional parameters (e.g., tone, format) in `AI-Input-Prompt`.
2. **Step 2 — Dispatch & Streaming:** User clicks "Generate". State machine enters `STREAMING`. An active pulsing cursor displays real-time token delivery. A prominent `"Stop Generating"` button becomes active.
3. **Step 3 — Generation Completion:** Model emits stream-end token. State machine transitions to `REVIEWING`. The output is locked into an editable draft container within the `AI-Result-Review` pattern.
4. **Step 4 — Human Inspection & Citation Audit:** User reads output, inspects referenced sources/citations via interactive badge popovers, and makes optional inline edits.
5. **Step 5 — Acceptance & Persistence:** User clicks `"Accept & Apply"`. State machine transitions to `SUCCESS_RESOLVED`. Synthesized content is committed to the application state; a success notification is announced.

---

## 9. Branches & Forks

```text
                    ┌──► [Branch A: User Aborts Stream] ──────► Halt Stream, Keep Partial Draft for Review
                    │
[Dispatch Prompt] ──┼──► [Branch B: Hallucination / Unsatisfied] ─► Click "Regenerate" with Refined Prompt
                    │
                    ├──► [Branch C: Model Rate Limit / 429] ──► Show "Model Busy" Banner with Backoff Retry
                    │
                    └──► [Branch D: User Discards Output] ────► Click "Discard"; Revert to Clean Entry
```

- **Branch A (Stream Abort):** User clicks "Stop Generating". Streaming halts immediately. The partial draft is preserved in `REVIEWING` state so work is not lost.
- **Branch B (Regeneration):** User clicks "Regenerate". System prompts for optional direction tweaks, archives the previous generation as a version, and starts a fresh stream.
- **Branch C (Rate Limit / Timeout):** Stream fails; an inline warning banner informs user of temporary capacity issues and offers a `"Retry in 10s"` button without losing prompt text.
- **Branch D (User Rejection):** User clicks "Discard". Generated content is purged; focus returns to the prompt input.

---

## 10. Decision Points
- **Stop Stream:** Deciding to halt mid-generation if the model deviates from user intent.
- **Acceptance Decision:** Deciding whether the output is sufficiently accurate and aligned to be committed.
- **Edit vs. Regenerate:** Deciding whether to manually edit the draft or request a new generation.

---

## 11. Patterns Used
- `AI-Input-Prompt` (`MDS/05-Patterns/AI/AI-Input-Prompt.md`): Prompt formulation, model selectors, and generation trigger.
- `AI-Result-Review` (`MDS/05-Patterns/AI/AI-Result-Review.md`): Structured review panel with streaming output container, citation chips, and action toolbar.

---

## 12. Components Used
- `Button` (Generate, Stop Generating, Accept, Regenerate, Discard)
- `Input` (Prompt textarea, parameter inputs)
- `Badge` (AI badge, streaming status, citation reference pills)
- `Dialog` (Discard confirmation if generated text has been heavily edited)

---

## 13. Experience States
- **Idle State:** Prompt input resting; review area empty.
- **Loading / Streaming State:** Active token stream; typing cadence indicator; `aria-busy="true"`.
- **Review State:** Stable output displayed with citation badges and action toolbar.
- **Error State:** Model failure alert with retry CTA; prompt text strictly preserved.
- **Success State:** Accepted text persisted; toast notification confirms integration.

---

## 14. Success Outcome
- High-quality synthesized content inspected, verified, and adopted by a human operator.
- Full auditability preserved with source citations.
- System state updated safely.

---

## 15. Failure Outcomes
- **Generation Hallucination:** Caught and rejected during human inspection step.
- **Network / API Drop:** Stream interrupted; partial text preserved with recovery retry button.

---

## 16. Recovery Paths
- **Inline Editing:** Fix minor factual errors directly in the review container.
- **Prompt Refinement:** Adjust prompt wording and re-run generation.
- **History Rollback:** Cycle between Generation V1 and Generation V2.

---

## 17. Cancellation & Exit Affordances
- **Stop Generating Button:** Halts streaming immediately.
- **Discard Button:** Rejects generation and clears review view.
- **Prompt Reset:** Clears prompt input back to placeholder state.

---

## 18. Data & State Requirements
```typescript
interface AISynthesisReviewState {
  prompt: string;
  parameters: { model: string; temperature?: number };
  status: 'IDLE' | 'STREAMING' | 'REVIEWING' | 'ACCEPTED' | 'ERROR';
  streamedText: string;
  citations: Array<{ id: string; source: string; url?: string }>;
  versionHistory: string[];
  activeVersionIndex: number;
  error: string | null;
}
```

---

## 19. Accessibility Contracts
- **Live Stream Announcements:** The streaming container uses `aria-live="polite"` with updates throttled (debounced 1000ms) to avoid overwhelming screen readers.
- **Status Change:** Generation completion is announced as *"Generation complete. Review your results."*
- **Citation Inspection:** Citation badge buttons are keyboard operable (`Enter` opens source popover, `Escape` closes).
- **WCAG Standard:** Implemented accessibility behaviors were validated against selected WCAG success criteria where applicable. Comprehensive cross-platform assistive technology testing remains deferred to Phase 8.

---

## 20. Responsive Behavior
- **Mobile (320px – 767px):** Prompt area and Review panel stack vertically. Action buttons (Accept, Regenerate, Discard) render in a sticky bottom cluster. Interactive controls preserve the MDS minimum interaction target where applicable.
- **Tablet & Desktop (768px – 1440px):** Two-pane layout (Prompt on left, Review on right) or sequential card stack with comfortable inline actions.
- **Overflow:** The current sandbox was checked at the defined MDS responsive modes and showed no observed horizontal overflow for the included Workflow examples.

---

## 21. RTL Behavior
- Stream text renders in natural reading direction (`dir="rtl"` for Arabic, `dir="ltr"` for English).
- Action buttons align logically (`start` to `end`).
- RTL structural and logical-property checks passed in the current sandbox. Broader language/content localization testing remains outside this closure pass.

---

## 22. Density Modes
- **Default Mode:** Prompt field min-height 120px; review container padding 24px.
- **Compact Mode:** Prompt field min-height 80px; review container padding 12px.

---

## 23. Motion & Transitions
- Streaming cursor pulse: `var(--mds-motion-duration-moderate, 250ms)` infinite pulse.
- Review action bar fade-in: `motion.duration.fast` (150ms).
- Reduced Motion: Cursor pulse replaced with static indicator.

---

## 24. AI Guardrails & Human Agency
- **Mandatory Human Sign-Off:** The system must never auto-commit an AI result without the user clicking "Accept".
- **Traceability:** Synthesized claims must link to source citations whenever factual extraction is performed.
- **Stop Guarantee:** The "Stop Generating" button must abort network streams within 200ms.

---

## 25. Validation Criteria
- [x] Human must explicitly accept output before persistence.
- [x] "Stop Generating" control terminates active stream immediately.
- [x] Streamed text remains editable by the user before committing.
- [x] Zero raw hex colors; 100% token-driven styling.

---

## 26. Anti-Patterns & Misuse
- ❌ **The Autonomous Persister:** Directly writing AI text to a production database with zero human review.
- ❌ **The Unstoppable Stream:** Generating 2,000 words with no way for the user to halt execution.
- ❌ **The Opaque Generator:** Presenting factual assertions without clickable source citations.

---

## 27. Governance & Lifecycle
- **Version:** `1.0.0`
- **Scope Invariant:** 0 new components, 0 new tokens, 0 deferred enterprise systems.
