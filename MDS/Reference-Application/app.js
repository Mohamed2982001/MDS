/**
 * MASTER DESIGN SYSTEM (MDS) — REFERENCE APPLICATION CONTROLLER
 * Application: MDS Workspace
 * Standard: Pure ECMAScript Modules (ESM), Zero NPM Dependencies.
 */

import { MdsSwitch, MdsTabs, MdsDialog, MdsTooltip } from "../Runtime/components/components.js";

class ReferenceApp {
  constructor() {
    this.state = {
      currentRoute: window.location.hash || "#/overview",
      currentRole: "Administrator", // Administrator | Manager | Reviewer | User
      currentTheme: "light",
      currentPreset: "soft",
      currentDensity: "comfortable",
      currentDirection: "rtl",
      simulatedState: "normal", // normal | loading | error | empty | permission_denied
      selectedItemId: "ITM-101",
      searchQuery: "",
      itemsTab: "all", // all | favorites | archived
      tasksFilter: "ALL", // ALL | IN_PROGRESS | REVIEW | DONE
      isDirty: false,
      aiState: "IDLE", // IDLE | PROCESSING | STREAMING | REVIEWING | SUCCESS_RESOLVED
      aiStreamBuffer: "",
      aiActivePromptIndex: 0,
      itemEditStep: 1,
      itemEditStep2Unlocked: false,
      data: null
    };

    this.mainContainer = null;
    this.toastShelf = null;
  }

  async init() {
    this.mainContainer = document.getElementById("ref-app-main");
    this.toastShelf = document.getElementById("ref-toast-shelf");

    // Load deterministic fixtures
    await this._loadData();

    // Bind global header controls & router
    this._bindHeaderControls();
    this._bindSimulationBar();
    this._initRouter();

    // Initial render
    this.render();
  }

  async _loadData() {
    try {
      const resp = await fetch("./fixtures/workspace_data.json");
      if (resp.ok) {
        this.state.data = await resp.json();
      }
    } catch (e) {
      console.warn("Using inline fallback mock data:", e);
    }
  }

  _bindHeaderControls() {
    // Role switcher
    const roleSelect = document.getElementById("ctrl-ref-role");
    if (roleSelect) {
      roleSelect.value = this.state.currentRole;
      roleSelect.addEventListener("change", (e) => {
        this.state.currentRole = e.target.value;
        this.showToast(`تم تبديل الدور إلى: ${this.state.currentRole}`, "info");
        this.render();
      });
    }

    // Theme switcher
    const themeSelect = document.getElementById("ctrl-ref-theme");
    if (themeSelect) {
      themeSelect.addEventListener("change", (e) => {
        this.setTheme(e.target.value);
      });
    }

    // Preset switcher
    const presetSelect = document.getElementById("ctrl-ref-preset");
    if (presetSelect) {
      presetSelect.addEventListener("change", (e) => {
        this.setPreset(e.target.value);
      });
    }

    // Density switcher
    const densitySelect = document.getElementById("ctrl-ref-density");
    if (densitySelect) {
      densitySelect.addEventListener("change", (e) => {
        this.setDensity(e.target.value);
      });
    }

    // Direction switcher
    const dirSelect = document.getElementById("ctrl-ref-dir");
    if (dirSelect) {
      dirSelect.addEventListener("change", (e) => {
        this.setDirection(e.target.value);
      });
    }

    // Mobile navigation drawer trigger (Composed via <mds-dialog> — R-003)
    const mobileBtn = document.getElementById("btn-mobile-nav");
    const navDialog = document.getElementById("dialog-mobile-nav");
    const closeMobileNavBtn = document.getElementById("btn-close-mobile-nav");
    if (mobileBtn && navDialog) {
      mobileBtn.addEventListener("click", () => {
        if (typeof navDialog.open === "function") {
          navDialog.open(mobileBtn);
        }
      });
      if (closeMobileNavBtn) {
        closeMobileNavBtn.addEventListener("click", () => {
          if (typeof navDialog.close === "function") {
            navDialog.close();
          }
        });
      }
      navDialog.querySelectorAll("a").forEach(a => {
        a.addEventListener("click", () => {
          if (typeof navDialog.close === "function") {
            navDialog.close();
          }
        });
      });
    }
  }

  _bindSimulationBar() {
    const simSelect = document.getElementById("ctrl-ref-sim-state");
    if (simSelect) {
      simSelect.addEventListener("change", (e) => {
        this.state.simulatedState = e.target.value;
        this.showToast(`تم تطبيق حالة المحاكاة: ${this.state.simulatedState}`, "warning");
        this.render();
      });
    }
  }

  _initRouter() {
    window.addEventListener("hashchange", () => {
      this.state.currentRoute = window.location.hash || "#/overview";
      // Close mobile navigation dialog on navigate if open
      const navDialog = document.getElementById("dialog-mobile-nav");
      if (navDialog && navDialog.isOpen && typeof navDialog.close === "function") {
        navDialog.close();
      }
      // Reset item edit stepper if entering edit screen
      if (this.state.currentRoute === "#/items/edit") {
        this.state.itemEditStep = 1;
        this.state.itemEditStep2Unlocked = false;
      }
      this.render();
    });
  }

  setTheme(theme) {
    this.state.currentTheme = theme;
    document.documentElement.setAttribute("data-theme", theme);
    document.documentElement.setAttribute("data-mode", theme);
  }

  setPreset(preset) {
    this.state.currentPreset = preset;
    document.documentElement.setAttribute("data-preset", preset);
  }

  setDensity(density) {
    this.state.currentDensity = density;
    document.documentElement.setAttribute("data-density", density);
  }

  setDirection(dir) {
    this.state.currentDirection = dir;
    document.documentElement.setAttribute("dir", dir);
    document.documentElement.setAttribute("lang", dir === "rtl" ? "ar" : "en");
  }

