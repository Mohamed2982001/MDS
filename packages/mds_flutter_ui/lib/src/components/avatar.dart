// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Available sizes for [MdsAvatar].
enum MdsAvatarSize {
  xs(24.0, 10.0, 6.0),
  sm(32.0, 12.0, 8.0),
  md(40.0, 14.0, 10.0),
  lg(48.0, 18.0, 12.0),
  xl(64.0, 24.0, 14.0),
  xxl(80.0, 30.0, 16.0);

  const MdsAvatarSize(this.dimension, this.fontSize, this.statusDotSize);

  final double dimension;
  final double fontSize;
  final double statusDotSize;
}

/// Geometric shape for [MdsAvatar].
enum MdsAvatarShape {
  circle,
  rounded,
}

/// Presence status indicator for [MdsAvatar].
enum MdsAvatarStatus {
  none,
  online,
  offline,
  busy,
  away,
}

/// Standard Master Design System avatar component.
///
/// Supports network images, asset images, fallback initials from names,
/// presence status badges, and rounded/circle geometries.
class MdsAvatar extends StatelessWidget {
  const MdsAvatar({
    super.key,
    this.name,
    this.initials,
    this.imageUrl,
    this.image,
    this.size = MdsAvatarSize.md,
    this.shape = MdsAvatarShape.circle,
    this.status = MdsAvatarStatus.none,
    this.backgroundColor,
    this.foregroundColor,
    this.borderRadius,
    this.child,
    this.onTap,
  });

  /// User display name used to compute fallback initials.
  final String? name;

  /// Explicit initials override (e.g. "MK").
  final String? initials;

  /// Optional remote image URL.
  final String? imageUrl;

  /// Optional [ImageProvider] (e.g., [NetworkImage], [AssetImage]).
  final ImageProvider? image;

  /// Size tier of the avatar.
  final MdsAvatarSize size;

  /// Shape of the avatar container.
  final MdsAvatarShape shape;

  /// Real-time presence indicator badge.
  final MdsAvatarStatus status;

  /// Background color for the initials avatar container.
  final Color? backgroundColor;

  /// Text color for initials.
  final Color? foregroundColor;

  /// Custom border radius when shape is [MdsAvatarShape.rounded].
  final BorderRadiusGeometry? borderRadius;

  /// Custom child widget to display inside avatar.
  final Widget? child;

  /// Optional tap callback.
  final VoidCallback? onTap;

