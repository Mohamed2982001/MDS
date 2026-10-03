// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Standard Master Design System form input field widget.
class MdsTextField extends StatefulWidget {
  const MdsTextField({
    super.key,
    this.controller,
    this.initialValue,
    this.label,
    this.hintText,
    this.helperText,
    this.errorText,
    this.prefixIcon,
    this.suffixIcon,
    this.obscureText = false,
    this.enabled = true,
    this.readOnly = false,
    this.autofocus = false,
    this.showClearButton = false,
    this.maxLines = 1,
    this.minLines,
    this.keyboardType,
    this.textInputAction,
    this.focusNode,
    this.onChanged,
    this.onSubmitted,
    this.borderRadius,
    this.contentPadding,
  });

  final TextEditingController? controller;
  final String? initialValue;
  final String? label;
  final String? hintText;
  final String? helperText;
  final String? errorText;
  final Widget? prefixIcon;
  final Widget? suffixIcon;
  final bool obscureText;
  final bool enabled;
  final bool readOnly;
  final bool autofocus;
  final bool showClearButton;
  final int? maxLines;
  final int? minLines;
  final TextInputType? keyboardType;
  final TextInputAction? textInputAction;
  final FocusNode? focusNode;
  final ValueChanged<String>? onChanged;
  final ValueChanged<String>? onSubmitted;
  final BorderRadiusGeometry? borderRadius;
  final EdgeInsetsGeometry? contentPadding;

  @override
  State<MdsTextField> createState() => _MdsTextFieldState();
}

class _MdsTextFieldState extends State<MdsTextField> {
  late final TextEditingController _controller;
  late final FocusNode _focusNode;
  bool _isInternalController = false;
  bool _isInternalFocusNode = false;
  bool _isFocused = false;

  @override
  void initState() {
    super.initState();
    if (widget.controller != null) {
      _controller = widget.controller!;
    } else {
      _controller = TextEditingController(text: widget.initialValue);
      _isInternalController = true;
    }

    if (widget.focusNode != null) {
      _focusNode = widget.focusNode!;
    } else {
      _focusNode = FocusNode();
      _isInternalFocusNode = true;
    }

    _focusNode.addListener(_handleFocusChange);
  }

  @override
  void dispose() {
    _focusNode.removeListener(_handleFocusChange);
    if (_isInternalFocusNode) {
      _focusNode.dispose();
    }
    if (_isInternalController) {
      _controller.dispose();
    }
    super.dispose();
  }

  void _handleFocusChange() {
    setState(() {
      _isFocused = _focusNode.hasFocus;
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    final bool hasError = widget.errorText != null && widget.errorText!.isNotEmpty;
    final textTheme = theme.textTheme;

    Color borderColor;
    double borderWidth = MdsRadius.borderWidthThin;

    if (hasError) {
      borderColor = mds.feedbackDanger;
      borderWidth = MdsRadius.borderWidthRegular;
    } else if (_isFocused) {
      borderColor = mds.focusRing;
      borderWidth = MdsRadius.borderWidthThick;
    } else {
      borderColor = isDark ? MdsColors.neutral700 : mds.borderDefault;
    }

    final effectiveRadius = widget.borderRadius ?? MdsRadius.borderMd;
    final effectivePadding = widget.contentPadding ?? MdsSpacing.paddingInput;

    Widget? effectiveSuffix = widget.suffixIcon;
    if (widget.showClearButton && _controller.text.isNotEmpty && widget.enabled) {
      effectiveSuffix = IconButton(
        icon: const Icon(Icons.clear, size: 18),
        onPressed: () {
          _controller.clear();
          widget.onChanged?.call('');
          setState(() {});
        },
      );
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        if (widget.label != null) ...[
          Text(
            widget.label!,
            style: textTheme.labelLarge?.copyWith(
              fontWeight: FontWeight.w600,
              color: hasError
                  ? mds.feedbackDanger
                  : (isDark ? MdsColors.neutral300 : MdsColors.neutral700),
            ),
            softWrap: true,
          ),
          const SizedBox(height: MdsSpacing.inlineXs),
        ],
        AnimatedContainer(
          duration: MdsDurations.fast,
          curve: MdsCurves.standard,
          decoration: BoxDecoration(
            color: widget.enabled ? mds.surfaceDefault : mds.actionDisabledBackground,
            borderRadius: effectiveRadius,
            border: Border.all(color: borderColor, width: borderWidth),
          ),
          child: TextField(
            controller: _controller,
            focusNode: _focusNode,
            obscureText: widget.obscureText,
            enabled: widget.enabled,
            readOnly: widget.readOnly,
            autofocus: widget.autofocus,
            maxLines: widget.maxLines,
            minLines: widget.minLines,
            keyboardType: widget.keyboardType,
            textInputAction: widget.textInputAction,
            onChanged: (val) {
              widget.onChanged?.call(val);
              setState(() {});
            },
            onSubmitted: widget.onSubmitted,
            style: textTheme.bodyLarge?.copyWith(
              color: widget.enabled
                  ? mds.textPrimary
                  : mds.actionDisabledForeground,
            ),
            decoration: InputDecoration(
              isDense: true,
              hintText: widget.hintText,
              hintStyle: textTheme.bodyMedium?.copyWith(
                color: isDark ? MdsColors.neutral500 : MdsColors.neutral400,
              ),
              prefixIcon: widget.prefixIcon != null
                  ? IconTheme(
                      data: IconThemeData(
                        color: _isFocused ? mds.focusRing : mds.textSecondary,
                        size: 20,
                      ),
                      child: widget.prefixIcon!,
                    )
                  : null,
              suffixIcon: effectiveSuffix != null
                  ? IconTheme(
                      data: IconThemeData(
                        color: hasError ? mds.feedbackDanger : mds.textSecondary,
                        size: 20,
                      ),
                      child: effectiveSuffix,
                    )
                  : null,
              contentPadding: effectivePadding,
              border: InputBorder.none,
              enabledBorder: InputBorder.none,
              focusedBorder: InputBorder.none,
              errorBorder: InputBorder.none,
              focusedErrorBorder: InputBorder.none,
              disabledBorder: InputBorder.none,
            ),
          ),
        ),
        if (hasError) ...[
          const SizedBox(height: MdsSpacing.inlineXs),
          Text(
            widget.errorText!,
            style: textTheme.bodySmall?.copyWith(
              color: mds.feedbackDanger,
              fontWeight: FontWeight.w500,
            ),
            softWrap: true,
          ),
        ] else if (widget.helperText != null) ...[
          const SizedBox(height: MdsSpacing.inlineXs),
          Text(
            widget.helperText!,
            style: textTheme.bodySmall?.copyWith(
              color: mds.textSecondary,
            ),
            softWrap: true,
          ),
        ],
      ],
    );
  }
}
