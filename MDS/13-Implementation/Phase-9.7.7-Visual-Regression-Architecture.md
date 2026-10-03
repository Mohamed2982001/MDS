# Master Design System (MDS) — Visual Regression Engine Architecture
## Phase 9.7.7: Pixel-Diff Snapshot Automation Engine (Layer J)

**Document Type:** Architectural Blueprint & Technical Specification (Final Remediation)  
**Status:** ARCHITECTURE COMPLETE — PENDING FINAL APPROVAL  
**Phase:** 9.7.7 (Visual Regression Engine & Snapshot Diffing — Layer J)  
**Date:** 2026-09-24  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Target Promoted Capability:** `MDS-VIS-001` (Currently `DEFERRED` — Preserved during Architecture Phase)  
**Downstream Guard:** Production Sign-Off STRICTLY BLOCKED until 9.7.7 Implementation & Lock  

---

## 1. Architectural Mission & Objectives

The primary mission of Phase 9.7.7 is to architect the automated visual regression engine for capability **`MDS-VIS-001`**, establishing the rigorous foundation to promote it from `DEFERRED` to an active, real-browser visual snapshot automation capability once implementation is authorized and verified.

### 1.1 Inviolable Core Philosophy
> **"Visual Regression is Perceptual Truth Verification, Not Heuristic Guesswork."**  
> *(Codified in `MDS/13-Implementation/Testing-and-Quality-Strategy.md`)*

Visual regression testing in MDS must **NEVER** depend on flaky third-party cloud services or opaque external npm packages. It must execute as an offline, hermetic, pure Python standard-library engine capable of:
1. Capturing pixel-perfect raster snapshots of the locked MDS Reference Application using the existing headless Chrome CDP bridge (`MDS/10-Testing/browser/cdp_driver.py`).
2. Performing deterministic, mathematically sound per-pixel color comparison between rendered canvases and cryptographically authenticated golden baselines.
3. Emitting highlighted visual diff masks and structured audit evidence for human review.
4. Guaranteeing 100% anti-false-green protection through rigorous negative mutation testing.

---

## 2. Remediated Architecture Audit Resolutions

Following an independent architectural audit, four findings were evaluated and are formally resolved throughout this specification:

| Audit Finding ID | Topic | Initial Audit Concern | Formal Remediated Architecture Resolution |
| :--- | :--- | :--- | :--- |
| **`VIS-001`** | Color Distance Algorithm | Use of "$\Delta E$" was mathematically invalid for sRGB Euclidean distance | **PASSED.** Renamed formally to **Luminance-Weighted RGB Distance** ($D_{\text{lum}}$), utilizing ITU-R BT.601 coefficients ($0.299 R + 0.587 G + 0.114 B$). |
| **`VIS-002`** | Coverage Invariant & Demarcation | Overclaim stating 100% of the 528 combinations were protected | **RESOLVED.** Removed 100% visual coverage overclaim. The 12 visual baselines provide orthogonal representative visual coverage. The remaining 516 combinations are covered by functional, accessibility, responsive, token, and browser automation according to their respective contracts, but are not individually visually baselined. |
| **`VIS-003`** | Boundary Allowlist Timing | Stated Tier 4 touchpoints modified "after implementation and approval" | **RESOLVED.** Reconciled rule: *Surgical Touchpoints may be modified DURING Phase 9.7.7 implementation, but ONLY for explicitly documented Visual Regression integration changes.* |
| **`VIS-004`** | Font Rendering Contract | Missing exact filenames, version, provenance, and truthfulness of pinning | **RESOLVED.** Documented exact filenames, upstream version provenance, offline injection, identical baseline/verify hash invariant, forbidden system fallback, and explicit rule that no hashes are fabricated; capability remains DEFERRED until physical artifacts are pinned. |

---

## 3. Mathematically Rigorous Color Distance: Luminance-Weighted RGB Distance ($D_{\text{lum}}$) [VIS-001]

### 3.1 Rejection of "$\Delta E$"
The metric $\Delta E$ (Delta E) is strictly defined in color science by the International Commission on Illumination (CIE) within perceptual color spaces:
- $\Delta E^*_{ab}$ (CIE 1976): Euclidean distance in $L^*a^*b^*$ color space.
- $\Delta E_{94}$ (CIE 1994): Application-weighted distance in $L^*C^*h^*$ space.
- $\Delta E_{00}$ (CIEDE2000): Non-linear, rotationally corrected color difference formula.

