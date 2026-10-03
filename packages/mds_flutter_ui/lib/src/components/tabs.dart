// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Available stylistic variants for [MdsTabs].
enum MdsTabVariant {
  underline,
  pill,
}

/// Represents an individual tab within [MdsTabs].
class MdsTabItem {
  const MdsTabItem({
    required this.label,
    this.icon,
    this.badge,
    this.isEnabled = true,
  });

  /// Text title for the tab.
  final String label;

  /// Optional leading icon.
  final Widget? icon;

  /// Optional trailing badge (e.g., [MdsBadge] with count).
  final Widget? badge;

  /// Whether this tab is interactive.
  final bool isEnabled;
}

/// Standard Master Design System responsive tab bar widget.
///
/// Supports underline and pill variants, smooth indicator transitions,
/// icons, notification badges, and scrollable/expanded distribution.
class MdsTabs extends StatelessWidget {
  const MdsTabs({
    super.key,
    required this.tabs,
    required this.selectedIndex,
    required this.onChanged,
    this.variant = MdsTabVariant.underline,
    this.isScrollable = false,
    this.isExpanded = false,
    this.padding,
    this.backgroundColor,
    this.indicatorColor,
  }) : assert(tabs.length > 0, 'tabs must not be empty');

  /// List of tab items.
  final List<MdsTabItem> tabs;

  /// Index of the currently active tab.
  final int selectedIndex;

  /// Callback when a tab is tapped.
  final ValueChanged<int> onChanged;

  /// Visual presentation style (underline or pill).
  final MdsTabVariant variant;

  /// Whether tabs can horizontally scroll when exceeding width.
  final bool isScrollable;

  /// Whether tabs expand equally to fill available width.
  final bool isExpanded;

  /// Outer padding around the tab container.
  final EdgeInsetsDirectional? padding;

  /// Background container color.
  final Color? backgroundColor;

  /// Custom active indicator color.
  final Color? indicatorColor;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    final activeIndicatorColor = indicatorColor ?? mds.actionPrimaryDefault;
    final effectivePadding = padding ?? const EdgeInsetsDirectional.all(4.0);

    Widget buildTab(int index, MdsTabItem item) {
      final isSelected = index == selectedIndex;
      final isEnabled = item.isEnabled;

      Color textColor;
      if (!isEnabled) {
        textColor = mds.actionDisabledForeground;
      } else if (isSelected) {
        textColor = variant == MdsTabVariant.pill
            ? MdsColors.neutral0
            : activeIndicatorColor;
      } else {
        textColor = mds.textSecondary;
      }

      final content = Row(
        mainAxisSize: MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          if (item.icon != null) ...[
            IconTheme(
              data: IconThemeData(
                size: 18,
                color: textColor,
              ),
              child: item.icon!,
            ),
            const SizedBox(width: 8.0),
          ],
          Flexible(
            child: Text(
              item.label,
              softWrap: true,
              style: theme.textTheme.labelLarge?.copyWith(
                color: textColor,
                fontWeight: isSelected ? FontWeight.w600 : FontWeight.w500,
              ),
            ),
          ),
          if (item.badge != null) ...[
            const SizedBox(width: 8.0),
            item.badge!,
          ],
        ],
      );

      if (variant == MdsTabVariant.pill) {
        return InkWell(
          onTap: isEnabled ? () => onChanged(index) : null,
          borderRadius: MdsRadius.borderMd,
          child: AnimatedContainer(
            duration: MdsDurations.normal,
            curve: MdsCurves.standard,
            padding: const EdgeInsetsDirectional.symmetric(horizontal: 16.0, vertical: 8.0),
            decoration: BoxDecoration(
              color: isSelected ? activeIndicatorColor : Colors.transparent,
              borderRadius: MdsRadius.borderMd,
              boxShadow: isSelected ? MdsElevation.shadow1 : null,
            ),
            child: content,
          ),
        );
      }

      // Underline variant
      return InkWell(
        onTap: isEnabled ? () => onChanged(index) : null,
        child: Container(
          padding: const EdgeInsetsDirectional.symmetric(horizontal: 16.0, vertical: 12.0),
          decoration: BoxDecoration(
            border: BorderDirectional(
              bottom: BorderSide(
                color: isSelected ? activeIndicatorColor : Colors.transparent,
                width: 2.5,
              ),
            ),
          ),
          child: content,
        ),
      );
    }

    final tabWidgets = [
      for (int i = 0; i < tabs.length; i++)
        if (isExpanded && !isScrollable)
          Expanded(child: buildTab(i, tabs[i]))
        else
          buildTab(i, tabs[i]),
    ];

    Widget body;
    if (isScrollable) {
      body = SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        physics: const BouncingScrollPhysics(),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: tabWidgets,
        ),
      );
    } else {
      body = Row(
        mainAxisSize: isExpanded ? MainAxisSize.max : MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.start,
        children: tabWidgets,
      );
    }

    if (variant == MdsTabVariant.pill) {
      return Container(
        padding: effectivePadding,
        decoration: BoxDecoration(
          color: backgroundColor ??
              (isDark ? MdsColors.neutral800 : MdsColors.neutral100),
          borderRadius: MdsRadius.borderLg,
        ),
        child: body,
      );
    }

    return Container(
      padding: effectivePadding,
      decoration: BoxDecoration(
        color: backgroundColor ?? Colors.transparent,
        border: BorderDirectional(
          bottom: BorderSide(
            color: isDark ? MdsColors.neutral800 : mds.borderSubtle,
            width: MdsRadius.borderWidthThin,
          ),
        ),
      ),
      child: body,
    );
  }
}
