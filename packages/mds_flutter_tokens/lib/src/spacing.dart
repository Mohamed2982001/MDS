// GENERATED CODE - DO NOT MODIFY BY HAND
// Master Design System (MDS) — Flutter Token Engine
// Phase 11: Multi-Platform Flutter Token Engine & Package
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';

/// Master Design System (MDS) Spacing Scale & Helpers.
/// Standard 4px grid with directional / RTL-safe padding definitions.
abstract final class MdsSpacing {
  // ---------------------------------------------------------------------------
  // 4px / 8px Grid Scale
  // ---------------------------------------------------------------------------
  /// 0.0px spacing scalar step 0
  static const double space0 = 0.0;
  /// 4.0px spacing scalar step 1
  static const double space1 = 4.0;
  /// 8.0px spacing scalar step 2
  static const double space2 = 8.0;
  /// 12.0px spacing scalar step 3
  static const double space3 = 12.0;
  /// 16.0px spacing scalar step 4
  static const double space4 = 16.0;
  /// 20.0px spacing scalar step 5
  static const double space5 = 20.0;
  /// 24.0px spacing scalar step 6
  static const double space6 = 24.0;
  /// 32.0px spacing scalar step 8
  static const double space8 = 32.0;
  /// 40.0px spacing scalar step 10
  static const double space10 = 40.0;
  /// 48.0px spacing scalar step 12
  static const double space12 = 48.0;
  /// 64.0px spacing scalar step 16
  static const double space16 = 64.0;

  // ---------------------------------------------------------------------------
  // Semantic Spacing Aliases
  // ---------------------------------------------------------------------------
  static const double inlineXs = 4.0;
  static const double inlineSm = 8.0;
  static const double inlineMd = 16.0;
  static const double inlineLg = 24.0;

  static const double blockXs = 4.0;
  static const double blockSm = 8.0;
  static const double blockMd = 16.0;
  static const double blockLg = 32.0;

  // ---------------------------------------------------------------------------
  // Directional EdgeInsets (Arabic RTL & English LTR Safe)
  // ---------------------------------------------------------------------------
  static const EdgeInsetsDirectional paddingInlineXs = EdgeInsetsDirectional.symmetric(horizontal: inlineXs);
  static const EdgeInsetsDirectional paddingInlineSm = EdgeInsetsDirectional.symmetric(horizontal: inlineSm);
  static const EdgeInsetsDirectional paddingInlineMd = EdgeInsetsDirectional.symmetric(horizontal: inlineMd);
  static const EdgeInsetsDirectional paddingInlineLg = EdgeInsetsDirectional.symmetric(horizontal: inlineLg);

  static const EdgeInsetsDirectional paddingBlockXs = EdgeInsetsDirectional.symmetric(vertical: blockXs);
  static const EdgeInsetsDirectional paddingBlockSm = EdgeInsetsDirectional.symmetric(vertical: blockSm);
  static const EdgeInsetsDirectional paddingBlockMd = EdgeInsetsDirectional.symmetric(vertical: blockMd);
  static const EdgeInsetsDirectional paddingBlockLg = EdgeInsetsDirectional.symmetric(vertical: blockLg);

  static const EdgeInsetsDirectional paddingCardSm = EdgeInsetsDirectional.all(12.0);
  static const EdgeInsetsDirectional paddingCardMd = EdgeInsetsDirectional.all(16.0);
  static const EdgeInsetsDirectional paddingCardLg = EdgeInsetsDirectional.all(24.0);

  static const EdgeInsetsDirectional paddingButtonSm = EdgeInsetsDirectional.symmetric(horizontal: 12.0, vertical: 6.0);
  static const EdgeInsetsDirectional paddingButtonMd = EdgeInsetsDirectional.symmetric(horizontal: 16.0, vertical: 10.0);
  static const EdgeInsetsDirectional paddingButtonLg = EdgeInsetsDirectional.symmetric(horizontal: 20.0, vertical: 12.0);

  static const EdgeInsetsDirectional paddingInput = EdgeInsetsDirectional.symmetric(horizontal: 12.0, vertical: 10.0);

  // ---------------------------------------------------------------------------
  // SizedBox Gaps
  // ---------------------------------------------------------------------------
  static const SizedBox gapHorizontalXs = SizedBox(width: inlineXs);
  static const SizedBox gapHorizontalSm = SizedBox(width: inlineSm);
  static const SizedBox gapHorizontalMd = SizedBox(width: inlineMd);
  static const SizedBox gapHorizontalLg = SizedBox(width: inlineLg);

  static const SizedBox gapVerticalXs = SizedBox(height: blockXs);
  static const SizedBox gapVerticalSm = SizedBox(height: blockSm);
  static const SizedBox gapVerticalMd = SizedBox(height: blockMd);
  static const SizedBox gapVerticalLg = SizedBox(height: blockLg);
}
