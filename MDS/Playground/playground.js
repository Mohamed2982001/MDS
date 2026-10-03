/**
 * MDS (Master Design System) — Reference Runtime Laboratory Controller
 * Architecture Layer: Layer 13 / Phase 9.5 (Reference Runtime Laboratory)
 * Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
 *
 * Laws:
 * 1. Zero external framework dependencies — pure Modern JavaScript (ES Modules).
 * 2. Shared-Core Law: Consumes MDS Runtime directly without modifying runtime sources.
 * 3. 100% Deterministic state management.
 */

// Import Core MDS Interactive Custom Elements
import { MdsSwitch, MdsTabs, MdsDialog, MdsTooltip } from "../Runtime/components/components.js";

class MDSPlayground {
  constructor() {
    this.tokens = [];
    this.activeCategory = "all";
    this.searchQuery = "";
    
    // FSM State Topology
    this.fsmStates = [
      "IDLE",
      "ACTIVE_INPUT",
      "VALIDATING",
      "CONFIRMING",
      "PROCESSING",
      "STREAMING",
      "SUCCESS_RESOLVED",
      "ERROR_INTERCEPTED"
    ];
    this.currentFsmIndex = 0;
  }

  async init() {
    this._initRouter();
    this._initGlobalControls();
    this._initComponentsSpecimens();
    this._initStateLaboratory();
    this._initResponsiveSimulator();
    this._initAccessibilityInspector();
    await this._loadSampleData();
    await this._loadTokens();
  }

