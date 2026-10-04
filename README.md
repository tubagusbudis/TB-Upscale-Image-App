<div align="center">
  <img src="https://img.icons8.com/color/120/000000/image-enhancement.png" alt="Upscale Studio Logo">
  <h1>✨ Upscale Studio</h1>
  <p><strong>A Minimalist, Local-First AI Image Upscaler Web Application.</strong></p>
  <p>Enhance and upscale your images up to 8K entirely on your own machine. No cloud subscriptions, no compromises.</p>
</div>

---

## 🌟 Overview

**Upscale Studio** is a personal, full-stack web application designed to run locally. It leverages the power of AI to upscale low-resolution images into stunning high-definition outputs. 

Built with simplicity in mind, it provides an intuitive workflow: **Upload → Upscale → Preview Before/After → Download**. All processing happens on your local backend, keeping your data 100% private. Supports **GPU acceleration** via CUDA for blazing-fast upscaling on NVIDIA GPUs, with automatic fallback to CPU.

## 🔥 Key Features

- **Local-First & Private:** Your images never leave your computer. Processing is done completely on your local server.
- **GPU Accelerated:** Leverages NVIDIA CUDA with fp16 for fast inference. Supports RTX 50-series (Blackwell, sm_120) and older architectures.
- **Auto Fallback:** Automatically falls back to CPU if no compatible GPU is detected.
- **Up to 8K Resolution:** Target specific resolutions (2K, 4K, 8K) while preserving the original aspect ratio.
- **Modern UI:** Clean, minimalist, and soft-colored interface designed for ease of use.
- **Before/After Preview:** Instantly compare the original and upscaled images side-by-side before downloading.

## ⚙️ Tech Stack

- **Frontend:** React, TypeScript, Vite, TailwindCSS (or Vanilla CSS)
- **Backend:** Python, FastAPI, Uvicorn (with PyTorch + CUDA for model inference)
- **AI Models:** Real-ESRGAN (x2 & x4) via `realesrgan` + `basicsr`

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- **For GPU:** NVIDIA GPU with CUDA support. RTX 50-series requires PyTorch with CUDA 12.8+.


### 1. Clone the Repository
```bash
git clone https://github.com/tubagusbudis/TB-Upscale-Image-App.git
cd TB-Upscale-Image-App
```

### 2. Setup the Backend
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install PyTorch with CUDA 12.8 (required for RTX 50-series / Blackwell)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# Install remaining dependencies
pip install -r requirements.txt

python main.py
```

> **Note:** If you have an older GPU (RTX 20/30/40 series), you can also use
> `cu124` or `cu121` wheels. Only RTX 50-series (sm_120) requires `cu128`.

#### Environment Variables (optional)
| Variable | Default | Description |
|---|---|---|
| `UPSCALE_TILE` | `400` | Tile size for inference. Lower = less VRAM usage. Set `0` to disable tiling. |
| `UPSCALE_TILE_PAD` | `10` | Tile padding pixels |
| `GPU_SEMAPHORE_LIMIT` | `1` | Max concurrent GPU inference jobs |

### 3. Setup the Frontend
```bash
cd frontend
npm install
npm run dev
```

### 4. Start Upscaling!
Open your browser and navigate to `http://localhost:5173` (or the port specified by Vite) and start upscaling your images!

---

## 📝 License
This project is for personal use and is a showcase of building local-first AI tools.

<div align="center">
  <p>Made with ❤️ by <a href="https://github.com/tubagusbudis">Tubagus Budi S</a></p>
</div>