  showToast(message, intent = "info") {
    if (!this.toastShelf) return;
    const toast = document.createElement("div");
    toast.className = `mds-alert mds-alert--${intent}`;
    toast.setAttribute("role", "status");
    toast.innerHTML = `
      <div class="mds-alert__content">
        <div class="mds-alert__title">${message}</div>
      </div>
    `;
    this.toastShelf.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transition = "opacity 0.25s ease";
      setTimeout(() => toast.remove(), 250);
    }, 3500);
  }

  // =========================================================================
  // Screen Dispatcher
  // =========================================================================
  render() {
    if (!this.mainContainer || !this.state.data) return;

    // Update active nav links
    document.querySelectorAll(".mds-ref-nav-item").forEach(link => {
      const href = link.getAttribute("href");
      if (href === this.state.currentRoute || (href !== "#/overview" && this.state.currentRoute.startsWith(href))) {
        link.classList.add("is-active");
        link.setAttribute("aria-current", "page");
      } else {
        link.classList.remove("is-active");
        link.removeAttribute("aria-current");
      }
    });

    const route = this.state.currentRoute;

    // Route dispatch
    if (route === "#/overview" || route === "") {
      this._renderOverview();
    } else if (route === "#/items") {
      this._renderItemsList();
    } else if (route.startsWith("#/items/detail")) {
      this._renderItemDetail();
    } else if (route.startsWith("#/items/edit")) {
      this._renderItemEdit();
    } else if (route === "#/tasks") {
      this._renderTasks();
    } else if (route === "#/ai-workspace") {
      this._renderAIWorkspace();
    } else if (route === "#/activity") {
      this._renderActivity();
    } else if (route.startsWith("#/settings")) {
      this._renderSettings();
    } else {
      this._renderNotFound();
    }
  }

  // =========================================================================
  // Screen 1: Dashboard Overview (MDS-TMP-001)
  // =========================================================================
  _renderOverview() {
    if (this.state.simulatedState === "loading") {
      this.mainContainer.innerHTML = `
        <div class="mds-ref-page-header">
          <div class="mds-skeleton mds-skeleton--text" style="inline-size: 200px; block-size: 32px;"></div>
          <div class="mds-skeleton mds-skeleton--text" style="inline-size: 320px; block-size: 16px;"></div>
        </div>
        <div class="mds-ref-stats-grid">
          ${[1, 2, 3, 4].map(() => `
            <div class="mds-card mds-card--raised" style="padding: 24px;">
              <div class="mds-skeleton mds-skeleton--text" style="inline-size: 60%; margin-block-end: 12px;"></div>
              <div class="mds-skeleton mds-skeleton--text" style="inline-size: 40%; block-size: 28px;"></div>
            </div>
          `).join("")}
        </div>
      `;
      return;
    }

    if (this.state.simulatedState === "error") {
      this.mainContainer.innerHTML = `
        <div class="mds-alert mds-alert--danger" role="alert">
          <div class="mds-alert__content">
            <div class="mds-alert__title">فشل تحميل بيانات لوحة القيادة</div>
            <div class="mds-alert__description">تعذر الاتصال بمزود البيانات التشغيلي (Simulation Mode).</div>
            <div style="margin-block-start: 12px;">
              <button type="button" class="mds-button mds-button--secondary mds-button--sm" id="btn-retry-overview">
                إعادة المحاولة (Retry)
              </button>
            </div>
          </div>
        </div>
      `;
      document.getElementById("btn-retry-overview")?.addEventListener("click", () => {
        this.state.simulatedState = "normal";
        const simSelect = document.getElementById("ctrl-ref-sim-state");
        if (simSelect) simSelect.value = "normal";
        this.render();
      });
      return;
    }

    const items = this.state.data.items;
    const tasks = this.state.data.tasks;
    const activities = this.state.data.activities;

    this.mainContainer.innerHTML = `
      <!-- Page-Header Pattern -->
      <div class="mds-ref-page-header">
        <div class="mds-ref-page-header__row">
          <div>
            <h1 class="mds-ref-page-header__title">نظرة عامة على مساحة العمل</h1>
            <p class="mds-ref-page-header__subtitle">مرحباً بك مجدداً، ${this.state.data.users.find(u => u.role === this.state.currentRole)?.name || "مستخدم"}</p>
          </div>
          <div class="mds-ref-controls-group">
            <span class="mds-badge mds-badge--brand">مساحة عمل مؤسسية</span>
            <a href="#/items/edit" class="mds-button mds-button--primary mds-button--sm">
              <span class="mds-button__label">+ عنصر جديد</span>
            </a>
          </div>
        </div>
      </div>

      <!-- KPI Stat Cards Pattern (Composed) -->
      <div class="mds-ref-stats-grid">
        <div class="mds-ref-stat-card">
          <p class="mds-ref-stat-card__title">إجمالي العناصر النشطة</p>
          <p class="mds-ref-stat-card__value">${items.filter(i => !i.isArchived).length}</p>
          <div class="mds-ref-stat-card__footer">
            <span class="mds-badge mds-badge--success">+12% نمو تشغيلي</span>
            <span>هذا الشهر</span>
          </div>
        </div>
        <div class="mds-ref-stat-card">
          <p class="mds-ref-stat-card__title">المهام قيد التنفيذ</p>
          <p class="mds-ref-stat-card__value">${tasks.filter(t => t.status === "IN_PROGRESS").length}</p>
          <div class="mds-ref-stat-card__footer">
            <span class="mds-badge mds-badge--warning">${tasks.filter(t => t.priority === "critical").length} ذات أولوية قصوى</span>
            <span>تتطلب إجراءً</span>
          </div>
        </div>
        <div class="mds-ref-stat-card">
          <p class="mds-ref-stat-card__title">وفر ساعات الذكاء الاصطناعي</p>
          <p class="mds-ref-stat-card__value">148.5 س</p>
          <div class="mds-ref-stat-card__footer">
            <span class="mds-badge mds-badge--brand">98.4% دقة</span>
            <span>معتمدة بشرياً</span>
          </div>
        </div>
        <div class="mds-ref-stat-card">
          <p class="mds-ref-stat-card__title">درجة التوافق المعماري</p>
          <p class="mds-ref-stat-card__value">100%</p>
          <div class="mds-ref-stat-card__footer">
            <span class="mds-badge mds-badge--success">WCAG AAA</span>
            <span>MDS Baseline</span>
          </div>
        </div>
      </div>

      <!-- Split Layout: Recent Tasks & Activity -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: var(--mds-space-inline-lg);">
        
        <!-- Left: Priority Tasks (Data-List-Card Pattern) -->
        <div class="mds-card mds-card--raised" style="padding: var(--mds-space-scale-5);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-block-end: var(--mds-space-block-md);">
            <h2 style="margin:0; font-size: var(--mds-font-size-lg);">أولويات العمل العاجلة</h2>
            <a href="#/tasks" class="mds-link mds-link--subtle">عرض الكل ←</a>
          </div>
          <div style="display: flex; flex-direction: column; gap: var(--mds-space-block-sm);">
            ${tasks.slice(0, 3).map(t => `
              <div class="mds-card" style="padding: var(--mds-space-scale-3); border: 1px solid var(--mds-color-border-subtle);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px;">
                  <div style="font-weight: var(--mds-font-weight-medium);">${t.title}</div>
                  <span class="mds-badge mds-badge--${t.priority === 'critical' ? 'danger' : 'brand'}">${t.priority}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-block-start: 8px; font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">
                  <span>المسؤول: ${t.assignee}</span>
                  <span class="mds-text--numeric">الاستحقاق: ${t.dueDate}</span>
                </div>
              </div>
            `).join("")}
          </div>
        </div>

        <!-- Right: Recent Activity -->
        <div class="mds-card mds-card--raised" style="padding: var(--mds-space-scale-5);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-block-end: var(--mds-space-block-md);">
            <h2 style="margin:0; font-size: var(--mds-font-size-lg);">سجل النشاط المباشر</h2>
            <a href="#/activity" class="mds-link mds-link--subtle">السجل الكامل ←</a>
          </div>
          <ul class="mds-ref-timeline">
            ${activities.slice(0, 3).map(a => `
              <li class="mds-ref-timeline-item">
                <div class="mds-ref-timeline-avatar">${a.avatar}</div>
                <div>
                  <div style="font-size: var(--mds-font-size-sm); font-weight: var(--mds-font-weight-medium);">${a.actor} ${a.action}</div>
                  <div style="font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">${a.timestamp}</div>
                </div>
              </li>
            `).join("")}
          </ul>
        </div>
      </div>
    `;
  }

  // =========================================================================
  // Screen 2: Items — List Management (MDS-TMP-002)
  // =========================================================================
  _renderItemsList() {
    if (this.state.simulatedState === "empty") {
      this._renderEmptyState("لا توجد عناصر في مساحة العمل", "تم تفعيل وضع القائمة الفارغة لمحاكاة تجربة الاستخدام.", "#/items/edit");
      return;
    }

    let items = this.state.data.items;
    
    // Tab filter
    if (this.state.itemsTab === "favorites") {
      items = items.filter(i => i.isFavorite && !i.isArchived);
    } else if (this.state.itemsTab === "archived") {
      items = items.filter(i => i.isArchived);
    } else {
      items = items.filter(i => !i.isArchived);
    }

    // Search query filter
    if (this.state.searchQuery) {
      const q = this.state.searchQuery.toLowerCase();
      items = items.filter(i => i.title.toLowerCase().includes(q) || i.category.toLowerCase().includes(q) || i.id.toLowerCase().includes(q));
    }

    this.mainContainer.innerHTML = `
      <div class="mds-ref-page-header">
        <div class="mds-ref-page-header__row">
          <div>
            <h1 class="mds-ref-page-header__title">إدارة عناصر ومشاريع العمل</h1>
            <p class="mds-ref-page-header__subtitle">استعراض وتصفية كافة السجلات التشغيلية ومتابعة الميزانيات والحالات</p>
          </div>
          <a href="#/items/edit" class="mds-button mds-button--primary mds-button--sm">
            <span class="mds-button__label">+ إنشاء عنصر</span>
          </a>
        </div>
      </div>

      <!-- Navigation Tabs (MdsTabs) -->
      <mds-tabs id="tabs-items">
        <div role="tablist" class="mds-tabs__list">
          <button type="button" role="tab" class="mds-tabs__tab ${this.state.itemsTab === 'all' ? 'is-active' : ''}" data-tab="all">
            كافة العناصر (${this.state.data.items.filter(i => !i.isArchived).length})
          </button>
          <button type="button" role="tab" class="mds-tabs__tab ${this.state.itemsTab === 'favorites' ? 'is-active' : ''}" data-tab="favorites">
            المفضلة (${this.state.data.items.filter(i => i.isFavorite && !i.isArchived).length})
          </button>
          <button type="button" role="tab" class="mds-tabs__tab ${this.state.itemsTab === 'archived' ? 'is-active' : ''}" data-tab="archived">
            المؤرشفة (${this.state.data.items.filter(i => i.isArchived).length})
          </button>
        </div>
      </mds-tabs>

      <!-- Search-Filter-Bar Pattern -->
      <div class="mds-ref-search-filter-bar">
        <div class="mds-ref-search-filter-bar__inputs">
          <input type="search" id="input-search-items" class="mds-input mds-input--sm" placeholder="ابحث بالاسم، الفئة، أو المعرّف..." value="${this.state.searchQuery}" style="inline-size: 260px;">
          <select id="select-category-filter" class="mds-select mds-select--sm" style="inline-size: 160px;">
            <option value="">كافة الفئات</option>
            <option value="Engineering">Engineering</option>
            <option value="Architecture">Architecture</option>
            <option value="Compliance">Compliance</option>
            <option value="AI">AI</option>
          </select>
        </div>
        <div style="font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">
          عرض <strong>${items.length}</strong> سجل
        </div>
      </div>

      <!-- Data Table with Focusable Container (AF-002) -->
      <div class="mds-table-container" tabindex="0" role="region" aria-label="جدول عناصر ومشاريع مساحة العمل">
        <table class="mds-table mds-table--striped">
          <thead>
            <tr>
              <th style="inline-size: 90px;">المعرف</th>
              <th>عنوان العنصر</th>
              <th>الفئة</th>
              <th>الأولوية</th>
              <th>المسؤول</th>
              <th style="text-align: end;">الميزانية (ج.م)</th>
              <th style="text-align: center; inline-size: 100px;">الإجراءات</th>
            </tr>
          </thead>
          <tbody>
            ${items.length === 0 ? `
              <tr>
                <td colspan="7" style="text-align: center; padding: var(--mds-space-scale-6);">
                  <div class="mds-text mds-text--secondary">لم يتم العثور على سجلات مطابقة لمعايير البحث.</div>
                </td>
              </tr>
            ` : items.map(item => `
              <tr>
                <td class="mds-text--code">${item.id}</td>
                <td>
                  <a href="#/items/detail" class="mds-link ref-item-link" data-id="${item.id}" style="font-weight: var(--mds-font-weight-medium);">
                    ${item.title}
                  </a>
                </td>
                <td><span class="mds-badge mds-badge--neutral">${item.category}</span></td>
                <td>
                  <span class="mds-badge mds-badge--${item.priority === 'critical' ? 'danger' : item.priority === 'high' ? 'warning' : 'brand'}">
                    ${item.priority}
                  </span>
                </td>
                <td>${item.owner}</td>
                <td class="mds-text--numeric" style="text-align: end;">${item.budget}</td>
                <td style="text-align: center;">
                  <div style="display: inline-flex; gap: 4px;">
                    <a href="#/items/edit" class="mds-icon-button mds-icon-button--ghost mds-icon-button--sm ref-item-edit-btn" data-id="${item.id}" aria-label="تعديل ${item.title}">
                      ✎
                    </a>
                  </div>
                </td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>

      <!-- Table Pager Pattern (Composed) -->
      <div class="mds-ref-pager">
        <div>صفحة 1 من 1</div>
        <div style="display: flex; gap: var(--mds-space-inline-xs); align-items: center;">
          <button type="button" class="mds-button mds-button--secondary mds-button--sm" disabled>السابق</button>
          <button type="button" class="mds-button mds-button--secondary mds-button--sm" disabled>التالي</button>
        </div>
      </div>
    `;

    // Bind tab clicks
    document.querySelectorAll("#tabs-items .mds-tabs__tab").forEach(tab => {
      tab.addEventListener("click", () => {
        this.state.itemsTab = tab.getAttribute("data-tab");
        this.render();
      });
    });

    // Bind search input
    const searchInput = document.getElementById("input-search-items");
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        this.state.searchQuery = e.target.value;
        this._renderItemsList();
      });
    }

    // Bind item selection links
    document.querySelectorAll(".ref-item-link, .ref-item-edit-btn").forEach(el => {
      el.addEventListener("click", () => {
        const id = el.getAttribute("data-id");
        if (id) this.state.selectedItemId = id;
      });
    });
  }

  // =========================================================================
  // Screen 3: Item Detail (MDS-TMP-003)
  // =========================================================================
  _renderItemDetail() {
    const item = this.state.data.items.find(i => i.id === this.state.selectedItemId) || this.state.data.items[0];

    this.mainContainer.innerHTML = `
      <div class="mds-ref-page-header">
        <div class="mds-ref-breadcrumbs">
          <a href="#/items" class="mds-link mds-link--subtle">العناصر</a>
          <span>/</span>
          <span class="mds-text--code">${item.id}</span>
        </div>
        <div class="mds-ref-page-header__row">
          <div>
            <h1 class="mds-ref-page-header__title">${item.title}</h1>
            <p class="mds-ref-page-header__subtitle">تم التحديث الأخير في ${item.updated} بواسطة ${item.owner}</p>
          </div>
          <div class="mds-ref-controls-group">
            <a href="#/items/edit" class="mds-button mds-button--secondary mds-button--sm">تعديل البيانات</a>
            <button type="button" id="btn-trigger-delete" class="mds-button mds-button--destructive mds-button--sm">
              حذف العنصر
            </button>
          </div>
        </div>
      </div>

      <!-- Two-Column Master Detail Split -->
      <div style="display: grid; grid-template-columns: 2fr 1fr; gap: var(--mds-space-inline-lg);">
        
        <!-- Main Pane -->
        <div class="mds-card mds-card--raised" style="padding: var(--mds-space-scale-6);">
          <h2 style="margin: 0 0 var(--mds-space-block-sm) 0; font-size: var(--mds-font-size-lg);">وصف المشروع والأهداف</h2>
          <p class="mds-text" style="color: var(--mds-color-text-secondary); line-height: var(--mds-font-line-height-relaxed);">
            ${item.description}
          </p>

          <h3 style="margin-block-start: var(--mds-space-block-lg); font-size: var(--mds-font-size-base);">الوسوم والتصنيفات</h3>
          <div class="mds-cluster" style="margin-block-start: var(--mds-space-block-xs);">
            ${item.tags.map(t => `<span class="mds-badge mds-badge--neutral">#${t}</span>`).join("")}
          </div>
        </div>

        <!-- Sidebar Metadata Pane -->
        <div class="mds-card" style="padding: var(--mds-space-scale-5); border: 1px solid var(--mds-color-border-subtle); display: flex; flex-direction: column; gap: var(--mds-space-block-md);">
          <h3 style="margin: 0; font-size: var(--mds-font-size-sm); color: var(--mds-color-text-secondary);">بيانات الاعتماد والحوكمة</h3>
          <div>
            <div style="font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">المسؤول المباشر</div>
            <div style="font-weight: var(--mds-font-weight-medium);">${item.owner}</div>
          </div>
          <div>
            <div style="font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">مستوى الأولوية</div>
            <span class="mds-badge mds-badge--${item.priority === 'critical' ? 'danger' : 'brand'}">${item.priority}</span>
          </div>
          <div>
            <div style="font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">الميزانية المعتمدة</div>
            <div class="mds-text--numeric" style="font-size: var(--mds-font-size-xl); font-weight: var(--mds-font-weight-bold);">${item.budget} ج.م</div>
          </div>
        </div>
      </div>

      <!-- Destructive Confirmation Modal (AF-002 Cancel-First Focus) -->
      <mds-dialog id="modal-delete-item">
        <div class="mds-dialog__surface">
          <div class="mds-dialog__header">
            <h2 class="mds-dialog__title">تأكيد حذف العنصر نهائياً</h2>
          </div>
          <div class="mds-dialog__body">
            <p class="mds-text">
              هل أنت متأكد من رغبتك في حذف <strong>${item.title}</strong>؟ هذا الإجراء لا يمكن التراجع عنه وسيتم تسجيله في سجل الأمان.
            </p>
          </div>
          <div class="mds-dialog__footer">
            <button type="button" class="mds-button mds-button--secondary" data-dialog-cancel>
              إلغاء الأمر (Cancel)
            </button>
            <button type="button" class="mds-button mds-button--destructive" id="btn-confirm-delete" data-dialog-confirm>
              تأكيد الحذف النهائي
            </button>
          </div>
        </div>
      </mds-dialog>
    `;

    // Bind delete button with Permission Guard
    const delBtn = document.getElementById("btn-trigger-delete");
    const modal = document.getElementById("modal-delete-item");
    if (delBtn && modal) {
      delBtn.addEventListener("click", () => {
        if (this.state.currentRole === "User") {
          this.showToast("عذراً، يتطلب تنفيذ هذا الإجراء صلاحيات مدير (Administrator). [Permission Denied]", "danger");
          return;
        }
        modal.open(delBtn);
      });
    }

    // Bind modal cancel
    const cancelBtn = modal?.querySelector("[data-dialog-cancel]");
    if (cancelBtn && modal) {
      cancelBtn.addEventListener("click", () => {
        modal.close();
      });
    }

    // Bind modal confirm
    const confirmBtn = document.getElementById("btn-confirm-delete");
    if (confirmBtn && modal) {
      confirmBtn.addEventListener("click", () => {
        // Remove item from data
        this.state.data.items = this.state.data.items.filter(i => i.id !== item.id);
        modal.close();
        this.showToast(`تم حذف العنصر ${item.id} بنجاح.`, "success");
        window.location.hash = "#/items";
      });
    }
  }

  // =========================================================================
  // Screen 4: Item Edit (MDS-TMP-004) — Composed Stepper via <mds-tabs> (R-004)
  // =========================================================================
  _renderItemEdit() {
    const item = this.state.data.items.find(i => i.id === this.state.selectedItemId) || this.state.data.items[0];

    this.mainContainer.innerHTML = `
      <div class="mds-ref-page-header">
        <div class="mds-ref-breadcrumbs">
          <a href="#/items" class="mds-link mds-link--subtle">العناصر</a>
          <span>/</span>
          <span>تعديل السجل</span>
        </div>
        <div class="mds-ref-page-header__row">
          <div>
            <h1 class="mds-ref-page-header__title">تعديل بيانات السجل التشغيلي (معالج متعدد الخطوات)</h1>
            <p class="mds-ref-page-header__subtitle">تحرير الحقول والميزانية وإعدادات الإظهار عبر معالج متدرج</p>
          </div>
          <div id="edit-dirty-indicator" style="display: none;">
            <span class="mds-badge mds-badge--warning">تغييرات غير محفوظة</span>
          </div>
        </div>
      </div>

      <form id="form-item-edit" class="mds-stack" style="gap: var(--mds-space-block-lg);">
        
        <!-- Multi-Step Stepper Component Composition (GAP-008 / R-004) -->
        <mds-tabs id="tabs-item-stepper" class="mds-ref-stepper-tabs">
          <div class="mds-tabs__list" role="tablist" aria-label="خطوات تعديل السجل التشغيلي">
            <button type="button" class="mds-tabs__tab mds-ref-stepper-tab ${this.state.itemEditStep === 1 ? 'mds-tabs__tab--active' : ''}" role="tab" id="step-tab-1" aria-controls="step-panel-1" aria-selected="${this.state.itemEditStep === 1 ? 'true' : 'false'}" tabindex="${this.state.itemEditStep === 1 ? '0' : '-1'}">
              <span class="mds-badge mds-badge--brand mds-badge--sm" style="margin-inline-end: 6px;">1</span>
              <span>البيانات الأساسية</span>
            </button>
            <button type="button" class="mds-tabs__tab mds-ref-stepper-tab ${this.state.itemEditStep === 2 ? 'mds-tabs__tab--active' : ''}" role="tab" id="step-tab-2" aria-controls="step-panel-2" aria-selected="${this.state.itemEditStep === 2 ? 'true' : 'false'}" tabindex="${this.state.itemEditStep === 2 ? '0' : '-1'}" ${this.state.itemEditStep2Unlocked ? '' : 'aria-disabled="true"'}>
              <span class="mds-badge ${this.state.itemEditStep2Unlocked ? 'mds-badge--brand' : 'mds-badge--neutral'} mds-badge--sm" style="margin-inline-end: 6px;">2</span>
              <span>خيارات التخصيص والمفضلة ${this.state.itemEditStep2Unlocked ? '' : '🔒'}</span>
            </button>
          </div>

          <!-- Step 1 Panel: Basic Information -->
          <div class="mds-tabs__panel" role="tabpanel" id="step-panel-1" aria-labelledby="step-tab-1" ${this.state.itemEditStep === 1 ? '' : 'hidden'}>
            <div class="mds-ref-form-section">
              <div class="mds-ref-form-section__header">
                <h2 style="margin: 0; font-size: var(--mds-font-size-lg);">الخطوة 1: المعلومات الأساسية</h2>
                <p style="margin: 0; font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">العنوان والفئة والميزانية المعتمدة للمشروع</p>
              </div>

              <div class="mds-field">
                <label class="mds-label" for="edit-title">
                  عنوان المشروع <span class="mds-field__required">*</span>
                </label>
                <input type="text" id="edit-title" class="mds-input" required value="${item.title}">
                <div class="mds-field__helper">أدخل عنواناً واضحاً وموجزاً يصف نطاق العمل.</div>
              </div>

              <div class="mds-ref-form-grid-2">
                <div class="mds-field">
                  <label class="mds-label" for="edit-category">فئة العمل</label>
                  <select id="edit-category" class="mds-select">
                    <option value="Engineering" ${item.category === 'Engineering' ? 'selected' : ''}>Engineering</option>
                    <option value="Architecture" ${item.category === 'Architecture' ? 'selected' : ''}>Architecture</option>
                    <option value="Compliance" ${item.category === 'Compliance' ? 'selected' : ''}>Compliance</option>
                    <option value="AI" ${item.category === 'AI' ? 'selected' : ''}>AI</option>
                  </select>
                </div>
                <div class="mds-field">
                  <label class="mds-label" for="edit-budget">الميزانية (ج.م) <span class="mds-field__required">*</span></label>
                  <input type="text" id="edit-budget" class="mds-input mds-text--numeric" required value="${item.budget}">
                </div>
              </div>

              <div class="mds-field">
                <label class="mds-label" for="edit-desc">الوصف الفني والتفاصيل</label>
                <textarea id="edit-desc" class="mds-textarea" rows="4">${item.description}</textarea>
              </div>

              <!-- Step 1 Controls -->
              <div style="display: flex; gap: var(--mds-space-inline-md); justify-content: flex-end; padding-block-start: var(--mds-space-block-md); border-block-start: 1px solid var(--mds-color-border-subtle); margin-block-start: var(--mds-space-block-md);">
                <a href="#/items/detail" class="mds-button mds-button--secondary">إلغاء الأمر</a>
                <button type="button" class="mds-button mds-button--primary" id="btn-stepper-next">
                  <span class="mds-button__label">التالي: خيارات التخصيص ←</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Step 2 Panel: Preferences & Customization -->
          <div class="mds-tabs__panel" role="tabpanel" id="step-panel-2" aria-labelledby="step-tab-2" ${this.state.itemEditStep === 2 ? '' : 'hidden'}>
            <div class="mds-ref-form-section">
              <div class="mds-ref-form-section__header">
                <h2 style="margin: 0; font-size: var(--mds-font-size-lg);">الخطوة 2: خيارات التخصيص والمفضلة</h2>
                <p style="margin: 0; font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">تفضيلات الإظهار وحفظ السجل في مساحة العمل</p>
              </div>

              <div style="display: flex; align-items: center; justify-content: space-between; padding-block: var(--mds-space-block-md);">
                <div>
                  <div style="font-weight: var(--mds-font-weight-medium);">إضافة للمفضلة السريعة</div>
                  <div style="font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">إظهار هذا العنصر في شاشة النظرة العامة وقائمة المفضلة</div>
                </div>
                <mds-switch id="edit-fav-switch" ${item.isFavorite ? 'checked' : ''}></mds-switch>
              </div>

              <!-- Step 2 Controls -->
              <div style="display: flex; gap: var(--mds-space-inline-md); justify-content: flex-end; padding-block-start: var(--mds-space-block-md); border-block-start: 1px solid var(--mds-color-border-subtle); margin-block-start: var(--mds-space-block-md);">
                <button type="button" class="mds-button mds-button--secondary" id="btn-stepper-prev">
                  <span class="mds-button__label">→ السابق: البيانات الأساسية</span>
                </button>
                <button type="submit" class="mds-button mds-button--primary" id="btn-save-item">
                  <span class="mds-button__label">حفظ التغييرات (Save)</span>
                </button>
              </div>
            </div>
          </div>
        </mds-tabs>
      </form>
    `;

    // Bind form events, validation, and stepper progression
    const form = document.getElementById("form-item-edit");
    const dirtyIndicator = document.getElementById("edit-dirty-indicator");
    const stepperTabs = document.getElementById("tabs-item-stepper");
    const stepTab2 = document.getElementById("step-tab-2");
    const nextBtn = document.getElementById("btn-stepper-next");
    const prevBtn = document.getElementById("btn-stepper-prev");

    if (form) {
      form.addEventListener("input", () => {
        this.state.isDirty = true;
        if (dirtyIndicator) dirtyIndicator.style.display = "block";
      });

      // Guard: direct tab click on Step 2 when locked
      if (stepTab2) {
        stepTab2.addEventListener("click", () => {
          if (!this.state.itemEditStep2Unlocked) {
            this.showToast("يرجى إكمال وتدقيق البيانات الأساسية أولاً قبل الانتقال للخطوة التالية", "warning");
          }
        });
      }

      // Next button: validate Step 1, unlock Step 2, transition
      if (nextBtn && stepperTabs) {
        nextBtn.addEventListener("click", () => {
          const titleInput = document.getElementById("edit-title");
          const budgetInput = document.getElementById("edit-budget");
          const titleVal = titleInput ? titleInput.value.trim() : "";
          const budgetVal = budgetInput ? budgetInput.value.trim() : "";

          if (!titleVal) {
            this.showToast("يرجى إدخال عنوان المشروع للمتابعة", "error");
            titleInput?.focus();
            return;
          }

          if (!budgetVal || isNaN(Number(budgetVal.replace(/[^\d.]/g, "")))) {
            this.showToast("يرجى إدخال ميزانية رقمية صالحة للمتابعة", "error");
            budgetInput?.focus();
            return;
          }

          // Step 1 satisfies validation -> Unlock Step 2
          this.state.itemEditStep2Unlocked = true;
          this.state.itemEditStep = 2;
          if (stepTab2) {
            stepTab2.removeAttribute("aria-disabled");
            stepTab2.innerHTML = `
              <span class="mds-badge mds-badge--brand mds-badge--sm" style="margin-inline-end: 6px;">2</span>
              <span>خيارات التخصيص والمفضلة</span>
            `;
          }
          if (typeof stepperTabs.selectTab === "function") {
            stepperTabs.selectTab(1);
          }
          this.showToast("تم التحقق من البيانات الأساسية والانتقال للخطوة 2", "info");
        });
      }

      // Previous button: return to Step 1
      if (prevBtn && stepperTabs) {
        prevBtn.addEventListener("click", () => {
          this.state.itemEditStep = 1;
          if (typeof stepperTabs.selectTab === "function") {
            stepperTabs.selectTab(0);
          }
        });
      }

      // Stepper tab change listener
      if (stepperTabs) {
        stepperTabs.addEventListener("change", (e) => {
          this.state.itemEditStep = e.detail.selectedIndex + 1;
        });
      }

      // Save Form Submit
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        const saveBtn = document.getElementById("btn-save-item");
        if (saveBtn) {
          saveBtn.classList.add("is-loading");
          saveBtn.setAttribute("aria-busy", "true");
        }

        setTimeout(() => {
          item.title = document.getElementById("edit-title")?.value || item.title;
          item.category = document.getElementById("edit-category")?.value || item.category;
          item.budget = document.getElementById("edit-budget")?.value || item.budget;
          item.description = document.getElementById("edit-desc")?.value || item.description;
          const favSwitch = document.getElementById("edit-fav-switch");
          if (favSwitch) {
            item.isFavorite = favSwitch.checked || favSwitch.hasAttribute("checked");
          }
          item.updated = "الآن (معدّل)";
          this.state.isDirty = false;
          this.state.itemEditStep = 1;
          this.state.itemEditStep2Unlocked = false;
          this.showToast("تم حفظ التغييرات بنجاح!", "success");
          window.location.hash = "#/items/detail";
        }, 500);
      });
    }
  }

  // =========================================================================
  // Screen 5: Tasks Workflow Engine (MDS-TMP-002)
  // =========================================================================
  _renderTasks() {
    let tasks = this.state.data.tasks;
    if (this.state.tasksFilter !== "ALL") {
      tasks = tasks.filter(t => t.status === this.state.tasksFilter);
    }

    this.mainContainer.innerHTML = `
      <div class="mds-ref-page-header">
        <div class="mds-ref-page-header__row">
          <div>
            <h1 class="mds-ref-page-header__title">إدارة مهام وتدفقات العمل</h1>
            <p class="mds-ref-page-header__subtitle">متابعة مراحل التنفيذ وإحالة المهام بين أعضاء الفريق</p>
          </div>
          <button type="button" class="mds-button mds-button--primary mds-button--sm" id="btn-new-task">
            + مهمة جديدة
          </button>
        </div>
      </div>

      <!-- Filter Tabs -->
      <div class="mds-inline" style="gap: var(--mds-space-inline-xs); margin-block-end: var(--mds-space-block-md);">
        ${["ALL", "TODO", "IN_PROGRESS", "REVIEW", "DONE"].map(st => `
          <button type="button" class="mds-button mds-button--sm ${this.state.tasksFilter === st ? 'mds-button--primary' : 'mds-button--ghost'} btn-filter-task" data-status="${st}">
            ${st === 'ALL' ? 'كافة المهام' : st}
          </button>
        `).join("")}
      </div>

      <!-- Tasks Grid -->
      <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: var(--mds-space-inline-md);">
        ${tasks.map(t => `
          <div class="mds-card mds-card--raised" style="padding: var(--mds-space-scale-4); display:flex; flex-direction:column; justify-content:space-between; gap: var(--mds-space-block-sm);">
            <div>
              <div style="display:flex; justify-content:space-between; align-items:flex-start; gap: 8px;">
                <span class="mds-text--code" style="font-size: var(--mds-font-size-xs);">${t.id}</span>
                <span class="mds-badge mds-badge--${t.priority === 'critical' ? 'danger' : 'warning'}">${t.priority}</span>
              </div>
              <h3 style="margin: 8px 0; font-size: var(--mds-font-size-base); font-weight: var(--mds-font-weight-medium);">${t.title}</h3>
            </div>
            <div>
              <div style="font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary); margin-block-end: 8px;">
                المسؤول: ${t.assignee} | الاستحقاق: ${t.dueDate}
              </div>
              <div style="display: flex; justify-content: space-between; align-items: center; border-block-start: 1px solid var(--mds-color-border-subtle); padding-block-start: 8px;">
                <span class="mds-badge mds-badge--neutral">${t.status}</span>
                ${t.status !== 'DONE' ? `
                  <button type="button" class="mds-button mds-button--secondary mds-button--sm btn-advance-task" data-id="${t.id}">
                    ترقية الحالة ✓
                  </button>
                ` : '<span style="color: var(--mds-color-feedback-success-text); font-size: var(--mds-font-size-xs);">مكتملة ✓</span>'}
              </div>
            </div>
          </div>
        `).join("")}
      </div>
    `;

    // Filter clicks
    document.querySelectorAll(".btn-filter-task").forEach(btn => {
      btn.addEventListener("click", () => {
        this.state.tasksFilter = btn.getAttribute("data-status");
        this._renderTasks();
      });
    });

    // Advance task click
    document.querySelectorAll(".btn-advance-task").forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.getAttribute("data-id");
        const task = this.state.data.tasks.find(t => t.id === id);
        if (task) {
          if (task.status === "TODO") task.status = "IN_PROGRESS";
          else if (task.status === "IN_PROGRESS") task.status = "REVIEW";
          else if (task.status === "REVIEW") task.status = "DONE";
          this.showToast(`تم تحديث حالة المهمة ${task.id} إلى ${task.status}`, "success");
          this._renderTasks();
        }
      });
    });
  }

  // =========================================================================
  // Screen 6: AI Workspace (MDS-TMP-006 & AF-001 LiveRegion)
  // =========================================================================
  _renderAIWorkspace() {
    const promptData = this.state.data.aiCorpus.prompts[this.state.aiActivePromptIndex];

    this.mainContainer.innerHTML = `
      <div class="mds-ref-page-header">
        <div class="mds-ref-page-header__row">
          <div>
            <h1 class="mds-ref-page-header__title">مساحة عمل التوليد والذكاء الاصطناعي</h1>
            <p class="mds-ref-page-header__subtitle">توليد وصياغة الملخصات التشغيلية بإشراف واعتماد بشري إلزامي (Human-in-the-loop)</p>
          </div>
          <span class="mds-badge mds-badge--brand">MDS-AI Engine v1.0</span>
        </div>
      </div>

      <div class="mds-ref-ai-canvas">
        
        <!-- AI-Input-Prompt Pattern -->
        <div class="mds-ref-ai-prompt">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <h2 style="margin:0; font-size: var(--mds-font-size-base); font-weight: var(--mds-font-weight-semibold);">موجه التوليد الذكي (Prompt Input)</h2>
            <div class="mds-inline" style="gap: 8px;">
              <select id="ai-model-select" class="mds-select mds-select--sm">
                <option value="MDS-Atlas-Pro">MDS-Atlas-Pro (دقة عالية)</option>
                <option value="MDS-Atlas-Speed">MDS-Atlas-Speed (فائق السرعة)</option>
              </select>
            </div>
          </div>
          <textarea id="ai-prompt-input" class="mds-textarea" rows="3" placeholder="أدخل تعليمات التوليد هنا...">${promptData.input}</textarea>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="mds-text--numeric" style="font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">
              الاستهلاك المتوقع: ~${promptData.tokensUsed} توكن
            </span>
            <button type="button" id="btn-ai-synthesize" class="mds-button mds-button--primary ${this.state.aiState === 'PROCESSING' ? 'is-loading' : ''}">
              <span class="mds-button__label">⚡ بدء التوليد والتحليل</span>
            </button>
          </div>
        </div>

        <!-- Throttled LiveRegion Announcer (AF-001) -->
        <div id="ai-live-announcer" class="mds-visually-hidden" aria-live="polite"></div>

        <!-- AI Streaming & Review Area -->
        ${this.state.aiState === "PROCESSING" || this.state.aiState === "STREAMING" ? `
          <div class="mds-card mds-card--raised" style="padding: var(--mds-space-scale-6);">
            <div style="display:flex; align-items:center; gap: 12px; margin-block-end: 12px;">
              <div class="mds-spinner mds-spinner--sm" aria-label="جاري التوليد..."></div>
              <span style="font-size: var(--mds-font-size-sm); font-weight: var(--mds-font-weight-medium);">
                ${this.state.aiState === 'PROCESSING' ? 'جاري تهيئة النموذج والتحليل الأولي...' : 'جاري تدفق الإجابة (Streaming)...'}
              </span>
            </div>
            <div class="mds-ref-ai-streaming-box">${this.state.aiStreamBuffer}</div>
          </div>
        ` : ''}

        <!-- AI-Result-Review Pattern (Human Review & Sign-Off) -->
        ${this.state.aiState === "REVIEWING" ? `
          <div class="mds-ref-ai-review">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <div style="display:flex; align-items:center; gap: 8px;">
                <span class="mds-badge mds-badge--success">جاهز للمراجعة البشرية</span>
                <span class="mds-badge mds-badge--neutral">نسبة الثقة: ${promptData.confidence}</span>
              </div>
              <span style="font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">النموذج: ${promptData.model}</span>
            </div>

            <div style="line-height: var(--mds-font-line-height-relaxed); white-space: pre-wrap;">${promptData.output}</div>

            <div style="display:flex; justify-content:flex-end; gap: var(--mds-space-inline-sm); margin-block-start: var(--mds-space-block-md); border-block-start: 1px solid var(--mds-color-border-subtle); padding-block-start: var(--mds-space-block-md);">
              <button type="button" id="btn-ai-retry" class="mds-button mds-button--ghost mds-button--sm">
                إعادة المحاولة (Retry)
              </button>
              <button type="button" id="btn-ai-reject" class="mds-button mds-button--destructive mds-button--sm">
                رفض المخرج (Reject)
              </button>
              <button type="button" id="btn-ai-approve" class="mds-button mds-button--primary mds-button--sm">
                اعتماد وتطبيق في النظام (Approve & Apply)
              </button>
            </div>
          </div>
        ` : ''}

        ${this.state.aiState === "SUCCESS_RESOLVED" ? `
          <div class="mds-alert mds-alert--success" role="status" style="display: flex; justify-content: space-between; align-items: center;">
            <div class="mds-alert__content">
              <div class="mds-alert__title">تم اعتماد المخرج الذكي وتطبيقه في بنك المعرفة بنجاح!</div>
              <div class="mds-alert__description">تم توثيق الاعتماد برقم جلسة معتمد وحفظه في سجل النشاط.</div>
            </div>
            <button type="button" id="btn-ai-new" class="mds-button mds-button--secondary mds-button--sm">
              بدء جلسة تحليل جديدة
            </button>
          </div>
        ` : ''}
      </div>
    `;

    // Bind Synthesize Button
    const synthBtn = document.getElementById("btn-ai-synthesize");
    if (synthBtn) {
      synthBtn.addEventListener("click", () => {
        this.state.aiState = "PROCESSING";
        this.state.aiStreamBuffer = "";
        this._renderAIWorkspace();

        // Simulate streaming chunks
        setTimeout(() => {
          this.state.aiState = "STREAMING";
          const fullText = promptData.output;
          let idx = 0;
          const interval = setInterval(() => {
            idx += 15;
            this.state.aiStreamBuffer = fullText.slice(0, idx);
            const streamBox = document.querySelector(".mds-ref-ai-streaming-box");
            if (streamBox) streamBox.textContent = this.state.aiStreamBuffer;

            if (idx >= fullText.length) {
              clearInterval(interval);
              this.state.aiState = "REVIEWING";
              // AF-001 LiveRegion announcement once complete
              const announcer = document.getElementById("ai-live-announcer");
              if (announcer) announcer.textContent = "اكتمل التوليد بنجاح، المخرج متاح للمراجعة الآن.";
              this._renderAIWorkspace();
            }
          }, 60);
        }, 500);
      });
    }

    // Bind Review Actions (Approve -> SUCCESS_RESOLVED, Reject/Retry -> IDLE)
    document.getElementById("btn-ai-approve")?.addEventListener("click", () => {
      this.state.aiState = "SUCCESS_RESOLVED";
      this.showToast("تم اعتماد مخرج الذكاء الاصطناعي بنجاح ✓", "success");
      this._renderAIWorkspace();
    });

    document.getElementById("btn-ai-reject")?.addEventListener("click", () => {
      this.state.aiState = "IDLE";
      this.state.aiStreamBuffer = "";
      this.showToast("تم رفض المخرج وإلغاء الاعتماد.", "warning");
      this._renderAIWorkspace();
    });

    document.getElementById("btn-ai-retry")?.addEventListener("click", () => {
      this.state.aiState = "IDLE";
      this.state.aiStreamBuffer = "";
      this._renderAIWorkspace();
    });

    document.getElementById("btn-ai-new")?.addEventListener("click", () => {
      this.state.aiState = "IDLE";
      this.state.aiStreamBuffer = "";
      this._renderAIWorkspace();
    });
  }

  // =========================================================================
  // Screen 7: Activity Timeline (MDS-TMP-003 Variant)
  // =========================================================================
  _renderActivity() {
    const activities = this.state.data.activities;

    this.mainContainer.innerHTML = `
      <div class="mds-ref-page-header">
        <div class="mds-ref-page-header__row">
          <div>
            <h1 class="mds-ref-page-header__title">سجل النشاط والتدقيق الأمني</h1>
            <p class="mds-ref-page-header__subtitle">تتبع زمني دقيق لكافة العمليات والإجراءات المنفذة عبر مساحة العمل</p>
          </div>
          <span class="mds-badge mds-badge--neutral">سجل تدقيق غير قابل للتعديل</span>
        </div>
      </div>

      <div class="mds-card mds-card--raised" style="padding: var(--mds-space-scale-6);">
        <ul class="mds-ref-timeline">
          ${activities.map(a => `
            <li class="mds-ref-timeline-item">
              <div class="mds-ref-timeline-avatar">${a.avatar}</div>
              <div style="flex: 1;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <span style="font-weight: var(--mds-font-weight-semibold);">${a.actor}</span>
                  <span class="mds-text--numeric" style="font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">${a.timestamp}</span>
                </div>
                <div style="font-size: var(--mds-font-size-sm); margin-block: 4px;">${a.action}</div>
                <span class="mds-badge mds-badge--neutral" style="font-size: 10px;">الهدف: ${a.target}</span>
              </div>
            </li>
          `).join("")}
        </ul>
      </div>
    `;
  }

  // =========================================================================
  // Screens 8-11: Settings Workspace (MDS-TMP-005)
  // =========================================================================
  _renderSettings() {
    const subRoute = this.state.currentRoute;

    this.mainContainer.innerHTML = `
      <div class="mds-ref-page-header">
        <h1 class="mds-ref-page-header__title">إعدادات مساحة العمل والحوكمة</h1>
        <p class="mds-ref-page-header__subtitle">تخصيص المظهر العام والسمات وتفضيلات التنبيهات وإدارة الصلاحيات</p>
      </div>

      <!-- Settings Tabs -->
      <mds-tabs id="tabs-settings">
        <div role="tablist" class="mds-tabs__list">
          <button type="button" role="tab" class="mds-tabs__tab ${subRoute.endsWith('general') || subRoute === '#/settings' ? 'is-active' : ''}" data-route="#/settings/general">
            العامة
          </button>
          <button type="button" role="tab" class="mds-tabs__tab ${subRoute.endsWith('appearance') ? 'is-active' : ''}" data-route="#/settings/appearance">
            المظهر والسمات
          </button>
          <button type="button" role="tab" class="mds-tabs__tab ${subRoute.endsWith('notifications') ? 'is-active' : ''}" data-route="#/settings/notifications">
            الإشعارات
          </button>
          <button type="button" role="tab" class="mds-tabs__tab ${subRoute.endsWith('access') ? 'is-active' : ''}" data-route="#/settings/access">
            الوصول والأمان
          </button>
        </div>
      </mds-tabs>

      <div id="settings-content-pane">
        ${subRoute.endsWith("appearance") ? this._getSettingsAppearanceMarkup() :
          subRoute.endsWith("notifications") ? this._getSettingsNotificationsMarkup() :
          subRoute.endsWith("access") ? this._getSettingsAccessMarkup() :
          this._getSettingsGeneralMarkup()}
      </div>
    `;

    // Bind settings tab routing
    document.querySelectorAll("#tabs-settings .mds-tabs__tab").forEach(tab => {
      tab.addEventListener("click", () => {
        window.location.hash = tab.getAttribute("data-route");
      });
    });

    this._bindSettingsSubEvents();
  }

  _getSettingsGeneralMarkup() {
    return `
      <div class="mds-ref-form-section">
        <h2 style="margin: 0; font-size: var(--mds-font-size-lg);">إعدادات مساحة العمل الأساسية</h2>
        <div class="mds-field">
          <label class="mds-label" for="set-name">اسم مساحة العمل</label>
          <input type="text" id="set-name" class="mds-input" value="${this.state.data.settings.workspaceName}">
        </div>
        <div class="mds-field">
          <label class="mds-label" for="set-tz">المنطقة الزمنية الرسمية</label>
          <input type="text" id="set-tz" class="mds-input" value="${this.state.data.settings.timezone}">
        </div>
        <div style="display:flex; justify-content:flex-end;">
          <button type="button" id="btn-save-gen-settings" class="mds-button mds-button--primary mds-button--sm">
            حفظ التغييرات
          </button>
        </div>
      </div>
    `;
  }

  _getSettingsAppearanceMarkup() {
    return `
      <div class="mds-ref-form-section">
        <h2 style="margin: 0; font-size: var(--mds-font-size-lg);">تخصيص المظهر وتوكنز النواة (Live Runtime)</h2>
        <p style="margin:0; font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">
          يتم تطبيق التغييرات فورياً عبر استهلاك كود CSS ومتغيرات التوكنز الرسمية دون أي طبقات خارجية.
        </p>

        <div class="mds-field">
          <label class="mds-label">نمط الإضاءة والتباين (Luminance Mode)</label>
          <div class="mds-inline" style="gap: var(--mds-space-inline-sm);">
            ${["light", "dark", "high-contrast"].map(mode => `
              <button type="button" class="mds-button mds-button--sm ${this.state.currentTheme === mode ? 'mds-button--primary' : 'mds-button--secondary'} btn-set-theme" data-val="${mode}">
                ${mode === 'light' ? 'فاتح (Light)' : mode === 'dark' ? 'داكن (Dark)' : 'عالي التباين (High Contrast)'}
              </button>
            `).join("")}
          </div>
        </div>

        <div class="mds-field">
          <label class="mds-label">النمط البصري (Preset)</label>
          <div class="mds-inline" style="gap: var(--mds-space-inline-sm);">
            ${["soft", "refined", "expressive"].map(pr => `
              <button type="button" class="mds-button mds-button--sm ${this.state.currentPreset === pr ? 'mds-button--primary' : 'mds-button--secondary'} btn-set-preset" data-val="${pr}">
                ${pr === 'soft' ? 'ناعم (Soft Modern)' : pr === 'refined' ? 'مختزل (Refined Minimal)' : 'تعبيري (Expressive)'}
              </button>
            `).join("")}
          </div>
        </div>

        <div class="mds-field">
          <label class="mds-label">مستوى الكثافة الفراغية (Spatial Density)</label>
          <div class="mds-inline" style="gap: var(--mds-space-inline-sm);">
            <button type="button" class="mds-button mds-button--sm ${this.state.currentDensity === 'comfortable' ? 'mds-button--primary' : 'mds-button--secondary'} btn-set-density" data-val="comfortable">
              مريح (Comfortable 40px)
            </button>
            <button type="button" class="mds-button mds-button--sm ${this.state.currentDensity === 'compact' ? 'mds-button--primary' : 'mds-button--secondary'} btn-set-density" data-val="compact">
              مدمج (Compact 32px)
            </button>
            <button type="button" class="mds-button mds-button--sm mds-button--secondary" disabled style="opacity: 0.5;">
              مكثف (Dense 28px) [Deferred]
            </button>
          </div>
        </div>
      </div>
    `;
  }

  _getSettingsNotificationsMarkup() {
    return `
      <div class="mds-ref-form-section">
        <h2 style="margin: 0; font-size: var(--mds-font-size-lg);">قنوات التنبيهات والإشعارات</h2>
        
        <div style="display:flex; justify-content:space-between; align-items:center; padding-block: 8px; border-block-end: 1px solid var(--mds-color-border-subtle);">
          <div>
            <div style="font-weight: var(--mds-font-weight-medium);">ملخص البريد الأسبوعي</div>
            <div style="font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">إرسال تقرير تحليلي أسبوعي بالمؤشرات والمهام</div>
          </div>
          <mds-switch checked></mds-switch>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; padding-block: 8px; border-block-end: 1px solid var(--mds-color-border-subtle);">
          <div>
            <div style="font-weight: var(--mds-font-weight-medium);">تنبيهات الأمان والوصول</div>
            <div style="font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">إشعار فوري عند محاولات الدخول غير المعتادة</div>
          </div>
          <mds-switch checked></mds-switch>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; padding-block: 8px;">
          <div>
            <div style="font-weight: var(--mds-font-weight-medium);">إشعارات الإشارة والتكليف (Mentions)</div>
            <div style="font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">تنبيه عند إحالة مهمة أو الإشارة إلى اسمك</div>
          </div>
          <mds-switch checked></mds-switch>
        </div>
      </div>
    `;
  }

  _getSettingsAccessMarkup() {
    const users = this.state.data.users;
    return `
      <div class="mds-ref-form-section">
        <h2 style="margin: 0; font-size: var(--mds-font-size-lg);">إدارة أدوار الوصول والصلاحيات</h2>
        
        <div class="mds-table-container" tabindex="0" role="region" aria-label="جدول أدوار المستخدمين">
          <table class="mds-table">
            <thead>
              <tr>
                <th>المستخدم</th>
                <th>البريد الإلكتروني</th>
                <th>الدور المعماري</th>
                <th>الحالة</th>
              </tr>
            </thead>
            <tbody>
              ${users.map(u => `
                <tr>
                  <td style="font-weight: var(--mds-font-weight-medium);">${u.name}</td>
                  <td>${u.email}</td>
                  <td><span class="mds-badge mds-badge--brand">${u.role}</span></td>
                  <td><span class="mds-badge mds-badge--success">نشط</span></td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>

        <!-- Danger Zone Panel -->
        <div class="mds-ref-danger-zone" style="margin-block-start: var(--mds-space-block-lg);">
          <div>
            <h3 style="margin:0; font-size: var(--mds-font-size-base); color: var(--mds-color-feedback-danger-text);">منطقة الإجراءات الحساسة (Danger Zone)</h3>
            <p style="margin: 4px 0 0 0; font-size: var(--mds-font-size-xs); color: var(--mds-color-text-secondary);">
              حذف مساحة العمل بالكامل يترتب عليه إلغاء جميع السجلات والمهام التشغيلية نهائياً.
            </p>
          </div>
          <button type="button" class="mds-button mds-button--destructive mds-button--sm" id="btn-delete-workspace">
            حذف مساحة العمل
          </button>
        </div>
      </div>

      <!-- Workspace Delete Modal -->
      <mds-dialog id="modal-delete-workspace">
        <div class="mds-dialog__surface">
          <div class="mds-dialog__header">
            <h2 class="mds-dialog__title">حذف مساحة العمل نهائياً</h2>
          </div>
          <div class="mds-dialog__body">
            <p class="mds-text">
              هل أنت متأكد من رغبتك في حذف مساحة العمل بالكامل؟ هذا الإجراء محمي ويتطلب صلاحيات Administrator.
            </p>
          </div>
          <div class="mds-dialog__footer">
            <button type="button" class="mds-button mds-button--secondary" data-dialog-cancel>إلغاء الأمر</button>
            <button type="button" class="mds-button mds-button--destructive" data-dialog-confirm id="btn-confirm-del-ws">حذف نهائي</button>
          </div>
        </div>
      </mds-dialog>
    `;
  }

  _bindSettingsSubEvents() {
    // General save
    document.getElementById("btn-save-gen-settings")?.addEventListener("click", () => {
      this.showToast("تم تحديث إعدادات مساحة العمل بنجاح ✓", "success");
    });

    // Appearance theme buttons
    document.querySelectorAll(".btn-set-theme").forEach(btn => {
      btn.addEventListener("click", () => {
        const val = btn.getAttribute("data-val");
        this.setTheme(val);
        const select = document.getElementById("ctrl-ref-theme");
        if (select) select.value = val;
        this.render();
      });
    });

    // Appearance preset buttons
    document.querySelectorAll(".btn-set-preset").forEach(btn => {
      btn.addEventListener("click", () => {
        const val = btn.getAttribute("data-val");
        this.setPreset(val);
        const select = document.getElementById("ctrl-ref-preset");
        if (select) select.value = val;
        this.render();
      });
    });

    // Appearance density buttons
    document.querySelectorAll(".btn-set-density").forEach(btn => {
      btn.addEventListener("click", () => {
        const val = btn.getAttribute("data-val");
        this.setDensity(val);
        const select = document.getElementById("ctrl-ref-density");
        if (select) select.value = val;
        this.render();
      });
    });

    // Danger zone delete workspace modal
    const wsDelBtn = document.getElementById("btn-delete-workspace");
    const wsModal = document.getElementById("modal-delete-workspace");
    if (wsDelBtn && wsModal) {
      wsDelBtn.addEventListener("click", () => {
        if (this.state.currentRole !== "Administrator") {
          this.showToast("عذراً، يتطلب تنفيذ هذا الإجراء صلاحيات مدير (Administrator). [Permission Denied]", "danger");
          return;
        }
        wsModal.open(wsDelBtn);
      });
    }

    document.getElementById("btn-confirm-del-ws")?.addEventListener("click", () => {
      wsModal.close();
      this.showToast("تم محاكاة حذف مساحة العمل بنجاح.", "warning");
    });
  }

  _renderEmptyState(title, desc, actionHref) {
    this.mainContainer.innerHTML = `
      <div class="mds-ref-empty-state">
        <div class="mds-ref-empty-state__icon">📭</div>
        <h2 style="margin: 0; font-size: var(--mds-font-size-xl);">${title}</h2>
        <p class="mds-text" style="color: var(--mds-color-text-secondary); max-inline-size: 400px; margin: 0;">${desc}</p>
        <div class="mds-inline" style="gap: 12px; margin-block-start: 8px;">
          <a href="${actionHref}" class="mds-button mds-button--primary mds-button--sm">إنشاء عنصر جديد</a>
          <button type="button" class="mds-button mds-button--secondary mds-button--sm" id="btn-reset-empty-state">إعادة التعيين (Reset)</button>
        </div>
      </div>
    `;

    document.getElementById("btn-reset-empty-state")?.addEventListener("click", () => {
      this.state.simulatedState = "normal";
      const simSelect = document.getElementById("ctrl-ref-sim-state");
      if (simSelect) simSelect.value = "normal";
      this.render();
    });
  }

  _renderNotFound() {
    this.mainContainer.innerHTML = `
      <div class="mds-ref-empty-state">
        <div class="mds-ref-empty-state__icon">🔍</div>
        <h2 style="margin: 0; font-size: var(--mds-font-size-2xl);">404 — الصفحة غير موجودة</h2>
        <p class="mds-text" style="color: var(--mds-color-text-secondary);">المسار المطلوب <code>${this.state.currentRoute}</code> غير معرّف في شجرة التنقل.</p>
        <a href="#/overview" class="mds-button mds-button--primary mds-button--sm">العودة للرئيسية</a>
      </div>
    `;
  }
}

// Global bootstrap
document.addEventListener("DOMContentLoaded", () => {
  window.mdsWorkspaceApp = new ReferenceApp();
  window.mdsWorkspaceApp.init();
});