  /// Computes uppercase initials from a name (e.g. "Mohamed Khalid" -> "MK").
  static String extractInitials(String? name) {
    if (name == null || name.trim().isEmpty) return '?';
    final parts = name.trim().split(RegExp(r'\s+'));
    if (parts.isEmpty) return '?';
    if (parts.length == 1) {
      final single = parts[0];
      return single.isNotEmpty ? single.characters.first.toUpperCase() : '?';
    }
    final first = parts.first.characters.first.toUpperCase();
    final last = parts.last.characters.first.toUpperCase();
    return '$first$last';
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    final double dim = size.dimension;
    final effectiveBg = backgroundColor ??
        (isDark ? MdsColors.neutral800 : MdsColors.brand100);
    final effectiveFg = foregroundColor ??
        (isDark ? MdsColors.brand200 : MdsColors.brand800);

    final BorderRadiusGeometry effectiveRadius = shape == MdsAvatarShape.circle
        ? BorderRadius.all(Radius.circular(dim / 2))
        : (borderRadius ?? MdsRadius.borderMd);

    ImageProvider? effectiveImageProvider = image;
    if (effectiveImageProvider == null && imageUrl != null && imageUrl!.isNotEmpty) {
      effectiveImageProvider = NetworkImage(imageUrl!);
    }

    Widget content;
    if (child != null) {
      content = child!;
    } else if (effectiveImageProvider != null) {
      content = Image(
        image: effectiveImageProvider,
        width: dim,
        height: dim,
        fit: BoxFit.cover,
        errorBuilder: (context, error, stackTrace) => _buildInitials(theme, effectiveFg),
      );
    } else {
      content = _buildInitials(theme, effectiveFg);
    }

    Widget avatarWidget = Container(
      width: dim,
      height: dim,
      decoration: BoxDecoration(
        color: effectiveBg,
        borderRadius: effectiveRadius,
        border: Border.all(
          color: isDark ? MdsColors.neutral700 : mds.borderDefault,
          width: MdsRadius.borderWidthThin,
        ),
      ),
      child: ClipRRect(
        borderRadius: effectiveRadius,
        child: Center(child: content),
      ),
    );

    if (onTap != null) {
      avatarWidget = GestureDetector(
        onTap: onTap,
        child: avatarWidget,
      );
    }

    if (status == MdsAvatarStatus.none) {
      return avatarWidget;
    }

    final Color statusColor = switch (status) {
      MdsAvatarStatus.online => mds.feedbackSuccess,
      MdsAvatarStatus.busy => mds.feedbackDanger,
      MdsAvatarStatus.away => mds.feedbackWarning,
      MdsAvatarStatus.offline => isDark ? MdsColors.neutral500 : mds.textSecondary,
      MdsAvatarStatus.none => Colors.transparent,
    };

    final double dotSize = size.statusDotSize;
    final Color ringColor = isDark ? MdsColors.neutral900 : MdsColors.neutral0;

    return Stack(
      clipBehavior: Clip.none,
      children: [
        avatarWidget,
        PositionedDirectional(
          bottom: 0,
          end: 0,
          child: Container(
            width: dotSize,
            height: dotSize,
            decoration: BoxDecoration(
              color: statusColor,
              shape: BoxShape.circle,
              border: Border.all(
                color: ringColor,
                width: 2.0,
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildInitials(ThemeData theme, Color fgColor) {
    final text = initials ?? extractInitials(name);
    return Text(
      text,
      textAlign: TextAlign.center,
      style: theme.textTheme.titleMedium?.copyWith(
        fontSize: size.fontSize,
        fontWeight: FontWeight.bold,
        color: fgColor,
        height: 1.0,
      ),
    );
  }
}

/// A stacked overlapping cluster of avatars with an overflow counter.
class MdsAvatarGroup extends StatelessWidget {
  const MdsAvatarGroup({
    super.key,
    required this.avatars,
    this.maxCount = 4,
    this.overlapOffset = 12.0,
    this.size = MdsAvatarSize.md,
  });

  /// List of avatars to display.
  final List<MdsAvatar> avatars;

  /// Maximum number of avatars before showing overflow badge.
  final int maxCount;

  /// Horizontal overlap spacing between avatars.
  final double overlapOffset;

  /// Size tier for the overflow badge.
  final MdsAvatarSize size;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    final visibleCount = avatars.length > maxCount ? maxCount : avatars.length;
    final overflowCount = avatars.length - visibleCount;

    final visibleAvatars = avatars.take(visibleCount).toList();

    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        for (int i = 0; i < visibleAvatars.length; i++)
          Align(
            widthFactor: i == 0 ? 1.0 : (1.0 - (overlapOffset / size.dimension)),
            child: Container(
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                border: Border.all(
                  color: isDark ? MdsColors.neutral900 : MdsColors.neutral0,
                  width: 2.0,
                ),
              ),
              child: visibleAvatars[i],
            ),
          ),
        if (overflowCount > 0)
          Align(
            widthFactor: 1.0 - (overlapOffset / size.dimension),
            child: Container(
              width: size.dimension,
              height: size.dimension,
              decoration: BoxDecoration(
                color: isDark ? MdsColors.neutral800 : MdsColors.neutral200,
                shape: BoxShape.circle,
                border: Border.all(
                  color: isDark ? MdsColors.neutral900 : MdsColors.neutral0,
                  width: 2.0,
                ),
              ),
              child: Center(
                child: Text(
                  '+$overflowCount',
                  style: theme.textTheme.labelMedium?.copyWith(
                    fontSize: size.fontSize * 0.9,
                    fontWeight: FontWeight.bold,
                    color: isDark ? MdsColors.neutral200 : MdsColors.neutral700,
                  ),
                ),
              ),
            ),
          ),
      ],
    );
  }
}
