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

  testWidgets('Test all 6 tabs in Showcase App', (tester) async {
    tester.view.physicalSize = const Size(1280, 800);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(() => tester.view.resetPhysicalSize());

    await tester.pumpWidget(const MdsShowcaseApp());
    await tester.pumpAndSettle();

    // Verify Title presence & Tab 0 (Buttons)
    expect(find.text('معرض Master Design System'), findsOneWidget);
    expect(find.text('زر أساسي'), findsOneWidget);

    // Tap Tab 1: Inputs & Forms
    await tester.tap(find.text('المدخلات والنماذج'));
    await tester.pumpAndSettle();
    expect(find.text('البريد الإلكتروني'), findsOneWidget);

    // Tap Tab 2: Cards & Alerts
    await tester.tap(find.text('البطاقات والتنبيهات'));
    await tester.pumpAndSettle();
    expect(find.text('معلومات عامة'), findsOneWidget);

    // Tap Tab 3: Modals & Feedback
    await tester.tap(find.text('النوافذ والتغذية الراجعة'));
    await tester.pumpAndSettle();
    expect(find.text('فتح نافذة تأكيد (Dialog)'), findsOneWidget);

    // Tap Tab 4: Data & Navigation
    await tester.tap(find.text('البيانات والتنقل'));
    await tester.pumpAndSettle();
    expect(find.text('MK'), findsOneWidget);

    // Tap Tab 5: Loaders & Shimmer
    await tester.tap(find.text('التحميل والشيمر'));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 300));
    expect(find.text('اكتمال المعمارية'), findsOneWidget);
  });
}
