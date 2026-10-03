# Agent Rule: Experience States (Empty, Error, Loading, & Recovery)

## 1. Mandatory State Coverage
Every screen, data container, list, table, form, or interactive view MUST explicitly implement and support the following core experience states:

### A. Data States
1. **Loading State:**
   - Use shimmer loaders / skeletons that match the actual geometry of the content.
   - Never use generic blank screens or blocking spinners where content skeleton is feasible.
2. **Empty State:**
   - Must be descriptive, friendly, and provide a clear call-to-action (CTA) to guide the user on what to do next.
   - Never leave empty whitespace without context.
3. **Error State:**
   - Must clearly explain what went wrong without technical jargon.
   - Must provide a contextual recovery path suited to the specific failure (never force a generic "Retry" CTA on every error).
4. **Partial State:**
   - Handle situations where only part of the data loaded successfully without breaking the whole layout.
5. **Success State:**
   - Provide clear, non-intrusive feedback upon task completion.

### B. Access & Permission States
- **Authentication Required:** Seamless prompt/modal or redirect to sign in (Contextual recovery: "Sign in").
- **Permission Denied / No Access:** Informative explanation of why access is restricted (Contextual recovery: "Request access" or navigate back).

### C. Resource States
- **Not Found (404):** Helpful navigation back to safety (Contextual recovery: "Explore homepage / Go back").
- **Deleted / Archived:** Contextual indicator showing historical/read-only status (Contextual recovery: "Restore" if authorized).

### D. Recovery & Resilience
- **Contextual Recovery Mapping:**
  - Network failure → Retry
  - Invalid input → Fix
  - Permission denied → Request access / appropriate next action
  - Authentication expired → Sign in
  - Conflict → Review / resolve
  - Deleted resource → Restore / navigate away
  - Recoverable operation → Undo
- **Offline Mode:** Graceful degradation, local caching indicators, and retry queues.
- **Conflict Resolution & Unsaved Changes:** Warning modals before navigation to prevent data loss.

## 2. Senior Implementation Standard
- In Flutter: Use sealed class / union states with `BlocBuilder` / `BlocConsumer` (e.g., `Initial`, `Loading`, `Success`, `Failure`, `Empty`).
- In React / Next.js: Use specialized boundary components (`loading.tsx`, `error.tsx`, `not-found.tsx`, and component-level skeletons).
