// GENERATED CODE - DO NOT MODIFY BY HAND
// Master Design System (MDS) — Flutter Token Engine
// Phase 11: Multi-Platform Flutter Token Engine & Package
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';

/// Master Design System (MDS) Elevation Depths & Shadows.
abstract final class MdsElevation {
  // ---------------------------------------------------------------------------
  // Depth Scalars
  // ---------------------------------------------------------------------------
  static const double level0 = 0.0;
  static const double level1 = 1.0;
  static const double level2 = 3.0;
  static const double level3 = 6.0;

  // ---------------------------------------------------------------------------
  // BoxShadow Lists
  // ---------------------------------------------------------------------------
  static const List<BoxShadow> shadow0 = <BoxShadow>[];
  static const List<BoxShadow> shadow1 = <BoxShadow>[
    BoxShadow(
      offset: Offset(0.0, 1.0),
      blurRadius: 3.0,
      spreadRadius: 0.0,
      color: Color(0x0F0F172A),
    ),
    BoxShadow(
      offset: Offset(0.0, 1.0),
      blurRadius: 2.0,
      spreadRadius: -1.0,
      color: Color(0x0A0F172A),
    ),
  ];
  static const List<BoxShadow> shadow2 = <BoxShadow>[
    BoxShadow(
      offset: Offset(0.0, 4.0),
      blurRadius: 6.0,
      spreadRadius: -1.0,
      color: Color(0x140F172A),
    ),
    BoxShadow(
      offset: Offset(0.0, 2.0),
      blurRadius: 4.0,
      spreadRadius: -2.0,
      color: Color(0x0A0F172A),
    ),
  ];
  static const List<BoxShadow> shadow3 = <BoxShadow>[
    BoxShadow(
      offset: Offset(0.0, 12.0),
      blurRadius: 16.0,
      spreadRadius: -4.0,
      color: Color(0x1F0F172A),
    ),
    BoxShadow(
      offset: Offset(0.0, 4.0),
      blurRadius: 6.0,
      spreadRadius: -2.0,
      color: Color(0x0D0F172A),
    ),
  ];

  /// Resolves BoxShadow list by elevation level index (0..3).
  static List<BoxShadow> getShadow(int level) => switch (level) {
    1 => shadow1,
    2 => shadow2,
    3 => shadow3,
    _ => shadow0,
  };
}
