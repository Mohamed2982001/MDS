# Master Design System (MDS) — Flutter Tokens Package

Official Flutter design token package for the **Master Design System (MDS)**.

**Lead Architect & Project Owner:** Mohamed Khalid (Senior Full Stack & Flutter Developer)

## 📦 Features
- **Strictly Typed Tokens:** Colors, Typography, Spacing, Radius, Elevation, Motion.
- **Cairo Typography:** Default typography using Cairo font across all 15 M3 text styles.
- **Material 3 Themes:** Production-ready `MdsThemeData.light()` and `MdsThemeData.dark()`.
- **RTL & Bidirectional Safe:** Directional padding and radius helpers with zero hardcoded left/right values.
- **Theme Extension:** Strongly typed `MdsSemanticColors` accessible via `context.mdsColors`.

## 🚀 Usage

```dart
import 'package:flutter/material.dart';
import 'package:mds_flutter_tokens/mds_flutter_tokens.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MDS Flutter App',
      theme: MdsThemeData.light(),
      darkTheme: MdsThemeData.dark(),
      home: const Scaffold(
        body: Center(
          child: Text('Hello Cairo MDS!'),
        ),
      ),
    );
  }
}
```
