#!/usr/bin/env python3
"""
MDS Pure Python Standard Library PNG Codec
Phase 9.7.7: Visual Regression Engine & Snapshot Diffing
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Provides pure Python decoding of PNG images into 32-bit RGBA buffers
and encoding of RGBA buffers into standard PNGs using strictly Python's
built-in `zlib` and `struct` modules (zero third-party dependencies).
"""

import struct
import zlib
from typing import Tuple


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def decode_png(png_bytes: bytes) -> Tuple[int, int, bytearray]:
    """
    Decodes a PNG byte sequence into (width, height, rgba_buffer).
    Returns rgba_buffer as a flat bytearray of size width * height * 4.
    Supports standard 8-bit truecolor (RGB) and truecolor with alpha (RGBA).
    """
    if not png_bytes.startswith(PNG_SIGNATURE):
        raise ValueError("Invalid PNG signature: input is not a valid PNG file.")

    offset = 8
    width = 0
    height = 0
    bit_depth = 0
    color_type = 0
    interlace_method = 0
    idat_chunks = []

    while offset < len(png_bytes):
        if offset + 8 > len(png_bytes):
            break
        length, chunk_type = struct.unpack(">I4s", png_bytes[offset:offset + 8])
        offset += 8
        chunk_data = png_bytes[offset:offset + length]
        offset += length
        crc = struct.unpack(">I", png_bytes[offset:offset + 4])[0]
        offset += 4

        # Verify CRC32
        expected_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if crc != expected_crc:
            raise ValueError(f"Corrupted PNG chunk {chunk_type.decode('latin1', 'replace')}: CRC mismatch.")

        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type, comp, filt, interlace_method = struct.unpack(
                ">IIBBBBB", chunk_data
            )
            if bit_depth != 8:
                raise ValueError(f"Unsupported PNG bit depth: {bit_depth} (expected 8-bit).")
            if color_type not in (2, 6):
                raise ValueError(f"Unsupported PNG color type: {color_type} (expected 2:RGB or 6:RGBA).")
            if interlace_method != 0:
                raise ValueError("Interlaced PNGs are not supported.")
        elif chunk_type == b"IDAT":
            idat_chunks.append(chunk_data)
        elif chunk_type == b"IEND":
            break

    if width <= 0 or height <= 0 or not idat_chunks:
        raise ValueError("Invalid or incomplete PNG structure: missing IHDR or IDAT chunks.")

    raw_decompressed = zlib.decompress(b"".join(idat_chunks))
    bpp = 4 if color_type == 6 else 3
    stride = width * bpp
    expected_len = height * (1 + stride)

    if len(raw_decompressed) < expected_len:
        raise ValueError(
            f"Decompressed IDAT size mismatch: expected {expected_len} bytes, got {len(raw_decompressed)}"
        )

    # Scanline unfiltering
    rgba_buffer = bytearray(width * height * 4)
    prior_line = bytearray(stride)
    curr_line = bytearray(stride)
    src_idx = 0
    dst_idx = 0

    for y in range(height):
        filter_type = raw_decompressed[src_idx]
        src_idx += 1
        raw_scanline = raw_decompressed[src_idx:src_idx + stride]
        src_idx += stride

        if filter_type == 0:  # None
            curr_line[:] = raw_scanline
        elif filter_type == 1:  # Sub
            for x in range(stride):
                a = curr_line[x - bpp] if x >= bpp else 0
                curr_line[x] = (raw_scanline[x] + a) & 0xFF
        elif filter_type == 2:  # Up
            for x in range(stride):
                b = prior_line[x]
                curr_line[x] = (raw_scanline[x] + b) & 0xFF
        elif filter_type == 3:  # Average
            for x in range(stride):
                a = curr_line[x - bpp] if x >= bpp else 0
                b = prior_line[x]
                curr_line[x] = (raw_scanline[x] + ((a + b) >> 1)) & 0xFF
        elif filter_type == 4:  # Paeth
            for x in range(stride):
                a = curr_line[x - bpp] if x >= bpp else 0
                b = prior_line[x]
                c = prior_line[x - bpp] if x >= bpp else 0
                p = a + b - c
                pa = abs(p - a)
                pb = abs(p - b)
                pc = abs(p - c)
                if pa <= pb and pa <= pc:
                    pr = a
                elif pb <= pc:
                    pr = b
                else:
                    pr = c
                curr_line[x] = (raw_scanline[x] + pr) & 0xFF
        else:
            raise ValueError(f"Unknown PNG filter type: {filter_type} at scanline {y}")

        # Transfer to flat RGBA buffer
        if color_type == 6:
            rgba_buffer[dst_idx:dst_idx + (width * 4)] = curr_line
            dst_idx += width * 4
        else:  # Expand RGB to RGBA
            line_idx = 0
            for _ in range(width):
                rgba_buffer[dst_idx] = curr_line[line_idx]
                rgba_buffer[dst_idx + 1] = curr_line[line_idx + 1]
                rgba_buffer[dst_idx + 2] = curr_line[line_idx + 2]
                rgba_buffer[dst_idx + 3] = 255
                dst_idx += 4
                line_idx += 3

        prior_line[:] = curr_line

    return width, height, rgba_buffer


def encode_png(width: int, height: int, rgba_buffer: bytes) -> bytes:
    """
    Encodes a 32-bit RGBA buffer of size width * height * 4 into standard PNG bytes.
    Uses filter type 0 (None) for deterministic, fast encoding.
    """
    if len(rgba_buffer) != width * height * 4:
        raise ValueError(
            f"Buffer size mismatch: expected {width * height * 4} bytes for {width}x{height} RGBA, got {len(rgba_buffer)}"
        )

    stride = width * 4
    raw_scanlines = bytearray(height * (1 + stride))
    src_idx = 0
    dst_idx = 0

    for _ in range(height):
        raw_scanlines[dst_idx] = 0  # Filter type 0: None
        dst_idx += 1
        raw_scanlines[dst_idx:dst_idx + stride] = rgba_buffer[src_idx:src_idx + stride]
        dst_idx += stride
        src_idx += stride

    compressed_idat = zlib.compress(bytes(raw_scanlines), level=6)

    def make_chunk(chunk_type: bytes, data: bytes) -> bytes:
        length = struct.pack(">I", len(data))
        crc = struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
        return length + chunk_type + data + crc

    # IHDR: 8-bit depth, color type 6 (RGBA), compression 0, filter 0, interlace 0
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    ihdr_chunk = make_chunk(b"IHDR", ihdr_data)
    idat_chunk = make_chunk(b"IDAT", compressed_idat)
    iend_chunk = make_chunk(b"IEND", b"")

    return PNG_SIGNATURE + ihdr_chunk + idat_chunk + iend_chunk
