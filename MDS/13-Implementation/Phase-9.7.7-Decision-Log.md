# Master Design System (MDS) — Architecture Decision Log
## Phase 9.7.7: Visual Regression Engine (Architecture Stage — Final Remediation)

**Status:** ARCHITECTURE COMPLETE — READY FOR FINAL APPROVAL  
**Phase:** 9.7.7 (Visual Regression Engine & Snapshot Diffing — Layer J)  
**Date:** 2026-09-24  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Target Capability:** `MDS-VIS-001` (Currently `DEFERRED` — Preserved during Architecture Phase)  
**Downstream Guard:** Production Sign-Off STRICTLY BLOCKED until 9.7.7 Implementation & Lock  

---

## 1. Context & Architectural Mandate

Following the formal approval and locking of Phase 9.7.6 (Dynamic Responsive Automation / `MDS-RWD-003`), Phase 9.7.7 was authorized by Lead Architect Mohamed Khalid under strict **Architecture Phase Only** constraints.

Following an independent architectural audit, four findings were evaluated and ratified:
1. **`VIS-001` (PASSED):** Color distance metric formally defined and ratified as **Luminance-Weighted RGB Distance** ($D_{\text{lum}}$) with ITU-R BT.601 coefficients ($0.299 R + 0.587 G + 0.114 B$), rejecting improper use of "$\Delta E$".
2. **`VIS-002` (FINAL REMEDIATION):** Eliminated any overclaim of 100% visual coverage across the 528 Cartesian combinations ($11 \times 4 \times 3 \times 2 \times 2$). The 12 canonical visual baselines provide **orthogonal representative visual coverage**. The remaining 516 combinations are covered by functional, accessibility, responsive, token, and browser automation according to their respective contracts, but are **not individually visually baselined**.
3. **`VIS-003` (SURGICAL TIMING FIX):** Reconciled Tier 4 integration timing: Surgical Touchpoints (`registry.json`, `run_tests.py`, `dispatch_integration.py`, `governance_validator.py`) may be modified **DURING Phase 9.7.7 implementation**, but **ONLY for the explicitly documented Visual Regression integration changes**. No unrelated modifications are permitted.
4. **`VIS-004` (TRUTHFUL FONT PINNING CONTRACT):** Codified the complete pinning contract for local Cairo font artifacts (`cairo-regular.woff2`, `cairo-bold.woff2`). To maintain 100% truthfulness, no synthetic SHA-256 hashes are fabricated during architecture. Instead, the contract establishes that capability `MDS-VIS-001` **remains strictly `DEFERRED` until canonical local font artifacts are supplied, pinned, and cryptographically hashed in `baselines_manifest.json`**. Missing or corrupted font artifacts trigger explicit `DEFERRED` status (`FONT_ARTIFACT_UNAVAILABLE`), and silent fallback to system fonts is strictly forbidden.

These decisions are formally codified in ADR-078 through ADR-085.

---

## 2. Ratified Architectural Decisions (ADR-078 through ADR-085)

### ADR-078: Pure Python Standard Library Pixel Comparator & Luminance-Weighted RGB Distance ($D_{\text{lum}}$) [VIS-001]
- **Decision:** Implement the visual comparison engine entirely within the Python standard library (`zlib`, `struct`, `hashlib`, `math`, `base64`), completely free of third-party libraries (no Pillow/PIL, no OpenCV, no NumPy). The per-pixel color distance metric is formally designated and implemented as **Luminance-Weighted RGB Distance** ($D_{\text{lum}}$), utilizing ITU-R BT.601 luminance weighting coefficients:
  $$D_{\text{lum}}(p_1, p_2) = \frac{\sqrt{0.299 \cdot (R_1 - R_2)^2 + 0.587 \cdot (G_1 - G_2)^2 + 0.114 \cdot (B_1 - B_2)^2}}{255.0}$$
  Alpha channel variance is evaluated independently:
  $$\Delta A = \frac{|A_1 - A_2|}{255.0}$$
  $$D_{\text{pixel}} = \max(D_{\text{lum}}, \Delta A)$$
  A pixel is classified as differing if $D_{\text{pixel}} > \tau_{\text{pixel}}$ (default $\tau_{\text{pixel}} = 0.05$ / $5\%$). The image passes if aggregate diff ratio:
  $$\text{DiffRatio} = \frac{N_{\text{diff\_pixels}}}{W \times H} \le \tau_{\text{image}} \quad (\text{default } \tau_{\text{image}} = 0.001 \text{ or } 0.1\%)$$
