# Agent Rule: Security & UI Hardening Standards

Derived from core security principles and threat modeling standards (referencing `D:\Work\Dev\Security Prompts.txt`):

## 1. Input & Form Security
- **Never Trust the Client:** Client-side validation in MDS input components is purely for user experience. Components must visually display server-side validation and sanitization errors seamlessly.
- **XSS & HTML Injection Prevention:**
  - All typography and rich text primitives must safely escape HTML/raw strings by default.
  - Markdown or rich-text rendering must pass through strict AST sanitizers.
- **Icon & SVG Sanitization:**
  - SVG icons must be stripped of `<script>`, `onload`, and inline event attributes prior to rendering.

## 2. Secrets & Sensitive Data Handling
- **Zero Secrets in Code/Repo:** Never hardcode API keys, tokens, or credentials in any component or example.
- **Sensitive Inputs:**
  - Password inputs must support masking, visibility toggling, and disable autocomplete on sensitive operational codes (OTP, CVV) when instructed.
  - Prevent accidental leakage of sensitive tokens in browser dev tools, clipboard, or local storage.

## 3. UI Resistance to Abuse
- **Rate-Limiting & Brute-Force Feedback:**
  - Auth components and action buttons must support debouncing, disabled states during inflight requests, and visual countdowns when encountering rate-limiting (HTTP 429).
- **IDOR & Broken Access Control Awareness:**
  - When rendering administrative or user-specific components, ensure authorization guards hide or disable controls and the UI gracefully reflects `403 Forbidden` / `401 Unauthorized` states without exposing protected data structures.
