# 👑 MDS — Master Design System: AI Agent Integration Prompt

> **Copy this entire document and paste it into any AI coding agent (Cursor, Windsurf, Copilot, Gemini, Claude, etc.) at the start of a new project.**
> The AI will automatically detect the project type, wire MDS, and use the correct components — zero guesswork.

---

## 📌 SECTION 0 — WHO YOU ARE WORKING WITH

You are pair-programming with **Mohamed Khalid**, a **Senior Full Stack & Flutter Developer** and Lead Architect.
He owns a custom-built enterprise design system engine called **Master Design System (MDS)**.
**Every new project must consume MDS.** Never invent ad-hoc UI components, hardcode colors, or reinvent widgets from scratch.

---

## 📌 SECTION 1 — WHAT IS MDS? (READ THIS FIRST)

MDS is **NOT** just a UI kit. It is a **Hybrid Design System Engine** with three layers:

| Layer | What It Contains | Where It Lives |
|---|---|---|
| **1. Design Tokens** | Colors, spacing (4px/8px grid), radii, typography, elevation, motion durations & curves | `packages/mds_flutter_tokens/` (Dart) and `dist/tokens/` (CSS/JSON) |
| **2. Canonical Components** | 19 production-tested widgets (Flutter) + 260 CSS component classes (Web) | `packages/mds_flutter_ui/` (Dart) and `dist/css/` + `dist/js/` (Web) |
| **3. Theme Engine** | Full Material 3 ThemeData factory (Dart) + CSS `data-theme`, `data-density`, `data-preset` attribute system (Web) | `MdsThemeData.light()` / `.dark()` (Dart) and `:root` / `[data-theme="dark"]` (CSS) |

### MDS Hybrid DNA — Where the Design Inspiration Comes From:

MDS is a multi-DNA hybrid that combines the strongest traits of each world-class design system:

- **Google Material 3:** Dynamic tonal color palettes, `ColorScheme`, state layers, native Flutter integration.
- **Apple HIG:** Signature smooth corner radii (10px `md`), refined micro-animations, glassmorphism-ready surfaces.
- **Shopify Polaris:** Strict semantic feedback colors, data-dense table/form patterns, dashboard-grade alert/badge system.
- **Vercel shadcn/Geist:** Deep dark mode surfaces, minimal border aesthetic, sweep shimmer loading states.
- **IBM Carbon:** 4px/8px spacing grid, WCAG-grade focus rings, high-contrast accessibility mode.

### Repository Location:
- **Local Path (Primary):** `d:/Work/Dev/Master Design System`
- **Remote Git (Fallback):** `https://github.com/Mohamed2982001/MDS.git`

---

## 📌 SECTION 2 — PROJECT TYPE DETECTION (AI MUST DO THIS FIRST)

Before writing any UI code, **classify the project** into one of these archetypes. This determines your design tone:

### Archetype A: Consumer / Services App (e.g. delivery, social, healthcare, e-commerce mobile)
- **Design Tone:** Apple HIG + Material 3
- **Characteristics:** Generous spacing, soft 10–14px radii, smooth page transitions, full shimmer loading, floating toasts, elegant bottom sheets.
- **Key MDS widgets:** `MdsCard(variant: .elevated)`, `MdsButton(variant: .primary)`, `MdsSkeleton.card()`, `MdsToast.showSuccess()`, `MdsAvatar`, `MdsAccordion`.

### Archetype B: Business / Dashboard / Pricing Tool (e.g. admin panels, CRM, FairDevPrice)
- **Design Tone:** Shopify Polaris + IBM Carbon
- **Characteristics:** Compact density, structured data tables, strict semantic badges (success/warning/error), high-contrast form validation, metric cards.
- **Key MDS widgets:** `MdsTable`, `MdsBadge(variant: .success/.warning/.error)`, `MdsTextField(errorText: ...)`, `MdsCard(variant: .outlined)`, `MdsProgressIndicator.linear()`, `MdsDialog.show()`.

### Archetype C: Modern SaaS / Developer Tool (e.g. analytics, monitoring, IDE-adjacent)
- **Design Tone:** Vercel shadcn/Geist
- **Characteristics:** Dark-mode-first, minimal borders, monospace code fonts (`JetBrains Mono` via `MdsTypography.monoFontFamily`), deep surfaces, subtle glow effects.
- **Key MDS widgets:** `MdsCard(variant: .filled)`, `MdsBadge(style: .outline)`, `MdsTabs(variant: .pill)`, `MdsDivider`, `MdsTooltip(variant: .dark)`.

### Archetype D: Landing Page / Marketing Website (HTML/CSS, no Flutter)
- **Design Tone:** Hybrid Web (Zero-NPM)
- **Characteristics:** Use `dist/bundles/mds.all.css` + `dist/bundles/mds.all.js` directly. No build tools required. CSS classes like `.mds-button--primary`, `.mds-card`, `.mds-input`.
- See **Section 8** for Web-specific instructions.

---

## 📌 SECTION 3 — FLUTTER: PROJECT SETUP

### Step 1: Add dependencies to `pubspec.yaml`

```yaml
dependencies:
  flutter:
    sdk: flutter
  # ── MDS Design Tokens Engine ──
  mds_flutter_tokens:
    path: d:/Work/Dev/Master Design System/packages/mds_flutter_tokens
  # ── MDS Canonical UI Components ──
  mds_flutter_ui:
    path: d:/Work/Dev/Master Design System/packages/mds_flutter_ui
```

