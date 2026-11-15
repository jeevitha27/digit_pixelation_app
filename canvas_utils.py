"""Helpers for turning streamlit-drawable-canvas output into numpy arrays."""
from __future__ import annotations

from typing import Any, Optional

import numpy as np

CANVAS_SIZE: int = 280


def canvas_to_rgba(canvas_result: Any) -> Optional[np.ndarray]:
    """Return the canvas RGBA image as a uint8 array, or None if nothing is available yet."""
    if canvas_result is None:
        return None
    # In newer streamlit-drawable-canvas versions, `image_data` is a property
    # that raises RuntimeError when no image data URL is available yet.
    # A plain getattr() won't catch that, so we use try/except.
    try:
        img = canvas_result.image_data
    except (RuntimeError, AttributeError):
        return None
    if img is None:
        return None
    data = np.asarray(img)
    if data.ndim != 3 or data.shape[2] != 4:
        return None
    return data.astype(np.uint8)


def canvas_to_grayscale(canvas_result: Any) -> np.ndarray:
    """Return a single-channel uint8 array (white stroke = high value, background = 0).

    An empty/not-yet-rendered canvas yields an all-zero array.
    """
    rgba = canvas_to_rgba(canvas_result)
    if rgba is None:
        return np.zeros((CANVAS_SIZE, CANVAS_SIZE), dtype=np.uint8)
    # Composite onto black via alpha, then average RGB -> luminance.
    rgb = rgba[..., :3].astype(np.float32) * (rgba[..., 3:4].astype(np.float32) / 255.0)
    gray = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    return np.clip(gray, 0, 255).astype(np.uint8)
