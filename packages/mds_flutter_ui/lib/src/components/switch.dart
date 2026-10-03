// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Standard Master Design System toggle switch control with smooth micro-animation.
class MdsSwitch extends StatelessWidget {
  const MdsSwitch({
    super.key,
    required this.value,
    required this.onChanged,
    this.label,
    this.description,
    this.disabled = false,
  });

  final bool value;
  final ValueChanged<bool>? onChanged;
  final String? label;
  final String? description;
  final bool disabled;

  void _handleTap() {
    if (disabled || onChanged == null) return;
    onChanged!(!value);
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    Color trackColor;
    Color thumbColor;

    if (disabled) {
      trackColor = mds.actionDisabledBackground;
      thumbColor = mds.actionDisabledForeground;
    } else if (value) {
      trackColor = mds.actionPrimaryDefault;
      thumbColor = MdsColors.neutral0;
    } else {
      trackColor = isDark ? MdsColors.neutral700 : MdsColors.neutral300;
      thumbColor = MdsColors.neutral0;
    }

    final switchTrack = AnimatedContainer(
      duration: MdsDurations.fast,
      curve: MdsCurves.standard,
      width: 44.0,
      height: 24.0,
      padding: const EdgeInsets.all(2.0),
      decoration: BoxDecoration(
        color: trackColor,
        borderRadius: BorderRadius.circular(12.0),
      ),
      child: AnimatedAlign(
        duration: MdsDurations.fast,
        curve: MdsCurves.standard,
        alignment: value ? AlignmentDirectional.centerEnd : AlignmentDirectional.centerStart,
        child: Container(
          width: 20.0,
          height: 20.0,
          decoration: BoxDecoration(
            color: thumbColor,
            shape: BoxShape.circle,
            boxShadow: const [
              BoxShadow(
                color: Color(0x28000000),
                offset: Offset(0, 1),
                blurRadius: 2,
              ),
            ],
          ),
        ),
      ),
    );

    if (label == null && description == null) {
      return GestureDetector(
        onTap: disabled ? null : _handleTap,
        behavior: HitTestBehavior.opaque,
        child: switchTrack,
      );
    }

    final textTheme = theme.textTheme;

    return InkWell(
      onTap: disabled ? null : _handleTap,
      borderRadius: MdsRadius.borderMd,
      child: Padding(
        padding: const EdgeInsetsDirectional.symmetric(vertical: 4.0),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
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
            const SizedBox(width: MdsSpacing.inlineMd),
            switchTrack,
          ],
        ),
      ),
    );
  }
}
