# MDS Pattern: AI-Input-Prompt

**Document Layer:** 05-Patterns / AI  
**Status:** STABLE (Phase 6 Implementation)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-16  

---

## 1. Purpose
The **AI-Input-Prompt** pattern provides a specialized, intelligent input console for interacting with generative AI models. It integrates a multi-line expanding text input, model/mode configuration chips, prompt suggestion pills, token count indicators, and a distinct prompt submission button.

---

## 2. User Intent
The user intends to instruct, prompt, or query an artificial intelligence model with structured or freeform natural language text, select appropriate generation parameters, and submit the prompt.

---

## 3. Problem Solved
Eliminates rigid, single-line text inputs that frustrate users composing detailed AI instructions. Prevents accidental submission while typing multi-paragraph prompts and exposes key model constraints (token limits, generation tone) cleanly.

---

## 4. When to Use
- AI chat assistants, generative copilot consoles, and code/text synthesis interfaces.
- Prompt engineering sandboxes and natural language search bars.
- When users need to provide contextual instructions with attachment pills or preset suggestions.

---

## 5. When Not to Use
- For standard single-line form inputs (e.g. Email, Name): Use `Input`.
- For standard multi-line comments or descriptions without AI integration: Use `Textarea`.
- For full-page chat history logs: Combine with `AI-Result-Review`.

---

## 6. Composition Architecture