> **Note:** `mds_flutter_ui` already re-exports `mds_flutter_tokens`, so a single import gives you everything:
> ```dart
> import 'package:mds_flutter_ui/mds_flutter_ui.dart';
> ```

### Step 2: Wire MDS Theme in `MaterialApp`

```dart
MaterialApp(
  theme: MdsThemeData.light(),
  darkTheme: MdsThemeData.dark(),
  themeMode: ThemeMode.system, // or your Cubit-driven mode
  // ...
);
```

This single call configures: `ColorScheme`, `TextTheme` (Cairo font), `AppBarTheme`, `CardTheme`, `ElevatedButtonTheme`, `OutlinedButtonTheme`, `InputDecorationTheme`, and registers `MdsSemanticColors` as a `ThemeExtension`.

### Step 3: Access MDS tokens anywhere in the widget tree

```dart
// Option A — Context extension (recommended, concise):
final mds = context.mdsColors;     // MdsSemanticColors
final textTheme = context.textTheme; // TextTheme
final colorScheme = context.colorScheme; // ColorScheme

// Option B — Manual extraction:
final theme = Theme.of(context);
final mds = theme.extension<MdsSemanticColors>() ??
    (theme.brightness == Brightness.dark
        ? MdsSemanticColors.dark()
        : MdsSemanticColors.light());
```

---

## 📌 SECTION 4 — FLUTTER: COMPLETE TOKEN API REFERENCE

### 4.1 Colors (`MdsColors` — abstract final class)

**Brand Palette (10 stops):**
`brand50`, `brand100`, `brand200`, `brand300`, `brand400`, `brand500`, `brand600`, `brand700`, `brand800`, `brand900`, `brand950`

**Neutral Palette (13 stops):**
`neutral0` (white), `neutral50`, `neutral100`, `neutral200`, `neutral300`, `neutral400`, `neutral500`, `neutral600`, `neutral700`, `neutral800`, `neutral900`, `neutral950`, `neutral1000` (black)

**Semantic Palette:**
`red50`, `red200`, `red500`, `red600`, `red700` — `green50`, `green200`, `green500`, `green600` — `amber50`, `amber200`, `amber500`, `amber600` — `blue50`, `blue200`, `blue500`, `blue600`

**Resolved Role Colors (Light suffix / Dark suffix):**
- Text: `textPrimaryLight/Dark`, `textSecondaryLight/Dark`, `textInverseLight/Dark`
- Surface: `surfaceCanvasLight/Dark`, `surfaceDefaultLight/Dark`, `surfaceRaisedLight/Dark`, `surfaceOverlayLight/Dark`
- Border: `borderSubtleLight/Dark`, `borderDefaultLight/Dark`
- Action: `actionPrimaryDefaultLight/Dark`, `actionPrimaryHoverLight/Dark`, `actionPrimaryPressedLight/Dark`
- Destructive: `actionDestructiveDefaultLight/Dark`, `actionDestructiveHoverLight/Dark`
- Disabled: `actionDisabledBackgroundLight/Dark`, `actionDisabledForegroundLight/Dark`
- Feedback: `feedbackDangerLight/Dark`, `feedbackWarningLight/Dark`, `feedbackSuccessLight/Dark`, `feedbackInfoLight/Dark`
- Focus: `focusRingLight/Dark`

### 4.2 Semantic Colors Theme Extension (`MdsSemanticColors`)

This is the **primary way** components resolve colors. All 21 fields:
`textPrimary`, `textSecondary`, `textInverse`, `surfaceCanvas`, `surfaceDefault`, `surfaceRaised`, `surfaceOverlay`, `borderSubtle`, `borderDefault`, `actionPrimaryDefault`, `actionPrimaryHover`, `actionPrimaryPressed`, `actionDestructiveDefault`, `actionDestructiveHover`, `actionDisabledBackground`, `actionDisabledForeground`, `feedbackDanger`, `feedbackWarning`, `feedbackSuccess`, `feedbackInfo`, `focusRing`

**Factories:** `MdsSemanticColors.light()`, `MdsSemanticColors.dark()`
**Supports:** `copyWith(...)` and `lerp(...)` for animated theme transitions.

### 4.3 Spacing (`MdsSpacing` — abstract final class, 4px grid)

**Raw Scale:**
`space0` (0), `space1` (4), `space2` (8), `space3` (12), `space4` (16), `space5` (20), `space6` (24), `space8` (32), `space10` (40), `space12` (48), `space16` (64)

**Semantic Aliases:**
- Inline (horizontal): `inlineXs` (4), `inlineSm` (8), `inlineMd` (16), `inlineLg` (24)
- Block (vertical): `blockXs` (4), `blockSm` (8), `blockMd` (16), `blockLg` (32)

**Pre-built EdgeInsetsDirectional (RTL-safe):**
- `paddingInlineXs/Sm/Md/Lg` — horizontal only
- `paddingBlockXs/Sm/Md/Lg` — vertical only
- `paddingCardSm` (12 all), `paddingCardMd` (16 all), `paddingCardLg` (24 all)
- `paddingButtonSm` (h:12, v:6), `paddingButtonMd` (h:16, v:10), `paddingButtonLg` (h:20, v:12)
- `paddingInput` (h:12, v:10)

**Pre-built SizedBox Gaps:**
- `gapHorizontalXs/Sm/Md/Lg`, `gapVerticalXs/Sm/Md/Lg`

### 4.4 Radius (`MdsRadius` — abstract final class)

