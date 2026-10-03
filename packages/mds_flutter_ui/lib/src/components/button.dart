// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';
import '../utils/animations.dart';

/// Available stylistic variants for [MdsButton].
enum MdsButtonVariant {
  primary,
  secondary,
  outline,
  ghost,
  danger,
}

/// Available size scales for [MdsButton].
enum MdsButtonSize {
  sm,
  md,
  lg,
}

/// Standard Master Design System interactive button widget.
class MdsButton extends StatelessWidget {
  const MdsButton({
    super.key,
    required this.onPressed,
    this.text,
    this.child,
    this.variant = MdsButtonVariant.primary,
    this.size = MdsButtonSize.md,
    this.leadingIcon,
    this.trailingIcon,
    this.isLoading = false,
    this.isFullWidth = false,
    this.borderRadius,
    this.padding,
    this.textStyle,
  }) : assert(text != null || child != null, 'Either text or child must be provided');

  final VoidCallback? onPressed;
  final String? text;
  final Widget? child;
  final MdsButtonVariant variant;
  final MdsButtonSize size;
  final Widget? leadingIcon;
  final Widget? trailingIcon;
  final bool isLoading;
  final bool isFullWidth;
  final BorderRadiusGeometry? borderRadius;
  final EdgeInsetsDirectional? padding;
  final TextStyle? textStyle;

  bool get _isEnabled => onPressed != null && !isLoading;

  EdgeInsetsDirectional get _defaultPadding => switch (size) {
    MdsButtonSize.sm => MdsSpacing.paddingButtonSm,
    MdsButtonSize.md => MdsSpacing.paddingButtonMd,
    MdsButtonSize.lg => MdsSpacing.paddingButtonLg,
  };

  double get _fontSize => switch (size) {
    MdsButtonSize.sm => MdsTypography.sizeXs,
    MdsButtonSize.md => MdsTypography.sizeSm,
    MdsButtonSize.lg => MdsTypography.sizeBase,
  };

  double get _iconSize => switch (size) {
    MdsButtonSize.sm => 16.0,
    MdsButtonSize.md => 18.0,
    MdsButtonSize.lg => 20.0,
  };

  (Color bg, Color fg, BorderSide border) _resolveColors(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    if (!_isEnabled && !isLoading) {
      return (
        mds.actionDisabledBackground,
        mds.actionDisabledForeground,
        BorderSide.none,
      );
    }

    return switch (variant) {
      MdsButtonVariant.primary => (
        mds.actionPrimaryDefault,
        MdsColors.neutral0,
        BorderSide.none,
      ),
      MdsButtonVariant.secondary => (
        isDark ? MdsColors.neutral800 : MdsColors.brand50,
        isDark ? MdsColors.brand300 : MdsColors.brand700,
        BorderSide.none,
      ),
      MdsButtonVariant.outline => (
        Colors.transparent,
        isDark ? MdsColors.brand300 : mds.actionPrimaryDefault,
        BorderSide(
          color: isDark ? MdsColors.neutral700 : mds.borderDefault,
          width: MdsRadius.borderWidthThin,
        ),
      ),
      MdsButtonVariant.ghost => (
        Colors.transparent,
        isDark ? MdsColors.neutral100 : mds.actionPrimaryDefault,
        BorderSide.none,
      ),
      MdsButtonVariant.danger => (
        mds.actionDestructiveDefault,
        MdsColors.neutral0,
        BorderSide.none,
      ),
    };
  }

  @override
  Widget build(BuildContext context) {
    final (bg, fg, border) = _resolveColors(context);
    final effectiveRadius = borderRadius ?? MdsRadius.borderMd;
    final effectivePadding = padding ?? _defaultPadding;

    final baseTextStyle = Theme.of(context).textTheme.labelLarge ??
        const TextStyle(fontWeight: FontWeight.w600);
    final resolvedTextStyle = baseTextStyle.copyWith(
      fontSize: textStyle?.fontSize ?? _fontSize,
      fontWeight: textStyle?.fontWeight ?? FontWeight.w600,
      color: textStyle?.color ?? fg,
    );

    Widget content = child ??
        Text(
          text!,
          style: resolvedTextStyle,
          softWrap: true,
          textAlign: TextAlign.center,
        );

    if (isLoading) {
      content = SizedBox(
        height: _iconSize,
        width: _iconSize,
        child: CircularProgressIndicator(
          strokeWidth: 2.0,
          valueColor: AlwaysStoppedAnimation<Color>(fg),
        ),
      );
    } else {
      final List<Widget> children = [];
      if (leadingIcon != null) {
        children.add(IconTheme(
          data: IconThemeData(color: fg, size: _iconSize),
          child: leadingIcon!,
        ));
        children.add(const SizedBox(width: MdsSpacing.inlineSm));
      }
      children.add(Flexible(child: content));
      if (trailingIcon != null) {
        children.add(const SizedBox(width: MdsSpacing.inlineSm));
        children.add(IconTheme(
          data: IconThemeData(color: fg, size: _iconSize),
          child: trailingIcon!,
        ));
      }

      if (children.length > 1) {
        content = Row(
          mainAxisSize: isFullWidth ? MainAxisSize.max : MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: children,
        );
      }
    }

    Widget button = AnimatedContainer(
      duration: MdsDurations.fast,
      curve: MdsCurves.standard,
      padding: effectivePadding,
      decoration: BoxDecoration(
        color: bg,
        borderRadius: effectiveRadius,
        border: border != BorderSide.none ? Border.fromBorderSide(border) : null,
      ),
      child: content,
    );

    if (isFullWidth) {
      button = SizedBox(width: double.infinity, child: Center(child: button));
    }

    return MdsPressEffect(
      onTap: _isEnabled ? onPressed : null,
      enabled: _isEnabled,
      child: Semantics(
        button: true,
        enabled: _isEnabled,
        child: button,
      ),
    );
  }
}
