# MDS Pattern: AI-Result-Review

**Document Layer:** 05-Patterns / AI  
**Status:** STABLE (Phase 6 Implementation)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-16  

---

## 1. Purpose
The **AI-Result-Review** pattern formats and displays artificial intelligence completions, synthesized reports, or code suggestions with explicit trust indicators, confidence ratings, citation disclosures, copy/regenerate utilities, and user feedback actions.

---

## 2. User Intent
The user intends to read, evaluate, verify, and utilize an AI-generated answer or code artifact, inspect underlying sources or rationale, and provide rating feedback (thumbs up / down) to improve model accuracy.

---

## 3. Problem Solved
Eliminates ungrounded, opaque AI responses that leave users uncertain about hallucination risks. Standardizes how citations, confidence scores, and feedback mechanisms accompany synthesized text.

---

## 4. When to Use
- AI assistant response bubbles and summary generation panels.
- Automated code explanation and documentation synthesis widgets.
- Any view presenting probabilistic generative text requiring user scrutiny.

---

## 5. When Not to Use
- For deterministic, system-generated transactional records: Use standard `Card` or `Alert`.
- For raw markdown files: Use a standard article viewer.
- Do NOT use for real-time video or audio streaming.

---

## 6. Composition Architecture

```text
┌───────────────────────────────────────────────────────────────────────────┐
│ AI-Result-Review (Surface.raised, border, radius.lg, padding="space.5")    │
│                                                                           │
│  Result Meta Header (Inline justify="space-between" align="center")       │
│   ├── Model & Confidence (Inline gap="xs" align="center")                 │
│   │    ├── AI Model Badge: Badge(variant="brand", "✨ Antigravity Pro")    │
│   │    └── Confidence Pill: Badge(variant="success", "98% Confidence")    │
│   │                                                                       │
│   └── Quick Actions (Inline gap="2xs" align="center")                     │
│        ├── Copy Button:       IconButton(icon="📋", label="Copy Output")   │
│        └── Regenerate Button: IconButton(icon="🔄", label="Regenerate")    │
│                                                                           │
│  Divider (border.subtle)                                                  │
│                                                                           │
│  Generated Content Area (Stack gap="sm")                                  │
│   ├── Heading H4 / Title (Optional): "Architecture Recommendations"       │
│   └── Body Prose (Text font.size.sm, line-height=1.6, softWrap: true)     │
│        "Based on the analysis of Phase 5 deliverables, the repository     │
│         satisfies all architectural criteria for Layer 05 patterns..."     │
│                                                                           │
│  Source Disclosure / Citations (Stack gap="2xs", padding="space.2")       │
│   ├── Caption: "📚 Grounding Sources:"                                    │
│   └── Source List: Inline(gap="xs") $\to$ Link("MDS_SPEC.md"), Link(...)   │
│                                                                           │
│  Feedback & Review Footer (Inline justify="space-between" align="center") │
│   ├── Generation Latency (Caption "Generated in 1.2s • 342 tokens")       │
│   └── Feedback Thumbs (Inline gap="2xs")                                  │
│        ├── Upvote:   IconButton(icon="👍", label="Helpful response")      │
│        └── Downvote: IconButton(icon="👎", label="Report issue")          │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Required Components
- `Card` / `Surface` (Layer 03/04 Primitives — elevated card surface)
- `Badge` (Layer 04 Data Display Component — model tag & confidence rating)
- `Text` / `Heading` (Layer 03 Typography Primitives)
- `IconButton` (Layer 04 Actions Component — copy, regenerate, feedback thumbs with mandatory labels)
- `Inline` & `Stack` (Layer 03 Layout Primitives)

---

## 8. Optional Components
- `Link` (Layer 04 Actions Component — source citation links)
- `Alert` (Layer 04 Feedback Component — for low-confidence or safety warnings)
- `Spinner` (Layer 04 Feedback Component — while regenerating or streaming)

---

## 9. Information Hierarchy
1. **Trust Header:** Model identity and confidence metric immediately validate provenance.
2. **Core Body:** The generated response rendered with high-contrast, comfortable line-height.
3. **Evidence Citations:** Supporting references enabling manual verification.
4. **Utility Footer:** Generation metrics and satisfaction feedback rating.

---

## 10. Interaction Model
- Clicking "Copy" copies the generated markdown to clipboard and changes icon to a checkmark for 2 seconds.
- Clicking "Regenerate" displays a `Spinner` and triggers an async API refresh.
- Clicking Upvote/Downvote toggles active state and sends rating telemetry.
- Clicking a source link opens the relevant documentation reference in a safe new tab (`rel="noopener noreferrer"`).

---

## 11. Experience States
- **Streaming In-Progress:** Content streams with a blinking cursor; quick actions are disabled; latency counter counts up.
- **Completed Result:** All actions enabled; citations rendered.
- **Low Confidence Warning:** If confidence $<80\%$, an `Alert(warning)` is prepended: *"Please verify facts independently."*
- **Feedback Submitted:** Thumbs icon remains active; a subtle thank-you caption is displayed.

---

## 12. Responsive Behavior
- **Compact (<640px):**
  - Header and footer inline strips wrap onto two lines.
  - Source citation links stack vertically.
  - Feedback thumbs remain anchored to the trailing edge.
- **Standard & Wide (>640px):**
  - Header and footer maintain clean single-row horizontal distribution (`Inline justify="space-between"`).

---

## 13. Accessibility (a11y)
> *Standards Scope:* Implemented accessibility behaviors were validated against selected WCAG success criteria where applicable. Comprehensive cross-platform assistive technology testing remains deferred to Phase 8.
- Result container has `role="region"` and `aria-label="AI response"`.
- Streaming responses declare `aria-live="polite"` so screen readers announce incoming content without interruption.
- All icon buttons have mandatory accessible labels via `VisuallyHidden` (`aria-label="Copy output"`, `aria-label="Helpful response"`).
- Interactive icon buttons preserve $\ge 44 \times 44\text{px}$ touch hit areas where applicable via `PressTarget`. Static badges and prose text are exempt.

---

## 14. RTL & Logical Progression
- Text prose follows natural script directionality (automatic bi-directional support).
- Model badge sits at `inline-start`, copy/regenerate actions sit at `inline-end`.
- Feedback thumbs sit at `inline-end` in the footer.
- Zero `row-reverse` is permitted.

---

## 15. Density Behavior
- **Comfortable:** Container padding `space.5` (20px), prose `font.size.sm` (14px) with 1.6 leading.
- **Compact:** Container padding `space.3` (12px), prose `font.size.xs` (12px).
- Density does not compress touch targets below $\ge 44 \times 44\text{px}$.

---

## 16. Motion & Animation
- Copy confirmation checkmark transition uses 150ms (`var(--mds-motion-fast)`).
- Collapses to 0s under `prefers-reduced-motion: reduce`.

---

## 17. Token Usage
- Surface: `color.surface.raised`
- Border: `color.border.default`
- Text: `color.text.primary`
- Metadata Text: `color.text.secondary`
- Model Badge: `color.brand.50` / `color.brand.700`
- Confidence Badge: `color.palette.green.50` / `color.palette.green.600`

---

## 18. Contextual Variants
- **Chat Assistant Bubble:** Compact layout tailored for vertical chat logs.
- **Expanded Synthesis Panel:** Full-width report layout with collapsible source citations.

---

## 19. Composition Rules
- Always disclose the generating model and citations where applicable.
- All action icons MUST include an explicit accessible name.
- Never truncate the body text; allow full vertical expansion.

---

## 20. Anti-Patterns & Prohibitions
- **NO SILENT HALLUCINATION RISK:** Never display low-confidence generative answers without a disclaimer.
- **NO UNLABELED ICON BUTTONS:** Never render thumbs up/down icons without `aria-label`.

---

## 21. AI Usage & Generation Rules
- When user asks to "display AI answers" or "show LLM output", the AI **MUST** select `AI-Result-Review`.
- The AI must attach model badges, copy actions, and feedback controls.
- The AI must use `Card` as the container.

---

## 22. Verification & Validation Criteria
- [ ] Container has `role="region"` and accessible label.
- [ ] All icon buttons have accessible names.
- [ ] Copy action successfully copies text.
- [ ] Text wrapping enabled with comfortable line height.
- [ ] 0 raw hex colors or physical coordinates.
