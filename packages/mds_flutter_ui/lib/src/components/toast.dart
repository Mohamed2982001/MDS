// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Semantic variants for [MdsToast].
enum MdsToastVariant {
  info,
  success,
  warning,
  danger,
  neutral,
}

/// Standard Master Design System floating toast notification banner.
class MdsToast {
  /// Presents a floating toast snackbar.
  static ScaffoldFeatureController<SnackBar, SnackBarClosedReason> show({
    required BuildContext context,
    required String message,
    String? title,
    MdsToastVariant variant = MdsToastVariant.neutral,
    Duration duration = const Duration(seconds: 4),
    SnackBarAction? action,
  }) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    final (Color bg, Color fg, IconData iconData) = switch (variant) {
      MdsToastVariant.info => (mds.feedbackInfo, MdsColors.neutral0, Icons.info_outline),
      MdsToastVariant.success => (mds.feedbackSuccess, MdsColors.neutral0, Icons.check_circle_outline),
      MdsToastVariant.warning => (mds.feedbackWarning, MdsColors.neutral0, Icons.warning_amber_rounded),
      MdsToastVariant.danger => (mds.feedbackDanger, MdsColors.neutral0, Icons.error_outline),
      MdsToastVariant.neutral => (isDark ? MdsColors.neutral800 : MdsColors.neutral900, MdsColors.neutral0, Icons.notifications_none),
    };

    final textTheme = theme.textTheme;

    final snackBar = SnackBar(
      elevation: MdsElevation.level2,
      behavior: SnackBarBehavior.floating,
      backgroundColor: bg,
      shape: const RoundedRectangleBorder(borderRadius: MdsRadius.borderMd),
      margin: const EdgeInsetsDirectional.all(16.0),
      duration: duration,
      action: action,
      content: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Icon(iconData, color: fg, size: 20),
          const SizedBox(width: MdsSpacing.inlineSm),
          Expanded(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (title != null) ...[
                  Text(
                    title,
                    style: textTheme.titleSmall?.copyWith(
                      color: fg,
                      fontWeight: FontWeight.w700,
                    ),
                    softWrap: true,
                  ),
                  const SizedBox(height: 2.0),
                ],
                Text(
                  message,
                  style: textTheme.bodyMedium?.copyWith(
                    color: fg,
                  ),
                  softWrap: true,
                ),
              ],
            ),
          ),
        ],
      ),
    );

    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    return ScaffoldMessenger.of(context).showSnackBar(snackBar);
  }

  /// Convenience helper for success toasts.
  static void showSuccess(BuildContext context, String message, {String? title}) {
    show(context: context, message: message, title: title, variant: MdsToastVariant.success);
  }

  /// Convenience helper for error toasts.
  static void showError(BuildContext context, String message, {String? title}) {
    show(context: context, message: message, title: title, variant: MdsToastVariant.danger);
  }

  /// Convenience helper for warning toasts.
  static void showWarning(BuildContext context, String message, {String? title}) {
    show(context: context, message: message, title: title, variant: MdsToastVariant.warning);
  }

  /// Convenience helper for info toasts.
  static void showInfo(BuildContext context, String message, {String? title}) {
    show(context: context, message: message, title: title, variant: MdsToastVariant.info);
  }
}