**Scalars:** `none` (0), `xs` (4), `sm` (6), `md` (10), `lg` (14), `xl` (20), `full` (9999)
**BorderRadius:** `borderNone`, `borderXs`, `borderSm`, `borderMd`, `borderLg`, `borderXl`, `borderFull`
**BorderRadiusDirectional (RTL-safe):** `directionalNone/Xs/Sm/Md/Lg/Xl/Full`
**Helpers:** `directionalStartOnly([radius])`, `directionalEndOnly([radius])`, `directionalTopOnly([radius])`, `directionalBottomOnly([radius])`
**Border Widths:** `borderWidthThin` (1.0), `borderWidthRegular` (1.5), `borderWidthThick` (2.0)

### 4.5 Typography (`MdsTypography` — abstract final class)

**Font Families:** `primaryFontFamily` = `'Cairo'`, `monoFontFamily` = `'JetBrains Mono'`
**Font Weights:** `regular` (w400), `medium` (w500), `semibold` (w600), `bold` (w700)
**Font Sizes:** `sizeXs` (12), `sizeSm` (14), `sizeBase` (16), `sizeLg` (20), `sizeXl` (24), `size2xl` (30), `size3xl` (36), `size4xl` (48)
**Line Heights:** `lineHeightTight` (1.25), `lineHeightNormal` (1.5), `lineHeightRelaxed` (1.75)
**Factory:** `MdsTypography.cairo(fontSize: ..., fontWeight: ..., color: ..., height: ..., letterSpacing: ..., decoration: ...)`
**TextTheme Factory:** `MdsTypography.createTextTheme(primaryColor: ..., secondaryColor: ...)` — returns a full M3 `TextTheme` mapped to Cairo.

### 4.6 Elevation (`MdsElevation` — abstract final class)

**Depth Scalars:** `level0` (0), `level1` (1), `level2` (3), `level3` (6)
**BoxShadow Lists:** `shadow0` (empty), `shadow1` (subtle), `shadow2` (medium), `shadow3` (strong)
**Resolver:** `MdsElevation.getShadow(int level)` → returns `List<BoxShadow>`

### 4.7 Motion (`MdsDurations` + `MdsCurves`)

**Durations:** `instant` (0ms), `fast` (150ms), `normal` (250ms), `slow` (350ms)
**Curves:** `standard` (0.2, 0.0, 0.0, 1.0), `enter` (0.0, 0.0, 0.2, 1.0), `exit` (0.4, 0.0, 1.0, 1.0)

---

## 📌 SECTION 5 — FLUTTER: COMPLETE COMPONENT API REFERENCE (ALL 19 WIDGETS)

> **CRITICAL RULE:** Never build custom buttons, inputs, alerts, cards, tables, dialogs, toasts, or loading states from raw Flutter primitives. Always use the MDS canonical widget.

### 5.1 `MdsButton`
```dart
MdsButton({
  required VoidCallback? onPressed,
  String? text,
  Widget? child,
  MdsButtonVariant variant = .primary, // primary | secondary | outline | ghost | danger
  MdsButtonSize size = .md,            // sm | md | lg
  Widget? leadingIcon,
  Widget? trailingIcon,
  bool isLoading = false,              // shows spinner, blocks taps
  bool isFullWidth = false,
  BorderRadiusGeometry? borderRadius,
  EdgeInsetsDirectional? padding,
  TextStyle? textStyle,
})
```

### 5.2 `MdsTextField`
```dart
MdsTextField({
  TextEditingController? controller,
  String? initialValue,
  String? label,
  String? hintText,
  String? helperText,
  String? errorText,       // non-null → red border + error message
  Widget? prefixIcon,
  Widget? suffixIcon,
  bool obscureText = false,
  bool enabled = true,
  bool readOnly = false,
  bool autofocus = false,
  bool showClearButton = false,
  int? maxLines = 1,
  int? minLines,
  TextInputType? keyboardType,
  TextInputAction? textInputAction,
  FocusNode? focusNode,
  ValueChanged<String>? onChanged,
  ValueChanged<String>? onSubmitted,
  BorderRadiusGeometry? borderRadius,
  EdgeInsetsGeometry? contentPadding,
})
```

### 5.3 `MdsCheckbox`
```dart
MdsCheckbox({
  required bool? value,
  required ValueChanged<bool?>? onChanged,
  String? label,
  String? description,
  String? errorText,
  bool disabled = false,
  bool tristate = false,
})
```

### 5.4 `MdsRadio<T>`
```dart
MdsRadio<T>({
  required T value,
  required T? groupValue,
  required ValueChanged<T?>? onChanged,
  String? label,
  String? description,
  bool disabled = false,
})
```

### 5.5 `MdsSwitch`
```dart
MdsSwitch({
  required bool value,
  required ValueChanged<bool>? onChanged,
  String? label,
  String? description,
  bool disabled = false,
})
```

### 5.6 `MdsDropdown<T>`
```dart
MdsDropdown<T>({
  required List<MdsDropdownItem<T>> items,
  T? value,
  ValueChanged<T?>? onChanged,
  String? label,
  String hintText = 'Select an option',
  String searchHintText = 'Search...',
  String? helperText,
  String? errorText,
  Widget? prefixIcon,
  MdsDropdownSize size = .md,  // sm | md | lg
  bool isSearchable = false,
  bool isClearable = false,
  bool isEnabled = true,
  double maxMenuHeight = 280.0,
  BorderRadiusGeometry? borderRadius,
  Widget? emptyWidget,
})

MdsDropdownItem<T>({
  required T value,
  required String label,
  Widget? child,
  Widget? icon,
  bool isEnabled = true,
})
```

