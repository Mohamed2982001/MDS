// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Semantic variants for [MdsBadge].
enum MdsBadgeVariant {
  success,
  warning,
  error,
  info,
  neutral,
  brand,
}

/// Stylistic variants for [MdsBadge].
enum MdsBadgeStyle {
  subtle,
  filled,
  outline,
}

/// Standard Master Design System badge and tag indicator widget.
class MdsBadge extends StatelessWidget {
  const MdsBadge({
    super.key,
    required this.label,
    this.variant = MdsBadgeVariant.brand,
    this.style = MdsBadgeStyle.subtle,
    this.icon,
    this.onTap,
    this.onDelete,
    this.isPill = true,
  });

  final String label;
  final MdsBadgeVariant variant;
  final MdsBadgeStyle style;
  final Widget? icon;
  final VoidCallback? onTap;
  final VoidCallback? onDelete;
  final bool isPill;

  (Color bg, Color fg, Color border) _resolveColors(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    final baseColor = switch (variant) {
      MdsBadgeVariant.success => mds.feedbackSuccess,
      MdsBadgeVariant.warning => mds.feedbackWarning,
      MdsBadgeVariant.error => mds.feedbackDanger,
      MdsBadgeVariant.info => mds.feedbackInfo,
      MdsBadgeVariant.neutral => isDark ? MdsColors.neutral400 : MdsColors.neutral600,
      MdsBadgeVariant.brand => mds.actionPrimaryDefault,
    };

    return switch (style) {
      MdsBadgeStyle.filled => (baseColor, MdsColors.neutral0, Colors.transparent),
      MdsBadgeStyle.outline => (
        Colors.transparent,
        baseColor,
        baseColor.withValues(alpha: 0.5),
      ),
      MdsBadgeStyle.subtle => (
        baseColor.withValues(alpha: isDark ? 0.2 : 0.12),
        isDark ? Color.lerp(baseColor, Colors.white, 0.3)! : baseColor,
        Colors.transparent,
      ),
    };
  }

  @override
  Widget build(BuildContext context) {
    final (bg, fg, border) = _resolveColors(context);
    final textTheme = Theme.of(context).textTheme;

    final badgeChild = Row(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        if (icon != null) ...[
          IconTheme(
            data: IconThemeData(color: fg, size: 14),
            child: icon!,
          ),
          const SizedBox(width: MdsSpacing.inlineXs),
        ],
        Text(
          label,
          style: textTheme.labelSmall?.copyWith(
            color: fg,
            fontWeight: FontWeight.w600,
            letterSpacing: 0.2,
          ),
          softWrap: false,
        ),
        if (onDelete != null) ...[
          const SizedBox(width: MdsSpacing.inlineXs),
          GestureDetector(
            onTap: onDelete,
            behavior: HitTestBehavior.opaque,
            child: Icon(Icons.close, size: 14, color: fg),
          ),
        ],
      ],
    );

    Widget badge = Container(
      padding: const EdgeInsetsDirectional.symmetric(
        horizontal: 8.0,
        vertical: 3.0,
      ),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: isPill ? MdsRadius.borderFull : MdsRadius.borderXs,
        border: border != Colors.transparent
            ? Border.all(color: border, width: MdsRadius.borderWidthThin)
            : null,
      ),
      child: badgeChild,
    );

    if (onTap != null) {
      badge = InkWell(
        onTap: onTap,
        borderRadius: isPill ? MdsRadius.borderFull : MdsRadius.borderXs,
        child: badge,
      );
    }

    return Semantics(
      label: label,
      child: badge,
    );
  }
}
