<!-- Classification: CURRENT_SPECIFICATION -->
# Master Design System (MDS) — Architecture Decision Log
## Phase 10.3: Production Artifact Compilation & Zero-NPM Distribution

**Document Reference:** `MDS-DEC-10.3-REV4`  
**Phase:** 10.3 (Production Artifact Compilation & Zero-NPM Distribution)  
**Layer:** Layer 13 (Implementation, Tooling & Operationalization)  
**Date:** 2026-10-02  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Audit Stage:** Strict Independent Architecture Audit Final Micro-Remediation (REV4)  
**Status:** **DRAFT (ARCHITECTURE STAGE REMEDIATION REV4) — AWAITING INDEPENDENT ARCHITECTURE AUDIT**  
**Execution Context:** Microsoft Windows, Google Chrome v153, Python 3.12.8 (Pure Standard Library)  
**Implementation Guard:** Phase 10.3 Implementation STRICTLY BLOCKED until Independent Architecture Audit approval  

---

## 1. Context & Architectural Mandate

Following the formal seal of **Phase 10.2 (MDS Agent Bootstrap & Handoff Contract)**, the Master Design System possesses a verified mathematical selection engine (`mds-dsse`), an inviolable 5-layer authority model, and a canonical onboarding contract for AI coding agents (`MDS_AGENT_BOOTSTRAP.md`). Phase 10.3 establishes the architectural decisions for the Production Compilation Pipeline, the Zero-NPM Distribution Model, standalone Python stdlib tooling, cryptographic manifests, deterministic archives, and project-agent distribution contracts.

Following the final Independent Architecture Audit evaluation, this revision (`REV4`) codifies the definitive micro-remediations closing the remaining architectural gaps:
1. **Source Manifest Cryptographic Trust Chain (ADR-206 / G-011):** Binds `canonical_source_manifest.json` cryptographically to the locked MDS Governance Root Trust Anchor (`trust_anchor.json` / `MDS-ROOT-ANCHOR-v1`) via `source_trust_binding.json` and a compiled authoritative constant.
2. **Exact Canonical 61 Source vs 94 Protected Core Partition Law (ADR-207 / G-012-A):** Formally reconciles `Runtime/css/` against informal `Runtime/core` aliases, enumerates all 61 canonical filesystem paths and 33 non-sources, and mathematically proves the partition ($\mathbf{ProtectedCore} = \mathbf{CompilationSourceSet} \cup \mathbf{ProtectedNonSourceSet}, \mathbf{CompilationSourceSet} \cap \mathbf{ProtectedNonSourceSet} = \emptyset$).
3. **Complete Build Environment Determinism & Eight-Tier Build Identity Model (ADR-212 / G-013-A):** Invariant: "Every input capable of changing generated artifact bytes MUST either be represented in Build Identity OR be explicitly prohibited/pinned by the reproducibility contract." Defines $I_{build} = \text{SHA-256}(I_{src} : I_{cmp} : I_{cfg} : I_{env} : \text{str}(T_{epoch}))$ with pinned Python 3.12.x runtime, stdlib archive engines, POSIX codepoint ordering, UTF-8/LF normalization, and UTC/C.UTF-8 locale.
4. **Reproducible Build Epoch Dual-Mode Contract (ADR-211 / G-014):** Enforces explicit `SOURCE_DATE_EPOCH` injection in reproducible mode with zero silent Git fallbacks, paired with complete archive metadata normalization.
5. **Strict Read-Only Bootstrap Distribution Gate (ADR-210):** Codifies `verify` as an exclusively read-only precondition before Step 8 code synthesis.

This Decision Log codifies Architectural Decision Records **ADR-189 through ADR-212**.

---

## 2. Ratified Architectural Decisions (ADR-189 through ADR-212)

### ADR-189: Unified Standalone Production Compiler Architecture (`tools/compiler/`)
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** The compilation engine will be built as a standalone, modular package housed in `tools/compiler/`:
  - `cli.py`: Command-line routing and deterministic exit code dispatch.
  - `engine.py`: 6-stage transactional compilation pipeline orchestrator.
  - `token_compiler.py`: DTCG parser, DAG dependency resolver, and cycle detector.
  - `css_bundler.py`: Cascade Layer scoping, concatenation, and line-ending normalizer.
  - `js_bundler.py`: Custom Elements packager, IIFE/ESM wrappers.
  - `manifest_generator.py`: SHA-256 hasher and distribution manifest builder.
  - `packager.py`: Deterministic archive creator (`.zip`, `.tar.gz`).
  - `validator.py`: Pre/post verification and Protected Core integrity validator.
