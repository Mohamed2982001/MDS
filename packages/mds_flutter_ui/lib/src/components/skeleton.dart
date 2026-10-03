// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Shimmer effect wrapper that applies an animated light sweep over its [child].
class MdsShimmer extends StatefulWidget {
  const MdsShimmer({
    super.key,
    required this.child,
    this.baseColor,
    this.highlightColor,
    this.duration = const Duration(milliseconds: 1500),
  });

  /// The child widget or placeholder tree to shimmer.
  final Widget child;

  /// The base background color of the skeleton shape.
  final Color? baseColor;

  /// The traveling shimmer highlight color.
  final Color? highlightColor;

  /// Duration for one complete shimmer sweep cycle.
  final Duration duration;

  @override
  State<MdsShimmer> createState() => _MdsShimmerState();
}

class _MdsShimmerState extends State<MdsShimmer> with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: widget.duration,
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    final effectiveBase = widget.baseColor ??
        (isDark ? MdsColors.neutral800 : MdsColors.neutral200);
    final effectiveHighlight = widget.highlightColor ??
        (isDark ? MdsColors.neutral700 : MdsColors.neutral100);

    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        final progress = _controller.value;
        return ShaderMask(
          blendMode: BlendMode.srcATop,
          shaderCallback: (bounds) {
            return LinearGradient(
              begin: const Alignment(-1.5, -0.3),
              end: const Alignment(1.5, 0.3),
              transform: _SlidingGradientTransform(slidePercent: progress),
              colors: [
                effectiveBase,
                effectiveHighlight,
                effectiveBase,
              ],
              stops: const [0.1, 0.5, 0.9],
            ).createShader(bounds);
          },
          child: child,
        );
      },
      child: widget.child,
    );
  }
}

class _SlidingGradientTransform extends GradientTransform {
  const _SlidingGradientTransform({required this.slidePercent});

  final double slidePercent;

  @override
  Matrix4? transform(Rect bounds, {TextDirection? textDirection}) {
    final translation = bounds.width * (slidePercent * 2.0 - 1.0);
    return Matrix4.translationValues(translation, 0.0, 0.0);
  }
}

/// Standard Master Design System skeleton placeholder component.
///
/// Features factory constructors for text blocks, circle avatars,
/// rounded rectangles, and compound composite cards with smooth shimmer animation.
class MdsSkeleton extends StatelessWidget {
  /// Base rectangular skeleton.
  const MdsSkeleton({
    super.key,
    this.width,
    this.height = 16.0,
    this.borderRadius,
    this.baseColor,
    this.highlightColor,
  })  : shape = BoxShape.rectangle,
        isText = false,
        textLines = 1,
        lineSpacing = 8.0,
        isCard = false;

  /// Circular skeleton (e.g. for avatar placeholders).
  const MdsSkeleton.circle({
    super.key,
    required double size,
    this.baseColor,
    this.highlightColor,
  })  : width = size,
        height = size,
        borderRadius = null,
        shape = BoxShape.circle,
        isText = false,
        textLines = 1,
        lineSpacing = 8.0,
        isCard = false;

  /// Multi-line text block skeleton.
  const MdsSkeleton.text({
    super.key,
    this.width,
    this.height = 14.0,
    this.textLines = 3,
    this.lineSpacing = 8.0,
    this.borderRadius,
    this.baseColor,
    this.highlightColor,
  })  : shape = BoxShape.rectangle,
        isText = true,
        isCard = false;

  /// Complete card skeleton with optional avatar and body text lines.
  const MdsSkeleton.card({
    super.key,
    this.width,
    this.height = 180.0,
    this.borderRadius,
    this.baseColor,
    this.highlightColor,
  })  : shape = BoxShape.rectangle,
        isText = false,
        textLines = 3,
        lineSpacing = 8.0,
        isCard = true;

  final double? width;
  final double height;
  final BorderRadiusGeometry? borderRadius;
  final BoxShape shape;
  final bool isText;
  final int textLines;
  final double lineSpacing;
  final bool isCard;
  final Color? baseColor;
  final Color? highlightColor;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final defaultBase = isDark ? MdsColors.neutral800 : MdsColors.neutral200;

    if (isCard) {
      final effectiveRadius = borderRadius ?? MdsRadius.borderLg;
      return MdsShimmer(
        baseColor: baseColor,
        highlightColor: highlightColor,
        child: Container(
          width: width,
          padding: const EdgeInsetsDirectional.all(16.0),
          decoration: BoxDecoration(
            color: defaultBase,
            borderRadius: effectiveRadius,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    width: 44,
                    height: 44,
                    decoration: BoxDecoration(
                      color: defaultBase,
                      shape: BoxShape.circle,
                    ),
                  ),
                  const SizedBox(width: 12.0),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          width: double.infinity,
                          height: 14,
                          decoration: BoxDecoration(
                            color: defaultBase,
                            borderRadius: MdsRadius.borderXs,
                          ),
                        ),
                        const SizedBox(height: 6.0),
                        Container(
                          width: 100,
                          height: 12,
                          decoration: BoxDecoration(
                            color: defaultBase,
                            borderRadius: MdsRadius.borderXs,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16.0),
              Container(
                width: double.infinity,
                height: 12,
                decoration: BoxDecoration(
                  color: defaultBase,
                  borderRadius: MdsRadius.borderXs,
                ),
              ),
              const SizedBox(height: 8.0),
              Container(
                width: 180,
                height: 12,
                decoration: BoxDecoration(
                  color: defaultBase,
                  borderRadius: MdsRadius.borderXs,
                ),
              ),
            ],
          ),
        ),
      );
    }

    if (isText) {
      final effectiveRadius = borderRadius ?? MdsRadius.borderXs;
      return MdsShimmer(
        baseColor: baseColor,
        highlightColor: highlightColor,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            for (int i = 0; i < textLines; i++) ...[
              if (i > 0) SizedBox(height: lineSpacing),
              Container(
                width: i == textLines - 1 && textLines > 1
                    ? (width != null ? width! * 0.65 : 180.0)
                    : width ?? double.infinity,
                height: height,
                decoration: BoxDecoration(
                  color: defaultBase,
                  borderRadius: effectiveRadius,
                ),
              ),
            ],
          ],
        ),
      );
    }

    final effectiveRadius = shape == BoxShape.circle
        ? null
        : (borderRadius ?? MdsRadius.borderSm);

    return MdsShimmer(
      baseColor: baseColor,
      highlightColor: highlightColor,
      child: Container(
        width: width,
        height: height,
        decoration: BoxDecoration(
          color: defaultBase,
          shape: shape,
          borderRadius: effectiveRadius,
        ),
      ),
    );
  }
}