```text
┌───────────────────────────────────────────────────────────────────────────┐
│ AI-Input-Prompt Container (Surface.raised, border, radius.lg, shadow)     │
│                                                                           │
│  Suggestion Chips Strip (Cluster gap="xs", padding="space.3")             │
│   ├── Suggestion: Badge(variant="neutral", "💡 Summarize release notes")  │
│   ├── Suggestion: Badge(variant="neutral", "⚡ Refactor authentication")   │
│   └── Suggestion: Badge(variant="neutral", "📝 Generate test suite")      │
│                                                                           │
│  Divider (border.subtle)                                                  │
│                                                                           │
│  Prompt Entry Area (padding="space.3")                                    │
│   └── Textarea (placeholder="Ask Antigravity anything...", border="none", │
│                 min-height: 72px, resize: vertical, softWrap: true)       │
│                                                                           │
│  Prompt Console Toolbar (Inline justify="space-between" align="center")   │
│   ├── Mode & Token Cluster (Inline gap="xs" align="center")               │
│   │    ├── Mode Selector: Button(variant="ghost", size="sm", "⚙️ Pro 2.5") │
│   │    └── Token Counter: Caption("142 / 4,000 tokens", color="secondary")│
│   │                                                                       │
│   └── Action Group (Inline gap="xs" align="center")                       │
│        ├── Stop Action (When streaming): Button(variant="secondary", "⏹") │
│        └── Submit Action: Button(variant="primary", size="sm", "Generate")│
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Required Components
- `Textarea` (Layer 04 Input Component — multi-line text input with vertical resizing)
- `Button` (Layer 04 Actions Component — primary generation submit action)
- `Card` / `Surface` (Layer 03/04 Primitives — elevated console container)
- `Inline` (Layer 03 Layout Primitive)
- `Stack` (Layer 03 Layout Primitive)
- `Caption` / `Text` (Layer 03 Typography Primitives)

---

## 8. Optional Components
- `Badge` (Layer 04 Data Display Component — for clickable suggestion chips)
- `IconButton` (Layer 04 Actions Component — attachment clip or microphone toggle)
- `Spinner` (Layer 04 Feedback Component — inside submit button during generation)

---

## 9. Information Hierarchy
1. **Primary Canvas:** Expansive multi-line textarea inviting user input.
2. **Context Accelerators:** Top suggestion chips showing viable prompt templates.
3. **Control Metadata:** Token usage count and active model mode in footer.
4. **Execution Point:** Primary submit button anchored at bottom-trailing corner.

---

## 10. Interaction Model
- `Enter` with `Shift` inserts a newline.
- `Enter` alone (or `Cmd+Enter` / `Ctrl+Enter`) submits the prompt.
- Clicking a suggestion chip populates the prompt textarea immediately.
- When generating, the Submit button shifts to a `Stop Generating` action.

---

## 11. Experience States
- **Resting:** Suggestion chips visible; textarea shows placeholder; submit button disabled if empty.
- **Typing:** Submit button becomes active (`variant="primary"`); token counter updates in real time.
- **Generating / Streaming:** Submit button transforms into Stop button (`variant="secondary"`); textarea is locked or disabled.
- **Token Limit Warning:** When tokens reach 90% of max, token counter turns to `color.feedback.warning`.
- **Error State:** If API generation fails, displays an inline `Alert(danger)` banner above the toolbar.

---

## 12. Responsive Behavior
- **Compact (<640px):**
  - Suggestion chips scroll horizontally or wrap tightly (`Cluster gap="xs"`).
  - Mode selector and token counter collapse or hide secondary labels.
  - Submit button expands or remains sticky at bottom.
- **Standard & Wide (>640px):**
  - Full toolbar visible with explicit model label and token count.

---

## 13. Accessibility (a11y)
> *Standards Scope:* Implemented accessibility behaviors were validated against selected WCAG success criteria where applicable. Comprehensive cross-platform assistive technology testing remains deferred to Phase 8.
- Textarea has `aria-label="AI prompt input"`.
- Suggestion chips have `role="button"` and `tabindex="0"`.
- Token count announcements: When token threshold reaches warning, updates are announced politely via a `LiveRegion`.
- Interactive buttons and suggestion chips preserve $\ge 44 \times 44\text{px}$ touch hit-boxes where applicable via `PressTarget`. Static counter text is exempt.

---

## 14. RTL & Logical Progression
- Textarea naturally supports bi-directional and RTL Arabic prompt composition (`dir="auto"` or `dir="rtl"`).
- Mode selector aligns to `inline-start` (right in RTL), submit button aligns to `inline-end` (left in RTL).
- Zero `row-reverse` is permitted.

---

## 15. Density Behavior
- **Comfortable:** Container padding `space.4` (16px), min-height `88px`.
- **Compact:** Container padding `space.3` (12px), min-height `72px`.
- Density does not compress touch targets below $\ge 44 \times 44\text{px}$.

---

## 16. Motion & Animation
- Expansion transition uses 150ms (`var(--mds-motion-fast)`).
- Collapses to 0s under `prefers-reduced-motion: reduce`.

---

## 17. Token Usage
- Surface: `color.surface.raised`
- Border: `color.border.default`
- Border Focus: `color.brand.600`
- Shadow: `elevation.level2`
- Radius: `radius.lg`

---

## 18. Contextual Variants
- **Floating Console:** Fixed at the bottom of the chat viewport.
- **Embedded Block:** Inline within a notebook, document editor, or configuration panel.

---

## 19. Composition Rules
- Never make the prompt input a single-line `<input>`; generative prompting requires multi-line capacity.
- Submit button must be visually distinguished with `variant="primary"`.

---

## 20. Anti-Patterns & Prohibitions
- **NO ACCIDENTAL SUBMISSIONS:** Do not submit on standard `Enter` without allowing `Shift+Enter` multi-line editing.
- **NO UNINFORMED TOKEN LIMITS:** Do not let the user type beyond model capacity without warning.

---

## 21. AI Usage & Generation Rules
- When user asks to "build a chat prompt box" or "copilot input", the AI **MUST** select `AI-Input-Prompt`.
- The AI must use `Textarea` with `softWrap: true` and `resize: vertical`.
- The AI must include suggestion chips and a submit button.

---

## 22. Verification & Validation Criteria
- [ ] Textarea supports multi-line text and `Shift+Enter`.
- [ ] Token count indicator updates dynamically.
- [ ] Accessible label (`aria-label`) present.
- [ ] Submit button switches to Stop during generation.
- [ ] 0 raw hex colors or physical coordinates.
