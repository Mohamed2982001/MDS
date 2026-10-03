/**
 * Master Design System (MDS) — Documentation Portal Interactive Client
 * Phase 8.1.4: Unified Documentation Catalog
 * Zero external dependencies. Native Browser Modern Vanilla JS.
 * Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
 */

(function () {
  'use strict';

  // --- 1. Embedded Canonical Index Dataset (Offline & file:// Resilient) ---
  const EMBEDDED_INDEX = {
    system: "Master Design System (MDS)",
    version: "1.0.0",
    phase: "8.1.4",
    lead_architect: "Mohamed Khalid",
    invariants: {
      tokens_total: 188,
      component_tokens: 47,
      components_total: 19,
      patterns_total: 8,
      workflows_total: 6,
      templates_total: 6,
      enterprise_deferred_total: 9,
      tests_defined: 44,
      tests_passed: 41,
      tests_deferred: 3
    },
    components: [
      { id: "button", name: "Button", family: "Actions", status: "Implemented", tokens: ["btn.primary.bg", "btn.primary.text", "btn.radius"], desc: "Primary interactive control for user actions with primary, secondary, danger, and ghost variants." },
      { id: "icon-button", name: "IconButton", family: "Actions", status: "Implemented", tokens: ["icon-btn.size.md", "icon-btn.padding"], desc: "Compact icon-only interactive button enforcing minimum 44x44px touch bounding box." },
      { id: "link", name: "Link", family: "Actions", status: "Implemented", tokens: ["link.color", "link.hover.color"], desc: "Navigational anchor with distinct underline styling and visible focus indicator." },
      { id: "field", name: "Field", family: "Inputs", status: "Implemented", tokens: ["field.gap", "field.label.color"], desc: "Composite form control container providing label, helper hint, and error message slots." },
      { id: "input", name: "Input", family: "Inputs", status: "Implemented", tokens: ["input.bg", "input.border", "input.focus.ring"], desc: "Single-line text input supporting text, email, password, and number data entries." },
      { id: "textarea", name: "Textarea", family: "Inputs", status: "Implemented", tokens: ["textarea.bg", "textarea.border"], desc: "Multi-line text input field with vertical resizing and character counter integration." },
      { id: "checkbox", name: "Checkbox", family: "Inputs", status: "Implemented", tokens: ["checkbox.size", "checkbox.checked.bg"], desc: "Binary or indeterminate selection control for multi-option selection lists." },
      { id: "radio", name: "Radio", family: "Inputs", status: "Implemented", tokens: ["radio.size", "radio.checked.dot"], desc: "Mutual-exclusion selection control for single selection within a defined option set." },
      { id: "switch", name: "Switch", family: "Inputs", status: "Implemented", tokens: ["switch.track.w", "switch.motion.duration"], desc: "Instant toggle control for binary settings with token-bound motion transition." },
      { id: "select", name: "Select", family: "Inputs", status: "Implemented", tokens: ["select.bg", "select.border"], desc: "Core baseline dropdown selection control utilizing native platform select element." },
      { id: "alert", name: "Alert", family: "Feedback", status: "Implemented", tokens: ["alert.info.bg", "alert.success.bg", "alert.error.bg"], desc: "Status banner communicating contextual feedback across info, success, warning, and error states." },
      { id: "spinner", name: "Spinner", family: "Feedback", status: "Implemented", tokens: ["spinner.size.md", "spinner.arc.color"], desc: "Continuous circular animation indicating active indeterminate background processing." },
      { id: "skeleton", name: "Skeleton", family: "Feedback", status: "Implemented", tokens: ["skeleton.bg", "skeleton.shimmer"], desc: "Placeholder shape rendering shimmer animation during asynchronous data loading." },
      { id: "badge", name: "Badge", family: "Data Display", status: "Implemented", tokens: ["badge.bg", "badge.text", "badge.radius"], desc: "Compact label displaying metadata, counts, category tags, or operational statuses." },
      { id: "card", name: "Card", family: "Data Display", status: "Implemented", tokens: ["card.bg", "card.border", "card.shadow"], desc: "Contained structural surface grouping related visual content and user actions." },
      { id: "table", name: "Table", family: "Data Display", status: "Implemented", tokens: ["table.header.bg", "table.row.hover"], desc: "Tabular grid organizing structured data rows with header cells and row hover feedback." },
      { id: "tabs", name: "Tabs", family: "Navigation", status: "Implemented", tokens: ["tabs.track.border", "tabs.active.border"], desc: "Segmented navigational control organizing content into selectable pane views." },
      { id: "dialog", name: "Dialog", family: "Overlays", status: "Specified", tokens: ["dialog.overlay.bg", "dialog.panel.bg"], desc: "Modal overlay dialog interrupting the workflow to present urgent decisions or confirmations." },
      { id: "tooltip", name: "Tooltip", family: "Overlays", status: "Specified", tokens: ["tooltip.bg", "tooltip.text"], desc: "Floating contextual label presenting descriptive hint text on focus or hover." }
    ],
    patterns: [
      { id: "page-header", name: "Page-Header", category: "Structural & Navigation", status: "Manually Verified", desc: "Top-level landmark pattern displaying page title, breadcrumb context, status badges, and action bars." },
      { id: "search-filter-bar", name: "Search-Filter-Bar", category: "Data & Discovery", status: "Manually Verified", desc: "Unified discovery bar combining real-time keyword search, filter dropdowns, and active tag chips." },
      { id: "data-list-card", name: "Data-List-Card", category: "Data & Discovery", status: "Manually Verified", desc: "Responsive entity card displaying thumbnail, title, status badge, metadata attributes, and quick action bar." },
      { id: "form-section", name: "Form-Section", category: "Data Input & Editing", status: "Manually Verified", desc: "Grouped form layout organizing related input fields under semantic section headings and helper text." },
      { id: "empty-state", name: "Empty-State", category: "Feedback & Resilience", status: "Manually Verified", desc: "Contextual placeholder communicating zero data records with visual illustration and clear call-to-action." },
      { id: "confirmation-dialog", name: "Confirmation-Dialog", category: "Overlay & Decision", status: "Manually Verified", desc: "Modal decision dialog safeguarding high-impact operations with explicit confirm and cancel actions." },
      { id: "ai-input-prompt", name: "AI-Input-Prompt", category: "AI Co-Pilot", status: "Manually Verified", desc: "Specialized prompt composition box supporting model parameter toggles, token count badges, and submit trigger." },
      { id: "ai-result-review", name: "AI-Result-Review", category: "AI Co-Pilot", status: "Manually Verified", desc: "Human-in-the-loop review panel displaying AI generated output, confidence score, and diff comparison." }
    ],
    workflows: [
      { id: "form-submission", code: "MDS-WFL-001", name: "Form-Submission", status: "Manually Verified", steps: ["Drafting", "Client Validation", "Submitting", "Server Confirmation", "Completed"], desc: "Canonical data entry workflow with asynchronous validation, loading feedback, and error recovery." },
      { id: "search-discovery", code: "MDS-WFL-002", name: "Search-Discovery", status: "Manually Verified", steps: ["Idle Query", "Debounced Search", "Results Rendering", "Facet Filtering", "Empty Fallback"], desc: "Query orchestration workflow handling instant search, facet management, pagination, and zero-match handling." },
      { id: "destructive-action", code: "MDS-WFL-003", name: "Destructive-Action", status: "Manually Verified", steps: ["Intent Trigger", "Modal Confirmation", "Typed Verification", "Execution", "Audit Logging"], desc: "High-risk workflow enforcing explicit user confirmation, two-phase verification, and irreversible action safeguarding." },
      { id: "settings-update", code: "MDS-WFL-004", name: "Settings-Update", status: "Manually Verified", steps: ["Read Current", "Field Mutation", "Autosave / Manual Save", "Toast Confirmation"], desc: "Workspace configuration workflow supporting immediate and batch persistence with rollback capability." },
      { id: "ai-synthesis-review", code: "MDS-WFL-005", name: "AI-Synthesis-Review", status: "Manually Verified", steps: ["Prompt Dispatch", "Streaming Response", "Human Verification", "Accept / Reject", "Persistence"], desc: "Generative AI workflow enforcing human-in-the-loop oversight and non-destructive output persistence." },
      { id: "error-recovery", code: "MDS-WFL-006", name: "Error-Recovery", status: "Manually Verified", steps: ["Fault Interception", "Categorization", "Contextual Fallback", "Retry Orchestration"], desc: "Resilience workflow intercepting network, auth, or validation faults with intelligent retry mechanics." }
    ],
    templates: [
      { id: "dashboard-overview", code: "MDS-TMP-001", name: "Dashboard-Overview", category: "Operational Overview", status: "Manually Verified", desc: "Executive monitoring dashboard aggregating high-level KPI metric cards, analytical charts, and recent activity." },
      { id: "list-management", code: "MDS-TMP-002", name: "List-Management", category: "Collection Management", status: "Manually Verified", desc: "Scalable entity management catalog unifying search, multi-faceted filtering, sorting, pagination, and batch actions." },
      { id: "detail-entity", code: "MDS-TMP-003", name: "Detail-Entity", category: "Entity Inspection", status: "Manually Verified", desc: "Comprehensive entity deep-dive layout with sticky header, tabbed metadata views, sidebar summary, and action bar." },
      { id: "form-edit", code: "MDS-TMP-004", name: "Form-Edit", category: "Data Authoring", status: "Manually Verified", desc: "Full-page transactional authoring layout featuring stepped form sections, field validation, and sticky footer bar." },
      { id: "settings-workspace", code: "MDS-TMP-005", name: "Settings-Workspace", category: "Configuration", status: "Manually Verified", desc: "Multi-pane workspace preferences layout with vertical category navigation, autosave toggles, and security controls." },
      { id: "ai-workspace", code: "MDS-TMP-006", name: "AI-Workspace", category: "Intelligence & Synthesis", status: "Manually Verified", desc: "Interactive AI studio integrating prompt engineering console, streaming preview, human review, and side-by-side diff." }
    ],
    sample_tokens: [
      { name: "--mds-color-brand-600", tier: "Semantic", value: "#2563EB", desc: "Primary brand sapphire accent for interactive actions" },
      { name: "--mds-color-brand-700", tier: "Semantic", value: "#1D4ED8", desc: "Hover state for brand actions" },
      { name: "--mds-color-surface-canvas", tier: "Semantic", value: "#F8FAFC", desc: "Background canvas surface level" },
      { name: "--mds-color-surface-default", tier: "Semantic", value: "#FFFFFF", desc: "Default card and container surface" },
      { name: "--mds-color-text-primary", tier: "Semantic", value: "#0F172A", desc: "High contrast primary body and heading text" },
      { name: "--mds-color-text-secondary", tier: "Semantic", value: "#475569", desc: "Secondary supportive text" },
      { name: "--mds-color-success", tier: "Semantic", value: "#059669", desc: "Positive outcome and confirmation indicator" },
      { name: "--mds-color-danger", tier: "Semantic", value: "#DC2626", desc: "Destructive action and error state indicator" },
      { name: "--mds-space-4", tier: "Primitive", value: "16px", desc: "Core base 4px-grid modular spacing step" },
      { name: "--mds-space-6", tier: "Primitive", value: "24px", desc: "Structural container padding and card margins" },
      { name: "--mds-radius-md", tier: "Primitive", value: "10px", desc: "Soft Modern corner radius for buttons and inputs" },
      { name: "--mds-radius-lg", tier: "Primitive", value: "14px", desc: "Card and dialog modal corner radius" }
    ]
  };

  let systemData = EMBEDDED_INDEX;

  // --- 2. Toast Notification Utility ---
  function showToast(message) {
    let toast = document.getElementById('mds-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'mds-toast';
      toast.className = 'mds-doc-toast';
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('is-visible');
    setTimeout(() => {
      toast.classList.remove('is-visible');
    }, 2200);
  }

  // --- 3. Clipboard Action ---
  window.copyToken = function (tokenName) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(`var(${tokenName})`).then(() => {
        showToast(`Copied: var(${tokenName})`);
      }).catch(() => {
        showToast(`Selected: ${tokenName}`);
      });
    } else {
      showToast(`Token: ${tokenName}`);
    }
  };

  // --- 4. View Renderers ---
  const views = {
    overview: function () {
      return `
        <header class="mds-doc-page-header">
          <div class="mds-doc-breadcrumb">
            <span>MDS</span> <span>/</span> <span>Overview</span>
          </div>
          <h1 class="mds-doc-page-title">Master Design System (MDS)</h1>
          <p class="mds-doc-page-desc">
            Unified single-pane-of-glass catalog and living documentation for enterprise full-stack & mobile applications.
            Built with Cairo typography, chromatic slate surfaces, 188 registered tokens, and soft modern elegance.
          </p>
        </header>

        <section class="mds-doc-stats-grid">
          <div class="mds-doc-stat-card">
            <span class="mds-doc-stat-value">188</span>
            <span class="mds-doc-stat-label">Total Design Tokens (DTCG 3-Tier)</span>
          </div>
          <div class="mds-doc-stat-card">
            <span class="mds-doc-stat-value">19</span>
            <span class="mds-doc-stat-label">Core Atomic Components (6 Families)</span>
          </div>
          <div class="mds-doc-stat-card">
            <span class="mds-doc-stat-value">8</span>
            <span class="mds-doc-stat-label">Canonical Composite Patterns</span>
          </div>
          <div class="mds-doc-stat-card">
            <span class="mds-doc-stat-value">6</span>
            <span class="mds-doc-stat-label">Canonical Business Workflows (FSM)</span>
          </div>
          <div class="mds-doc-stat-card">
            <span class="mds-doc-stat-value">6</span>
            <span class="mds-doc-stat-label">Page Archetype Templates</span>
          </div>
          <div class="mds-doc-stat-card">
            <span class="mds-doc-stat-value">41 / 44</span>
            <span class="mds-doc-stat-label">Automated Tests Passed (100% Executable)</span>
          </div>
        </section>

        <h2 style="font-size: var(--mds-font-size-xl); margin-block-end: var(--mds-space-4);">MDS 14-Layer Hierarchy</h2>
        <div class="mds-doc-grid">
          ${[
            { num: "01", name: "Strategy & DNA", desc: "Brand values, soft modern aesthetic, Cairo typography, persona architecture." },
            { num: "02", name: "Design Tokens", desc: "188 tokens in W3C DTCG format across Primitive, Semantic, and Component tiers." },
            { num: "03", name: "Primitives", desc: "Layout engines (Stack, Grid, Container), Surface Triad, and Accessibility Primitives." },
            { num: "04", name: "Components", desc: "19 production-grade core components adhering to 16-point component anatomy." },
            { num: "05", name: "Patterns", desc: "8 canonical patterns (Page-Header, Search-Filter-Bar, Data-List-Card, etc.)." },
            { num: "06", name: "Workflows", desc: "6 multi-step business flows with formal 11-state FSM progression & recovery." },
            { num: "07", name: "Templates", desc: "6 full-page responsive archetypes (Dashboard, List, Detail, Form, Settings, AI)." },
            { num: "08", name: "States", desc: "Universal 11 operational states (Loading, Empty, Error, Retrying, etc.)." },
            { num: "09", name: "Accessibility", desc: "33-test AT audit matrix, 7-facet law, 44px min touch hitboxes." },
            { num: "10", name: "Responsive", desc: "5 breakpoint tiers (320px–1440px), fluid reflow, container queries." },
            { num: "11", name: "AI Layer", desc: "Human-in-the-loop synthesis review, prompt box, non-destructive persistence." },
            { num: "12", name: "Governance", desc: "8-stage lifecycle, 4 governance laws, ADR architectural decision logs." },
            { num: "13", name: "Testing", desc: "Executable Python test harness with 44 test cases across 12 suites." },
            { num: "14", name: "Documentation", desc: "Zero-dependency static portal, live search index, and token explorer." }
          ].map(l => `
            <div class="mds-doc-card">
              <div class="mds-doc-card-header">
                <span class="mds-doc-badge mds-doc-badge--info">Layer ${l.num}</span>
                <span class="mds-doc-badge mds-doc-badge--success">APPROVED</span>
              </div>
              <h3 class="mds-doc-card-title">${l.name}</h3>
              <p class="mds-doc-card-body">${l.desc}</p>
            </div>
          `).join('')}
        </div>
      `;
    },

    tokens: function () {
      return `
        <header class="mds-doc-page-header">
          <div class="mds-doc-breadcrumb">
            <span>MDS</span> <span>/</span> <span>Tokens</span>
          </div>
          <h1 class="mds-doc-page-title">Design Token Explorer</h1>
          <p class="mds-doc-page-desc">
            Explore 188 registered design tokens organized across the 3-Tier W3C DTCG Model.
            Click any token CSS variable to copy its invocation snippet directly to your clipboard.
          </p>
        </header>

        <div class="mds-doc-filter-strip">
          <button class="mds-doc-filter-btn is-active" onclick="filterTokens('all')">All Tokens (188)</button>
          <button class="mds-doc-filter-btn" onclick="filterTokens('color')">Colors & Surfaces</button>
          <button class="mds-doc-filter-btn" onclick="filterTokens('space')">Spacing (4px Grid)</button>
          <button class="mds-doc-filter-btn" onclick="filterTokens('radius')">Shape & Radii</button>
          <button class="mds-doc-filter-btn" onclick="filterTokens('motion')">Motion & Easing</button>
        </div>

        <table class="mds-doc-token-table" id="token-table">
          <thead>
            <tr>
              <th>Token Name (Click to Copy)</th>
              <th>Tier</th>
              <th>Visual Swatch / Preview</th>
              <th>Resolved Value</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            ${systemData.sample_tokens.map(t => {
              const isColor = t.value.startsWith('#') || t.value.includes('rgba');
              const isRadius = t.name.includes('radius');
              const isSpace = t.name.includes('space');
              return `
                <tr>
                  <td>
                    <span class="mds-doc-token-code" onclick="copyToken('${t.name}')" title="Click to copy var(${t.name})">
                      ${t.name}
                    </span>
                  </td>
                  <td><span class="mds-doc-badge mds-doc-badge--neutral">${t.tier}</span></td>
                  <td>
                    ${isColor ? `<span class="mds-doc-swatch" style="background-color: var(${t.name}, ${t.value});"></span>` : ''}
                    ${isRadius ? `<span class="mds-doc-swatch" style="background-color: var(--mds-color-brand-100); border-radius: var(${t.name});"></span>` : ''}
                    ${isSpace ? `<span class="mds-doc-swatch" style="background-color: var(--mds-color-brand-500); width: ${t.value}; height: 12px;"></span>` : ''}
                  </td>
                  <td style="font-family: var(--mds-font-family-mono); font-size: var(--mds-font-size-xs);">${t.value}</td>
                  <td>${t.desc}</td>
                </tr>
              `;
            }).join('')}
          </tbody>
        </table>
      `;
    },

    components: function () {
      return `
        <header class="mds-doc-page-header">
          <div class="mds-doc-breadcrumb">
            <span>MDS</span> <span>/</span> <span>Components</span>
          </div>
          <h1 class="mds-doc-page-title">Core Component Catalog (19 Components)</h1>
          <p class="mds-doc-page-desc">
            Complete inventory of all 19 approved core components grouped across 6 families.
            17 components are fully implemented and verified; Dialog and Tooltip are specification-verified.
          </p>
        </header>

        <div class="mds-doc-grid">
          ${systemData.components.map(c => `
            <div class="mds-doc-card">
              <div class="mds-doc-card-header">
                <span class="mds-doc-badge mds-doc-badge--neutral">${c.family}</span>
                <span class="mds-doc-badge ${c.status === 'Implemented' ? 'mds-doc-badge--success' : 'mds-doc-badge--warning'}">
                  ${c.status}
                </span>
              </div>
              <h3 class="mds-doc-card-title">${c.name}</h3>
              <p class="mds-doc-card-body">${c.desc}</p>
              <div class="mds-doc-card-footer">
                <span>Tokens: ${c.tokens.length}</span>
                <span style="font-family: var(--mds-font-family-mono);">16-Point Anatomy</span>
              </div>
            </div>
          `).join('')}
        </div>

        <div style="margin-block-start: var(--mds-space-8); padding: var(--mds-space-6); background-color: var(--mds-color-surface-default); border: var(--mds-border-width-thin) dashed var(--mds-color-border-default); border-radius: var(--mds-radius-lg);">
          <h3 style="margin-block-start: 0; font-size: var(--mds-font-size-base);">🔒 9 Complex Enterprise Systems (Deferred to Phase 9)</h3>
          <p style="font-size: var(--mds-font-size-sm); color: var(--mds-color-text-secondary); margin-block-end: var(--mds-space-4);">
            To safeguard architectural discipline, the following complex systems remain strictly deferred and will not be introduced until Phase 9:
          </p>
          <div style="display: flex; flex-wrap: wrap; gap: var(--mds-space-2);">
            ${["DataGrid", "RichTextEditor", "Calendar", "DateRangePicker", "CommandSystem", "Tree", "Combobox", "VirtualizedList", "FileUploadManager"].map(s => `
              <span class="mds-doc-badge mds-doc-badge--deferred">${s} (Deferred)</span>
            `).join('')}
          </div>
        </div>
      `;
    },

    patterns: function () {
      return `
        <header class="mds-doc-page-header">
          <div class="mds-doc-breadcrumb">
            <span>MDS</span> <span>/</span> <span>Patterns</span>
          </div>
          <h1 class="mds-doc-page-title">Canonical Pattern Catalog (8 Patterns)</h1>
          <p class="mds-doc-page-desc">
            Reusable multi-component patterns resolving frequent user interaction challenges.
            Adheres strictly to the 22-point pattern anatomy and 10 Inviolable Composition Laws.
          </p>
        </header>

        <div class="mds-doc-grid">
          ${systemData.patterns.map(p => `
            <div class="mds-doc-card">
              <div class="mds-doc-card-header">
                <span class="mds-doc-badge mds-doc-badge--info">${p.category}</span>
                <span class="mds-doc-badge mds-doc-badge--success">${p.status}</span>
              </div>
              <h3 class="mds-doc-card-title">${p.name}</h3>
              <p class="mds-doc-card-body">${p.desc}</p>
              <div class="mds-doc-card-footer">
                <span>RTL Symmetric</span>
                <span style="font-family: var(--mds-font-family-mono);">22-Pt Anatomy</span>
              </div>
            </div>
          `).join('')}
        </div>
      `;
    },

    workflows: function () {
      return `
        <header class="mds-doc-page-header">
          <div class="mds-doc-breadcrumb">
            <span>MDS</span> <span>/</span> <span>Workflows</span>
          </div>
          <h1 class="mds-doc-page-title">Canonical Multi-Step Workflows (6 Workflows)</h1>
          <p class="mds-doc-page-desc">
            End-to-end business workflows orchestrating state progression, fault tolerance, and security triages.
            Includes an interactive state machine visualizer for testing transition states.
          </p>
        </header>

        <h3 style="font-size: var(--mds-font-size-base); margin-block-end: var(--mds-space-2);">Interactive FSM State Simulator</h3>
        <p style="font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary); margin-block-end: var(--mds-space-4);">
          Click on any state node below to simulate progression across universal operational lifecycle states:
        </p>
        <div class="mds-doc-fsm-container" id="fsm-sim">
          <div class="mds-doc-fsm-node is-active" onclick="setFsmState(this)">1. IDLE / DRAFT</div>
          <span class="mds-doc-fsm-arrow">➔</span>
          <div class="mds-doc-fsm-node" onclick="setFsmState(this)">2. VALIDATING</div>
          <span class="mds-doc-fsm-arrow">➔</span>
          <div class="mds-doc-fsm-node" onclick="setFsmState(this)">3. PROCESSING</div>
          <span class="mds-doc-fsm-arrow">➔</span>
          <div class="mds-doc-fsm-node" onclick="setFsmState(this)">4. SUCCESS / PERSISTED</div>
          <span class="mds-doc-fsm-arrow">➔</span>
          <div class="mds-doc-fsm-node" onclick="setFsmState(this)">5. ERROR / RECOVERY</div>
        </div>

        <div class="mds-doc-grid">
          ${systemData.workflows.map(w => `
            <div class="mds-doc-card">
              <div class="mds-doc-card-header">
                <span class="mds-doc-badge mds-doc-badge--info">${w.code}</span>
                <span class="mds-doc-badge mds-doc-badge--success">${w.status}</span>
              </div>
              <h3 class="mds-doc-card-title">${w.name}</h3>
              <p class="mds-doc-card-body">${w.desc}</p>
              <div style="margin-block-end: var(--mds-space-4);">
                <div style="font-size: var(--mds-font-size-xs); font-weight: 600; margin-block-end: var(--mds-space-1);">Progression Steps:</div>
                <div style="font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">
                  ${w.steps.join(' ➔ ')}
                </div>
              </div>
              <div class="mds-doc-card-footer">
                <span>Security Triad Verified</span>
                <span style="font-family: var(--mds-font-family-mono);">11-State FSM</span>
              </div>
            </div>
          `).join('')}
        </div>
      `;
    },

    templates: function () {
      return `
        <header class="mds-doc-page-header">
          <div class="mds-doc-breadcrumb">
            <span>MDS</span> <span>/</span> <span>Templates</span>
          </div>
          <h1 class="mds-doc-page-title">Page Archetype Templates (6 Templates)</h1>
          <p class="mds-doc-page-desc">
            Production-ready full-page layouts providing blueprints for application views.
            Combines patterns, hosted workflow slots, and responsive recomposition rules.
          </p>
        </header>

        <div class="mds-doc-grid">
          ${systemData.templates.map(t => `
            <div class="mds-doc-card">
              <div class="mds-doc-card-header">
                <span class="mds-doc-badge mds-doc-badge--info">${t.code}</span>
                <span class="mds-doc-badge mds-doc-badge--success">${t.status}</span>
              </div>
              <h3 class="mds-doc-card-title">${t.name}</h3>
              <p class="mds-doc-card-body">${t.desc}</p>
              <div class="mds-doc-card-footer">
                <span>${t.category}</span>
                <span style="font-family: var(--mds-font-family-mono);">32-Pt Anatomy</span>
              </div>
            </div>
          `).join('')}
        </div>
      `;
    },

    accessibility: function () {
      return `
        <header class="mds-doc-page-header">
          <div class="mds-doc-breadcrumb">
            <span>MDS</span> <span>/</span> <span>Accessibility</span>
          </div>
          <h1 class="mds-doc-page-title">Accessibility & Assistive Technology Matrix</h1>
          <p class="mds-doc-page-desc">
            Detailed verification matrix covering 33 accessibility audits, semantic landmarks, and keyboard focus lifecycles.
            Physical screen reader testing is formally deferred to QA Lab per Phase 8.1.1.
          </p>
        </header>

        <div class="mds-doc-stats-grid">
          <div class="mds-doc-stat-card">
            <span class="mds-doc-stat-value">23 / 33</span>
            <span class="mds-doc-stat-label">Environmentally Verified in Dev Runtime</span>
          </div>
          <div class="mds-doc-stat-card">
            <span class="mds-doc-stat-value">10 / 33</span>
            <span class="mds-doc-stat-label">Specification Verified Contracts</span>
          </div>
          <div class="mds-doc-stat-card">
            <span class="mds-doc-stat-value">6 Cases</span>
            <span class="mds-doc-stat-label">Physical Screen Reader Tests (Deferred to QA Lab)</span>
          </div>
        </div>

        <table class="mds-doc-token-table">
          <thead>
            <tr>
              <th>Audit Dimension</th>
              <th>Evaluation Criteria</th>
              <th>Compliance Standard</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Keyboard Traversal</strong></td>
              <td>Logical Tab order, visible focus ring, Escape to dismiss</td>
              <td>WCAG 2.1.1, 2.4.7</td>
              <td><span class="mds-doc-badge mds-doc-badge--success">PASS</span></td>
            </tr>
            <tr>
              <td><strong>Touch Targets</strong></td>
              <td>Minimum 44×44px interactive hitbox for touch</td>
              <td>WCAG 2.5.5, MDS-CMP-003</td>
              <td><span class="mds-doc-badge mds-doc-badge--success">PASS</span></td>
            </tr>
            <tr>
              <td><strong>Color Contrast</strong></td>
              <td>4.5:1 text/bg ratio, 3:1 graphical elements</td>
              <td>WCAG 1.4.3, 1.4.11</td>
              <td><span class="mds-doc-badge mds-doc-badge--success">PASS</span></td>
            </tr>
            <tr>
              <td><strong>State Communication</strong></td>
              <td>Visual states accompanied by text/icon (not color alone)</td>
              <td>WCAG 1.4.1</td>
              <td><span class="mds-doc-badge mds-doc-badge--success">PASS</span></td>
            </tr>
            <tr>
              <td><strong>Bidirectional Mirroring</strong></td>
              <td>Zero flex row-reverse, 100% CSS logical properties</td>
              <td>MDS Bidi Law</td>
              <td><span class="mds-doc-badge mds-doc-badge--success">PASS</span></td>
            </tr>
            <tr>
              <td><strong>Screen Readers (NVDA/VoiceOver)</strong></td>
              <td>Real-world speech synthesizer annunciations</td>
              <td>Physical AT</td>
              <td><span class="mds-doc-badge mds-doc-badge--deferred">DEFERRED TO QA LAB</span></td>
            </tr>
          </tbody>
        </table>
      `;
    },

    testing: function () {
      return `
        <header class="mds-doc-page-header">
          <div class="mds-doc-breadcrumb">
            <span>MDS</span> <span>/</span> <span>Testing</span>
          </div>
          <h1 class="mds-doc-page-title">Automated Test Suite & Regression Harness</h1>
          <p class="mds-doc-page-desc">
            Centralized Python testing harness (<code>MDS/10-Testing/run_tests.py</code>) running 41 executable test cases
            across 12 architectural suites with 100% pass rate and zero failures.
          </p>
        </header>

        <div class="mds-doc-stats-grid">
          <div class="mds-doc-stat-card">
            <span class="mds-doc-stat-value">44</span>
            <span class="mds-doc-stat-label">Total Tests Defined</span>
          </div>
          <div class="mds-doc-stat-card">
            <span class="mds-doc-stat-value">41</span>
            <span class="mds-doc-stat-label">Tests Executed & Passed</span>
          </div>
          <div class="mds-doc-stat-card">
            <span class="mds-doc-stat-value">0</span>
            <span class="mds-doc-stat-label">Failures Recorded</span>
          </div>
          <div class="mds-doc-stat-card">
            <span class="mds-doc-stat-value">3</span>
            <span class="mds-doc-stat-label">Deferred Tests (CI / Headless)</span>
          </div>
        </div>

        <h3 style="font-size: var(--mds-font-size-base); margin-block-end: var(--mds-space-4);">Test Suites Inventory (12 Suites)</h3>
        <div class="mds-doc-grid">
          ${[
            { id: "SUITE 1", name: "Token Integrity", count: "6 Tests", status: "PASS" },
            { id: "SUITE 2", name: "Core Primitives", count: "5 Tests", status: "PASS" },
            { id: "SUITE 3", name: "Component Contracts", count: "5 Tests", status: "PASS" },
            { id: "SUITE 4", name: "Pattern Integrity", count: "4 Tests", status: "PASS" },
            { id: "SUITE 5", name: "Workflow Architecture", count: "4 Tests", status: "PASS" },
            { id: "SUITE 6", name: "Accessibility Rules", count: "4 Tests", status: "3 PASS / 1 DEFERRED" },
            { id: "SUITE 7", name: "Bidirectional & RTL", count: "3 Tests", status: "PASS" },
            { id: "SUITE 8", name: "Responsive Design", count: "3 Tests", status: "2 PASS / 1 DEFERRED" },
            { id: "SUITE 9", name: "Experience States", count: "3 Tests", status: "PASS" },
            { id: "SUITE 10", name: "Visual Regression", count: "1 Test", status: "DEFERRED TO CI" },
            { id: "SUITE 11", name: "Templates Architecture", count: "4 Tests", status: "PASS" },
            { id: "SUITE 12", name: "Documentation Portal", count: "4 Tests", status: "PASS" }
          ].map(s => `
            <div class="mds-doc-card">
              <div class="mds-doc-card-header">
                <span class="mds-doc-badge mds-doc-badge--info">${s.id}</span>
                <span class="mds-doc-badge ${s.status.includes('DEFERRED') ? 'mds-doc-badge--warning' : 'mds-doc-badge--success'}">${s.status}</span>
              </div>
              <h4 class="mds-doc-card-title" style="font-size: var(--mds-font-size-base);">${s.name}</h4>
              <p class="mds-doc-card-body" style="margin: 0;">${s.count}</p>
            </div>
          `).join('')}
        </div>
      `;
    }
  };

  // --- 5. FSM Interactive Helper ---
  window.setFsmState = function (element) {
    const parent = element.parentElement;
    parent.querySelectorAll('.mds-doc-fsm-node').forEach(node => node.classList.remove('is-active'));
    element.classList.add('is-active');
    showToast(`State transition: ${element.textContent.trim()}`);
  };

  // --- 6. Global Search & Filter ---
  window.handleSearch = function (query) {
    const q = query.trim().toLowerCase();
    const main = document.getElementById('main-content');
    if (!q) {
      renderRoute();
      return;
    }

    const matches = [];
    systemData.components.forEach(c => {
      if (c.name.toLowerCase().includes(q) || c.desc.toLowerCase().includes(q) || c.family.toLowerCase().includes(q)) {
        matches.push({ type: "Component", title: c.name, desc: c.desc, badge: c.family });
      }
    });
    systemData.patterns.forEach(p => {
      if (p.name.toLowerCase().includes(q) || p.desc.toLowerCase().includes(q) || p.category.toLowerCase().includes(q)) {
        matches.push({ type: "Pattern", title: p.name, desc: p.desc, badge: p.category });
      }
    });
    systemData.workflows.forEach(w => {
      if (w.name.toLowerCase().includes(q) || w.desc.toLowerCase().includes(q) || w.code.toLowerCase().includes(q)) {
        matches.push({ type: "Workflow", title: w.name, desc: w.desc, badge: w.code });
      }
    });
    systemData.templates.forEach(t => {
      if (t.name.toLowerCase().includes(q) || t.desc.toLowerCase().includes(q) || t.code.toLowerCase().includes(q)) {
        matches.push({ type: "Template", title: t.name, desc: t.desc, badge: t.code });
      }
    });

    main.innerHTML = `
      <header class="mds-doc-page-header">
        <h1 class="mds-doc-page-title">Search Results</h1>
        <p class="mds-doc-page-desc" aria-live="polite">
          Found <strong>${matches.length}</strong> matching item(s) for "${query}".
        </p>
      </header>
      <div class="mds-doc-grid">
        ${matches.length === 0 ? `
          <div style="grid-column: 1 / -1; padding: var(--mds-space-8); text-align: center; background-color: var(--mds-color-surface-default); border-radius: var(--mds-radius-lg);">
            <p style="font-size: var(--mds-font-size-lg); color: var(--mds-color-text-secondary);">No matching entities found.</p>
          </div>
        ` : matches.map(m => `
          <div class="mds-doc-card">
            <div class="mds-doc-card-header">
              <span class="mds-doc-badge mds-doc-badge--info">${m.type}</span>
              <span class="mds-doc-badge mds-doc-badge--neutral">${m.badge}</span>
            </div>
            <h3 class="mds-doc-card-title">${m.title}</h3>
            <p class="mds-doc-card-body">${m.desc}</p>
          </div>
        `).join('')}
      </div>
    `;
  };

  // --- 7. Theme, Direction, and Density Controllers ---
  window.toggleTheme = function () {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme') || 'light';
    let next = 'dark';
    if (current === 'dark') next = 'high-contrast';
    else if (current === 'high-contrast') next = 'light';
    html.setAttribute('data-theme', next);
    showToast(`Theme switched to: ${next.toUpperCase()}`);
  };

  window.toggleDirection = function () {
    const html = document.documentElement;
    const current = html.getAttribute('dir') || 'rtl';
    const next = current === 'rtl' ? 'ltr' : 'rtl';
    html.setAttribute('dir', next);
    html.setAttribute('lang', next === 'rtl' ? 'ar' : 'en');
    showToast(`Direction switched to: ${next.toUpperCase()}`);
  };

  window.toggleDensity = function () {
    const html = document.documentElement;
    const current = html.getAttribute('data-density') || 'default';
    const next = current === 'default' ? 'compact' : 'default';
    html.setAttribute('data-density', next);
    showToast(`Density set to: ${next.toUpperCase()}`);
  };

  window.toggleSidebar = function () {
    const sidebar = document.getElementById('mds-sidebar');
    if (sidebar) {
      sidebar.classList.toggle('is-open');
    }
  };

  // --- 8. Router Engine ---
  function renderRoute() {
    const hash = window.location.hash.replace(/^#\/?/, '').toLowerCase() || 'overview';
    const main = document.getElementById('main-content');
    if (!main) return;

    // Update active nav class
    document.querySelectorAll('.mds-doc-nav-item').forEach(link => {
      const target = link.getAttribute('href').replace(/^#\/?/, '').toLowerCase();
      if (target === hash) {
        link.classList.add('is-active');
      } else {
        link.classList.remove('is-active');
      }
    });

    if (views[hash]) {
      main.innerHTML = views[hash]();
    } else {
      main.innerHTML = views.overview();
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // --- 9. Initialization ---
  window.addEventListener('hashchange', renderRoute);
  window.addEventListener('DOMContentLoaded', () => {
    // Try fetching external JSON if available; silently fall back to embedded data
    fetch('../Documentation-Index.json')
      .then(res => res.json())
      .then(data => {
        if (data && data.catalog) {
          systemData.components = data.catalog.components || systemData.components;
          systemData.patterns = data.catalog.patterns || systemData.patterns;
          systemData.workflows = data.catalog.workflows || systemData.workflows;
          systemData.templates = data.catalog.templates || systemData.templates;
        }
      })
      .catch(() => {
        // Silently preserve offline EMBEDDED_INDEX
      })
      .finally(() => {
        renderRoute();
      });

    // Keyboard shortcut (Cmd+K / Ctrl+K)
    window.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.getElementById('global-search-input');
        if (searchInput) searchInput.focus();
      }
    });
  });

})();
