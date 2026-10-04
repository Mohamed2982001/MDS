// GENERATED CODE - DO NOT MODIFY BY HAND
// Master Design System (MDS) — Flutter Token Engine Tests
// Phase 11: Multi-Platform Flutter Token Engine & Package
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUpAll(() {
    GoogleFonts.config.allowRuntimeFetching = false;
  });

  group('MdsColors & Palettes Tests', () {
    test('Core brand action color matches Royal Sapphire (#2563EB)', () {
      expect(MdsColors.brand600, equals(const Color(0xFF2563EB)));
      expect(MdsColors.actionPrimaryDefaultLight, equals(const Color(0xFF2563EB)));
    });

    test('Neutral palette extremes match specification', () {
      expect(MdsColors.neutral0, equals(const Color(0xFFFFFFFF)));
      expect(MdsColors.neutral1000, equals(const Color(0xFF000000)));
      expect(MdsColors.neutral900, equals(const Color(0xFF0F172A)));
    });

    test('Semantic light & dark surfaces are properly stepped', () {
      expect(MdsColors.surfaceCanvasLight, equals(const Color(0xFFF8FAFC)));
      expect(MdsColors.surfaceDefaultLight, equals(const Color(0xFFFFFFFF)));
      expect(MdsColors.surfaceCanvasDark, equals(const Color(0xFF090D16)));
      expect(MdsColors.surfaceDefaultDark, equals(const Color(0xFF0F172A)));
    });
  });

  group('MdsTypography & Cairo Font Tests', () {
    test('Primary font family is strictly Cairo', () {
      expect(MdsTypography.primaryFontFamily, equals('Cairo'));
    });

    test('TextTheme contains Cairo font family across all M3 styles', () {
      final textTheme = MdsTypography.createTextTheme();
      const cairoFamily = MdsTypography.primaryFontFamily;

      expect(textTheme.displayLarge?.fontFamily, equals(cairoFamily));
      expect(textTheme.displayMedium?.fontFamily, equals(cairoFamily));
      expect(textTheme.displaySmall?.fontFamily, equals(cairoFamily));
      expect(textTheme.headlineLarge?.fontFamily, equals(cairoFamily));
      expect(textTheme.headlineMedium?.fontFamily, equals(cairoFamily));
      expect(textTheme.headlineSmall?.fontFamily, equals(cairoFamily));
      expect(textTheme.titleLarge?.fontFamily, equals(cairoFamily));
      expect(textTheme.titleMedium?.fontFamily, equals(cairoFamily));
      expect(textTheme.titleSmall?.fontFamily, equals(cairoFamily));
      expect(textTheme.bodyLarge?.fontFamily, equals(cairoFamily));
      expect(textTheme.bodyMedium?.fontFamily, equals(cairoFamily));
      expect(textTheme.bodySmall?.fontFamily, equals(cairoFamily));
      expect(textTheme.labelLarge?.fontFamily, equals(cairoFamily));
      expect(textTheme.labelMedium?.fontFamily, equals(cairoFamily));
      expect(textTheme.labelSmall?.fontFamily, equals(cairoFamily));
    });

    test('Font size metrics match specification', () {
      expect(MdsTypography.sizeXs, equals(12.0));
      expect(MdsTypography.sizeSm, equals(14.0));
      expect(MdsTypography.sizeBase, equals(16.0));
      expect(MdsTypography.sizeLg, equals(20.0));
      expect(MdsTypography.sizeXl, equals(24.0));
      expect(MdsTypography.size2xl, equals(30.0));
      expect(MdsTypography.size3xl, equals(36.0));
      expect(MdsTypography.size4xl, equals(48.0));
    });
  });

  group('MdsSpacing & RTL Directional Tests', () {
    test('4px grid spacing scale values match specification', () {
      expect(MdsSpacing.space0, equals(0.0));
      expect(MdsSpacing.space1, equals(4.0));
      expect(MdsSpacing.space2, equals(8.0));
      expect(MdsSpacing.space3, equals(12.0));
      expect(MdsSpacing.space4, equals(16.0));
      expect(MdsSpacing.space5, equals(20.0));
      expect(MdsSpacing.space6, equals(24.0));
      expect(MdsSpacing.space8, equals(32.0));
      expect(MdsSpacing.space10, equals(40.0));
      expect(MdsSpacing.space12, equals(48.0));
      expect(MdsSpacing.space16, equals(64.0));
    });

    test('Directional padding helpers are RTL/LTR symmetric without raw left/right', () {
      expect(MdsSpacing.paddingInlineMd.start, equals(16.0));
      expect(MdsSpacing.paddingInlineMd.end, equals(16.0));
      expect(MdsSpacing.paddingBlockMd.top, equals(16.0));
      expect(MdsSpacing.paddingBlockMd.bottom, equals(16.0));
    });
  });

  group('MdsRadius & Border Tests', () {
    test('Signature Soft Modern radius is 10px', () {
      expect(MdsRadius.md, equals(10.0));
      expect(MdsRadius.borderMd.topLeft.x, equals(10.0));
    });

    test('Directional radius start and end resolve correctly', () {
      final startOnly = MdsRadius.directionalStartOnly(10.0);
      expect(startOnly.topStart.x, equals(10.0));
      expect(startOnly.bottomStart.x, equals(10.0));
      expect(startOnly.topEnd.x, equals(0.0));
    });

    test('Border width scale matches specification', () {
      expect(MdsRadius.borderWidthThin, equals(1.0));
      expect(MdsRadius.borderWidthRegular, equals(1.5));
      expect(MdsRadius.borderWidthThick, equals(2.0));
    });
  });

  group('MdsElevation & Motion Tests', () {
    test('Elevation levels match depths', () {
      expect(MdsElevation.level0, equals(0.0));
      expect(MdsElevation.level1, equals(1.0));
      expect(MdsElevation.level2, equals(3.0));
      expect(MdsElevation.level3, equals(6.0));
    });

    test('Elevation shadow lists contain multi-layer shadows', () {
      expect(MdsElevation.shadow0, isEmpty);
      expect(MdsElevation.shadow1.length, equals(2));
      expect(MdsElevation.shadow2.length, equals(2));
      expect(MdsElevation.shadow3.length, equals(2));
    });

    test('Motion durations match specification', () {
      expect(MdsDurations.instant.inMilliseconds, equals(0));
      expect(MdsDurations.fast.inMilliseconds, equals(150));
      expect(MdsDurations.normal.inMilliseconds, equals(250));
      expect(MdsDurations.slow.inMilliseconds, equals(350));
    });

    test('Curves cubic-bezier matches standard natural easing', () {
      expect(MdsCurves.standard.a, equals(0.2));
      expect(MdsCurves.standard.b, equals(0.0));
      expect(MdsCurves.standard.c, equals(0.0));
      expect(MdsCurves.standard.d, equals(1.0));
    });
  });

  group('MdsThemeData Material 3 Tests', () {
    test('Light theme creates valid Material 3 ThemeData with Cairo font', () {
      final theme = MdsThemeData.light();
      expect(theme.useMaterial3, isTrue);
      expect(theme.brightness, equals(Brightness.light));
      expect(theme.scaffoldBackgroundColor, equals(MdsColors.surfaceCanvasLight));
      expect(theme.colorScheme.primary, equals(MdsColors.actionPrimaryDefaultLight));
      expect(theme.textTheme.bodyLarge?.fontFamily, equals(MdsTypography.primaryFontFamily));

      final ext = theme.extension<MdsSemanticColors>();
      expect(ext, isNotNull);
      expect(ext?.actionPrimaryDefault, equals(MdsColors.actionPrimaryDefaultLight));
    });

    test('Dark theme creates valid Material 3 ThemeData with Cairo font', () {
      final theme = MdsThemeData.dark();
      expect(theme.useMaterial3, isTrue);
      expect(theme.brightness, equals(Brightness.dark));
      expect(theme.scaffoldBackgroundColor, equals(MdsColors.surfaceCanvasDark));
      expect(theme.colorScheme.primary, equals(MdsColors.actionPrimaryDefaultDark));
      expect(theme.textTheme.bodyLarge?.fontFamily, equals(MdsTypography.primaryFontFamily));

      final ext = theme.extension<MdsSemanticColors>();
      expect(ext, isNotNull);
      expect(ext?.surfaceCanvas, equals(MdsColors.surfaceCanvasDark));
    });

    test('ThemeData dynamically supports custom font family', () {
      final customLight = MdsThemeData.light(fontFamily: 'Tajawal');
      expect(customLight.textTheme.bodyLarge?.fontFamily, equals('Tajawal'));
      expect(customLight.appBarTheme.titleTextStyle?.fontFamily, equals('Tajawal'));
    });

    test('Font archetype recommendations return expected families', () {
      expect(MdsTypography.resolveFontForArchetype('e_commerce'), equals('Tajawal'));
      expect(MdsTypography.resolveFontForArchetype('dashboard_saas'), equals('Inter'));
      expect(MdsTypography.resolveFontForArchetype('unknown'), equals('Cairo'));
    });
  });
}
