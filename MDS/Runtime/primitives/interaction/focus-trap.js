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

export class FocusTrap {
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