  // =========================================================================
  // 1. Router & Section Navigation
  // =========================================================================
  _initRouter() {
    const navLinks = document.querySelectorAll(".mds-pg-nav-link");
    const sections = document.querySelectorAll(".mds-pg-section");

    const navigateTo = (targetId) => {
      const cleanId = targetId.replace(/^#/, "").replace(/^sec-/, "");
      const targetSection = document.getElementById(`sec-${cleanId}`) || document.getElementById("sec-overview");
      
      sections.forEach(sec => sec.classList.remove("is-active"));
      navLinks.forEach(link => link.classList.remove("is-active"));

      if (targetSection) {
        targetSection.classList.add("is-active");
        const activeLink = document.querySelector(`.mds-pg-nav-link[data-section="${cleanId}"]`);
        if (activeLink) {
          activeLink.classList.add("is-active");
        }
      }
    };

    // Listen to hash changes
    window.addEventListener("hashchange", () => {
      navigateTo(window.location.hash || "overview");
    });

    // Handle initial navigation
    navigateTo(window.location.hash || "overview");

    // Click handler for sidebar links
    navLinks.forEach(link => {
      link.addEventListener("click", (e) => {
        const sectionId = link.getAttribute("data-section");
        if (sectionId) {
          window.location.hash = sectionId;
        }
      });
    });
  }

  // =========================================================================
  // 2. Global Controls (Theme, Preset, Density, Direction, Motion)
  // =========================================================================
  _initGlobalControls() {
    const themeSelect = document.getElementById("ctrl-theme");
    const presetSelect = document.getElementById("ctrl-preset");
    const densitySelect = document.getElementById("ctrl-density");
    const dirSelect = document.getElementById("ctrl-dir");
    const motionBtn = document.getElementById("ctrl-motion-toggle");

    if (themeSelect) {
      themeSelect.addEventListener("change", (e) => {
        const mode = e.target.value;
        document.documentElement.setAttribute("data-theme", mode);
        document.documentElement.setAttribute("data-mode", mode);
      });
    }

    if (presetSelect) {
      presetSelect.addEventListener("change", (e) => {
        document.documentElement.setAttribute("data-preset", e.target.value);
      });
    }

    if (densitySelect) {
      densitySelect.addEventListener("change", (e) => {
        document.documentElement.setAttribute("data-density", e.target.value);
      });
    }

    if (dirSelect) {
      dirSelect.addEventListener("change", (e) => {
        const dir = e.target.value;
        document.documentElement.setAttribute("dir", dir);
        document.documentElement.setAttribute("lang", dir === "rtl" ? "ar" : "en");
      });
    }

    if (motionBtn) {
      motionBtn.addEventListener("click", () => {
        const isReduced = document.body.classList.toggle("mds-simulate-reduced-motion");
        motionBtn.classList.toggle("is-active", isReduced);
        motionBtn.setAttribute("aria-pressed", isReduced ? "true" : "false");
      });
    }
  }

  // =========================================================================
  // 3. Components Specimen Wiring
  // =========================================================================
  _initComponentsSpecimens() {
    // Button Loading State Toggle
    const btnToggleLoading = document.getElementById("btn-toggle-loading");
    const primaryDemoBtn = document.getElementById("btn-demo-primary");
    let isLoading = false;

    if (btnToggleLoading && primaryDemoBtn) {
      btnToggleLoading.addEventListener("click", () => {
        isLoading = !isLoading;
        if (isLoading) {
          primaryDemoBtn.dataset.originalText = primaryDemoBtn.innerHTML;
          primaryDemoBtn.innerHTML = `
            <span class="mds-spinner mds-spinner--sm" style="display: inline-block; vertical-align: middle; margin-inline-end: 6px;"></span>
            <span>جاري المعالجة...</span>
          `;
          primaryDemoBtn.setAttribute("aria-busy", "true");
          btnToggleLoading.textContent = "إلغاء التحميل";
        } else {
          primaryDemoBtn.innerHTML = primaryDemoBtn.dataset.originalText || "زر أساسي";
          primaryDemoBtn.removeAttribute("aria-busy");
          btnToggleLoading.textContent = "تبديل التحميل (Loading)";
        }
      });
    }

    // Dialog Modal Trigger & Actions
    const openDialogBtn = document.getElementById("btn-open-dialog");
    const demoDialog = document.getElementById("demo-dialog");

    if (openDialogBtn && demoDialog) {
      openDialogBtn.addEventListener("click", () => {
        demoDialog.removeAttribute("hidden");
        demoDialog.open(openDialogBtn);
      });

      demoDialog.querySelectorAll("[data-dialog-close], [data-dialog-cancel]").forEach(btn => {
        btn.addEventListener("click", () => {
          demoDialog.close();
          demoDialog.setAttribute("hidden", "");
        });
      });

      const confirmBtn = demoDialog.querySelector("[data-dialog-confirm]");
      if (confirmBtn) {
        confirmBtn.addEventListener("click", () => {
          alert("تم تأكيد الإجراء بنجاح في بيئة المختبر.");
          demoDialog.close();
          demoDialog.setAttribute("hidden", "");
        });
      }
    }
  }

  // =========================================================================
  // 4. State Machine Laboratory
  // =========================================================================
  _initStateLaboratory() {
    const badge = document.getElementById("fsm-current-state-badge");
    const timelineNodes = document.querySelectorAll("#fsm-timeline .mds-pg-state-node");
    const prevBtn = document.getElementById("btn-fsm-prev");
    const nextBtn = document.getElementById("btn-fsm-next");
    const resetBtn = document.getElementById("btn-fsm-reset");
    const startInputBtn = document.getElementById("btn-fsm-start-input");

    const views = {
      IDLE: document.getElementById("fsm-view-idle"),
      ACTIVE_INPUT: document.getElementById("fsm-view-input"),
      VALIDATING: document.getElementById("fsm-view-validating"),
      CONFIRMING: document.getElementById("fsm-view-input"),
      PROCESSING: document.getElementById("fsm-view-processing"),
      STREAMING: document.getElementById("fsm-view-streaming"),
      SUCCESS_RESOLVED: document.getElementById("fsm-view-success"),
      ERROR_INTERCEPTED: document.getElementById("fsm-view-error")
    };

    const updateFSM = (index) => {
      this.currentFsmIndex = Math.max(0, Math.min(index, this.fsmStates.length - 1));
      const stateName = this.fsmStates[this.currentFsmIndex];

      if (badge) {
        badge.textContent = stateName;
        badge.className = "mds-badge";
        if (stateName === "SUCCESS_RESOLVED") {
          badge.classList.add("mds-badge--success");
        } else if (stateName === "ERROR_INTERCEPTED") {
          badge.classList.add("mds-badge--danger");
        } else {
          badge.classList.add("mds-badge--brand");
        }
      }

      // Update timeline highlighting
      timelineNodes.forEach((node, i) => {
        if (i === this.currentFsmIndex) {
          node.classList.add("is-active");
        } else {
          node.classList.remove("is-active");
        }
      });

      // Update Views
      Object.keys(views).forEach(key => {
        if (views[key]) {
          views[key].hidden = key !== stateName;
        }
      });
    };

    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        updateFSM((this.currentFsmIndex + 1) % this.fsmStates.length);
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        updateFSM((this.currentFsmIndex - 1 + this.fsmStates.length) % this.fsmStates.length);
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener("click", () => {
        updateFSM(0);
      });
    }

    if (startInputBtn) {
      startInputBtn.addEventListener("click", () => {
        updateFSM(1); // Go to ACTIVE_INPUT
      });
    }

    // Click on timeline nodes
    timelineNodes.forEach((node, idx) => {
      node.style.cursor = "pointer";
      node.addEventListener("click", () => updateFSM(idx));
    });
  }

