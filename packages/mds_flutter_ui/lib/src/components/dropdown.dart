// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Sizing scale for [MdsDropdown].
enum MdsDropdownSize {
  sm,
  md,
  lg,
}

/// Represents a single option item inside [MdsDropdown].
class MdsDropdownItem<T> {
  const MdsDropdownItem({
    required this.value,
    required this.label,
    this.child,
    this.icon,
    this.isEnabled = true,
  });

  /// The underlying value of this item.
  final T value;

  /// Human-readable text label, also used for search filtering.
  final String label;

  /// Custom widget representation of this item. If null, [label] is rendered.
  final Widget? child;

  /// Optional leading icon for the item.
  final Widget? icon;

  /// Whether this item can be selected.
  final bool isEnabled;
}

/// Standard Master Design System accessible select / dropdown component.
///
/// Supports searchable items, clearable selection, keyboard navigation,
/// RTL/bidirectional layout, and custom item builders.
class MdsDropdown<T> extends StatefulWidget {
  const MdsDropdown({
    super.key,
    required this.items,
    this.value,
    this.onChanged,
    this.label,
    this.hintText = 'Select an option',
    this.searchHintText = 'Search...',
    this.helperText,
    this.errorText,
    this.prefixIcon,
    this.size = MdsDropdownSize.md,
    this.isSearchable = false,
    this.isClearable = false,
    this.isEnabled = true,
    this.maxMenuHeight = 280.0,
    this.borderRadius,
    this.emptyWidget,
  });

  /// All selectable items in the dropdown.
  final List<MdsDropdownItem<T>> items;

  /// Currently selected value.
  final T? value;

  /// Callback when a new value is selected, or null when cleared.
  final ValueChanged<T?>? onChanged;

  /// Optional label displayed above the dropdown input.
  final String? label;

  /// Placeholder text when no item is selected.
  final String hintText;

  /// Placeholder text for the search filter input.
  final String searchHintText;

  /// Informational helper text rendered below the dropdown.
  final String? helperText;

  /// Validation error text rendered below the dropdown.
  final String? errorText;

  /// Optional leading prefix icon.
  final Widget? prefixIcon;

  /// Visual size scale of the dropdown trigger.
  final MdsDropdownSize size;

  /// Whether an inline search filter is provided inside the menu.
  final bool isSearchable;

  /// Whether a clear icon appears when an item is selected.
  final bool isClearable;

  /// Whether the dropdown interaction is enabled.
  final bool isEnabled;

  /// Maximum height of the dropdown popup overlay.
  final double maxMenuHeight;

  /// Optional custom border radius.
  final BorderRadiusGeometry? borderRadius;

  /// Custom widget displayed when search filter yields no results.
  final Widget? emptyWidget;

  @override
  State<MdsDropdown<T>> createState() => _MdsDropdownState<T>();
}

class _MdsDropdownState<T> extends State<MdsDropdown<T>> with SingleTickerProviderStateMixin {
  final LayerLink _layerLink = LayerLink();
  OverlayEntry? _overlayEntry;
  bool _isOpen = false;
  late final AnimationController _arrowController;
  late final Animation<double> _arrowAnimation;
  final TextEditingController _searchController = TextEditingController();
  String _searchQuery = '';

  @override
  void initState() {
    super.initState();
    _arrowController = AnimationController(
      vsync: this,
      duration: MdsDurations.fast,
    );
    _arrowAnimation = Tween<double>(begin: 0.0, end: 0.5).animate(
      CurvedAnimation(parent: _arrowController, curve: MdsCurves.standard),
    );
  }

  @override
  void didUpdateWidget(covariant MdsDropdown<T> oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (!widget.isEnabled && _isOpen) {
      _closeDropdown();
    }
  }

  @override
  void dispose() {
    _closeDropdown();
    _arrowController.dispose();
    _searchController.dispose();
    super.dispose();
  }

  void _toggleDropdown() {
    if (!widget.isEnabled) return;
    if (_isOpen) {
      _closeDropdown();
    } else {
      _openDropdown();
    }
  }

  void _openDropdown() {
    if (_isOpen) return;
    _searchController.clear();
    _searchQuery = '';
    _overlayEntry = _createOverlayEntry();
    Overlay.of(context).insert(_overlayEntry!);
    _arrowController.forward();
    setState(() {
      _isOpen = true;
    });
  }

  void _closeDropdown() {
    if (!_isOpen) return;
    _overlayEntry?.remove();
    _overlayEntry = null;
    _arrowController.reverse();
    if (mounted) {
      setState(() {
        _isOpen = false;
      });
    }
  }

  void _selectItem(MdsDropdownItem<T> item) {
    if (!item.isEnabled) return;
    _closeDropdown();
    widget.onChanged?.call(item.value);
  }

  void _clearSelection() {
    widget.onChanged?.call(null);
  }

  MdsDropdownItem<T>? get _selectedItem {
    if (widget.value == null) return null;
    for (final item in widget.items) {
      if (item.value == widget.value) return item;
    }
    return null;
  }

