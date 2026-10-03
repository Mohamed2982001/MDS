# Agent Rule: Typography & RTL First-Class Strategy

## 1. Multilingual Typography Strategy
- **Arabic and Latin First-Class:** Both scripts are core first-class citizens in MDS.
- **Font Family Selection:** Primary font family is canonical **Cairo** (Google Fonts) for Arabic + Latin text; **JetBrains Mono** for code, identifiers, and tabular telemetry data.
- **Fallbacks:** Modern system fallback stacks (`system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`).
- **Weights:** Use restrained, intentional font weights (e.g., Regular 400, Medium 500, SemiBold 600, Bold 700).

## 2. Arabic & RTL as First-Class Citizens
- **Logical Properties Only:**
  - Never hardcode `margin-left`, `margin-right`, `padding-left`, or `padding-right`.
  - Always use logical properties: `padding-inline-start`, `padding-inline-end`, `margin-inline-start`, `margin-inline-end`.
  - In Flutter, use `EdgeInsetsDirectional.fromSTEB(...)` or `EdgeInsetsDirectional.only(...)` wrapped in `Directionality`.
- **Directional Icon Mirroring:**
  - Navigation icons (back arrows, forward arrows, chevrons) must mirror automatically in RTL environments.
  - Non-directional icons (search, settings, checkmarks) must not mirror.

## 3. Context-Aware Leading & Text Length
- **Arabic Text Length:** Arabic text runs longer than Latin equivalents; layouts must accommodate natural multiline expansion.
- **Line-Height (Leading):** Arabic typography may require context-specific increased leading relative to Latin typography to preserve readability, diacritic clarity, and vertical rhythm without clipping.
- **No Aggressive Ellipsis:** Never use `TextOverflow.ellipsis` on descriptive or informational text. Use soft wrapping with expandable lines.
