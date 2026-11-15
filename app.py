"""Digit Pixelation Visualizer - Streamlit UI only."""
from __future__ import annotations

import streamlit as st
from streamlit_drawable_canvas import st_canvas

from canvas_utils import CANVAS_SIZE, canvas_to_grayscale
from pixelation import process_digit, render_pixel_grid_with_values

st.set_page_config(page_title="Digit Pixelation Visualizer", layout="wide")

# Each canvas is 280px wide, so 10 side-by-side columns need more than a typical screen.
# Give columns a minimum width and let the row scroll horizontally instead of overflowing.
st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] { overflow-x: auto; flex-wrap: nowrap; }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"],
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] { min-width: 330px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Digit Pixelation Visualizer")
st.caption("Draw each digit (mouse or pen). It is centered, shrunk to 32×32, and shown with its pixel values.")

# Changing this counter changes every canvas key, which resets all canvases.
if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

if st.button("Clear All"):
    st.session_state.reset_counter += 1

cols = st.columns(10)
for digit, col in enumerate(cols):
    with col:
        st.markdown(f"### {digit}")

        # 1. Drawing canvas: black background, white stroke. Live-updates on every stroke.
        result = st_canvas(
            fill_color="rgba(255, 255, 255, 1)",
            stroke_width=20,
            stroke_color="#FFFFFF",
            background_color="#000000",
            height=CANVAS_SIZE,
            width=CANVAS_SIZE,
            drawing_mode="freedraw",
            update_streamlit=True,
            key=f"canvas_{digit}_{st.session_state.reset_counter}",
        )

        # 2. Down arrow + caption.
        st.markdown(
            "<div style='text-align:center'><span style='font-size:32px'>↓</span><br>"
            "<span style='font-size:13px;color:gray'>raw → pixelated</span></div>",
            unsafe_allow_html=True,
        )

        # 3 + 4. Process the drawing and show the 32x32 grid with values overlaid.
        # An empty canvas yields an all-zero grid (no error).
        gray = canvas_to_grayscale(result)
        pixels = process_digit(gray)
        st.image(render_pixel_grid_with_values(pixels, upscale_to=320), width=320)