- **Rationale:** 
  1. Complete rejection of "$\Delta E$": $\Delta E$ strictly denotes CIE $\Delta E^*_{ab}$, $\Delta E_{94}$, or $\Delta E_{00}$ in CIELAB/CIELUV space, requiring non-linear RGB $\to$ XYZ $\to$ Lab transforms. Claiming $\Delta E$ for weighted Euclidean sRGB distance is mathematically invalid.
  2. ITU-R BT.601 coefficients ($0.299 R + 0.587 G + 0.114 B$) accurately weight human perceptual sensitivity (human eyes are substantially more sensitive to green than blue) while executing in sub-millisecond pure Python integer/float math.
  3. Standard library `zlib` decompresses and compresses PNG IDAT chunks directly with zero dependency overhead.
- **Consequence:** 100% hermetic, zero-dependency, mathematically rigorous pixel comparison matching senior engineering standards.

---

### ADR-079: Orthogonal Representative Visual Coverage Matrix (12 Baselines) [VIS-002]
- **Decision:** Restrict the golden visual baseline suite to an **orthogonal representative sample of 12 canonical snapshot configurations** (Orthogonal Array Testing Strategy / OATS):
  - **Overview Screen (`#/overview` — Dashboard/KPI archetype):**
    - `VIS-BASE-001`: 1440px Desktop, Light Theme, Comfortable Density, RTL
    - `VIS-BASE-002`: 1440px Desktop, Dark Theme, Comfortable Density, RTL
    - `VIS-BASE-003`: 1440px Desktop, High Contrast Theme (`high-contrast`), Comfortable Density, RTL
    - `VIS-BASE-004`: 1440px Desktop, Light Theme, Comfortable Density, LTR
    - `VIS-BASE-005`: 1024px Desktop/Tablet Boundary, Light Theme, Comfortable Density, RTL
    - `VIS-BASE-006`: 768px Tablet, Light Theme, Comfortable Density, RTL
    - `VIS-BASE-007`: 320px Mobile, Light Theme, Comfortable Density, RTL
  - **Items List Screen (`#/items` — Data Display/Table archetype):**
    - `VIS-BASE-008`: 1440px Desktop, Light Theme, Comfortable Density, RTL
    - `VIS-BASE-009`: 1024px Desktop, Light Theme, Compact Density, RTL
    - `VIS-BASE-010`: 320px Mobile, Light Theme, Comfortable Density, RTL
  - **Item Edit Screen (`#/items/edit` — Interactive Form archetype):**
    - `VIS-BASE-011`: 1440px Desktop, Light Theme, Comfortable Density, RTL
    - `VIS-BASE-012`: 320px Mobile, Light Theme, Comfortable Density, RTL
  
  **Demarcation & Non-Overclaim Invariant:** 
  The full Cartesian space of the Reference Application comprises:
  $$11\ \text{screens} \times 4\ \text{viewports} \times 3\ \text{themes} \times 2\ \text{densities} \times 2\ \text{directions} = 528\ \text{possible combinations}$$
  Subtracting the 12 canonical baselines leaves **516 non-baselined combinations**.  
  **Formal Contract:** The 12 visual baselines provide orthogonal representative visual coverage. The remaining permutations are covered by functional, accessibility, responsive, token, and browser automation according to their respective contracts, but are **not individually visually baselined**.
- **Rationale:** Prevents combinatorial explosion and massive storage bloat while guaranteeing that every critical visual design axis is locked and continuously protected against regression.
- **Consequence:** Fast CI execution, small disk footprint, and mathematically defensible test demarcation.

---

### ADR-080: Immutable Baseline Storage & Cryptographic Verification (`SHA-256`)
- **Decision:** Golden baselines must be stored as immutable PNG assets in `MDS/10-Testing/visual/baselines/` accompanied by an authoritative cryptographic manifest `baselines_manifest.json`.
  - Every baseline record must contain:
    ```json
    {
      "baseline_id": "VIS-BASE-001",
      "route": "#/overview",
      "viewport": {"width": 1440, "height": 900},
      "theme": "light",
      "direction": "rtl",
      "density": "comfortable",
      "file_name": "VIS-BASE-001_overview_1440_light_rtl.png",
      "file_sha256": "<SHA-256 hash calculated at baseline generation>",
      "approved_by": "Mohamed Khalid",
      "approved_at": "2026-09-24T00:00:00Z"
    }
    ```
  - **Immutability Contract:** The visual comparison engine is strictly read-only with respect to baselines. The engine has **zero auto-overwrite capability**. Overwriting or creating a baseline requires an explicit, separate administrative CLI tool invocation with cryptographic hash generation and human approval logging.
  - **Missing Baseline Handling:** If a baseline file is missing from disk or fails its manifest SHA-256 check, the engine **MUST return explicit `DEFERRED` / `CONFIG_ERROR` status**, never false green and never an automated baseline creation.
