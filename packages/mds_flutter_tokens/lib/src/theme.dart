// GENERATED CODE - DO NOT MODIFY BY HAND
// Master Design System (MDS) — Flutter Token Engine
// Phase 11: Multi-Platform Flutter Token Engine & Package
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'colors.dart';
import 'radius.dart';
import 'spacing.dart';
import 'typography.dart';

/// Production-grade Material 3 ThemeData Factory for Light & Dark modes.
abstract final class MdsThemeData {
  /// Builds complete Material 3 Light ThemeData derived directly from MDS tokens.
  static ThemeData light() {
    final colorScheme = MdsColorScheme.light();
    final textTheme = MdsTypography.createTextTheme(
      primaryColor: MdsColors.textPrimaryLight,
      secondaryColor: MdsColors.textSecondaryLight,
    );

    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      colorScheme: colorScheme,
      textTheme: textTheme,
      fontFamily: MdsTypography.primaryFontFamily,
      scaffoldBackgroundColor: MdsColors.surfaceCanvasLight,
      cardTheme: const CardThemeData(
        elevation: 0,
        color: MdsColors.surfaceDefaultLight,
        margin: EdgeInsets.zero,
        shape: RoundedRectangleBorder(
          borderRadius: MdsRadius.borderMd,
          side: BorderSide(color: MdsColors.borderSubtleLight, width: MdsRadius.borderWidthThin),
        ),
      ),
      appBarTheme: AppBarTheme(
        elevation: 0,
        scrolledUnderElevation: 1,
        backgroundColor: MdsColors.surfaceDefaultLight,
        foregroundColor: MdsColors.textPrimaryLight,
        centerTitle: false,
        titleTextStyle: MdsTypography.cairo(
          fontSize: MdsTypography.sizeLg,
          fontWeight: MdsTypography.semibold,
          color: MdsColors.textPrimaryLight,
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          elevation: 0,
          backgroundColor: MdsColors.actionPrimaryDefaultLight,
          foregroundColor: MdsColors.textInverseLight,
          shape: const RoundedRectangleBorder(borderRadius: MdsRadius.borderMd),
          padding: MdsSpacing.paddingButtonMd,
          textStyle: MdsTypography.cairo(
            fontSize: MdsTypography.sizeSm,
            fontWeight: MdsTypography.medium,
          ),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: MdsColors.actionPrimaryDefaultLight,
          side: const BorderSide(color: MdsColors.borderDefaultLight, width: MdsRadius.borderWidthThin),
          shape: const RoundedRectangleBorder(borderRadius: MdsRadius.borderMd),
          padding: MdsSpacing.paddingButtonMd,
          textStyle: MdsTypography.cairo(
            fontSize: MdsTypography.sizeSm,
            fontWeight: MdsTypography.medium,
          ),
        ),
      ),
      inputDecorationTheme: const InputDecorationTheme(
        filled: true,
        fillColor: MdsColors.surfaceDefaultLight,
        contentPadding: MdsSpacing.paddingInput,
        border: OutlineInputBorder(
          borderRadius: MdsRadius.borderMd,
          borderSide: BorderSide(color: MdsColors.borderDefaultLight, width: MdsRadius.borderWidthThin),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: MdsRadius.borderMd,
          borderSide: BorderSide(color: MdsColors.borderDefaultLight, width: MdsRadius.borderWidthThin),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: MdsRadius.borderMd,
          borderSide: BorderSide(color: MdsColors.focusRingLight, width: MdsRadius.borderWidthThick),
        ),
      ),
      extensions: <ThemeExtension<dynamic>>[
        MdsSemanticColors.light(),
      ],
    );
  }

  /// Builds complete Material 3 Dark ThemeData derived directly from MDS tokens.
  static ThemeData dark() {
    final colorScheme = MdsColorScheme.dark();
    final textTheme = MdsTypography.createTextTheme(
      primaryColor: MdsColors.textPrimaryDark,
      secondaryColor: MdsColors.textSecondaryDark,
    );

    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      colorScheme: colorScheme,
      textTheme: textTheme,
      fontFamily: MdsTypography.primaryFontFamily,
      scaffoldBackgroundColor: MdsColors.surfaceCanvasDark,
      cardTheme: const CardThemeData(
        elevation: 0,
        color: MdsColors.surfaceDefaultDark,
        margin: EdgeInsets.zero,
        shape: RoundedRectangleBorder(
          borderRadius: MdsRadius.borderMd,
          side: BorderSide(color: MdsColors.borderSubtleDark, width: MdsRadius.borderWidthThin),
        ),
      ),
      appBarTheme: AppBarTheme(
        elevation: 0,
        scrolledUnderElevation: 1,
        backgroundColor: MdsColors.surfaceDefaultDark,
        foregroundColor: MdsColors.textPrimaryDark,
        centerTitle: false,
        titleTextStyle: MdsTypography.cairo(
          fontSize: MdsTypography.sizeLg,
          fontWeight: MdsTypography.semibold,
          color: MdsColors.textPrimaryDark,
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          elevation: 0,
          backgroundColor: MdsColors.actionPrimaryDefaultDark,
          foregroundColor: MdsColors.neutral900,
          shape: const RoundedRectangleBorder(borderRadius: MdsRadius.borderMd),
          padding: MdsSpacing.paddingButtonMd,
          textStyle: MdsTypography.cairo(
            fontSize: MdsTypography.sizeSm,
            fontWeight: MdsTypography.medium,
          ),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: MdsColors.actionPrimaryDefaultDark,
          side: const BorderSide(color: MdsColors.borderDefaultDark, width: MdsRadius.borderWidthThin),
          shape: const RoundedRectangleBorder(borderRadius: MdsRadius.borderMd),
          padding: MdsSpacing.paddingButtonMd,
          textStyle: MdsTypography.cairo(
            fontSize: MdsTypography.sizeSm,
            fontWeight: MdsTypography.medium,
          ),
        ),
      ),
      inputDecorationTheme: const InputDecorationTheme(
        filled: true,
        fillColor: MdsColors.surfaceDefaultDark,
        contentPadding: MdsSpacing.paddingInput,
        border: OutlineInputBorder(
          borderRadius: MdsRadius.borderMd,
          borderSide: BorderSide(color: MdsColors.borderDefaultDark, width: MdsRadius.borderWidthThin),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: MdsRadius.borderMd,
          borderSide: BorderSide(color: MdsColors.borderDefaultDark, width: MdsRadius.borderWidthThin),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: MdsRadius.borderMd,
          borderSide: BorderSide(color: MdsColors.focusRingDark, width: MdsRadius.borderWidthThick),
        ),
      ),
      extensions: <ThemeExtension<dynamic>>[
        MdsSemanticColors.dark(),
      ],
    );
  }
}

/// Context convenience extension for accessing MDS tokens.
extension MdsThemeContextExtension on BuildContext {
  ThemeData get theme => Theme.of(this);
  ColorScheme get colorScheme => Theme.of(this).colorScheme;
  TextTheme get textTheme => Theme.of(this).textTheme;
  MdsSemanticColors get mdsColors =>
      Theme.of(this).extension<MdsSemanticColors>() ?? MdsSemanticColors.light();
}
