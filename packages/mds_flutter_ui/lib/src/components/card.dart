// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';
import '../utils/animations.dart';

/// Available styling variants for [MdsCard].
enum MdsCardVariant {
  elevated,
  outlined,
  filled,
}

/// Standard Master Design System container card widget with structured slot layout.
class MdsCard extends StatelessWidget {
  const MdsCard({
    super.key,
    this.child,
    this.title,
    this.subtitle,
    this.leading,
    this.trailing,
    this.header,
    this.footer,
    this.actions,
    this.variant = MdsCardVariant.elevated,
    this.padding,
    this.margin,
    this.borderRadius,
    this.onTap,
  });

  final Widget? child;
  final Widget? title;
  final Widget? subtitle;
  final Widget? leading;
  final Widget? trailing;
  final Widget? header;
  final Widget? footer;
  final List<Widget>? actions;
  final MdsCardVariant variant;
  final EdgeInsetsDirectional? padding;
  final EdgeInsetsGeometry? margin;
  final BorderRadiusGeometry? borderRadius;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    final effectiveRadius = borderRadius ?? MdsRadius.borderMd;
    final effectivePadding = padding ?? MdsSpacing.paddingCardMd;

    Color bg;
    Border? border;
    List<BoxShadow>? shadows;

    switch (variant) {
      case MdsCardVariant.elevated:
        bg = isDark ? mds.surfaceRaised : mds.surfaceDefault;
        shadows = MdsElevation.shadow1;
        border = Border.all(
          color: isDark ? mds.borderSubtle : mds.borderSubtle.withValues(alpha: 0.5),
          width: MdsRadius.borderWidthThin,
        );
        break;
      case MdsCardVariant.outlined:
        bg = mds.surfaceDefault;
        shadows = null;
        border = Border.all(
          color: mds.borderDefault,
          width: MdsRadius.borderWidthThin,
        );
        break;
      case MdsCardVariant.filled:
        bg = isDark ? mds.surfaceRaised : mds.surfaceRaised;
        shadows = null;
        border = null;
        break;
    }

    final bool hasHeaderSection = header != null || title != null || subtitle != null || leading != null || trailing != null;

    final cardBody = Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      mainAxisSize: MainAxisSize.min,
      children: [
        if (header != null)
          header!
        else if (hasHeaderSection) ...[
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              if (leading != null) ...[
                leading!,
                const SizedBox(width: MdsSpacing.inlineSm),
              ],
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    if (title != null)
                      DefaultTextStyle(
                        style: theme.textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.w600,
                          color: mds.textPrimary,
                        ) ?? TextStyle(color: mds.textPrimary),
                        child: title!,
                      ),
                    if (subtitle != null) ...[
                      const SizedBox(height: 2),
                      DefaultTextStyle(
                        style: theme.textTheme.bodySmall?.copyWith(
                          color: mds.textSecondary,
                        ) ?? TextStyle(color: mds.textSecondary),
                        child: subtitle!,
                      ),
                    ],
                  ],
                ),
              ),
              if (trailing != null) ...[
                const SizedBox(width: MdsSpacing.inlineSm),
                trailing!,
              ],
            ],
          ),
          if (child != null) const SizedBox(height: MdsSpacing.blockSm),
        ],
        if (child != null) child!,
        if (footer != null) ...[
          const SizedBox(height: MdsSpacing.blockSm),
          footer!,
        ],
        if (actions != null && actions!.isNotEmpty) ...[
          const SizedBox(height: MdsSpacing.blockSm),
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
    );

    Widget container = Container(
      margin: margin,
      padding: effectivePadding,
      decoration: BoxDecoration(
        color: bg,
        borderRadius: effectiveRadius,
        border: border,
        boxShadow: shadows,
      ),
      child: cardBody,
    );

    if (onTap != null) {
      container = MdsPressEffect(
        onTap: onTap,
        child: container,
      );
    }

    return container;
  }
}
