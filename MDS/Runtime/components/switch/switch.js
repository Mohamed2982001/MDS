/**
 * MDS (Master Design System) — Switch Custom Element & Controller
 * Architecture Layer: Layer 04 (Components / Inputs)
 * Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
 *
 * Implements accessible WAI-ARIA role="switch" custom element: <mds-switch>
 * Supports Space and Enter toggling, aria-checked reflection, and change event dispatching.
 */

export class MdsSwitch extends HTMLElement {
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
