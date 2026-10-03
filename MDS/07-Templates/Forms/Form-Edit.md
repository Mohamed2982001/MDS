# MDS Template: Form-Edit (`MDS-TMP-004`)

**Document Layer:** 07-Templates / Forms  
**Status:** APPROVED (Phase 8.1.3 Delivery)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-17  

---

## 1. Template ID
`MDS-TMP-004`

## 2. Name
Form & Scoped Task Edit Template

## 3. Intent
To provide a distraction-free, width-constrained, linear layout optimized for high-completion task flows, entity creation, structured editing, and multi-step forms.

## 4. Problem Solved
Prevents wide-screen form distortion ("The Tennis Match" anti-pattern where labels and inputs stretch across unreadable widths), standardizes form section grouping, and establishes clear validation error recovery and unsaved changes safety.

## 5. When to Use
- For dedicated entity creation views ("New User", "Create Project", "Submit Request").
- For complex multi-field editing forms requiring thematic sections.
- For sequential multi-step intake flows (wizards) with step indicators.

## 6. When Not to Use
- For high-density operational telemetry: Use `Dashboard-Overview` (`MDS-TMP-001`) instead.
- For read-heavy single-entity inspection: Use `Detail-Entity` (`MDS-TMP-003`) instead.
- For application-wide preference configuration: Use `Settings-Workspace` (`MDS-TMP-005`) instead.

## 7. Page Regions
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Region 1: Focused Task Header (Back / Cancel, Task Title, Step Indicator)   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 2: Scoped Form Container (Constrained Max-Width: 768px – 1024px)     │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ Thematic Form Section 1 (Title, Description, Field Grid)                │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ Thematic Form Section 2 (Title, Description, Field Grid)                │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ Optional Secondary Upload / Attachment Zone                             │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ Region 3: Sticky Form Action Rail (Cancel, Save Draft, Submit / Continue)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 8. Region Hierarchy
`Focused Task Header` $\to$ `Scoped Form Container` (Thematic Sections) $\to$ `Sticky Form Action Rail`.

## 9. Pattern Composition
- **`Page-Header` (`MDS/05-Patterns/Navigation/Page-Header.md`):** Focused header with cancel link, H1 task title, and step indicator badge.
- **`Form-Section` (`MDS/05-Patterns/Forms/Form-Section.md`):** Modular thematic groupings (e.g. "Basic Details", "Contact Information", "Access Permissions").
- **`Confirmation-Dialog` (`MDS/05-Patterns/Feedback/Confirmation-Dialog.md`):** Triggered when navigating away with dirty unsaved changes or clicking Cancel.
- **`Empty-State` (`MDS/05-Patterns/Feedback/Empty-State.md`):** For optional dynamic sub-lists (e.g. "No line items added yet — Add Item").

## 10. Workflow Slots
- **`Form-Submission` (`MDS/06-Workflows/Forms/Form-Submission.md`):** Client-side validation, async submission dispatch, error focus shifting, and non-destructive retry.
- **`Destructive-Action` (`MDS/06-Workflows/Actions/Destructive-Action.md`):** Discarding drafts or resetting form fields.
- **`Error-Recovery` (`MDS/06-Workflows/Recovery/Error-Recovery.md`):** Handles network failure during submit without wiping entered field values.

## 11. Component Dependencies
- `Button`, `Link` (Actions)
- `Field`, `Input`, `Textarea`, `Checkbox`, `Radio`, `Switch`, `Select` (Inputs)
- `Alert`, `Spinner`, `Skeleton` (Feedback)
- `Badge`, `Card` (Data Display)
- `Surface`, `Stack`, `Inline`, `Grid`, `Container` (Primitives)

## 12. Content Slots
- `slot="task-header"`: Title, Subtitle, Stepper component.
- `slot="form-body"`: Multiple `Form-Section` instances.
- `slot="action-bar"`: Primary Submit CTA, Secondary Save Draft, Tertiary Cancel.

## 13. Required vs Optional Regions
- **Required:** Focused Task Header, Scoped Form Container, Sticky Form Action Rail.
- **Optional:** Stepper Indicator (for multi-step flows), Save Draft button.

