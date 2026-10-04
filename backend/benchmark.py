"""
Benchmark script: CPU vs GPU upscale using Real-ESRGAN x2.
Tests on a single image and prints timing comparison.
"""
import os
import sys

# Fix Windows console encoding for emoji/unicode
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import time
import cv2
import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

INPUT_PATH = "input/download.jpg"
MODEL_URL = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth"


def build_upscaler(device_str: str):
    """Build a RealESRGANer on the given device."""
    device = torch.device(device_str)
    gpu_id = 0 if device_str == "cuda" else None
    use_half = device_str == "cuda"

    model = RRDBNet(
        num_in_ch=3, num_out_ch=3, num_feat=64,
        num_block=23, num_grow_ch=32, scale=2,
    )
    return RealESRGANer(
        scale=2, model_path=MODEL_URL, model=model,
        tile=400, tile_pad=10, pre_pad=0,
        half=use_half, gpu_id=gpu_id, device=device,
    )


def benchmark(device_str: str, img, output_path: str) -> float:
    """Run upscale and return elapsed time in seconds."""
    print(f"\n{'='*50}")
    print(f"  Benchmarking on: {device_str.upper()}")
    print(f"{'='*50}")

    upscaler = build_upscaler(device_str)

    # Warm-up run for GPU (first run includes CUDA kernel compilation)
    if device_str == "cuda":
        print("  Warm-up run...")
        with torch.inference_mode():
            upscaler.enhance(img, outscale=2)
        torch.cuda.synchronize()

    # Timed run
    print("  Timed run...")
    t0 = time.perf_counter()
    with torch.inference_mode():
        output, _ = upscaler.enhance(img, outscale=2)
    if device_str == "cuda":
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - t0

    cv2.imwrite(output_path, output)
    print(f"  ✅ Done in {elapsed:.3f}s — saved to {output_path}")

    # Cleanup
    del upscaler
    if device_str == "cuda":
        torch.cuda.empty_cache()

    return elapsed


def main():
    print(f"PyTorch: {torch.__version__}")
    print(f"CUDA: {torch.version.cuda}")
    print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'}")
    print(f"Arch list: {torch.cuda.get_arch_list() if torch.cuda.is_available() else 'N/A'}")

    if not os.path.exists(INPUT_PATH):
        print(f"❌ Gambar {INPUT_PATH} tidak ditemukan!")
        return

    img = cv2.imread(INPUT_PATH, cv2.IMREAD_UNCHANGED)
    h, w = img.shape[:2]
    print(f"\nInput: {INPUT_PATH} ({w}x{h})")

    # CPU benchmark
    cpu_time = benchmark("cpu", img, "output/benchmark_cpu.png")

    # GPU benchmark
    if torch.cuda.is_available():
        gpu_time = benchmark("cuda", img, "output/benchmark_gpu.png")
    else:
        print("\n⚠️ CUDA not available, skipping GPU benchmark")
        gpu_time = None

    # Summary
    print(f"\n{'='*50}")
    print(f"  BENCHMARK RESULTS")
    print(f"{'='*50}")
    print(f"  CPU: {cpu_time:.3f}s")
    if gpu_time is not None:
        print(f"  GPU: {gpu_time:.3f}s")
        speedup = cpu_time / gpu_time
        print(f"  Speedup: {speedup:.1f}x faster on GPU 🚀")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