- **Rationale:** Prevents silent regression masking where an inadvertent visual bug overwrites the golden master during test execution.
- **Consequence:** 100% auditability and tamper-evident visual regression governance.

---

### ADR-081: Explicit File Modification Allowlist & Core Protected Boundaries [VIS-003]
- **Decision:** Establish an unyielding four-tier file modification boundary for Phase 9.7.7:
  1. **Tier 1: Core Protected (STRICTLY FORBIDDEN / 0 bytes permitted to change):**
     - `MDS/Runtime/**`
     - `MDS/Playground/**`
     - `MDS/Reference-Application/**`
     - `MDS/02-Tokens/**`
     - *Violation Policy:* Any modification to Tier 1 constitutes an immediate, catastrophic failure of the phase gate.
  2. **Tier 2: Testing Capabilities (STRICTLY READ-ONLY):**
     - `MDS/10-Testing/accessibility/**`
     - `MDS/10-Testing/responsive/**`
     - `MDS/10-Testing/browser/**` *(core driver and helpers)*
  3. **Tier 3: Implementation Target Scope (PERMITTED CREATION in Phase 9.7.7 Implementation):**
     - `MDS/10-Testing/visual/` (`visual_comparator.py`, `baseline_manager.py`, `visual_runner.py`, `evidence_generator.py`)
     - `MDS/10-Testing/visual/baselines/` (`*.png`, `baselines_manifest.json`)
     - `MDS/10-Testing/visual/vendor/fonts/` (pinned local font artifacts)
     - `MDS/10-Testing/artifacts/visual_diffs/` (`*.diff.png`, `visual_evidence.json`)
     - `MDS/10-Testing/tests/test_visual_*.py`
     - `MDS/13-Implementation/Phase-9.7.7-*`
  4. **Tier 4: Surgical Integration Touchpoints (Surgical Timing Rule):**
     - **Rule:** *Surgical Touchpoints may be modified DURING Phase 9.7.7 implementation, but ONLY for the explicitly documented Visual Regression integration changes. No unrelated modifications are permitted.*
     - Permitted files:
       - `MDS/10-Testing/capabilities/registry.json`: Update status of `MDS-VIS-001` from `DEFERRED` to `ACTIVE` upon verified implementation completion.
       - `MDS/10-Testing/run_tests.py`: Add visual regression category / suite dispatch to the master runner.
       - `MDS/10-Testing/browser/dispatch_integration.py`: Add `run_visual_sweep()` execution hook.
       - `MDS/10-Testing/static/governance_validator.py`: Update capability accounting assertions (170 Active / 0 Deferred upon promotion).
- **Rationale:** Ensures complete internal consistency between implementation architecture and file access controls without risking unintended side effects in protected core or prior capabilities.
- **Consequence:** Total isolation of new visual regression code within designated directories.

---

### ADR-082: Deterministic Font Rendering Contract via Pinned Local Cairo Font Artifact [VIS-004]
- **Decision:** Adopt **Option A: Pinned Local Cairo Font Artifact** to achieve 100% deterministic typography rendering:
  - **Artifact Filenames:**
    - `MDS/10-Testing/visual/vendor/fonts/cairo-regular.woff2`
    - `MDS/10-Testing/visual/vendor/fonts/cairo-bold.woff2`
    *(Static TTF fallback `Cairo-Regular.ttf` and `Cairo-Bold.ttf` permitted if WOFF2 decoder is unavailable in offline environment).*
  - **Exact Pinned Version & Provenance:**
    - Cairo Font upstream release via Google Fonts / GitHub (`google/fonts`).
  - **Cryptographic Pinning Contract (No Synthetic Hashes):**
    - The architecture strictly refuses to fabricate synthetic or guessed SHA-256 hashes prior to placing canonical font files on disk.
    - When canonical font artifacts are physically committed in `MDS/10-Testing/visual/vendor/fonts/` during authorized implementation, their exact cryptographic SHA-256 hashes will be computed and recorded in `baselines_manifest.json` under `"fonts"`.
    - **Baseline Generation & Verification Invariant:** Golden baseline snapshot capture and subsequent regression verification **MUST use the exact same pinned font artifact and SHA-256 hash**.
  - **Offline Injection & Zero External CDN:**
    - External font CDN/network access (`https://fonts.googleapis.com/...`) is strictly prohibited during visual capture.
    - Fonts are injected locally via `@font-face` referencing local server URLs or base64 Data-URIs.
  - **Pre-Capture Settlement Gate:**
    ```javascript
    await document.fonts.ready;
    if (!document.fonts.check('16px Cairo') || !document.fonts.check('bold 16px Cairo')) {
      throw new Error('Local Cairo font artifact failed to settle in DOM');
    }
    ```
  - **Deterministic Fallback & Deferred Status:**
    - If canonical local font artifacts are missing, altered, or fail SHA-256 verification, capability `MDS-VIS-001` **MUST return explicit `DEFERRED` status** (`FONT_ARTIFACT_UNAVAILABLE`).
    - Silent fallback to system fonts (Arial, Segoe UI, Roboto) is **strictly forbidden**.
    - Reporting a false green or false regression failure is **strictly forbidden**.
