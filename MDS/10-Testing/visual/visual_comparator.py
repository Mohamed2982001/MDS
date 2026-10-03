#!/usr/bin/env python3
"""
MDS Visual Comparator & Luminance-Weighted RGB Distance Engine
Phase 9.7.7: Visual Regression Engine & Snapshot Diffing
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Implements mathematically rigorous pixel-diff comparison using
Luminance-Weighted RGB Distance (D_lum) based on ITU-R BT.601 coefficients,
alpha variance evaluation, configurable tolerance thresholds,
and highlighted diff mask generation.
"""

import math
import time
from typing import Tuple, Optional
from pathlib import Path

from .visual_models import (
    ComparisonMetrics,
    ComparisonResult,
    VisualExecutionStatus
)
from .png_codec import decode_png, encode_png


class DimensionMismatchError(ValueError):
    """Raised when actual and baseline image dimensions do not match."""
    pass


class VisualComparator:
    """
    Performs deterministic pixel-by-pixel visual comparison between
    a live raster capture and a golden baseline master.
    """

    # ITU-R BT.601 Luminance coefficients
    COEFF_R = 0.299
    COEFF_G = 0.587
    COEFF_B = 0.114

    DEFAULT_PIXEL_THRESHOLD = 0.05   # tau_pixel (5% perceptual color distance)
    DEFAULT_IMAGE_THRESHOLD = 0.001  # tau_image (0.1% aggregate pixel diff ratio)

    def __init__(
        self,
        pixel_threshold: float = DEFAULT_PIXEL_THRESHOLD,
        image_threshold: float = DEFAULT_IMAGE_THRESHOLD
    ):
        self.pixel_threshold = pixel_threshold
        self.image_threshold = image_threshold

    @classmethod
    def calculate_pixel_distance(
        cls,
        r1: int, g1: int, b1: int, a1: int,
        r2: int, g2: int, b2: int, a2: int
    ) -> float:
        """
        Calculates Luminance-Weighted RGB Distance (D_lum) and composite pixel distance:
        D_lum = sqrt(0.299*(R1-R2)^2 + 0.587*(G1-G2)^2 + 0.114*(B1-B2)^2) / 255.0
        Delta_A = |A1 - A2| / 255.0
        D_pixel = max(D_lum, Delta_A)
        """
        dr = r1 - r2
        dg = g1 - g2
        db = b1 - b2
        d_lum_sq = (cls.COEFF_R * dr * dr) + (cls.COEFF_G * dg * dg) + (cls.COEFF_B * db * db)
        d_lum = math.sqrt(d_lum_sq) / 255.0
        delta_a = abs(a1 - a2) / 255.0
        return max(d_lum, delta_a)

    def compare_buffers(
        self,
        width: int,
        height: int,
        baseline_buf: bytearray,
        actual_buf: bytearray,
        baseline_id: str = "UNKNOWN"
    ) -> Tuple[ComparisonMetrics, bytearray]:
        """
        Compares two raw RGBA bytearrays of identical dimensions.
        Returns (ComparisonMetrics, diff_mask_rgba_bytearray).
        """
        start_time = time.perf_counter()
        total_pixels = width * height
        mismatched_count = 0
        diff_mask = bytearray(total_pixels * 4)

        tau_pix = self.pixel_threshold

        for idx in range(0, total_pixels * 4, 4):
            r1, g1, b1, a1 = baseline_buf[idx], baseline_buf[idx + 1], baseline_buf[idx + 2], baseline_buf[idx + 3]
            r2, g2, b2, a2 = actual_buf[idx], actual_buf[idx + 1], actual_buf[idx + 2], actual_buf[idx + 3]

            dist = self.calculate_pixel_distance(r1, g1, b1, a1, r2, g2, b2, a2)

            if dist > tau_pix:
                mismatched_count += 1
                # Fluorescent Magenta for mismatched pixels: (255, 0, 255, 255)
                diff_mask[idx] = 255
                diff_mask[idx + 1] = 0
                diff_mask[idx + 2] = 255
                diff_mask[idx + 3] = 255
            else:
                # Dimmed original baseline context (20% opacity on grayscale luminance)
                lum = int(self.COEFF_R * r1 + self.COEFF_G * g1 + self.COEFF_B * b1)
                dimmed = int(lum * 0.2) + 200
                diff_mask[idx] = min(dimmed, 255)
                diff_mask[idx + 1] = min(dimmed, 255)
                diff_mask[idx + 2] = min(dimmed, 255)
                diff_mask[idx + 3] = 255

        duration_ms = (time.perf_counter() - start_time) * 1000.0
        diff_ratio = mismatched_count / float(total_pixels) if total_pixels > 0 else 0.0

        metrics = ComparisonMetrics(
            total_pixels=total_pixels,
            mismatched_pixels=mismatched_count,
            diff_ratio=diff_ratio,
            pixel_threshold=self.pixel_threshold,
            image_threshold=self.image_threshold,
            duration_ms=duration_ms,
            width=width,
            height=height
        )

        return metrics, diff_mask

    def compare_png_bytes(
        self,
        baseline_png: bytes,
        actual_png: bytes,
        baseline_id: str = "UNKNOWN"
    ) -> Tuple[ComparisonMetrics, bytes]:
        """
        Decodes baseline and actual PNG bytes, compares buffers, and returns
        (ComparisonMetrics, diff_mask_png_bytes).
        """
        bw, bh, b_buf = decode_png(baseline_png)
        aw, ah, a_buf = decode_png(actual_png)

        if (bw, bh) != (aw, ah):
            raise DimensionMismatchError(
                f"Image dimensions do not match: baseline is {bw}x{bh}, actual capture is {aw}x{ah}."
            )

        metrics, diff_buf = self.compare_buffers(bw, bh, b_buf, a_buf, baseline_id=baseline_id)
        diff_png = encode_png(bw, bh, diff_buf)
        return metrics, diff_png

    def evaluate(
        self,
        baseline_png: bytes,
        actual_png: bytes,
        baseline_id: str = "UNKNOWN",
        output_diff_path: Optional[Path] = None
    ) -> ComparisonResult:
        """
        Full evaluation workflow: compares images, determines PASS/FAIL verdict,
        and optionally writes out the diff mask PNG.
        """
        try:
            metrics, diff_png = self.compare_png_bytes(baseline_png, actual_png, baseline_id)
        except DimensionMismatchError as dme:
            return ComparisonResult(
                baseline_id=baseline_id,
                status=VisualExecutionStatus.FAIL,
                metrics=ComparisonMetrics(),
                error_message=str(dme)
            )
        except Exception as e:
            return ComparisonResult(
                baseline_id=baseline_id,
                status=VisualExecutionStatus.ERROR,
                metrics=ComparisonMetrics(),
                error_message=f"Comparison failed: {e}"
            )

        if output_diff_path and metrics.diff_ratio > self.image_threshold:
            output_diff_path.parent.mkdir(parents=True, exist_ok=True)
            output_diff_path.write_bytes(diff_png)

        verdict = (
            VisualExecutionStatus.PASS
            if metrics.diff_ratio <= self.image_threshold
            else VisualExecutionStatus.FAIL
        )

        return ComparisonResult(
            baseline_id=baseline_id,
            status=verdict,
            metrics=metrics,
            diff_image_path=output_diff_path if (output_diff_path and verdict == VisualExecutionStatus.FAIL) else None,
            evidence={
                "diff_ratio": metrics.diff_ratio,
                "diff_percent": round(metrics.diff_ratio * 100, 4),
                "mismatched_pixels": metrics.mismatched_pixels,
                "duration_ms": metrics.duration_ms
            }
        )
