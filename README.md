# 🏛️ Master Design System (MDS)

[![MDS Certification](https://img.shields.io/badge/MDS_Certification-v1.0.0_CERTIFIED-2563EB.svg)](evidence/certification/MDS_v1.0.0_PRODUCTION_CERTIFICATE.json)
[![Platform: Web & Flutter](https://img.shields.io/badge/Platform-Web%20%7C%20Flutter-059669.svg)](#)
[![Zero-NPM](https://img.shields.io/badge/Zero--NPM-100%25%20Pure%20W3C-7C3AED.svg)](#)
[![Dart 3](https://img.shields.io/badge/Dart-3.x%20Sound%20Null--Safe-0284C7.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-gray.svg)](LICENSE)

An enterprise-grade, deterministic, zero-dependency design system engine spanning **Pure W3C Standards for Web** and **Material 3 for Flutter/Dart Mobile**. 

Architected and developed by **Mohamed Khalid** (Senior Full Stack & Flutter Developer).

---

## 🌟 Key Architecture Pillars

- **Zero-NPM Web Runtime:** 100% pure W3C standards (CSS custom properties, native Web Components, standard ECMAScript modules) without Node.js runtime dependencies.
- **Multi-Platform Token Transpiler:** Automated Python 3.12 stdlib engine translating JSON tokens into idiomatic Dart packages and CSS bundles.
- **Arabic / RTL Native:** Directional geometry (`EdgeInsetsDirectional`, `BorderRadiusDirectional`) with zero hardcoded `left`/`right`.
- **Flexible & Adaptive Typography:** Configurable across all components, defaulting cleanly to Google Fonts Cairo.
- **Cryptographic Certification:** Fully automated 13-gate certification engine verifying bit-for-bit build reproducibility, security invariants, accessibility, and artifact trust chains.

---

## 📦 Repository Structure

```text
├── MDS/                                   # Canonical Specification & Baselines (Layers 00–13)
│   ├── 00-Tokens/                         # Source JSON Design Tokens (colors, spacing, etc.)
│   ├── 10-Testing/                        # Automated Master Verification Suites (136 tests)
│   ├── 12-Governance/                     # Trust Anchors & Governance Manifests
│   ├── 13-Implementation/                 # Architecture Specs & Implementation Reports
│   └── Runtime/                           # Pure W3C Web Runtime Sources
├── packages/
│   ├── mds_flutter_tokens/                # Standalone Dart package for Design Tokens & M3 Theme
│   └── mds_flutter_ui/                    # Standalone Flutter UI Library (19 Canonical Components)
├── dist/                                  # Certified Web Release Distribution (35 Files)
│   ├── bundles/                           # Monolithic CSS & JS ESM Bundles
│   ├── css/                               # Modular per-component CSS stylesheets
│   └── components/                        # W3C Custom Elements definitions
├── tools/
│   ├── compiler/                          # Deterministic Python compiler & packager
│   ├── certification/                     # 13-Gate Production Certification CLI & Engine
│   └── tokens/                            # Flutter Multi-Platform Token Transpiler
└── evidence/certification/                # Production Certificate, Evidence Manifest & Seal
```

---

## 🚀 Quickstart

### 1. Flutter Mobile Development

Add dependencies to your Flutter `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  mds_flutter_tokens:
    path: path/to/Master Design System/packages/mds_flutter_tokens
  mds_flutter_ui:
    path: path/to/Master Design System/packages/mds_flutter_ui
```

In your application root:

```dart
import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';
import 'package:mds_flutter_ui/mds_flutter_ui.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MDS Application',
      theme: MdsThemeData.light(),
      darkTheme: MdsThemeData.dark(),
      home: Scaffold(
        appBar: AppBar(title: const Text('Master Design System')),
        body: Center(
          child: MdsButton.primary(
            label: 'تسجيل الدخول',
            onPressed: () {},
          ),
        ),
      ),
    );
  }
}
```

### 2. Web Applications (HTML / React / Next.js)

Import the certified bundles directly from `dist/`:

```html
<!-- Monolithic Stylesheet -->
<link rel="stylesheet" href="dist/bundles/mds.all.css">

<!-- Native ECMAScript Web Components -->
<script type="module" src="dist/bundles/mds.all.esm.js"></script>

<!-- Use anywhere in HTML -->
<mds-button variant="primary">Click Me</mds-button>
```

---

## 🧩 The 19 Canonical UI Components

| # | Component | Flutter Widget (`mds_flutter_ui`) | Web Component (`dist/`) |
|---|---|---|---|
| 1 | **Button** | `MdsButton` | `<mds-button>` |
| 2 | **Input** | `MdsTextField` | `<mds-input>` |
| 3 | **Badge** | `MdsBadge` | `<mds-badge>` |
| 4 | **Card** | `MdsCard` | `<mds-card>` |
| 5 | **Alert** | `MdsAlert` | `<mds-alert>` |
| 6 | **Dialog** | `MdsDialog` | `<mds-dialog>` |
| 7 | **Toast** | `MdsToast` | `<mds-toast>` |
| 8 | **Checkbox** | `MdsCheckbox` | `<mds-checkbox>` |
| 9 | **Radio** | `MdsRadio` | `<mds-radio>` |
| 10 | **Switch** | `MdsSwitch` | `<mds-switch>` |
| 11 | **Dropdown** | `MdsDropdown` | `<mds-dropdown>` |
| 12 | **Avatar** | `MdsAvatar`, `MdsAvatarGroup` | `<mds-avatar>` |
| 13 | **Progress** | `MdsProgressIndicator` | `<mds-progress>` |
| 14 | **Tooltip** | `MdsTooltip` | `<mds-tooltip>` |
| 15 | **Divider** | `MdsDivider` | `<mds-divider>` |
| 16 | **Tabs** | `MdsTabs` | `<mds-tabs>` |
| 17 | **Table** | `MdsTable` | `<mds-table>` |
| 18 | **Accordion** | `MdsAccordion` | `<mds-accordion>` |
| 19 | **Skeleton** | `MdsSkeleton`, `MdsShimmer` | `<mds-skeleton>` |

---

## 🔒 Verification & Quality Gates

Run any verification command directly:

```powershell
# 1. Verify Distribution Package (35 files, 0 extra files)
python tools/compiler/cli.py verify --dist dist

# 2. Verify Production Certificate & Trust Seal
python tools/certification/cli.py verify-certificate

# 3. Verify Token Transpiler Synchronization
python tools/tokens/transpile_flutter.py --verify

# 4. Run Flutter Package Analysis & Tests
cd packages/mds_flutter_tokens && flutter test
cd ../mds_flutter_ui && flutter test

# 5. Run Python Master Verification Suite (136 tests)
python -m unittest discover -s MDS/10-Testing -p "test_*.py"
```

---

## 📜 License

MIT License. Designed and maintained by Mohamed Khalid.