- **Boundary Law:** `tools/compiler/` is completely decoupled from the 94 Protected Core files and the Historical Phase Guard. It is strictly a compiler and packager.

---

### ADR-190: Zero-NPM Distribution Model & Standards-Based Web Runtime
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** MDS establishes a strict **Zero-NPM Distribution Model** partitioned across three domains:
  1. *Zero-NPM Runtime:* The compiled web assets (`dist/`) require 0 Node.js / npm runtime dependencies and execute in any standard web browser.
  2. *Zero-NPM & Zero-Pip Tooling:* The compiler (`tools/compiler/`) executes using pure Python 3.12+ standard library with 0 pip packages.
  3. *Zero-NPM Consumption:* Downstream web projects can consume MDS via direct file drops without `package.json` or `npm install`.
- **Runtime Standards:** The runtime is built on W3C standards: CSS Cascade Layers (`@layer`), CSS Custom Properties (`--mds-*`), Native HTML5 Custom Elements (`<mds-dialog>`, `<mds-switch>`, `<mds-tabs>`, `<mds-tooltip>`), and WAI-ARIA interaction patterns.

---

### ADR-191: Multi-Tier Artifact Taxonomy & Physical Distribution Topology
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** Organize compiled distribution assets in `dist/` under a strictly defined hierarchy:
  ```text
  dist/
  ├── bundles/
  │   ├── mds.all.css             # Monolithic CSS bundle (all layers included)
  │   ├── mds.all.js              # Standalone vanilla JS custom elements bundle (IIFE/UMD)
  │   └── mds.all.esm.js          # Standalone ES Module custom elements bundle
  ├── css/
  │   ├── mds.tokens.css          # Resolved tokens wrapped in @layer mds.tokens
  │   ├── mds.primitives.css      # Primitives wrapped in @layer mds.primitives
  │   ├── mds.components.css      # 19 components wrapped in @layer mds.components
  │   └── themes/                 # Scoped theme overrides
  │       ├── mds.theme-dark.css
  │       ├── mds.theme-high-contrast.css
  │       ├── mds.density-compact.css
  │       └── mds.preset-refined.css
  ├── js/
  │   ├── mds.primitives.js       # Focus trap and live region utilities
  │   └── mds.components.js       # Native custom elements controllers
  ├── tokens/
  │   └── tokens.json             # Flat, resolved DTCG token dictionary
  ├── types/
  │   ├── tokens.d.ts             # TypeScript definitions for tokens
  │   └── components.d.ts         # TypeScript definitions for custom elements
  ├── archives/
  │   ├── mds-v1.0.0-dist.zip     # Portable offline distribution ZIP
  │   └── mds-v1.0.0-dist.tar.gz  # POSIX distribution tarball
  ├── mds_dist_manifest.json      # Cryptographic distribution inventory
  └── mds_dist_manifest.sha256    # Non-circular manifest self-integrity digest
  ```

---

### ADR-192: Deterministic & Bit-Exact Compilation Engine
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** Mandate byte-exact determinism across all build artifacts:
  1. *Line Ending Normalization:* All text files (CSS, JS, JSON, d.ts) are strictly written with POSIX LF (`\n`, `0x0A`).
  2. *Deterministic Dictionary Sorting:* All JSON outputs use `sort_keys=True` and 2-space indentation.
  3. *Alphabetical Traversal:* Source file scanning and archive entries are processed in strictly sorted order.
  4. *Fixed Build Timestamp:* Derived strictly from `SOURCE_DATE_EPOCH` (ADR-211).
  5. *Normalized Archive Permissions:* Files set to `0644`, directories set to `0755`.

---

### ADR-193: Cryptographic Manifest Architecture & Non-Circular Self-Integrity (`mds_dist_manifest.json`)
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** Adopt the non-circular manifest integrity architecture ratified in Phase 9.7.11 (ADR-146):
  1. `dist/mds_dist_manifest.json` contains metadata, source hash, build id, build epoch, and SHA-256 digests of all generated files in `dist/`.
  2. The compiler calculates the SHA-256 of the completed `mds_dist_manifest.json` and writes it to `dist/mds_dist_manifest.sha256`.
  3. Verifiers compute the hash of `mds_dist_manifest.json` and assert equality with `mds_dist_manifest.sha256`, completely avoiding circularity.

