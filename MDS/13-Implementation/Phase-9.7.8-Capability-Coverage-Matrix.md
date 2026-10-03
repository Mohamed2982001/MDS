# Master Design System (MDS) — Canonical Capability Coverage Matrix
## Phase 9.7.8 Architecture Canonical Artifact (Finding G-001 Micro-Remediation)

**Document Reference:** `MDS-GOV-COV-170`  
**Layer:** Layer M (Governance & Test Traceability)  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Status:** CANONICAL ARCHITECTURAL ARTIFACT — BINDING SPECIFICATION  
**Target Invariant:** `INV-009` (Test Accounting & Bipartite Coverage Model)  
**Total Declarative Capabilities:** 170 (133 Core Systemic + 37 DSSE Mathematical)  
**Master Harness Suites:** 48 Integration Suites in `MDS/10-Testing/run_tests.py`  
**Subsystem Unit Discovery Tests:** 141 Tests across 15 Modules in `MDS/10-Testing/tests/`  
**Date:** 2026-09-26  

---

## 1. Formal Coverage Model & Mathematical Definitions

The MDS Test Architecture rejects numerical equivalence ($170 \ne 48 \ne 141$) and formalizes traceability as a **Typed Bipartite Coverage Relation**:

$$\mathcal{R} \subseteq \mathcal{C} \times \mathcal{T}$$

Where:
- $\mathcal{C}$ is the set of 170 Declarative Capabilities defined in `MDS/10-Testing/capabilities/registry.json`.
- $\mathcal{T}$ is the set of Executable Tests ($48$ Master Harness integration suites in `run_tests.py` + $141$ unit tests across 15 modules in `MDS/10-Testing/tests/`).
- Every edge $e = (c, \text{rel\_type}, t) \in \mathcal{R}$ carries a deterministic classification $\text{rel\_type} \in \{\text{DIRECT}, \text{WRAPPED}, \text{INDIRECT}\}$.

### 1.1 Deterministic Coverage Computation Algorithm

For any capability $C \in \mathcal{C}$:

$$\text{coverage}(C) = \{ (C, \text{rel\_type}, T) \in \mathcal{R} \}$$

1. **`UNCOVERED(C)`:**
   $$\text{UNCOVERED}(C) \iff \text{coverage}(C) = \emptyset$$
   *Governance Rule:* If $|\text{UNCOVERED}| > 0$, the Governance Engine immediately halts with a **`CRITICAL Blocker`** (Exit Code 1).

2. **`DUPLICATE_COVERAGE(C)`:**
   $$\text{DUPLICATE\_COVERAGE}(C) \iff |\text{coverage}(C)| > 1$$
   *Governance Rule:* Represents deliberate cross-layer verification redundancy (e.g. Master Harness integration test + headless browser test + unit scanner). Tracked as healthy defense-in-depth, not an accounting error.

3. **`WRAPPED_COVERAGE(C, T)`:**
   $$\text{WRAPPED\_COVERAGE}(C, T) \iff T \text{ is explicitly declared in registry and harness as a composite runner for } C$$
   *Specific Binding:* Master Harness Test 48 (`MDS-DSS-004`) is the canonical 1-to-37 wrapper for all 37 DSSE assertions:
   $$\forall c \in \{\text{MDS-DSS-001}, \dots, \text{MDS-DSS-037}\}, \quad (c, \text{WRAPPED\_COVERAGE}, \text{run\_tests.py::MDSTestRunner.MDS-DSS-004}) \in \mathcal{R}$$

4. **`DIRECT_COVERAGE(C, T)`:**
   $$\text{DIRECT\_COVERAGE}(C, T) \iff T \text{ directly targets, executes, or asserts } C \text{ by capability ID}$$

5. **`INDIRECT_COVERAGE(C, T)`:**
   $$\text{INDIRECT\_COVERAGE}(C, T) \iff T \text{ validates an underlying parser, AST walker, mock fixture, or supporting subsystem required by } C$$

### 1.2 Invalid Reference & Error Handling Protocol
During graph construction and validation, the Governance Engine applies strict semantic checking:
- **`invalid relation`:** Any relation with an unrecognized relation type $\to$ **`Governance ERROR`** (`CRITICAL`).
- **`missing test reference`:** Any test file or entrypoint method referenced in $\mathcal{R}$ that does not exist physically on disk $\to$ **`Governance ERROR`** (`CRITICAL`).
- **`unknown capability ID`:** Any capability ID in test assertions or manifests that is not declared in `registry.json` $\to$ **`Governance ERROR`** (`CRITICAL`).
- **`zero coverage`:** Any capability where $\text{coverage}(C) = \emptyset$ $\to$ **`CRITICAL Blocker`** (`BLOCKER`, Exit 2).