### 5.7 `MdsCard`
```dart
MdsCard({
  Widget? child,
  Widget? title,
  Widget? subtitle,
  Widget? leading,
  Widget? trailing,
  Widget? header,
  Widget? footer,
  List<Widget>? actions,
  MdsCardVariant variant = .elevated, // elevated | outlined | filled
  EdgeInsetsDirectional? padding,
  EdgeInsetsGeometry? margin,
  BorderRadiusGeometry? borderRadius,
  VoidCallback? onTap,
})
```

### 5.8 `MdsBadge`
```dart
MdsBadge({
  required String label,
  MdsBadgeVariant variant = .brand, // success | warning | error | info | neutral | brand
  MdsBadgeStyle style = .subtle,    // subtle | filled | outline
  Widget? icon,
  VoidCallback? onTap,
  VoidCallback? onDelete,           // shows × close icon
  bool isPill = true,
})
```

### 5.9 `MdsAlert`
```dart
MdsAlert({
  required String message,
  String? title,
  MdsAlertVariant variant = .info, // info | success | warning | danger
  Widget? icon,
  Widget? action,
  VoidCallback? onDismiss,
  bool dismissible = false,
})
```

### 5.10 `MdsDialog`
```dart
// As a widget:
MdsDialog({
  required String title,
  required Widget content,
  Widget? icon,
  List<Widget>? actions,
  bool showCloseButton = true,
  double maxWidth = 480.0,
})

// Static show method (recommended):
MdsDialog.show<T>({
  required BuildContext context,
  required String title,
  required Widget content,
  Widget? icon,
  List<Widget>? actions,
  bool showCloseButton = true,
  bool barrierDismissible = true,
})
```

### 5.11 `MdsToast`
```dart
// Full control:
MdsToast.show({
  required BuildContext context,
  required String message,
  String? title,
  MdsToastVariant variant = .neutral, // info | success | warning | danger | neutral
  Duration duration = const Duration(seconds: 4),
  SnackBarAction? action,
})

// Convenience shortcuts:
MdsToast.showSuccess(context, 'Saved!', title: 'Done');
MdsToast.showError(context, 'Failed to save');
MdsToast.showWarning(context, 'Session expiring');
MdsToast.showInfo(context, 'Update available');
```

### 5.12 `MdsTable`
```dart
MdsTable({
  required List<MdsTableColumn> columns,
  required List<MdsTableRow> rows,
  bool isStriped = true,
  bool isBordered = true,
  double? minWidth,
  Widget? emptyWidget,
  BorderRadiusGeometry? borderRadius,
  EdgeInsetsDirectional cellPadding = EdgeInsetsDirectional.symmetric(horizontal: 16, vertical: 12),
  Color? headerBackgroundColor,
})

MdsTableColumn({
  required String title,
  Widget? titleWidget,
  double? width,
  int flex = 1,
  AlignmentDirectional alignment = .centerStart,
  bool isSortable = false,
  bool isSorted = false,
  bool isAscending = true,
  VoidCallback? onSort,
})

MdsTableRow({
  required List<Widget> cells,
  VoidCallback? onTap,
  Color? backgroundColor,
  bool isSelected = false,
})
```

### 5.13 `MdsTabs`
```dart
MdsTabs({
  required List<MdsTabItem> tabs,
  required int selectedIndex,
  required ValueChanged<int> onChanged,
  MdsTabVariant variant = .underline, // underline | pill
  bool isScrollable = false,
  bool isExpanded = false,
  EdgeInsetsDirectional? padding,
  Color? backgroundColor,
  Color? indicatorColor,
})

MdsTabItem({
  required String label,
  Widget? icon,
  Widget? badge,
  bool isEnabled = true,
})
```

### 5.14 `MdsAccordion` / `MdsAccordionGroup`
```dart
MdsAccordion({
  required String title,
  required Widget child,
  String? subtitle,
  Widget? leading,
  Widget? trailing,
  bool isExpanded = false,
  ValueChanged<bool>? onExpansionChanged,
  BorderRadiusGeometry? borderRadius,
  EdgeInsetsDirectional headerPadding,
  EdgeInsetsDirectional bodyPadding,
  bool isBordered = true,
})

MdsAccordionGroup({
  required List<MdsAccordion> children,
  bool allowMultiple = false,
  double spacing = 8.0,
})
```

### 5.15 `MdsAvatar` / `MdsAvatarGroup`
```dart
MdsAvatar({
  String? name,              // auto-extracts initials via extractInitials()
  String? initials,          // explicit override
  String? imageUrl,
  ImageProvider? image,
  MdsAvatarSize size = .md,  // xs(24) | sm(32) | md(40) | lg(48) | xl(56) | xxl(64)
  MdsAvatarShape shape = .circle, // circle | rounded
  MdsAvatarStatus status = .none, // none | online | offline | busy | away
  Color? backgroundColor,
  Color? foregroundColor,
  BorderRadiusGeometry? borderRadius,
  Widget? child,
  VoidCallback? onTap,
})

// Static utility:
MdsAvatar.extractInitials('Mohamed Khalid') // → 'MK'

MdsAvatarGroup({
  required List<MdsAvatar> avatars,
  int maxCount = 4,          // shows "+N" overflow badge
  double overlapOffset = 12.0,
  MdsAvatarSize size = .md,
})
```

