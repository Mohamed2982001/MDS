// GENERATED CODE - DO NOT MODIFY BY HAND
// Master Design System (MDS) — Flutter Token Engine
// Phase 11: Multi-Platform Flutter Token Engine & Package
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';

/// Master Design System (MDS) Animation Durations.
abstract final class MdsDurations {
  static const Duration instant = Duration(milliseconds: 0);
  static const Duration fast = Duration(milliseconds: 150);
  static const Duration normal = Duration(milliseconds: 250);
  static const Duration slow = Duration(milliseconds: 350);
}

/// Master Design System (MDS) Easing Curves (Cubic-bezier).
abstract final class MdsCurves {
  /// Signature MDS natural curve ([0.2, 0.0, 0.0, 1.0])
  static const Cubic standard = Cubic(0.2, 0.0, 0.0, 1.0);
  /// Curve enter ([0.0, 0.0, 0.2, 1.0])
  static const Cubic enter = Cubic(0.0, 0.0, 0.2, 1.0);
  /// Curve exit ([0.4, 0.0, 1.0, 1.0])
  static const Cubic exit = Cubic(0.4, 0.0, 1.0, 1.0);
}