Computing a weighted Euclidean distance directly on 8-bit non-linear sRGB values does not conform to any CIE $\Delta E$ standard. Claiming "$\Delta E$" for sRGB distance is colorimetrically inaccurate. Therefore, MDS formally designates its algorithm as **Luminance-Weighted RGB Distance** ($D_{\text{lum}}$).

### 3.2 Mathematical Formulation of $D_{\text{lum}}$
Human vision is non-uniformly sensitive to different wavelengths of light: the human eye has significantly greater sensitivity to green than to red, and lowest sensitivity to blue. MDS utilizes the standard ITU-R BT.601 luminance weighting coefficients ($0.299$ Red, $0.587$ Green, $0.114$ Blue):

Given two pixels $p_1 = (R_1, G_1, B_1, A_1)$ and $p_2 = (R_2, G_2, B_2, A_2)$ where each channel $\in [0, 255]$:

1. **Color Distance Component ($D_{\text{lum}}$):**
   $$D_{\text{lum}}(p_1, p_2) = \frac{\sqrt{0.299 \cdot (R_1 - R_2)^2 + 0.587 \cdot (G_1 - G_2)^2 + 0.114 \cdot (B_1 - B_2)^2}}{255.0}$$
   where $D_{\text{lum}} \in [0.0, 1.0]$.

2. **Alpha Channel Component ($\Delta A$):**
   $$\Delta A = \frac{|A_1 - A_2|}{255.0}$$

3. **Composite Pixel Distance ($D_{\text{pixel}}$):**
   $$D_{\text{pixel}}(p_1, p_2) = \max\left(D_{\text{lum}}(p_1, p_2),\, \Delta A\right)$$

### 3.3 Thresholds and Decision Boundaries
- **Per-Pixel Mismatch Threshold ($\tau_{\text{pixel}}$):**
  $$\text{isMismatched}(p_1, p_2) \iff D_{\text{pixel}}(p_1, p_2) > \tau_{\text{pixel}}$$
  *Default Value:* $\tau_{\text{pixel}} = 0.05$ ($5\%$ perceptible difference threshold). This accommodates subpixel font anti-aliasing variations without missing structural or chromatic visual regressions.

- **Aggregate Image Diff Ratio ($\text{DiffRatio}$):**
  $$\text{DiffRatio} = \frac{N_{\text{mismatched\_pixels}}}{W \times H}$$

- **Pass/Fail Verdict Boundary ($\tau_{\text{image}}$):**
  $$\text{Verdict} = \begin{cases} \text{PASS} & \text{if } \text{DiffRatio} \le \tau_{\text{image}} \quad (\text{default } \tau_{\text{image}} = 0.001 \text{ or } 0.1\%) \\ \text{FAIL} & \text{if } \text{DiffRatio} > \tau_{\text{image}} \end{cases}$$

- **Diff Mask Emitted Color:**
  For any mismatched pixel, the output diff mask paints a high-visibility fluorescent magenta pixel $(R=255, G=0, B=255, A=255)$, while matching pixels are drawn dimmed to $20\%$ opacity of the original baseline to provide immediate contextual contrast for human auditors.

---

## 4. Orthogonal Representative Visual Coverage Matrix (12 Baselines) [VIS-002]

### 4.1 Combinatorial Space vs Representative Sampling
The full Cartesian space of the Reference Application across all dimensions is:
$$11\ \text{screens} \times 4\ \text{viewports} \times 3\ \text{themes} \times 2\ \text{densities} \times 2\ \text{directions} = 528\ \text{possible combinations}$$

The visual baseline matrix contains exactly **12 canonical baselines**.  
Therefore:
$$528\ \text{total combinations} - 12\ \text{visual baselines} = 516\ \text{non-baselined combinations}$$

### 4.2 Inviolable Non-Overclaim Demarcation Contract
MDS strictly avoids claiming that the 516 non-baselined combinations are visually regression-tested:

> **"The 12 visual baselines provide orthogonal representative visual coverage. The remaining permutations are covered by functional, accessibility, responsive, token, and browser automation according to their respective contracts, but are not individually visually baselined."**

