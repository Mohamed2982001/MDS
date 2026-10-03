// Master Design System (MDS) — Flutter UI Component Library
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

/// Specification for a single column header within [MdsTable].
class MdsTableColumn {
  const MdsTableColumn({
    required this.title,
    this.titleWidget,
    this.width,
    this.flex = 1,
    this.alignment = AlignmentDirectional.centerStart,
    this.isSortable = false,
    this.isSorted = false,
    this.isAscending = true,
    this.onSort,
  });

  /// Plain text column title.
  final String title;

  /// Custom widget replacement for column header.
  final Widget? titleWidget;

  /// Optional fixed width for the column.
  final double? width;

  /// Flex factor when width is not explicitly fixed.
  final int flex;

  /// Directional alignment of the cell content.
  final AlignmentDirectional alignment;

  /// Whether column header is clickable for sorting.
  final bool isSortable;

  /// Whether this column is the active sort key.
  final bool isSorted;

  /// Sorting order direction if sorted.
  final bool isAscending;

  /// Callback when header is tapped for sorting.
  final VoidCallback? onSort;
}

/// Represents a single data row inside [MdsTable].
class MdsTableRow {
  const MdsTableRow({
    required this.cells,
    this.onTap,
    this.backgroundColor,
    this.isSelected = false,
  });

  /// Widget content for each cell in the row matching columns order.
  final List<Widget> cells;

  /// Optional row click callback.
  final VoidCallback? onTap;

  /// Custom row background color override.
  final Color? backgroundColor;

  /// Whether the row is flagged as selected.
  final bool isSelected;
}

/// Standard Master Design System data table component.
///
/// Supports striped alternating rows, responsive horizontal scrolling,
/// custom column alignments, directional cell paddings, and empty states.
class MdsTable extends StatelessWidget {
  const MdsTable({
    super.key,
    required this.columns,
    required this.rows,
    this.isStriped = true,
    this.isBordered = true,
    this.minWidth,
    this.emptyWidget,
    this.borderRadius,
    this.cellPadding = const EdgeInsetsDirectional.symmetric(horizontal: 16.0, vertical: 12.0),
    this.headerBackgroundColor,
  });

  /// Column definitions.
  final List<MdsTableColumn> columns;

  /// Row items to render.
  final List<MdsTableRow> rows;

  /// Whether to alternate row background colors for improved legibility.
  final bool isStriped;

  /// Whether outer borders and cell dividers are drawn.
  final bool isBordered;

  /// Minimum width of the table. If set and screen is narrower, enables horizontal scroll.
  final double? minWidth;

  /// Widget shown when [rows] is empty.
  final Widget? emptyWidget;

  /// Table container corner radius.
  final BorderRadiusGeometry? borderRadius;

  /// Internal padding for table cells.
  final EdgeInsetsDirectional cellPadding;

  /// Header row background color override.
  final Color? headerBackgroundColor;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final mds = theme.extension<MdsSemanticColors>() ??
        (isDark ? MdsSemanticColors.dark() : MdsSemanticColors.light());

    final effectiveRadius = borderRadius ?? MdsRadius.borderMd;
    final borderColor = isDark ? MdsColors.neutral700 : mds.borderDefault;
    final headerBg = headerBackgroundColor ??
        (isDark ? MdsColors.neutral800 : MdsColors.neutral100);

    Widget buildHeaderCell(MdsTableColumn col) {
      Widget cellContent = Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          col.titleWidget ??
              Flexible(
                child: Text(
                  col.title,
                  softWrap: true,
                  style: theme.textTheme.labelMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: mds.textPrimary,
                  ),
                ),
              ),
          if (col.isSortable) ...[
            const SizedBox(width: 4.0),
            Icon(
              col.isSorted
                  ? (col.isAscending ? Icons.arrow_upward : Icons.arrow_downward)
                  : Icons.unfold_more,
              size: 16,
              color: col.isSorted ? mds.actionPrimaryDefault : mds.textSecondary,
            ),
          ],
        ],
      );

      if (col.isSortable && col.onSort != null) {
        cellContent = InkWell(
          onTap: col.onSort,
          child: cellContent,
        );
      }

      final padded = Container(
        padding: cellPadding,
        alignment: col.alignment,
        child: cellContent,
      );

      if (col.width != null) {
        return SizedBox(width: col.width, child: padded);
      }
      return Expanded(flex: col.flex, child: padded);
    }

    Widget buildDataCell(MdsTableColumn col, Widget cell) {
      final padded = Container(
        padding: cellPadding,
        alignment: col.alignment,
        child: cell,
      );

      if (col.width != null) {
        return SizedBox(width: col.width, child: padded);
      }
      return Expanded(flex: col.flex, child: padded);
    }

    Widget tableBody;

    if (rows.isEmpty) {
      tableBody = emptyWidget ??
          Padding(
            padding: const EdgeInsetsDirectional.all(32.0),
            child: Center(
              child: Text(
                'No data available',
                softWrap: true,
                style: theme.textTheme.bodyMedium?.copyWith(
                  color: mds.textSecondary,
                ),
              ),
            ),
          );
    } else {
      tableBody = Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          for (int r = 0; r < rows.length; r++) ...[
            if (r > 0 && isBordered)
              Divider(
                height: 1,
                thickness: MdsRadius.borderWidthThin,
                color: isDark ? MdsColors.neutral800 : mds.borderSubtle,
              ),
            Builder(
              builder: (context) {
                final row = rows[r];
                final isEven = r % 2 == 0;
                Color rowBg;

                if (row.isSelected) {
                  rowBg = isDark
                      ? MdsColors.brand800.withValues(alpha: 0.3)
                      : MdsColors.brand50;
                } else if (row.backgroundColor != null) {
                  rowBg = row.backgroundColor!;
                } else if (isStriped && !isEven) {
                  rowBg = isDark ? MdsColors.neutral800.withValues(alpha: 0.5) : MdsColors.neutral50;
                } else {
                  rowBg = mds.surfaceDefault;
                }

                Widget rowContent = Container(
                  color: rowBg,
                  child: Row(
                    children: [
                      for (int c = 0; c < columns.length; c++)
                        buildDataCell(
                          columns[c],
                          c < row.cells.length ? row.cells[c] : const SizedBox.shrink(),
                        ),
                    ],
                  ),
                );

                if (row.onTap != null) {
                  rowContent = InkWell(
                    onTap: row.onTap,
                    child: rowContent,
                  );
                }

                return rowContent;
              },
            ),
          ],
        ],
      );
    }

    Widget tableLayout = Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // Header
        Container(
          color: headerBg,
          child: Row(
            children: [
              for (final col in columns) buildHeaderCell(col),
            ],
          ),
        ),
        if (isBordered)
          Divider(
            height: 1,
            thickness: MdsRadius.borderWidthRegular,
            color: borderColor,
          ),
        tableBody,
      ],
    );

    if (minWidth != null) {
      tableLayout = SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        physics: const BouncingScrollPhysics(),
        child: SizedBox(
          width: minWidth,
          child: tableLayout,
        ),
      );
    }

    return Container(
      decoration: BoxDecoration(
        color: mds.surfaceDefault,
        borderRadius: effectiveRadius,
        border: isBordered
            ? Border.all(
                color: borderColor,
                width: MdsRadius.borderWidthThin,
              )
            : null,
      ),
      child: ClipRRect(
        borderRadius: effectiveRadius,
        child: tableLayout,
      ),
    );
  }
}