## 14. Responsive Composition
- **Compact (< 768px):** 2-column field grids collapse to a single column; Action Rail docks as a sticky full-width bottom bar with $\ge 44\text{px}$ touch targets; step indicator simplifies to "Step 2 of 4".
- **Standard (768px – 1151px):** Form container constrained to 768px width; 2-column field grids active where appropriate; action bar remains sticky.
- **Wide (1152px – 1439px):** Form container centered with canonical 768px or 1024px maximum width (never expanding to full 1152px); optimal field widths preserved.
- **Full ($\ge$ 1440px):** Form container strictly centered with generous lateral canvas margins.

## 15. Mobile Composition
- Field labels remain stacked directly above inputs (never horizontal side-labels on mobile).
- Action buttons expand to full width or 50/50 side-by-side with safe-area spacing.
- Form inputs automatically trigger appropriate mobile keyboards (`type="email"`, `type="tel"`).

## 16. RTL Behavior
- Form labels and helper text align to inline-start (`right` in RTL).
- Action bar primary button sits on inline-end; cancel button on inline-start.
- Multi-step progress bar flows right-to-left.
- Zero `row-reverse` hacks used.

## 17. Accessibility Structure
- `<main>` landmark encompasses the scoped form container.
- `<form>` landmark with `aria-labelledby` referencing the H1 title.
- Dynamic error summary banner at the top of the form with `role="alert"` upon failed submission.
- Focus jumps programmatically to the first invalid field upon validation failure.

## 18. Experience States
- **`Default / Pristine`:** Empty or populated fields in resting state.
- **`Dirty / Active Input`:** User has modified fields; unsaved changes navigation guard active.
- **`Validating`:** Instant inline validation feedback on blur.
- **`Submitting`:** Primary submit button shows `Spinner` and enters disabled state; inputs locked to prevent race conditions.
- **`Error Intercepted`:** Validation banner appears; invalid fields highlighted with error message; payload preserved in memory.
- **`Success Resolved`:** Form resolves and redirects to detail/list view or displays confirmation alert.

## 19. Loading Strategy
When editing an existing entity, renders a centered form skeleton (3 section header skeletons, 6 input field skeletons). Zero layout shift.

## 20. Error Strategy
Non-destructive error retention: network failures or validation rejections NEVER clear form inputs. A top-level alert summarizes errors with focus links to each invalid field.

## 21. Empty Strategy
For dynamic child lists within the form (e.g. "Add Additional Contacts"), renders an inline empty placeholder with an "Add Contact" button.

## 22. Recovery Strategy
Offline or network dropout caches form state in session storage; user can click "Retry Submission" once connection is restored without retyping.

## 23. Density Behavior
- **Comfortable:** Standard 48px control height, 16px field padding, 24px vertical stack gap.
- **Compact:** 40px control height, 12px field padding, 16px vertical stack gap.

## 24. Theme/Mode Behavior
- **Light:** Surface Canvas `#F8FAFC`, Form Card `#FFFFFF`, Input Border `#CBD5E1`.
- **Dark:** Surface Canvas `#020617`, Form Card `#0F172A`, Input Border `#334155`.
- **High Contrast:** 2px high-visibility focus rings and 2px input borders.

## 25. AI Integration
Optional "AI Form Auto-Fill / Suggestion" utility: parses uploaded document or prompt to populate fields with clear visual badges indicating "AI Suggested — Review Required".

## 26. Navigation Context
Cancel or browser back triggers an unsaved changes confirmation dialog if form `isDirty == true`.

## 27. Focus Management
Initial focus enters the first input field on page mount; keyboard `Tab` progresses linearly down through fields to the action bar.

## 28. Motion Behavior
Validation error messages expand smoothly with 150ms ease; step transitions slide horizontally; collapses to 0ms in reduced motion mode.

## 29. Token Dependencies
`container.sm` (768px), `container.md` (1024px), `space.4`, `space.6`, `color.surface.*`, `color.action.*`.

## 30. Anti-Patterns
- ❌ Do NOT stretch form inputs full-width across 1440px displays.
- ❌ Do NOT clear form inputs when a submission fails.
- ❌ Do NOT navigate away without warning users about unsaved modifications.

## 31. Validation Requirements
Verified by `run_tests.py`, HTML showcase testbed, and 100% token usage.

## 32. Selection Criteria
Select when user intent is structured data entry, entity creation, checkout, or multi-step wizard workflows.
