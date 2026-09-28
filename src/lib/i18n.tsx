import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";

export type Lang = "en" | "hi";
export type L = { en: string; hi: string };

const STORAGE_KEY = "safestep.lang";

type Ctx = {
  lang: Lang;
  setLang: (l: Lang) => void;
  /** Pick a string for the current language. */
  t: (en: string, hi: string) => string;
  /** Pick from a bilingual content object. */
  tx: (value: L) => string;
};

const LanguageContext = createContext<Ctx | null>(null);

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>("en");

  useEffect(() => {
    const saved = window.localStorage.getItem(STORAGE_KEY);
    if (saved === "hi" || saved === "en") setLangState(saved);
  }, []);

  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);

  const setLang = useCallback((l: Lang) => {
    setLangState(l);
    window.localStorage.setItem(STORAGE_KEY, l);
  }, []);

  const t = useCallback((en: string, hi: string) => (lang === "hi" ? hi : en), [lang]);
  const tx = useCallback((v: L) => (lang === "hi" ? v.hi : v.en), [lang]);

  return (
    <LanguageContext.Provider value={{ lang, setLang, t, tx }}>{children}</LanguageContext.Provider>
  );
}

export function useLang() {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error("useLang must be used inside LanguageProvider");
  return ctx;
}
