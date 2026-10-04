import { useState, useRef } from "react";
import { useLanguage } from "../contexts/LanguageContext";

interface CompareViewerProps {
  originalUrl: string;
  resultUrl: string;
}

export default function CompareViewer({
  originalUrl,
  resultUrl,
}: CompareViewerProps) {
  const [position, setPosition] = useState(50);
  const containerRef = useRef<HTMLDivElement>(null);
  const { t } = useLanguage();

  const handleMove = (e: React.MouseEvent | React.TouchEvent) => {
    if (!containerRef.current) return;

    const { left, width } = containerRef.current.getBoundingClientRect();
    let clientX = 0;

    if ("touches" in e) {
      clientX = e.touches[0].clientX;
    } else {
      clientX = (e as React.MouseEvent).clientX;
    }

    // Hitung persentase posisi mouse/jari
    const x = Math.max(0, Math.min(clientX - left, width));
    const percent = (x / width) * 100;
    setPosition(percent);
  };

  return (
    <div
      ref={containerRef}
      className="relative w-full h-[300px] sm:h-[400px] overflow-hidden rounded-2xl cursor-ew-resize select-none border border-[var(--border)] bg-[var(--surface-soft)]"
      onMouseMove={handleMove}
      onTouchMove={handleMove}
    >
      {/* Gambar Asli (Layer Bawah) */}
      <img
        src={originalUrl}
        alt="Original"
        className="absolute inset-0 w-full h-full object-contain pointer-events-none opacity-80"
      />
      <div className="absolute top-4 left-4 bg-black/60 text-white px-3 py-1 rounded-lg text-xs font-semibold backdrop-blur-md">
        {t.original}
      </div>

      {/* Gambar Hasil (Layer Atas, di-crop pakai clip-path) */}
      <div
        className="absolute inset-0 w-full h-full pointer-events-none"
        style={{ clipPath: `inset(0 0 0 ${position}%)` }}
      >
        
        <img
          src={resultUrl}
          alt="Upscaled"
          className="absolute inset-0 w-full h-full object-contain"
        />
      </div>

      {/* Label After (Menempel di kanan container, bukan di layer atasnya) */}
      <div className="absolute top-4 right-4 bg-[var(--accent)] text-white px-3 py-1 rounded-lg text-xs font-semibold shadow-md pointer-events-none">
        {t.upscaled}
      </div>

      {/* Garis Slider */}
      <div
        className="absolute top-0 bottom-0 w-1 bg-white shadow-[0_0_10px_rgba(0,0,0,0.3)] pointer-events-none"
        style={{ left: `calc(${position}% - 2px)` }}
      >
        {/* Tombol Bulat di Tengah Garis */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-lg border border-gray-200">
          <div className="flex gap-1">
            <div className="w-0.5 h-3 bg-gray-400 rounded-full"></div>
            <div className="w-0.5 h-3 bg-gray-400 rounded-full"></div>
          </div>
        </div>
      </div>
    </div>
  );
}
