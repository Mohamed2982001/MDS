"""
Master Design System (MDS) — Flutter Token Engine Unit Tests
Phase 11: Multi-Platform Flutter Token Engine & Package
Layer 10: Testing & Verification
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.tokens.transpile_flutter import FlutterTokenTranspiler, hex_to_flutter_color, normalize_newlines


class TestFlutterTokenTranspiler(unittest.TestCase):
    """Unit test suite for tools/tokens/transpile_flutter.py."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.workspace_root = Path(__file__).resolve().parent.parent.parent
        cls.tokens_dir = cls.workspace_root / "MDS" / "00-Tokens"
        cls.package_dir = cls.workspace_root / "packages" / "mds_flutter_tokens"
        cls.cli_path = cls.workspace_root / "tools" / "tokens" / "transpile_flutter.py"

    def test_hex_to_flutter_color(self) -> None:
        """Verifies hex string to Flutter Color integer formatting."""
        self.assertEqual(hex_to_flutter_color("#2563EB"), "Color(0xFF2563EB)")
        self.assertEqual(hex_to_flutter_color("#FFFFFF"), "Color(0xFFFFFFFF)")
        self.assertEqual(hex_to_flutter_color("#000"), "Color(0xFF000000)")
        self.assertEqual(hex_to_flutter_color("#334155"), "Color(0xFF334155)")
        with self.assertRaises(ValueError):
            hex_to_flutter_color("invalid_hex")

    def test_load_tokens_success(self) -> None:
        """Verifies parsing of all 6 canonical JSON token specifications."""
        transpiler = FlutterTokenTranspiler(self.workspace_root, self.tokens_dir)
        transpiler.load_tokens()

        self.assertIn("colors", transpiler.tokens)
        self.assertIn("typography", transpiler.tokens)
        self.assertIn("spacing", transpiler.tokens)
        self.assertIn("radius", transpiler.tokens)
        self.assertIn("elevation", transpiler.tokens)
        self.assertIn("motion", transpiler.tokens)

        # Value inspection
        colors = transpiler.tokens["colors"]
        self.assertEqual(colors["palettes"]["brand"]["600"], "#2563EB")
        self.assertEqual(colors["palettes"]["neutral"]["0"], "#FFFFFF")

        typo = transpiler.tokens["typography"]
        self.assertEqual(typo["font_families"]["primary"], "Cairo")
        self.assertEqual(typo["weights"]["bold"], 700)

        radius = transpiler.tokens["radius"]
        self.assertEqual(radius["scale"]["md"], 10.0)

    def test_load_tokens_missing_file_raises_error(self) -> None:
        """Verifies that missing token files raise FileNotFoundError."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            empty_tokens_dir = Path(tmp_dir)
            transpiler = FlutterTokenTranspiler(self.workspace_root, empty_tokens_dir)
            with self.assertRaises(FileNotFoundError):
                transpiler.load_tokens()

    def test_generate_all_files_dictionary(self) -> None:
        """Verifies in-memory file dictionary generation."""
        transpiler = FlutterTokenTranspiler(self.workspace_root, self.tokens_dir)
        files = transpiler.generate_all_files()

        expected_files = {
            "pubspec.yaml",
            "README.md",
            "LICENSE",
            "analysis_options.yaml",
            "lib/mds_flutter_tokens.dart",
            "lib/src/colors.dart",
            "lib/src/typography.dart",
            "lib/src/spacing.dart",
            "lib/src/radius.dart",
            "lib/src/elevation.dart",
            "lib/src/motion.dart",
            "lib/src/theme.dart",
            "test/mds_flutter_tokens_test.dart",
        }
        self.assertEqual(set(files.keys()), expected_files)

        # File content assertions
        for path, content in files.items():
            self.assertTrue(len(content) > 50, f"File {path} is suspiciously short")
            if path.endswith(".dart"):
                self.assertIn("// GENERATED CODE - DO NOT MODIFY BY HAND", content)

        # Domain specifics
        self.assertIn("Color(0xFF2563EB)", files["lib/src/colors.dart"])
        self.assertIn("Cairo", files["lib/src/typography.dart"])
        self.assertIn("MdsSpacing", files["lib/src/spacing.dart"])
        self.assertIn("MdsRadius", files["lib/src/radius.dart"])
        self.assertIn("useMaterial3: true", files["lib/src/theme.dart"])

    def test_verify_synchronization_on_disk(self) -> None:
        """Verifies that current disk package is in 100% sync with in-memory generation."""
        transpiler = FlutterTokenTranspiler(self.workspace_root, self.tokens_dir)
        is_synced, diffs = transpiler.verify_synchronization(self.package_dir)
        self.assertTrue(is_synced, f"Disk out of sync: {diffs}")
        self.assertEqual(len(diffs), 0)

    def test_verify_drift_detection(self) -> None:
        """Verifies that tampering with a generated file triggers synchronization failure."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_pkg_dir = Path(tmp_dir) / "pkg"
            transpiler = FlutterTokenTranspiler(self.workspace_root, self.tokens_dir)
            transpiler.write_to_disk(temp_pkg_dir)

            # Initially synced
            synced, diffs = transpiler.verify_synchronization(temp_pkg_dir)
            self.assertTrue(synced)
            self.assertEqual(len(diffs), 0)

            # Tamper with colors.dart
            colors_file = temp_pkg_dir / "lib" / "src" / "colors.dart"
            tampered_content = colors_file.read_text(encoding="utf-8") + "\n// TAMPERED LINE\n"
            colors_file.write_text(tampered_content, encoding="utf-8")

            # Must detect mismatch
            synced, diffs = transpiler.verify_synchronization(temp_pkg_dir)
            self.assertFalse(synced)
            self.assertTrue(any("CONTENT MISMATCH" in d and "colors.dart" in d for d in diffs))

            # Missing file detection
            colors_file.unlink()
            synced, diffs = transpiler.verify_synchronization(temp_pkg_dir)
            self.assertFalse(synced)
            self.assertTrue(any("MISSING FILE" in d and "colors.dart" in d for d in diffs))

    def test_cli_verify_exit_code_zero(self) -> None:
        """Verifies that python tools/tokens/transpile_flutter.py --verify exits with code 0."""
        cmd = [sys.executable, str(self.cli_path), "--verify"]
        res = subprocess.run(cmd, cwd=str(self.workspace_root), capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"CLI --verify failed: {res.stderr}\n{res.stdout}")
        self.assertIn("SYNCHRONIZED", res.stdout)

    def test_cli_json_output(self) -> None:
        """Verifies that --json outputs parseable JSON metadata."""
        cmd = [sys.executable, str(self.cli_path), "--verify", "--json"]
        res = subprocess.run(cmd, cwd=str(self.workspace_root), capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout.strip())
        self.assertEqual(data.get("status"), "PASS")
        self.assertTrue(data.get("synced"))


if __name__ == "__main__":
    unittest.main()
