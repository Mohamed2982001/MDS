// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Standard Master Design System modal dialog widget.
class MdsDialog extends StatelessWidget {
  const MdsDialog({
    super.key,
    required this.title,
    required this.content,
    this.icon,
    this.actions,
    this.showCloseButton = true,
    this.maxWidth = 480.0,
  });

  final String title;
  final Widget content;
  final Widget? icon;
  final List<Widget>? actions;
  final bool showCloseButton;
  final double maxWidth;

  /// Convenience static helper to present an [MdsDialog] with standard backdrop & animation.
  static Future<T?> show<T>({
    required BuildContext context,
    required String title,
    required Widget content,
    Widget? icon,
    List<Widget>? actions,
    bool showCloseButton = true,
    bool barrierDismissible = true,
  }) {
    return showGeneralDialog<T>(
      context: context,
      barrierDismissible: barrierDismissible,
      barrierLabel: 'Dismiss Dialog',
      barrierColor: Colors.black54,
      transitionDuration: MdsDurations.normal,
      pageBuilder: (context, anim1, anim2) {
        return MdsDialog(
          title: title,
          content: content,
          icon: icon,
          actions: actions,
          showCloseButton: showCloseButton,
        );
      },
      transitionBuilder: (context, anim1, anim2, child) {
        final curveValue = MdsCurves.enter.transform(anim1.value);
        return Transform.scale(
          scale: 0.92 + (0.08 * curveValue),
          child: Opacity(
            opacity: anim1.value,
            child: child,
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    final textTheme = theme.textTheme;

    return Center(
      child: ConstrainedBox(
        constraints: BoxConstraints(maxWidth: maxWidth),
        child: Material(
          color: mds.surfaceOverlay,
          borderRadius: MdsRadius.borderXl,
          elevation: MdsElevation.level3,
          shadowColor: const Color(0x330F172A),
          child: Padding(
            padding: const EdgeInsetsDirectional.all(24.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Header Row
                Row(
                  children: [
                    if (icon != null) ...[
                      icon!,
                      const SizedBox(width: MdsSpacing.inlineSm),
                    ],
                    Expanded(
                      child: Text(
                        title,
                        style: textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.w700,
                          color: mds.textPrimary,
                        ),
                        softWrap: true,
                      ),
                    ),
                    if (showCloseButton)
                      IconButton(
                        icon: const Icon(Icons.close, size: 20),
                        color: mds.textSecondary,
                        onPressed: () => Navigator.of(context).pop(),
                        padding: EdgeInsets.zero,
                        constraints: const BoxConstraints(),
                      ),
                  ],
                ),
                const SizedBox(height: MdsSpacing.blockSm),
                // Content Body (Scrollable if overflow)
                Flexible(
                  child: SingleChildScrollView(
                    child: DefaultTextStyle(
                      style: textTheme.bodyMedium?.copyWith(
                        color: mds.textSecondary,
                      ) ?? TextStyle(color: mds.textSecondary),
                      child: content,
                    ),
                  ),
                ),
                if (actions != null && actions!.isNotEmpty) ...[
                  const SizedBox(height: MdsSpacing.blockMd),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: actions!
                        .map((a) => Padding(
                              padding: const EdgeInsetsDirectional.only(start: MdsSpacing.inlineSm),
                              child: a,
                            ))
                        .toList(),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}
