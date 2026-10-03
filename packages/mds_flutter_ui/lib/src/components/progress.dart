// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Standard Master Design System linear progress indicator.
class MdsLinearProgress extends StatelessWidget {
  const MdsLinearProgress({
    super.key,
    this.value,
    this.color,
    this.backgroundColor,
    this.height = 6.0,
    this.borderRadius,
    this.showPercentage = false,
    this.label,
  });

  /// Progress value between 0.0 and 1.0. If null, displays indeterminate animation.
  final double? value;

  /// Active fill color of the progress bar.
  final Color? color;

  /// Background track color.
  final Color? backgroundColor;

  /// Bar height thickness.
  final double height;

  /// Border radius for the track and indicator bar.
  final BorderRadiusGeometry? borderRadius;

  /// Whether to render percentage text above the bar.
  final bool showPercentage;

  /// Optional descriptive label text displayed above the bar.
  final String? label;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    final activeColor = color ?? mds.actionPrimaryDefault;
    final trackColor = backgroundColor ??
        (isDark ? MdsColors.neutral800 : MdsColors.neutral200);
    final effectiveRadius = borderRadius ?? BorderRadius.all(Radius.circular(height / 2));

    final clampedValue = value?.clamp(0.0, 1.0);

    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        if (label != null || (showPercentage && clampedValue != null)) ...[
          Padding(
            padding: const EdgeInsetsDirectional.only(bottom: 6.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                if (label != null)
                  Expanded(
                    child: Text(
                      label!,
                      softWrap: true,
                      style: theme.textTheme.labelMedium?.copyWith(
                        color: mds.textPrimary,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  )
                else
                  const Spacer(),
                if (showPercentage && clampedValue != null)
                  Text(
                    '${(clampedValue * 100).round()}%',
                    style: theme.textTheme.labelMedium?.copyWith(
                      color: mds.textSecondary,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
              ],
            ),
          ),
        ],
        ClipRRect(
          borderRadius: effectiveRadius,
          child: Container(
            height: height,
            decoration: BoxDecoration(
              color: trackColor,
              borderRadius: effectiveRadius,
            ),
            child: clampedValue != null
                ? LayoutBuilder(
                    builder: (context, constraints) {
                      return TweenAnimationBuilder<double>(
                        duration: MdsDurations.normal,
                        curve: MdsCurves.standard,
                        tween: Tween<double>(begin: 0.0, end: clampedValue),
                        builder: (context, animValue, _) {
                          return Align(
                            alignment: AlignmentDirectional.centerStart,
                            child: Container(
                              width: constraints.maxWidth * animValue,
                              height: height,
                              decoration: BoxDecoration(
                                color: activeColor,
                                borderRadius: effectiveRadius,
                              ),
                            ),
                          );
                        },
                      );
                    },
                  )
                : LinearProgressIndicator(
                    color: activeColor,
                    backgroundColor: trackColor,
                    minHeight: height,
                  ),
          ),
        ),
      ],
    );
  }
}

/// Standard Master Design System circular progress spinner.
class MdsCircularProgress extends StatelessWidget {
  const MdsCircularProgress({
    super.key,
    this.value,
    this.size = 36.0,
    this.strokeWidth = 3.5,
    this.color,
    this.backgroundColor,
    this.showPercentage = false,
  });

  /// Progress value between 0.0 and 1.0. If null, displays indeterminate spinner.
  final double? value;

  /// Diameter size of the circular indicator.
  final double size;

  /// Thickness of the spinner stroke.
  final double strokeWidth;

  /// Active stroke color.
  final Color? color;

  /// Background track stroke color.
  final Color? backgroundColor;

  /// Whether to render percentage text in the center (only when [value] != null).
  final bool showPercentage;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    final activeColor = color ?? mds.actionPrimaryDefault;
    final trackColor = backgroundColor ??
        (isDark ? MdsColors.neutral800 : MdsColors.neutral200);

    final clampedValue = value?.clamp(0.0, 1.0);

    final spinner = SizedBox(
      width: size,
      height: size,
      child: clampedValue != null
          ? TweenAnimationBuilder<double>(
              duration: MdsDurations.normal,
              curve: MdsCurves.standard,
              tween: Tween<double>(begin: 0.0, end: clampedValue),
              builder: (context, animValue, _) {
                return CircularProgressIndicator(
                  value: animValue,
                  strokeWidth: strokeWidth,
                  color: activeColor,
                  backgroundColor: trackColor,
                  strokeCap: StrokeCap.round,
                );
              },
            )
          : CircularProgressIndicator(
              strokeWidth: strokeWidth,
              color: activeColor,
              backgroundColor: trackColor,
              strokeCap: StrokeCap.round,
            ),
    );

    if (showPercentage && clampedValue != null) {
      return Stack(
        alignment: Alignment.center,
        children: [
          spinner,
          Text(
            '${(clampedValue * 100).round()}%',
            style: theme.textTheme.labelSmall?.copyWith(
              fontSize: size * 0.25,
              fontWeight: FontWeight.bold,
              color: mds.textPrimary,
            ),
          ),
        ],
      );
    }

    return spinner;
  }
}

/// Unified entry-point for Master Design System progress indicators.
class MdsProgressIndicator extends StatelessWidget {
  const MdsProgressIndicator.linear({
    super.key,
    this.value,
    this.color,
    this.backgroundColor,
    this.height = 6.0,
    this.borderRadius,
    this.showPercentage = false,
    this.label,
  })  : isCircular = false,
        size = 36.0,
        strokeWidth = 3.5;

  const MdsProgressIndicator.circular({
    super.key,
    this.value,
    this.color,
    this.backgroundColor,
    this.size = 36.0,
    this.strokeWidth = 3.5,
    this.showPercentage = false,
  })  : isCircular = true,
        height = 6.0,
        borderRadius = null,
        label = null;

  final bool isCircular;
  final double? value;
  final Color? color;
  final Color? backgroundColor;
  final double height;
  final double size;
  final double strokeWidth;
  final BorderRadiusGeometry? borderRadius;
  final bool showPercentage;
  final String? label;

  @override
  Widget build(BuildContext context) {
    if (isCircular) {
      return MdsCircularProgress(
        value: value,
        size: size,
        strokeWidth: strokeWidth,
        color: color,
        backgroundColor: backgroundColor,
        showPercentage: showPercentage,
      );
    }
    return MdsLinearProgress(
      value: value,
      color: color,
      backgroundColor: backgroundColor,
      height: height,
      borderRadius: borderRadius,
      showPercentage: showPercentage,
      label: label,
    );
  }
}
