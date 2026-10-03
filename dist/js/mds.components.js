/**
 * Master Design System (MDS) — Modular Components Runtime
 */
(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
  typeof define === 'function' && define.amd ? define(factory) :
  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.MDS_Components = factory());
})(this, (function () {
  'use strict';

/**
 * MDS (Master Design System) — FocusTrap Accessibility Primitive
 * Architecture Layer: Layer 03 (Primitives / Accessibility)
 * Standard: W3C WAI-ARIA Modal Focus Containment Infrastructure
 * Responsibility: Keyboard focus containment & restoration (Component-Agnostic)
 */

const FOCUSABLE_SELECTOR = [
  'a[href]',
  'area[href]',
  'input:not([disabled]):not([type="hidden"])',
  'select:not([disabled])',
  'textarea:not([disabled])',
  'button:not([disabled])',
  'iframe',
  'object',
  'embed',
  '[contenteditable]',
  '[tabindex]:not([tabindex="-1"])'
].join(', ');

class FocusTrap {
  /**
   * @param {HTMLElement} element - The DOM node within which to trap focus.
   * @param {Object} [options]
   * @param {HTMLElement|string} [options.initialFocus] - Element or selector to receive initial focus.
   * @param {Function} [options.onEscape] - Callback invoked when Escape key is pressed.
   * @param {boolean} [options.returnFocusOnDeactivate=true] - Whether to restore focus upon deactivation.
   */
  constructor(element, options = {}) {
    if (!element) {
      throw new Error('FocusTrap requires a valid DOM element.');
    }
    this.element = element;
    this.options = {
      returnFocusOnDeactivate: true,
      ...options
    };
    this.active = false;
    this.paused = false;
    this.previouslyFocused = null;
    this._handleKeyDown = this._handleKeyDown.bind(this);
  }

  getFocusableElements() {
    return Array.from(this.element.querySelectorAll(FOCUSABLE_SELECTOR)).filter(
      (el) => el.offsetParent !== null && !el.hasAttribute('disabled')
    );
  }

  activate() {
    if (this.active) return;
    this.previouslyFocused = document.activeElement;
    this.active = true;
    this.paused = false;

    this.element.addEventListener('keydown', this._handleKeyDown);

    // Set initial focus
    const focusables = this.getFocusableElements();
    let targetToFocus = null;

    if (this.options.initialFocus) {
      targetToFocus =
        typeof this.options.initialFocus === 'string'
          ? this.element.querySelector(this.options.initialFocus)
          : this.options.initialFocus;
    }

    if (!targetToFocus && focusables.length > 0) {
      targetToFocus = focusables[0];
    }

    if (targetToFocus && typeof targetToFocus.focus === 'function') {
      targetToFocus.focus();
    }
  }

  deactivate() {
    if (!this.active) return;
    this.element.removeEventListener('keydown', this._handleKeyDown);
    this.active = false;
    this.paused = false;

    if (this.options.returnFocusOnDeactivate && this.previouslyFocused && typeof this.previouslyFocused.focus === 'function') {
      this.previouslyFocused.focus();
    }
    this.previouslyFocused = null;
  }

  pause() {
    this.paused = true;
  }

  resume() {
    this.paused = false;
  }

  _handleKeyDown(event) {
    if (!this.active || this.paused) return;

    // Handle Escape key
    if (event.key === 'Escape' || event.key === 'Esc') {
      if (typeof this.options.onEscape === 'function') {
        event.stopPropagation();
        this.options.onEscape(event);
        return;
      }
    }

    // Handle Tab key containment
    if (event.key === 'Tab') {
      const focusables = this.getFocusableElements();
      if (focusables.length === 0) {
        event.preventDefault();
        return;
      }

      const firstFocusable = focusables[0];
      const lastFocusable = focusables[focusables.length - 1];

      if (event.shiftKey) {
        // Backward navigation (Shift + Tab)
        if (document.activeElement === firstFocusable || !this.element.contains(document.activeElement)) {
          event.preventDefault();
          lastFocusable.focus();
        }
      } else {
        // Forward navigation (Tab)
        if (document.activeElement === lastFocusable || !this.element.contains(document.activeElement)) {
          event.preventDefault();
          firstFocusable.focus();
        }
      }
    }
  }
}

// Native Custom Element wrapper for declarative usage: <mds-focus-trap active>
if (typeof customElements !== 'undefined' && !customElements.get('mds-focus-trap')) {
  customElements.define(
    'mds-focus-trap',
    class MDSFocusTrapElement extends HTMLElement {
      connectedCallback() {
        this.trap = new FocusTrap(this, {
          onEscape: () => this.dispatchEvent(new CustomEvent('mds-escape', { bubbles: true }))
        });
        if (this.hasAttribute('active')) {
          this.trap.activate();
        }
      }

      disconnectedCallback() {
        if (this.trap) {
          this.trap.deactivate();
        }
      }

      static get observedAttributes() {
        return ['active'];
      }

      attributeChangedCallback(name, oldValue, newValue) {
        if (name === 'active' && this.trap) {
          if (newValue !== null) {
            this.trap.activate();
          } else {
            this.trap.deactivate();
          }
        }
      }
    }
  );
}


/**
 * MDS (Master Design System) — Switch Custom Element & Controller
 * Architecture Layer: Layer 04 (Components / Inputs)
 * Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
 *
 * Implements accessible WAI-ARIA role="switch" custom element: <mds-switch>
 * Supports Space and Enter toggling, aria-checked reflection, and change event dispatching.
 */

class MdsSwitch extends HTMLElement {
  static get observedAttributes() {
    return ["checked", "disabled", "label"];
  }

  constructor() {
    super();
    this._onKeyDown = this._onKeyDown.bind(this);
    this._onClick = this._onClick.bind(this);
  }

  connectedCallback() {
    if (!this.hasAttribute("role")) {
      this.setAttribute("role", "switch");
    }
    if (!this.hasAttribute("tabindex") && !this.hasAttribute("disabled")) {
      this.setAttribute("tabindex", "0");
    }
    this._syncAria();

    this.addEventListener("click", this._onClick);
    this.addEventListener("keydown", this._onKeyDown);
  }

  disconnectedCallback() {
    this.removeEventListener("click", this._onClick);
    this.removeEventListener("keydown", this._onKeyDown);
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue !== newValue) {
      this._syncAria();
    }
  }

  get checked() {
    return this.hasAttribute("checked");
  }

  set checked(val) {
    if (val) {
      this.setAttribute("checked", "");
    } else {
      this.removeAttribute("checked");
    }
  }

  get disabled() {
    return this.hasAttribute("disabled");
  }

  set disabled(val) {
    if (val) {
      this.setAttribute("disabled", "");
      this.removeAttribute("tabindex");
    } else {
      this.removeAttribute("disabled");
      this.setAttribute("tabindex", "0");
    }
  }

  toggle() {
    if (this.disabled) return;
    this.checked = !this.checked;
    this.dispatchEvent(new CustomEvent("change", {
      bubbles: true,
      composed: true,
      detail: { checked: this.checked }
    }));
  }

  _onClick(e) {
    if (this.disabled) {
      e.preventDefault();
      return;
    }
    this.toggle();
  }

  _onKeyDown(e) {
    if (this.disabled) return;
    if (e.key === " " || e.key === "Enter") {
      e.preventDefault();
      this.toggle();
    }
  }

  _syncAria() {
    this.setAttribute("aria-checked", this.checked ? "true" : "false");
    if (this.disabled) {
      this.setAttribute("aria-disabled", "true");
      this.removeAttribute("tabindex");
    } else {
      this.removeAttribute("aria-disabled");
      if (!this.hasAttribute("tabindex")) {
        this.setAttribute("tabindex", "0");
      }
    }
  }
}

if (typeof customElements !== "undefined" && !customElements.get("mds-switch")) {
  customElements.define("mds-switch", MdsSwitch);
}


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

class MdsTabs extends HTMLElement {
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


/**
 * MDS (Master Design System) — Tooltip Custom Element & Controller
 * Architecture Layer: Layer 04 (Components / Overlays)
 * Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
 *
 * Implements WAI-ARIA Tooltip Pattern: <mds-tooltip>
 * Invariants:
 * - 300ms intentional hover delay to prevent flickering
 * - Instant display on keyboard focus (:focus-visible)
 * - Immediate dismissal on Escape key
 * - Programmatic aria-describedby linkage
 * - role="tooltip" on bubble
 */

class MdsTooltip extends HTMLElement {
  constructor() {
    super();
    this._showTimer = null;
    this._isVisible = false;
    this._onMouseEnter = this._onMouseEnter.bind(this);
    this._onMouseLeave = this._onMouseLeave.bind(this);
    this._onFocusIn = this._onFocusIn.bind(this);
    this._onFocusOut = this._onFocusOut.bind(this);
    this._onKeyDown = this._onKeyDown.bind(this);
  }

  connectedCallback() {
    this._initTooltip();
    this.addEventListener("mouseenter", this._onMouseEnter);
    this.addEventListener("mouseleave", this._onMouseLeave);
    this.addEventListener("focusin", this._onFocusIn);
    this.addEventListener("focusout", this._onFocusOut);
    this.addEventListener("keydown", this._onKeyDown);
  }

  disconnectedCallback() {
    this._clearTimer();
    this.removeEventListener("mouseenter", this._onMouseEnter);
    this.removeEventListener("mouseleave", this._onMouseLeave);
    this.removeEventListener("focusin", this._onFocusIn);
    this.removeEventListener("focusout", this._onFocusOut);
    this.removeEventListener("keydown", this._onKeyDown);
  }

  get _bubble() {
    return this.querySelector('[role="tooltip"], .mds-tooltip__bubble');
  }

  get _trigger() {
    return this.querySelector('button, a, input, [tabindex]:not([tabindex="-1"])') || this.firstElementChild;
  }

  _initTooltip() {
    const bubble = this._bubble;
    const trigger = this._trigger;

    if (bubble) {
      if (!bubble.id) {
        bubble.id = `mds-tooltip-${Math.random().toString(36).slice(2, 9)}`;
      }
      bubble.setAttribute("role", "tooltip");
      bubble.setAttribute("aria-hidden", "true");

      if (trigger && !trigger.hasAttribute("aria-describedby")) {
        trigger.setAttribute("aria-describedby", bubble.id);
      }
    }
  }

  show(immediate = false) {
    this._clearTimer();
    if (this._isVisible) return;

    if (immediate) {
      this._applyVisibility(true);
    } else {
      // 300ms intentional hover delay
      this._showTimer = setTimeout(() => {
        this._applyVisibility(true);
      }, 300);
    }
  }

  hide() {
    this._clearTimer();
    if (!this._isVisible) return;
    this._applyVisibility(false);
  }

  _applyVisibility(visible) {
    this._isVisible = visible;
    const bubble = this._bubble;
    if (bubble) {
      bubble.setAttribute("data-visible", visible ? "true" : "false");
      bubble.setAttribute("aria-hidden", visible ? "false" : "true");
    }
  }

  _clearTimer() {
    if (this._showTimer) {
      clearTimeout(this._showTimer);
      this._showTimer = null;
    }
  }

  _onMouseEnter() {
    this.show(false);
  }

  _onMouseLeave() {
    this.hide();
  }

  _onFocusIn() {
    this.show(true); // Instant on keyboard focus
  }

  _onFocusOut() {
    this.hide();
  }

  _onKeyDown(e) {
    if (e.key === "Escape" && this._isVisible) {
      e.stopPropagation();
      this.hide();
    }
  }
}

if (typeof customElements !== "undefined" && !customElements.get("mds-tooltip")) {
  customElements.define("mds-tooltip", MdsTooltip);
}


/**
 * MDS (Master Design System) — Dialog Custom Element & Controller
 * Architecture Layer: Layer 04 (Components / Overlays)
 * Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
 *
 * Implements WAI-ARIA Dialog (Modal) Pattern: <mds-dialog>
 * Key Invariants:
 * - FocusTrap integration: Traps Tab traversal strictly within the modal
 * - Finding AF-002 Initial Focus Safety: For destructive confirmations, lands on Cancel button
 * - Finding AF-003 Inertness: Native <dialog> or sets background inert
 * - Escape key dismissal
 * - Focus return to opening trigger element
 */


class MdsDialog extends HTMLElement {
  constructor() {
    super();
    this._isOpen = false;
    this._triggerElement = null;
    this._focusTrap = null;
    this._onKeyDown = this._onKeyDown.bind(this);
    this._onBackdropClick = this._onBackdropClick.bind(this);
  }

  connectedCallback() {
    this.setAttribute("role", "dialog");
    this.setAttribute("aria-modal", "true");
    if (!this.hasAttribute("tabindex")) {
      this.setAttribute("tabindex", "-1");
    }

    this.addEventListener("keydown", this._onKeyDown);
    this.addEventListener("click", this._onBackdropClick);

    // If opened via attribute
    if (this.hasAttribute("open")) {
      this.open();
    }
  }

  disconnectedCallback() {
    this.removeEventListener("keydown", this._onKeyDown);
    this.removeEventListener("click", this._onBackdropClick);
    if (this._focusTrap) {
      this._focusTrap.deactivate();
    }
  }

  get isOpen() {
    return this._isOpen;
  }

  open(triggerElement = null) {
    if (this._isOpen) return;
    this._isOpen = true;
    this._triggerElement = triggerElement || document.activeElement;
    this.setAttribute("open", "");
    this.style.display = "block";

    // Initialize FocusTrap
    if (!this._focusTrap) {
      this._focusTrap = new FocusTrap(this, {
        initialFocus: this._resolveInitialFocus(),
        onEscape: () => this.close()
      });
    }
    this._focusTrap.activate();

    this.dispatchEvent(new CustomEvent("mds:dialog:open", {
      bubbles: true,
      composed: true
    }));
  }

  close() {
    if (!this._isOpen) return;
    this._isOpen = false;
    this.removeAttribute("open");
    this.style.display = "none";

    if (this._focusTrap) {
      this._focusTrap.deactivate();
    }

    // Return focus to trigger element
    if (this._triggerElement && typeof this._triggerElement.focus === "function") {
      this._triggerElement.focus();
    }

    this.dispatchEvent(new CustomEvent("mds:dialog:close", {
      bubbles: true,
      composed: true
    }));
  }

  /**
   * Architectural Finding AF-002:
   * Destructive confirmation dialogs must place initial focus on the Cancel button,
   * never on the destructive action button.
   */
  _resolveInitialFocus() {
    const hasDestructiveAction = this.querySelector(
      '.mds-button--destructive, [data-intent="destructive"], [data-destructive="true"]'
    );

    if (hasDestructiveAction) {
      const cancelButton = this.querySelector(
        '.mds-button--secondary, [data-action="cancel"], [data-cancel="true"]'
      );
      if (cancelButton) {
        return cancelButton;
      }
    }

    // Default: first focusable element or dialog itself
    const firstFocusable = this.querySelector(
      'button:not(:disabled), [href], input:not(:disabled), select:not(:disabled), textarea:not(:disabled), [tabindex]:not([tabindex="-1"])'
    );
    return firstFocusable || this;
  }

  _onKeyDown(e) {
    if (e.key === "Escape") {
      e.preventDefault();
      this.close();
    }
  }

  _onBackdropClick(e) {
    // If clicking directly on dialog backdrop scrim
    if (e.target === this && !this.hasAttribute("data-persistent")) {
      this.close();
    }
  }
}

if (typeof customElements !== "undefined" && !customElements.get("mds-dialog")) {
  customElements.define("mds-dialog", MdsDialog);
}


  return { MdsSwitch, MdsTabs, MdsTooltip, MdsDialog };
}));
