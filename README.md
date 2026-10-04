<div align="center">
  <img src="https://img.icons8.com/color/120/000000/image-enhancement.png" alt="Upscale Studio Logo">
  <h1>✨ Upscale Studio</h1>
  <p><strong>A Minimalist, Local-First AI Image Upscaler Web Application.</strong></p>
  <p>Enhance and upscale your images up to 8K entirely on your own machine. No cloud subscriptions, no compromises.</p>
</div>

---

## 🌟 Overview

**Upscale Studio** is a personal, full-stack web application designed to run locally. It leverages the power of AI to upscale low-resolution images into stunning high-definition outputs. 

Built with simplicity in mind, it provides an intuitive workflow: **Upload → Upscale → Preview Before/After → Download**. All processing happens on your local backend, keeping your data 100% private. (Note: Currently running on CPU as the latest GPU architectures are not yet supported for the local models used).

## 🔥 Key Features

- **Local-First & Private:** Your images never leave your computer. Processing is done completely on your local server.
- **CPU Based (For Now):** Currently utilizes CPU for processing, as newer GPU architectures are not yet supported by the local AI tools being used. GPU support is planned for the future.
- **Up to 8K Resolution:** Target specific resolutions (2K, 4K, 8K) while preserving the original aspect ratio.
- **Modern UI:** Clean, minimalist, and soft-colored interface designed for ease of use.
- **Before/After Preview:** Instantly compare the original and upscaled images side-by-side before downloading.

## ⚙️ Tech Stack

- **Frontend:** React, TypeScript, Vite, TailwindCSS (or Vanilla CSS)
- **Backend:** Python, FastAPI / Flask (with PyTorch or ONNX for model inference)
- **AI Models:** Integrates with local upscaling models (e.g., Real-ESRGAN).

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.10+)


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

pip install -r requirements.txt
python main.py
```

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
