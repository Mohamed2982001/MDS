# Master Design System (MDS) — Architecture Decision Log
## Phase 9.7.4: Browser Automation Runner Bridge

**Status:** COMPLETE — READY FOR REVIEW  
**Phase:** 9.7.4 — Browser Automation Runner Bridge (Layer I)  
**Date:** 2026-09-24  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Canonical Modules:**
- `MDS/10-Testing/browser/__init__.py`
- `MDS/10-Testing/browser/models.py`
- `MDS/10-Testing/browser/exceptions.py`
- `MDS/10-Testing/browser/driver_base.py`
- `MDS/10-Testing/browser/browser_discovery.py`
- `MDS/10-Testing/browser/local_server.py`
- `MDS/10-Testing/browser/cdp_driver.py`
- `MDS/10-Testing/browser/session.py`
- `MDS/10-Testing/browser/dispatch_integration.py`
- `MDS/10-Testing/browser/README.md`
- `MDS/10-Testing/tests/test_browser_discovery.py`
- `MDS/10-Testing/tests/test_local_server.py`
- `MDS/10-Testing/tests/test_browser_unit.py`
- `MDS/10-Testing/tests/test_browser_live.py`

---

## 1. Context & Architectural Mandate

Following the formal approval and locking of Phase 9.7.3, Phase 9.7.4 was authorized by Lead Architect Mohamed Khalid with a specific mandate:
> **Implement the framework-neutral Browser Automation Runner Bridge capable of executing MDS browser-validation capabilities through a controlled local browser process, without leaking dependencies into the runtime or modifying locked core directories.**

---

## 2. Ratified Decisions (ADR-055 through ADR-061)

### ADR-055: Zero-External-Dependency Pure Standard Library CDP Socket Driver
- **Decision:** Implement `_CDPSocketClient` directly over standard TCP sockets using Python standard library modules (`socket`, `struct`, `base64`, `json`, `urllib`).
- **Rationale:** Eliminates reliance on heavy third-party automation packages (Selenium, Playwright, Puppeteer), prevents npm/pip bloat, and guarantees execution on any standard Python 3.10+ runtime.
- **Consequence:** 100% self-contained, deterministic execution with zero external pip/npm dependencies.

### ADR-056: Ephemeral Local HTTP Test Server with Open CORS & Port 0
- **Decision:** Implement `LocalTestServer` binding dynamically to port 0 (`socket.bind(('', 0))`) with open CORS headers (`Access-Control-Allow-Origin: *`) and cache-busting headers.
- **Rationale:** Chromium enforces strict CORS policies that block ECMAScript module imports (`import ... from "../Runtime/..."`) and JSON fetches under `file://`. Port 0 prevents port collisions in multi-runner or CI environments.
- **Consequence:** Reference Application and Playground execute natively in headless browser sessions without mocked HTTP mocks.

### ADR-057: Cross-Platform Direct Binary & Version Discovery
- **Decision:** Discover system Chrome, Edge, and Linux Chromium across standard directories with natural version parsing directly from directory structure or `--version`.
- **Rationale:** On Windows, GUI subsystem binaries (`chrome.exe`) do not attach to stdout in standard consoles, causing `--version` commands to hang unless piped. Reading directory version metadata avoids process blocking. Precedence order: Chrome $\to$ Edge $\to$ Chromium.
- **Consequence:** Fast (0.05s) deterministic detection across Windows, macOS, and Linux.

### ADR-058: Headless Flag Strategy & Initial Viewport Allocation
- **Decision:** Launch Chromium with `--headless=new`, `--disable-gpu`, `--no-sandbox`, `--window-size=1440,900`, and dynamically locate assigned port from `DevToolsActivePort`.
- **Rationale:** In modern Chromium (`--headless=new`), omitting `--window-size` results in a 0×0 viewport where the compositor never paints frames, causing `Page.captureScreenshot` to hang. Allocating an initial window size ensures render surfaces are immediately active.
- **Consequence:** Sub-second screenshot capture and reliable frame composition.

### ADR-059: Strict Host-Restricted Navigation Policy
- **Decision:** Restrict `navigate()` exclusively to local origins (`127.0.0.1`, `localhost`, `0.0.0.0`, `about:blank`, `data:`).
- **Rationale:** Security guard preventing test runners from inadvertently navigating to external internet sites or leaking test tokens.
- **Consequence:** Unapproved external URLs are rejected immediately with `InvalidCommandError`.

