"""Pure image-processing functions for the Digit Pixelation Visualizer.

No Streamlit imports here: every function takes arrays in and returns arrays/images out.
"""
from __future__ import annotations

import math

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

GRID_SIZE: int = 32
PADDING_RATIO: float = 0.20  # 20% extra space around the digit's bounding box


def _to_grayscale(arr: np.ndarray) -> np.ndarray:
    """Step 1: collapse an RGBA/RGB/gray array into a single-channel uint8 image.

    White stroke on black background -> stroke is high intensity, background is 0.
    """
    arr = np.asarray(arr)
    if arr.ndim == 2:
        return arr.astype(np.uint8)
    if arr.ndim == 3 and arr.shape[2] == 4:
        # Composite onto black using alpha so transparent pixels become 0.
        rgb = arr[..., :3].astype(np.float32)
        alpha = arr[..., 3:4].astype(np.float32) / 255.0
        rgb = rgb * alpha
        return cv2.cvtColor(np.clip(rgb, 0, 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
    if arr.ndim == 3 and arr.shape[2] == 3:
        return cv2.cvtColor(arr.astype(np.uint8), cv2.COLOR_RGB2GRAY)
    raise ValueError(f"Unsupported array shape: {arr.shape}")


def process_digit(raw_rgba_array: np.ndarray) -> np.ndarray:
    """Convert a raw canvas drawing into a centered 32x32 uint8 grayscale array."""
    # 1. Grayscale conversion.
    gray = _to_grayscale(raw_rgba_array)

    # 2. Threshold + bounding box of all drawn (non-zero) pixels.
    ys, xs = np.nonzero(gray > 0)
    if ys.size == 0:
        return np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)  # nothing drawn
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    crop = gray[y0:y1, x0:x1]
    h, w = crop.shape

    # 3. Center the digit: place the cropped ink in the middle of a square canvas whose
    #    side is the longer bbox edge plus ~20% margin (bounding-box-center centering,
    #    MNIST-style). This keeps the aspect ratio and equal space on all sides.
    side = max(1, math.ceil(max(h, w) * (1.0 + PADDING_RATIO)))
    square = np.zeros((side, side), dtype=np.uint8)
    top = (side - h) // 2
    left = (side - w) // 2
    square[top:top + h, left:left + w] = crop

    # 4. Resize to 32x32 with area-based downsampling for anti-aliased intensities.
    #    (INTER_AREA is meant for shrinking; fall back to LANCZOS if the square is tiny.)
    interp = cv2.INTER_AREA if side >= GRID_SIZE else cv2.INTER_LANCZOS4
    small = cv2.resize(square, (GRID_SIZE, GRID_SIZE), interpolation=interp)

    # 5. Return uint8 values 0-255.
    return np.clip(small, 0, 255).astype(np.uint8)


def _load_font(size: int) -> ImageFont.ImageFont:
    """Load a small font, falling back gracefully across Pillow versions/platforms."""
    for name in ("DejaVuSans.ttf", "arial.ttf", "Arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)  # Pillow >= 10.1
    except TypeError:
        return ImageFont.load_default()


def render_pixel_grid_with_values(pixel_array: np.ndarray, upscale_to: int = 320) -> Image.Image:
    """Render a 32x32 array as a crisp block grid with each cell's 0-255 value overlaid."""
    arr = np.asarray(pixel_array, dtype=np.uint8)
    n = arr.shape[0]

    # Upscale with nearest-neighbor so each cell stays a crisp, un-blurred block.
    img = Image.fromarray(arr, mode="L").resize((upscale_to, upscale_to), Image.NEAREST).convert("RGB")
    draw = ImageDraw.Draw(img)
    cell = upscale_to / n

    # Thin grid lines between cells.
    grid_color = (70, 70, 70)
    for i in range(1, n):
        p = round(i * cell)
        draw.line([(p, 0), (p, upscale_to)], fill=grid_color, width=1)
        draw.line([(0, p), (upscale_to, p)], fill=grid_color, width=1)

    # Intensity text centered in each cell; white on dark cells, black on light cells.
    font = _load_font(7)
    for r in range(n):
        for c in range(n):
            v = int(arr[r, c])
            color = (255, 255, 255) if v < 128 else (0, 0, 0)
            cx, cy = (c + 0.5) * cell, (r + 0.5) * cell
            draw.text((cx, cy), str(v), fill=color, font=font, anchor="mm")
    return img