### 5.16 `MdsProgressIndicator`
```dart
MdsProgressIndicator.linear({
  double? value,             // null → indeterminate
  Color? color,
  Color? backgroundColor,
  double height = 6.0,
  BorderRadiusGeometry? borderRadius,
  bool showPercentage = false,
  String? label,
})

MdsProgressIndicator.circular({
  double? value,
  Color? color,
  Color? backgroundColor,
  double size = 36.0,
  double strokeWidth = 3.5,
  bool showPercentage = false,
})
```

### 5.17 `MdsSkeleton` (Shimmer Loading)
```dart
MdsSkeleton({double? width, double height = 16.0, BorderRadiusGeometry? borderRadius, ...})
MdsSkeleton.circle({required double size, ...})
MdsSkeleton.text({double? width, double height = 14.0, int textLines = 3, double lineSpacing = 8.0, ...})
MdsSkeleton.card({double? width, double height = 180.0, ...})
```
Wrap in `MdsShimmer(child: ...)` for custom shimmer control.

### 5.18 `MdsTooltip`
```dart
MdsTooltip({
  required Widget child,
  required String message,
  MdsTooltipVariant variant = .dark,    // dark | light | primary
  MdsTooltipPosition position = .bottom, // top | bottom
  Duration waitDuration = 300ms,
  Duration showDuration = 2000ms,
  TooltipTriggerMode triggerMode = .longPress,
  EdgeInsetsGeometry? padding,
  BorderRadiusGeometry? borderRadius,
  double maxWidth = 260.0,
  bool enableFeedback = true,
})
```

### 5.19 `MdsDivider`
```dart
MdsDivider({
  String? text,
  Widget? labelWidget,
  MdsDividerAlignment alignment = .center, // start | center | end
  Color? color,
  double thickness = 1.0,
  double indent = 0.0,
  double endIndent = 0.0,
  double spacing = 16.0,
})
MdsDivider.vertical({Color? color, double thickness, double indent, double endIndent, double spacing})
```

### Bonus: Animation Utilities
```dart
MdsPressEffect({required Widget child, VoidCallback? onTap, bool enabled = true, double pressedScale = 0.97, Duration duration, Curve curve})
MdsFadeIn({required Widget child, Duration duration, Curve curve})
MdsDirectionality.isRtl(context) // → bool
MdsDirectionality.resolve(context, [TextDirection? override]) // → TextDirection
```

---

## 📌 SECTION 6 — FLUTTER: ABSOLUTE RULES (NEVER BREAK THESE)

### 6.1 No Hardcoded Colors
```dart
// ❌ WRONG — Never do this:
Container(color: Color(0xFF2563EB))
Container(color: Colors.blue)

// ✅ CORRECT — Always use MDS tokens:
Container(color: context.mdsColors.actionPrimaryDefault)
Container(color: MdsColors.brand600) // only for static palette reference
```

### 6.2 No Hardcoded Spacing
```dart
// ❌ WRONG:
Padding(padding: EdgeInsets.all(16))

// ✅ CORRECT:
Padding(padding: MdsSpacing.paddingCardMd)
SizedBox(height: MdsSpacing.blockMd)  // 16px vertical gap
MdsSpacing.gapVerticalMd              // pre-built SizedBox
```

### 6.3 No Physical Left/Right (RTL Safety)
```dart
// ❌ WRONG:
EdgeInsets.only(left: 16)
Alignment.topLeft

// ✅ CORRECT:
EdgeInsetsDirectional.only(start: 16)
AlignmentDirectional.topStart
MdsRadius.directionalStartOnly(10) // leading corners only
```

### 6.4 No Text Truncation with Ellipsis on Descriptive Text
```dart
// ❌ WRONG — Arabic text gets destroyed:
Text('...', overflow: TextOverflow.ellipsis, maxLines: 1)

// ✅ CORRECT:
Text('...', softWrap: true)
```

### 6.5 Theme-Driven Typography (Never hardcode font)
```dart
// ❌ WRONG:
TextStyle(fontFamily: 'Cairo', fontSize: 16)

// ✅ CORRECT:
Theme.of(context).textTheme.bodyLarge
MdsTypography.cairo(fontSize: MdsTypography.sizeBase, fontWeight: MdsTypography.semibold)
```

### 6.6 Mandatory Verification Before Delivery
Run `dart analyze` — **MUST** produce **ZERO errors and ZERO warnings**.

---

## 📌 SECTION 7 — FLUTTER: ARCHITECTURE & STATE MANAGEMENT

- **Architecture:** Clean Architecture + Feature-First folder structure.
- **State Management:** `flutter_bloc` / `Cubit` (primary). `Riverpod` acceptable for standalone utilities.
- **Null Safety:** Sound null safety enforced. The `!` operator is almost always a code smell.
- **Dart 3+:** Use records, pattern matching (`switch` expressions), and sealed classes where appropriate.
- **Const constructors:** Always mark widgets `const` where possible.
- **No `TODO` comments** in delivered code.
- **No `print()` in production** — use proper logging.

---

## 📌 SECTION 8 — WEB: PROJECT SETUP (Next.js / HTML / Vanilla)

For web projects (dashboards, landing pages, Next.js apps), MDS provides a **zero-dependency** CSS + JS distribution.

### Option A: Direct HTML (Zero Build Tools)
```html
<link rel="stylesheet" href="d:/Work/Dev/Master Design System/dist/bundles/mds.all.css">
<script src="d:/Work/Dev/Master Design System/dist/bundles/mds.all.js" type="module"></script>
```
Or copy the files into your project's `public/` folder.