---

## 2. Statistical Summary of Canonical Bipartite Relations

| Metric | Ground Truth Value | Deterministic Verification Formula | Governance Status |
| :--- | :---: | :--- | :---: |
| **Total Capabilities ($\|\mathcal{C}\|$)** | **170** | `len(registry.json["capabilities"])` | Canonical Catalog |
| ├── Core Systemic Capabilities | 133 | $170 - 37\text{ (DSSE)}$ | Active Contract |
| └── DSSE Mathematical Capabilities | 37 | `MDS-DSS-001` through `MDS-DSS-037` | Wrapped Core |
| **Direct Relations ($R_{\text{direct}}$)** | **170** | $\sum_{c \in \mathcal{C}} \mathbf{1}_{\exists T_{\text{direct}}}$ | 100% Direct Path |
| **Wrapped Relations ($R_{\text{wrapped}}$)** | **37** | $\sum_{c \in \text{DSSE}} \mathbf{1}_{(c, \text{MDS-DSS-004}) \in \mathcal{R}}$ | 1-to-37 DSSE Wrapper |
| **Indirect Supporting Relations ($R_{\text{indirect}}$)** | **213** | Edge count from 15 subsystem unit test modules | Subsystem Defense |
| **Duplicate-Covered Capabilities** | **167** | $\{ c \in \mathcal{C} \mid \|\text{coverage}(c)\| > 1 \}$ | Multi-Tier Verification |
| **Single-Covered Capabilities** | **3** | $\{ c \in \mathcal{C} \mid \|\text{coverage}(c)\| = 1 \}$ (`EXP-001`, `002`, `003`) | Direct Harness Path |
| **Uncovered Capabilities ($\|\text{UNCOVERED}\|$)** | **0** | $\{ c \in \mathcal{C} \mid \text{coverage}(c) = \emptyset \}$ | **ZERO GAPS — PASS** |

---

## 3. Canonical Capability-to-Test Mapping Table (All 170 Capabilities)


