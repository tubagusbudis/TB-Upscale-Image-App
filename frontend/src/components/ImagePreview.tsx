import { useState, useEffect } from "react";
import { X, Zap, Monitor, Maximize } from "lucide-react";
import { motion } from "framer-motion";
import { useLanguage } from "../contexts/LanguageContext";

interface ImagePreviewProps {
  file: File;
  onClear: () => void;
  onUpscale: (resolution: string) => void;
}

export default function ImagePreview({
  file,
  onClear,
  onUpscale,
}: ImagePreviewProps) {
  const [previewUrl, setPreviewUrl] = useState<string>("");
  const [resolution, setResolution] = useState("x2");
  const { t } = useLanguage();

  useEffect(() => {
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Image Preview Box */}
      <div className="relative rounded-2xl overflow-hidden border border-[var(--border)] bg-[var(--surface-soft)]">
        <img
          src={previewUrl}
          alt="Preview"
          className="w-full max-h-[300px] sm:max-h-[400px] object-contain"
        />
        <button
          onClick={onClear}
          className="absolute top-4 right-4 p-2 bg-black/50 hover:bg-black/70 text-white rounded-full backdrop-blur-sm transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Resolution Selector */}
      <div>
        <h3 className="text-sm font-medium mb-3">{t.selectResolution}</h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {[
            { id: "2k", label: "2K Fast", icon: Zap },
            { id: "4k", label: "4K Ultra", icon: Monitor },
            { id: "8k", label: "8K Max", icon: Maximize },
          ].map((res) => (
            <button
              key={res.id}
              onClick={() => setResolution(res.id)}
              className={`flex flex-col items-center justify-center p-3 rounded-xl border-2 transition-all ${
                resolution === res.id
                  ? "border-[var(--accent)] bg-[var(--accent-soft)] text-[var(--accent)]"
                  : "border-[var(--border)] bg-[var(--surface)] text-[var(--text-secondary)] hover:border-[var(--text-muted)]"
              }`}
            >
              <res.icon className="w-6 h-6 mb-2" />
              <span className="text-sm font-semibold">{res.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Action Button */}
      <button
        onClick={() => onUpscale(resolution)}
        className="w-full py-4 bg-[var(--accent)] hover:bg-[#7a8be6] text-white rounded-xl font-bold text-lg shadow-sm transition-colors flex items-center justify-center gap-2"
      >
        <Zap className="w-5 h-5 fill-current" />
        {t.startUpscale}
      </button>
    </motion.div>
  );
}