---

### ADR-194: CSS Cascade Layer Packaging & Dual Distribution (Monolithic vs Modular)
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** Package CSS under standard CSS Cascade Layers (`@layer`) and provide dual distribution:
  1. *Layer Hierarchy:* Every compiled stylesheet declares or belongs to:
     ```css
     @layer mds.reset, mds.tokens, mds.foundations, mds.primitives, mds.components, mds.themes;
     ```
  2. *Monolithic Bundle (`mds.all.css`):* Concatenates all layers in canonical order for instant `<link>` inclusion.
  3. *Modular Stylesheets:* Allows consumers to import only tokens (`mds.tokens.css`), primitives (`mds.primitives.css`), or components (`mds.components.css`) while preserving layer isolation.

---

### ADR-195: Zero-Dependency Vanilla JavaScript Custom Elements Packaging
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** Bundle JavaScript using native browser standards:
  1. Implement Custom Elements extending `HTMLElement` with standard lifecycle callbacks.
  2. Idempotent registration: Check `if (!window.customElements.get('mds-dialog')) customElements.define(...)`.
  3. Dual packaging: Emit both `mds.all.js` (IIFE/UMD for script tags) and `mds.all.esm.js` (ES Module for modern bundlers).
  4. Zero external imports: The compiler verifies that zero `npm`, `node`, or external module dependencies exist in the bundle.

---

### ADR-196: Pure Python Standard Library Tooling Boundary (Zero Pip / Zero NPM in Tooling)
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** Enforce that `tools/compiler/` relies exclusively on the **Python 3.12+ standard library**:
  - `pathlib`, `json`, `hashlib`, `re`, `argparse`, `zipfile`, `tarfile`, `typing`, `dataclasses`, `time`, `shutil`.
  - Zero pip packages (`pip list` remains empty of third-party requirements).
  - Can execute out-of-the-box on any machine with standard Python 3.12+.

---

### ADR-197: Standalone Compiler CLI Specification & Deterministic Exit Code Matrix (0–4)
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** Codify the CLI interface and exit code semantics:
  - Subcommands: `compile`, `verify`, `pack`, `ratify-sources`.
  - Exit Codes:
    - `0`: SUCCESS (All tasks executed and verified).
    - `1`: ADVISORY_WARNING (Non-blocking notices).
    - `2`: SOURCE_VALIDATION_FAILURE (Missing required `SOURCE_DATE_EPOCH` in reproducible mode, DTCG syntax error, circular token alias).
    - `3`: INTEGRITY_VIOLATION (Source manifest tampering, source hash mismatch against baseline, manifest tampering, Protected Core mutated).
    - `4`: FATAL_SYSTEM_ERROR (Disk full, permission denied, OS failure).

---

### ADR-198: Clean-Machine Offline Distribution Bundle (`.zip` / `.tar.gz`)
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** The compiler automatically generates self-contained distribution archives:
  - `dist/archives/mds-v1.0.0-dist.zip` (for Windows/Cross-Platform).
  - `dist/archives/mds-v1.0.0-dist.tar.gz` (for POSIX/Linux).
  - Contains all compiled CSS, JS, tokens, types, and manifests.
  - Can be served via `file://` or local static servers without external network calls.

---

### ADR-199: Downstream Project-Agent Distribution Contract
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** Downstream AI agents and developers acquire MDS via the distribution package:
  1. The agent locates the package in `vendor/mds/` or `dist/`.
  2. The agent executes verification via `verify` subcommand before writing code (ADR-210).
  3. The agent injects `mds.all.css` and `mds.all.js` into project HTML or imports them in layout files.
  4. The agent sets active design personality, theme, and density via HTML attributes according to `project_design_config.json`.

---

### ADR-200: Protected Core & Historical Guard Absolute Read-Only Immunity
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** Mandate absolute read-only immunity:
  1. The compiler treats `MDS/02-Tokens/`, `MDS/Runtime/`, `MDS/Playground/`, `MDS/Reference-Application/`, and `MDS/10-Testing/baselines/historical/` as immutable.
  2. Pre-compilation snapshot records SHA-256 of all 94 Protected Core files.
  3. Post-compilation verification confirms zero alterations; any detected write immediately triggers `Exit 3: INTEGRITY_VIOLATION`.

---

