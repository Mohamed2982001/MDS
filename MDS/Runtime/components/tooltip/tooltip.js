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

export class MdsTooltip extends HTMLElement {
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
