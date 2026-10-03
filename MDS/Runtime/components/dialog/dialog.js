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

import { FocusTrap } from "../../primitives/interaction/focus-trap.js";

export class MdsDialog extends HTMLElement {
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