  // =========================================================================
  // 5. Responsive Simulator
  // =========================================================================
  _initResponsiveSimulator() {
    const container = document.getElementById("vp-container");
    const buttons = document.querySelectorAll(".mds-pg-viewport-simulator [data-vp]");

    if (!container || buttons.length === 0) return;

    buttons.forEach(btn => {
      btn.addEventListener("click", () => {
        const vp = btn.getAttribute("data-vp");
        if (vp === "100%") {
          container.style.inlineSize = "100%";
        } else {
          container.style.inlineSize = `${vp}px`;
        }
        buttons.forEach(b => b.classList.remove("mds-button--primary"));
        buttons.forEach(b => b.classList.add("mds-button--secondary"));
        btn.classList.remove("mds-button--secondary");
        btn.classList.add("mds-button--primary");
      });
    });
  }

  // =========================================================================
  // 6. Accessibility Live Inspector
  // =========================================================================
  _initAccessibilityInspector() {
    const politeBtn = document.getElementById("btn-test-announce-polite");
    const assertiveBtn = document.getElementById("btn-test-announce-assertive");
    const liveAnnouncer = document.getElementById("live-announcer");
    const log = document.getElementById("live-announcer-log");

    const announce = (message, mode) => {
      if (!liveAnnouncer) return;
      liveAnnouncer.setAttribute("aria-live", mode);
      liveAnnouncer.textContent = "";
      setTimeout(() => {
        liveAnnouncer.textContent = message;
        if (log) {
          log.innerHTML = `<strong>تم الإعلان (${mode}):</strong> ${message} <span style="opacity: 0.6;">[${new Date().toLocaleTimeString()}]</span>`;
        }
      }, 50);
    };

    if (politeBtn) {
      politeBtn.addEventListener("click", () => {
        announce("تم تحديث قائمة البيانات بنجاح في الخلفية.", "polite");
      });
    }

    if (assertiveBtn) {
      assertiveBtn.addEventListener("click", () => {
        announce("تنبيه أمني عاجل: تم اكتشاف محاولة تسجيل دخول غير مصرح بها!", "assertive");
      });
    }
  }

  // =========================================================================
  // 7. Dynamic Sample Data (Table & Cards)
  // =========================================================================
  async _loadSampleData() {
    try {
      const response = await fetch("./fixtures/sample_data.json");
      if (!response.ok) return;
      const data = await response.json();
      
      const tbody = document.getElementById("demo-table-body");
      if (tbody && data.transactions && data.transactions.length > 0) {
        tbody.innerHTML = data.transactions.map(item => `
          <tr>
            <td class="mds-text--code">${item.id}</td>
            <td>${item.client}</td>
            <td>${item.date}</td>
            <td>
              <span class="mds-badge mds-badge--${item.status === 'ناجحة' ? 'success' : item.status === 'قيد المعالجة' ? 'brand' : 'warning'}">
                ${item.status}
              </span>
            </td>
            <td class="mds-text--numeric" style="text-align: end;">${item.amount}</td>
          </tr>
        `).join("");
      }
    } catch (err) {
      console.warn("Sample data loading skipped or running in file:// protocol:", err);
    }
  }

  // =========================================================================
  // 8. Token Inspector (W3C DTCG Token Browser)
  // =========================================================================
  async _loadTokens() {
    const tableBody = document.getElementById("token-table-body");
    const searchInput = document.getElementById("token-search-input");
    const categoryChips = document.querySelectorAll("#token-category-chips [data-cat]");

    if (!tableBody) return;

    try {
      const response = await fetch("../Runtime/tokens/dist/tokens.json");
      if (!response.ok) throw new Error("tokens.json fetch failed");
      const data = await response.json();
      
      this.tokens = this._flattenDtcgTokens(data);
      this._renderTokenTable();

      // Search event
      if (searchInput) {
        searchInput.addEventListener("input", (e) => {
          this.searchQuery = e.target.value.toLowerCase().trim();
          this._renderTokenTable();
        });
      }

      // Category filter events
      categoryChips.forEach(chip => {
        chip.addEventListener("click", () => {
          categoryChips.forEach(c => {
            c.classList.remove("mds-badge--brand");
            c.classList.add("mds-badge--neutral");
          });
          chip.classList.remove("mds-badge--neutral");
          chip.classList.add("mds-badge--brand");
          this.activeCategory = chip.getAttribute("data-cat");
          this._renderTokenTable();
        });
      });

    } catch (err) {
      console.warn("Token dist loading fallback:", err);
      tableBody.innerHTML = `
        <tr>
          <td colspan="5" style="text-align: center; padding: 24px;">
            <div class="mds-text mds-text--secondary">
              لم يتم تحميل tokens.json مباشرة (قد يكون بسبب متصفح محلي بدون HTTP Server).
              يتم استهلاك ملف CSS المترجم مباشرة من <code>tokens.css</code> في نظام النواة.
            </div>
          </td>
        </tr>
      `;
    }
  }

