import { useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { Mic, Send } from "lucide-react";
import { PageHeader, RiskMeter } from "@/components/safestep/ui";
import { AlertTriangle } from "lucide-react";

export const Route = createFileRoute("/_app/assistant")({
  validateSearch: (search: Record<string, unknown>) => ({
    message: typeof search.message === "string" ? search.message : undefined,
  }),
  head: () => ({
    meta: [
      { title: "SafeStep Assistant — SafeStep" },
      {
        name: "description",
        content:
          "Ask the SafeStep Assistant about a message or a word, and get a calm, plain-language answer.",
      },
      { property: "og:title", content: "SafeStep Assistant" },
      {
        property: "og:description",
        content: "Ask anything about a message you received.",
      },
    ],
  }),
  component: AssistantPage,
});

type Msg =
  | { id: number; role: "user"; text: string }
  | { id: number; role: "bot"; text: string; risk?: number; reasons?: string[] };

const suggestions = [
  "Is this message safe?",
  "What is vishing?",
  "Someone asked for my OTP",
  "How do I check a QR code?",
];

let nextId = 3;

function AssistantPage() {
  const { message } = Route.useSearch();
  const [input, setInput] = useState(message ?? "");
  const [messages, setMessages] = useState<Msg[]>([
    {
      id: 1,
      role: "bot",
      text: "Hello! I'm here to help. You can paste a message you received, or ask me what a word means.",
    },
  ]);

  function send(text: string) {
    const clean = text.trim();
    if (!clean) return;
    const user: Msg = { id: nextId++, role: "user", text: clean };
    const bot: Msg = {
      id: nextId++,
      role: "bot",
      text: "Let's look at this together. Here's how it reads to me:",
      risk: 78,
      reasons: [
        "It creates a sense of urgency",
        "It asks you to click a link or share a code",
        "The sender isn't someone you already know",
      ],
    };
    setMessages((m) => [...m, user, bot]);
    setInput("");
  }

  return (
    <div>
      <PageHeader title="SafeStep Assistant" />
      <div className="grid grid-cols-[240px_1fr] gap-8 items-start">
        <aside>
          <h2 className="text-base font-bold">You can ask me things like...</h2>
          <div className="mt-4 flex flex-col gap-3">
            {suggestions.map((s) => (
              <button
                key={s}
                type="button"
                onClick={() => send(s)}
                className="min-h-[52px] rounded-2xl border-2 border-border bg-card px-5 py-3 text-left text-base transition-all duration-200 hover:border-primary hover:bg-primary-soft"
              >
                {s}
              </button>
            ))}
          </div>
        </aside>

        <div className="card-surface flex h-[620px] flex-col p-6">
          <div className="flex-1 space-y-6 overflow-y-auto pr-2">
            {messages.map((m) =>
              m.role === "user" ? (
                <div key={m.id} className="flex justify-end">
                  <p className="max-w-[80%] rounded-2xl bg-primary p-4 text-base text-primary-foreground">
                    {m.text}
                  </p>
                </div>
              ) : (
                <div key={m.id} className="flex justify-start">
                  <div className="max-w-[85%] rounded-2xl bg-muted p-4 text-base">
                    <p>{m.text}</p>
                    {m.risk !== undefined ? (
                      <div className="mt-5">
                        <RiskMeter value={m.risk} />
                        <ul className="mt-5 space-y-3">
                          {(m.reasons ?? []).map((r) => (
                            <li key={r} className="flex items-start gap-3">
                              <AlertTriangle
                                strokeWidth={1.75}
                                className="mt-1 size-5 shrink-0 text-risk"
                                aria-hidden
                              />
                              <span>{r}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    ) : null}
                  </div>
                </div>
              ),
            )}
          </div>

          <div className="mt-6 flex items-center gap-4 border-t border-border pt-6">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") send(input);
              }}
              aria-label="Type your question"
              placeholder="Type your question here..."
              className="h-[60px] flex-1 rounded-full border-2 border-input bg-card px-6 text-lg"
            />
            <button
              type="button"
              aria-label="Tap to speak"
              className="inline-flex min-h-[60px] items-center gap-2 rounded-full border-2 border-accent bg-card px-6 text-base font-semibold transition-all duration-200 hover:bg-accent-soft"
            >
              <Mic strokeWidth={1.75} className="size-6" aria-hidden />
              Tap to speak
            </button>
            <button
              type="button"
              onClick={() => send(input)}
              aria-label="Send message"
              className="inline-flex size-[60px] items-center justify-center rounded-full bg-primary text-primary-foreground transition-all duration-200 hover:bg-primary/90"
            >
              <Send strokeWidth={2} className="size-6" aria-hidden />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
