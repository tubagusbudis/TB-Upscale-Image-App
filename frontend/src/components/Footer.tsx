import { useLanguage } from "../contexts/LanguageContext";

export default function Footer() {
  const currentYear = new Date().getFullYear();
  const { t } = useLanguage();

  return (
    <footer className="mt-16 text-center text-sm text-[var(--text-muted)] transition-colors">
      <p>
        © {currentYear}{" "}
        <span className="font-semibold text-[var(--text-secondary)]">
          {t.title}
        </span>
        . {t.developedBy}{" "}
        <span className="font-semibold text-[var(--accent)]">Tubagus Budi S</span>.
      </p>
      <p className="mt-1 text-xs">{t.poweredBy}</p>
    </footer>
  );
}