### ADR-201: Semantic Versioning, Schema Lock-Step, and Rollback Mechanics
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** 
  1. *SemVer 2.0.0:* Releases follow `MAJOR.MINOR.PATCH`.
  2. *Schema Lock-Step:* `project_design_config.json` `schema_version` matches package `MAJOR` version.
  3. *Zero-State Rollback:* Because MDS has no database or node_modules state, rolling back is instant: restore the previous `dist/` or `vendor/mds/` directory and verify hashes.

---

### ADR-202: Multi-Platform Token Export (DTCG JSON)
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** Emit `dist/tokens/tokens.json` as a fully resolved, flattened key-value dictionary containing:
  - Exact primitive values (hex colors, pixel values, milliseconds, line heights).
  - Multi-dimensional theme overrides (`dark`, `high-contrast`, `compact`, `refined`).
  - Readily ingested by Dart code generators in Flutter projects to produce `MdsTokens` classes.

---

### ADR-203: Comprehensive 5-Suite Test Architecture for Compiler & Distribution
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** Authorize a dedicated 5-suite test harness in `MDS/10-Testing/test_compiler.py`:
  1. `TestCompilerPipeline`: Ingestion, DAG resolution, CSS layer wrapping, JS bundling.
  2. `TestDeterministicBuilds`: Bit-exact SHA-256 matching across independent runs and platforms.
  3. `TestArtifactIntegrity`: Manifest consistency, file sizes, and non-circular hash verification.
  4. `TestZeroNPMContract`: Zero Node/npm imports or globals in emitted JavaScript.
  5. `TestCleanMachineConsumption`: Pure DOM execution of custom elements and tokens.

---

### ADR-204: Compiler Failure, Recovery, and Transactional Rollback Model
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** Implement atomic transactional generation:
  1. Write all output artifacts to an isolated staging directory (`dist/.staging/`).
  2. Run validation and manifest hashing in staging.
  3. Atomically promote staging to `dist/` only upon 100% success.
  4. On any failure (Exit 2, 3, or 4), cleanly delete `dist/.staging/`, leaving existing distributions untouched.

---

### ADR-205: Strict Scope Partitioning: Phase 10.3 Distribution vs Phase 10.4 Certification
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** 
  - *Phase 10.3 Scope:* Compilation engine, Zero-NPM packaging, manifest generator, offline archives, and compiler test harness.
  - *Phase 10.4 Scope:* Formal MDS v1.0.0 Production Certification, cross-platform browser matrix certification (Chrome, Firefox, Safari, Edge), end-to-end integration audits, and final production sign-off.
  - *Boundary Invariant:* Phase 10.3 does NOT execute Phase 10.4 certification and does NOT claim final production sign-off.

---

### ADR-206: Canonical Source Manifest Trust Chain & Dual-Anchored Cryptographic Verification (G-011)
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Context:** The compiler cannot trust `canonical_source_manifest.json` simply because it exists on disk, as an attacker could mutate both the source and the manifest.
- **Decision:**
  1. Binds `canonical_source_manifest.json` to the Root Trust Anchor (`trust_anchor.json` / `MDS-ROOT-ANCHOR-v1`) via `source_trust_binding.json`.
  2. The compiler asserts that the SHA-256 digest of `trust_anchor.json` matches the hardcoded constant `ROOT_TRUST_ANCHOR_FINGERPRINT`.
  3. The compiler asserts that `canonical_source_manifest.json` matches both the digest recorded in `source_trust_binding.json` and the compiled constant `AUTHORITATIVE_SOURCE_MANIFEST_DIGEST`.
  4. Only after the manifest itself is proven authentic does the compiler verify the 61 source file hashes on disk.
  5. Any tampering with the manifest, the binding, the anchor, or any source file immediately halts execution with `Exit 3: INTEGRITY_VIOLATION`.

---

