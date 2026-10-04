import React, { createContext, useContext, useState, ReactNode } from 'react';

type Language = 'id' | 'en';

interface Translations {
  title: string;
  subtitle: string;
  dropzoneDrag: string;
  dropzoneIdle: string;
  dropzoneFormat: string;
  dropzoneError: string;
  selectResolution: string;
  startUpscale: string;
  processingTitle: string;
  processingDesc: string;
  successTitle: string;
  upscaleOther: string;
  downloadResult: string;
  uploadError: string;
  uploadErrorAlert: string;
  original: string;
  upscaled: string;
  developedBy: string;
  poweredBy: string;
}

const translations: Record<Language, Translations> = {
  id: {
    title: "TB. Upscale Studio",
    subtitle: "Personal AI Image Enhancer",
    dropzoneDrag: "Lepaskan gambar di sini",
    dropzoneIdle: "Klik atau seret gambar ke sini",
    dropzoneFormat: "Support format JPG, PNG, WebP (Max 25MB)",
    dropzoneError: "Tolong upload file gambar ya!",
    selectResolution: "Pilih Target Resolusi:",
    startUpscale: "Mulai Upscale",
    processingTitle: "AI sedang bekerja...",
    processingDesc: "Ini mungkin memakan waktu beberapa menit (Mode GPU).",
    successTitle: "Yeay! Upscale berhasil.",
    upscaleOther: "Upscale Gambar Lain",
    downloadResult: "Download Hasil",
    uploadError: "Gagal memproses gambar",
    uploadErrorAlert: "Waduh, terjadi kesalahan saat upscale.",
    original: "Original",
    upscaled: "Upscaled",
    developedBy: "Developed with ❤️ by",
    poweredBy: "Powered by Real-ESRGAN & FastAPI"
  },
  en: {
    title: "TB. Upscale Studio",
    subtitle: "Personal AI Image Enhancer",
    dropzoneDrag: "Drop image here",
    dropzoneIdle: "Click or drag image here",
    dropzoneFormat: "Supports JPG, PNG, WebP (Max 25MB)",
    dropzoneError: "Please upload an image file!",
    selectResolution: "Select Target Resolution:",
    startUpscale: "Start Upscale",
    processingTitle: "AI is working...",
    processingDesc: "This might take a few minutes (GPU Mode).",
    successTitle: "Yay! Upscale successful.",
    upscaleOther: "Upscale Another Image",
    downloadResult: "Download Result",
    uploadError: "Failed to process image",
    uploadErrorAlert: "Oops, an error occurred during upscale.",
    original: "Original",
    upscaled: "Upscaled",
    developedBy: "Developed with ❤️ by",
    poweredBy: "Powered by Real-ESRGAN & FastAPI"
  }
};

interface LanguageContextProps {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: Translations;
}

const LanguageContext = createContext<LanguageContextProps | undefined>(undefined);

export const LanguageProvider = ({ children }: { children: ReactNode }) => {
  const [language, setLanguage] = useState<Language>('id');

  const t = translations[language];

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};
