// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Standard Master Design System radio choice selector widget.
class MdsRadio<T> extends StatelessWidget {
  const MdsRadio({
    super.key,
    required this.value,
    required this.groupValue,
    required this.onChanged,
    this.label,
    this.description,
    this.disabled = false,
  });

  final T value;
  final T? groupValue;
  final ValueChanged<T?>? onChanged;
  final String? label;
  final String? description;
  final bool disabled;

  bool get _isSelected => value == groupValue;

  void _handleTap() {
    if (disabled || onChanged == null) return;
    onChanged!(value);
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    Color borderColor;
    Color dotColor;

    if (disabled) {
      borderColor = mds.actionDisabledForeground;
      dotColor = mds.actionDisabledForeground;
    } else if (_isSelected) {
      borderColor = mds.actionPrimaryDefault;
      dotColor = mds.actionPrimaryDefault;
    } else {
      borderColor = isDark ? MdsColors.neutral600 : mds.borderDefault;
      dotColor = Colors.transparent;
    }

    final radioCircle = AnimatedContainer(
      duration: MdsDurations.fast,
      curve: MdsCurves.standard,
      width: 20.0,
      height: 20.0,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        border: Border.all(
          color: borderColor,
          width: _isSelected ? 2.0 : MdsRadius.borderWidthRegular,
        ),
      ),
      child: Center(
        child: AnimatedContainer(
          duration: MdsDurations.fast,
          curve: MdsCurves.standard,
          width: _isSelected ? 10.0 : 0.0,
          height: _isSelected ? 10.0 : 0.0,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: dotColor,
          ),
        ),
      ),
    );

    if (label == null && description == null) {
      return GestureDetector(
        onTap: disabled ? null : _handleTap,
        behavior: HitTestBehavior.opaque,
        child: radioCircle,
      );
    }

    final textTheme = theme.textTheme;

    return InkWell(
      onTap: disabled ? null : _handleTap,
      borderRadius: MdsRadius.borderMd,
      child: Padding(
        padding: const EdgeInsetsDirectional.symmetric(vertical: 4.0),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsetsDirectional.only(top: 2.0, end: MdsSpacing.inlineSm),
              child: radioCircle,
            ),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  if (label != null)
                    Text(
                      label!,
                      style: textTheme.bodyMedium?.copyWith(
                        fontWeight: FontWeight.w500,
                        color: disabled ? mds.actionDisabledForeground : mds.textPrimary,
                      ),
                      softWrap: true,
                    ),
                  if (description != null) ...[
                    const SizedBox(height: 2.0),
                    Text(
                      description!,
                      style: textTheme.bodySmall?.copyWith(
                        color: mds.textSecondary,
                      ),
                      softWrap: true,
                    ),
                  ],
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