### ADR-207: Exact Canonical 61 Source vs 94 Protected Core Mathematical Partition Law (G-012-A)
- **Status:** APPROVED (ARCHITECTURE STAGE — REV4)
- **Context:** Protected Core contains exactly 94 files. The architecture must eliminate ambiguous logical aliases (such as `Runtime/core`), establish the exact canonical on-disk paths, and mathematically prove the binary partition.
- **Decision:**
  1. Reconcile foundational stylesheet paths: Formally declare that `Runtime/core` was an informal logical label. The authoritative canonical path on disk is `MDS/Runtime/css/`, containing 4 files (`foundations.css`, `mds-core.css`, `primitives.css`, `reset.css`). Zero directories named `Runtime/core` exist or may exist.
  2. Ratify the formal mathematical partition law:
     $$\mathbf{ProtectedCore} = \mathbf{CompilationSourceSet} \cup \mathbf{ProtectedNonSourceSet}$$
     $$\mathbf{CompilationSourceSet} \cap \mathbf{ProtectedNonSourceSet} = \emptyset$$
     $$|\mathbf{ProtectedCore}| = 94, \quad |\mathbf{CompilationSourceSet}| = 61, \quad |\mathbf{ProtectedNonSourceSet}| = 33$$
  3. `CompilationSourceSet` contains exactly 61 canonical POSIX filesystem paths:
     - 18 DTCG token files (`MDS/02-Tokens/`)
     - 4 core CSS files (`MDS/Runtime/css/`)
     - 12 primitive CSS files (`MDS/Runtime/primitives/`)
     - 2 primitive JS files (`MDS/Runtime/primitives/interaction/`)
     - 20 component CSS files (`MDS/Runtime/components/`)
     - 5 component JS files (`MDS/Runtime/components/`)
  4. `ProtectedNonSourceSet` contains exactly 33 canonical paths:
     - 1 documentation specification in `MDS/02-Tokens/`
     - 7 sandbox files in `MDS/Playground/`
     - 7 application files in `MDS/Reference-Application/`
     - 13 legacy token build tools in `MDS/Runtime/tokens/`
     - 3 primitive docs and unit tests in `MDS/Runtime/primitives/`
     - 2 component docs and unit tests in `MDS/Runtime/components/`
  5. The compiler enforces strict binary classification: every Protected Core file belongs to exactly one set. Ingestion is bound strictly to `CompilationSourceSet`. Any attempt to inspect non-source or external files raises `CompilerScopeViolationError` with `Exit 3: INTEGRITY_VIOLATION`.

---

### ADR-208: JavaScript Dependency DAG, Entrypoint Architecture, and Topological Registration (G-003)
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:**
  1. Define the topological dependency order:
     $$\mathbf{FocusTrap} \longrightarrow \mathbf{LiveRegion} \longrightarrow \mathbf{MdsSwitch} \longrightarrow \mathbf{MdsTabs} \longrightarrow \mathbf{MdsTooltip} \longrightarrow \mathbf{MdsDialog}$$
     (`MdsDialog` depends strictly on `FocusTrap`; alphabetical ordering is prohibited).
  2. Enforce idempotent registration in every Custom Element:
     `if (!window.customElements.get(tagName)) window.customElements.define(tagName, Class);`
  3. Dual packaging:
     - `mds.all.js`: IIFE bundle that auto-registers elements and exposes `window.MDS`.
     - `mds.all.esm.js`: ES Module exporting named classes and utilities with explicit `registerMdsCustomElements()`.
  4. Emit modular scripts: `dist/js/mds.primitives.js` and `dist/js/mds.components.js`.

---

### ADR-209: Flutter Distribution Scope (Option A: Platform-Neutral Token Dictionary Contract) (G-004)
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:** Select **OPTION A**:
  1. Phase 10.3 produces **canonical `dist/tokens/tokens.json` only**.
  2. Phase 10.3 **DOES NOT** build a Dart code generator or generate `.dart` files.
  3. Flutter projects consume `tokens.json` using their own Dart generator or `build_runner` workflows.
  4. This preserves the Zero-NPM, Python stdlib boundary of Phase 10.3 and avoids coupling to the Dart SDK.

---

### ADR-210: Mandatory Read-Only Pre-Synthesis Bootstrap Verification Gate (G-005)
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:**
  1. The **MDS Distribution Verification Gate** is codified as a **mandatory precondition of Step 8**:
     `Step 7 (Config Locked) -> Verify Distribution (READ-ONLY) -> PASS -> Step 8 (Code Synthesis)`.
  2. The `verify` command is strictly read-only: performs zero compilation, zero packing, zero disk writes, and zero code generation.
  3. Downstream AI agents must execute `python tools/compiler/cli.py verify`.
  4. Gate asserts:
     - Manifest exists and matches `mds_dist_manifest.sha256`.
     - SHA-256 of `mds.all.css` and `mds.all.js` match manifest entries.
     - Reproducibility flag: `manifest.reproducible === true`.
     - Major version lock-step: `manifest.mds_version.split('.')[0] == config.schema_version.split('.')[0]`.
  5. If verification fails, code synthesis is **STRICTLY PROHIBITED** and the agent aborts with `Exit 2: CONTRACT_VIOLATION`.

---

