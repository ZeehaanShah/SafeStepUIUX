import { useState } from "react";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { ShieldCheck } from "lucide-react";
import { Button } from "@/components/safestep/ui";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "SafeStep — Your friendly guide to staying safe online" },
      {
        name: "description",
        content:
          "Choose your language and start learning how to spot scam calls, messages, and payment tricks.",
      },
      { property: "og:title", content: "SafeStep — Stay safe online" },
      {
        property: "og:description",
        content: "A warm, patient guide to spotting online scams.",
      },
    ],
  }),
  component: Landing,
});

function Landing() {
  const [language, setLanguage] = useState<"English" | "हिंदी">("English");
  const navigate = useNavigate();

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-8 py-20">
      <div className="flex w-full max-w-[640px] flex-col items-center text-center">
        <ShieldCheck strokeWidth={1.25} className="size-24 text-primary" aria-hidden />
        <h1 className="mt-8 text-[40px] font-bold tracking-tight">SafeStep</h1>
        <p className="mt-4 text-xl text-muted-foreground">
          Your friendly guide to staying safe online.
        </p>

        <p className="mt-16 text-lg font-semibold">Choose the language you prefer</p>
        <div className="mt-6 flex gap-6">
          {(["English", "हिंदी"] as const).map((lang) => (
            <button
              key={lang}
              type="button"
              onClick={() => setLanguage(lang)}
              aria-pressed={language === lang}
              className={
                language === lang
                  ? "min-h-[64px] rounded-full border-2 border-primary bg-primary px-14 text-xl font-semibold text-primary-foreground shadow-soft transition-all duration-200"
                  : "min-h-[64px] rounded-full border-2 border-border bg-card px-14 text-xl font-semibold transition-all duration-200 hover:border-primary hover:bg-primary-soft"
              }
            >
              {lang}
            </button>
          ))}
        </div>

        <div className="mt-14">
          <Button size="lg" onClick={() => navigate({ to: "/login" })}>
            Continue
          </Button>
        </div>
      </div>
    </div>
  );
}