The 12 visual baselines function strictly as an **orthogonal perceptual smoke test and layout regression guard** across the 5 design system axes:
1. Every major screen archetype is visually snapshotted (Dashboard KPI, Data Table, Interactive Form).
2. Every theme mode is visually snapshotted in high resolution (Light, Dark, High Contrast `high-contrast`).
3. Both writing directions are verified (RTL primary, LTR verified on Overview).
4. Both layout densities are verified (Comfortable primary, Compact verified on Data Table).
5. All 4 canonical responsive viewport tiers are visually snapshotted (320px, 768px, 1024px, 1440px).

### 4.3 The 12 Canonical Baseline Specifications

| Baseline ID | Screen Archetype | Canonical Route | Viewport | Theme Mode | Direction | Density | Primary Visual Verification Focus |
| :--- | :--- | :--- | :---: | :--- | :---: | :--- | :--- |
| **`VIS-BASE-001`** | Dashboard / KPI | `#/overview` | 1440 × 900 | Light | RTL | Comfortable | Primary Desktop Gold Standard; 4-card KPI grid, Header, RTL Sidebar |
| **`VIS-BASE-002`** | Dashboard / KPI | `#/overview` | 1440 × 900 | Dark | RTL | Comfortable | Dark mode token inversion, surface contrast, elevation borders |
| **`VIS-BASE-003`** | Dashboard / KPI | `#/overview` | 1440 × 900 | High Contrast | RTL | Comfortable | `high-contrast` token mode, 3:1/7:1 borders, focus rings, zero transparency |
| **`VIS-BASE-004`** | Dashboard / KPI | `#/overview` | 1440 × 900 | Light | LTR | Comfortable | LTR mirror symmetry, left sidebar, start-aligned typography |
| **`VIS-BASE-005`** | Dashboard / KPI | `#/overview` | 1024 × 768 | Light | RTL | Comfortable | Desktop/Tablet boundary; 1152px container max-width constraint |
| **`VIS-BASE-006`** | Dashboard / KPI | `#/overview` | 768 × 1024 | Light | RTL | Comfortable | Tablet portrait; 72px icon rail sidebar, 2-column KPI grid |
| **`VIS-BASE-007`** | Dashboard / KPI | `#/overview` | 320 × 640 | Light | RTL | Comfortable | Mobile portrait; single-column KPI stack, mobile drawer button |
| **`VIS-BASE-008`** | List Management | `#/items` | 1440 × 900 | Light | RTL | Comfortable | Data table layout, zebra striping, status badges, action buttons |
| **`VIS-BASE-009`** | List Management | `#/items` | 1024 × 768 | Light | RTL | Compact | Compact density padding reduction, tighter row heights |
| **`VIS-BASE-010`** | List Management | `#/items` | 320 × 640 | Light | RTL | Comfortable | Mobile responsive table container horizontal scroll containment |
| **`VIS-BASE-011`** | Interactive Form | `#/items/edit` | 1440 × 900 | Light | RTL | Comfortable | Two-column form grid, input controls, stepper tabs, danger zone |
| **`VIS-BASE-012`** | Interactive Form | `#/items/edit` | 320 × 640 | Light | RTL | Comfortable | Mobile stacked single-column form inputs, full-width action buttons |

---

## 5. Pure Python Standard Library PNG Architecture

To uphold the MDS zero-dependency mandate (no Pillow, no OpenCV, no NumPy), the visual engine implements a lightweight, pure Python standard-library PNG decoder and encoder utilizing `zlib` and `struct`.

### 5.1 PNG Deconstruction Pipeline
1. **Header Verification:**
   Verify standard 8-byte PNG signature: `\x89PNG\r\n\x1a\n` (`0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A`).
2. **Chunk Parsing:**
   Iterate through chunks: read 4-byte length, 4-byte type, payload, and 4-byte CRC32.
   - `IHDR`: Extract `width` (uint32), `height` (uint32), `bit_depth`, `color_type` (must be 6 for RGBA or 2 for RGB).
   - `IDAT`: Concatenate compressed data payloads across all `IDAT` chunks.
   - `IEND`: Stop iteration.