  OverlayEntry _createOverlayEntry() {
    final renderBox = context.findRenderObject() as RenderBox?;
    final size = renderBox?.size ?? Size.zero;

    return OverlayEntry(
      builder: (overlayContext) {
        final theme = Theme.of(overlayContext);
        final isDark = theme.brightness == Brightness.dark;
        final mds = theme.extension<MdsSemanticColors>() ??
            (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

        return Stack(
          children: [
            Positioned.fill(
              child: GestureDetector(
                behavior: HitTestBehavior.translucent,
                onTap: _closeDropdown,
              ),
            ),
            CompositedTransformFollower(
              link: _layerLink,
              showWhenUnlinked: false,
              offset: Offset(0.0, size.height + 4.0),
              child: Material(
                elevation: 0,
                color: Colors.transparent,
                child: StatefulBuilder(
                  builder: (context, setMenuState) {
                    final filteredItems = widget.items.where((item) {
                      if (_searchQuery.isEmpty) return true;
                      return item.label.toLowerCase().contains(_searchQuery.toLowerCase());
                    }).toList();

                    return Container(
                      width: size.width,
                      constraints: BoxConstraints(
                        maxHeight: widget.maxMenuHeight,
                      ),
                      decoration: BoxDecoration(
                        color: mds.surfaceDefault,
                        borderRadius: widget.borderRadius ?? MdsRadius.borderMd,
                        border: Border.all(
                          color: isDark ? MdsColors.neutral700 : mds.borderDefault,
                          width: MdsRadius.borderWidthThin,
                        ),
                        boxShadow: MdsElevation.shadow2,
                      ),
                      child: ClipRRect(
                        borderRadius: widget.borderRadius ?? MdsRadius.borderMd,
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          crossAxisAlignment: CrossAxisAlignment.stretch,
                          children: [
                            if (widget.isSearchable) ...[
                              Padding(
                                padding: const EdgeInsetsDirectional.all(8.0),
                                child: Container(
                                  height: 38,
                                  decoration: BoxDecoration(
                                    color: isDark ? MdsColors.neutral800 : MdsColors.neutral100,
                                    borderRadius: MdsRadius.borderSm,
                                  ),
                                  child: TextField(
                                    controller: _searchController,
                                    autofocus: true,
                                    style: theme.textTheme.bodyMedium?.copyWith(
                                      color: mds.textPrimary,
                                    ),
                                    decoration: InputDecoration(
                                      hintText: widget.searchHintText,
                                      hintStyle: theme.textTheme.bodyMedium?.copyWith(
                                        color: mds.textSecondary,
                                      ),
                                      prefixIcon: Icon(
                                        Icons.search,
                                        size: 18,
                                        color: mds.textSecondary,
                                      ),
                                      border: InputBorder.none,
                                      contentPadding: const EdgeInsetsDirectional.symmetric(
                                        horizontal: 8.0,
                                        vertical: 10.0,
                                      ),
                                    ),
                                    onChanged: (query) {
                                      setMenuState(() {
                                        _searchQuery = query;
                                      });
                                    },
                                  ),
                                ),
                              ),
                              Divider(
                                height: 1,
                                thickness: MdsRadius.borderWidthThin,
                                color: isDark ? MdsColors.neutral800 : mds.borderSubtle,
                              ),
                            ],
                            Flexible(
                              child: filteredItems.isEmpty
                                  ? widget.emptyWidget ??
                                      Padding(
                                        padding: const EdgeInsetsDirectional.all(16.0),
                                        child: Center(
                                          child: Text(
                                            'No matching options',
                                            softWrap: true,
                                            style: theme.textTheme.bodyMedium?.copyWith(
                                              color: mds.textSecondary,
                                            ),
                                          ),
                                        ),
                                      )
                                  : ListView.separated(
                                      padding: const EdgeInsetsDirectional.symmetric(vertical: 4.0),
                                      shrinkWrap: true,
                                      itemCount: filteredItems.length,
                                      separatorBuilder: (_, __) => const SizedBox(height: 2),
                                      itemBuilder: (context, index) {
                                        final item = filteredItems[index];
                                        final isSelected = item.value == widget.value;

                                        return InkWell(
                                          onTap: item.isEnabled ? () => _selectItem(item) : null,
                                          child: Container(
                                            padding: const EdgeInsetsDirectional.symmetric(
                                              horizontal: 12.0,
                                              vertical: 10.0,
                                            ),
                                            color: isSelected
                                                ? (isDark
                                                    ? MdsColors.brand800.withValues(alpha: 0.35)
                                                    : MdsColors.brand50)
                                                : Colors.transparent,
                                            child: Row(
                                              children: [
                                                if (item.icon != null) ...[
                                                  item.icon!,
                                                  const SizedBox(width: 8.0),
                                                ],
                                                Expanded(
                                                  child: item.child ??
                                                      Text(
                                                        item.label,
                                                        softWrap: true,
                                                        style: theme.textTheme.bodyMedium?.copyWith(
                                                          color: !item.isEnabled
                                                              ? mds.actionDisabledForeground
                                                              : isSelected
                                                                  ? (isDark
                                                                      ? MdsColors.brand200
                                                                      : MdsColors.brand700)
                                                                  : mds.textPrimary,
                                                          fontWeight: isSelected
                                                              ? FontWeight.w600
                                                              : FontWeight.normal,
                                                        ),
                                                      ),
                                                ),
                                                if (isSelected)
                                                  Icon(
                                                    Icons.check,
                                                    size: 18,
                                                    color: isDark
                                                        ? MdsColors.brand300
                                                        : MdsColors.brand600,
                                                  ),
                                              ],
                                            ),
                                          ),
                                        );
                                      },
                                    ),
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
              ),
            ),
          ],
        );
      },
    );
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

    if (!widget.isEnabled) {
      borderColor = isDark ? MdsColors.neutral800 : mds.borderSubtle;
    } else if (hasError) {
      borderColor = mds.feedbackDanger;
      borderWidth = MdsRadius.borderWidthRegular;
    } else if (_isOpen) {
      borderColor = mds.focusRing;
      borderWidth = MdsRadius.borderWidthThick;
    } else {
      borderColor = isDark ? MdsColors.neutral700 : mds.borderDefault;
    }

    final effectiveRadius = widget.borderRadius ?? MdsRadius.borderMd;
    final selectedItem = _selectedItem;

    final double minHeight = switch (widget.size) {
      MdsDropdownSize.sm => 36.0,
      MdsDropdownSize.md => 44.0,
      MdsDropdownSize.lg => 52.0,
    };

    final EdgeInsetsDirectional padding = switch (widget.size) {
      MdsDropdownSize.sm => const EdgeInsetsDirectional.symmetric(horizontal: 10.0, vertical: 6.0),
      MdsDropdownSize.md => const EdgeInsetsDirectional.symmetric(horizontal: 14.0, vertical: 10.0),
      MdsDropdownSize.lg => const EdgeInsetsDirectional.symmetric(horizontal: 16.0, vertical: 14.0),
    };

    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (widget.label != null) ...[
          Padding(
            padding: const EdgeInsetsDirectional.only(bottom: 6.0),
            child: Text(
              widget.label!,
              softWrap: true,
              style: textTheme.labelLarge?.copyWith(
                fontWeight: FontWeight.w600,
                color: widget.isEnabled ? mds.textPrimary : mds.actionDisabledForeground,
              ),
            ),
          ),
        ],
        CompositedTransformTarget(
          link: _layerLink,
          child: InkWell(
            onTap: widget.isEnabled ? _toggleDropdown : null,
            borderRadius: MdsRadius.borderMd,
            child: AnimatedContainer(
              duration: MdsDurations.fast,
              curve: MdsCurves.standard,
              constraints: BoxConstraints(minHeight: minHeight),
              padding: padding,
              decoration: BoxDecoration(
                color: widget.isEnabled ? mds.surfaceDefault : mds.surfaceRaised,
                borderRadius: effectiveRadius,
                border: Border.all(
                  color: borderColor,
                  width: borderWidth,
                ),
                boxShadow: _isOpen ? MdsElevation.shadow1 : null,
              ),
              child: Row(
                children: [
                  if (widget.prefixIcon != null) ...[
                    widget.prefixIcon!,
                    const SizedBox(width: 8.0),
                  ],
                  Expanded(
                    child: selectedItem != null
                        ? (selectedItem.child ??
                            Text(
                              selectedItem.label,
                              softWrap: true,
                              style: textTheme.bodyMedium?.copyWith(
                                color: widget.isEnabled ? mds.textPrimary : mds.actionDisabledForeground,
                              ),
                            ))
                        : Text(
                            widget.hintText,
                            softWrap: true,
                            style: textTheme.bodyMedium?.copyWith(
                              color: mds.textSecondary,
                            ),
                          ),
                  ),
                  if (widget.isClearable && selectedItem != null && widget.isEnabled) ...[
                    GestureDetector(
                      onTap: _clearSelection,
                      child: Padding(
                        padding: const EdgeInsetsDirectional.only(end: 4.0),
                        child: Icon(
                          Icons.clear,
                          size: 18,
                          color: mds.textSecondary,
                        ),
                      ),
                    ),
                  ],
                  RotationTransition(
                    turns: _arrowAnimation,
                    child: Icon(
                      Icons.keyboard_arrow_down,
                      size: 20,
                      color: widget.isEnabled ? mds.textSecondary : mds.actionDisabledForeground,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
        if (hasError) ...[
          Padding(
            padding: const EdgeInsetsDirectional.only(top: 4.0, start: 4.0),
            child: Text(
              widget.errorText!,
              softWrap: true,
              style: textTheme.bodySmall?.copyWith(
                color: mds.feedbackDanger,
              ),
            ),
          ),
        ] else if (widget.helperText != null) ...[
          Padding(
            padding: const EdgeInsetsDirectional.only(top: 4.0, start: 4.0),
            child: Text(
              widget.helperText!,
              softWrap: true,
              style: textTheme.bodySmall?.copyWith(
                color: mds.textSecondary,
              ),
            ),
          ),
        ],
      ],
    );
  }
}
