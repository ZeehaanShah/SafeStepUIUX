import { useState } from "react";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Button, Card, PageHeader } from "@/components/safestep/ui";
import { mockUser } from "@/lib/safestep-data";

export const Route = createFileRoute("/_app/account")({
  head: () => ({
    meta: [
      { title: "My Account — SafeStep" },
      {
        name: "description",
        content: "Your SafeStep profile, language preference, and notification settings.",
      },
      { property: "og:title", content: "My Account — SafeStep" },
      { property: "og:description", content: "Your profile and simple settings." },
    ],
  }),
  component: AccountPage,
});

function Toggle({
  label,
  checked,
  onChange,
}: {
  label: string;
  checked: boolean;
  onChange: (v: boolean) => void;
}) {
  return (
    <div className="flex items-center justify-between gap-8 py-4">
      <span className="text-lg">{label}</span>
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        aria-label={label}
        onClick={() => onChange(!checked)}
        className={`inline-flex h-[40px] w-[72px] shrink-0 items-center rounded-full border-2 transition-colors duration-200 ${checked ? "border-primary bg-primary" : "border-border bg-muted"}`}
      >
        <span
          className={`mx-1 size-7 rounded-full bg-card transition-transform duration-200 ${checked ? "translate-x-8" : ""}`}
        />
      </button>
    </div>
  );
}

function AccountPage() {
  const [language, setLanguage] = useState<"English" | "हिंदी">("English");
  const [weekly, setWeekly] = useState(true);
  const [tips, setTips] = useState(false);
  const navigate = useNavigate();

  return (
    <div>
      <PageHeader title="My Account" />

      <Card>
        <h2 className="text-xl font-bold">Your details</h2>
        <dl className="mt-6 space-y-5 text-lg">
          <div className="flex justify-between gap-8">
            <dt className="text-muted-foreground">Name</dt>
            <dd className="font-semibold">{mockUser.name}</dd>
          </div>
          <div className="flex justify-between gap-8">
            <dt className="text-muted-foreground">Phone number</dt>
            <dd className="font-semibold">{mockUser.phoneMasked}</dd>
          </div>
        </dl>

        <div className="mt-8">
          <p className="text-lg font-semibold">Language</p>
          <div className="mt-4 flex gap-4">
            {(["English", "हिंदी"] as const).map((lang) => (
              <button
                key={lang}
                type="button"
                aria-pressed={language === lang}
                onClick={() => setLanguage(lang)}
                className={
                  language === lang
                    ? "min-h-[48px] rounded-full border-2 border-primary bg-primary px-8 text-base font-semibold text-primary-foreground"
                    : "min-h-[48px] rounded-full border-2 border-border bg-card px-8 text-base font-semibold transition-colors duration-200 hover:border-primary hover:bg-primary-soft"
                }
              >
                {lang}
              </button>
            ))}
          </div>
        </div>
      </Card>

      <Card className="mt-8">
        <h2 className="text-xl font-bold">Notification preferences</h2>
        <div className="mt-4 divide-y divide-border">
          <Toggle label="Send me my weekly recap" checked={weekly} onChange={setWeekly} />
          <Toggle label="Send me an occasional safety tip" checked={tips} onChange={setTips} />
        </div>
      </Card>

      <div className="mt-12">
        <Button variant="muted" onClick={() => navigate({ to: "/" })}>
          Log out
        </Button>
      </div>
    </div>
  );
}