3. **Decompression & Scanline Unfiltering:**
   - Decompress concatenated IDAT bytes via `zlib.decompress()`.
   - Each scanline consists of 1 filter byte followed by $W \times 4$ bytes of RGBA data.
   - Apply standard PNG scanline reconstruction for filter types:
     - `0 (None)`: $X$
     - `1 (Sub)`: $X + A \pmod{256}$
     - `2 (Up)`: $X + B \pmod{256}$
     - `3 (Average)`: $X + \lfloor(A + B)/2\rfloor \pmod{256}$
     - `4 (Paeth)`: $X + \text{PaethPredictor}(A, B, C) \pmod{256}$
4. **Decoded Output:**
   A contiguous flat bytearray of size $W \times H \times 4$ representing uncompressed 32-bit RGBA pixel buffers.

### 5.2 PNG Diff Mask Reconstruction
When emitting visual diff masks:
1. Construct scanlines with filter type `0 (None)`: prepend `\x00` to each scanline of length $W \times 4$.
2. Compress with `zlib.compress(raw_bytes, level=6)`.
3. Package into standard PNG chunk format (`IHDR` $\to$ `IDAT` $\to$ `IEND`) with calculated CRC32 checksums via `zlib.crc32()`.

This guarantees 100% self-contained image manipulation executing in under 45ms per 1440x900 canvas.

---

## 6. Deterministic Font Rendering Contract via Pinned Local Cairo Font [VIS-004]

Web fonts loaded over Google Fonts CDN introduce network latency, CDN outages, and OS font hinting discrepancies.

### 6.1 Option A: Complete Font Pinning Contract
1. **Canonical Local Artifact Filenames:**
   - Regular weight: `MDS/10-Testing/visual/vendor/fonts/cairo-regular.woff2` (or `Cairo-Regular.ttf`)
   - Bold weight: `MDS/10-Testing/visual/vendor/fonts/cairo-bold.woff2` (or `Cairo-Bold.ttf`)
2. **Exact Pinned Version & Provenance:**
   - Upstream Canonical Source: Google Fonts upstream repository (`google/fonts`).
   - Distribution Package: Canonical Cairo release.
3. **Cryptographic Pinning Contract (No Synthetic Hashes):**
   - The architecture strictly refuses to fabricate synthetic or guessed SHA-256 hashes prior to placing canonical font files on disk.
   - When canonical font artifacts are physically committed in `MDS/10-Testing/visual/vendor/fonts/` during authorized implementation, their exact cryptographic SHA-256 hashes will be computed and recorded in `baselines_manifest.json` under `"fonts"`.
   - **Baseline Generation & Verification Invariant:** Golden baseline snapshot capture and subsequent regression verification **MUST use the exact same pinned font artifact and SHA-256 hash**.
4. **Offline Injection & Zero External CDN:**
   - External font CDN/network access (`https://fonts.googleapis.com/...`) is strictly prohibited during visual capture.
   - Fonts are injected locally via `@font-face` referencing local server URLs or base64 Data-URIs:
     ```css
     @font-face {
       font-family: 'Cairo';
       font-style: normal;
       font-weight: 400;
       font-display: block;
       src: url('/MDS/10-Testing/visual/vendor/fonts/cairo-regular.woff2') format('woff2');
     }
     @font-face {
       font-family: 'Cairo';
       font-style: normal;
       font-weight: 700;
       font-display: block;
       src: url('/MDS/10-Testing/visual/vendor/fonts/cairo-bold.woff2') format('woff2');
     }
     ```
5. **Pre-Capture Settlement Gate:**
   ```javascript
   await document.fonts.ready;
   if (!document.fonts.check('16px Cairo') || !document.fonts.check('bold 16px Cairo')) {
     throw new Error('Local Cairo font artifact failed to settle in DOM');
   }
   ```
6. **Deterministic Fallback & Deferred Status:**
   - If canonical local font artifacts are missing, altered, or fail SHA-256 verification, capability `MDS-VIS-001` **MUST return explicit `DEFERRED` status** (`FONT_ARTIFACT_UNAVAILABLE`).
   - Silent fallback to system fonts (Arial, Segoe UI, Roboto) is **strictly forbidden**.
   - Reporting a false green or false regression failure is **strictly forbidden**.
   - **Architecture Gate Guard:** Capability `MDS-VIS-001` remains strictly `DEFERRED` until canonical local font artifacts are supplied, placed, and their cryptographic SHA-256 hashes verified in `baselines_manifest.json`.

