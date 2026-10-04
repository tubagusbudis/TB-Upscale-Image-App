import os
import time
import asyncio
import logging

import cv2
import torch
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.concurrency import run_in_threadpool
from contextlib import asynccontextmanager

from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("upscale-studio")

# ---------------------------------------------------------------------------
# Configuration (via env vars, with sensible defaults)
# ---------------------------------------------------------------------------
UPSCALE_TILE: int = int(os.environ.get("UPSCALE_TILE", "400"))
UPSCALE_TILE_PAD: int = int(os.environ.get("UPSCALE_TILE_PAD", "10"))
GPU_SEMAPHORE_LIMIT: int = int(os.environ.get("GPU_SEMAPHORE_LIMIT", "1"))

# ---------------------------------------------------------------------------
# Device detection
# ---------------------------------------------------------------------------
def get_device() -> torch.device:
    """Return the best available device, with a clear log."""
    if torch.cuda.is_available():
        name = torch.cuda.get_device_name(0)
        cap = torch.cuda.get_device_capability(0)
        logger.info(f"🟢 CUDA tersedia — GPU: {name} (sm_{cap[0]}{cap[1]})")
        return torch.device("cuda", 0)
    else:
        logger.warning("🟡 CUDA tidak tersedia — fallback ke CPU (proses akan lambat!)")
        return torch.device("cpu")

DEVICE = get_device()
USE_HALF = DEVICE.type == "cuda"
GPU_ID = 0 if DEVICE.type == "cuda" else None

logger.info(f"   fp16 (half): {USE_HALF}")
logger.info(f"   tile: {UPSCALE_TILE}")
logger.info(f"   gpu_id: {GPU_ID}")

# ---------------------------------------------------------------------------
# Model URLs
# ---------------------------------------------------------------------------
MODEL_X2_URL = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth"
MODEL_X4_URL = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"

# ---------------------------------------------------------------------------
# Global upscaler references (populated in lifespan)
# ---------------------------------------------------------------------------
upscaler_x2: RealESRGANer | None = None
upscaler_x4: RealESRGANer | None = None
gpu_semaphore: asyncio.Semaphore | None = None


def _build_upscaler(scale: int, model_url: str) -> RealESRGANer:
    """Build a RealESRGANer for the given scale factor."""
    model = RRDBNet(
        num_in_ch=3, num_out_ch=3, num_feat=64,
        num_block=23, num_grow_ch=32, scale=scale,
    )
    return RealESRGANer(
        scale=scale,
        model_path=model_url,
        model=model,
        tile=UPSCALE_TILE,
        tile_pad=UPSCALE_TILE_PAD,
        pre_pad=0,
        half=USE_HALF,
        gpu_id=GPU_ID,
        device=DEVICE,
    )


# ---------------------------------------------------------------------------
# FastAPI lifespan — load models ONCE at startup
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    global upscaler_x2, upscaler_x4, gpu_semaphore

    logger.info("⏳ Loading AI Models ke memory (x2 + x4)...")
    t0 = time.perf_counter()

    upscaler_x2 = _build_upscaler(2, MODEL_X2_URL)
    upscaler_x4 = _build_upscaler(4, MODEL_X4_URL)
    gpu_semaphore = asyncio.Semaphore(GPU_SEMAPHORE_LIMIT)

    elapsed = time.perf_counter() - t0
    logger.info(f"✅ AI Models Ready! ({elapsed:.1f}s) — device={DEVICE}, half={USE_HALF}")

    yield  # ---- app runs here ----

    # Cleanup on shutdown
    logger.info("🛑 Shutting down — releasing GPU memory...")
    del upscaler_x2, upscaler_x4
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


app = FastAPI(title="Upscale Studio API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)


# ---------------------------------------------------------------------------
# Inference helper (runs in threadpool, guarded by semaphore)
# ---------------------------------------------------------------------------
def _do_enhance(img, upscaler: RealESRGANer, outscale: int, tile: int):
    """
    Run inference inside torch.inference_mode().
    On OOM, retry with a smaller tile.
    """
    with torch.inference_mode():
        try:
            upscaler.tile = tile
            output, _ = upscaler.enhance(img, outscale=outscale)
            return output
        except torch.cuda.OutOfMemoryError:
            smaller_tile = max(tile // 2, 128)
            logger.warning(
                f"⚠️ OOM dengan tile={tile}, coba ulang dengan tile={smaller_tile}"
            )
            torch.cuda.empty_cache()
            upscaler.tile = smaller_tile
            output, _ = upscaler.enhance(img, outscale=outscale)
            return output
        finally:
            if torch.cuda.is_available():
                torch.cuda.empty_cache()


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/")
def health_check():
    return {"status": "ok", "message": "Backend Upscale Studio jalan!"}


@app.get("/health/gpu")
def gpu_health():
    """GPU / CUDA health info endpoint."""
    info = {
        "cuda_available": torch.cuda.is_available(),
        "torch_version": torch.__version__,
        "cuda_version": torch.version.cuda,
        "device_in_use": str(DEVICE),
        "half_precision": USE_HALF,
        "tile": UPSCALE_TILE,
    }
    if torch.cuda.is_available():
        info["device_name"] = torch.cuda.get_device_name(0)
        cap = torch.cuda.get_device_capability(0)
        info["compute_capability"] = f"sm_{cap[0]}{cap[1]}"
        info["arch_list"] = torch.cuda.get_arch_list()
        mem = torch.cuda.mem_get_info(0)
        info["vram_free_mb"] = round(mem[0] / 1024 / 1024)
        info["vram_total_mb"] = round(mem[1] / 1024 / 1024)
    return info


@app.post("/api/v1/upscale")
async def upload_and_upscale(
    file: UploadFile = File(...),
    target_scale: int = Form(2),  # Default ke 2x kalau tidak ada input
):
    input_path = f"input/{file.filename}"
    output_filename = f"upscaled_{target_scale}x_{file.filename}.png"
    output_path = f"output/{output_filename}"

    with open(input_path, "wb") as buffer:
        buffer.write(await file.read())

    logger.info(
        f"📥 Request upscale: {file.filename} | scale=x{target_scale} | device={DEVICE}"
    )

    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    t0 = time.perf_counter()

    try:
        # Pilih upscaler berdasarkan target_scale
        if target_scale == 2:
            upscaler, outscale = upscaler_x2, 2
        elif target_scale == 4:
            upscaler, outscale = upscaler_x4, 4
        elif target_scale == 8:
            upscaler, outscale = upscaler_x4, 8
        else:
            upscaler, outscale = upscaler_x2, 2  # Fallback aman

        # Jalankan inference di threadpool, dibatasi semaphore
        async with gpu_semaphore:
            output = await run_in_threadpool(
                _do_enhance, img, upscaler, outscale, UPSCALE_TILE
            )

        elapsed = time.perf_counter() - t0
        cv2.imwrite(output_path, output)

        logger.info(
            f"✅ Upscale x{target_scale} selesai — "
            f"{elapsed:.2f}s | device={DEVICE} | half={USE_HALF}"
        )

        return FileResponse(
            output_path, media_type="image/png", filename=output_filename
        )
    except Exception as e:
        elapsed = time.perf_counter() - t0
        logger.error(f"❌ Gagal upscale ({elapsed:.2f}s): {e}")
        return {"error": f"Waduh, gagal proses: {str(e)}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False, workers=1)