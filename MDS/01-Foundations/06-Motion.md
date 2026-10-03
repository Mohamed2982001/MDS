# MDS Foundation: Motion & Interaction Timing Specification
**Foundational Layer:** 01-Foundations  
**Status:** APPROVED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Executive Summary & Core Principle

> **"Motion should explain change, not decorate it."**

In MDS, animation is a functional communication tool that provides instant interaction feedback, establishes spatial continuity, and clarifies structural state transitions. Gratuitous bounces, playful wobbles, and slow decorative reveals are strictly forbidden.

---

## 2. Calibrated Transition Durations

| Token | Milliseconds | Usage & Component Assignment |
| :--- | :---: | :--- |
| `motion.duration.instant` | 0ms   | Immediate feedback, hard state resets, reduced-motion overrides |
| `motion.duration.fast`    | 150ms | Micro-interactions: button hover/press, checkbox toggle, focus ring fade |
| `motion.duration.normal`  | 250ms | Standard UI transitions: accordion expansion, dropdown menu open, tooltip reveal |
| `motion.duration.slow`    | 350ms | Macro structural transitions: modal dialog pop-in, side sheet slide-in, page route transition |

---

## 3. Calibrated Easing Curves (Platform-Agnostic)

MDS utilizes natural, physics-inspired deceleration curves that prioritize quick user response:

| Token | Cubic-Bezier Curve | Curve Coordinates | Role & Behavioral Physics |
| :--- | :--- | :---: | :--- |
| `motion.easing.standard` | `cubic-bezier(0.2, 0.0, 0.0, 1.0)` | `[0.2, 0.0, 0.0, 1.0]` | Elements moving between two stable visible positions |
| `motion.easing.enter`    | `cubic-bezier(0.0, 0.0, 0.2, 1.0)` | `[0.0, 0.0, 0.2, 1.0]` | Deceleration curve; enters rapidly and settles smoothly |
| `motion.easing.exit`     | `cubic-bezier(0.4, 0.0, 1.0, 1.0)` | `[0.4, 0.0, 1.0, 1.0]` | Acceleration curve; leaves promptly without lingering |

---

## 4. Reduced Motion & Accessibility Standard

Assistive technology and vestibular disorder safeguards are first-class:
- **Canonical Behavior:** Under user reduced-motion preference (`prefers-reduced-motion: reduce` or accessibility settings), all spatial translation animations (slide, scale, bounce) are **disabled**.
- **Tokenized Fallback:** All animated transitions collapse directly to `motion.duration.instant` (**0ms**), or optionally an implementation-level discrete cross-fade.

---

## 5. AI Agent States & Continuous Loop Timings (Proposed Domain)

AI-native interaction behaviors use discrete transition tokens for entry/exit and continuous cycle timings for ambient tasks:

| AI Agent State | Motion Role | Timing Specification | Status |
| :--- | :--- | :--- | :--- |
| **Completed** | Entry Transition | 150ms (`motion.duration.fast`, `motion.easing.enter`) | Active Token |
| **Error Shake** | Alert Transition | 150ms (`motion.duration.fast`) | Active Token |
| **Working (Spinner)** | Continuous Loop | 1000ms linear continuous rotation | Deferred (Future Phase) |
| **Thinking (Shimmer)**| Ambient Pulse | 1500ms cycle (`cubic-bezier(0.4, 0, 0.6, 1)`) | Deferred (Future Phase) |
| **Streaming (Token)** | Ingestion Cadence| 80ms per-token visual reveal | Implementation Cadence |

> **Architectural Boundary Note:** Continuous loop cycle timings (1000ms / 1500ms) are distinct from state transition durations. They are tracked as Proposal 1 (`motion.loop.*`) with status **DEFERRED — FUTURE PHASE**, to be evaluated when concrete Loading, AI, and Streaming components are designed in Phase 5. They are NOT added to the active token repository.
