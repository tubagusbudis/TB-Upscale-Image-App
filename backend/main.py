import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import cv2
import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

app = FastAPI(title="Upscale Studio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)

print("⏳ Loading AI Models ke memory (tunggu bentar, ini load 2 model lho)...")

# 1. Inisialisasi Model x2
model_x2 = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
url_x2 = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth'
upscaler_x2 = RealESRGANer(scale=2, model_path=url_x2, model=model_x2, tile=512, tile_pad=10, pre_pad=0, half=False, gpu_id=None)

# 2. Inisialisasi Model x4
model_x4 = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
url_x4 = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth'
upscaler_x4 = RealESRGANer(scale=4, model_path=url_x4, model=model_x4, tile=512, tile_pad=10, pre_pad=0, half=False, gpu_id=None)

print("✅ AI Models Ready! Server API siap nerima request.")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Backend Upscale Studio jalan!"}

@app.post("/api/v1/upscale")
async def upload_and_upscale(
    file: UploadFile = File(...),
    target_scale: int = Form(2) # Default ke 2x kalau tidak ada input
):
    input_path = f"input/{file.filename}"
    output_filename = f"upscaled_{target_scale}x_{file.filename}.png"
    output_path = f"output/{output_filename}"
    
    with open(input_path, "wb") as buffer:
        buffer.write(await file.read())
        
    print(f"Mulai memproses gambar: {file.filename} dengan skala x{target_scale}...")
    
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    try:
        # Logika pemilihan AI berdasarkan request Frontend
        if target_scale == 2:
            output, _ = upscaler_x2.enhance(img, outscale=2)
        elif target_scale == 4:
            output, _ = upscaler_x4.enhance(img, outscale=4)
        elif target_scale == 8:
            output, _ = upscaler_x4.enhance(img, outscale=8)
        else:
            output, _ = upscaler_x2.enhance(img, outscale=2) # Fallback aman

        cv2.imwrite(output_path, output)
        print(f"✅ Upscale x{target_scale} beres!")
        
        return FileResponse(output_path, media_type="image/png", filename=output_filename)
    except Exception as e:
        return {"error": f"Waduh, gagal proses: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)