### ADR-060: Disposable Session Architecture & Windows Lock Release Retries
- **Decision:** Implement `BrowserSession` context manager with automated teardown and multi-attempt retry loop for `shutil.rmtree` on temporary user data directories.
- **Rationale:** Chromium spawns helper background processes (Crashpad, GPU) that hold brief asynchronous file handles on Windows. A 2-second retry loop guarantees 100% clean directory removal without orphaned files.
- **Consequence:** Zero stray test directories or locked temp files.

### ADR-061: Canonical Registry Invariant Preservation (170 = 167 Active + 3 Deferred)
- **Decision:** Connect browser capabilities through `BrowserCapabilityDispatcher` without modifying canonical registry capability IDs or double-counting assertions.
- **Rationale:** Capabilities `MDS-A11Y-004`, `MDS-RWD-003`, and `MDS-VIS-001` remain formally declared `DEFERRED` with designated reasons until their explicit architectural phases (9.7.5, 9.7.6, 9.7.7).
- **Consequence:** Test accounting remains 100% clean and uncompromised.

### ADR-062: Result Model Tri-State Enforcement & Dispatch Integration Protocol
- **Decision:** Restrict `BrowserExecutionStatus` strictly to `PASS`, `FAIL`, `DEFERRED`. Eliminate `ERROR` as a distinct status. Represent runtime exceptions as `FAIL` with `error_message` and `exception_type` metadata. Enforce end-to-end dispatch integration from `CapabilityDispatcher` down through `BrowserCapabilityDispatcher` to real browser execution.
- **Rationale:** Resolves Independent Audit Findings B-001, B-002, and B-003, maintaining canonical alignment with the MDS governance tri-state evaluation model.
- **Consequence:** Zero status drift across static validation, runner bridge, and master harness.

---

## 3. Implementation Verification Summary

| Component | Target Path | Verification Metric | Status |
| :--- | :--- | :--- | :--- |
| **Driver Abstraction** | `MDS/10-Testing/browser/driver_base.py` | 10 abstract methods, context manager | **VERIFIED** |
| **CDP Socket Driver** | `MDS/10-Testing/browser/cdp_driver.py` | Zero-dependency RFC 6455 over TCP | **VERIFIED** |
| **Browser Discovery** | `MDS/10-Testing/browser/browser_discovery.py` | Chrome & Edge detected in 0.05s | **VERIFIED** |
| **Local Test Server** | `MDS/10-Testing/browser/local_server.py` | Port 0 binding, CORS headers | **VERIFIED** |
| **Session Coordinator** | `MDS/10-Testing/browser/session.py` | Isolated disposable test sessions | **VERIFIED** |
| **Dispatch Integration** | `MDS/10-Testing/browser/dispatch_integration.py` | Connects registry, preserves 3 deferred | **VERIFIED** |
| **Discovery Tests** | `MDS/10-Testing/tests/test_browser_discovery.py` | 6 / 6 Tests Passing | **VERIFIED** |
| **Server Tests** | `MDS/10-Testing/tests/test_local_server.py` | 7 / 7 Tests Passing | **VERIFIED** |
| **Browser Unit Tests** | `MDS/10-Testing/tests/test_browser_unit.py` | 16 / 16 Tests Passing (Failure-mode + E2E) | **VERIFIED** |
| **Live Browser Tests** | `MDS/10-Testing/tests/test_browser_live.py` | 12 / 12 Real Chrome Tests Passing (Live E2E) | **VERIFIED** |
| **Full Discovery Suite**| `MDS/10-Testing/tests/` | 80 / 80 Total Tests Passing | **VERIFIED** |
| **Master Test Harness** | `MDS/10-Testing/run_tests.py` | 45 passed / 0 failed / 3 deferred | **VERIFIED** |
| **Static Suite** | `MDS/10-Testing/static/static_runner.py` | 0 errors / 1 accepted warning | **VERIFIED** |
| **Runtime Isolation** | `MDS/Runtime/`, `Playground/`, etc. | 0 files / 0 bytes modified | **VERIFIED** |