### Option B: Next.js / Build Tool
```tsx
import 'd:/Work/Dev/Master Design System/dist/bundles/mds.all.css';
// Components are custom elements — no JS import needed for CSS-only components
```

### Dark Mode
```html
<html data-theme="dark"> <!-- switches all token variables automatically -->
```

### Compact Density (Dashboards)
```html
<body data-density="compact"> <!-- tightens spacing and control heights -->
```

### High Contrast (Accessibility)
```html
<body data-contrast="high"> <!-- thickens borders, strengthens focus rings -->
```

### Refined Preset (Apple-like)
```html
<body data-preset="refined"> <!-- reduces radii for a more Apple/Polaris feel -->
```

### CSS Variables Available (203 total) — Key Ones:
```css
/* Colors */
var(--mds-color-action-primary-default)    /* #2563EB */
var(--mds-color-feedback-success)          /* #059669 */
var(--mds-color-feedback-danger)           /* #DC2626 */
var(--mds-color-text-primary)              /* auto light/dark */
var(--mds-color-surface-default)           /* auto light/dark */
var(--mds-color-border-default)            /* auto light/dark */

/* Spacing (4px grid) */
var(--mds-space-scale-1)  /* 4px */   var(--mds-space-scale-4)  /* 16px */
var(--mds-space-scale-6)  /* 24px */  var(--mds-space-scale-8)  /* 32px */
var(--mds-space-inline-md) /* 16px */ var(--mds-space-block-md) /* 16px */

/* Radius */
var(--mds-radius-sm) /* 6px */  var(--mds-radius-md) /* 10px */
var(--mds-radius-lg) /* 14px */ var(--mds-radius-full) /* 9999px */

/* Typography */
var(--mds-font-family-primary)  /* Cairo */
var(--mds-font-family-mono)     /* JetBrains Mono */
var(--mds-font-size-base) /* 16px */ var(--mds-font-size-lg) /* 20px */

/* Motion */
var(--mds-motion-duration-fast) /* 150ms */
var(--mds-motion-easing-standard) /* cubic-bezier(0.2,0,0,1) */
```

### Web CSS Class Examples:
```html
<button class="mds-button mds-button--primary mds-button--md">Submit</button>
<button class="mds-button mds-button--ghost mds-button--sm">Cancel</button>
<input class="mds-input mds-input--md" placeholder="Email">
<div class="mds-card mds-card--raised mds-card--md">...</div>
<div class="mds-alert mds-alert--success">...</div>
<span class="mds-badge mds-badge--warning mds-badge--sm">Pending</span>
<table class="mds-table mds-table--striped mds-table--bordered">...</table>
<div class="mds-skeleton mds-skeleton--text"></div>
<div class="mds-spinner mds-spinner--brand mds-spinner--md"></div>
```

### Web Custom Elements (JavaScript):
```html
<mds-dialog id="confirm">...</mds-dialog>
<mds-tabs>...</mds-tabs>
<mds-switch></mds-switch>
<mds-tooltip>...</mds-tooltip>
```
```js
document.querySelector('#confirm').open();
document.querySelector('#confirm').close();
```

### Layout Utilities:
```html
<div class="mds-stack mds-stack--gap-md">...</div>         <!-- vertical stack -->
<div class="mds-cluster mds-cluster--gap-sm">...</div>     <!-- horizontal wrap -->
<div class="mds-inline mds-inline--gap-md">...</div>       <!-- inline flex -->
<div class="mds-grid mds-grid--auto-tiles">...</div>       <!-- responsive grid -->
<div class="mds-container mds-container--standard">...</div>
```

---

## 📌 SECTION 9 — PRACTICAL EXAMPLES BY PROJECT TYPE

### Example A: Consumer App Login Screen (Flutter)
```dart
Scaffold(
  body: SafeArea(
    child: Padding(
      padding: MdsSpacing.paddingCardLg,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          MdsSpacing.gapVerticalLg,
          Text('Welcome Back', style: context.textTheme.headlineMedium),
          MdsSpacing.gapVerticalXs,
          Text('Sign in to continue', style: context.textTheme.bodyMedium),
          MdsSpacing.gapVerticalLg,
          const MdsTextField(label: 'Email', hintText: 'you@example.com', prefixIcon: Icon(Icons.email_outlined)),
          MdsSpacing.gapVerticalMd,
          const MdsTextField(label: 'Password', hintText: '••••••••', prefixIcon: Icon(Icons.lock_outline), obscureText: true),
          MdsSpacing.gapVerticalLg,
          MdsButton(text: 'Sign In', onPressed: () {}, isFullWidth: true),
          MdsSpacing.gapVerticalSm,
          MdsButton(text: 'Forgot Password?', variant: MdsButtonVariant.ghost, onPressed: () {}),
        ],
      ),
    ),
  ),
)
```

### Example B: Dashboard Pricing Table (Flutter)
```dart
MdsTable(
  columns: [
    MdsTableColumn(title: 'Feature', flex: 3),
    MdsTableColumn(title: 'Hours', flex: 1, alignment: AlignmentDirectional.centerEnd),
    MdsTableColumn(title: 'Cost (EGP)', flex: 1, alignment: AlignmentDirectional.centerEnd),
  ],
  rows: items.map((item) => MdsTableRow(
    cells: [
      Text(item.name),
      Text('${item.hours}h', style: context.textTheme.bodyMedium),
      Text('${item.cost} EGP', style: context.textTheme.titleSmall),
    ],
  )).toList(),
)
```

