#!/usr/bin/env python3
"""
MDS Visual Engine Unit Tests
Phase 9.7.7: Visual Regression Engine & Snapshot Diffing
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Validates the pure Python PNG codec, ITU-R BT.601 Luminance-Weighted RGB
Distance calculations, BaselineManager cryptographic hashing, and
manifest validation.
"""

import unittest
from pathlib import Path
import sys

TESTING_DIR = Path(__file__).resolve().parent.parent
if str(TESTING_DIR) not in sys.path:
    sys.path.insert(0, str(TESTING_DIR))

from visual.png_codec import decode_png, encode_png
from visual.visual_comparator import VisualComparator, DimensionMismatchError
from visual.baseline_manager import BaselineManager, BaselineIntegrityError
from visual.visual_models import VisualExecutionStatus


class TestVisualEngine(unittest.TestCase):
    """Unit tests for the zero-dependency pure Python visual regression core."""

    def setUp(self):
        self.comparator = VisualComparator(pixel_threshold=0.05, image_threshold=0.001)
        self.mgr = BaselineManager(workspace_root=TESTING_DIR.parent.parent)

    # 1. PNG Codec Tests
    def test_01_png_codec_roundtrip(self):
        """Verifies lossless encoding and decoding of synthetic 32-bit RGBA buffers."""
        width, height = 8, 8
        buffer = bytearray(width * height * 4)
        for i in range(0, len(buffer), 4):
            buffer[i] = (i * 7) % 256      # R
            buffer[i + 1] = (i * 13) % 256  # G
            buffer[i + 2] = (i * 19) % 256  # B
            buffer[i + 3] = 255            # A

        encoded_png = encode_png(width, height, buffer)
        self.assertTrue(encoded_png.startswith(b"\x89PNG\r\n\x1a\n"))

        dw, dh, decoded_buf = decode_png(encoded_png)
        self.assertEqual(dw, width)
        self.assertEqual(dh, height)
        self.assertEqual(decoded_buf, buffer)

    def test_02_png_codec_invalid_signature(self):
        """Verifies that decode_png raises ValueError on invalid signatures."""
        with self.assertRaises(ValueError):
            decode_png(b"NOT_A_PNG_FILE_DATA")

    # 2. Color Distance Math Tests
    def test_03_luminance_weighted_distance_identical_pixels(self):
        """Identical pixels must have exactly 0.0 distance."""
        dist = VisualComparator.calculate_pixel_distance(100, 150, 200, 255, 100, 150, 200, 255)
        self.assertEqual(dist, 0.0)

    def test_04_luminance_weighted_distance_green_vs_blue_sensitivity(self):
        """
        Human perception is more sensitive to green (0.587) than blue (0.114).
        A 50-value shift in green must yield a higher distance than a 50-value shift in blue.
        """
        dist_green = VisualComparator.calculate_pixel_distance(128, 100, 128, 255, 128, 150, 128, 255)
        dist_blue = VisualComparator.calculate_pixel_distance(128, 128, 100, 255, 128, 128, 150, 255)

        self.assertGreater(dist_green, dist_blue)
        self.assertAlmostEqual(dist_green, (0.587 ** 0.5 * 50) / 255.0, places=4)
        self.assertAlmostEqual(dist_blue, (0.114 ** 0.5 * 50) / 255.0, places=4)

    def test_05_luminance_weighted_distance_alpha_channel(self):
        """Verifies that alpha channel variance is correctly accounted for."""
        dist = VisualComparator.calculate_pixel_distance(100, 100, 100, 255, 100, 100, 100, 0)
        self.assertEqual(dist, 1.0)

    # 3. Comparator Evaluation Tests
    def test_06_comparator_identical_images_pass(self):
        """Comparing identical images yields PASS and 0.0 diff ratio."""
        w, h = 10, 10
        buf = bytearray([50, 100, 150, 255] * (w * h))
        png = encode_png(w, h, buf)

        res = self.comparator.evaluate(png, png, baseline_id="TEST-001")
        self.assertEqual(res.status, VisualExecutionStatus.PASS)
        self.assertEqual(res.metrics.diff_ratio, 0.0)
        self.assertEqual(res.metrics.mismatched_pixels, 0)

    def test_07_comparator_dimension_mismatch_fails(self):
        """Comparing different sized images reports failure with clear diagnostic."""
        png_a = encode_png(10, 10, bytearray([0, 0, 0, 255] * 100))
        png_b = encode_png(10, 20, bytearray([0, 0, 0, 255] * 200))

        res = self.comparator.evaluate(png_a, png_b, baseline_id="TEST-002")
        self.assertEqual(res.status, VisualExecutionStatus.FAIL)
        self.assertIn("dimensions do not match", res.error_message)

    # 4. Baseline Manager & Font Pinning Tests
    def test_08_font_artifacts_verification(self):
        """Verifies that canonical Cairo font artifacts are present with genuine SHA-256 hashes."""
        is_valid, msg, telemetry = self.mgr.verify_fonts()
        self.assertTrue(is_valid, f"Font verification failed: {msg}")
        self.assertIn("regular", telemetry)
        self.assertIn("bold", telemetry)
        self.assertEqual(
            telemetry["regular"]["sha256"],
            "44786a38e27c58262cbd65341beda4fa4f6c7085ec42e830b35ba1ae37807030"
        )
        self.assertEqual(
            telemetry["bold"]["sha256"],
            "a0e58d71b85b15902ea87914d8e31a6d22da48ac2db70213dcfd1a7dad3f198a"
        )

    def test_09_manifest_12_canonical_baselines(self):
        """Verifies that baselines_manifest.json contains exactly the 12 approved baselines."""
        manifest = self.mgr.load_manifest()
        baselines = manifest.get("baselines", [])
        self.assertEqual(len(baselines), 12)
        baseline_ids = [b["baseline_id"] for b in baselines]
        self.assertEqual(baseline_ids, self.mgr.CANONICAL_BASELINE_IDS)

        # Verify all 12 baselines have real SHA-256 hashes recorded
        for b in baselines:
            self.assertIsNotNone(b.get("file_sha256"))
            self.assertEqual(len(b["file_sha256"]), 64)
            self.assertGreater(b.get("file_size_bytes", 0), 1000)

    def test_10_immutable_baseline_write_guard(self):
        """Verifies that saving baselines raises PermissionError when allow_write is False."""
        with self.assertRaises(PermissionError):
            self.mgr.save_baseline_image("VIS-BASE-001", b"dummy", allow_write=False)


if __name__ == "__main__":
    unittest.main()
