import cv2
import torch
import os

# Trik ninja: Sembunyikan GPU biar PyTorch terpaksa murni pakai CPU
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

def main():
    print("🚀 Mulai proses persiapan upscale...")
    
    input_path = 'input/test.jpg'
    output_path = 'output/test_upscaled.png'
    
    if not os.path.exists(input_path):
        print(f"❌ Gambar {input_path} belum ada! Masukin dulu gambarnya ya.")
        return

    # Baca gambar pakai OpenCV
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    
    # Setup arsitektur model bawaan Real-ESRGAN x4
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
    
    # URL model (akan otomatis di-download kalau belum ada)
    model_url = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth'
    
    print("⏳ Menyiapkan AI Model (kalau baru pertama, bakal download modelnya dulu, tungguin aja)...")
    
    # Inisialisasi Upscaler
    upscaler = RealESRGANer(
        scale=4,
        model_path=model_url,
        model=model,
        tile=512, # Pecah gambar jadi kotak-kotak 512px biar VRAM aman
        tile_pad=10,
        pre_pad=0,
        half=False, # Kita set False dulu buat ngehindarin error dari RTX 5050
        gpu_id=None
    )

    print("🧠 AI lagi mikir (Proses upscaling x4 sedang berjalan)...")
    try:
        # Eksekusi upscale
        output, _ = upscaler.enhance(img, outscale=4)
        
        # Simpan hasil
        cv2.imwrite(output_path, output)
        print(f"✅ Sukses 100%! Cek hasil gambarnya di {output_path}")
    except Exception as e:
        print(f"❌ Waduh, prosesnya error: {e}")

if __name__ == '__main__':
    main()