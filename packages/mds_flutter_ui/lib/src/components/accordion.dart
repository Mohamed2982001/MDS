// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Standard Master Design System expandable accordion panel.
///
/// Features smooth chevron rotation, height size transition,
/// leading icon, subtitle, and directional paddings.
class MdsAccordion extends StatefulWidget {
  const MdsAccordion({
    super.key,
    required this.title,
    required this.child,
    this.subtitle,
    this.leading,
    this.trailing,
    this.isExpanded = false,
    this.onExpansionChanged,
    this.borderRadius,
    this.headerPadding = const EdgeInsetsDirectional.symmetric(horizontal: 16.0, vertical: 14.0),
    this.bodyPadding = const EdgeInsetsDirectional.fromSTEB(16.0, 0.0, 16.0, 16.0),
    this.isBordered = true,
  });

  /// Main title text rendered in the header.
  final String title;

  /// Expanded body widget content.
  final Widget child;

  /// Optional subtitle rendered below the title.
  final String? subtitle;

  /// Optional leading widget (e.g. icon or badge).
  final Widget? leading;

  /// Optional custom trailing widget replacing the default rotating chevron.
  final Widget? trailing;

  /// Initial expansion state when uncontrolled.
  final bool isExpanded;

  /// Callback when expansion state changes.
  final ValueChanged<bool>? onExpansionChanged;

  /// Corner radius of the accordion card.
  final BorderRadiusGeometry? borderRadius;

  /// Internal padding for the clickable header.
  final EdgeInsetsDirectional headerPadding;

  /// Internal padding for the expanded content area.
  final EdgeInsetsDirectional bodyPadding;

  /// Whether to render an outer border.
  final bool isBordered;

  @override
  State<MdsAccordion> createState() => _MdsAccordionState();
}

class _MdsAccordionState extends State<MdsAccordion> with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _iconTurns;
  late final Animation<double> _heightFactor;
  late bool _isExpanded;

  @override
  void initState() {
    super.initState();
    _isExpanded = widget.isExpanded;
    _controller = AnimationController(
      duration: MdsDurations.normal,
      vsync: this,
    );
    _iconTurns = Tween<double>(begin: 0.0, end: 0.5).animate(
      CurvedAnimation(parent: _controller, curve: MdsCurves.standard),
    );
    _heightFactor = CurvedAnimation(
      parent: _controller,
      curve: MdsCurves.standard,
    );

    if (_isExpanded) {
      _controller.value = 1.0;
    }
  }

  @override
  void didUpdateWidget(covariant MdsAccordion oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.isExpanded != oldWidget.isExpanded && widget.isExpanded != _isExpanded) {
      _toggleExpansion(widget.isExpanded);
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _toggleExpansion([bool? target]) {
    final nextState = target ?? !_isExpanded;
    setState(() {
      _isExpanded = nextState;
      if (_isExpanded) {
        _controller.forward();
      } else {
        _controller.reverse();
      }
    });
    widget.onExpansionChanged?.call(_isExpanded);
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    final effectiveRadius = widget.borderRadius ?? MdsRadius.borderMd;
    final borderColor = isDark ? MdsColors.neutral700 : mds.borderDefault;

    return Container(
      decoration: BoxDecoration(
        color: mds.surfaceDefault,
        borderRadius: effectiveRadius,
        border: widget.isBordered
            ? Border.all(
                color: borderColor,
                width: MdsRadius.borderWidthThin,
              )
            : null,
      ),
      child: ClipRRect(
        borderRadius: effectiveRadius,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            InkWell(
              onTap: () => _toggleExpansion(),
              child: Padding(
                padding: widget.headerPadding,
                child: Row(
                  children: [
                    if (widget.leading != null) ...[
                      widget.leading!,
                      const SizedBox(width: 12.0),
                    ],
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            widget.title,
                            softWrap: true,
                            style: theme.textTheme.titleSmall?.copyWith(
                              fontWeight: FontWeight.w600,
                              color: mds.textPrimary,
                            ),
                          ),
                          if (widget.subtitle != null) ...[
                            const SizedBox(height: 2.0),
                            Text(
                              widget.subtitle!,
                              softWrap: true,
                              style: theme.textTheme.bodySmall?.copyWith(
                                color: mds.textSecondary,
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                    const SizedBox(width: 8.0),
                    widget.trailing ??
                        RotationTransition(
                          turns: _iconTurns,
                          child: Icon(
                            Icons.keyboard_arrow_down,
                            size: 20,
                            color: mds.textSecondary,
                          ),
                        ),
                  ],
                ),
              ),
            ),
            ClipRect(
              child: AnimatedBuilder(
                animation: _heightFactor,
                builder: (context, child) {
                  return Align(
                    alignment: Alignment.centerLeft,
                    heightFactor: _heightFactor.value,
                    child: child,
                  );
                },
                child: Padding(
                  padding: widget.bodyPadding,
                  child: widget.child,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

/// A coordinated group of [MdsAccordion] items with optional single-panel mode.
class MdsAccordionGroup extends StatefulWidget {
  const MdsAccordionGroup({
    super.key,
    required this.children,
    this.allowMultiple = false,
    this.spacing = 8.0,
  });

  /// The list of accordion panels.
  final List<MdsAccordion> children;

  /// Whether multiple panels can be expanded simultaneously.
  final bool allowMultiple;

  /// Vertical spacing between panels.
  final double spacing;

  @override
  State<MdsAccordionGroup> createState() => _MdsAccordionGroupState();
}

class _MdsAccordionGroupState extends State<MdsAccordionGroup> {
  int? _expandedIndex;

  @override
  void initState() {
    super.initState();
    for (int i = 0; i < widget.children.length; i++) {
      if (widget.children[i].isExpanded) {
        _expandedIndex = i;
        break;
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (widget.allowMultiple) {
      return Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          for (int i = 0; i < widget.children.length; i++) ...[
            if (i > 0) SizedBox(height: widget.spacing),
            widget.children[i],
          ],
        ],
      );
    }

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        for (int i = 0; i < widget.children.length; i++) ...[
          if (i > 0) SizedBox(height: widget.spacing),
          MdsAccordion(
            key: widget.children[i].key,
            title: widget.children[i].title,
            subtitle: widget.children[i].subtitle,
            leading: widget.children[i].leading,
            trailing: widget.children[i].trailing,
            borderRadius: widget.children[i].borderRadius,
            headerPadding: widget.children[i].headerPadding,
            bodyPadding: widget.children[i].bodyPadding,
            isBordered: widget.children[i].isBordered,
            isExpanded: _expandedIndex == i,
            onExpansionChanged: (isExp) {
              setState(() {
                _expandedIndex = isExp ? i : null;
              });
              widget.children[i].onExpansionChanged?.call(isExp);
            },
            child: widget.children[i].child,
          ),
        ],
      ],
    );
  }
}