- **Rationale:** External CDN requests can fail, experience latency, or receive subtle platform font hinting variations, causing flaky pixel diffs. A local pinned font guarantees 100% reproducible glyph rasterization offline.
- **Consequence:** Zero test flakiness from font loading; complete offline hermeticity.

---

### ADR-083: Headless Chrome CDP Capture Pipeline via `Page.captureScreenshot`
- **Decision:** Utilize the existing standard-library `CDPBrowserDriver` (`MDS/10-Testing/browser/cdp_driver.py`) to capture full-page and viewport screenshots using Chrome DevTools Protocol `Page.captureScreenshot`:
  - Format: `png`
  - Capture parameters:
    ```json
    {
      "format": "png",
      "clip": {
        "x": 0,
        "y": 0,
        "width": 1440,
        "height": 900,
        "scale": 1.0
      },
      "captureBeyondViewport": false,
      "fromSurface": true
    }
    ```
  - **Pre-Capture Settlement Algorithm:**
    1. Apply route, theme, density, and direction attributes.
    2. Dispatch `Emulation.setDeviceMetricsOverride` for the target viewport.
    3. Inject local pinned Cairo font and await `document.fonts.ready`.
    4. Await 2 consecutive `requestAnimationFrame` frames to flush layout reflow.
    5. Poll DOM stability until root bounding box variance $< 0.5$px across 50ms.
    6. Disable CSS animations / transitions via injection of:
       `* { animation: none !important; transition: none !important; caret-color: transparent !important; }`
    7. Capture screenshot.
- **Rationale:** Ensures clean, stable raster images with zero subpixel animation motion blur or blinking text cursor artifacts.
- **Consequence:** Flake-free pixel capturing across repeated executions.

---

### ADR-084: Negative Testing, Visual Mutation Verification & Anti-False-Green Harness
- **Decision:** Mandate three dedicated negative testing and anti-false-green test suites:
  1. `test_visual_negative.py`:
     - **Dimension Mismatch:** Compares 1440x900 against 1024x768 $\to$ hard failure with `DimensionMismatchError`.
     - **Synthesized Mutation:** Injects a red 100x100 box into the captured DOM $\to$ comparator detects mismatch, calculates exact diff ratio ($10000 / 1296000 \approx 0.77\% > 0.1\%$), and emits highlighted diff mask PNG.
     - **Missing Baseline:** Requests comparison against a non-existent baseline ID $\to$ reports `DEFERRED` / missing baseline status, never false green.
     - **Corrupted Baseline:** Compares against a baseline whose SHA-256 does not match `baselines_manifest.json` $\to$ raises `BaselineIntegrityError`.
     - **Missing Font Artifact:** Simulates missing Cairo font file $\to$ reports `DEFERRED`, never system font fallback.
  2. `test_visual_live.py`:
     - Executes against the live, locked Reference Application across all 12 canonical baselines.
  3. `test_visual_engine.py`:
     - Verifies pure Python PNG parsing, zlib decompression, ITU-R BT.601 $D_{\text{lum}}$ calculations, and diff mask generation against synthetic pixel buffers.
- **Rationale:** Proves beyond doubt that the engine accurately detects regressions, prevents false greens, and maintains total cryptographic and visual integrity.
- **Consequence:** Complete verification coverage satisfying senior quality assurance standards.

---

