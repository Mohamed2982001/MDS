# MDS Token Runtime Engine

**Layer:** 13-Implementation / Token Runtime  
**Phase:** 9.2 (Token Runtime Engine)  
**Status:** APPROVED & IMPLEMENTED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Specification:** [`MDS/13-Implementation/Token-Runtime-Architecture.md`](file:///d:/Work/Dev/Master%20Design%20System/MDS/13-Implementation/Token-Runtime-Architecture.md)  
**Runtime Dependencies:** Zero (Pure Python 3.12 Standard Library)

---

## 1. Architectural Mission

The **MDS Token Runtime Engine** is the automated, deterministic bridge between the machine-readable design tokens codified in `MDS/02-Tokens/` (W3C Design Tokens Community Group format) and the executable runtime artifacts required by web browsers, client frameworks, and design tooling.

### Inviolable Guarantees:
1. **Single Source of Truth:** All values originate strictly in the 18 DTCG `.tokens.json` files. The compiler never invents or hardcodes design values.
2. **Zero Runtime Dependencies:** Built using 100% Python standard library (no Node.js/npm dependencies, no Python pip packages).
3. **100% Deterministic Output:** Repeated compilation produces bit-for-bit identical files. Tokens are sorted alphabetically with zero dynamic timestamps.
4. **Compile-Time Graph Safety:** Constructs a Directed Acyclic Graph (DAG) to enforce:
   - Zero circular references (with exact cycle path tracing: `A -> B -> C -> A`).
   - Maximum alias depth $\le 3$ hops (current canonical repository is 2 hops: Component $\to$ Semantic $\to$ Primitive).
   - Zero broken or dangling references.
5. **Multi-Dimensional Theme Cascading:** Generates CSS custom properties organized into `:root` and scoped theme selectors (`[data-mode]`, `[data-preset]`, `[data-density]`) isolated inside `@layer mds.tokens`.

---

## 2. Directory Structure

```text
MDS/Runtime/tokens/
├── src/
│   ├── __init__.py              # Package exports
│   ├── models.py                # Data classes (Token, ResolvedToken, ThemeOverride, etc.) and exceptions
│   ├── loader.py                # Recursive DTCG discoverer & JSON parser (18 files)
│   ├── validator.py             # Schema, empty-value, tier, and invariant validator
│   ├── resolver.py              # Dependency DAG, cycle detector, 3-hop alias resolver
│   └── compiler.py              # CSS (@layer mds.tokens), JSON catalog, TypeScript emitter
├── tests/
│   ├── __init__.py              # Test package
│   └── test_token_runtime.py    # Comprehensive 13-test verification suite (100% passing)
├── dist/
│   ├── tokens.css               # CSS custom properties wrapped in @layer mds.tokens
│   ├── tokens.json              # Pre-resolved dictionary for AI, tooling, and portals
│   └── tokens.d.ts              # TypeScript type definitions (MDSTokenName union & dictionary)
├── compile_tokens.py            # CLI entry point (compile and --check modes)
└── README.md                    # This documentation file
```

---

## 3. CLI Usage

### Full Compilation (writes to `dist/`):
```powershell
python "MDS/Runtime/tokens/compile_tokens.py"
```

### Dry-Run Validation Mode (`--check`):
Validates DTCG schema, invariant counts, acyclic graph, and alias depth without touching disk:
```powershell
python "MDS/Runtime/tokens/compile_tokens.py" --check
```

### Custom Source or Output Directory:
```powershell
python "MDS/Runtime/tokens/compile_tokens.py" --tokens-dir "path/to/tokens" --out-dir "path/to/dist"
```

---

## 4. Distribution Artifacts (`dist/`)

| Artifact | Target Consumer | Architectural Responsibility |
| :--- | :--- | :--- |
| [`tokens.css`](file:///d:/Work/Dev/Master%20Design%20System/MDS/Runtime/tokens/dist/tokens.css) | Web Browsers / Cascade Layers | Contains all CSS custom properties wrapped in `@layer mds.tokens`. Defines `:root` (185 base tokens) plus 4 scoped theme blocks (`[data-mode="dark"]`, `[data-mode="high-contrast"]`, `[data-preset="refined"]`, `[data-density="compact"]`). |
| [`tokens.json`](file:///d:/Work/Dev/Master%20Design%20System/MDS/Runtime/tokens/dist/tokens.json) | AI Agents, Tooling, Doc Portal | Flat pre-resolved dictionary for sub-millisecond lookup. Includes token values, types, tiers, resolution chains, and theme override blocks. |
| [`tokens.d.ts`](file:///d:/Work/Dev/Master%20Design%20System/MDS/Runtime/tokens/dist/tokens.d.ts) | Downstream TypeScript Projects | Static autocomplete for all 188 token CSS variable names via `MDSTokenName` union type and dictionary interfaces. |

---

## 5. Verification & Testing

Execute the dedicated Token Runtime test suite:
```powershell
python "MDS/Runtime/tokens/tests/test_token_runtime.py"
```

### 13 Automated Test Assertions:
1. `test_01_discovery_file_count`: Asserts exactly 18 DTCG token files discovered.
2. `test_02_token_count_invariants`: Asserts 188 total distinct tokens, 185 base tokens, 3 theme-only tokens.
3. `test_03_component_tokens_count`: Asserts 47 component tokens (24 button, 10 input, 13 badge).
4. `test_04_alias_resolution_clean`: Asserts 100% of aliases resolve with zero broken targets.
5. `test_05_alias_max_depth`: Asserts maximum alias depth $\le 3$ hops (109 depth 0, 45 depth 1, 31 depth 2).
6. `test_06_cycle_detector`: Verifies synthetic cycle (`A -> B -> C -> A`) raises `CycleDetectedError` with complete cycle path.
7. `test_07_depth_exceeded_detector`: Verifies synthetic 4-hop chain raises `AliasDepthExceededError`.
8. `test_08_missing_token_detector`: Verifies synthetic dangling alias raises `MissingTokenError`.
9. `test_09_theme_overrides_resolution`: Verifies all 4 theme override files resolve cleanly.
10. `test_10_css_output_layer_and_structure`: Verifies `@layer mds.tokens`, `:root`, and all 4 theme selectors.
11. `test_11_json_catalog_structure`: Verifies schema structure of pre-resolved JSON dictionary.
12. `test_12_typescript_dts_structure`: Verifies `MDSTokenName` union contains all generated CSS variable names.
13. `test_13_compilation_determinism`: Verifies byte-for-byte identity across repeated compilation runs.
