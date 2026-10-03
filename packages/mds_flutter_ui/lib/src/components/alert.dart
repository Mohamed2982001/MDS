// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Semantic variants for [MdsAlert].
enum MdsAlertVariant {
  info,
  success,
  warning,
  danger,
}

/// Standard Master Design System banner alert widget with dismiss animation.
class MdsAlert extends StatefulWidget {
  const MdsAlert({
    super.key,
    required this.message,
    this.title,
    this.variant = MdsAlertVariant.info,
    this.icon,
    this.action,
    this.onDismiss,
    this.dismissible = false,
  });

  final String message;
  final String? title;
  final MdsAlertVariant variant;
  final Widget? icon;
  final Widget? action;
  final VoidCallback? onDismiss;
  final bool dismissible;

  @override
  State<MdsAlert> createState() => _MdsAlertState();
}

class _MdsAlertState extends State<MdsAlert> {
  bool _isVisible = true;

  (Color bg, Color border, Color accent, IconData defaultIcon) _resolveTheme(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    return switch (widget.variant) {
      MdsAlertVariant.info => (
        mds.feedbackInfo.withValues(alpha: isDark ? 0.15 : 0.08),
        mds.feedbackInfo.withValues(alpha: isDark ? 0.4 : 0.25),
        mds.feedbackInfo,
        Icons.info_outline,
      ),
      MdsAlertVariant.success => (
        mds.feedbackSuccess.withValues(alpha: isDark ? 0.15 : 0.08),
        mds.feedbackSuccess.withValues(alpha: isDark ? 0.4 : 0.25),
        mds.feedbackSuccess,
        Icons.check_circle_outline,
      ),
      MdsAlertVariant.warning => (
        mds.feedbackWarning.withValues(alpha: isDark ? 0.15 : 0.08),
        mds.feedbackWarning.withValues(alpha: isDark ? 0.4 : 0.25),
        mds.feedbackWarning,
        Icons.warning_amber_rounded,
      ),
      MdsAlertVariant.danger => (
        mds.feedbackDanger.withValues(alpha: isDark ? 0.15 : 0.08),
        mds.feedbackDanger.withValues(alpha: isDark ? 0.4 : 0.25),
        mds.feedbackDanger,
        Icons.error_outline,
      ),
    };
  }

  void _dismiss() {
    setState(() => _isVisible = false);
    widget.onDismiss?.call();
  }

  @override
  Widget build(BuildContext context) {
    if (!_isVisible) {
      return const SizedBox.shrink();
    }

    final (bg, border, accent, defaultIcon) = _resolveTheme(context);
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final textTheme = theme.textTheme;

    return AnimatedSize(
      duration: MdsDurations.fast,
      curve: MdsCurves.standard,
      child: Container(
        padding: const EdgeInsetsDirectional.all(12.0),
        decoration: BoxDecoration(
          color: bg,
          borderRadius: MdsRadius.borderMd,
          border: Border.all(color: border, width: MdsRadius.borderWidthThin),
        ),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsetsDirectional.only(end: MdsSpacing.inlineSm, top: 1.0),
              child: widget.icon ?? Icon(defaultIcon, color: accent, size: 20),
            ),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  if (widget.title != null) ...[
                    Text(
                      widget.title!,
                      style: textTheme.titleSmall?.copyWith(
                        color: isDark ? MdsColors.neutral100 : MdsColors.neutral900,
                        fontWeight: FontWeight.w600,
                      ),
                      softWrap: true,
                    ),
                    const SizedBox(height: 2.0),
                  ],
                  Text(
                    widget.message,
                    style: textTheme.bodyMedium?.copyWith(
                      color: isDark ? MdsColors.neutral300 : MdsColors.neutral700,
                    ),
                    softWrap: true,
                  ),
                  if (widget.action != null) ...[
                    const SizedBox(height: MdsSpacing.inlineXs),
                    widget.action!,
                  ],
                ],
              ),
            ),
            if (widget.dismissible) ...[
              const SizedBox(width: MdsSpacing.inlineXs),
              GestureDetector(
                onTap: _dismiss,
                behavior: HitTestBehavior.opaque,
                child: Padding(
                  padding: const EdgeInsetsDirectional.all(2.0),
                  child: Icon(
                    Icons.close,
                    size: 18,
                    color: isDark ? MdsColors.neutral400 : MdsColors.neutral500,
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
