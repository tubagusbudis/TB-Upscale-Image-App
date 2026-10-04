import { useState, useEffect } from "react";
import { WandSparkles, Moon, Sun, Loader2, Download } from "lucide-react";
import UploadDropzone from "./components/UploadDropzone";
import ImagePreview from "./components/ImagePreview";
import CompareViewer from "./components/CompareViewer";
import Footer from "./components/Footer";
import BouncyText from "./components/BouncyText";
import { useLanguage } from "./contexts/LanguageContext";

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [resultUrl, setResultUrl] = useState<string | null>(null);
  const [appliedScale, setAppliedScale] = useState<number | null>(null);
  const { t, language, setLanguage } = useLanguage();

  const [isDarkMode, setIsDarkMode] = useState(() => {
    if (typeof window !== "undefined") {
      return (
        document.documentElement.classList.contains("dark") ||
        window.matchMedia("(prefers-color-scheme: dark)").matches
      );
    }
    return false;
  });

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDarkMode]);

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setResultUrl(null);
    setAppliedScale(null);
  };

  const handleUpscale = async (resolution: string) => {
    if (!selectedFile) return;

    setIsProcessing(true);

    // Terjemahkan ID tombol (x2, 4k, 8k) menjadi angka skala (2, 4, 8)
    let scaleValue = 2;
    if (resolution === "4k") scaleValue = 4;
    if (resolution === "8k") scaleValue = 8;

    setAppliedScale(scaleValue);

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("target_scale", scaleValue.toString()); // Kirim angka skala ke backend

    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/upscale", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error(t.uploadError);

      const blob = await response.blob();
      const objectUrl = URL.createObjectURL(blob);
      setResultUrl(objectUrl);
    } catch (error) {
      console.error(error);
      alert(t.uploadErrorAlert);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center py-12 px-4 sm:px-6 transition-colors duration-300">
      <div className="absolute top-6 right-6 flex gap-2">
        <button
          onClick={() => setLanguage(language === 'id' ? 'en' : 'id')}
          className="p-2 rounded-full border border-[var(--border)] bg-[var(--surface)] text-[var(--text-secondary)] hover:text-[var(--accent)] transition-colors flex items-center justify-center font-bold text-xs"
          title="Toggle Language"
        >
          {language === 'id' ? 'EN' : 'ID'}
        </button>
        <button
          onClick={() => setIsDarkMode(!isDarkMode)}
          className="p-2 rounded-full border border-[var(--border)] bg-[var(--surface)] text-[var(--text-secondary)] hover:text-[var(--accent)] transition-colors"
        >
          {isDarkMode ? (
            <Sun className="w-5 h-5" />
          ) : (
            <Moon className="w-5 h-5" />
          )}
        </button>
      </div>

      <div className="text-center mb-10 mt-8 px-2">
        <div className="inline-flex items-center justify-center p-3 bg-[var(--surface)] rounded-2xl shadow-sm border border-[var(--border)] mb-4 transition-colors">
          <WandSparkles className="w-8 h-8 text-[var(--accent)]" />
        </div>
        <BouncyText 
          text={t.title} 
          className="text-2xl sm:text-3xl font-bold tracking-tight text-[var(--text-primary)]" 
        />
        <p className="mt-2 text-[var(--text-secondary)]">
          {t.subtitle}
        </p>
      </div>

      <div className="w-full max-w-2xl bg-[var(--surface)] rounded-3xl shadow-sm border border-[var(--border)] p-4 sm:p-8 transition-colors">
        {/* State 1: Awal, belum ada gambar */}
        {!selectedFile && <UploadDropzone onFileSelect={handleFileSelect} />}

        {/* State 2: Gambar dipilih & diproses */}
        {selectedFile && !resultUrl && (
          <div className="relative">
            <ImagePreview
              file={selectedFile}
              onClear={() => setSelectedFile(null)}
              onUpscale={handleUpscale}
            />

            {/* Overlay Loading kalau lagi diproses */}
            {isProcessing && (
              <div className="absolute inset-0 bg-[var(--surface)]/80 backdrop-blur-sm rounded-2xl flex flex-col items-center justify-center z-10">
                <Loader2 className="w-10 h-10 text-[var(--accent)] animate-spin mb-4" />
                <p className="font-semibold">{t.processingTitle}</p>
                <p className="text-sm text-[var(--text-muted)] mt-1">
                  {t.processingDesc}
                </p>
              </div>
            )}
          </div>
        )}

        {/* State 3: Hasil Selesai */}
        {resultUrl && (
          <div className="space-y-6 animate-in fade-in zoom-in duration-300">
            <div className="p-4 bg-[var(--success)]/10 border border-[var(--success)]/20 rounded-2xl text-center">
              <p className="font-bold text-[var(--success)]">
                {t.successTitle}
              </p>
            </div>

            <CompareViewer
              originalUrl={URL.createObjectURL(selectedFile!)}
              resultUrl={resultUrl}
            />

            <div className="flex flex-col sm:flex-row gap-4">
              <button
                onClick={() => {
                  setSelectedFile(null);
                  setResultUrl(null);
                }}
                className="flex-1 py-3 px-4 border border-[var(--border)] rounded-xl font-medium hover:bg-[var(--surface-soft)] transition-colors"
              >
                {t.upscaleOther}
              </button>

              <a
                href={resultUrl}
                download={`upscale_x${appliedScale}_${selectedFile?.name}`}
                className="flex-[2] py-3 px-4 bg-[var(--accent)] hover:bg-[#7a8be6] text-white rounded-xl font-bold flex items-center justify-center gap-2 transition-colors shadow-sm"
              >
                <Download className="w-5 h-5" />
                {t.downloadResult}
              </a>
            </div>
          </div>
        )}
        <Footer />
      </div>
    </div>
  );
}

export default App;
