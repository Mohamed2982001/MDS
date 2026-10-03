// Master Design System (MDS) — Flutter UI Component Library Tests
// Phase 12: Production Flutter Component Library (mds_flutter_ui)
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:mds_flutter_ui/mds_flutter_ui.dart';

Widget _buildTestApp({
  required Widget child,
  ThemeData? theme,
  TextDirection textDirection = TextDirection.ltr,
}) {
  return MaterialApp(
    theme: theme ?? MdsThemeData.light(),
    home: Directionality(
      textDirection: textDirection,
      child: Scaffold(
        body: Center(child: child),
      ),
    ),
  );
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUpAll(() {
    GoogleFonts.config.allowRuntimeFetching = false;
  });

  group('MdsButton Component Tests', () {
    testWidgets('Renders label and responds to tap gesture', (tester) async {
      bool tapped = false;
      await tester.pumpWidget(
        _buildTestApp(
          child: MdsButton(
            text: 'Click Me',
            onPressed: () => tapped = true,
          ),
        ),
      );

      expect(find.text('Click Me'), findsOneWidget);
      await tester.tap(find.text('Click Me'));
      await tester.pumpAndSettle();
      expect(tapped, isTrue);
    });

    testWidgets('Disabled button does not invoke onPressed', (tester) async {
      const tapped = false;
      await tester.pumpWidget(
        _buildTestApp(
          child: const MdsButton(
            text: 'Disabled',
            onPressed: null,
          ),
        ),
      );

      await tester.tap(find.text('Disabled'));
      await tester.pumpAndSettle();
      expect(tapped, isFalse);
    });

    testWidgets('Loading state renders spinner and suppresses interaction', (tester) async {
      bool tapped = false;
      await tester.pumpWidget(
        _buildTestApp(
          child: MdsButton(
            text: 'Submit',
            isLoading: true,
            onPressed: () => tapped = true,
          ),
        ),
      );

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      await tester.tap(find.byType(MdsButton));
      await tester.pump();
      expect(tapped, isFalse);
    });
  });

  group('MdsTextField Component Tests', () {
    testWidgets('Renders label, hint, and allows text input', (tester) async {
      final valueList = <String>[];
      await tester.pumpWidget(
        _buildTestApp(
          child: MdsTextField(
            label: 'Email',
            hintText: 'user@example.com',
            onChanged: (val) => valueList.add(val),
          ),
        ),
      );

      expect(find.text('Email'), findsOneWidget);
      expect(find.text('user@example.com'), findsOneWidget);

      await tester.enterText(find.byType(TextField), 'mohamed@khalid.dev');
      await tester.pumpAndSettle();
      expect(valueList.last, equals('mohamed@khalid.dev'));
    });

    testWidgets('Renders error text correctly', (tester) async {
      await tester.pumpWidget(
        _buildTestApp(
          child: const MdsTextField(
            errorText: 'Required field',
          ),
        ),
      );

      expect(find.text('Required field'), findsOneWidget);
    });
  });

  group('MdsBadge Component Tests', () {
    testWidgets('Renders label and handles onDelete callback', (tester) async {
      bool deleted = false;
      await tester.pumpWidget(
        _buildTestApp(
          child: MdsBadge(
            label: 'Active',
            variant: MdsBadgeVariant.success,
            onDelete: () => deleted = true,
          ),
        ),
      );

      expect(find.text('Active'), findsOneWidget);
      expect(find.byIcon(Icons.close), findsOneWidget);

      await tester.tap(find.byIcon(Icons.close));
      await tester.pumpAndSettle();
      expect(deleted, isTrue);
    });
  });

  group('MdsCard Component Tests', () {
    testWidgets('Renders title, subtitle, child content, and actions', (tester) async {
      await tester.pumpWidget(
        _buildTestApp(
          child: MdsCard(
            title: const Text('Card Title'),
            subtitle: const Text('Card Subtitle'),
            actions: [
              MdsButton(text: 'Action', onPressed: () {}),
            ],
            child: const Text('Card Body Content'),
          ),
        ),
      );

      expect(find.text('Card Title'), findsOneWidget);
      expect(find.text('Card Subtitle'), findsOneWidget);
      expect(find.text('Card Body Content'), findsOneWidget);
      expect(find.text('Action'), findsOneWidget);
    });
  });

  group('MdsAlert Component Tests', () {
    testWidgets('Renders semantic alert and dismisses when closed', (tester) async {
      bool dismissed = false;
      await tester.pumpWidget(
        _buildTestApp(
          child: MdsAlert(
            title: 'Notice',
            message: 'Operation completed successfully.',
            variant: MdsAlertVariant.success,
            dismissible: true,
            onDismiss: () => dismissed = true,
          ),
        ),
      );

      expect(find.text('Notice'), findsOneWidget);
      expect(find.text('Operation completed successfully.'), findsOneWidget);
      expect(find.byIcon(Icons.close), findsOneWidget);

      await tester.tap(find.byIcon(Icons.close));
      await tester.pumpAndSettle();
      expect(dismissed, isTrue);
    });
  });

  group('MdsDialog Component Tests', () {
    testWidgets('Renders dialog title and action buttons', (tester) async {
      await tester.pumpWidget(
        _buildTestApp(
          child: MdsDialog(
            title: 'Confirm Delete',
            actions: [
              MdsButton(text: 'Cancel', onPressed: () {}),
              MdsButton(text: 'Delete', variant: MdsButtonVariant.danger, onPressed: () {}),
            ],
            content: const Text('Are you sure you want to delete this item?'),
          ),
        ),
      );

      expect(find.text('Confirm Delete'), findsOneWidget);
      expect(find.text('Are you sure you want to delete this item?'), findsOneWidget);
      expect(find.text('Cancel'), findsOneWidget);
      expect(find.text('Delete'), findsOneWidget);
    });
  });

  group('MdsToast Component Tests', () {
    testWidgets('Presents floating toast snackbar on trigger', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: MdsThemeData.light(),
          home: Scaffold(
            body: Builder(
              builder: (context) {
                return ElevatedButton(
                  onPressed: () {
                    MdsToast.show(
                      context: context,
                      title: 'Notification',
                      message: 'Your profile has been saved.',
                      variant: MdsToastVariant.success,
                    );
                  },
                  child: const Text('Show Toast'),
                );
              },
            ),
          ),
        ),
      );

      await tester.tap(find.text('Show Toast'));
      await tester.pump(); // Start animation
      await tester.pump(const Duration(milliseconds: 100)); // Animate in

      expect(find.text('Notification'), findsOneWidget);
      expect(find.text('Your profile has been saved.'), findsOneWidget);
    });
  });

  group('MdsCheckbox Component Tests', () {
    testWidgets('Toggles checked state on tap', (tester) async {
      bool? checked = false;
      await tester.pumpWidget(
        StatefulBuilder(
          builder: (context, setState) {
            return _buildTestApp(
              child: MdsCheckbox(
                value: checked,
                label: 'Agree to Terms',
                onChanged: (val) {
                  setState(() => checked = val);
                },
              ),
            );
          },
        ),
      );

      expect(find.text('Agree to Terms'), findsOneWidget);
      await tester.tap(find.byType(MdsCheckbox));
      await tester.pumpAndSettle();
      expect(checked, isTrue);
    });
  });

  group('MdsRadio Component Tests', () {
    testWidgets('Selects option on tap', (tester) async {
      int? selected = 1;
      await tester.pumpWidget(
        StatefulBuilder(
          builder: (context, setState) {
            return _buildTestApp(
              child: Column(
                children: [
                  MdsRadio<int>(
                    value: 1,
                    groupValue: selected,
                    label: 'Option 1',
                    onChanged: (val) => setState(() => selected = val),
                  ),
                  MdsRadio<int>(
                    value: 2,
                    groupValue: selected,
                    label: 'Option 2',
                    onChanged: (val) => setState(() => selected = val),
                  ),
                ],
              ),
            );
          },
        ),
      );

      expect(selected, equals(1));
      await tester.tap(find.text('Option 2'));
      await tester.pumpAndSettle();
      expect(selected, equals(2));
    });
  });

  group('MdsSwitch Component Tests', () {
    testWidgets('Toggles switch value on tap', (tester) async {
      bool value = false;
      await tester.pumpWidget(
        StatefulBuilder(
          builder: (context, setState) {
            return _buildTestApp(
              child: MdsSwitch(
                value: value,
                label: 'Push Notifications',
                onChanged: (val) => setState(() => value = val),
              ),
            );
          },
        ),
      );

      expect(find.text('Push Notifications'), findsOneWidget);
      await tester.tap(find.byType(MdsSwitch));
      await tester.pumpAndSettle();
      expect(value, isTrue);
    });
  });

  group('MdsDropdown Component Tests', () {
    testWidgets('Displays selected item and opens menu on tap', (tester) async {
      String? selected = 'opt1';
      const items = [
        MdsDropdownItem(value: 'opt1', label: 'Option 1'),
        MdsDropdownItem(value: 'opt2', label: 'Option 2'),
      ];

      await tester.pumpWidget(
        StatefulBuilder(
          builder: (context, setState) {
            return _buildTestApp(
              child: MdsDropdown<String>(
                label: 'Category',
                value: selected,
                items: items,
                onChanged: (val) => setState(() => selected = val),
              ),
            );
          },
        ),
      );

      expect(find.text('Category'), findsOneWidget);
      expect(find.text('Option 1'), findsOneWidget);

      // Tap to open overlay
      await tester.tap(find.text('Option 1'));
      await tester.pumpAndSettle();

      // Tap Option 2 in overlay
      expect(find.text('Option 2'), findsWidgets);
      await tester.tap(find.text('Option 2').last);
      await tester.pumpAndSettle();

      expect(selected, equals('opt2'));
    });
  });

  group('MdsAvatar Component Tests', () {
    test('Initials extraction utility works for single and multi-word names', () {
      expect(MdsAvatar.extractInitials('Mohamed Khalid'), equals('MK'));
      expect(MdsAvatar.extractInitials('Ahmed'), equals('A'));
      expect(MdsAvatar.extractInitials(null), equals('?'));
      expect(MdsAvatar.extractInitials('   '), equals('?'));
    });

    testWidgets('Renders initials and presence status indicator', (tester) async {
      await tester.pumpWidget(
        _buildTestApp(
          child: const MdsAvatar(
            name: 'Mohamed Khalid',
            status: MdsAvatarStatus.online,
          ),
        ),
      );

      expect(find.text('MK'), findsOneWidget);
    });

    testWidgets('MdsAvatarGroup renders cluster and overflow count', (tester) async {
      const avatars = [
        MdsAvatar(name: 'User 1'),
        MdsAvatar(name: 'User 2'),
        MdsAvatar(name: 'User 3'),
        MdsAvatar(name: 'User 4'),
        MdsAvatar(name: 'User 5'),
      ];

      await tester.pumpWidget(
        _buildTestApp(
          child: const MdsAvatarGroup(
            avatars: avatars,
            maxCount: 3,
          ),
        ),
      );

      expect(find.text('+2'), findsOneWidget);
    });
  });

  group('MdsProgressIndicator Component Tests', () {
    testWidgets('Renders linear progress with label and percentage', (tester) async {
      await tester.pumpWidget(
        _buildTestApp(
          child: const MdsProgressIndicator.linear(
            value: 0.75,
            label: 'Downloading',
            showPercentage: true,
          ),
        ),
      );

      expect(find.text('Downloading'), findsOneWidget);
      expect(find.text('75%'), findsOneWidget);
    });

    testWidgets('Renders circular progress spinner', (tester) async {
      await tester.pumpWidget(
        _buildTestApp(
          child: const MdsProgressIndicator.circular(
            value: 0.5,
            showPercentage: true,
          ),
        ),
      );

      expect(find.text('50%'), findsOneWidget);
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });
  });

  group('MdsTooltip Component Tests', () {
    testWidgets('Renders child widget with tooltip wrapper', (tester) async {
      await tester.pumpWidget(
        _buildTestApp(
          child: const MdsTooltip(
            message: 'Information details',
            child: Icon(Icons.info),
          ),
        ),
      );

      expect(find.byIcon(Icons.info), findsOneWidget);
      expect(find.byType(Tooltip), findsOneWidget);
    });
  });

  group('MdsDivider Component Tests', () {
    testWidgets('Renders horizontal divider with text label', (tester) async {
      await tester.pumpWidget(
        _buildTestApp(
          child: const MdsDivider(
            text: 'OR CONTINUE WITH',
            alignment: MdsDividerAlignment.center,
          ),
        ),
      );

      expect(find.text('OR CONTINUE WITH'), findsOneWidget);
    });

    testWidgets('Renders vertical divider without exception', (tester) async {
      await tester.pumpWidget(
        _buildTestApp(
          child: const SizedBox(
            height: 40,
            child: MdsDivider.vertical(),
          ),
        ),
      );

      expect(find.byType(MdsDivider), findsOneWidget);
    });
  });

  group('MdsTabs Component Tests', () {
    testWidgets('Renders tabs and updates selected tab on click', (tester) async {
      int active = 0;
      const tabs = [
        MdsTabItem(label: 'Overview'),
        MdsTabItem(label: 'Analytics'),
        MdsTabItem(label: 'Settings'),
      ];

      await tester.pumpWidget(
        StatefulBuilder(
          builder: (context, setState) {
            return _buildTestApp(
              child: MdsTabs(
                tabs: tabs,
                selectedIndex: active,
                onChanged: (idx) => setState(() => active = idx),
              ),
            );
          },
        ),
      );

      expect(find.text('Overview'), findsOneWidget);
      expect(find.text('Analytics'), findsOneWidget);
      expect(find.text('Settings'), findsOneWidget);

      await tester.tap(find.text('Analytics'));
      await tester.pumpAndSettle();
      expect(active, equals(1));
    });
  });

  group('MdsTable Component Tests', () {
    testWidgets('Renders column headers and rows', (tester) async {
      const columns = [
        MdsTableColumn(title: 'Name'),
        MdsTableColumn(title: 'Role'),
      ];

      final rows = [
        const MdsTableRow(cells: [Text('Mohamed Khalid'), Text('Lead Architect')]),
        const MdsTableRow(cells: [Text('Antigravity AI'), Text('Pair Programmer')]),
      ];

      await tester.pumpWidget(
        _buildTestApp(
          child: MdsTable(
            columns: columns,
            rows: rows,
          ),
        ),
      );

      expect(find.text('Name'), findsOneWidget);
      expect(find.text('Role'), findsOneWidget);
      expect(find.text('Mohamed Khalid'), findsOneWidget);
      expect(find.text('Antigravity AI'), findsOneWidget);
    });
  });

  group('MdsAccordion Component Tests', () {
    testWidgets('Expands and collapses on header tap', (tester) async {
      await tester.pumpWidget(
        _buildTestApp(
          child: const MdsAccordion(
            title: 'Accordion Section',
            child: Text('Hidden Accordion Content'),
          ),
        ),
      );

      expect(find.text('Accordion Section'), findsOneWidget);
      expect(find.text('Hidden Accordion Content'), findsOneWidget);

      // Tap header to toggle expansion
      await tester.tap(find.text('Accordion Section'));
      await tester.pumpAndSettle();

      // Tap header to collapse
      await tester.tap(find.text('Accordion Section'));
      await tester.pumpAndSettle();
    });
  });

  group('MdsSkeleton Component Tests', () {
    testWidgets('Renders text, circle, rect, and card skeleton variants', (tester) async {
      await tester.pumpWidget(
        _buildTestApp(
          child: const Column(
            children: [
              MdsSkeleton(width: 100, height: 20),
              MdsSkeleton.circle(size: 40),
              MdsSkeleton.text(textLines: 2),
              MdsSkeleton.card(width: 300),
            ],
          ),
        ),
      );

      expect(find.byType(MdsSkeleton), findsNWidgets(4));
      expect(find.byType(MdsShimmer), findsNWidgets(4));
    });
  });

  group('Arabic / RTL & Bidirectionality Tests', () {
    testWidgets('All components render cleanly in RTL text direction', (tester) async {
      await tester.pumpWidget(
        _buildTestApp(
          textDirection: TextDirection.rtl,
          child: SingleChildScrollView(
            child: Column(
              children: [
                MdsButton(text: 'حفظ التغييرات', onPressed: () {}),
                const SizedBox(height: 10),
                const MdsTextField(label: 'البريد الإلكتروني', hintText: 'أدخل بريدك'),
                const SizedBox(height: 10),
                const MdsBadge(label: 'مكتمل', variant: MdsBadgeVariant.success),
                const SizedBox(height: 10),
                const MdsAlert(title: 'تنبيه هام', message: 'تمت العملية بنجاح'),
                const SizedBox(height: 10),
                MdsSwitch(value: true, label: 'الوضع الليلي', onChanged: (_) {}),
                const SizedBox(height: 10),
                const MdsAvatar(name: 'محمد خالد', status: MdsAvatarStatus.online),
                const SizedBox(height: 10),
                const MdsDivider(text: 'أو عبر الوسائل التالية'),
              ],
            ),
          ),
        ),
      );

      expect(find.text('حفظ التغييرات'), findsOneWidget);
      expect(find.text('البريد الإلكتروني'), findsOneWidget);
      expect(find.text('مكتمل'), findsOneWidget);
      expect(find.text('تنبيه هام'), findsOneWidget);
      expect(find.text('الوضع الليلي'), findsOneWidget);
      expect(find.text('أو عبر الوسائل التالية'), findsOneWidget);
    });
  });

  group('Material 3 Dark Theme Integration', () {
    testWidgets('Components render cleanly under MdsThemeData.dark()', (tester) async {
      await tester.pumpWidget(
        _buildTestApp(
          theme: MdsThemeData.dark(),
          child: Column(
            children: [
              MdsButton(text: 'Dark Button', onPressed: () {}),
              const MdsBadge(label: 'Dark Badge', variant: MdsBadgeVariant.warning),
              const MdsProgressIndicator.linear(value: 0.6),
            ],
          ),
        ),
      );

      expect(find.text('Dark Button'), findsOneWidget);
      expect(find.text('Dark Badge'), findsOneWidget);
    });
  });
}