### Example C: Status Badge with Toast Feedback (Flutter)
```dart
MdsBadge(label: 'Completed', variant: MdsBadgeVariant.success, icon: Icon(Icons.check, size: 14));
MdsBadge(label: 'Pending', variant: MdsBadgeVariant.warning);
MdsBadge(label: 'Failed', variant: MdsBadgeVariant.error, onDelete: () => MdsToast.showError(context, 'Item removed'));
```

---

## 📌 SECTION 10 — FILE STRUCTURE QUICK REFERENCE

```
d:/Work/Dev/Master Design System/
├── packages/
│   ├── mds_flutter_tokens/          ← Dart token engine
│   │   └── lib/src/
│   │       ├── colors.dart          ← MdsColors, MdsColorScheme, MdsSemanticColors
│   │       ├── spacing.dart         ← MdsSpacing
│   │       ├── radius.dart          ← MdsRadius
│   │       ├── typography.dart      ← MdsTypography
│   │       ├── elevation.dart       ← MdsElevation
│   │       ├── motion.dart          ← MdsDurations, MdsCurves
│   │       └── theme.dart           ← MdsThemeData, MdsThemeContextExtension
│   └── mds_flutter_ui/             ← 19 canonical Flutter widgets
│       └── lib/src/components/
│           ├── button.dart, text_field.dart, checkbox.dart, radio.dart,
│           ├── switch.dart, dropdown.dart, card.dart, badge.dart,
│           ├── alert.dart, dialog.dart, toast.dart, table.dart,
│           ├── tabs.dart, accordion.dart, avatar.dart, progress.dart,
│           ├── skeleton.dart, tooltip.dart, divider.dart
│           └── ../utils/animations.dart, directionality.dart
├── dist/                            ← Zero-NPM Web distribution
│   ├── bundles/mds.all.css          ← Single CSS bundle (all tokens + components)
│   ├── bundles/mds.all.js           ← Single JS bundle (custom elements)
│   ├── css/mds.tokens.css           ← Token-only CSS (203 variables)
│   ├── css/mds.components.css       ← Component-only CSS (260 classes)
│   ├── css/components/*.css         ← Individual component CSS files
│   ├── js/mds.components.js         ← Component JS
│   ├── tokens/tokens.json           ← Raw token JSON
│   └── types/components.d.ts        ← TypeScript declarations
└── examples/flutter_showcase/       ← Interactive showcase app (reference)
```

---

## 📌 SECTION 11 — DECISION CHECKLIST FOR THE AI

Before writing any widget or HTML element, ask yourself:

1. ✅ Did I add `mds_flutter_ui` (Flutter) or `mds.all.css` (Web) to the project?
2. ✅ Did I wire `MdsThemeData.light()` / `.dark()` in `MaterialApp`?
3. ✅ Am I using an MDS canonical component instead of building from scratch?
4. ✅ Am I using `MdsSpacing.*` instead of raw `SizedBox(height: 16)`?
5. ✅ Am I using `MdsRadius.*` instead of `BorderRadius.circular(10)`?
6. ✅ Am I using `context.mdsColors.*` or `MdsColors.*` instead of `Color(0xFF...)`?
7. ✅ Am I using `EdgeInsetsDirectional` (not `EdgeInsets`) for RTL safety?
8. ✅ Am I using `softWrap: true` instead of `TextOverflow.ellipsis` on descriptive text?
9. ✅ Did I run `dart analyze` with zero warnings before delivering?
10. ✅ Did I determine the project archetype (A/B/C/D) and apply the correct design tone?

**If any answer is NO → fix it before proceeding.**

---

## 📌 SECTION 12 — BROWNFIELD INJECTION: WORKING WITH EXISTING PROJECTS

> **CRITICAL PROTOCOL:** When injected into an existing codebase (e.g. refactoring an existing screen in `Azhal`, migrating `FairDevPrice`, or upgrading any live production app to MDS):

### 12.1 The 5 Cardinal Rules of Brownfield Injection
1. **TOUCH ONLY THE PRESENTATION LAYER:** Never modify Cubit/Bloc states, events, domain models, entity definitions, API services, local storage (Hive/SQLite/SharedPreferences), or routing logic unless explicitly asked. Your mission is strictly visual elevation and UI modernization.
2. **ZERO REGRESSION POLICY:** Every callback (`onPressed`, `onChanged`, `onTap`, `onSubmitted`), `TextEditingController`, `FocusNode`, `GlobalKey<FormState>`, and form validation logic MUST remain functionally identical and intact.
3. **INCREMENTAL MIGRATION (SCREEN-BY-SCREEN):** Never attempt to refactor the entire app in one giant PR or response. Refactor **one component, one card, or one screen at a time**. Validate each step before proceeding.
4. **SAFE THEME BRIDGING (DUAL-THEME COEXISTENCE):** 
   - If the existing app already has a custom `ThemeData`, do NOT aggressively wipe it.
   - Bridge MDS by injecting the `MdsSemanticColors` extension into the existing theme:
     ```dart
     ThemeData(
       // ... existing theme properties ...
       extensions: [
         theme.brightness == Brightness.dark
             ? MdsSemanticColors.dark()
             : MdsSemanticColors.light(),
       ],
     )
     ```
   - Or, if doing a full UI overhaul, adopt `MdsThemeData.light()` / `MdsThemeData.dark()`.
