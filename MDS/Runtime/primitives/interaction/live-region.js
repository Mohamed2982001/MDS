/**
 * MDS (Master Design System) — LiveRegion Accessibility Primitive
 * Architecture Layer: Layer 03 (Primitives / Accessibility)
 * Standard: W3C WAI-ARIA Dynamic Announcements & Screen Reader Speech Buffer Protection
 * Addresses Architectural Finding: AF-001 (Decoupled Streaming Speech Throttling)
 */

export class LiveRegion {
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

export function announcePolite(message) {
  if (!defaultPolite) defaultPolite = new LiveRegion({ mode: 'polite' });
  defaultPolite.announce(message);
}

export function announceAssertive(message) {
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
