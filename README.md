# Digit Pixelation Visualizer

An interactive Streamlit web app that lets you draw digits (0–9) and instantly see them pixelated into a 32×32 grid with intensity values overlaid — perfect for understanding how digit recognition systems (like MNIST) pre-process handwritten input.

## ✨ Features

- **10 side-by-side drawing canvases** — one per digit (0–9)
- **Real-time pixelation** — every stroke updates the 32×32 output instantly
- **MNIST-style centering** — drawn digits are bounding-box centered with 20% padding
- **Anti-aliased downscaling** — area-based interpolation preserves smooth grayscale values
- **Pixel value overlay** — each of the 1,024 cells shows its 0–255 intensity
- **Clear All** button to reset every canvas at once

## 🖼️ How It Works

1. **Draw** a digit on any canvas (mouse or pen/tablet)
2. The raw drawing is **cropped, centered, and resized** to 32×32 pixels
3. The result is **upscaled with nearest-neighbor** for a crisp block view
4. **Grid lines and intensity values** are overlaid so you can read every pixel

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/digit_pixelation_app.git
cd digit_pixelation_app

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📁 Project Structure

```
digit_pixelation_app/
├── app.py              # Streamlit UI — layout, canvases, and display
├── pixelation.py       # Pure image processing (no Streamlit dependency)
├── canvas_utils.py     # Canvas output → numpy array converters
├── requirements.txt    # Python dependencies
└── README.md
```

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/)** — interactive web UI
- **[streamlit-drawable-canvas](https://github.com/andfanilo/streamlit-drawable-canvas)** — freehand drawing component
- **NumPy** — array manipulation
- **Pillow** — image rendering & text overlay
- **OpenCV** — grayscale conversion & resizing

## 📦 Requirements

- Python 3.10+
- See [`requirements.txt`](requirements.txt) for pip dependencies

## 🌐 Deploy on Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account and select this repository
4. Set the main file path to `app.py`
5. Click **Deploy**

## 📄 License

MIT
