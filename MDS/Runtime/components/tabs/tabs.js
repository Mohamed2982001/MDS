/**
 * MDS (Master Design System) — Tabs Custom Element & Controller
 * Architecture Layer: Layer 04 (Components / Navigation)
 * Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
 *
 * Implements WAI-ARIA APG Tabs Pattern custom element: <mds-tabs>
 * Features:
 * - Roving tabindex (selected tab tabindex="0", unselected tabindex="-1")
 * - Logical Arrow navigation (inverts Left/Right in RTL direction)
 * - Home and End key shortcuts
 * - TabPanel synchronization (hidden toggling)
 * - Custom "change" event dispatch
 */

export class MdsTabs extends HTMLElement {
  constructor() {
    super();
    this._onKeyDown = this._onKeyDown.bind(this);
    this._onClick = this._onClick.bind(this);
  }

  connectedCallback() {
    this._initTabs();
    this.addEventListener("click", this._onClick);
    this.addEventListener("keydown", this._onKeyDown);
  }

  disconnectedCallback() {
    this.removeEventListener("click", this._onClick);
    this.removeEventListener("keydown", this._onKeyDown);
  }

  get _tablist() {
    return this.querySelector('[role="tablist"], .mds-tabs__list');
  }

  get _tabs() {
    return Array.from(this.querySelectorAll('[role="tab"], .mds-tabs__tab'));
  }

  get _panels() {
    return Array.from(this.querySelectorAll('[role="tabpanel"], .mds-tabs__panel'));
  }

  _initTabs() {
    const tabs = this._tabs;
    if (tabs.length === 0) return;

    let selectedIndex = tabs.findIndex(tab => tab.getAttribute("aria-selected") === "true");
    if (selectedIndex === -1) {
      selectedIndex = 0;
      tabs[0].setAttribute("aria-selected", "true");
    }

    tabs.forEach((tab, index) => {
      tab.setAttribute("role", "tab");
      if (index === selectedIndex) {
        tab.setAttribute("tabindex", "0");
        tab.classList.add("mds-tabs__tab--active");
      } else {
        tab.setAttribute("tabindex", "-1");
        tab.setAttribute("aria-selected", "false");
        tab.classList.remove("mds-tabs__tab--active");
      }
    });

    this._syncPanels(selectedIndex);
  }

  _syncPanels(selectedIndex) {
    const tabs = this._tabs;
    const panels = this._panels;

    if (tabs[selectedIndex] && panels.length > 0) {
      const activeTab = tabs[selectedIndex];
      const controlsId = activeTab.getAttribute("aria-controls");

      panels.forEach((panel, i) => {
        panel.setAttribute("role", "tabpanel");
        const match = controlsId ? panel.id === controlsId : i === selectedIndex;
        if (match) {
          panel.removeAttribute("hidden");
          panel.setAttribute("tabindex", "0");
        } else {
          panel.setAttribute("hidden", "");
        }
      });
    }
  }

  selectTab(tabOrIndex) {
    const tabs = this._tabs;
    let index = typeof tabOrIndex === "number" ? tabOrIndex : tabs.indexOf(tabOrIndex);
    if (index < 0 || index >= tabs.length) return;

    tabs.forEach((tab, i) => {
      const isSelected = i === index;
      tab.setAttribute("aria-selected", isSelected ? "true" : "false");
      tab.setAttribute("tabindex", isSelected ? "0" : "-1");
      if (isSelected) {
        tab.classList.add("mds-tabs__tab--active");
        tab.focus();
      } else {
        tab.classList.remove("mds-tabs__tab--active");
      }
    });

    this._syncPanels(index);

    this.dispatchEvent(new CustomEvent("change", {
      bubbles: true,
      composed: true,
      detail: { selectedIndex: index, selectedTab: tabs[index] }
    }));
  }

  _onClick(e) {
    const tab = e.target.closest('[role="tab"], .mds-tabs__tab');
    if (tab && this.contains(tab)) {
      if (tab.hasAttribute("disabled") || tab.getAttribute("aria-disabled") === "true") return;
      this.selectTab(tab);
    }
  }

  _onKeyDown(e) {
    const tabs = this._tabs;
    const currentTab = e.target.closest('[role="tab"], .mds-tabs__tab');
    if (!currentTab || !tabs.includes(currentTab)) return;

    const currentIndex = tabs.indexOf(currentTab);
    const isRtl = this._isRtl();
    let targetIndex = -1;

    switch (e.key) {
      case "ArrowLeft":
        targetIndex = isRtl ? (currentIndex + 1) % tabs.length : (currentIndex - 1 + tabs.length) % tabs.length;
        break;
      case "ArrowRight":
        targetIndex = isRtl ? (currentIndex - 1 + tabs.length) % tabs.length : (currentIndex + 1) % tabs.length;
        break;
      case "Home":
        targetIndex = 0;
        break;
      case "End":
        targetIndex = tabs.length - 1;
        break;
      default:
        return;
    }

    e.preventDefault();
    this.selectTab(targetIndex);
  }

  _isRtl() {
    const dir = this.getAttribute("dir") || document.documentElement.getAttribute("dir") || "ltr";
    return dir.toLowerCase() === "rtl";
  }
}

if (typeof customElements !== "undefined" && !customElements.get("mds-tabs")) {
  customElements.define("mds-tabs", MdsTabs);
}