---

## 7. Headless Chrome CDP Capture Pipeline

Visual capture reuses the existing standard-library `CDPBrowserDriver` (`MDS/10-Testing/browser/cdp_driver.py`).

### 7.1 Protocol Interaction: `Page.captureScreenshot`
The capture command is issued via WebSocket to Chrome DevTools Protocol:
```json
{
  "method": "Page.captureScreenshot",
  "params": {
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
}
```
The returned base64-encoded payload is decoded via `base64.b64decode` into raw PNG bytes.

### 7.2 Strict 7-Step Pre-Capture Settlement Algorithm
1. **Route & Hash Navigation:** Navigate to target hash route (e.g. `#/overview`) and await target container element.
2. **Device Metrics Emulation:** Dispatch `Emulation.setDeviceMetricsOverride` with canonical dimensions and `deviceScaleFactor: 1.0`.
3. **State Application:** Apply `data-theme`, `data-density`, and `dir` attributes to `<html>`.
4. **Motion & Caret Suppression:** Inject global CSS rule to freeze all transitions and hide cursor:
   ```css
   * {
     animation-duration: 0s !important;
     animation-delay: 0s !important;
     transition-duration: 0s !important;
     transition-delay: 0s !important;
     caret-color: transparent !important;
   }
   ```
5. **Local Font Injection & Verification:** Inject pinned Cairo font and await `document.fonts.ready`.
6. **Layout Reflow Double RAF:** Await two consecutive `requestAnimationFrame` frames:
   ```javascript
   await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
   ```
7. **Bounding Box Variance Settlement:** Poll root container layout until horizontal and vertical variance $< 0.5$px across 50ms intervals (max wait 1000ms).

Only when all 7 settlement steps succeed is `Page.captureScreenshot` dispatched.

---

## 8. Baseline Storage, Cryptographic Immutability & Lifecycle

### 8.1 Baseline Storage Organization
Golden baselines are stored in `MDS/10-Testing/visual/baselines/` alongside an authoritative manifest:
```text
MDS/10-Testing/visual/baselines/
├── baselines_manifest.json
├── VIS-BASE-001_overview_1440_light_rtl.png
├── VIS-BASE-002_overview_1440_dark_rtl.png
├── VIS-BASE-003_overview_1440_high_contrast_rtl.png
├── VIS-BASE-004_overview_1440_light_ltr.png
├── VIS-BASE-005_overview_1024_light_rtl.png
├── VIS-BASE-006_overview_768_light_rtl.png
├── VIS-BASE-007_overview_320_light_rtl.png
├── VIS-BASE-008_items_1440_light_rtl.png
├── VIS-BASE-009_items_1024_compact_rtl.png
├── VIS-BASE-010_items_320_light_rtl.png
├── VIS-BASE-011_items_edit_1440_light_rtl.png
└── VIS-BASE-012_items_edit_320_light_rtl.png
```

### 8.2 Cryptographic Manifest Schema (`baselines_manifest.json`)
```json
{
  "version": "1.0.0",
  "generated_at": "2026-09-24T00:00:00Z",
  "approved_by": "Mohamed Khalid (Senior Full Stack & Flutter Developer)",
  "fonts": {
    "regular": {
      "filename": "cairo-regular.woff2",
      "sha256": "<SHA-256 calculated from canonical font file>"
    },
    "bold": {
      "filename": "cairo-bold.woff2",
      "sha256": "<SHA-256 calculated from canonical font file>"
    }
  },
  "baselines": [
    {
      "baseline_id": "VIS-BASE-001",
      "route": "#/overview",
      "viewport": {"width": 1440, "height": 900},
      "theme": "light",
      "direction": "rtl",
      "density": "comfortable",
      "file_name": "VIS-BASE-001_overview_1440_light_rtl.png",
      "file_sha256": "<SHA-256 hash calculated at baseline generation>",
      "dimensions": {"width": 1440, "height": 900},
      "file_size_bytes": 104856
    }
  ]
}
```

