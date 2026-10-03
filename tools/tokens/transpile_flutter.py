"""
Master Design System (MDS) — Pure-Python Flutter Token Engine & Transpiler
Phase 11: Multi-Platform Flutter Token Engine & Package
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Deterministically transpiles canonical JSON token specifications from MDS/00-Tokens/
into the production-ready packages/mds_flutter_tokens Dart package.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


def hex_to_flutter_color(hex_str: str) -> str:
    """Converts a #RGB, #RRGGBB, or #AARRGGBB hex color string to Flutter Color(0xAARRGGBB)."""
    hex_clean = hex_str.strip().lstrip("#").upper()
    if len(hex_clean) == 3:
        r = hex_clean[0] * 2
        g = hex_clean[1] * 2
        b = hex_clean[2] * 2
        return f"Color(0xFF{r}{g}{b})"
    elif len(hex_clean) == 6:
        return f"Color(0xFF{hex_clean})"
    elif len(hex_clean) == 8:
        return f"Color(0x{hex_clean})"
    else:
        raise ValueError(f"Invalid hex color string: {hex_str}")


def normalize_newlines(text: str) -> str:
    """Normalizes CRLF and CR to LF."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


class FlutterTokenTranspiler:
    """Deterministic transpiler producing the mds_flutter_tokens Dart package."""

    def __init__(self, workspace_root: Path, tokens_dir: Path | None = None):
        self.workspace_root = workspace_root.resolve()
        self.tokens_dir = (tokens_dir or (self.workspace_root / "MDS" / "00-Tokens")).resolve()
        self.tokens: Dict[str, Any] = {}

    def load_tokens(self) -> None:
        """Loads all canonical JSON token specifications."""
        required_specs = [
            "colors.json",
            "typography.json",
            "spacing.json",
            "radius.json",
            "elevation.json",
            "motion.json",
        ]
        for spec_file in required_specs:
            file_path = self.tokens_dir / spec_file
            if not file_path.exists():
                raise FileNotFoundError(f"Missing required token specification: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                key = spec_file.replace(".json", "")
                self.tokens[key] = json.load(f)

    def generate_colors_dart(self) -> str:
        """Generates lib/src/colors.dart."""
        colors_data = self.tokens["colors"]
        palettes = colors_data.get("palettes", {})
        brand = palettes.get("brand", {})
        neutral = palettes.get("neutral", {})
        red = palettes.get("red", {})
        green = palettes.get("green", {})
        amber = palettes.get("amber", {})
        blue = palettes.get("blue", {})

        semantics = colors_data.get("semantics", {})
        light = semantics.get("light", {})
        dark = semantics.get("dark", {})

        light_text = light.get("text", {})
        light_surface = light.get("surface", {})
        light_border = light.get("border", {})
        light_action = light.get("action", {})
        light_act_pri = light_action.get("primary", {})
        light_act_dest = light_action.get("destructive", {})
        light_act_dis = light_action.get("disabled", {})
        light_feedback = light.get("feedback", {})
        light_focus = light.get("focus", {})

        dark_text = dark.get("text", {})
        dark_surface = dark.get("surface", {})
        dark_border = dark.get("border", {})
        dark_action = dark.get("action", {})
        dark_act_pri = dark_action.get("primary", {})
        dark_act_dest = dark_action.get("destructive", {})
        dark_act_dis = dark_action.get("disabled", {})
        dark_feedback = dark.get("feedback", {})
        dark_focus = dark.get("focus", {})

        lines = [
            "// GENERATED CODE - DO NOT MODIFY BY HAND",
            "// Master Design System (MDS) — Flutter Token Engine",
            "// Phase 11: Multi-Platform Flutter Token Engine & Package",
            "// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)",
            "",
            "import 'package:flutter/material.dart';",
            "",
            "/// Master Design System (MDS) Color Tokens.",
            "/// Strictly typed, WCAG AAA/AA contrast-verified palettes and semantics.",
            "abstract final class MdsColors {",
            "  // ---------------------------------------------------------------------------",
            "  // Brand Palette",
            "  // ---------------------------------------------------------------------------",
        ]

        for step in ["50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950"]:
            val = brand.get(step, "#000000")
            desc = "Core Royal Sapphire" if step == "600" else f"Brand step {step}"
            lines.append(f"  /// {desc} ({val})")
            lines.append(f"  static const Color brand{step} = {hex_to_flutter_color(val)};")

        lines.extend([
            "",
            "  // ---------------------------------------------------------------------------",
            "  // Neutral Palette",
            "  // ---------------------------------------------------------------------------",
        ])

        for step in ["0", "50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950", "1000"]:
            val = neutral.get(step, "#000000")
            lines.append(f"  /// Neutral step {step} ({val})")
            lines.append(f"  static const Color neutral{step} = {hex_to_flutter_color(val)};")

        lines.extend([
            "",
            "  // ---------------------------------------------------------------------------",
            "  // Feedback Palettes (Red, Green, Amber, Blue)",
            "  // ---------------------------------------------------------------------------",
        ])

        for pal_name, pal_dict in [("red", red), ("green", green), ("amber", amber), ("blue", blue)]:
            for step, val in pal_dict.items():
                lines.append(f"  static const Color {pal_name}{step} = {hex_to_flutter_color(val)};")

        lines.extend([
            "",
            "  // ---------------------------------------------------------------------------",
            "  // Semantic Light Colors",
            "  // ---------------------------------------------------------------------------",
            f"  static const Color textPrimaryLight = {hex_to_flutter_color(light_text.get('primary', '#0F172A'))};",
            f"  static const Color textSecondaryLight = {hex_to_flutter_color(light_text.get('secondary', '#64748B'))};",
            f"  static const Color textInverseLight = {hex_to_flutter_color(light_text.get('inverse', '#FFFFFF'))};",
            "",
            f"  static const Color surfaceCanvasLight = {hex_to_flutter_color(light_surface.get('canvas', '#F8FAFC'))};",
            f"  static const Color surfaceDefaultLight = {hex_to_flutter_color(light_surface.get('default', '#FFFFFF'))};",
            f"  static const Color surfaceRaisedLight = {hex_to_flutter_color(light_surface.get('raised', '#F1F5F9'))};",
            f"  static const Color surfaceOverlayLight = {hex_to_flutter_color(light_surface.get('overlay', '#FFFFFF'))};",
            "",
            f"  static const Color borderSubtleLight = {hex_to_flutter_color(light_border.get('subtle', '#E2E8F0'))};",
            f"  static const Color borderDefaultLight = {hex_to_flutter_color(light_border.get('default', '#CBD5E1'))};",
            "",
            f"  static const Color actionPrimaryDefaultLight = {hex_to_flutter_color(light_act_pri.get('default', '#2563EB'))};",
            f"  static const Color actionPrimaryHoverLight = {hex_to_flutter_color(light_act_pri.get('hover', '#1D4ED8'))};",
            f"  static const Color actionPrimaryPressedLight = {hex_to_flutter_color(light_act_pri.get('pressed', '#1E40AF'))};",
            "",
            f"  static const Color actionDestructiveDefaultLight = {hex_to_flutter_color(light_act_dest.get('default', '#DC2626'))};",
            f"  static const Color actionDestructiveHoverLight = {hex_to_flutter_color(light_act_dest.get('hover', '#B91C1C'))};",
            "",
            f"  static const Color actionDisabledBackgroundLight = {hex_to_flutter_color(light_act_dis.get('background', '#F1F5F9'))};",
            f"  static const Color actionDisabledForegroundLight = {hex_to_flutter_color(light_act_dis.get('foreground', '#94A3B8'))};",
            "",
            f"  static const Color feedbackDangerLight = {hex_to_flutter_color(light_feedback.get('danger', '#DC2626'))};",
            f"  static const Color feedbackWarningLight = {hex_to_flutter_color(light_feedback.get('warning', '#D97706'))};",
            f"  static const Color feedbackSuccessLight = {hex_to_flutter_color(light_feedback.get('success', '#059669'))};",
            f"  static const Color feedbackInfoLight = {hex_to_flutter_color(light_feedback.get('info', '#0284C7'))};",
            f"  static const Color focusRingLight = {hex_to_flutter_color(light_focus.get('ring', '#2563EB'))};",
            "",
            "  // ---------------------------------------------------------------------------",
            "  // Semantic Dark Colors",
            "  // ---------------------------------------------------------------------------",
            f"  static const Color textPrimaryDark = {hex_to_flutter_color(dark_text.get('primary', '#FFFFFF'))};",
            f"  static const Color textSecondaryDark = {hex_to_flutter_color(dark_text.get('secondary', '#94A3B8'))};",
            f"  static const Color textInverseDark = {hex_to_flutter_color(dark_text.get('inverse', '#0F172A'))};",
            "",
            f"  static const Color surfaceCanvasDark = {hex_to_flutter_color(dark_surface.get('canvas', '#090D16'))};",
            f"  static const Color surfaceDefaultDark = {hex_to_flutter_color(dark_surface.get('default', '#0F172A'))};",
            f"  static const Color surfaceRaisedDark = {hex_to_flutter_color(dark_surface.get('raised', '#1E293B'))};",
            f"  static const Color surfaceOverlayDark = {hex_to_flutter_color(dark_surface.get('overlay', '#334155'))};",
            "",
            f"  static const Color borderSubtleDark = {hex_to_flutter_color(dark_border.get('subtle', '#1E293B'))};",
            f"  static const Color borderDefaultDark = {hex_to_flutter_color(dark_border.get('default', '#334155'))};",
            "",
            f"  static const Color actionPrimaryDefaultDark = {hex_to_flutter_color(dark_act_pri.get('default', '#3B82F6'))};",
            f"  static const Color actionPrimaryHoverDark = {hex_to_flutter_color(dark_act_pri.get('hover', '#60A5FA'))};",
            f"  static const Color actionPrimaryPressedDark = {hex_to_flutter_color(dark_act_pri.get('pressed', '#1D4ED8'))};",
            "",
            f"  static const Color actionDestructiveDefaultDark = {hex_to_flutter_color(dark_act_dest.get('default', '#EF4444'))};",
            f"  static const Color actionDestructiveHoverDark = {hex_to_flutter_color(dark_act_dest.get('hover', '#F87171'))};",
            "",
            f"  static const Color actionDisabledBackgroundDark = {hex_to_flutter_color(dark_act_dis.get('background', '#1E293B'))};",
            f"  static const Color actionDisabledForegroundDark = {hex_to_flutter_color(dark_act_dis.get('foreground', '#64748B'))};",
            "",
            f"  static const Color feedbackDangerDark = {hex_to_flutter_color(dark_feedback.get('danger', '#EF4444'))};",
            f"  static const Color feedbackWarningDark = {hex_to_flutter_color(dark_feedback.get('warning', '#F59E0B'))};",
            f"  static const Color feedbackSuccessDark = {hex_to_flutter_color(dark_feedback.get('success', '#10B981'))};",
            f"  static const Color feedbackInfoDark = {hex_to_flutter_color(dark_feedback.get('info', '#0EA5E9'))};",
            f"  static const Color focusRingDark = {hex_to_flutter_color(dark_focus.get('ring', '#60A5FA'))};",
            "}",
            "",
            "/// Material 3 ColorScheme Factory grounded in MDS tokens.",
            "abstract final class MdsColorScheme {",
            "  /// Factory for Material 3 Light ColorScheme.",
            "  static ColorScheme light() {",
            "    return const ColorScheme(",
            "      brightness: Brightness.light,",
            "      primary: MdsColors.actionPrimaryDefaultLight,",
            "      onPrimary: MdsColors.textInverseLight,",
            "      primaryContainer: MdsColors.brand100,",
            "      onPrimaryContainer: MdsColors.brand900,",
            "      secondary: MdsColors.brand500,",
            "      onSecondary: MdsColors.neutral0,",
            "      secondaryContainer: MdsColors.brand50,",
            "      onSecondaryContainer: MdsColors.brand800,",
            "      tertiary: MdsColors.blue600,",
            "      onTertiary: MdsColors.neutral0,",
            "      error: MdsColors.feedbackDangerLight,",
            "      onError: MdsColors.neutral0,",
            "      errorContainer: MdsColors.red50,",
            "      onErrorContainer: MdsColors.red700,",
            "      surface: MdsColors.surfaceDefaultLight,",
            "      onSurface: MdsColors.textPrimaryLight,",
            "      onSurfaceVariant: MdsColors.textSecondaryLight,",
            "      outline: MdsColors.borderDefaultLight,",
            "      outlineVariant: MdsColors.borderSubtleLight,",
            "      shadow: Color(0x330F172A),",
            "      inverseSurface: MdsColors.neutral900,",
            "      onInverseSurface: MdsColors.neutral0,",
            "      inversePrimary: MdsColors.brand400,",
            "    );",
            "  }",
            "",
            "  /// Factory for Material 3 Dark ColorScheme.",
            "  static ColorScheme dark() {",
            "    return const ColorScheme(",
            "      brightness: Brightness.dark,",
            "      primary: MdsColors.actionPrimaryDefaultDark,",
            "      onPrimary: MdsColors.neutral900,",
            "      primaryContainer: MdsColors.brand900,",
            "      onPrimaryContainer: MdsColors.brand100,",
            "      secondary: MdsColors.brand400,",
            "      onSecondary: MdsColors.neutral950,",
            "      secondaryContainer: MdsColors.brand800,",
            "      onSecondaryContainer: MdsColors.brand50,",
            "      tertiary: MdsColors.blue500,",
            "      onTertiary: MdsColors.neutral950,",
            "      error: MdsColors.feedbackDangerDark,",
            "      onError: MdsColors.neutral900,",
            "      errorContainer: MdsColors.red700,",
            "      onErrorContainer: MdsColors.red50,",
            "      surface: MdsColors.surfaceDefaultDark,",
            "      onSurface: MdsColors.textPrimaryDark,",
            "      onSurfaceVariant: MdsColors.textSecondaryDark,",
            "      outline: MdsColors.borderDefaultDark,",
            "      outlineVariant: MdsColors.borderSubtleDark,",
            "      shadow: Color(0x66000000),",
            "      inverseSurface: MdsColors.neutral50,",
            "      onInverseSurface: MdsColors.neutral900,",
            "      inversePrimary: MdsColors.brand600,",
            "    );",
            "  }",
            "}",
            "",
            "/// ThemeExtension for strongly typed access to semantic design tokens.",
            "@immutable",
            "class MdsSemanticColors extends ThemeExtension<MdsSemanticColors> {",
            "  const MdsSemanticColors({",
            "    required this.textPrimary,",
            "    required this.textSecondary,",
            "    required this.textInverse,",
            "    required this.surfaceCanvas,",
            "    required this.surfaceDefault,",
            "    required this.surfaceRaised,",
            "    required this.surfaceOverlay,",
            "    required this.borderSubtle,",
            "    required this.borderDefault,",
            "    required this.actionPrimaryDefault,",
            "    required this.actionPrimaryHover,",
            "    required this.actionPrimaryPressed,",
            "    required this.actionDestructiveDefault,",
            "    required this.actionDestructiveHover,",
            "    required this.actionDisabledBackground,",
            "    required this.actionDisabledForeground,",
            "    required this.feedbackDanger,",
            "    required this.feedbackWarning,",
            "    required this.feedbackSuccess,",
            "    required this.feedbackInfo,",
            "    required this.focusRing,",
            "  });",
            "",
            "  final Color textPrimary;",
            "  final Color textSecondary;",
            "  final Color textInverse;",
            "  final Color surfaceCanvas;",
            "  final Color surfaceDefault;",
            "  final Color surfaceRaised;",
            "  final Color surfaceOverlay;",
            "  final Color borderSubtle;",
            "  final Color borderDefault;",
            "  final Color actionPrimaryDefault;",
            "  final Color actionPrimaryHover;",
            "  final Color actionPrimaryPressed;",
            "  final Color actionDestructiveDefault;",
            "  final Color actionDestructiveHover;",
            "  final Color actionDisabledBackground;",
            "  final Color actionDisabledForeground;",
            "  final Color feedbackDanger;",
            "  final Color feedbackWarning;",
            "  final Color feedbackSuccess;",
            "  final Color feedbackInfo;",
            "  final Color focusRing;",
            "",
            "  factory MdsSemanticColors.light() => const MdsSemanticColors(",
            "    textPrimary: MdsColors.textPrimaryLight,",
            "    textSecondary: MdsColors.textSecondaryLight,",
            "    textInverse: MdsColors.textInverseLight,",
            "    surfaceCanvas: MdsColors.surfaceCanvasLight,",
            "    surfaceDefault: MdsColors.surfaceDefaultLight,",
            "    surfaceRaised: MdsColors.surfaceRaisedLight,",
            "    surfaceOverlay: MdsColors.surfaceOverlayLight,",
            "    borderSubtle: MdsColors.borderSubtleLight,",
            "    borderDefault: MdsColors.borderDefaultLight,",
            "    actionPrimaryDefault: MdsColors.actionPrimaryDefaultLight,",
            "    actionPrimaryHover: MdsColors.actionPrimaryHoverLight,",
            "    actionPrimaryPressed: MdsColors.actionPrimaryPressedLight,",
            "    actionDestructiveDefault: MdsColors.actionDestructiveDefaultLight,",
            "    actionDestructiveHover: MdsColors.actionDestructiveHoverLight,",
            "    actionDisabledBackground: MdsColors.actionDisabledBackgroundLight,",
            "    actionDisabledForeground: MdsColors.actionDisabledForegroundLight,",
            "    feedbackDanger: MdsColors.feedbackDangerLight,",
            "    feedbackWarning: MdsColors.feedbackWarningLight,",
            "    feedbackSuccess: MdsColors.feedbackSuccessLight,",
            "    feedbackInfo: MdsColors.feedbackInfoLight,",
            "    focusRing: MdsColors.focusRingLight,",
            "  );",
            "",
            "  factory MdsSemanticColors.dark() => const MdsSemanticColors(",
            "    textPrimary: MdsColors.textPrimaryDark,",
            "    textSecondary: MdsColors.textSecondaryDark,",
            "    textInverse: MdsColors.textInverseDark,",
            "    surfaceCanvas: MdsColors.surfaceCanvasDark,",
            "    surfaceDefault: MdsColors.surfaceDefaultDark,",
            "    surfaceRaised: MdsColors.surfaceRaisedDark,",
            "    surfaceOverlay: MdsColors.surfaceOverlayDark,",
            "    borderSubtle: MdsColors.borderSubtleDark,",
            "    borderDefault: MdsColors.borderDefaultDark,",
            "    actionPrimaryDefault: MdsColors.actionPrimaryDefaultDark,",
            "    actionPrimaryHover: MdsColors.actionPrimaryHoverDark,",
            "    actionPrimaryPressed: MdsColors.actionPrimaryPressedDark,",
            "    actionDestructiveDefault: MdsColors.actionDestructiveDefaultDark,",
            "    actionDestructiveHover: MdsColors.actionDestructiveHoverDark,",
            "    actionDisabledBackground: MdsColors.actionDisabledBackgroundDark,",
            "    actionDisabledForeground: MdsColors.actionDisabledForegroundDark,",
            "    feedbackDanger: MdsColors.feedbackDangerDark,",
            "    feedbackWarning: MdsColors.feedbackWarningDark,",
            "    feedbackSuccess: MdsColors.feedbackSuccessDark,",
            "    feedbackInfo: MdsColors.feedbackInfoDark,",
            "    focusRing: MdsColors.focusRingDark,",
            "  );",
            "",
            "  @override",
            "  MdsSemanticColors copyWith({",
            "    Color? textPrimary,",
            "    Color? textSecondary,",
            "    Color? textInverse,",
            "    Color? surfaceCanvas,",
            "    Color? surfaceDefault,",
            "    Color? surfaceRaised,",
            "    Color? surfaceOverlay,",
            "    Color? borderSubtle,",
            "    Color? borderDefault,",
            "    Color? actionPrimaryDefault,",
            "    Color? actionPrimaryHover,",
            "    Color? actionPrimaryPressed,",
            "    Color? actionDestructiveDefault,",
            "    Color? actionDestructiveHover,",
            "    Color? actionDisabledBackground,",
            "    Color? actionDisabledForeground,",
            "    Color? feedbackDanger,",
            "    Color? feedbackWarning,",
            "    Color? feedbackSuccess,",
            "    Color? feedbackInfo,",
            "    Color? focusRing,",
            "  }) {",
            "    return MdsSemanticColors(",
            "      textPrimary: textPrimary ?? this.textPrimary,",
            "      textSecondary: textSecondary ?? this.textSecondary,",
            "      textInverse: textInverse ?? this.textInverse,",
            "      surfaceCanvas: surfaceCanvas ?? this.surfaceCanvas,",
            "      surfaceDefault: surfaceDefault ?? this.surfaceDefault,",
            "      surfaceRaised: surfaceRaised ?? this.surfaceRaised,",
            "      surfaceOverlay: surfaceOverlay ?? this.surfaceOverlay,",
            "      borderSubtle: borderSubtle ?? this.borderSubtle,",
            "      borderDefault: borderDefault ?? this.borderDefault,",
            "      actionPrimaryDefault: actionPrimaryDefault ?? this.actionPrimaryDefault,",
            "      actionPrimaryHover: actionPrimaryHover ?? this.actionPrimaryHover,",
            "      actionPrimaryPressed: actionPrimaryPressed ?? this.actionPrimaryPressed,",
            "      actionDestructiveDefault: actionDestructiveDefault ?? this.actionDestructiveDefault,",
            "      actionDestructiveHover: actionDestructiveHover ?? this.actionDestructiveHover,",
            "      actionDisabledBackground: actionDisabledBackground ?? this.actionDisabledBackground,",
            "      actionDisabledForeground: actionDisabledForeground ?? this.actionDisabledForeground,",
            "      feedbackDanger: feedbackDanger ?? this.feedbackDanger,",
            "      feedbackWarning: feedbackWarning ?? this.feedbackWarning,",
            "      feedbackSuccess: feedbackSuccess ?? this.feedbackSuccess,",
            "      feedbackInfo: feedbackInfo ?? this.feedbackInfo,",
            "      focusRing: focusRing ?? this.focusRing,",
            "    );",
            "  }",
            "",
            "  @override",
            "  MdsSemanticColors lerp(ThemeExtension<MdsSemanticColors>? other, double t) {",
            "    if (other is! MdsSemanticColors) return this;",
            "    return MdsSemanticColors(",
            "      textPrimary: Color.lerp(textPrimary, other.textPrimary, t)!,",
            "      textSecondary: Color.lerp(textSecondary, other.textSecondary, t)!,",
            "      textInverse: Color.lerp(textInverse, other.textInverse, t)!,",
            "      surfaceCanvas: Color.lerp(surfaceCanvas, other.surfaceCanvas, t)!,",
            "      surfaceDefault: Color.lerp(surfaceDefault, other.surfaceDefault, t)!,",
            "      surfaceRaised: Color.lerp(surfaceRaised, other.surfaceRaised, t)!,",
            "      surfaceOverlay: Color.lerp(surfaceOverlay, other.surfaceOverlay, t)!,",
            "      borderSubtle: Color.lerp(borderSubtle, other.borderSubtle, t)!,",
            "      borderDefault: Color.lerp(borderDefault, other.borderDefault, t)!,",
            "      actionPrimaryDefault: Color.lerp(actionPrimaryDefault, other.actionPrimaryDefault, t)!,",
            "      actionPrimaryHover: Color.lerp(actionPrimaryHover, other.actionPrimaryHover, t)!,",
            "      actionPrimaryPressed: Color.lerp(actionPrimaryPressed, other.actionPrimaryPressed, t)!,",
            "      actionDestructiveDefault: Color.lerp(actionDestructiveDefault, other.actionDestructiveDefault, t)!,",
            "      actionDestructiveHover: Color.lerp(actionDestructiveHover, other.actionDestructiveHover, t)!,",
            "      actionDisabledBackground: Color.lerp(actionDisabledBackground, other.actionDisabledBackground, t)!,",
            "      actionDisabledForeground: Color.lerp(actionDisabledForeground, other.actionDisabledForeground, t)!,",
            "      feedbackDanger: Color.lerp(feedbackDanger, other.feedbackDanger, t)!,",
            "      feedbackWarning: Color.lerp(feedbackWarning, other.feedbackWarning, t)!,",
            "      feedbackSuccess: Color.lerp(feedbackSuccess, other.feedbackSuccess, t)!,",
            "      feedbackInfo: Color.lerp(feedbackInfo, other.feedbackInfo, t)!,",
            "      focusRing: Color.lerp(focusRing, other.focusRing, t)!,",
            "    );",
            "  }",
            "}",
            "",
        ])

        return normalize_newlines("\n".join(lines))

    def generate_typography_dart(self) -> str:
        """Generates lib/src/typography.dart."""
        typo = self.tokens["typography"]
        weights = typo.get("weights", {})
        sizes = typo.get("sizes", {})
        line_heights = typo.get("line_heights", {})

        lines = [
            "// GENERATED CODE - DO NOT MODIFY BY HAND",
            "// Master Design System (MDS) — Flutter Token Engine",
            "// Phase 11: Multi-Platform Flutter Token Engine & Package",
            "// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)",
            "",
            "import 'package:flutter/material.dart';",
            "import 'package:google_fonts/google_fonts.dart';",
            "import 'colors.dart';",
            "",
            "/// Master Design System (MDS) Typography.",
            "/// Strictly Cairo font family with Arabic (RTL) & English (LTR) metrics.",
            "abstract final class MdsTypography {",
            "  /// Primary multilingual font family (strictly Cairo).",
            "  static const String primaryFontFamily = 'Cairo';",
            "",
            "  /// Monospace font family.",
            "  static const String monoFontFamily = 'JetBrains Mono';",
            "",
            "  // ---------------------------------------------------------------------------",
            "  // Font Weights",
            "  // ---------------------------------------------------------------------------",
            f"  static const FontWeight regular = FontWeight.w{weights.get('regular', 400)};",
            f"  static const FontWeight medium = FontWeight.w{weights.get('medium', 500)};",
            f"  static const FontWeight semibold = FontWeight.w{weights.get('semibold', 600)};",
            f"  static const FontWeight bold = FontWeight.w{weights.get('bold', 700)};",
            "",
            "  // ---------------------------------------------------------------------------",
            "  // Font Sizes",
            "  // ---------------------------------------------------------------------------",
            f"  static const double sizeXs = {sizes.get('xs', 12.0):.1f};",
            f"  static const double sizeSm = {sizes.get('sm', 14.0):.1f};",
            f"  static const double sizeBase = {sizes.get('base', 16.0):.1f};",
            f"  static const double sizeLg = {sizes.get('lg', 20.0):.1f};",
            f"  static const double sizeXl = {sizes.get('xl', 24.0):.1f};",
            f"  static const double size2xl = {sizes.get('2xl', 30.0):.1f};",
            f"  static const double size3xl = {sizes.get('3xl', 36.0):.1f};",
            f"  static const double size4xl = {sizes.get('4xl', 48.0):.1f};",
            "",
            "  // ---------------------------------------------------------------------------",
            "  // Line Heights",
            "  // ---------------------------------------------------------------------------",
            f"  static const double lineHeightTight = {line_heights.get('tight', 1.25)};",
            f"  static const double lineHeightNormal = {line_heights.get('normal', 1.5)};",
            f"  static const double lineHeightRelaxed = {line_heights.get('relaxed', 1.75)};",
            "",
            "  // ---------------------------------------------------------------------------",
            "  // Cairo TextStyle Factory",
            "  // ---------------------------------------------------------------------------",
            "  static TextStyle cairo({",
            "    double? fontSize,",
            "    FontWeight? fontWeight,",
            "    Color? color,",
            "    double? height,",
            "    double? letterSpacing,",
            "    TextDecoration? decoration,",
            "  }) {",
            "    if (!GoogleFonts.config.allowRuntimeFetching) {",
            "      return TextStyle(",
            "        fontFamily: primaryFontFamily,",
            "        fontFamilyFallback: const <String>[primaryFontFamily, 'sans-serif'],",
            "        fontSize: fontSize,",
            "        fontWeight: fontWeight,",
            "        color: color,",
            "        height: height,",
            "        letterSpacing: letterSpacing,",
            "        decoration: decoration,",
            "      );",
            "    }",
            "    return GoogleFonts.cairo(",
            "      fontSize: fontSize,",
            "      fontWeight: fontWeight,",
            "      color: color,",
            "      height: height,",
            "      letterSpacing: letterSpacing,",
            "      decoration: decoration,",
            "    );",
            "  }",
            "",
            "  // ---------------------------------------------------------------------------",
            "  // Material 3 Cairo TextTheme Factory",
            "  // ---------------------------------------------------------------------------",
            "  static TextTheme createTextTheme({",
            "    Color primaryColor = MdsColors.textPrimaryLight,",
            "    Color secondaryColor = MdsColors.textSecondaryLight,",
            "  }) {",
            "    return TextTheme(",
            "      displayLarge: cairo(fontSize: size4xl, fontWeight: bold, height: lineHeightTight, color: primaryColor, letterSpacing: -0.5),",
            "      displayMedium: cairo(fontSize: size3xl, fontWeight: bold, height: lineHeightTight, color: primaryColor, letterSpacing: -0.25),",
            "      displaySmall: cairo(fontSize: size2xl, fontWeight: semibold, height: lineHeightTight, color: primaryColor),",
            "      headlineLarge: cairo(fontSize: size2xl, fontWeight: semibold, height: lineHeightTight, color: primaryColor),",
            "      headlineMedium: cairo(fontSize: sizeXl, fontWeight: semibold, height: lineHeightTight, color: primaryColor),",
            "      headlineSmall: cairo(fontSize: sizeLg, fontWeight: semibold, height: lineHeightNormal, color: primaryColor),",
            "      titleLarge: cairo(fontSize: sizeLg, fontWeight: semibold, height: lineHeightNormal, color: primaryColor),",
            "      titleMedium: cairo(fontSize: sizeBase, fontWeight: semibold, height: lineHeightNormal, color: primaryColor, letterSpacing: 0.15),",
            "      titleSmall: cairo(fontSize: sizeSm, fontWeight: semibold, height: lineHeightNormal, color: primaryColor, letterSpacing: 0.1),",
            "      bodyLarge: cairo(fontSize: sizeBase, fontWeight: regular, height: lineHeightNormal, color: primaryColor, letterSpacing: 0.5),",
            "      bodyMedium: cairo(fontSize: sizeSm, fontWeight: regular, height: lineHeightNormal, color: primaryColor, letterSpacing: 0.25),",
            "      bodySmall: cairo(fontSize: sizeXs, fontWeight: regular, height: lineHeightNormal, color: secondaryColor, letterSpacing: 0.4),",
            "      labelLarge: cairo(fontSize: sizeSm, fontWeight: medium, height: lineHeightTight, color: primaryColor, letterSpacing: 0.1),",
            "      labelMedium: cairo(fontSize: sizeXs, fontWeight: medium, height: lineHeightTight, color: secondaryColor, letterSpacing: 0.5),",
            "      labelSmall: cairo(fontSize: 10.0, fontWeight: medium, height: lineHeightTight, color: secondaryColor, letterSpacing: 0.5),",
            "    );",
            "  }",
            "}",
            "",
        ]
        return normalize_newlines("\n".join(lines))

    def generate_spacing_dart(self) -> str:
        """Generates lib/src/spacing.dart."""
        spacing = self.tokens["spacing"]
        scale = spacing.get("scale", {})
        semantic = spacing.get("semantic", {})
        inline = semantic.get("inline", {})
        block = semantic.get("block", {})

        lines = [
            "// GENERATED CODE - DO NOT MODIFY BY HAND",
            "// Master Design System (MDS) — Flutter Token Engine",
            "// Phase 11: Multi-Platform Flutter Token Engine & Package",
            "// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)",
            "",
            "import 'package:flutter/material.dart';",
            "",
            "/// Master Design System (MDS) Spacing Scale & Helpers.",
            "/// Standard 4px grid with directional / RTL-safe padding definitions.",
            "abstract final class MdsSpacing {",
            "  // ---------------------------------------------------------------------------",
            "  // 4px / 8px Grid Scale",
            "  // ---------------------------------------------------------------------------",
        ]

        for step in ["0", "1", "2", "3", "4", "5", "6", "8", "10", "12", "16"]:
            val = float(scale.get(step, 0.0))
            lines.append(f"  /// {val}px spacing scalar step {step}")
            lines.append(f"  static const double space{step} = {val:.1f};")

        lines.extend([
            "",
            "  // ---------------------------------------------------------------------------",
            "  // Semantic Spacing Aliases",
            "  // ---------------------------------------------------------------------------",
            f"  static const double inlineXs = {float(inline.get('xs', 4.0)):.1f};",
            f"  static const double inlineSm = {float(inline.get('sm', 8.0)):.1f};",
            f"  static const double inlineMd = {float(inline.get('md', 16.0)):.1f};",
            f"  static const double inlineLg = {float(inline.get('lg', 24.0)):.1f};",
            "",
            f"  static const double blockXs = {float(block.get('xs', 4.0)):.1f};",
            f"  static const double blockSm = {float(block.get('sm', 8.0)):.1f};",
            f"  static const double blockMd = {float(block.get('md', 16.0)):.1f};",
            f"  static const double blockLg = {float(block.get('lg', 32.0)):.1f};",
            "",
            "  // ---------------------------------------------------------------------------",
            "  // Directional EdgeInsets (Arabic RTL & English LTR Safe)",
            "  // ---------------------------------------------------------------------------",
            "  static const EdgeInsetsDirectional paddingInlineXs = EdgeInsetsDirectional.symmetric(horizontal: inlineXs);",
            "  static const EdgeInsetsDirectional paddingInlineSm = EdgeInsetsDirectional.symmetric(horizontal: inlineSm);",
            "  static const EdgeInsetsDirectional paddingInlineMd = EdgeInsetsDirectional.symmetric(horizontal: inlineMd);",
            "  static const EdgeInsetsDirectional paddingInlineLg = EdgeInsetsDirectional.symmetric(horizontal: inlineLg);",
            "",
            "  static const EdgeInsetsDirectional paddingBlockXs = EdgeInsetsDirectional.symmetric(vertical: blockXs);",
            "  static const EdgeInsetsDirectional paddingBlockSm = EdgeInsetsDirectional.symmetric(vertical: blockSm);",
            "  static const EdgeInsetsDirectional paddingBlockMd = EdgeInsetsDirectional.symmetric(vertical: blockMd);",
            "  static const EdgeInsetsDirectional paddingBlockLg = EdgeInsetsDirectional.symmetric(vertical: blockLg);",
            "",
            "  static const EdgeInsetsDirectional paddingCardSm = EdgeInsetsDirectional.all(12.0);",
            "  static const EdgeInsetsDirectional paddingCardMd = EdgeInsetsDirectional.all(16.0);",
            "  static const EdgeInsetsDirectional paddingCardLg = EdgeInsetsDirectional.all(24.0);",
            "",
            "  static const EdgeInsetsDirectional paddingButtonSm = EdgeInsetsDirectional.symmetric(horizontal: 12.0, vertical: 6.0);",
            "  static const EdgeInsetsDirectional paddingButtonMd = EdgeInsetsDirectional.symmetric(horizontal: 16.0, vertical: 10.0);",
            "  static const EdgeInsetsDirectional paddingButtonLg = EdgeInsetsDirectional.symmetric(horizontal: 20.0, vertical: 12.0);",
            "",
            "  static const EdgeInsetsDirectional paddingInput = EdgeInsetsDirectional.symmetric(horizontal: 12.0, vertical: 10.0);",
            "",
            "  // ---------------------------------------------------------------------------",
            "  // SizedBox Gaps",
            "  // ---------------------------------------------------------------------------",
            "  static const SizedBox gapHorizontalXs = SizedBox(width: inlineXs);",
            "  static const SizedBox gapHorizontalSm = SizedBox(width: inlineSm);",
            "  static const SizedBox gapHorizontalMd = SizedBox(width: inlineMd);",
            "  static const SizedBox gapHorizontalLg = SizedBox(width: inlineLg);",
            "",
            "  static const SizedBox gapVerticalXs = SizedBox(height: blockXs);",
            "  static const SizedBox gapVerticalSm = SizedBox(height: blockSm);",
            "  static const SizedBox gapVerticalMd = SizedBox(height: blockMd);",
            "  static const SizedBox gapVerticalLg = SizedBox(height: blockLg);",
            "}",
            "",
        ])
        return normalize_newlines("\n".join(lines))

    def generate_radius_dart(self) -> str:
        """Generates lib/src/radius.dart."""
        radius_data = self.tokens["radius"]
        scale = radius_data.get("scale", {})
        border_width = radius_data.get("border_width", {})

        lines = [
            "// GENERATED CODE - DO NOT MODIFY BY HAND",
            "// Master Design System (MDS) — Flutter Token Engine",
            "// Phase 11: Multi-Platform Flutter Token Engine & Package",
            "// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)",
            "",
            "import 'package:flutter/material.dart';",
            "",
            "/// Master Design System (MDS) Corner Radii & Border Widths.",
            "/// Signature 10px Soft Modern radius with directional helpers.",
            "abstract final class MdsRadius {",
            "  // ---------------------------------------------------------------------------",
            "  // Radius Scalars",
            "  // ---------------------------------------------------------------------------",
            f"  static const double none = {float(scale.get('none', 0.0)):.1f};",
            f"  static const double xs = {float(scale.get('xs', 4.0)):.1f};",
            f"  static const double sm = {float(scale.get('sm', 6.0)):.1f};",
            f"  static const double md = {float(scale.get('md', 10.0)):.1f};",
            f"  static const double lg = {float(scale.get('lg', 14.0)):.1f};",
            f"  static const double xl = {float(scale.get('xl', 20.0)):.1f};",
            f"  static const double full = {float(scale.get('full', 9999.0)):.1f};",
            "",
            "  // ---------------------------------------------------------------------------",
            "  // Border Widths",
            "  // ---------------------------------------------------------------------------",
            f"  static const double borderWidthThin = {float(border_width.get('thin', 1.0)):.1f};",
            f"  static const double borderWidthRegular = {float(border_width.get('regular', 1.5)):.1f};",
            f"  static const double borderWidthThick = {float(border_width.get('thick', 2.0)):.1f};",
            "",
            "  // ---------------------------------------------------------------------------",
            "  // BorderRadius Helpers",
            "  // ---------------------------------------------------------------------------",
            "  static const BorderRadius borderNone = BorderRadius.zero;",
            "  static const BorderRadius borderXs = BorderRadius.all(Radius.circular(xs));",
            "  static const BorderRadius borderSm = BorderRadius.all(Radius.circular(sm));",
            "  static const BorderRadius borderMd = BorderRadius.all(Radius.circular(md));",
            "  static const BorderRadius borderLg = BorderRadius.all(Radius.circular(lg));",
            "  static const BorderRadius borderXl = BorderRadius.all(Radius.circular(xl));",
            "  static const BorderRadius borderFull = BorderRadius.all(Radius.circular(full));",
            "",
            "  // ---------------------------------------------------------------------------",
            "  // Directional BorderRadius (RTL / LTR Bi-directional Safe)",
            "  // ---------------------------------------------------------------------------",
            "  static const BorderRadiusDirectional directionalNone = BorderRadiusDirectional.zero;",
            "  static const BorderRadiusDirectional directionalXs = BorderRadiusDirectional.all(Radius.circular(xs));",
            "  static const BorderRadiusDirectional directionalSm = BorderRadiusDirectional.all(Radius.circular(sm));",
            "  static const BorderRadiusDirectional directionalMd = BorderRadiusDirectional.all(Radius.circular(md));",
            "  static const BorderRadiusDirectional directionalLg = BorderRadiusDirectional.all(Radius.circular(lg));",
            "  static const BorderRadiusDirectional directionalXl = BorderRadiusDirectional.all(Radius.circular(xl));",
            "  static const BorderRadiusDirectional directionalFull = BorderRadiusDirectional.all(Radius.circular(full));",
            "",
            "  /// Directional start radius helper (Leading corners in RTL/LTR).",
            "  static BorderRadiusDirectional directionalStartOnly([double radius = md]) =>",
            "      BorderRadiusDirectional.horizontal(start: Radius.circular(radius));",
            "",
            "  /// Directional end radius helper (Trailing corners in RTL/LTR).",
            "  static BorderRadiusDirectional directionalEndOnly([double radius = md]) =>",
            "      BorderRadiusDirectional.horizontal(end: Radius.circular(radius));",
            "",
            "  /// Directional top radius helper.",
            "  static BorderRadiusDirectional directionalTopOnly([double radius = md]) =>",
            "      BorderRadiusDirectional.vertical(top: Radius.circular(radius));",
            "",
            "  /// Directional bottom radius helper.",
            "  static BorderRadiusDirectional directionalBottomOnly([double radius = md]) =>",
            "      BorderRadiusDirectional.vertical(bottom: Radius.circular(radius));",
            "}",
            "",
        ]
        return normalize_newlines("\n".join(lines))

    def generate_elevation_dart(self) -> str:
        """Generates lib/src/elevation.dart."""
        elev = self.tokens["elevation"]
        levels = elev.get("levels", {})

        def parse_shadow_color(color_str: str) -> str:
            # Handles "rgba(15, 23, 42, 0.06)" or hex
            if color_str.startswith("rgba(") and color_str.endswith(")"):
                inner = color_str[5:-1]
                parts = [p.strip() for p in inner.split(",")]
                r = int(parts[0])
                g = int(parts[1])
                b = int(parts[2])
                a = float(parts[3])
                alpha_int = int(round(a * 255))
                return f"Color(0x{alpha_int:02X}{r:02X}{g:02X}{b:02X})"
            return hex_to_flutter_color(color_str)

        lines = [
            "// GENERATED CODE - DO NOT MODIFY BY HAND",
            "// Master Design System (MDS) — Flutter Token Engine",
            "// Phase 11: Multi-Platform Flutter Token Engine & Package",
            "// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)",
            "",
            "import 'package:flutter/material.dart';",
            "",
            "/// Master Design System (MDS) Elevation Depths & Shadows.",
            "abstract final class MdsElevation {",
            "  // ---------------------------------------------------------------------------",
            "  // Depth Scalars",
            "  // ---------------------------------------------------------------------------",
            f"  static const double level0 = {float(levels.get('level0', {}).get('elevation', 0.0)):.1f};",
            f"  static const double level1 = {float(levels.get('level1', {}).get('elevation', 1.0)):.1f};",
            f"  static const double level2 = {float(levels.get('level2', {}).get('elevation', 3.0)):.1f};",
            f"  static const double level3 = {float(levels.get('level3', {}).get('elevation', 6.0)):.1f};",
            "",
            "  // ---------------------------------------------------------------------------",
            "  // BoxShadow Lists",
            "  // ---------------------------------------------------------------------------",
        ]

        for lvl_name in ["level0", "level1", "level2", "level3"]:
            lvl_info = levels.get(lvl_name, {})
            shadows = lvl_info.get("shadows", [])
            lvl_num = lvl_name.replace("level", "")
            if not shadows or (len(shadows) == 1 and shadows[0].get("blur") == 0 and shadows[0].get("offsetY") == 0):
                lines.append(f"  static const List<BoxShadow> shadow{lvl_num} = <BoxShadow>[];")
            else:
                lines.append(f"  static const List<BoxShadow> shadow{lvl_num} = <BoxShadow>[")
                for s in shadows:
                    ox = float(s.get("offsetX", 0.0))
                    oy = float(s.get("offsetY", 0.0))
                    blur = float(s.get("blur", 0.0))
                    spread = float(s.get("spread", 0.0))
                    color_call = parse_shadow_color(s.get("color", "rgba(0,0,0,0)"))
                    lines.append(f"    BoxShadow(")
                    lines.append(f"      offset: Offset({ox:.1f}, {oy:.1f}),")
                    lines.append(f"      blurRadius: {blur:.1f},")
                    lines.append(f"      spreadRadius: {spread:.1f},")
                    lines.append(f"      color: {color_call},")
                    lines.append(f"    ),")
                lines.append("  ];")

        lines.extend([
            "",
            "  /// Resolves BoxShadow list by elevation level index (0..3).",
            "  static List<BoxShadow> getShadow(int level) => switch (level) {",
            "    1 => shadow1,",
            "    2 => shadow2,",
            "    3 => shadow3,",
            "    _ => shadow0,",
            "  };",
            "}",
            "",
        ])
        return normalize_newlines("\n".join(lines))

    def generate_motion_dart(self) -> str:
        """Generates lib/src/motion.dart."""
        motion = self.tokens["motion"]
        durations = motion.get("durations", {})
        easing = motion.get("easing", {})

        lines = [
            "// GENERATED CODE - DO NOT MODIFY BY HAND",
            "// Master Design System (MDS) — Flutter Token Engine",
            "// Phase 11: Multi-Platform Flutter Token Engine & Package",
            "// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)",
            "",
            "import 'package:flutter/material.dart';",
            "",
            "/// Master Design System (MDS) Animation Durations.",
            "abstract final class MdsDurations {",
            f"  static const Duration instant = Duration(milliseconds: {int(durations.get('instant', 0))});",
            f"  static const Duration fast = Duration(milliseconds: {int(durations.get('fast', 150))});",
            f"  static const Duration normal = Duration(milliseconds: {int(durations.get('normal', 250))});",
            f"  static const Duration slow = Duration(milliseconds: {int(durations.get('slow', 350))});",
            "}",
            "",
            "/// Master Design System (MDS) Easing Curves (Cubic-bezier).",
            "abstract final class MdsCurves {",
        ]

        for curve_name in ["standard", "enter", "exit"]:
            coords = easing.get(curve_name, [0.2, 0.0, 0.0, 1.0])
            desc = "Signature MDS natural curve" if curve_name == "standard" else f"Curve {curve_name}"
            lines.append(f"  /// {desc} ({coords})")
            lines.append(f"  static const Cubic {curve_name} = Cubic({coords[0]}, {coords[1]}, {coords[2]}, {coords[3]});")

        lines.extend([
            "}",
            "",
        ])
        return normalize_newlines("\n".join(lines))

    def generate_theme_dart(self) -> str:
        """Generates lib/src/theme.dart."""
        lines = [
            "// GENERATED CODE - DO NOT MODIFY BY HAND",
            "// Master Design System (MDS) — Flutter Token Engine",
            "// Phase 11: Multi-Platform Flutter Token Engine & Package",
            "// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)",
            "",
            "import 'package:flutter/material.dart';",
            "import 'colors.dart';",
            "import 'radius.dart';",
            "import 'spacing.dart';",
            "import 'typography.dart';",
            "",
            "/// Production-grade Material 3 ThemeData Factory for Light & Dark modes.",
            "abstract final class MdsThemeData {",
            "  /// Builds complete Material 3 Light ThemeData derived directly from MDS tokens.",
            "  static ThemeData light() {",
            "    final colorScheme = MdsColorScheme.light();",
            "    final textTheme = MdsTypography.createTextTheme(",
            "      primaryColor: MdsColors.textPrimaryLight,",
            "      secondaryColor: MdsColors.textSecondaryLight,",
            "    );",
            "",
            "    return ThemeData(",
            "      useMaterial3: true,",
            "      brightness: Brightness.light,",
            "      colorScheme: colorScheme,",
            "      textTheme: textTheme,",
            "      fontFamily: MdsTypography.primaryFontFamily,",
            "      scaffoldBackgroundColor: MdsColors.surfaceCanvasLight,",
            "      cardTheme: const CardThemeData(",
            "        elevation: 0,",
            "        color: MdsColors.surfaceDefaultLight,",
            "        margin: EdgeInsets.zero,",
            "        shape: RoundedRectangleBorder(",
            "          borderRadius: MdsRadius.borderMd,",
            "          side: BorderSide(color: MdsColors.borderSubtleLight, width: MdsRadius.borderWidthThin),",
            "        ),",
            "      ),",
            "      appBarTheme: AppBarTheme(",
            "        elevation: 0,",
            "        scrolledUnderElevation: 1,",
            "        backgroundColor: MdsColors.surfaceDefaultLight,",
            "        foregroundColor: MdsColors.textPrimaryLight,",
            "        centerTitle: false,",
            "        titleTextStyle: MdsTypography.cairo(",
            "          fontSize: MdsTypography.sizeLg,",
            "          fontWeight: MdsTypography.semibold,",
            "          color: MdsColors.textPrimaryLight,",
            "        ),",
            "      ),",
            "      elevatedButtonTheme: ElevatedButtonThemeData(",
            "        style: ElevatedButton.styleFrom(",
            "          elevation: 0,",
            "          backgroundColor: MdsColors.actionPrimaryDefaultLight,",
            "          foregroundColor: MdsColors.textInverseLight,",
            "          shape: const RoundedRectangleBorder(borderRadius: MdsRadius.borderMd),",
            "          padding: MdsSpacing.paddingButtonMd,",
            "          textStyle: MdsTypography.cairo(",
            "            fontSize: MdsTypography.sizeSm,",
            "            fontWeight: MdsTypography.medium,",
            "          ),",
            "        ),",
            "      ),",
            "      outlinedButtonTheme: OutlinedButtonThemeData(",
            "        style: OutlinedButton.styleFrom(",
            "          foregroundColor: MdsColors.actionPrimaryDefaultLight,",
            "          side: const BorderSide(color: MdsColors.borderDefaultLight, width: MdsRadius.borderWidthThin),",
            "          shape: const RoundedRectangleBorder(borderRadius: MdsRadius.borderMd),",
            "          padding: MdsSpacing.paddingButtonMd,",
            "          textStyle: MdsTypography.cairo(",
            "            fontSize: MdsTypography.sizeSm,",
            "            fontWeight: MdsTypography.medium,",
            "          ),",
            "        ),",
            "      ),",
            "      inputDecorationTheme: const InputDecorationTheme(",
            "        filled: true,",
            "        fillColor: MdsColors.surfaceDefaultLight,",
            "        contentPadding: MdsSpacing.paddingInput,",
            "        border: OutlineInputBorder(",
            "          borderRadius: MdsRadius.borderMd,",
            "          borderSide: BorderSide(color: MdsColors.borderDefaultLight, width: MdsRadius.borderWidthThin),",
            "        ),",
            "        enabledBorder: OutlineInputBorder(",
            "          borderRadius: MdsRadius.borderMd,",
            "          borderSide: BorderSide(color: MdsColors.borderDefaultLight, width: MdsRadius.borderWidthThin),",
            "        ),",
            "        focusedBorder: OutlineInputBorder(",
            "          borderRadius: MdsRadius.borderMd,",
            "          borderSide: BorderSide(color: MdsColors.focusRingLight, width: MdsRadius.borderWidthThick),",
            "        ),",
            "      ),",
            "      extensions: <ThemeExtension<dynamic>>[",
            "        MdsSemanticColors.light(),",
            "      ],",
            "    );",
            "  }",
            "",
            "  /// Builds complete Material 3 Dark ThemeData derived directly from MDS tokens.",
            "  static ThemeData dark() {",
            "    final colorScheme = MdsColorScheme.dark();",
            "    final textTheme = MdsTypography.createTextTheme(",
            "      primaryColor: MdsColors.textPrimaryDark,",
            "      secondaryColor: MdsColors.textSecondaryDark,",
            "    );",
            "",
            "    return ThemeData(",
            "      useMaterial3: true,",
            "      brightness: Brightness.dark,",
            "      colorScheme: colorScheme,",
            "      textTheme: textTheme,",
            "      fontFamily: MdsTypography.primaryFontFamily,",
            "      scaffoldBackgroundColor: MdsColors.surfaceCanvasDark,",
            "      cardTheme: const CardThemeData(",
            "        elevation: 0,",
            "        color: MdsColors.surfaceDefaultDark,",
            "        margin: EdgeInsets.zero,",
            "        shape: RoundedRectangleBorder(",
            "          borderRadius: MdsRadius.borderMd,",
            "          side: BorderSide(color: MdsColors.borderSubtleDark, width: MdsRadius.borderWidthThin),",
            "        ),",
            "      ),",
            "      appBarTheme: AppBarTheme(",
            "        elevation: 0,",
            "        scrolledUnderElevation: 1,",
            "        backgroundColor: MdsColors.surfaceDefaultDark,",
            "        foregroundColor: MdsColors.textPrimaryDark,",
            "        centerTitle: false,",
            "        titleTextStyle: MdsTypography.cairo(",
            "          fontSize: MdsTypography.sizeLg,",
            "          fontWeight: MdsTypography.semibold,",
            "          color: MdsColors.textPrimaryDark,",
            "        ),",
            "      ),",
            "      elevatedButtonTheme: ElevatedButtonThemeData(",
            "        style: ElevatedButton.styleFrom(",
            "          elevation: 0,",
            "          backgroundColor: MdsColors.actionPrimaryDefaultDark,",
            "          foregroundColor: MdsColors.neutral900,",
            "          shape: const RoundedRectangleBorder(borderRadius: MdsRadius.borderMd),",
            "          padding: MdsSpacing.paddingButtonMd,",
            "          textStyle: MdsTypography.cairo(",
            "            fontSize: MdsTypography.sizeSm,",
            "            fontWeight: MdsTypography.medium,",
            "          ),",
            "        ),",
            "      ),",
            "      outlinedButtonTheme: OutlinedButtonThemeData(",
            "        style: OutlinedButton.styleFrom(",
            "          foregroundColor: MdsColors.actionPrimaryDefaultDark,",
            "          side: const BorderSide(color: MdsColors.borderDefaultDark, width: MdsRadius.borderWidthThin),",
            "          shape: const RoundedRectangleBorder(borderRadius: MdsRadius.borderMd),",
            "          padding: MdsSpacing.paddingButtonMd,",
            "          textStyle: MdsTypography.cairo(",
            "            fontSize: MdsTypography.sizeSm,",
            "            fontWeight: MdsTypography.medium,",
            "          ),",
            "        ),",
            "      ),",
            "      inputDecorationTheme: const InputDecorationTheme(",
            "        filled: true,",
            "        fillColor: MdsColors.surfaceDefaultDark,",
            "        contentPadding: MdsSpacing.paddingInput,",
            "        border: OutlineInputBorder(",
            "          borderRadius: MdsRadius.borderMd,",
            "          borderSide: BorderSide(color: MdsColors.borderDefaultDark, width: MdsRadius.borderWidthThin),",
            "        ),",
            "        enabledBorder: OutlineInputBorder(",
            "          borderRadius: MdsRadius.borderMd,",
            "          borderSide: BorderSide(color: MdsColors.borderDefaultDark, width: MdsRadius.borderWidthThin),",
            "        ),",
            "        focusedBorder: OutlineInputBorder(",
            "          borderRadius: MdsRadius.borderMd,",
            "          borderSide: BorderSide(color: MdsColors.focusRingDark, width: MdsRadius.borderWidthThick),",
            "        ),",
            "      ),",
            "      extensions: <ThemeExtension<dynamic>>[",
            "        MdsSemanticColors.dark(),",
            "      ],",
            "    );",
            "  }",
            "}",
            "",
            "/// Context convenience extension for accessing MDS tokens.",
            "extension MdsThemeContextExtension on BuildContext {",
            "  ThemeData get theme => Theme.of(this);",
            "  ColorScheme get colorScheme => Theme.of(this).colorScheme;",
            "  TextTheme get textTheme => Theme.of(this).textTheme;",
            "  MdsSemanticColors get mdsColors =>",
            "      Theme.of(this).extension<MdsSemanticColors>() ?? MdsSemanticColors.light();",
            "}",
            "",
        ]
        return normalize_newlines("\n".join(lines))

    def generate_barrel_dart(self) -> str:
        """Generates lib/mds_flutter_tokens.dart."""
        lines = [
            "// GENERATED CODE - DO NOT MODIFY BY HAND",
            "// Master Design System (MDS) — Flutter Token Engine",
            "// Phase 11: Multi-Platform Flutter Token Engine & Package",
            "// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)",
            "",
            "library;",
            "",
            "export 'src/colors.dart';",
            "export 'src/elevation.dart';",
            "export 'src/motion.dart';",
            "export 'src/radius.dart';",
            "export 'src/spacing.dart';",
            "export 'src/theme.dart';",
            "export 'src/typography.dart';",
            "",
        ]
        return normalize_newlines("\n".join(lines))

    def generate_pubspec_yaml(self) -> str:
        """Generates pubspec.yaml."""
        lines = [
            "name: mds_flutter_tokens",
            "description: Master Design System (MDS) design tokens, Cairo typography, and Material 3 theme builders for Flutter.",
            "version: 1.0.0",
            "publish_to: none",
            "",
            "environment:",
            "  sdk: ^3.0.0",
            '  flutter: ">=3.10.0"',
            "",
            "dependencies:",
            "  flutter:",
            "    sdk: flutter",
            "  google_fonts: ^6.2.1",
            "",
            "dev_dependencies:",
            "  flutter_test:",
            "    sdk: flutter",
            "  flutter_lints: ^5.0.0",
            "",
        ]
        return normalize_newlines("\n".join(lines))

    def generate_analysis_options_yaml(self) -> str:
        """Generates analysis_options.yaml."""
        lines = [
            "include: package:flutter_lints/flutter.yaml",
            "",
            "analyzer:",
            "  language:",
            "    strict-casts: true",
            "    strict-inference: true",
            "    strict-raw-types: true",
            "  errors:",
            "    missing_required_param: error",
            "    missing_return: error",
            "    todo: ignore",
            "",
            "linter:",
            "  rules:",
            "    - prefer_const_constructors",
            "    - prefer_const_declarations",
            "    - prefer_final_locals",
            "    - avoid_print",
            "    - use_super_parameters",
            "",
        ]
        return normalize_newlines("\n".join(lines))

    def generate_readme_md(self) -> str:
        """Generates README.md."""
        lines = [
            "# Master Design System (MDS) — Flutter Tokens Package",
            "",
            "Official Flutter design token package for the **Master Design System (MDS)**.",
            "",
            "**Lead Architect & Project Owner:** Mohamed Khalid (Senior Full Stack & Flutter Developer)",
            "",
            "## 📦 Features",
            "- **Strictly Typed Tokens:** Colors, Typography, Spacing, Radius, Elevation, Motion.",
            "- **Cairo Typography:** Default typography using Cairo font across all 15 M3 text styles.",
            "- **Material 3 Themes:** Production-ready `MdsThemeData.light()` and `MdsThemeData.dark()`.",
            "- **RTL & Bidirectional Safe:** Directional padding and radius helpers with zero hardcoded left/right values.",
            "- **Theme Extension:** Strongly typed `MdsSemanticColors` accessible via `context.mdsColors`.",
            "",
            "## 🚀 Usage",
            "",
            "```dart",
            "import 'package:flutter/material.dart';",
            "import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';",
            "",
            "void main() {",
            "  runApp(const MyApp());",
            "}",
            "",
            "class MyApp extends StatelessWidget {",
            "  const MyApp({super.key});",
            "",
            "  @override",
            "  Widget build(BuildContext context) {",
            "    return MaterialApp(",
            "      title: 'MDS Flutter App',",
            "      theme: MdsThemeData.light(),",
            "      darkTheme: MdsThemeData.dark(),",
            "      home: const Scaffold(",
            "        body: Center(",
            "          child: Text('Hello Cairo MDS!'),",
            "        ),",
            "      ),",
            "    );",
            "  }",
            "}",
            "```",
            "",
        ]
        return normalize_newlines("\n".join(lines))

    def generate_license(self) -> str:
        """Generates LICENSE."""
        lines = [
            "MIT License",
            "",
            "Copyright (c) 2026 Mohamed Khalid. Master Design System (MDS).",
            "",
            "Permission is hereby granted, free of charge, to any person obtaining a copy",
            'of this software and associated documentation files (the "Software"), to deal',
            "in the Software without restriction, including without limitation the rights",
            "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell",
            "copies of the Software, and to permit persons to whom the Software is",
            "furnished to do so, subject to the following conditions:",
            "",
            "The above copyright notice and this permission notice shall be included in all",
            "copies or substantial portions of the Software.",
            "",
            'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR',
            "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,",
            "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE",
            "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER",
            "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,",
            "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE",
            "SOFTWARE.",
            "",
        ]
        return normalize_newlines("\n".join(lines))

    def generate_tests_dart(self) -> str:
        """Generates test/mds_flutter_tokens_test.dart."""
        lines = [
            "// GENERATED CODE - DO NOT MODIFY BY HAND",
            "// Master Design System (MDS) — Flutter Token Engine Tests",
            "// Phase 11: Multi-Platform Flutter Token Engine & Package",
            "// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)",
            "",
            "import 'package:flutter/material.dart';",
            "import 'package:flutter_test/flutter_test.dart';",
            "import 'package:google_fonts/google_fonts.dart';",
            "import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';",
            "",
            "void main() {",
            "  TestWidgetsFlutterBinding.ensureInitialized();",
            "",
            "  setUpAll(() {",
            "    GoogleFonts.config.allowRuntimeFetching = false;",
            "  });",
            "",
            "  group('MdsColors & Palettes Tests', () {",
            "    test('Core brand action color matches Royal Sapphire (#2563EB)', () {",
            "      expect(MdsColors.brand600, equals(const Color(0xFF2563EB)));",
            "      expect(MdsColors.actionPrimaryDefaultLight, equals(const Color(0xFF2563EB)));",
            "    });",
            "",
            "    test('Neutral palette extremes match specification', () {",
            "      expect(MdsColors.neutral0, equals(const Color(0xFFFFFFFF)));",
            "      expect(MdsColors.neutral1000, equals(const Color(0xFF000000)));",
            "      expect(MdsColors.neutral900, equals(const Color(0xFF0F172A)));",
            "    });",
            "",
            "    test('Semantic light & dark surfaces are properly stepped', () {",
            "      expect(MdsColors.surfaceCanvasLight, equals(const Color(0xFFF8FAFC)));",
            "      expect(MdsColors.surfaceDefaultLight, equals(const Color(0xFFFFFFFF)));",
            "      expect(MdsColors.surfaceCanvasDark, equals(const Color(0xFF090D16)));",
            "      expect(MdsColors.surfaceDefaultDark, equals(const Color(0xFF0F172A)));",
            "    });",
            "  });",
            "",
            "  group('MdsTypography & Cairo Font Tests', () {",
            "    test('Primary font family is strictly Cairo', () {",
            "      expect(MdsTypography.primaryFontFamily, equals('Cairo'));",
            "    });",
            "",
            "    test('TextTheme contains Cairo font family across all M3 styles', () {",
            "      final textTheme = MdsTypography.createTextTheme();",
            "      const cairoFamily = MdsTypography.primaryFontFamily;",
            "",
            "      expect(textTheme.displayLarge?.fontFamily, equals(cairoFamily));",
            "      expect(textTheme.displayMedium?.fontFamily, equals(cairoFamily));",
            "      expect(textTheme.displaySmall?.fontFamily, equals(cairoFamily));",
            "      expect(textTheme.headlineLarge?.fontFamily, equals(cairoFamily));",
            "      expect(textTheme.headlineMedium?.fontFamily, equals(cairoFamily));",
            "      expect(textTheme.headlineSmall?.fontFamily, equals(cairoFamily));",
            "      expect(textTheme.titleLarge?.fontFamily, equals(cairoFamily));",
            "      expect(textTheme.titleMedium?.fontFamily, equals(cairoFamily));",
            "      expect(textTheme.titleSmall?.fontFamily, equals(cairoFamily));",
            "      expect(textTheme.bodyLarge?.fontFamily, equals(cairoFamily));",
            "      expect(textTheme.bodyMedium?.fontFamily, equals(cairoFamily));",
            "      expect(textTheme.bodySmall?.fontFamily, equals(cairoFamily));",
            "      expect(textTheme.labelLarge?.fontFamily, equals(cairoFamily));",
            "      expect(textTheme.labelMedium?.fontFamily, equals(cairoFamily));",
            "      expect(textTheme.labelSmall?.fontFamily, equals(cairoFamily));",
            "    });",
            "",
            "    test('Font size metrics match specification', () {",
            "      expect(MdsTypography.sizeXs, equals(12.0));",
            "      expect(MdsTypography.sizeSm, equals(14.0));",
            "      expect(MdsTypography.sizeBase, equals(16.0));",
            "      expect(MdsTypography.sizeLg, equals(20.0));",
            "      expect(MdsTypography.sizeXl, equals(24.0));",
            "      expect(MdsTypography.size2xl, equals(30.0));",
            "      expect(MdsTypography.size3xl, equals(36.0));",
            "      expect(MdsTypography.size4xl, equals(48.0));",
            "    });",
            "  });",
            "",
            "  group('MdsSpacing & RTL Directional Tests', () {",
            "    test('4px grid spacing scale values match specification', () {",
            "      expect(MdsSpacing.space0, equals(0.0));",
            "      expect(MdsSpacing.space1, equals(4.0));",
            "      expect(MdsSpacing.space2, equals(8.0));",
            "      expect(MdsSpacing.space3, equals(12.0));",
            "      expect(MdsSpacing.space4, equals(16.0));",
            "      expect(MdsSpacing.space5, equals(20.0));",
            "      expect(MdsSpacing.space6, equals(24.0));",
            "      expect(MdsSpacing.space8, equals(32.0));",
            "      expect(MdsSpacing.space10, equals(40.0));",
            "      expect(MdsSpacing.space12, equals(48.0));",
            "      expect(MdsSpacing.space16, equals(64.0));",
            "    });",
            "",
            "    test('Directional padding helpers are RTL/LTR symmetric without raw left/right', () {",
            "      expect(MdsSpacing.paddingInlineMd.start, equals(16.0));",
            "      expect(MdsSpacing.paddingInlineMd.end, equals(16.0));",
            "      expect(MdsSpacing.paddingBlockMd.top, equals(16.0));",
            "      expect(MdsSpacing.paddingBlockMd.bottom, equals(16.0));",
            "    });",
            "  });",
            "",
            "  group('MdsRadius & Border Tests', () {",
            "    test('Signature Soft Modern radius is 10px', () {",
            "      expect(MdsRadius.md, equals(10.0));",
            "      expect(MdsRadius.borderMd.topLeft.x, equals(10.0));",
            "    });",
            "",
            "    test('Directional radius start and end resolve correctly', () {",
            "      final startOnly = MdsRadius.directionalStartOnly(10.0);",
            "      expect(startOnly.topStart.x, equals(10.0));",
            "      expect(startOnly.bottomStart.x, equals(10.0));",
            "      expect(startOnly.topEnd.x, equals(0.0));",
            "    });",
            "",
            "    test('Border width scale matches specification', () {",
            "      expect(MdsRadius.borderWidthThin, equals(1.0));",
            "      expect(MdsRadius.borderWidthRegular, equals(1.5));",
            "      expect(MdsRadius.borderWidthThick, equals(2.0));",
            "    });",
            "  });",
            "",
            "  group('MdsElevation & Motion Tests', () {",
            "    test('Elevation levels match depths', () {",
            "      expect(MdsElevation.level0, equals(0.0));",
            "      expect(MdsElevation.level1, equals(1.0));",
            "      expect(MdsElevation.level2, equals(3.0));",
            "      expect(MdsElevation.level3, equals(6.0));",
            "    });",
            "",
            "    test('Elevation shadow lists contain multi-layer shadows', () {",
            "      expect(MdsElevation.shadow0, isEmpty);",
            "      expect(MdsElevation.shadow1.length, equals(2));",
            "      expect(MdsElevation.shadow2.length, equals(2));",
            "      expect(MdsElevation.shadow3.length, equals(2));",
            "    });",
            "",
            "    test('Motion durations match specification', () {",
            "      expect(MdsDurations.instant.inMilliseconds, equals(0));",
            "      expect(MdsDurations.fast.inMilliseconds, equals(150));",
            "      expect(MdsDurations.normal.inMilliseconds, equals(250));",
            "      expect(MdsDurations.slow.inMilliseconds, equals(350));",
            "    });",
            "",
            "    test('Curves cubic-bezier matches standard natural easing', () {",
            "      expect(MdsCurves.standard.a, equals(0.2));",
            "      expect(MdsCurves.standard.b, equals(0.0));",
            "      expect(MdsCurves.standard.c, equals(0.0));",
            "      expect(MdsCurves.standard.d, equals(1.0));",
            "    });",
            "  });",
            "",
            "  group('MdsThemeData Material 3 Tests', () {",
            "    test('Light theme creates valid Material 3 ThemeData with Cairo font', () {",
            "      final theme = MdsThemeData.light();",
            "      expect(theme.useMaterial3, isTrue);",
            "      expect(theme.brightness, equals(Brightness.light));",
            "      expect(theme.scaffoldBackgroundColor, equals(MdsColors.surfaceCanvasLight));",
            "      expect(theme.colorScheme.primary, equals(MdsColors.actionPrimaryDefaultLight));",
            "      expect(theme.textTheme.bodyLarge?.fontFamily, equals(MdsTypography.primaryFontFamily));",
            "",
            "      final ext = theme.extension<MdsSemanticColors>();",
            "      expect(ext, isNotNull);",
            "      expect(ext?.actionPrimaryDefault, equals(MdsColors.actionPrimaryDefaultLight));",
            "    });",
            "",
            "    test('Dark theme creates valid Material 3 ThemeData with Cairo font', () {",
            "      final theme = MdsThemeData.dark();",
            "      expect(theme.useMaterial3, isTrue);",
            "      expect(theme.brightness, equals(Brightness.dark));",
            "      expect(theme.scaffoldBackgroundColor, equals(MdsColors.surfaceCanvasDark));",
            "      expect(theme.colorScheme.primary, equals(MdsColors.actionPrimaryDefaultDark));",
            "      expect(theme.textTheme.bodyLarge?.fontFamily, equals(MdsTypography.primaryFontFamily));",
            "",
            "      final ext = theme.extension<MdsSemanticColors>();",
            "      expect(ext, isNotNull);",
            "      expect(ext?.surfaceCanvas, equals(MdsColors.surfaceCanvasDark));",
            "    });",
            "  });",
            "}",
            "",
        ]
        return normalize_newlines("\n".join(lines))

    def generate_all_files(self) -> Dict[str, str]:
        """Generates all files for the package as an in-memory dictionary {relative_path: content}."""
        self.load_tokens()
        return {
            "pubspec.yaml": self.generate_pubspec_yaml(),
            "README.md": self.generate_readme_md(),
            "LICENSE": self.generate_license(),
            "analysis_options.yaml": self.generate_analysis_options_yaml(),
            "lib/mds_flutter_tokens.dart": self.generate_barrel_dart(),
            "lib/src/colors.dart": self.generate_colors_dart(),
            "lib/src/typography.dart": self.generate_typography_dart(),
            "lib/src/spacing.dart": self.generate_spacing_dart(),
            "lib/src/radius.dart": self.generate_radius_dart(),
            "lib/src/elevation.dart": self.generate_elevation_dart(),
            "lib/src/motion.dart": self.generate_motion_dart(),
            "lib/src/theme.dart": self.generate_theme_dart(),
            "test/mds_flutter_tokens_test.dart": self.generate_tests_dart(),
        }

    def write_to_disk(self, output_dir: Path) -> List[Tuple[str, int]]:
        """Writes all generated files to output_dir."""
        files = self.generate_all_files()
        results: List[Tuple[str, int]] = []
        for rel_path, content in files.items():
            dest = output_dir / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            encoded = content.encode("utf-8")
            dest.write_bytes(encoded)
            results.append((rel_path, len(encoded)))
        return results

    def verify_synchronization(self, output_dir: Path) -> Tuple[bool, List[str]]:
        """
        Verifies in-memory generated files against disk.
        Returns (is_synced, diff_messages).
        """
        files = self.generate_all_files()
        diff_messages: List[str] = []

        for rel_path, expected_content in files.items():
            dest = output_dir / rel_path
            if not dest.exists():
                diff_messages.append(f"MISSING FILE: {rel_path} does not exist on disk.")
                continue

            disk_content = normalize_newlines(dest.read_text(encoding="utf-8"))
            expected_normalized = normalize_newlines(expected_content)

            if disk_content != expected_normalized:
                diff = difflib.unified_diff(
                    disk_content.splitlines(keepends=True),
                    expected_normalized.splitlines(keepends=True),
                    fromfile=f"disk/{rel_path}",
                    tofile=f"generated/{rel_path}",
                    n=3,
                )
                diff_messages.append(f"CONTENT MISMATCH in {rel_path}:\n" + "".join(diff))

        is_synced = len(diff_messages) == 0
        return is_synced, diff_messages


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="transpile_flutter",
        description="Master Design System (MDS) Flutter Token Engine Transpiler",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("packages/mds_flutter_tokens"),
        help="Target output directory for the Dart package (default: packages/mds_flutter_tokens)",
    )
    parser.add_argument(
        "--tokens-dir",
        type=Path,
        default=None,
        help="Source directory containing canonical JSON tokens (default: MDS/00-Tokens)",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify synchronization without writing to disk. Exits 0 if in sync, 1 if out of sync.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output summary in JSON format",
    )

    args = parser.parse_args()
    workspace_root = Path.cwd()
    output_dir = (args.output if args.output.is_absolute() else workspace_root / args.output).resolve()
    tokens_dir = (args.tokens_dir if args.tokens_dir and args.tokens_dir.is_absolute() else (workspace_root / args.tokens_dir if args.tokens_dir else None))

    transpiler = FlutterTokenTranspiler(workspace_root=workspace_root, tokens_dir=tokens_dir)

    try:
        if args.verify:
            is_synced, diffs = transpiler.verify_synchronization(output_dir)
            if is_synced:
                if args.json:
                    print(json.dumps({"status": "PASS", "synced": True, "files_checked": 13}))
                else:
                    print("================================================================================")
                    print("  MDS FLUTTER TOKEN TRANSPILER VERIFICATION — PASS (Exit 0)")
                    print("================================================================================")
                    print(f"  Target Package:    {output_dir}")
                    print("  Status:            SYNCHRONIZED (100% in-memory matching disk)")
                    print("  Checked Files:     13")
                    print("================================================================================")
                return 0
            else:
                if args.json:
                    print(json.dumps({"status": "FAIL", "synced": False, "errors": diffs}))
                else:
                    print("================================================================================", file=sys.stderr)
                    print("  MDS FLUTTER TOKEN TRANSPILER VERIFICATION — FAIL (Exit 1)", file=sys.stderr)
                    print("================================================================================", file=sys.stderr)
                    print(f"  Target Package:    {output_dir}", file=sys.stderr)
                    print("  Status:            OUT OF SYNC", file=sys.stderr)
                    for err in diffs:
                        print(f"  - {err}", file=sys.stderr)
                    print("================================================================================", file=sys.stderr)
                return 1
        else:
            written = transpiler.write_to_disk(output_dir)
            if args.json:
                print(json.dumps({"status": "SUCCESS", "files": [p for p, _ in written], "total_files": len(written)}))
            else:
                print("================================================================================")
                print("  MDS FLUTTER TOKEN TRANSPILER — SUCCESS (Exit 0)")
                print("================================================================================")
                print(f"  Source Tokens:     {transpiler.tokens_dir}")
                print(f"  Output Package:    {output_dir}")
                print(f"  Generated Files:   {len(written)}")
                for rel_path, byte_size in written:
                    print(f"    - {rel_path: <38} ({byte_size:,} bytes)")
                print("================================================================================")
            return 0
    except Exception as e:
        sys.stderr.write(f"[ERROR] Transpiler execution failed: {e}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