  _flattenDtcgTokens(obj, prefix = "") {
    let result = [];
    for (const [key, val] of Object.entries(obj)) {
      if (key.startsWith("$")) continue;
      const currentPath = prefix ? `${prefix}.${key}` : key;
      if (val && typeof val === "object") {
        if ("$value" in val) {
          // Token leaf
          const cssVar = `--mds-${currentPath.replace(/\./g, "-")}`;
          result.push({
            name: currentPath,
            cssVar: cssVar,
            type: val.$type || "dimension",
            value: String(val.$value),
            description: val.$description || ""
          });
        }
        result = result.concat(this._flattenDtcgTokens(val, currentPath));
      }
    }
    return result;
  }

  _renderTokenTable() {
    const tableBody = document.getElementById("token-table-body");
    if (!tableBody) return;

    const filtered = this.tokens.filter(t => {
      const matchesCategory = this.activeCategory === "all" || t.name.startsWith(this.activeCategory);
      const matchesSearch = !this.searchQuery || 
        t.name.toLowerCase().includes(this.searchQuery) || 
        t.cssVar.toLowerCase().includes(this.searchQuery) ||
        t.value.toLowerCase().includes(this.searchQuery);
      return matchesCategory && matchesSearch;
    });

    if (filtered.length === 0) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="5" style="text-align: center; padding: 24px; color: var(--mds-color-text-secondary);">
            لا توجد توكنز مطابقة لبحثك.
          </td>
        </tr>
      `;
      return;
    }

    tableBody.innerHTML = filtered.slice(0, 100).map(t => {
      let preview = "";
      if (t.name.includes("color") || t.value.startsWith("#") || t.value.startsWith("rgb")) {
        preview = `<span class="mds-pg-swatch" style="background: var(${t.cssVar}, ${t.value}); margin-inline-end: 6px;"></span>`;
      } else if (t.name.includes("radius")) {
        preview = `<span style="display:inline-block; inline-size:18px; block-size:18px; border:1px solid var(--mds-color-brand-600); border-radius: var(${t.cssVar}); margin-inline-end: 6px;"></span>`;
      }

      return `
        <tr>
          <td>
            <div class="mds-inline" style="align-items: center;">
              ${preview}
              <div>
                <strong>${t.name}</strong>
                ${t.description ? `<span class="mds-text mds-text--xs mds-text--secondary" style="display: block;">${t.description}</span>` : ""}
              </div>
            </div>
          </td>
          <td><span class="mds-badge mds-badge--neutral mds-badge--sm">${t.type}</span></td>
          <td><code class="mds-pg-token-code">${t.value}</code></td>
          <td><code class="mds-pg-token-code">${t.cssVar}</code></td>
          <td style="text-align: end;">
            <button type="button" class="mds-button mds-button--secondary mds-button--sm" data-copy="var(${t.cssVar})">
              نسخ
            </button>
          </td>
        </tr>
      `;
    }).join("");

    // Attach copy handlers
    tableBody.querySelectorAll("[data-copy]").forEach(btn => {
      btn.addEventListener("click", () => {
        const text = btn.getAttribute("data-copy");
        navigator.clipboard.writeText(text).then(() => {
          const original = btn.textContent;
          btn.textContent = "تم النسخ ✓";
          btn.classList.remove("mds-button--secondary");
          btn.classList.add("mds-button--primary");
          setTimeout(() => {
            btn.textContent = original;
            btn.classList.remove("mds-button--primary");
            btn.classList.add("mds-button--secondary");
          }, 1500);
        }).catch(() => {
          prompt("انسخ المتغير يدوياً:", text);
        });
      });
    });
  }
}

// Initialize Playground on DOM ready
document.addEventListener("DOMContentLoaded", () => {
  const lab = new MDSPlayground();
  lab.init();
});