5. **MANDATORY PRE/POST TESTING:**
   - **Pre-Test:** Inspect the existing screen and verify its current state and controllers before touching any code.
   - **Post-Test:** Run `dart analyze` to ensure zero compilation or lint errors, and verify all interactions still work.

---

### 12.2 Direct 1-to-1 Component Replacement Dictionary

Use this exact mapping table to swap legacy Flutter widgets with MDS canonical components:

| Legacy Flutter Widget | MDS Replacement | How to Map Properties |
|---|---|---|
| `ElevatedButton` / `FilledButton` | `MdsButton(variant: .primary)` | `onPressed: onPressed`, `text: 'Label'` or `child: child`, `isLoading: state.isLoading` |
| `OutlinedButton` | `MdsButton(variant: .outline)` | Same as above |
| `TextButton` | `MdsButton(variant: .ghost)` | Same as above |
| Danger / Delete Button | `MdsButton(variant: .danger)` | Use for destructive actions |
| `TextFormField` / `TextField` | `MdsTextField` | Map `controller`, `label: decoration.labelText`, `hintText: decoration.hintText`, `errorText: errorText`, `obscureText`, `prefixIcon`, `suffixIcon`, `onChanged` |
| `Card` / `Container(BoxDecoration)` | `MdsCard(variant: .elevated / .outlined / .filled)` | Move padding to `padding: MdsSpacing.paddingCardMd`, keep `child` or use `title`/`subtitle`/`leading`/`trailing` slots |
| `ScaffoldMessenger.showSnackBar` | `MdsToast.show(...)` / `MdsToast.showSuccess/Error` | Replace bulky SnackBar with floating MDS Toast |
| `AlertDialog` / `showDialog` | `MdsDialog.show(...)` | Pass `title`, `content`, `actions: [MdsButton(...)]` |
| `CircularProgressIndicator` (inline) | `MdsProgressIndicator.circular()` | `size: 24`, `strokeWidth: 2.5` |
| `CircularProgressIndicator` (fullscreen/loading) | `MdsSkeleton` shimmer cards/lines | Replace full-screen blockers with sleek shimmer placeholders |
| `ExpansionTile` | `MdsAccordion` / `MdsAccordionGroup` | `title: ...`, `child: ...`, `isExpanded: ...` |
| `Chip` / `ActionChip` / Status Container | `MdsBadge` | `label: ...`, `variant: .brand/.success/.warning/.error`, `style: .subtle/.filled/.outline` |
| `Checkbox` / `CheckboxListTile` | `MdsCheckbox` | `value: ...`, `onChanged: ...`, `label: ...`, `description: ...` |
| `Radio` / `RadioListTile` | `MdsRadio<T>` | `value: ...`, `groupValue: ...`, `onChanged: ...`, `label: ...` |
| `Switch` / `SwitchListTile` | `MdsSwitch` | `value: ...`, `onChanged: ...`, `label: ...` |
| `Divider` | `MdsDivider` / `MdsDivider.vertical` | Optional middle text label: `MdsDivider(text: 'OR')` |
| `CircleAvatar` | `MdsAvatar` / `MdsAvatarGroup` | `name: user.name` (auto initials), `imageUrl: ...`, `status: .online` |
| `Tooltip` | `MdsTooltip` | `message: ...`, `child: ...`, `variant: .dark` |
| `DataTable` | `MdsTable` | Map columns to `MdsTableColumn` and rows to `MdsTableRow` |
| `TabBar` | `MdsTabs` | Map tabs to `MdsTabItem`, variant: `.underline` or `.pill` |
| `Padding(EdgeInsets.all(16))` | `Padding(MdsSpacing.paddingCardMd)` | Standardize to 4px/8px MDS spacing grid |
| `SizedBox(height: 16)` | `MdsSpacing.gapVerticalMd` | Standardize vertical gaps |
| `SizedBox(width: 8)` | `MdsSpacing.gapHorizontalSm` | Standardize horizontal gaps |
| `BorderRadius.circular(10)` | `MdsRadius.borderMd` | Standardize radii |
| `Color(0xFF...)` / `Colors.blue` | `context.mdsColors.actionPrimaryDefault` | Eliminate raw hex/Material colors |

---

### 12.3 Step-by-Step Injection Recipe for Existing Screens

When migrating an existing screen (e.g. `LoginView.dart` or `CartView.dart`):

1. **Step 1: Check `pubspec.yaml`:**
   Ensure `mds_flutter_ui` is added. If not, add:
   ```yaml
   dependencies:
     mds_flutter_ui:
       path: d:/Work/Dev/Master Design System/packages/mds_flutter_ui
   ```
2. **Step 2: Add Single Import:**
   In the target screen file, add:
   ```dart
   import 'package:mds_flutter_ui/mds_flutter_ui.dart';
   ```
3. **Step 3: Keep State & Logic Untouched:**
   Preserve all `BlocBuilder`, `BlocConsumer`, `Provider`, `setState`, controllers, and validators.
4. **Step 4: Swap UI Elements via the Replacement Dictionary:**
   - Replace `ElevatedButton` with `MdsButton`.
   - Replace `TextFormField` with `MdsTextField`.
   - Replace `Card` with `MdsCard`.
   - Replace raw padding with `MdsSpacing.paddingCardMd` and `MdsSpacing.gapVertical*`.
5. **Step 5: Verify With Zero Warnings:**
   Run `dart analyze` to ensure zero compilation or lint issues before moving to the next screen.
