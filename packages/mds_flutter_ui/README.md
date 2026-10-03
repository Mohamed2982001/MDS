# Master Design System (MDS) — Flutter Component Library (`mds_flutter_ui`)

Production Flutter UI Component Library implementing the 19 standard MDS design system components.

**Lead Architect & Project Owner:** Mohamed Khalid (Senior Full Stack & Flutter Developer)

---

## 📦 Features

- **19 Canonical Components:** Button, TextField, Badge, Card, Alert, Dialog, Toast, Checkbox, Radio, Switch, Dropdown, Avatar, Progress, Tooltip, Divider, Tabs, Table, Accordion, Skeleton.
- **Token-Grounded:** Consumes design tokens directly from `mds_flutter_tokens`.
- **RTL & Bidirectionality Native:** Complete Arabic (RTL) and English (LTR) support using directional properties (`EdgeInsetsDirectional`, `BorderRadiusDirectional`, `AlignmentDirectional`).
- **Flexible Typography:** Driven by the active theme's `TextTheme` (Cairo default), fully customizable without rigid hardcoding.
- **Sound Null Safety & Dart 3+:** Records, pattern matching, sealed states, and `const` constructors.
- **Zero Ellipsis Truncation:** Allows `softWrap: true` on descriptive text for natural multi-line layout.
- **Genuine Shimmer Animations:** Built-in animated micro-interactions and skeleton loaders without third-party bloat.

---

## 🚀 Quick Start

```dart
import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';
import 'package:mds_flutter_ui/mds_flutter_ui.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: MdsThemeData.light(),
      darkTheme: MdsThemeData.dark(),
      home: Directionality(
        textDirection: TextDirection.rtl, // Fully Arabic / RTL Native
        child: Scaffold(
          body: Center(
            child: MdsButton(
              text: 'حفظ التغييرات',
              variant: MdsButtonVariant.primary,
              size: MdsButtonSize.md,
              onPressed: () {},
            ),
          ),
        ),
      ),
    );
  }
}
```

---

## 🧩 The 19 Canonical Components Catalog

| # | Component | Class Name | Key Features |
|---|---|---|---|
| 1 | **Button** | `MdsButton` | 5 variants (`primary`, `secondary`, `outline`, `ghost`, `danger`), 3 sizes (`sm`, `md`, `lg`), loading spinner, press effect |
| 2 | **Input** | `MdsTextField` | Floating label, hint, helper text, error text, prefix/suffix icons, clear button, focus ring |
| 3 | **Badge** | `MdsBadge` | 6 semantic variants, 3 styles (`subtle`, `filled`, `outline`), pill/square geometry, delete action |
| 4 | **Card** | `MdsCard` | 3 variants (`elevated`, `outlined`, `filled`), structured slots: header, title, subtitle, leading, trailing, body, footer, actions |
| 5 | **Alert** | `MdsAlert` | 4 semantic variants (`info`, `success`, `warning`, `danger`), animated dismiss, custom action slot |
| 6 | **Dialog** | `MdsDialog` | Header, scrollable content area, action buttons, `MdsDialog.show` modal helper |
| 7 | **Toast** | `MdsToast` | Floating snackbars with semantic status styling (`showSuccess`, `showError`, `showWarning`, `showInfo`) |
| 8 | **Checkbox** | `MdsCheckbox` | Checked, unchecked, and tristate indeterminate, label, description, error feedback |
| 9 | **Radio** | `MdsRadio<T>` | Group value management, smooth animated concentric circle, directional label |
| 10 | **Switch** | `MdsSwitch` | Sliding thumb micro-animation, active/inactive color states, label position |
| 11 | **Select / Dropdown** | `MdsDropdown<T>` | Accessible overlay popup, searchable items filter, clearable selection, keyboard navigable |
| 12 | **Avatar** | `MdsAvatar` | Network/asset images with automatic fallback initials (e.g. "Mohamed Khalid" -> "MK"), presence status dot, `MdsAvatarGroup` |
| 13 | **Progress Indicator** | `MdsProgressIndicator` | Determinate & indeterminate linear bars (`MdsLinearProgress`) and circular spinners (`MdsCircularProgress`) with percentage |
| 14 | **Tooltip** | `MdsTooltip` | Styled popup bubble, 3 variants (`dark`, `light`, `primary`), directional placement, mobile touch-hold trigger |
| 15 | **Divider** | `MdsDivider` | Horizontal and vertical variants, directional start/center/end embedded label or chip |
| 16 | **Tabs** | `MdsTabs` | Underline and pill variants, smooth indicator animation, badge & icon support, scrollable/expanded distribution |
| 17 | **Table** | `MdsTable` | Structured columns and rows, alternating row stripes, column sorting, responsive horizontal scroll |
| 18 | **Accordion** | `MdsAccordion` | Collapsible panel with animated rotating chevron, size transition, single or grouped (`MdsAccordionGroup`) |
| 19 | **Skeleton / Shimmer** | `MdsSkeleton` | Animated sweep gradient shimmer with factory constructors (`rect`, `circle`, `text`, `card`) |

---

## 🔒 Verification & Compliance

- `dart analyze`: **0 warnings, 0 lints, 0 errors**
- `flutter test`: **28/28 tests passing (100%)**
- `mds_flutter_tokens`: **17/17 tests passing (100%)**
- Cryptographic Distribution Gate: **Exit 0 (33 verified distribution files intact)**
- Production Certificate: **Valid & Sealed (`MDS-CERT-v1.0.0-426b8bf473112cf5`)**