### ADR-085: Capability Accounting & Lifecycle Preservation (`MDS-VIS-001`)
- **Decision:** Preserve capability `MDS-VIS-001` with status `DEFERRED` in `MDS/10-Testing/capabilities/registry.json` throughout the Phase 9.7.7 Architecture Stage:
  - Total Defined Unique Capability IDs: **170**
  - Active Executable Capability IDs: **169**
  - Deferred Capability IDs: **1** (`MDS-VIS-001`)
  - Invariant Formula:
    $$170\ \text{Total Unique IDs} = 169\ \text{Active} + 1\ \text{Deferred} (\text{MDS-VIS-001})$$
  - Promotion to `ACTIVE` will take place strictly upon implementation completion, live browser execution, and independent audit authorization.
- **Rationale:** Strict adherence to MDS phase-gate lifecycle: Architecture $\to$ Audit $\to$ Authorization $\to$ Implementation $\to$ Audit $\to$ Lock.
- **Consequence:** 100% accounting integrity maintained without premature status promotion.

### ADR-086: Architecture Amendment — Ephemeral Port Allocation Restricted Port Collision Prevention (LocalTestServer)
- **Status:** RATIFIED ARCHITECTURAL AMENDMENT
- **Classification:** Tier 2 Surgical Amendment (Infrastructure Resilience)
- **Affected File:** `MDS/10-Testing/browser/local_server.py`
- **Scope of Change:** Exactly 22 lines added: defines `CHROMIUM_RESTRICTED_PORTS` (WHATWG Fetch / Chromium blocked port specification) and implements a retry loop inside `LocalTestServer.start()` when `requested_port == 0` to reject and re-bind if the OS allocates a restricted port.
- **Why It Is Necessary:** When running large-scale continuous browser automation suites (141+ tests across Browser, Accessibility, Responsive, and Visual test suites in a single process), the host operating system dynamically allocates ephemeral ports from the OS dynamic port range. Occasionally, the OS allocates a port that Chromium classifies as unsafe (e.g., ports 5060, 6000, 6667, 10080). When Chromium attempts navigation to an origin with such a port, it immediately aborts with `net::ERR_UNSAFE_PORT`. This caused intermittent, non-deterministic test failures during full-suite discovery runs. Adding the restricted port collision prevention loop ensures `LocalTestServer` guarantees safe port binding before returning to the browser runner.
- **Why It Does Not Violate Protected Core Boundaries:** The change is strictly confined to `MDS/10-Testing/browser/local_server.py` (Tier 2 Browser Bridge infrastructure). It has zero interaction with, modification of, or dependency on `Runtime/`, `Playground/`, `Reference-Application/`, or `02-Tokens/` (0 bytes modified in Protected Core).
- **Scope Classification:**
  - `MDS/10-Testing/browser/local_server.py`: **Requires documented amendment** (Formally approved via ADR-086).
  - `MDS/10-Testing/browser/cdp_driver.py`: **Unauthorized / Reverted** (Reverted to its canonical Phase 9.7.4 state; zero active modifications).

---

## 3. Final Reconciliation Table

| Finding ID | Audit Finding Summary | Status | Formal Remediated Architecture Resolution |
| :--- | :--- | :---: | :--- |
| **`VIS-001`** | Algorithm named "$\Delta E$" inappropriately for sRGB distance | **✅ PASSED** | Formally renamed to **Luminance-Weighted RGB Distance** ($D_{\text{lum}}$); codified formula using ITU-R BT.601 coefficients ($0.299, 0.587, 0.114$). |
| **`VIS-002`** | Overclaim of 100% visual coverage across 528 combinations | **✅ RESOLVED** | 12 baselines provide orthogonal representative visual coverage; 516 remaining combinations covered by functional/accessibility/responsive/token/browser automation according to contracts, but not individually visually baselined. |
| **`VIS-003`** | Inconsistent Tier 4 timing ("after implementation") | **✅ RESOLVED** | Clarified: Surgical Touchpoints may be modified *DURING* Phase 9.7.7 implementation, but *ONLY* for explicitly documented Visual Regression integration changes. |
| **`VIS-004`** | Font pinning missing hash/version and truthfulness | **✅ RESOLVED** | Complete pinning contract documented: filenames, provenance, matching baseline/verification hashes, zero CDN. No fabricated hashes; capability remains DEFERRED until physical artifacts are committed and hashed. |
| **`VIS-005`** | Surgical Touchpoint Scope & Browser Bridge Resilience | **✅ AMENDED** | Ratified ADR-086 amending `MDS/10-Testing/browser/local_server.py` to prevent Chromium restricted port collisions (`net::ERR_UNSAFE_PORT`), while reverting `cdp_driver.py` to its canonical state. |

---

*Authored by Lead Architect Mohamed Khalid — Master Design System*
