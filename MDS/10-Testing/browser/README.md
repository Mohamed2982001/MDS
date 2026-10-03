# Master Design System (MDS) — Browser Automation Runner Bridge
## Layer I: Headless Browser Driver & Execution Bridge

**Module Reference:** `MDS-BROWSER-BRIDGE`  
**Phase:** 9.7.4 — Browser Automation Runner Bridge  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Layer:** `MDS/10-Testing/browser/`  
**Status:** PHASE 9.7.4 COMPLETE — READY FOR REVIEW  

---

## 1. Architectural Mission & Overview

The **MDS Browser Automation Runner Bridge** establishes a framework-neutral, dependency-free automation engine capable of executing live DOM, layout reflow, accessibility, and visual assertions against the Master Design System reference runtime and applications.

### Core Architectural Invariants:
1. **Zero Runtime Leakage:** 0 browser automation dependencies leak into `MDS/Runtime/`, `MDS/Playground/`, `MDS/Reference-Application/`, or `MDS/02-Tokens/`. All testing infrastructure is strictly quarantined within `MDS/10-Testing/`.
2. **Pure Standard-Library Communication:** Communicates with Chromium binaries over standard TCP sockets using a synchronous RFC 6455 WebSocket client implemented in Python standard library (`socket`, `struct`, `base64`, `json`). Zero external pip or npm packages required.
3. **Deterministic Subprocess Supervision:** Browser processes are spawned headlessly with isolated ephemeral user data directories (`--user-data-dir`), eliminating profile contamination and ensuring guaranteed cleanup.
4. **Ephemeral Local HTTP Server:** Starts an on-demand, non-privileged HTTP daemon (`LocalTestServer`) binding to port 0 with open CORS headers (`Access-Control-Allow-Origin: *`) to satisfy browser CORS policies for native ES module imports (`import ... from "../Runtime/..."`).
5. **Zero False-Green Mandate:** When no browser binary is installed on the host, tests are explicitly declared `DEFERRED` with reason. Passes are never simulated or fabricated.

---

## 2. Component Architecture

```text
MDS/10-Testing/browser/
├── __init__.py               # Public package exports
├── models.py                 # Value models: Viewport, BrowserInfo, BrowserCapabilityResult
├── exceptions.py             # Domain exception hierarchy (BrowserBridgeError, etc.)
├── driver_base.py            # Abstract driver contract (BrowserDriverBase)
├── browser_discovery.py      # Cross-platform browser detector (Chrome, Edge, Chromium)
├── local_server.py           # Ephemeral HTTP daemon with open CORS headers
├── cdp_driver.py             # Chromium CDP driver over standard TCP sockets
├── session.py                # High-level test session context manager
├── dispatch_integration.py   # Registry dispatch integration bridge
└── README.md                 # Architectural reference and guide
```

---

## 3. The 10 Driver Methods Contract

Any compliant MDS browser driver implements the standard `BrowserDriverBase` interface:

| # | Method Signature | Operational Contract |
| :-: | :--- | :--- |
| 1 | `launch(headless=True, port=0)` | Spawns headless browser subprocess, reads `DevToolsActivePort`, connects CDP. |
| 2 | `navigate(url)` | Validates local origin, dispatches `Page.navigate`, waits for `readyState === 'complete'`. |
| 3 | `set_viewport(w, h, dsf=1.0)` | Calls `Emulation.setDeviceMetricsOverride` and stores active `Viewport`. |
| 4 | `click(selector, timeout_ms=5000)` | Waits for element, scrolls into view, and dispatches native click event. |
| 5 | `type_text(selector, text, timeout_ms=5000)` | Focuses element, sets `.value`, and fires `input` and `change` events. |
| 6 | `wait_for(selector, timeout_ms=5000)` | Polls DOM until element matching selector exists in document. |
| 7 | `screenshot(output_path=None) -> bytes` | Captures raster PNG snapshot via `Page.captureScreenshot` (format: PNG). |
| 8 | `evaluate(script) -> Any` | Evaluates JavaScript in global page context and returns serialized value. |
| 9 | `get_console_logs() -> List[ConsoleLogEntry]` | Returns all captured console logs, warnings, and uncaught exceptions. |
| 10 | `close()` | Sends `Browser.close`, terminates subprocess, and removes temp user data directory. |

---

## 4. Browser Discovery Matrix

`BrowserDiscovery` automatically identifies compatible binaries across operating systems:

- **Windows:**
  - Google Chrome: `%ProgramFiles%\Google\Chrome\Application\chrome.exe`, `%ProgramFiles(x86)%`, `%LocalAppData%`.
  - Microsoft Edge: `%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe`, `%ProgramFiles%`.
  - Version inspection: Directly parses version directory without console blocking.
- **Linux:** `/usr/bin/google-chrome`, `/usr/bin/google-chrome-stable`, `/usr/bin/chromium`, `/snap/bin/chromium`.
- **macOS:** `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`, `/Applications/Microsoft Edge.app`.
- **System PATH:** Scans `PATH` for `chrome`, `google-chrome`, `msedge`, `chromium`.

Precedence Order: **Google Chrome $\to$ Microsoft Edge $\to$ Chromium**.

---

## 5. Security & Safety Controls

1. **Origin Restriction:** Navigation is strictly restricted to local hosts (`127.0.0.1`, `localhost`, `0.0.0.0`, `about:blank`, `data:`). External network requests are rejected by `InvalidCommandError`.
2. **Session Isolation:** Each session creates a unique temporary directory via `tempfile.mkdtemp(prefix="mds_browser_")` and guarantees deletion in `close()` and `__del__()`.
3. **Execution Safety:** JavaScript evaluation handles errors gracefully by wrapping thrown exceptions in `CDPCommandError` without crashing the Python runner.

---

## 6. Canonical Registry Integration & Downstream Compatibility

The browser bridge connects to the Capability Registry without altering test accounting:

$$\mathbf{170\ \text{Total Unique Defined IDs}} = \mathbf{167\ \text{Active Executable Assertions}} + \mathbf{3\ \text{Deferred Capabilities}}$$

The 3 deferred capabilities remain formally preserved until their dedicated phases:
- `MDS-A11Y-004`: Dynamic axe-core accessibility injection (Scheduled for Phase 9.7.5).
- `MDS-RWD-003`: Multi-viewport automated reflow testing (Scheduled for Phase 9.7.6).
- `MDS-VIS-001`: 12-baseline visual pixel diffing engine (Scheduled for Phase 9.7.7).

When dispatched, `BrowserCapabilityDispatcher` returns `BrowserExecutionStatus.DEFERRED` with explicit environment reason, ensuring zero false passes.
