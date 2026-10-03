// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Standard Master Design System checkbox control supporting tristate selection.
class MdsCheckbox extends StatelessWidget {
  const MdsCheckbox({
    super.key,
    required this.value,
    required this.onChanged,
    this.label,
    this.description,
    this.errorText,
    this.disabled = false,
    this.tristate = false,
  });

  final bool? value;
  final ValueChanged<bool?>? onChanged;
  final String? label;
  final String? description;
  final String? errorText;
  final bool disabled;
  final bool tristate;

  void _handleTap() {
    if (disabled || onChanged == null) return;
    if (tristate) {
      if (value == null) {
        onChanged!(true);
      } else if (value == true) {
        onChanged!(false);
      } else {
        onChanged!(null);
      }
    } else {
      onChanged!(!(value ?? false));
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    final bool isChecked = value == true;
    final bool isIndeterminate = value == null;
    final bool isSelected = isChecked || isIndeterminate;
    final bool hasError = errorText != null && errorText!.isNotEmpty;

    Color boxBg;
    Color boxBorder;
    Color iconColor;

    if (disabled) {
      boxBg = isSelected ? mds.actionDisabledForeground : mds.actionDisabledBackground;
      boxBorder = mds.actionDisabledForeground;
      iconColor = mds.surfaceDefault;
    } else if (hasError) {
      boxBg = isSelected ? mds.feedbackDanger : Colors.transparent;
      boxBorder = mds.feedbackDanger;
      iconColor = MdsColors.neutral0;
    } else if (isSelected) {
      boxBg = mds.actionPrimaryDefault;
      boxBorder = mds.actionPrimaryDefault;
      iconColor = MdsColors.neutral0;
    } else {
      boxBg = Colors.transparent;
      boxBorder = isDark ? MdsColors.neutral600 : mds.borderDefault;
      iconColor = Colors.transparent;
    }

    final boxWidget = AnimatedContainer(
      duration: MdsDurations.fast,
      curve: MdsCurves.standard,
      width: 20.0,
      height: 20.0,
      decoration: BoxDecoration(
        color: boxBg,
        borderRadius: MdsRadius.borderXs,
        border: Border.all(
          color: boxBorder,
          width: isSelected ? 0.0 : MdsRadius.borderWidthRegular,
        ),
      ),
      child: Center(
        child: isIndeterminate
            ? Container(
                width: 10.0,
                height: 2.0,
                decoration: BoxDecoration(
                  color: iconColor,
                  borderRadius: BorderRadius.circular(1.0),
                ),
              )
            : AnimatedOpacity(
                opacity: isChecked ? 1.0 : 0.0,
                duration: MdsDurations.fast,
                child: Icon(
                  Icons.check,
                  size: 15.0,
                  color: iconColor,
                ),
              ),
      ),
    );

    if (label == null && description == null && errorText == null) {
      return GestureDetector(
        onTap: disabled ? null : _handleTap,
        behavior: HitTestBehavior.opaque,
        child: boxWidget,
      );
    }

    final textTheme = theme.textTheme;

    return InkWell(
      onTap: disabled ? null : _handleTap,
      borderRadius: MdsRadius.borderMd,
      child: Padding(
        padding: const EdgeInsetsDirectional.symmetric(vertical: 4.0),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsetsDirectional.only(top: 2.0, end: MdsSpacing.inlineSm),
              child: boxWidget,
            ),
            Flexible(
              fit: FlexFit.loose,
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
                  if (hasError) ...[
                    const SizedBox(height: 2.0),
                    Text(
                      errorText!,
                      style: textTheme.bodySmall?.copyWith(
                        color: mds.feedbackDanger,
                        fontWeight: FontWeight.w500,
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