| # | Capability ID | Domain / Scope | Capability Name | Direct Test ($T_{\text{direct}}$) | Wrapper Test ($T_{\text{wrapper}}$) | Supporting Unit Tests ($T_{\text{indirect}}$) | Classification |
| :-: | :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| **001** | `MDS-REF-001` | REF | Core files existence | `Reference-Application/tests/test_reference_app.py::test_01_core_files_exist` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **002** | `MDS-REF-002` | REF | Zero NPM dependencies | `Reference-Application/tests/test_reference_app.py::test_02_zero_npm_dependencies` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **003** | `MDS-REF-003` | REF | Imports MDS core CSS | `Reference-Application/tests/test_reference_app.py::test_03_imports_mds_core_css` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **004** | `MDS-REF-004` | REF | Imports components JS | `Reference-Application/tests/test_reference_app.py::test_04_imports_components_js` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **005** | `MDS-REF-005` | REF | CSS layer overrides | `Reference-Application/tests/test_reference_app.py::test_05_css_in_layer_overrides` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **006** | `MDS-REF-006` | REF | Cairo font and RTL defaults | `Reference-Application/tests/test_reference_app.py::test_06_cairo_font_and_rtl_defaults` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **007** | `MDS-REF-007` | REF | All 6 templates implemented | `Reference-Application/tests/test_reference_app.py::test_07_all_6_templates_implemented` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **008** | `MDS-REF-008` | REF | All 8 patterns implemented | `Reference-Application/tests/test_reference_app.py::test_08_all_8_patterns_implemented` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **009** | `MDS-REF-009` | REF | All 4 mock roles exist | `Reference-Application/tests/test_reference_app.py::test_09_all_4_mock_roles_exist` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **010** | `MDS-REF-010` | REF | AI human-in-loop FSM | `Reference-Application/tests/test_reference_app.py::test_10_ai_human_in_the_loop_states` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **011** | `MDS-REF-011` | REF | Zero physical directional properties | `Reference-Application/tests/test_reference_app.py::test_11_zero_physical_directional_properties` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **012** | `MDS-REF-012` | REF | Zero row-reverse | `Reference-Application/tests/test_reference_app.py::test_12_zero_row_reverse` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **013** | `MDS-REF-013` | REF | Zero hardcoded hex colors | `Reference-Application/tests/test_reference_app.py::test_13_zero_hardcoded_hex_colors` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **014** | `MDS-REF-014` | REF | Dense spatial density deferred | `Reference-Application/tests/test_reference_app.py::test_14_dense_density_is_deferred` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **015** | `MDS-REF-015` | REF | Fixtures data integrity | `Reference-Application/tests/test_reference_app.py::test_15_fixtures_valid_json_and_complete` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **016** | `MDS-PLG-001` | PLG | Playground core files exist | `Playground/tests/test_playground.py::test_01_core_files_exist` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **017** | `MDS-PLG-002` | PLG | Zero NPM dependencies | `Playground/tests/test_playground.py::test_02_zero_npm_dependencies` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **018** | `MDS-PLG-003` | PLG | Imports MDS core CSS | `Playground/tests/test_playground.py::test_03_imports_mds_core_css` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **019** | `MDS-PLG-004` | PLG | Imports components JS | `Playground/tests/test_playground.py::test_04_imports_components_js` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **020** | `MDS-PLG-005` | PLG | Cairo font and RTL defaults | `Playground/tests/test_playground.py::test_05_html_arabic_rtl_cairo_defaults` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **021** | `MDS-PLG-006` | PLG | All 11 sections present | `Playground/tests/test_playground.py::test_06_all_11_sections_present` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **022** | `MDS-PLG-007` | PLG | All 19 components in specimens | `Playground/tests/test_playground.py::test_07_all_19_components_in_specimens` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **023** | `MDS-PLG-008` | PLG | Zero banned enterprise components | `Playground/tests/test_playground.py::test_08_zero_banned_enterprise_components` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **024** | `MDS-PLG-009` | PLG | Dense spatial tier deferred | `Playground/tests/test_playground.py::test_09_dense_tier_marked_deferred` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **025** | `MDS-PLG-010` | PLG | Zero physical properties | `Playground/tests/test_playground.py::test_10_zero_physical_properties` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **026** | `MDS-PLG-011` | PLG | Zero row-reverse | `Playground/tests/test_playground.py::test_11_zero_row_reverse` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **027** | `MDS-PLG-012` | PLG | Zero hardcoded hex colors | `Playground/tests/test_playground.py::test_12_zero_hardcoded_hex_colors` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **028** | `MDS-PLG-013` | PLG | Sample data valid JSON | `Playground/tests/test_playground.py::test_13_sample_data_valid_json` | None | `tests/test_repo_validator.py`, `tests/test_browser_live.py` | `DUPLICATE_COVERAGE` |
| **029** | `MDS-CRT-001` | CRT | Canonical 19 components exist | `Runtime/components/tests/test_components_runtime.py::test_01_canonical_19_components_exist` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **030** | `MDS-CRT-002` | CRT | Zero banned enterprise components | `Runtime/components/tests/test_components_runtime.py::test_02_zero_banned_enterprise_components` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **031** | `MDS-CRT-003` | CRT | Modular CSS files exist | `Runtime/components/tests/test_components_runtime.py::test_03_modular_css_files_exist` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **032** | `MDS-CRT-004` | CRT | JS controllers exist | `Runtime/components/tests/test_components_runtime.py::test_04_js_controllers_exist` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **033** | `MDS-CRT-005` | CRT | Consolidated components CSS | `Runtime/components/tests/test_components_runtime.py::test_05_consolidated_components_css_exists` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **034** | `MDS-CRT-006` | CRT | Components layer wrapping | `Runtime/components/tests/test_components_runtime.py::test_06_components_layer_wrapping` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **035** | `MDS-CRT-007` | CRT | MDS core imports components | `Runtime/components/tests/test_components_runtime.py::test_07_mds_core_imports_components` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **036** | `MDS-CRT-008` | CRT | Zero external margins on root | `Runtime/components/tests/test_components_runtime.py::test_08_zero_external_margins_on_root_components` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **037** | `MDS-CRT-009` | CRT | Zero physical directional properties | `Runtime/components/tests/test_components_runtime.py::test_09_zero_physical_directional_properties` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **038** | `MDS-CRT-010` | CRT | Zero row-reverse | `Runtime/components/tests/test_components_runtime.py::test_10_zero_row_reverse` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **039** | `MDS-CRT-011` | CRT | Zero hardcoded hex colors | `Runtime/components/tests/test_components_runtime.py::test_11_zero_hardcoded_hex_colors` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **040** | `MDS-CRT-012` | CRT | Component tokens consumed | `Runtime/components/tests/test_components_runtime.py::test_12_component_tokens_consumed` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **041** | `MDS-CRT-013` | CRT | Press target 44px rule | `Runtime/components/tests/test_components_runtime.py::test_13_press_target_44px_rule` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **042** | `MDS-CRT-014` | CRT | Focus ring 2px contract | `Runtime/components/tests/test_components_runtime.py::test_14_focus_ring_2px` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **043** | `MDS-CRT-015` | CRT | Table scroll container (AF-002) | `Runtime/components/tests/test_components_runtime.py::test_15_accessibility_finding_af002_table_scroll_container` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **044** | `MDS-CRT-016` | CRT | Dialog focus safety (AF-002) | `Runtime/components/tests/test_components_runtime.py::test_16_accessibility_finding_af002_dialog_initial_focus_safety` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **045** | `MDS-CRT-017` | CRT | Vestibular reduced motion contract | `Runtime/components/tests/test_components_runtime.py::test_17_vestibular_reduced_motion_contract` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **046** | `MDS-CRT-018` | CRT | Custom elements registered | `Runtime/components/tests/test_components_runtime.py::test_18_custom_elements_registered` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **047** | `MDS-PRT-001` | PRT | Consolidated CSS files exist | `Runtime/primitives/tests/test_primitives_runtime.py::test_consolidated_css_files_exist` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **048** | `MDS-PRT-002` | PRT | Modular primitive files exist | `Runtime/primitives/tests/test_primitives_runtime.py::test_modular_primitive_files_exist` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **049** | `MDS-PRT-003` | PRT | Canonical layer order declaration | `Runtime/primitives/tests/test_primitives_runtime.py::test_canonical_layer_order_declaration` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **050** | `MDS-PRT-004` | PRT | Stylesheet layer wrapping | `Runtime/primitives/tests/test_primitives_runtime.py::test_stylesheet_layer_wrapping` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **051** | `MDS-PRT-005` | PRT | MDS core imports primitives | `Runtime/primitives/tests/test_primitives_runtime.py::test_mds_core_imports` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **052** | `MDS-PRT-006` | PRT | Zero component classes | `Runtime/primitives/tests/test_primitives_runtime.py::test_zero_component_classes` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **053** | `MDS-PRT-007` | PRT | Zero physical directional properties | `Runtime/primitives/tests/test_primitives_runtime.py::test_zero_physical_directional_properties` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **054** | `MDS-PRT-008` | PRT | Zero row-reverse | `Runtime/primitives/tests/test_primitives_runtime.py::test_zero_row_reverse` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **055** | `MDS-PRT-009` | PRT | Zero hardcoded hex colors | `Runtime/primitives/tests/test_primitives_runtime.py::test_zero_hardcoded_hex_colors` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **056** | `MDS-PRT-010` | PRT | Zero raw RGB/HSL colors | `Runtime/primitives/tests/test_primitives_runtime.py::test_zero_raw_rgb_hsl_colors` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **057** | `MDS-PRT-011` | PRT | Tokens consumed via CSS variables | `Runtime/primitives/tests/test_primitives_runtime.py::test_tokens_consumed_via_css_variables` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **058** | `MDS-PRT-012` | PRT | Container constraints | `Runtime/primitives/tests/test_primitives_runtime.py::test_container_constraints` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **059** | `MDS-PRT-013` | PRT | Stack layout primitive | `Runtime/primitives/tests/test_primitives_runtime.py::test_stack_structure` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **060** | `MDS-PRT-014` | PRT | Inline layout primitive | `Runtime/primitives/tests/test_primitives_runtime.py::test_inline_structure` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **061** | `MDS-PRT-015` | PRT | Grid layout primitive | `Runtime/primitives/tests/test_primitives_runtime.py::test_grid_structure` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **062** | `MDS-PRT-016` | PRT | Cluster layout primitive | `Runtime/primitives/tests/test_primitives_runtime.py::test_cluster_structure` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **063** | `MDS-PRT-017` | PRT | Soft wrap overflow contract | `Runtime/primitives/tests/test_primitives_runtime.py::test_soft_wrap_no_text_overflow_ellipsis` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **064** | `MDS-PRT-018` | PRT | Headings typography hierarchy | `Runtime/primitives/tests/test_primitives_runtime.py::test_headings_hierarchy` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **065** | `MDS-PRT-019` | PRT | Numeric tabular figures | `Runtime/primitives/tests/test_primitives_runtime.py::test_numeric_tabular_nums` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **066** | `MDS-PRT-020` | PRT | Code monospace font contract | `Runtime/primitives/tests/test_primitives_runtime.py::test_code_mono_font` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **067** | `MDS-PRT-021` | PRT | Depth triad surface levels | `Runtime/primitives/tests/test_primitives_runtime.py::test_depth_triad_levels` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **068** | `MDS-PRT-022` | PRT | Surface elevation tokens | `Runtime/primitives/tests/test_primitives_runtime.py::test_surface_elevation_tokens` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **069** | `MDS-PRT-023` | PRT | Press target 44px rule | `Runtime/primitives/tests/test_primitives_runtime.py::test_press_target_44px_rule` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **070** | `MDS-PRT-024` | PRT | Focus ring 2px contract | `Runtime/primitives/tests/test_primitives_runtime.py::test_focus_ring_2px` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **071** | `MDS-PRT-025` | PRT | Visually hidden clip | `Runtime/primitives/tests/test_primitives_runtime.py::test_visually_hidden_accessible_clip` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **072** | `MDS-PRT-026` | PRT | Reduced motion contract | `Runtime/primitives/tests/test_primitives_runtime.py::test_reduced_motion_contract` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **073** | `MDS-PRT-027` | PRT | FocusTrap custom element | `Runtime/primitives/tests/test_primitives_runtime.py::test_focus_trap_exports_and_custom_element` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **074** | `MDS-PRT-028` | PRT | LiveRegion announcer (AF-001) | `Runtime/primitives/tests/test_primitives_runtime.py::test_live_region_af001_streaming_speech_throttling` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **075** | `MDS-PRT-029` | PRT | Icon optical sizes contract | `Runtime/primitives/tests/test_primitives_runtime.py::test_icon_optical_sizes` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **076** | `MDS-PRT-030` | PRT | Icon RTL directional mirroring | `Runtime/primitives/tests/test_primitives_runtime.py::test_icon_rtl_directional_mirroring` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **077** | `MDS-TRT-001` | TRT | Discovery file count | `Runtime/tokens/tests/test_token_runtime.py::test_01_discovery_file_count` | None | `tests/test_registry_validator.py` | `DUPLICATE_COVERAGE` |
| **078** | `MDS-TRT-002` | TRT | Token count invariants | `Runtime/tokens/tests/test_token_runtime.py::test_02_token_count_invariants` | None | `tests/test_registry_validator.py` | `DUPLICATE_COVERAGE` |
| **079** | `MDS-TRT-003` | TRT | Component tokens count | `Runtime/tokens/tests/test_token_runtime.py::test_03_component_tokens_count` | None | `tests/test_registry_validator.py` | `DUPLICATE_COVERAGE` |
| **080** | `MDS-TRT-004` | TRT | Alias resolution clean | `Runtime/tokens/tests/test_token_runtime.py::test_04_alias_resolution_clean` | None | `tests/test_registry_validator.py` | `DUPLICATE_COVERAGE` |
| **081** | `MDS-TRT-005` | TRT | Alias max depth | `Runtime/tokens/tests/test_token_runtime.py::test_05_alias_max_depth` | None | `tests/test_registry_validator.py` | `DUPLICATE_COVERAGE` |
| **082** | `MDS-TRT-006` | TRT | Cycle detector | `Runtime/tokens/tests/test_token_runtime.py::test_06_cycle_detector` | None | `tests/test_registry_validator.py` | `DUPLICATE_COVERAGE` |
| **083** | `MDS-TRT-007` | TRT | Depth exceeded detector | `Runtime/tokens/tests/test_token_runtime.py::test_07_depth_exceeded_detector` | None | `tests/test_registry_validator.py` | `DUPLICATE_COVERAGE` |
| **084** | `MDS-TRT-008` | TRT | Missing token detector | `Runtime/tokens/tests/test_token_runtime.py::test_08_missing_token_detector` | None | `tests/test_registry_validator.py` | `DUPLICATE_COVERAGE` |
| **085** | `MDS-TRT-009` | TRT | Theme overrides resolution | `Runtime/tokens/tests/test_token_runtime.py::test_09_theme_overrides_resolution` | None | `tests/test_registry_validator.py` | `DUPLICATE_COVERAGE` |
| **086** | `MDS-TRT-010` | TRT | CSS output layer and structure | `Runtime/tokens/tests/test_token_runtime.py::test_10_css_output_layer_and_structure` | None | `tests/test_registry_validator.py` | `DUPLICATE_COVERAGE` |
| **087** | `MDS-TRT-011` | TRT | JSON catalog structure | `Runtime/tokens/tests/test_token_runtime.py::test_11_json_catalog_structure` | None | `tests/test_registry_validator.py` | `DUPLICATE_COVERAGE` |
| **088** | `MDS-TRT-012` | TRT | TypeScript DTS structure | `Runtime/tokens/tests/test_token_runtime.py::test_12_typescript_dts_structure` | None | `tests/test_registry_validator.py` | `DUPLICATE_COVERAGE` |
| **089** | `MDS-TRT-013` | TRT | Compilation determinism | `Runtime/tokens/tests/test_token_runtime.py::test_13_compilation_determinism` | None | `tests/test_registry_validator.py` | `DUPLICATE_COVERAGE` |
| **090** | `MDS-DSS-001` | DSS | C_req full 12 dimensions | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **091** | `MDS-DSS-002` | DSS | C_req 6 declared 6 omitted | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **092** | `MDS-DSS-003` | DSS | C_req explicit NA counts | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **093** | `MDS-DSS-004` | DSS | C_req single dimension | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **094** | `MDS-DSS-005` | DSS | C_eval 100% active rated | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **095** | `MDS-DSS-006` | DSS | C_eval 3 of 4 rated | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **096** | `MDS-DSS-007` | DSS | C_eval single active rated | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **097** | `MDS-DSS-008` | DSS | C_eval zero active rated | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **098** | `MDS-DSS-009` | DSS | C_evid importance weighted | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **099** | `MDS-DSS-010` | DSS | C_evid pure CODE_AUDITED | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **100** | `MDS-DSS-011` | DSS | C_evid pure UNKNOWN | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **101** | `MDS-DSS-012` | DSS | C_epistemic perfect inputs | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **102** | `MDS-DSS-013` | DSS | C_epistemic collapse on C_req | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **103** | `MDS-DSS-014` | DSS | C_epistemic zero evidence collapse | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **104** | `MDS-DSS-015` | DSS | Hard constraint PASS keeps score | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **105** | `MDS-DSS-016` | DSS | Hard constraint FAIL forces 0 | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **106** | `MDS-DSS-017` | DSS | Margin <= 1.0% Virtual Tie | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **107** | `MDS-DSS-018` | DSS | Margin 1.0% exact Virtual Tie | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **108** | `MDS-DSS-019` | DSS | Margin 1.1% to 3.0% Tie-Break | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **109** | `MDS-DSS-020` | DSS | Margin 3.0% exact Tie-Break | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **110** | `MDS-DSS-021` | DSS | Margin > 3.0% Decisive Lead | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **111** | `MDS-DSS-022` | DSS | Tier HIGH criteria | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **112** | `MDS-DSS-023` | DSS | Tier MEDIUM criteria | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **113** | `MDS-DSS-024` | DSS | Tier LOW on low C_req | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **114** | `MDS-DSS-025` | DSS | Tier LOW on low C_evid | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **115** | `MDS-DSS-026` | DSS | Tier LOW on critical gap | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **116** | `MDS-DSS-027` | DSS | Governance decisive HIGH | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **117** | `MDS-DSS-028` | DSS | Governance Virtual Tie review | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **118** | `MDS-DSS-029` | DSS | Governance UNKNOWN constraint review | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **119** | `MDS-DSS-030` | DSS | Calibration Scenario A (Decisive Healthcare) | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **120** | `MDS-DSS-031` | DSS | Calibration Scenario B (Close SaaS Virtual Tie) | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **121** | `MDS-DSS-032` | DSS | Calibration Scenario C (Incomplete Startup) | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **122** | `MDS-DSS-033` | DSS | Calibration Scenario D (AI Workspace Inferred) | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **123** | `MDS-DSS-034` | DSS | Calibration Scenario E (Hard Constraint UNKNOWN) | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **124** | `MDS-DSS-035` | DSS | Calibration Scenario F (Weak Everything) | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **125** | `MDS-DSS-036` | DSS | Calibration Scenario G (Sole Survivor) | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **126** | `MDS-DSS-037` | DSS | Calibration Scenario H (Elite Virtual Tie) | `10-Testing/test_dsse.py::DSSETestSuite.run_all` | `run_tests.py::MDS-DSS-004` | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |
| **127** | `MDS-TKN-001` | TKN | DTCG token files inventory | `10-Testing/run_tests.py::MDSTestRunner.MDS-TKN-001` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **128** | `MDS-TKN-002` | TKN | DTCG JSON syntax validation | `10-Testing/run_tests.py::MDSTestRunner.MDS-TKN-002` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **129** | `MDS-TKN-003` | TKN | Canonical token registry count | `10-Testing/run_tests.py::MDSTestRunner.MDS-TKN-003` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **130** | `MDS-TKN-004` | TKN | Alias graph linkage validation | `10-Testing/run_tests.py::MDSTestRunner.MDS-TKN-004` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **131** | `MDS-TKN-005` | TKN | Zero raw hex in consumer CSS | `10-Testing/run_tests.py::MDSTestRunner.MDS-TKN-005` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **132** | `MDS-TKN-006` | TKN | Theme overrides presence | `10-Testing/run_tests.py::MDSTestRunner.MDS-TKN-006` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **133** | `MDS-PRI-001` | PRI | Layout primitives suite | `10-Testing/run_tests.py::MDSTestRunner.MDS-PRI-001` | None | `tests/test_css_scanner.py`, `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **134** | `MDS-PRI-002` | PRI | Parent-owned spacing invariant | `10-Testing/run_tests.py::MDSTestRunner.MDS-PRI-002` | None | `tests/test_css_scanner.py`, `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **135** | `MDS-PRI-003` | PRI | Surface suite & depth triad | `10-Testing/run_tests.py::MDSTestRunner.MDS-PRI-003` | None | `tests/test_css_scanner.py`, `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **136** | `MDS-PRI-004` | PRI | Accessibility primitives suite | `10-Testing/run_tests.py::MDSTestRunner.MDS-PRI-004` | None | `tests/test_css_scanner.py`, `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **137** | `MDS-PRI-005` | PRI | Vendor-agnostic icon contract | `10-Testing/run_tests.py::MDSTestRunner.MDS-PRI-005` | None | `tests/test_css_scanner.py`, `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **138** | `MDS-CMP-001` | CMP | Canonical 19 components inventory | `10-Testing/run_tests.py::MDSTestRunner.MDS-CMP-001` | None | `tests/test_css_scanner.py`, `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **139** | `MDS-CMP-002` | CMP | Banned enterprise systems guard | `10-Testing/run_tests.py::MDSTestRunner.MDS-CMP-002` | None | `tests/test_css_scanner.py`, `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **140** | `MDS-CMP-003` | CMP | Touch target 44px contract | `10-Testing/run_tests.py::MDSTestRunner.MDS-CMP-003` | None | `tests/test_css_scanner.py`, `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **141** | `MDS-CMP-004` | CMP | Select baseline tier separation | `10-Testing/run_tests.py::MDSTestRunner.MDS-CMP-004` | None | `tests/test_css_scanner.py`, `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **142** | `MDS-PAT-001` | PAT | Canonical 8 patterns inventory | `10-Testing/run_tests.py::MDSTestRunner.MDS-PAT-001` | None | `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **143** | `MDS-PAT-002` | PAT | Composition laws codification | `10-Testing/run_tests.py::MDSTestRunner.MDS-PAT-002` | None | `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **144** | `MDS-PAT-003` | PAT | Pattern selection engine rules | `10-Testing/run_tests.py::MDSTestRunner.MDS-PAT-003` | None | `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **145** | `MDS-WKF-001` | WKF | Canonical 6 workflows inventory | `10-Testing/run_tests.py::MDSTestRunner.MDS-WKF-001` | None | `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **146** | `MDS-WKF-002` | WKF | Universal 11-state FSM topology | `10-Testing/run_tests.py::MDSTestRunner.MDS-WKF-002` | None | `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **147** | `MDS-WKF-003` | WKF | FSM transition engine guards | `10-Testing/run_tests.py::MDSTestRunner.MDS-WKF-003` | None | `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **148** | `MDS-WKF-004` | WKF | Security triad decoupling | `10-Testing/run_tests.py::MDSTestRunner.MDS-WKF-004` | None | `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **149** | `MDS-A11Y-001` | A11Y | Master AT audit matrix | `10-Testing/run_tests.py::MDSTestRunner.MDS-A11Y-001` | None | `tests/test_accessibility_live.py`, `tests/test_accessibility_unit.py` | `DUPLICATE_COVERAGE` |
| **150** | `MDS-A11Y-002` | A11Y | Destructive dialog focus safety | `10-Testing/run_tests.py::MDSTestRunner.MDS-A11Y-002` | None | `tests/test_accessibility_live.py`, `tests/test_accessibility_unit.py` | `DUPLICATE_COVERAGE` |
| **151** | `MDS-A11Y-003` | A11Y | AI streaming live region (AF-001) | `10-Testing/run_tests.py::MDSTestRunner.MDS-A11Y-003` | None | `tests/test_accessibility_live.py`, `tests/test_accessibility_unit.py` | `DUPLICATE_COVERAGE` |
| **152** | `MDS-A11Y-004` | A11Y | Dynamic axe-core live injection | `10-Testing/accessibility/accessibility_dispatch.py::run_accessibility_capability` | None | `tests/test_accessibility_live.py`, `tests/test_accessibility_unit.py` | `DUPLICATE_COVERAGE` |
| **153** | `MDS-RTL-001` | RTL | Zero functional row-reverse | `10-Testing/run_tests.py::MDSTestRunner.MDS-RTL-001` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **154** | `MDS-RTL-002` | RTL | 100% CSS logical properties | `10-Testing/run_tests.py::MDSTestRunner.MDS-RTL-002` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **155** | `MDS-RTL-003` | RTL | Cairo font and RTL default | `10-Testing/run_tests.py::MDSTestRunner.MDS-RTL-003` | None | `tests/test_css_scanner.py` | `DUPLICATE_COVERAGE` |
| **156** | `MDS-RWD-001` | RWD | Container constraints codified | `10-Testing/run_tests.py::MDSTestRunner.MDS-RWD-001` | None | `tests/test_responsive_live.py`, `tests/test_responsive_unit.py` | `DUPLICATE_COVERAGE` |
| **157** | `MDS-RWD-002` | RWD | Recomposition invariant | `10-Testing/run_tests.py::MDSTestRunner.MDS-RWD-002` | None | `tests/test_responsive_live.py`, `tests/test_responsive_unit.py` | `DUPLICATE_COVERAGE` |
| **158** | `MDS-RWD-003` | RWD | Headless viewport resizing | `10-Testing/responsive/responsive_dispatch.py::run_responsive_capability` | None | `tests/test_responsive_live.py`, `tests/test_responsive_unit.py` | `DUPLICATE_COVERAGE` |
| **159** | `MDS-EXP-001` | EXP | Mandatory experience states | `10-Testing/run_tests.py::MDSTestRunner.MDS-EXP-001` | None | None | `DIRECT_COVERAGE` |
| **160** | `MDS-EXP-002` | EXP | Contextual recovery pairing | `10-Testing/run_tests.py::MDSTestRunner.MDS-EXP-002` | None | None | `DIRECT_COVERAGE` |
| **161** | `MDS-EXP-003` | EXP | Non-color-only state communication | `10-Testing/run_tests.py::MDSTestRunner.MDS-EXP-003` | None | None | `DIRECT_COVERAGE` |
| **162** | `MDS-VIS-001` | VIS | Pixel-diff snapshot automation | `10-Testing/visual/visual_dispatch.py::run_visual_capability` | None | `tests/test_visual_engine.py`, `tests/test_visual_live.py`, `tests/test_visual_negative.py` | `DUPLICATE_COVERAGE` |
| **163** | `MDS-TMP-001` | TMP | Canonical 6 templates inventory | `10-Testing/run_tests.py::MDSTestRunner.MDS-TMP-001` | None | `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **164** | `MDS-TMP-002` | TMP | 32-Point template anatomy | `10-Testing/run_tests.py::MDSTestRunner.MDS-TMP-002` | None | `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **165** | `MDS-TMP-003` | TMP | Template composition laws | `10-Testing/run_tests.py::MDSTestRunner.MDS-TMP-003` | None | `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **166** | `MDS-TMP-004` | TMP | Template selection engine | `10-Testing/run_tests.py::MDSTestRunner.MDS-TMP-004` | None | `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **167** | `MDS-DOC-001` | DOC | Documentation portal spec & index | `10-Testing/run_tests.py::MDSTestRunner.MDS-DOC-001` | None | `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **168** | `MDS-DOC-002` | DOC | Documentation CSS token enforcement | `10-Testing/run_tests.py::MDSTestRunner.MDS-DOC-002` | None | `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **169** | `MDS-DOC-003` | DOC | Portal app shell contracts | `10-Testing/run_tests.py::MDSTestRunner.MDS-DOC-003` | None | `tests/test_repo_validator.py` | `DUPLICATE_COVERAGE` |
| **170** | `MDS-DSS-000` | DSS | Automated DSSE mathematical suite | `10-Testing/run_tests.py::MDSTestRunner.MDS-DSS-004` | None | `test_dsse.py::DSSETestSuite` | `DUPLICATE_COVERAGE` |

---

*Canonical Capability Coverage Matrix complete for Phase 9.7.8 Final Independent Audit.*
