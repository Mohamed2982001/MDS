// GENERATED CODE - DO NOT MODIFY BY HAND
// Master Design System (MDS) — Flutter Token Engine
// Phase 11: Multi-Platform Flutter Token Engine & Package
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';

/// Master Design System (MDS) Corner Radii & Border Widths.
/// Signature 10px Soft Modern radius with directional helpers.
abstract final class MdsRadius {
  // ---------------------------------------------------------------------------
  // Radius Scalars
  // ---------------------------------------------------------------------------
  static const double none = 0.0;
  static const double xs = 4.0;
  static const double sm = 6.0;
  static const double md = 10.0;
  static const double lg = 14.0;
  static const double xl = 20.0;
  static const double full = 9999.0;

  // ---------------------------------------------------------------------------
  // Border Widths
  // ---------------------------------------------------------------------------
  static const double borderWidthThin = 1.0;
  static const double borderWidthRegular = 1.5;
  static const double borderWidthThick = 2.0;

  // ---------------------------------------------------------------------------
  // BorderRadius Helpers
  // ---------------------------------------------------------------------------
  static const BorderRadius borderNone = BorderRadius.zero;
  static const BorderRadius borderXs = BorderRadius.all(Radius.circular(xs));
  static const BorderRadius borderSm = BorderRadius.all(Radius.circular(sm));
  static const BorderRadius borderMd = BorderRadius.all(Radius.circular(md));
  static const BorderRadius borderLg = BorderRadius.all(Radius.circular(lg));
  static const BorderRadius borderXl = BorderRadius.all(Radius.circular(xl));
  static const BorderRadius borderFull = BorderRadius.all(Radius.circular(full));

  // ---------------------------------------------------------------------------
  // Directional BorderRadius (RTL / LTR Bi-directional Safe)
  // ---------------------------------------------------------------------------
  static const BorderRadiusDirectional directionalNone = BorderRadiusDirectional.zero;
  static const BorderRadiusDirectional directionalXs = BorderRadiusDirectional.all(Radius.circular(xs));
  static const BorderRadiusDirectional directionalSm = BorderRadiusDirectional.all(Radius.circular(sm));
  static const BorderRadiusDirectional directionalMd = BorderRadiusDirectional.all(Radius.circular(md));
  static const BorderRadiusDirectional directionalLg = BorderRadiusDirectional.all(Radius.circular(lg));
  static const BorderRadiusDirectional directionalXl = BorderRadiusDirectional.all(Radius.circular(xl));
  static const BorderRadiusDirectional directionalFull = BorderRadiusDirectional.all(Radius.circular(full));

  /// Directional start radius helper (Leading corners in RTL/LTR).
  static BorderRadiusDirectional directionalStartOnly([double radius = md]) =>
      BorderRadiusDirectional.horizontal(start: Radius.circular(radius));

  /// Directional end radius helper (Trailing corners in RTL/LTR).
  static BorderRadiusDirectional directionalEndOnly([double radius = md]) =>
      BorderRadiusDirectional.horizontal(end: Radius.circular(radius));

  /// Directional top radius helper.
  static BorderRadiusDirectional directionalTopOnly([double radius = md]) =>
      BorderRadiusDirectional.vertical(top: Radius.circular(radius));

  /// Directional bottom radius helper.
  static BorderRadiusDirectional directionalBottomOnly([double radius = md]) =>
      BorderRadiusDirectional.vertical(bottom: Radius.circular(radius));
}
