// Master Design System (MDS) — Showcase Gallery Widget Test
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:mds_flutter_showcase/main.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUpAll(() {
    GoogleFonts.config.allowRuntimeFetching = false;
  });

  testWidgets('Showcase App loads cleanly with tabs, RTL, and dark theme toggles', (tester) async {
    await tester.pumpWidget(const MdsShowcaseApp());
    await tester.pumpAndSettle();

    // Verify Title presence
    expect(find.text('معرض Master Design System'), findsOneWidget);

    // Verify Tabs presence
    expect(find.text('الأزرار والإجراءات'), findsOneWidget);
    expect(find.text('المدخلات والنماذج'), findsOneWidget);

    // Toggle Direction to LTR
    await tester.tap(find.byIcon(Icons.format_textdirection_r_to_l));
    await tester.pumpAndSettle();
    expect(find.text('Master Design System Showcase'), findsOneWidget);

    // Toggle Theme to Dark
    await tester.tap(find.byIcon(Icons.dark_mode));
    await tester.pumpAndSettle();
    expect(find.byIcon(Icons.light_mode), findsOneWidget);
  });
}
