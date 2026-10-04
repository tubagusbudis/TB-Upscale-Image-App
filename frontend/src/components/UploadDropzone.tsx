import { useState, useRef } from "react";
import { motion } from "framer-motion";
import { UploadCloud, Image as ImageIcon } from "lucide-react";
import { useLanguage } from "../contexts/LanguageContext";

interface UploadDropzoneProps {
  onFileSelect: (file: File) => void;
}

export default function UploadDropzone({ onFileSelect }: UploadDropzoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { t } = useLanguage();

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      if (file.type.startsWith("image/")) {
        onFileSelect(file);
      } else {
        alert(t.dropzoneError);
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onFileSelect(e.target.files[0]);
    }
  };

  return (
    <motion.div
      className={`relative flex flex-col items-center justify-center py-16 px-4 border-2 border-dashed rounded-2xl cursor-pointer transition-colors ${
        isDragging
          ? "border-[var(--accent)] bg-[var(--accent-soft)]"
          : "border-[var(--border)] bg-[var(--surface-soft)] hover:bg-gray-50"
      }`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={() => fileInputRef.current?.click()}
      whileHover={{ scale: 0.99 }}
      whileTap={{ scale: 0.97 }}
    >
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept="image/*"
        className="hidden"
      />

      <motion.div
        className="p-4 bg-[var(--surface)] rounded-full shadow-sm mb-4"
        animate={{ y: isDragging ? -10 : 0 }}
      >
        {isDragging ? (
          <UploadCloud className="w-8 h-8 text-[var(--accent)]" />
        ) : (
          <ImageIcon className="w-8 h-8 text-[var(--text-secondary)]" />
        )}
      </motion.div>

      <p className="text-lg font-medium text-[var(--text-primary)]">
        {isDragging
          ? t.dropzoneDrag
          : t.dropzoneIdle}
      </p>
      <p className="text-sm text-[var(--text-muted)] mt-2 text-center">
        {t.dropzoneFormat}
      </p>
    </motion.div>
  );
}
