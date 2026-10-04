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
  // Dynamic Font TextStyle Factory
  // ---------------------------------------------------------------------------
  /// Universal dynamic TextStyle factory supporting any Google Font or system font.
  static TextStyle font(
    String fontFamily, {
    double? fontSize,
    FontWeight? fontWeight,
    Color? color,
    double? height,
    double? letterSpacing,
    TextDecoration? decoration,
  }) {
    if (!GoogleFonts.config.allowRuntimeFetching) {
      return TextStyle(
        fontFamily: fontFamily,
        fontFamilyFallback: <String>[fontFamily, primaryFontFamily, 'sans-serif'],
        fontSize: fontSize,
        fontWeight: fontWeight,
        color: color,
        height: height,
        letterSpacing: letterSpacing,
        decoration: decoration,
      );
    }
    try {
      return GoogleFonts.getFont(
        fontFamily,
        fontSize: fontSize,
        fontWeight: fontWeight,
        color: color,
        height: height,
        letterSpacing: letterSpacing,
        decoration: decoration,
      );
    } catch (_) {
      return TextStyle(
        fontFamily: fontFamily,
        fontFamilyFallback: const <String>[primaryFontFamily, 'sans-serif'],
        fontSize: fontSize,
        fontWeight: fontWeight,
        color: color,
        height: height,
        letterSpacing: letterSpacing,
        decoration: decoration,
      );
    }
  }

  /// Backward-compatible Cairo TextStyle Factory.
  static TextStyle cairo({
    double? fontSize,
    FontWeight? fontWeight,
    Color? color,
    double? height,
    double? letterSpacing,
    TextDecoration? decoration,
  }) {
    return font(
      primaryFontFamily,
      fontSize: fontSize,
      fontWeight: fontWeight,
      color: color,
      height: height,
      letterSpacing: letterSpacing,
      decoration: decoration,
    );
  }

  // ---------------------------------------------------------------------------
  // Material 3 Dynamic TextTheme Factory
  // ---------------------------------------------------------------------------
  /// Builds complete Material 3 TextTheme dynamically for any specified font family.
  static TextTheme createTextTheme({
    String fontFamily = primaryFontFamily,
    Color primaryColor = MdsColors.textPrimaryLight,
    Color secondaryColor = MdsColors.textSecondaryLight,
  }) {
    return TextTheme(
      displayLarge: font(fontFamily, fontSize: size4xl, fontWeight: bold, height: lineHeightTight, color: primaryColor, letterSpacing: -0.5),
      displayMedium: font(fontFamily, fontSize: size3xl, fontWeight: bold, height: lineHeightTight, color: primaryColor, letterSpacing: -0.25),
      displaySmall: font(fontFamily, fontSize: size2xl, fontWeight: semibold, height: lineHeightTight, color: primaryColor),
      headlineLarge: font(fontFamily, fontSize: size2xl, fontWeight: semibold, height: lineHeightTight, color: primaryColor),
      headlineMedium: font(fontFamily, fontSize: sizeXl, fontWeight: semibold, height: lineHeightTight, color: primaryColor),
      headlineSmall: font(fontFamily, fontSize: sizeLg, fontWeight: semibold, height: lineHeightNormal, color: primaryColor),
      titleLarge: font(fontFamily, fontSize: sizeLg, fontWeight: semibold, height: lineHeightNormal, color: primaryColor),
      titleMedium: font(fontFamily, fontSize: sizeBase, fontWeight: semibold, height: lineHeightNormal, color: primaryColor, letterSpacing: 0.15),
      titleSmall: font(fontFamily, fontSize: sizeSm, fontWeight: semibold, height: lineHeightNormal, color: primaryColor, letterSpacing: 0.1),
      bodyLarge: font(fontFamily, fontSize: sizeBase, fontWeight: regular, height: lineHeightNormal, color: primaryColor, letterSpacing: 0.5),
      bodyMedium: font(fontFamily, fontSize: sizeSm, fontWeight: regular, height: lineHeightNormal, color: primaryColor, letterSpacing: 0.25),
      bodySmall: font(fontFamily, fontSize: sizeXs, fontWeight: regular, height: lineHeightNormal, color: secondaryColor, letterSpacing: 0.4),
      labelLarge: font(fontFamily, fontSize: sizeSm, fontWeight: medium, height: lineHeightTight, color: primaryColor, letterSpacing: 0.1),
      labelMedium: font(fontFamily, fontSize: sizeXs, fontWeight: medium, height: lineHeightTight, color: secondaryColor, letterSpacing: 0.5),
      labelSmall: font(fontFamily, fontSize: 10.0, fontWeight: medium, height: lineHeightTight, color: secondaryColor, letterSpacing: 0.5),
    );
  }

  // ---------------------------------------------------------------------------
  // Intelligent Font Archetype Recommendations Matrix
  // ---------------------------------------------------------------------------
  /// Recommended font families curated by project archetype/domain.
  static const Map<String, List<String>> fontArchetypes = <String, List<String>>{
    'e_commerce': <String>['Tajawal', 'Readex Pro', 'Almarai'],
    'delivery_services': <String>['Tajawal', 'Readex Pro', 'Cairo'],
    'fintech_luxury': <String>['Alexandria', 'Cairo', 'IBM Plex Sans Arabic'],
    'dashboard_saas': <String>['Inter', 'Rubik', 'Noto Sans Arabic'],
    'social_consumer': <String>['Cairo', 'Tajawal', 'Readex Pro'],
    'editorial_content': <String>['Amiri', 'Changa', 'Cairo'],
  };

  /// Resolves the recommended font family for a given project category.
  static String resolveFontForArchetype(String archetype, {String fallback = primaryFontFamily}) {
    final fonts = fontArchetypes[archetype];
    if (fonts != null && fonts.isNotEmpty) return fonts.first;
    return fallback;
  }
}