### ADR-211: Reproducible Build Epoch Dual-Mode Contract & Archive Metadata Normalization (G-006, G-014, G-009)
- **Status:** APPROVED (ARCHITECTURE STAGE)
- **Decision:**
  1. Enforce strict dual-mode build contract:
     - **Mode A (Reproducible Mode / Production Default):** `SOURCE_DATE_EPOCH` is an **explicit, mandatory input** (via `$SOURCE_DATE_EPOCH` or `--epoch`). Missing input raises `Exit 2: SOURCE_VALIDATION_FAILURE`. Zero silent Git fallback. Manifest tags `"reproducible": true`.
     - **Mode B (Convenience / Dev Mode):** Fallback allowed for local scratch debugging; manifest tags `"reproducible": false`. Strictly rejected by Bootstrap Gate.
  2. Pinned archive metadata:
     - File permissions: `0644`.
     - Directory permissions: `0755`.
     - UID/GID: `0/0`.
     - User/Group names: `"root"/"root"`.
     - Extra fields: Stripped (`b""`).
     - Gzip headers: `mtime = build_epoch`, `OS = 255`, zero filename embedded.
     - Compression: Pinned to `zlib` level 9.
  3. Bit-exact guarantee: Compiling twice from the same source with identical `SOURCE_DATE_EPOCH` produces bit-exact identical `.zip` and `.tar.gz` archives.

---

### ADR-212: Complete Build Environment Determinism & Eight-Tier Build Identity Model (G-013-A)
- **Status:** APPROVED (ARCHITECTURE STAGE — REV4)
- **Context:** Build reproducibility requires that every input capable of altering output bytes MUST either be mathematically represented in Build Identity OR be explicitly prohibited/pinned by the reproducibility contract.
- **Decision:**
  1. Enforce the Inviolable Reproducibility Invariant:
     "Same canonical source ($I_{src}$) + same compiler identity ($I_{cmp}$) + same build configuration ($I_{cfg}$) + same build environment contract ($I_{env}$) + same build epoch ($T_{epoch}$) MUST produce byte-identical distribution artifacts."
  2. Establish eight decoupled identity tiers:
     - `source_identity`: SHA-256 of sorted concatenation of 61 canonical source hashes.
     - `compiler_identity`: `SHA-256(compiler_version + ":" + engine_source_digest)`.
     - `build_config_identity`: SHA-256 of canonical JSON of reproducibility-critical configuration.
     - `build_env_identity`: SHA-256 of canonical JSON of byte-affecting environment contract (`python_runtime_major_minor`: "3.12", `archive_engine`: "stdlib.zipfile+stdlib.tarfile", `filesystem_sort_order`: "posix_codepoint_utf8", `text_encoding`: "utf-8", `newline_convention`: "LF", `timezone_normalization`: "UTC", `locale_normalization`: "C.UTF-8").
     - `build_epoch`: Explicit integer seconds + ISO-8601 UTC string.
     - `build_id`: `SHA-256(I_src + ":" + I_cmp + ":" + I_cfg + ":" + I_env + ":" + str(T_epoch))`.
     - `release_identity`: `(package_name, version)`.
     - `artifact_identity`: Individual SHA-256 per file in `manifest.artifacts`.
  3. Pin and prohibit all external byte-affecting factors:
     - Python runtime: Strictly pinned to Python 3.12.x in reproducible mode (deviations halt with `Exit 4`).
     - Archive engines: Pure stdlib `zipfile` and `tarfile` only (zero system binaries).
     - Traversal order: Posix codepoint ascending (`sorted(paths, key=lambda p: p.as_posix())`).
     - Text encoding & newlines: Strict UTF-8 with LF (`\n`); CRLF strictly prohibited.
     - Locale & timezone: C.UTF-8 codepoint collation and UTC (+00:00).
     - Environment variables: Host environment variables (`USER`, `HOSTNAME`, `TEMP`, `PATH`) are strictly isolated and barred from leaking into artifacts.

---

## 3. Submission for Independent Architecture Audit

This remediated Decision Log codifies ADR-189 through ADR-212. Both final architecture findings (`G-012-A` and `G-013-A`) have been resolved and prepared for final independent audit.

Submitted by:  
**Antigravity AI Agent**  
For: **Mohamed Khalid**, Lead Architect (Senior Full Stack & Flutter Developer)  
Status: **PHASE 10.3 — ARCHITECTURE REV4 READY FOR FINAL INDEPENDENT AUDIT**

