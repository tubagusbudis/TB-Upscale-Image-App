"""
Standalone upscale script (for testing outside of the API).
Uses GPU automatically if available, falls back to CPU.
"""

import cv2
import torch
import os
import time

from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer


def main():
    print("🚀 Mulai proses persiapan upscale...")

    input_path = "input/test.jpg"
    output_path = "output/test_upscaled.png"

    if not os.path.exists(input_path):
        print(f"❌ Gambar {input_path} belum ada! Masukin dulu gambarnya ya.")
        return

    # Device detection
    if torch.cuda.is_available():
        device = torch.device("cuda", 0)
        gpu_id = 0
        use_half = True
        print(f"🟢 Pakai GPU: {torch.cuda.get_device_name(0)}")
    else:
        device = torch.device("cpu")
        gpu_id = None
        use_half = False
        print("🟡 GPU tidak tersedia, pakai CPU (akan lambat)")

    # Baca gambar pakai OpenCV
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)

    # Setup arsitektur model bawaan Real-ESRGAN x4
    model = RRDBNet(
        num_in_ch=3, num_out_ch=3, num_feat=64,
        num_block=23, num_grow_ch=32, scale=4,
    )

    # URL model (akan otomatis di-download kalau belum ada)
    model_url = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"

    tile = int(os.environ.get("UPSCALE_TILE", "400"))
    print(f"⏳ Menyiapkan AI Model (tile={tile}, half={use_half}, device={device})...")

    # Inisialisasi Upscaler
    upscaler = RealESRGANer(
        scale=4,
        model_path=model_url,
        model=model,
        tile=tile,
        tile_pad=10,
        pre_pad=0,
        half=use_half,
        gpu_id=gpu_id,
        device=device,
    )

    print("🧠 AI lagi mikir (Proses upscaling x4 sedang berjalan)...")
    t0 = time.perf_counter()
    try:
        with torch.inference_mode():
            output, _ = upscaler.enhance(img, outscale=4)

        elapsed = time.perf_counter() - t0
        cv2.imwrite(output_path, output)
        print(f"✅ Sukses 100%! ({elapsed:.2f}s) Cek hasil gambarnya di {output_path}")
    except Exception as e:
        print(f"❌ Waduh, prosesnya error: {e}")
    finally:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


if __name__ == "__main__":
    main()