// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Alignment of optional label within [MdsDivider].
enum MdsDividerAlignment {
  start,
  center,
  end,
}

/// Standard Master Design System dividing line widget.
///
/// Supports horizontal and vertical orientations, directional indents,
/// and optional embedded text labels or badges.
class MdsDivider extends StatelessWidget {
  /// Creates a horizontal divider.
  const MdsDivider({
    super.key,
    this.text,
    this.labelWidget,
    this.alignment = MdsDividerAlignment.center,
    this.color,
    this.thickness = 1.0,
    this.indent = 0.0,
    this.endIndent = 0.0,
    this.spacing = 16.0,
  }) : isVertical = false;

  /// Creates a vertical divider.
  const MdsDivider.vertical({
    super.key,
    this.color,
    this.thickness = 1.0,
    this.indent = 0.0,
    this.endIndent = 0.0,
    this.spacing = 16.0,
  })  : isVertical = true,
        text = null,
        labelWidget = null,
        alignment = MdsDividerAlignment.center;

  /// Whether the divider is oriented vertically.
  final bool isVertical;

  /// Optional plain text label rendered inside a horizontal divider.
  final String? text;

  /// Optional custom widget rendered inside a horizontal divider.
  final Widget? labelWidget;

  /// Placement of the label along the divider (start, center, end).
  final MdsDividerAlignment alignment;

  /// Custom divider line color.
  final Color? color;

  /// Stroke thickness of the divider line.
  final double thickness;

  /// Directional leading indent (start).
  final double indent;

  /// Directional trailing indent (end).
  final double endIndent;

  /// Total space allocated for the divider (height for horizontal, width for vertical).
  final double spacing;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    final effectiveColor = color ??
        (isDark ? MdsColors.neutral800 : mds.borderSubtle);

    if (isVertical) {
      return Container(
        width: spacing,
        alignment: Alignment.center,
        child: Padding(
          padding: EdgeInsetsDirectional.only(top: indent, bottom: endIndent),
          child: Container(
            width: thickness,
            color: effectiveColor,
          ),
        ),
      );
    }

    final hasLabel = (text != null && text!.isNotEmpty) || labelWidget != null;

    if (!hasLabel) {
      return Container(
        height: spacing,
        alignment: Alignment.center,
        child: Padding(
          padding: EdgeInsetsDirectional.only(start: indent, end: endIndent),
          child: Container(
            height: thickness,
            color: effectiveColor,
          ),
        ),
      );
    }

    final label = labelWidget ??
        Text(
          text!,
          softWrap: true,
          style: theme.textTheme.labelMedium?.copyWith(
            color: mds.textSecondary,
            fontWeight: FontWeight.w500,
          ),
        );

    final line = Expanded(
      child: Container(
        height: thickness,
        color: effectiveColor,
      ),
    );

    return Container(
      height: spacing,
      alignment: Alignment.center,
      child: Padding(
        padding: EdgeInsetsDirectional.only(start: indent, end: endIndent),
        child: Row(
          children: switch (alignment) {
            MdsDividerAlignment.start => [
                const SizedBox(width: 8.0),
                label,
                const SizedBox(width: 12.0),
                line,
              ],
            MdsDividerAlignment.center => [
                line,
                Padding(
                  padding: const EdgeInsetsDirectional.symmetric(horizontal: 12.0),
                  child: label,
                ),
                line,
              ],
            MdsDividerAlignment.end => [
                line,
                const SizedBox(width: 12.0),
                label,
                const SizedBox(width: 8.0),
              ],
          },
        ),
      ),
    );
  }
}
