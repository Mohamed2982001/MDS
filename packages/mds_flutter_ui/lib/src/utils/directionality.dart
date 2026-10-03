// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';

/// Directionality and bi-directional layout utilities (Arabic RTL & English LTR).
abstract final class MdsDirectionality {
  /// Checks whether the current context is operating in Right-to-Left (RTL) mode.
  static bool isRtl(BuildContext context) {
    return Directionality.of(context) == TextDirection.rtl;
  }

  /// Resolves the effective TextDirection.
  static TextDirection resolve(BuildContext context, [TextDirection? override]) {
    return override ?? Directionality.of(context);
  }

  /// Returns leading edge alignment (centerLeft for LTR, centerRight for RTL).
  static AlignmentGeometry startAlignment = AlignmentDirectional.centerStart;

  /// Returns trailing edge alignment (centerRight for LTR, centerLeft for RTL).
  static AlignmentGeometry endAlignment = AlignmentDirectional.centerEnd;
}
