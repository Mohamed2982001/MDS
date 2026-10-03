// Master Design System (MDS) — Interactive Flutter Showcase Gallery
// Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

import 'package:flutter/material.dart';
import 'package:mds_flutter_ui/mds_flutter_ui.dart';

void main() {
  runApp(const MdsShowcaseApp());
}

class MdsShowcaseApp extends StatefulWidget {
  const MdsShowcaseApp({super.key});

  @override
  State<MdsShowcaseApp> createState() => _MdsShowcaseAppState();
}

class _MdsShowcaseAppState extends State<MdsShowcaseApp> {
  ThemeMode _themeMode = ThemeMode.light;
  TextDirection _textDirection = TextDirection.rtl; // Default to Arabic / RTL

  void _toggleTheme() {
    setState(() {
      _themeMode = _themeMode == ThemeMode.light ? ThemeMode.dark : ThemeMode.light;
    });
  }

  void _toggleDirection() {
    setState(() {
      _textDirection = _textDirection == TextDirection.rtl ? TextDirection.ltr : TextDirection.rtl;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MDS Showcase Gallery',
      debugShowCheckedModeBanner: false,
      theme: MdsThemeData.light(),
      darkTheme: MdsThemeData.dark(),
      themeMode: _themeMode,
      builder: (context, child) {
        return Directionality(
          textDirection: _textDirection,
          child: child ?? const SizedBox.shrink(),
        );
      },
      home: ShowcaseHomeScreen(
        themeMode: _themeMode,
        textDirection: _textDirection,
        onToggleTheme: _toggleTheme,
        onToggleDirection: _toggleDirection,
      ),
    );
  }
}

class ShowcaseHomeScreen extends StatefulWidget {
  final ThemeMode themeMode;
  final TextDirection textDirection;
  final VoidCallback onToggleTheme;
  final VoidCallback onToggleDirection;

  const ShowcaseHomeScreen({
    super.key,
    required this.themeMode,
    required this.textDirection,
    required this.onToggleTheme,
    required this.onToggleDirection,
  });

