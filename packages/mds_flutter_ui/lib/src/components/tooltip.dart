// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Visual style theme for [MdsTooltip].
enum MdsTooltipVariant {
  dark,
  light,
  primary,
}

/// Preferred vertical position of the tooltip relative to child.
enum MdsTooltipPosition {
  top,
  bottom,
}

/// Standard Master Design System styled tooltip widget.
///
/// Features Cairo typography, directional padding, token elevations,
/// soft text wrapping without ellipsis, and mobile touch-friendly trigger modes.
class MdsTooltip extends StatelessWidget {
  const MdsTooltip({
    super.key,
    required this.child,
    required this.message,
    this.variant = MdsTooltipVariant.dark,
    this.position = MdsTooltipPosition.bottom,
    this.waitDuration = const Duration(milliseconds: 300),
    this.showDuration = const Duration(milliseconds: 2000),
    this.triggerMode = TooltipTriggerMode.longPress,
    this.padding,
    this.borderRadius,
    this.maxWidth = 260.0,
    this.enableFeedback = true,
  });

  /// The child widget triggering the tooltip on hover / long-press / tap.
  final Widget child;

  /// Tooltip message text. Soft wraps gracefully across multiple lines.
  final String message;

  /// Stylistic variant (dark, light, primary).
  final MdsTooltipVariant variant;

  /// Preferred position (top or bottom).
  final MdsTooltipPosition position;

  /// Wait delay before showing tooltip on pointer hover.
  final Duration waitDuration;

  /// Duration to stay visible after touch release.
  final Duration showDuration;

  /// Trigger gesture on touch devices (tap or longPress).
  final TooltipTriggerMode triggerMode;

  /// Inner padding around the tooltip message.
  final EdgeInsetsGeometry? padding;

  /// Corner radius of the tooltip bubble.
  final BorderRadiusGeometry? borderRadius;

  /// Maximum container width to enforce clean line breaks.
  final double maxWidth;

  /// Whether to produce haptic feedback on touch trigger.
  final bool enableFeedback;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    Color bgColor;
    Color textColor;
    Border? border;

    switch (variant) {
      case MdsTooltipVariant.dark:
        bgColor = isDark ? MdsColors.neutral800 : MdsColors.neutral900;
        textColor = MdsColors.neutral0;
        border = Border.all(
          color: isDark ? MdsColors.neutral700 : MdsColors.neutral800,
          width: MdsRadius.borderWidthThin,
        );
        break;
      case MdsTooltipVariant.light:
        bgColor = isDark ? MdsColors.neutral900 : MdsColors.neutral0;
        textColor = isDark ? MdsColors.neutral100 : MdsColors.neutral900;
        border = Border.all(
          color: isDark ? MdsColors.neutral700 : mds.borderDefault,
          width: MdsRadius.borderWidthThin,
        );
        break;
      case MdsTooltipVariant.primary:
        bgColor = mds.actionPrimaryDefault;
        textColor = MdsColors.neutral0;
        border = null;
        break;
    }

    final effectiveRadius = borderRadius ?? MdsRadius.borderSm;
    final effectivePadding = padding ??
        const EdgeInsetsDirectional.symmetric(horizontal: 10.0, vertical: 6.0);

    return Tooltip(
      message: message,
      preferBelow: position == MdsTooltipPosition.bottom,
      waitDuration: waitDuration,
      showDuration: showDuration,
      triggerMode: triggerMode,
      enableFeedback: enableFeedback,
      margin: const EdgeInsets.symmetric(horizontal: 16.0),
      padding: effectivePadding,
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: effectiveRadius,
        border: border,
        boxShadow: MdsElevation.shadow2,
      ),
      textStyle: theme.textTheme.bodySmall?.copyWith(
        color: textColor,
        fontWeight: FontWeight.w500,
        height: 1.3,
      ),
      child: child,
    );
  }
}