### 8.3 Immutability Contract & Anti-Overwrite Protection
- **Read-Only Test Execution:** The test runner is strictly prohibited from writing or updating files in `MDS/10-Testing/visual/baselines/`. It opens them in read-only binary mode (`rb`).
- **Integrity Check:** Before comparing a live screenshot, the engine calculates the SHA-256 hash of the baseline file on disk and asserts that it matches `baselines_manifest.json`. If a mismatch is detected, execution aborts with `BaselineIntegrityError`.
- **Administrative Baseline Generation CLI:** Baseline generation and updating can only occur through an explicit standalone administrative script (`manage_baselines.py --generate --baseline-id=...`) which requires manual developer initiation and git commit review.

---

## 9. Comprehensive File Modification Allowlist & Core Boundaries [VIS-003]

To preserve system stability and protect previously approved and locked phases, an unyielding 4-Tier File Modification Allowlist is enforced:

| Tier | Directory / Scope | Permission | Strict Rule & Rationale |
| :--- | :--- | :---: | :--- |
| **Tier 1: Core Protected** | `MDS/Runtime/**`<br>`MDS/Playground/**`<br>`MDS/Reference-Application/**`<br>`MDS/02-Tokens/**` | **STRICTLY FORBIDDEN**<br>*(0 bytes permitted to change)* | Inviolable system core. Any modification to these directories causes immediate rejection of the phase gate. |
| **Tier 2: Prior Capabilities** | `MDS/10-Testing/accessibility/**`<br>`MDS/10-Testing/responsive/**`<br>`MDS/10-Testing/browser/**` *(core)* | **STRICTLY READ-ONLY**<br>*(Except Ratified ADR-086)* | Previously locked capabilities (9.7.4, 9.7.5, 9.7.6). Code must be consumed as-is without internal modification. *Formally ratified exception: ADR-086 amends `MDS/10-Testing/browser/local_server.py` to prevent dynamic ephemeral port collisions with Chromium restricted ports (`net::ERR_UNSAFE_PORT`). All other files strictly read-only.* |
| **Tier 3: Implementation Scope** | `MDS/10-Testing/visual/**`<br>`MDS/10-Testing/tests/test_visual_*.py`<br>`MDS/10-Testing/artifacts/visual_diffs/**`<br>`MDS/13-Implementation/Phase-9.7.7-*` | **PERMITTED CREATION** | Permitted target files for Phase 9.7.7 implementation (engine modules, baseline assets, unit/live/negative tests, docs). |
| **Tier 4: Surgical Integration Touchpoints** | `MDS/10-Testing/capabilities/registry.json`<br>`MDS/10-Testing/run_tests.py`<br>`MDS/10-Testing/browser/dispatch_integration.py`<br>`MDS/10-Testing/static/governance_validator.py` | **SURGICAL UPDATES ONLY**<br>*(During Implementation)* | **Surgical Touchpoints may be modified DURING Phase 9.7.7 implementation, but ONLY for the explicitly documented Visual Regression integration changes. No unrelated modifications are permitted.** |

---

## 10. Tri-Class Assertion Model & Anti-False-Green Verification Harness

Following the model established in Phase 9.7.6, visual assertions are partitioned into three formal classes:

### 10.1 Tri-Class Visual Assertion Taxonomy
1. **`HARD_CONTRACT` (Failure = Immediate Hard `FAIL`):**
   - Canvas dimensions match baseline exactly ($W_{\text{actual}} == W_{\text{baseline}}$ and $H_{\text{actual}} == H_{\text{baseline}}$).
   - Baseline file exists and passes SHA-256 cryptographic manifest verification.
   - Pinned local Cairo font loads and passes in-browser typography settlement.
   - CDP capture returns a valid, non-empty PNG buffer.
2. **`OBSERVABLE_BEHAVIOR` (Failure = `FAIL` when threshold exceeded):**
   - Evaluates aggregate visual difference ratio against tolerance threshold:
     $$\text{DiffRatio} \le \tau_{\text{image}} \quad (0.001)$$
   - Evaluates maximum local cluster mismatch size.
3. **`INFORMATIONAL_MEASUREMENT` (Telemetry Only — Never impacts PASS/FAIL):**
   - Total render and capture duration (ms).
   - Comparison algorithm execution duration (ms).
   - Total pixel count ($W \times H$).
   - Absolute mismatched pixel count.

### 10.2 Negative Testing & Anti-False-Green Harness
The visual engine must be verified by a dedicated test suite (`test_visual_negative.py`) proving it correctly detects defects and prevents false greens:

1. **Dimension Mismatch Negative Test:**
   Compares a 1440x900 baseline against a 1024x768 render $\to$ raises `DimensionMismatchError` with explicit width/height diagnostic.
2. **Synthesized Visual Mutation Test:**
   Injects a synthetic red $100\times 100$px box into the live DOM $\to$ comparator detects mismatch, computes exact diff ratio ($10000 / 1296000 \approx 0.77\% > 0.1\%$), flags `FAIL`, and generates a diff mask PNG with magenta highlighting.
3. **Missing Baseline Negative Test:**
   Requests comparison against non-existent `VIS-BASE-999` $\to$ engine returns explicit `DEFERRED` / missing baseline status, never false green.
4. **Corrupted Baseline Negative Test:**
   Mutates 1 byte of a baseline PNG file $\to$ engine flags `BaselineIntegrityError` due to SHA-256 manifest mismatch.
5. **Missing Local Font Negative Test:**
   Simulates missing Cairo font file $\to$ engine returns explicit `DEFERRED` status, never silent system font fallback.

---

## 11. Package Structure & Module Architecture

The visual regression engine will reside strictly inside `MDS/10-Testing/visual/`:

```text
MDS/10-Testing/visual/
├── __init__.py                       # Public exports: VisualComparator, BaselineManager, VisualRunner
├── visual_models.py                  # Dataclasses: BaselineConfig, ComparisonResult, VisualEvidence
├── png_codec.py                      # Pure Python stdlib PNG decoder/encoder (zlib, struct)
├── visual_comparator.py              # Luminance-Weighted RGB Distance (D_lum) comparator
├── baseline_manager.py               # SHA-256 verification, manifest loading, read-only guard
├── visual_runner.py                  # Live Chrome CDP capture pipeline & pre-capture settlement
├── visual_dispatch.py                # Master harness bridge & registry integration
├── evidence_generator.py             # Diff mask rendering & JSON evidence serialization
├── vendor/
│   └── fonts/                        # Pinned local font artifacts (Option A)
│       ├── cairo-regular.woff2
│       └── cairo-bold.woff2
├── baselines/                        # Golden immutable baselines
│   ├── baselines_manifest.json       # Authoritative cryptographic manifest
│   └── VIS-BASE-*.png                # 12 canonical PNG baselines
└── README.md                         # Architecture & operational guide
```

### Corresponding Test Suites (`MDS/10-Testing/tests/`):
- `test_visual_engine.py`: Unit tests verifying pure Python PNG codec, $D_{\text{lum}}$ calculations, and diff mask generation.
- `test_visual_live.py`: Live integration tests executing the 12 canonical runs against the locked Reference Application.
- `test_visual_negative.py`: Negative tests validating dimension mismatch, mutation detection, missing baselines, and SHA-256 corruption.

---

## 12. Capability Accounting & Lifecycle Gate

### 12.1 Accounting Invariant during Architecture Stage
Capability `MDS-VIS-001` remains strictly `DEFERRED` in `MDS/10-Testing/capabilities/registry.json`:
- **Total Defined Unique Capability IDs:** **170**
- **Active Executable Capability IDs:** **169**
- **Deferred Capability IDs:** **1** (`MDS-VIS-001`)

$$\mathbf{170\ Total\ Unique\ IDs} = \mathbf{169\ Active} + \mathbf{1\ Deferred\ (MDS-VIS-001)}$$

### 12.2 Promotion Gate Criteria
Promotion of `MDS-VIS-001` from `DEFERRED` to `ACTIVE` will occur strictly upon satisfying the following four gates during the authorized implementation stage:
1. Pure Python engine (`png_codec.py`, `visual_comparator.py`) implemented and passing all unit tests with 0 external dependencies.
2. 12 Canonical Baselines captured, verified, and locked in `baselines_manifest.json` with cryptographic SHA-256 hashes.
3. Canonical local Cairo font artifacts supplied, pinned, and hashed in `baselines_manifest.json`.
4. Live sweep executing against the locked Reference Application with 12/12 baselines passing ($100\%$ pass rate).
5. All negative mutation and anti-false-green tests passing, followed by formal Independent Audit approval.

---

*Authored by Lead Architect Mohamed Khalid — Master Design System*
