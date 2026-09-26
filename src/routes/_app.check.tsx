import { useState } from "react";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Button, PageHeader, ResultCard } from "@/components/safestep/ui";

export const Route = createFileRoute("/_app/check")({
  head: () => ({
    meta: [
      { title: "Ask Before You Click — SafeStep" },
      {
        name: "description",
        content:
          "Paste a message you received and SafeStep explains, in plain words, whether it looks risky.",
      },
      { property: "og:title", content: "Ask Before You Click — SafeStep" },
      {
        property: "og:description",
        content: "Not sure about a message? Let's check it together.",
      },
    ],
  }),
  component: CheckPage,
});

const riskyWords = ["otp", "click", "link", "urgent", "blocked", "verify", "prize", "win"];

function CheckPage() {
  const [message, setMessage] = useState("");
  const [checked, setChecked] = useState<null | { safe: boolean }>(null);
  const navigate = useNavigate();

  const risky = riskyWords.some((w) => message.toLowerCase().includes(w));

  return (
    <div>
      <PageHeader title="Not sure about a message? Let's check it together." />

      <div className={checked ? "grid grid-cols-[55fr_45fr] gap-8 items-start" : ""}>
        <div>
          <label htmlFor="message" className="sr-only">
            The message you received
          </label>
          <textarea
            id="message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Paste or type the message you received here..."
            className="min-h-[160px] w-full rounded-2xl border-2 border-input bg-card p-6 text-lg leading-relaxed"
          />
          <div className="mt-6">
            <Button onClick={() => setChecked({ safe: !risky })} disabled={!message.trim()}>
              Check It
            </Button>
          </div>
        </div>

        {checked ? (
          <ResultCard
            safe={checked.safe}
            verdict={checked.safe ? "This looks safe" : "This looks risky"}
            flags={
              checked.safe
                ? [
                    "No links asking you to act quickly",
                    "Nothing is asking for a code or password",
                    "The wording is calm, not urgent",
                  ]
                : [
                    "Creates urgency",
                    "Asks you to click a link",
                    "Message is from an unknown number",
                  ]
            }
            action={
              checked.safe
                ? "Looks fine — but if money or a code is ever mentioned, come back and check again."
                : "Don't click this — call your bank directly using the number on your card."
            }
            footer={
              <Button
                variant="ghost"
                onClick={() => navigate({ to: "/assistant", search: { message } })}
              >
                Still unsure? Ask SafeStep Assistant
              </Button>
            }
          />
        ) : null}
      </div>
    </div>
  );
}
