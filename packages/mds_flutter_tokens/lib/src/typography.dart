// GENERATED CODE - DO NOT MODIFY BY HAND
// Master Design System (MDS) — Flutter Token Engine
// Phase 11: Multi-Platform Flutter Token Engine & Package
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'colors.dart';

/// Master Design System (MDS) Typography.
/// Strictly Cairo font family with Arabic (RTL) & English (LTR) metrics.
abstract final class MdsTypography {
  /// Primary multilingual font family (strictly Cairo).
  static const String primaryFontFamily = 'Cairo';

  /// Monospace font family.
  static const String monoFontFamily = 'JetBrains Mono';

  // ---------------------------------------------------------------------------
  // Font Weights
  // ---------------------------------------------------------------------------
  static const FontWeight regular = FontWeight.w400;
  static const FontWeight medium = FontWeight.w500;
  static const FontWeight semibold = FontWeight.w600;
  static const FontWeight bold = FontWeight.w700;

  // ---------------------------------------------------------------------------
  // Font Sizes
  // ---------------------------------------------------------------------------
  static const double sizeXs = 12.0;
  static const double sizeSm = 14.0;
  static const double sizeBase = 16.0;
  static const double sizeLg = 20.0;
  static const double sizeXl = 24.0;
  static const double size2xl = 30.0;
  static const double size3xl = 36.0;
  static const double size4xl = 48.0;

  // ---------------------------------------------------------------------------
  // Line Heights
  // ---------------------------------------------------------------------------
  static const double lineHeightTight = 1.25;
  static const double lineHeightNormal = 1.5;
  static const double lineHeightRelaxed = 1.75;

  // ---------------------------------------------------------------------------
  // Cairo TextStyle Factory
  // ---------------------------------------------------------------------------
  static TextStyle cairo({
    double? fontSize,
    FontWeight? fontWeight,
    Color? color,
    double? height,
    double? letterSpacing,
    TextDecoration? decoration,
  }) {
    if (!GoogleFonts.config.allowRuntimeFetching) {
      return TextStyle(
        fontFamily: primaryFontFamily,
        fontFamilyFallback: const <String>[primaryFontFamily, 'sans-serif'],
        fontSize: fontSize,
        fontWeight: fontWeight,
        color: color,
        height: height,
        letterSpacing: letterSpacing,
        decoration: decoration,
      );
    }
    return GoogleFonts.cairo(
      fontSize: fontSize,
      fontWeight: fontWeight,
      color: color,
      height: height,
      letterSpacing: letterSpacing,
      decoration: decoration,
    );
  }

  // ---------------------------------------------------------------------------
  // Material 3 Cairo TextTheme Factory
  // ---------------------------------------------------------------------------
  static TextTheme createTextTheme({
    Color primaryColor = MdsColors.textPrimaryLight,
    Color secondaryColor = MdsColors.textSecondaryLight,
  }) {
    return TextTheme(
      displayLarge: cairo(fontSize: size4xl, fontWeight: bold, height: lineHeightTight, color: primaryColor, letterSpacing: -0.5),
      displayMedium: cairo(fontSize: size3xl, fontWeight: bold, height: lineHeightTight, color: primaryColor, letterSpacing: -0.25),
      displaySmall: cairo(fontSize: size2xl, fontWeight: semibold, height: lineHeightTight, color: primaryColor),
      headlineLarge: cairo(fontSize: size2xl, fontWeight: semibold, height: lineHeightTight, color: primaryColor),
      headlineMedium: cairo(fontSize: sizeXl, fontWeight: semibold, height: lineHeightTight, color: primaryColor),
      headlineSmall: cairo(fontSize: sizeLg, fontWeight: semibold, height: lineHeightNormal, color: primaryColor),
      titleLarge: cairo(fontSize: sizeLg, fontWeight: semibold, height: lineHeightNormal, color: primaryColor),
      titleMedium: cairo(fontSize: sizeBase, fontWeight: semibold, height: lineHeightNormal, color: primaryColor, letterSpacing: 0.15),
      titleSmall: cairo(fontSize: sizeSm, fontWeight: semibold, height: lineHeightNormal, color: primaryColor, letterSpacing: 0.1),
      bodyLarge: cairo(fontSize: sizeBase, fontWeight: regular, height: lineHeightNormal, color: primaryColor, letterSpacing: 0.5),
      bodyMedium: cairo(fontSize: sizeSm, fontWeight: regular, height: lineHeightNormal, color: primaryColor, letterSpacing: 0.25),
      bodySmall: cairo(fontSize: sizeXs, fontWeight: regular, height: lineHeightNormal, color: secondaryColor, letterSpacing: 0.4),
      labelLarge: cairo(fontSize: sizeSm, fontWeight: medium, height: lineHeightTight, color: primaryColor, letterSpacing: 0.1),
      labelMedium: cairo(fontSize: sizeXs, fontWeight: medium, height: lineHeightTight, color: secondaryColor, letterSpacing: 0.5),
      labelSmall: cairo(fontSize: 10.0, fontWeight: medium, height: lineHeightTight, color: secondaryColor, letterSpacing: 0.5),
    );
  }
}