  @override
  State<ShowcaseHomeScreen> createState() => _ShowcaseHomeScreenState();
}

class _ShowcaseHomeScreenState extends State<ShowcaseHomeScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  // Interactive demo states
  bool _btnLoading = false;
  bool _checkboxVal = true;
  String _radioVal = 'opt1';
  bool _switchVal = true;
  String? _dropdownVal = 'Cairo';
  final double _progressVal = 0.65;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 6, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isRtl = widget.textDirection == TextDirection.rtl;
    final isDark = widget.themeMode == ThemeMode.dark;

    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(isRtl ? 'معرض Master Design System' : 'Master Design System Showcase'),
            Text(
              isRtl ? 'إصدار v1.2.0 — إنتاجي بالكامل' : 'v1.2.0 — Production Ready',
              style: Theme.of(context).textTheme.bodySmall?.copyWith(color: MdsColors.textSecondaryLight),
            ),
          ],
        ),
        actions: [
          IconButton(
            tooltip: isRtl ? 'تبديل الاتجاه (RTL / LTR)' : 'Toggle Direction (RTL / LTR)',
            icon: Icon(isRtl ? Icons.format_textdirection_r_to_l : Icons.format_textdirection_l_to_r),
            onPressed: widget.onToggleDirection,
          ),
          IconButton(
            tooltip: isDark ? 'الوضع النهاري' : 'الوضع الليلي',
            icon: Icon(isDark ? Icons.light_mode : Icons.dark_mode),
            onPressed: widget.onToggleTheme,
          ),
          const SizedBox(width: 8),
        ],
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          tabs: [
            Tab(text: isRtl ? 'الأزرار والإجراءات' : 'Buttons & Actions'),
            Tab(text: isRtl ? 'المدخلات والنماذج' : 'Inputs & Forms'),
            Tab(text: isRtl ? 'البطاقات والتنبيهات' : 'Cards & Alerts'),
            Tab(text: isRtl ? 'النوافذ والتغذية الراجعة' : 'Modals & Feedback'),
            Tab(text: isRtl ? 'البيانات والتنقل' : 'Data & Navigation'),
            Tab(text: isRtl ? 'التحميل والشيمر' : 'Loaders & Shimmer'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildButtonsTab(context, isRtl),
          _buildInputsTab(context, isRtl),
          _buildCardsAlertsTab(context, isRtl),
          _buildFeedbackTab(context, isRtl),
          _buildDataNavigationTab(context, isRtl),
          _buildLoadersShimmerTab(context, isRtl),
        ],
      ),
    );
  }

  // 1. Buttons & Actions
  Widget _buildButtonsTab(BuildContext context, bool isRtl) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        _buildSectionHeader(isRtl ? 'أنواع الأزرار (Variants)' : 'Button Variants'),
        Wrap(
          spacing: 12,
          runSpacing: 12,
          children: [
            MdsButton(
              text: isRtl ? 'زر أساسي' : 'Primary Button',
              leadingIcon: const Icon(Icons.check_circle_outline, size: 18),
              onPressed: () {},
            ),
            MdsButton(
              text: isRtl ? 'زر ثانوي' : 'Secondary Button',
              variant: MdsButtonVariant.secondary,
              onPressed: () {},
            ),
            MdsButton(
              text: isRtl ? 'زر محدد (Outline)' : 'Outline Button',
              variant: MdsButtonVariant.outline,
              onPressed: () {},
            ),
            MdsButton(
              text: isRtl ? 'زر شفاف (Ghost)' : 'Ghost Button',
              variant: MdsButtonVariant.ghost,
              onPressed: () {},
            ),
            MdsButton(
              text: isRtl ? 'زر تحذير (Danger)' : 'Danger Button',
              variant: MdsButtonVariant.danger,
              leadingIcon: const Icon(Icons.delete_outline, size: 18),
              onPressed: () {},
            ),
          ],
        ),
        const SizedBox(height: 24),
        _buildSectionHeader(isRtl ? 'أحجام الأزرار وحالة التحميل' : 'Button Sizes & Loading State'),
        Wrap(
          spacing: 12,
          runSpacing: 12,
          crossAxisAlignment: WrapCrossAlignment.center,
          children: [
            MdsButton(
              text: isRtl ? 'صغير (Small)' : 'Small',
              size: MdsButtonSize.sm,
              onPressed: () {},
            ),
            MdsButton(
              text: isRtl ? 'متوسط (Medium)' : 'Medium',
              size: MdsButtonSize.md,
              onPressed: () {},
            ),
            MdsButton(
              text: isRtl ? 'كبير (Large)' : 'Large',
              size: MdsButtonSize.lg,
              onPressed: () {},
            ),
            MdsButton(
              text: isRtl ? 'حالة التحميل' : 'Loading State',
              isLoading: _btnLoading,
              onPressed: () {
                setState(() => _btnLoading = !_btnLoading);
              },
            ),
          ],
        ),
      ],
    );
  }

  // 2. Inputs & Forms
  Widget _buildInputsTab(BuildContext context, bool isRtl) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        _buildSectionHeader(isRtl ? 'حقول الإدخال (Text Fields)' : 'Text Fields'),
        MdsTextField(
          label: isRtl ? 'البريد الإلكتروني' : 'Email Address',
          hintText: isRtl ? 'أدخل بريدك الإلكتروني' : 'Enter your email',
          prefixIcon: const Icon(Icons.email_outlined),
        ),
        const SizedBox(height: 16),
        MdsTextField(
          label: isRtl ? 'كلمة المرور' : 'Password',
          hintText: '••••••••',
          prefixIcon: const Icon(Icons.lock_outline),
          helperText: isRtl ? 'يجب ألا تقل عن 8 أحرف' : 'Must be at least 8 characters',
        ),
        const SizedBox(height: 16),
        MdsTextField(
          label: isRtl ? 'حقل به خطأ' : 'Field with Error',
          initialValue: 'invalid_data',
          errorText: isRtl ? 'القيمة المدخلة غير صحيحة' : 'Invalid input value provided',
        ),
        const SizedBox(height: 24),
        _buildSectionHeader(isRtl ? 'عناصر الاختيار (Selection Controls)' : 'Selection Controls'),
        MdsCheckbox(
          value: _checkboxVal,
          label: isRtl ? 'أوافق على الشروط والأحكام' : 'I agree to the terms and conditions',
          onChanged: (val) => setState(() => _checkboxVal = val ?? false),
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            MdsRadio<String>(
              value: 'opt1',
              groupValue: _radioVal,
              label: isRtl ? 'الخيار الأول' : 'Option 1',
              onChanged: (val) => setState(() => _radioVal = val!),
            ),
            const SizedBox(width: 24),
            MdsRadio<String>(
              value: 'opt2',
              groupValue: _radioVal,
              label: isRtl ? 'الخيار الثاني' : 'Option 2',
              onChanged: (val) => setState(() => _radioVal = val!),
            ),
          ],
        ),
        const SizedBox(height: 12),
        MdsSwitch(
          value: _switchVal,
          label: isRtl ? 'تفعيل الإشعارات الفورية' : 'Enable Push Notifications',
          onChanged: (val) => setState(() => _switchVal = val),
        ),
        const SizedBox(height: 16),
        _buildSectionHeader(isRtl ? 'القائمة المنسدلة (Dropdown)' : 'Dropdown Selection'),
        MdsDropdown<String>(
          label: isRtl ? 'اختر المدينة' : 'Select City',
          value: _dropdownVal,
          items: const [
            MdsDropdownItem(value: 'Cairo', label: 'القاهرة (Cairo)'),
            MdsDropdownItem(value: 'Alexandria', label: 'الإسكندرية (Alexandria)'),
            MdsDropdownItem(value: 'Giza', label: 'الجيزة (Giza)'),
            MdsDropdownItem(value: 'Mansoura', label: 'المنصورة (Mansoura)'),
          ],
          onChanged: (val) => setState(() => _dropdownVal = val),
        ),
      ],
    );
  }

  // 3. Cards & Alerts
  Widget _buildCardsAlertsTab(BuildContext context, bool isRtl) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        _buildSectionHeader(isRtl ? 'التنبيهات الدلالية (Semantic Alerts)' : 'Semantic Alerts'),
        MdsAlert(
          title: isRtl ? 'معلومات عامة' : 'Information',
          message: isRtl ? 'تم تحديث الديزاين سيستم إلى الإصدار v1.2.0 بنجاح.' : 'Design system updated to v1.2.0 successfully.',
          variant: MdsAlertVariant.info,
        ),
        const SizedBox(height: 12),
        MdsAlert(
          title: isRtl ? 'تم بنجاح' : 'Success',
          message: isRtl ? 'تم اعتماد كافة بوابات الإنتاج الـ 13 بنسبة 100%.' : 'All 13 production certification gates passed.',
          variant: MdsAlertVariant.success,
        ),
        const SizedBox(height: 12),
        MdsAlert(
          title: isRtl ? 'تنبيه' : 'Warning',
          message: isRtl ? 'يرجى مراجعة إعدادات التوثيق قبل النشر المباشر.' : 'Please verify configuration settings before deploy.',
          variant: MdsAlertVariant.warning,
        ),
        const SizedBox(height: 12),
        MdsAlert(
          title: isRtl ? 'خطأ' : 'Danger',
          message: isRtl ? 'فشل الاتصال بالخادم، يرجى إعادة المحاولة لاحقاً.' : 'Connection to server failed. Please retry.',
          variant: MdsAlertVariant.danger,
        ),
        const SizedBox(height: 24),
        _buildSectionHeader(isRtl ? 'الشارات (Badges / Tags)' : 'Badges & Tags'),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: [
            MdsBadge(label: isRtl ? 'مكتمل' : 'Completed', variant: MdsBadgeVariant.success),
            MdsBadge(label: isRtl ? 'قيد المراجعة' : 'In Review', variant: MdsBadgeVariant.info),
            MdsBadge(label: isRtl ? 'قيد التنفيذ' : 'In Progress', variant: MdsBadgeVariant.warning),
            MdsBadge(label: isRtl ? 'ملغي' : 'Canceled', variant: MdsBadgeVariant.error),
            MdsBadge(label: isRtl ? 'مسودة' : 'Draft', variant: MdsBadgeVariant.neutral),
          ],
        ),
        const SizedBox(height: 24),
        _buildSectionHeader(isRtl ? 'البطاقات (Cards)' : 'Cards'),
        MdsCard(
          title: Text(isRtl ? 'بطاقة تفاعلية' : 'Interactive Card'),
          subtitle: Text(isRtl ? 'عرض تفاصيل المكونات' : 'Displaying component details'),
          actions: [
            MdsButton(
              text: isRtl ? 'إلغاء' : 'Cancel',
              variant: MdsButtonVariant.outline,
              size: MdsButtonSize.sm,
              onPressed: () {},
            ),
            MdsButton(
              text: isRtl ? 'تأكيد' : 'Confirm',
              size: MdsButtonSize.sm,
              onPressed: () {},
            ),
          ],
          child: Text(
            isRtl
                ? 'هذه بطاقة مصممة وفق أحدث معايير Material 3 مع دعم الهوية البصرية لـ MDS والزوايا الناعمة 10px.'
                : 'This card is built using modern Material 3 tokens with soft 10px radii and curated elevations.',
          ),
        ),
      ],
    );
  }

  // 4. Modals & Feedback
  Widget _buildFeedbackTab(BuildContext context, bool isRtl) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        _buildSectionHeader(isRtl ? 'النوافذ المنبثقة (Dialog Modal)' : 'Dialog Modals'),
        MdsButton(
          text: isRtl ? 'فتح نافذة تأكيد (Dialog)' : 'Open Confirmation Dialog',
          onPressed: () {
            showDialog(
              context: context,
              builder: (dialogCtx) => MdsDialog(
                title: isRtl ? 'تأكيد العملية' : 'Confirm Action',
                content: Text(
                  isRtl
                      ? 'هل أنت متأكد من رغبتك في اعتماد هذا الإصدار؟ هذه العملية ستسجل في سجل الحوكمة.'
                      : 'Are you sure you want to approve this release? This will be recorded in governance logs.',
                ),
                actions: [
                  MdsButton(
                    text: isRtl ? 'إلغاء' : 'Cancel',
                    variant: MdsButtonVariant.outline,
                    onPressed: () => Navigator.pop(dialogCtx),
                  ),
                  MdsButton(
                    text: isRtl ? 'تأكيد الاعتماد' : 'Confirm',
                    onPressed: () => Navigator.pop(dialogCtx),
                  ),
                ],
              ),
            );
          },
        ),
        const SizedBox(height: 24),
        _buildSectionHeader(isRtl ? 'إشعارات التوست (Toasts / SnackBars)' : 'Floating Toasts'),
        Wrap(
          spacing: 12,
          runSpacing: 12,
          children: [
            MdsButton(
              text: isRtl ? 'توست نجاح' : 'Success Toast',
              variant: MdsButtonVariant.outline,
              onPressed: () => MdsToast.show(
                context: context,
                title: isRtl ? 'تم بنجاح' : 'Success',
                message: isRtl ? 'تم حفظ التغييرات بنجاح!' : 'Changes saved successfully!',
                variant: MdsToastVariant.success,
              ),
            ),
            MdsButton(
              text: isRtl ? 'توست تحذير' : 'Warning Toast',
              variant: MdsButtonVariant.outline,
              onPressed: () => MdsToast.show(
                context: context,
                title: isRtl ? 'تنبيه' : 'Warning',
                message: isRtl ? 'يرجى الانتباه إلى انتهاء الجلسة قريباً' : 'Session expiring soon',
                variant: MdsToastVariant.warning,
              ),
            ),
            MdsButton(
              text: isRtl ? 'توست خطأ' : 'Error Toast',
              variant: MdsButtonVariant.outline,
              onPressed: () => MdsToast.show(
                context: context,
                title: isRtl ? 'خطأ' : 'Error',
                message: isRtl ? 'حدث خطأ أثناء معالجة الطلب' : 'An error occurred during request',
                variant: MdsToastVariant.danger,
              ),
            ),
          ],
        ),
        const SizedBox(height: 24),
        _buildSectionHeader(isRtl ? 'التلميحات (Tooltips)' : 'Tooltips'),
        Center(
          child: MdsTooltip(
            message: isRtl ? 'هذا تلميح توضيحي مخصص للمكون' : 'This is a helpful contextual tooltip',
            child: Chip(
              avatar: const Icon(Icons.info_outline, size: 18),
              label: Text(isRtl ? 'المس مطولاً لرؤية التلميح' : 'Long-press to see tooltip'),
            ),
          ),
        ),
      ],
    );
  }

  // 5. Data & Navigation
  Widget _buildDataNavigationTab(BuildContext context, bool isRtl) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        _buildSectionHeader(isRtl ? 'الصور الشخصية والمجموعات (Avatars)' : 'Avatars & Groups'),
        Row(
          children: const [
            MdsAvatar(
              name: 'Mohamed Khalid',
              size: MdsAvatarSize.lg,
              status: MdsAvatarStatus.online,
            ),
            SizedBox(width: 16),
            MdsAvatar(
              name: 'Ahmed Ali',
              size: MdsAvatarSize.md,
              status: MdsAvatarStatus.busy,
            ),
            SizedBox(width: 16),
            MdsAvatarGroup(
              avatars: [
                MdsAvatar(name: 'Sarah Connor', size: MdsAvatarSize.md),
                MdsAvatar(name: 'John Doe', size: MdsAvatarSize.md),
                MdsAvatar(name: 'Tony Stark', size: MdsAvatarSize.md),
                MdsAvatar(name: 'Bruce Wayne', size: MdsAvatarSize.md),
                MdsAvatar(name: 'Peter Parker', size: MdsAvatarSize.md),
              ],
              maxCount: 3,
            ),
          ],
        ),
        const SizedBox(height: 24),
        _buildSectionHeader(isRtl ? 'الأكورديون القابل للطي (Accordion)' : 'Accordion Panels'),
        MdsAccordion(
          title: isRtl ? 'ما هي مواصفات Master Design System؟' : 'What are MDS specifications?',
          child: Text(
            isRtl
                ? 'نظام تصميم شامل يغطي الويب وفلاتر، مبني بمعايير W3C القياسية وبدون أي مكتبات NPM على الويب، ومتوافق 100% مع Material 3 والـ RTL.'
                : 'A comprehensive cross-platform design system spanning W3C Web standards and Flutter Material 3 with full native RTL.',
          ),
        ),
        const SizedBox(height: 12),
        MdsAccordion(
          title: isRtl ? 'كيف يتم التعامل مع الخطوط والتيبوغرافي؟' : 'How does MDS handle typography?',
          child: Text(
            isRtl
                ? 'التيبوغرافي مرن وديناميكي ويعتمد على TextTheme المشروع، مع دعم خط Cairo كخيار افتراضي متناسق متعدد اللغات.'
                : 'Typography is fully dynamic and driven by TextTheme, gracefully defaulting to Cairo for multilingual balance.',
          ),
        ),
        const SizedBox(height: 24),
        _buildSectionHeader(isRtl ? 'الجداول المنظمة (Data Table)' : 'Data Table'),
        MdsTable(
          columns: [
            MdsTableColumn(title: isRtl ? 'المكون' : 'Component'),
            MdsTableColumn(title: isRtl ? 'المنصة' : 'Platform'),
            MdsTableColumn(title: isRtl ? 'الحالة' : 'Status'),
          ],
          rows: [
            MdsTableRow(cells: [
              const Text('MdsButton'),
              const Text('Flutter & Web'),
              MdsBadge(label: isRtl ? 'معتمد' : 'Certified', variant: MdsBadgeVariant.success),
            ]),
            MdsTableRow(cells: [
              const Text('MdsTextField'),
              const Text('Flutter & Web'),
              MdsBadge(label: isRtl ? 'معتمد' : 'Certified', variant: MdsBadgeVariant.success),
            ]),
            MdsTableRow(cells: [
              const Text('MdsCard'),
              const Text('Flutter & Web'),
              MdsBadge(label: isRtl ? 'معتمد' : 'Certified', variant: MdsBadgeVariant.success),
            ]),
          ],
        ),
        const SizedBox(height: 24),
        MdsDivider(
          text: isRtl ? 'فاصل نصوص مخصص' : 'Custom Divider with Text',
        ),
      ],
    );
  }

  // 6. Loaders & Shimmer
  Widget _buildLoadersShimmerTab(BuildContext context, bool isRtl) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        _buildSectionHeader(isRtl ? 'مؤشرات التقدم (Progress Indicators)' : 'Progress Indicators'),
        MdsProgressIndicator.linear(
          value: _progressVal,
          label: isRtl ? 'اكتمال المعمارية' : 'Architecture Completion',
        ),
        const SizedBox(height: 16),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const MdsProgressIndicator.circular(),
            const SizedBox(width: 32),
            MdsProgressIndicator.circular(value: _progressVal),
          ],
        ),
        const SizedBox(height: 24),
        _buildSectionHeader(isRtl ? 'هياكل التحميل والشيمر (Skeleton Shimmer)' : 'Skeleton Shimmer'),
        Text(
          isRtl ? 'حركات شيمر أصلية ناعمة بدون مكتبات خارجية:' : 'Native sweep-gradient shimmers without external packages:',
          style: Theme.of(context).textTheme.bodySmall,
        ),
        const SizedBox(height: 12),
        const MdsSkeleton.card(),
        const SizedBox(height: 16),
        Row(
          children: [
            const MdsSkeleton.circle(size: 48),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: const [
                  MdsSkeleton.text(textLines: 1, width: 140),
                  SizedBox(height: 8),
                  MdsSkeleton.text(textLines: 1, width: 220),
                ],
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Text(
        title,
        style: Theme.of(context).textTheme.titleMedium?.copyWith(
              fontWeight: FontWeight.bold,
              color: MdsColors.actionPrimaryDefaultLight,
            ),
      ),
    );
  }
}
