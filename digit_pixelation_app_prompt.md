# Build Prompt: Digit Pixelation Visualizer (Streamlit)

Build a Streamlit web app called **Digit Pixelation Visualizer**. Follow every instruction below exactly — do not substitute different libraries, layouts, or algorithms unless something below is technically impossible, in which case state the substitution explicitly before proceeding.

## 1\. Project structure

Create exactly these files:

```
digit_pixelation_app/
├── app.py                # Streamlit hosting/UI module only
├── pixelation.py         # Image processing module only (no Streamlit code here)
├── canvas_utils.py       # Canvas capture + conversion helpers
└── requirements.txt
```

`requirements.txt` must include: `streamlit`, `streamlit-drawable-canvas`, `numpy`, `Pillow`, `opencv-python-headless`.

Keep a strict separation of concerns:

- `pixelation.py` contains pure functions only (input: image array, output: image array or metadata). No UI, no Streamlit imports.  
- `canvas_utils.py` handles converting the drawable-canvas JSON/RGBA output into a usable grayscale numpy array.  
- `app.py` only handles layout, state, and calling functions from the other two modules.

## 2\. Layout requirements

- Use `streamlit-drawable-canvas` for freehand drawing (supports both mouse and pen/tablet input natively — do not build a custom canvas).  
- Display **10 columns side by side** (`st.columns(10)`), one per digit 0–9, each labeled with its digit above the canvas.  
- In each column, **stacked vertically, top to bottom**:  
  1. A drawing canvas (background: black, stroke: white, stroke width \~18–22px, canvas size 280x280 px) — this is where the user draws that digit.  
  2. A visible **down arrow (↓)** with the caption "raw → pixelated" directly underneath the canvas.  
  3. The processed 32×32 pixelated result, displayed scaled up (e.g., rendered at 320×320 px using nearest-neighbor/`Image.NEAREST` upscaling so each of the 32×32 cells is a crisp visible block, not blurred).  
  4. On top of each of the 32×32 blocks in that pixelated image, overlay the grayscale intensity value (an integer 0–255) as small text, so the numeric pixel grid is readable (use PIL `ImageDraw` to draw text on the upscaled image, font size small enough to fit, e.g. 7–9px).  
- Each digit column is independent — drawing digit "0" must not affect or require the other 9 canvases.  
- Add a "Clear All" button that resets all 10 canvases.  
- Each canvas should auto-update its pixelated output on every stroke/change (use the canvas component's `key` \+ rerun behavior — do not require a manual "process" button, though a manual button is an acceptable fallback if live update proves unreliable).

## 3\. Processing pipeline (implement in `pixelation.py`)

Implement this exact sequence as a function `process_digit(raw_rgba_array: np.ndarray) -> np.ndarray` that returns a 32×32 uint8 grayscale array (values 0–255):

1. **Convert to grayscale**: Convert the RGBA canvas output to a single-channel grayscale array where the drawn stroke (white on black) becomes high intensity and background is 0\.  
2. **Threshold \+ bounding box**: Find the bounding box of all non-zero (drawn) pixels. If nothing is drawn, return a blank 32×32 array of zeros.  
3. **Center the digit**: Crop to the bounding box, then pad the crop into a square canvas (side length \= max(bbox width, bbox height) \+ a small margin, e.g. 20% padding) so the digit is centered with equal space on all sides — do not just resize the raw canvas; the centering must be based on the bounding box of actual ink, matching the standard MNIST-style centering approach (center of mass or bounding-box-center, bounding-box-center is sufficient here).  
4. **Resize to 32×32**: Resize the centered, padded square to exactly 32×32 pixels using area-based downsampling (`cv2.INTER_AREA` or PIL `Image.LANCZOS`) — not nearest-neighbor, since we want proper anti-aliased intensity values, not a blocky binary result.  
5. **Return** the 32×32 uint8 array (values 0 \= black/background, 255 \= full white stroke, with proper anti-aliased grayscale values in between from the resize).

This function must have no Streamlit dependency — it should be testable by passing in a plain numpy array and asserting the output shape is (32, 32\) and dtype is uint8.

Implement a second function in `pixelation.py`: `render_pixel_grid_with_values(pixel_array: np.ndarray, upscale_to: int = 320) -> PIL.Image` that:

- Upscales the 32×32 array to `upscale_to`×`upscale_to` using nearest-neighbor (so blocks stay crisp).  
- Draws a thin grid line between each of the 32×32 cells.  
- Draws the original 0–255 intensity value as text centered in each cell, using a contrasting text color (white text on dark cells, black text on light cells) so it's legible regardless of background intensity.

## 4\. Technical constraints

- Python 3.10+, type hints on all function signatures.  
- No hardcoded absolute file paths.  
- No external network calls, no database, no persistence — this is a pure in-memory, single-session visual tool.  
- The app must run with a single command: `streamlit run app.py`.  
- Handle the empty-canvas case gracefully (show a placeholder/gray 32×32 grid with "0" values rather than erroring) for any digit the user hasn't drawn yet.  
- Add minimal inline comments explaining each processing step (centering, resizing, overlay) since this is for a teaching/demo context.

## 5\. Deliverable

Output the complete contents of all four files (`app.py`, `pixelation.py`, `canvas_utils.py`, `requirements.txt`), fully working, ready to run locally and deployable as-is to Streamlit Community Cloud.