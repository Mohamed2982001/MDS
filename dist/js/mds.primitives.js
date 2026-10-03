/**
 * Master Design System (MDS) — Modular Primitives Runtime
 */
(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
  typeof define === 'function' && define.amd ? define(factory) :
  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.MDS_Primitives = factory());
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
 * MDS (Master Design System) — LiveRegion Accessibility Primitive
 * Architecture Layer: Layer 03 (Primitives / Accessibility)
 * Standard: W3C WAI-ARIA Dynamic Announcements & Screen Reader Speech Buffer Protection
 * Addresses Architectural Finding: AF-001 (Decoupled Streaming Speech Throttling)
 */

class LiveRegion {
  /**
   * @param {Object} [options]
   * @param {'polite'|'assertive'} [options.mode='polite']
   * @param {number} [options.throttleMs=1000] - Minimum duration between consecutive announcements
   */
  constructor(options = {}) {
    this.mode = options.mode || 'polite';
    this.throttleMs = options.throttleMs || 1000;
    this.lastAnnouncementTime = 0;
    this.queuedMessage = null;
    this.timer = null;

    this.container = this._createContainer();
  }

  _createContainer() {
    if (typeof document === 'undefined') return null;

    const el = document.createElement('div');
    el.className = 'mds-visually-hidden';
    el.setAttribute('role', this.mode === 'assertive' ? 'alert' : 'status');
    el.setAttribute('aria-live', this.mode);
    el.setAttribute('aria-atomic', 'true');
    document.body.appendChild(el);
    return el;
  }

  /**
   * Sends a standard announcement to screen readers.
   * @param {string} message
   */
  announce(message) {
    if (!this.container || !message) return;

    const now = Date.now();
    if (now - this.lastAnnouncementTime < this.throttleMs) {
      // Throttle announcement to protect screen reader speech queue
      this.queuedMessage = message;
      if (!this.timer) {
        this.timer = setTimeout(() => {
          this.timer = null;
          if (this.queuedMessage) {
            this._commit(this.queuedMessage);
            this.queuedMessage = null;
          }
        }, this.throttleMs - (now - this.lastAnnouncementTime));
      }
      return;
    }

    this._commit(message);
  }

  _commit(message) {
    this.lastAnnouncementTime = Date.now();
    // Clearing text briefly triggers screen readers to re-read identical content
    this.container.textContent = '';
    requestAnimationFrame(() => {
      if (this.container) {
        this.container.textContent = message;
      }
    });
  }

  /**
   * AF-001 Compliant Streaming Announcer:
   * Protects screen reader speech synthesizers during generative AI token streaming.
   * Decouples rapid visual DOM updates (50-120ms) from assistive announcements.
   */
  startStreaming(startMessage = 'بدأ توليد المحتوى...') {
    this.announce(startMessage);
  }

  updateStreamingProgress(progressMessage, intervalMs = 3000) {
    const now = Date.now();
    if (now - this.lastAnnouncementTime >= intervalMs) {
      this.announce(progressMessage);
    }
  }

  completeStreaming(completeMessage = 'اكتمل توليد المحتوى. المسودة جاهزة للمراجعة.') {
    // Immediate flush on completion
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
    this._commit(completeMessage);
  }

  destroy() {
    if (this.timer) {
      clearTimeout(this.timer);
    }
    if (this.container && this.container.parentNode) {
      this.container.parentNode.removeChild(this.container);
    }
    this.container = null;
  }
}

// Global default instances
let defaultPolite = null;
let defaultAssertive = null;

function announcePolite(message) {
  if (!defaultPolite) defaultPolite = new LiveRegion({ mode: 'polite' });
  defaultPolite.announce(message);
}

function announceAssertive(message) {
  if (!defaultAssertive) defaultAssertive = new LiveRegion({ mode: 'assertive' });
  defaultAssertive.announce(message);
}

// Declarative Custom Element: <mds-live-region mode="polite">
if (typeof customElements !== 'undefined' && !customElements.get('mds-live-region')) {
  customElements.define(
    'mds-live-region',
    class MDSLiveRegionElement extends HTMLElement {
      connectedCallback() {
        const mode = this.getAttribute('mode') || 'polite';
        this.setAttribute('role', mode === 'assertive' ? 'alert' : 'status');
        this.setAttribute('aria-live', mode);
        this.setAttribute('aria-atomic', 'true');
        if (!this.classList.contains('mds-visually-hidden')) {
          this.classList.add('mds-visually-hidden');
        }
      }

      announce(text) {
        this.textContent = '';
        requestAnimationFrame(() => {
          this.textContent = text;
        });
      }
    }
  );
}


  return { FocusTrap, LiveRegion };
}));
