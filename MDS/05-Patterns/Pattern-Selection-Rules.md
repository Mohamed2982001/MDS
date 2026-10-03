# MDS Pattern Selection Engine (PSE) & Selection Rules

**Document Layer:** 05-Patterns  
**Status:** APPROVED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-16  

---

## 1. Purpose & Engine Architecture

The **Pattern Selection Engine (PSE)** provides an algorithmic, deterministic decision framework for selecting the appropriate MDS Pattern for any given user experience requirement. It prevents ad-hoc, inconsistent component assembly by humans and generative AI models.

The selection pipeline flows through 8 sequential evaluation stages:

```text
1. USER INTENT DISCOVERY
        ↓
2. TASK TYPE CLASSIFICATION
        ↓
3. INFORMATION STRUCTURE & VOLUME
        ↓
4. INTERACTION COMPLEXITY
        ↓
5. REQUIRED EXPERIENCE STATES
        ↓
6. RESPONSIVE CONSTRAINTS
        ↓
7. PATTERN CANDIDATE EVALUATION
        ↓
8. SELECTED PATTERN & COMPOSITION BLUEPRINT
```

---

## 2. The 8-Stage Selection Algorithm

### Stage 1: User Intent Discovery
Identify the core goal the end-user is seeking to accomplish:
- **Intent A (Data Entry):** User needs to provide, update, or configure information $\longrightarrow$ **Forms Family**
- **Intent B (Querying & Finding):** User needs to locate specific records from a dataset $\longrightarrow$ **Search & Discovery Family**
- **Intent C (Browsing & Evaluating):** User needs to inspect items, compare entities, or take contextual actions $\longrightarrow$ **Data Interaction Family**
- **Intent D (Feedback & Recovery):** User encounters an empty dataset, system error, or critical decision boundary $\longrightarrow$ **Feedback & Recovery Family**
- **Intent E (Orientation & Navigation):** User needs to understand current application context and access page-level actions $\longrightarrow$ **Navigation & Context Family**
- **Intent F (AI Assistance):** User is prompting a generative model, evaluating an AI completion, or providing feedback $\longrightarrow$ **AI Interaction Family**

---

### Stage 2: Task Type Classification
Determine the workflow criticality and cognitive load:
- `Create / Configure:` Add new entity $\longrightarrow$ `Form-Section`
- `Filter / Narrow:` Refine an existing collection $\longrightarrow$ `Search-Filter-Bar`
- `Inspect / Act:` Read record summary and trigger status change $\longrightarrow$ `Data-List-Card`
- `Handle Empty / Interrupted:` No records found or initial onboarding $\longrightarrow$ `Empty-State`
- `Confirm Destructive Action:` Permanent deletion or high-risk mutation $\longrightarrow$ `Confirmation-Dialog`
- `Top-Level Wayfinding:` Section title and global actions $\longrightarrow$ `Page-Header`
- `Generative Query:` Prompt submission $\longrightarrow$ `AI-Input-Prompt`
- `Generative Review:` Model output inspection and citation review $\longrightarrow$ `AI-Result-Review`

---

### Stage 3: Information Structure & Volume Evaluation
- **Few Discrete Entities (<10 records):** Prefer `Data-List-Card` or simple stacked list; avoid heavy paginated tables.
- **Many Structured Records (>20 rows):** Use `Table` wrapped in a Data Interaction pattern with `Search-Filter-Bar` and pagination. (Never invent a DataGrid).
- **Form Complexity (<6 fields):** Single `Form-Section` in stacked layout.
- **Form Complexity (>8 fields):** Multiple thematic `Form-Section` blocks with descriptive headers and progressive disclosure.

---

### Stage 4: Interaction Complexity
- **Inline / Instant:** Changes take effect immediately $\longrightarrow$ Use `Switch` or inline filter chips without explicit submit.
- **Batched / Staged:** Changes require validation and explicit commit $\longrightarrow$ Use `Form-Section` with footer Action Bar (`Save` primary, `Cancel` secondary).
- **Irreversible / High Risk:** Action cannot be undone $\longrightarrow$ MANDATORY `Confirmation-Dialog` with destructive intent (`variant="destructive"`).

---

### Stage 5: Experience State Requirements
Map required states for the selected pattern:
- Must the pattern support zero items? $\longrightarrow$ Must pair with `Empty-State`.
- Must the pattern support async network fetching? $\longrightarrow$ Must embed `Skeleton` placeholders or `Spinner`.
- Can the submission fail? $\longrightarrow$ Must support `Alert(danger)` or centralized `Field` error annotations.

---

### Stage 6: Responsive Constraints & Viewport Mapping
- **Mobile Viewport (<640px):**
  - Horizontal filter bars must collapse into a vertically stacked layout or modal filter drawer.
  - Page header action bars must stack below the title or collapse secondary actions into an overflow menu.
  - Cards take 100% width; tables enable horizontal scroll containment (`overflow-x: auto`).

---

### Stage 7: Candidate Evaluation Matrix

| If User Intent Is... | And Data Volume Is... | And Risk Level Is... | Then Select Pattern: |
| :--- | :--- | :--- | :--- |
| Enter or update configuration | 1–8 fields | Low / Medium | **`Form-Section`** |
| Locate specific items in collection | Any | Low | **`Search-Filter-Bar`** |
| Scan, review, and act on entities | 1–50 items | Medium | **`Data-List-Card`** |
| Guide user when no data exists | 0 items | Informational | **`Empty-State`** |
| Confirm permanent removal/loss | 1 entity / batch | High (Destructive) | **`Confirmation-Dialog`** |
| Orient user at top of screen | Header context | Informational | **`Page-Header`** |
| Submit generative AI instructions | Variable text | Medium | **`AI-Input-Prompt`** |
| Review and rate generative output | Rich text / cards | Medium | **`AI-Result-Review`** |

---

## 3. Explicit Anti-Pattern Catalog

The following design decisions are **strictly prohibited** by the Pattern Selection Engine:

1. **The "Empty State Without Action" Anti-Pattern:**
   - *Error:* Showing an empty graphic and message with zero path forward.
   - *Requirement:* Every `Empty-State` must provide a primary CTA button (e.g. "Create Item", "Reset Filters", "Learn More").
2. **The "Dialog Over Dialog" Anti-Pattern:**
   - *Error:* Triggering a confirmation modal from inside an existing open modal.
   - *Requirement:* Never stack modal overlays. Use inline confirmation inside the parent modal or replace modal context sequentially.
3. **The "Search Without Clear" Anti-Pattern:**
   - *Error:* Providing a search bar or filter tags with no instant one-click way to reset filters.
   - *Requirement:* All active filters must be dismissible via a "Clear All" link or individual removable badges.
4. **The "Truncated Error Banner" Anti-Pattern:**
   - *Error:* Forcing long form validation errors or alert banners to single-line with ellipsis.
   - *Requirement:* All feedback banners must use `softWrap: true` and display complete error descriptions.
5. **The "Premature Grid" Anti-Pattern:**
   - *Error:* Assembling custom table headers with editable input cells and virtual scrolling in a pattern.
   - *Requirement:* DataGrid is deferred. Use the approved static `Table` component.
