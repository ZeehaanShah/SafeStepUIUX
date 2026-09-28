import { useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { ChevronDown, Link2, MailSearch, MessageSquareCheck } from "lucide-react";
import { Button, Card, DotTracker, PageHeader } from "@/components/safestep/ui";
import { TermGlyph } from "@/components/safestep/icons";
import { mockWeek, terms, weekDayLabels } from "@/lib/safestep-data";
import { useLang } from "@/lib/i18n";
const weekDots = mockWeek.map((d) => d.check || d.practice);

export const Route = createFileRoute("/_app/recap")({
  head: () => ({
    meta: [
      { title: "My Weekly Recap — SafeStep" },
      {
        name: "description",
        content:
          "A gentle weekly summary of the messages you checked, scenarios you practised, and words you learned.",
      },
      { property: "og:title", content: "My Weekly Recap — SafeStep" },
      { property: "og:description", content: "Your safety week, at a glance." },
    ],
  }),
  component: RecapPage,
});

const learned = terms.slice(0, 3);

function RecapPage() {
  const [openTerm, setOpenTerm] = useState<string | null>(null);
  const [share, setShare] = useState(false);
  const { tx } = useLang();

  return (
    <div>
      <PageHeader title="Your Safety Week" />

      <div className="grid grid-cols-2 gap-6">
        <Card className="flex items-center gap-5">
          <MailSearch strokeWidth={1.5} className="size-10 text-primary" aria-hidden />
          <p className="text-2xl font-bold">5 Messages Checked</p>
        </Card>
        <Card className="flex items-center gap-5">
          <MessageSquareCheck
            strokeWidth={1.5}
            className="size-10 text-primary"
            aria-hidden
          />
          <p className="text-2xl font-bold">3 Scenarios Practiced</p>
        </Card>
      </div>

      <Card className="mt-8">
        <h2 className="text-xl font-bold">Your week, day by day</h2>
        <div className="mt-6">
          <DotTracker days={weekDots} labels={weekDayLabels.map(tx)} />
        </div>
      </Card>

      <section className="mt-8">
        <h2 className="mb-5 text-xl font-bold">Words You Learned This Week</h2>
        <div className="flex flex-col gap-4">
          {learned.map((term) => (
            <Card key={term.id} className="py-6">
              <div className="flex items-center justify-between gap-6">
                <div className="flex items-center gap-4">
                  <TermGlyph name={term.icon} className="size-8" />
                  <span className="text-lg font-bold">{tx(term.name)}</span>
                </div>
                <button
                  type="button"
                  aria-expanded={openTerm === term.id}
                  onClick={() => setOpenTerm(openTerm === term.id ? null : term.id)}
                  className="inline-flex min-h-[48px] items-center gap-2 rounded-full px-5 text-base font-semibold text-primary underline-offset-4 hover:underline"
                >
                  Read more
                  <ChevronDown
                    strokeWidth={2}
                    className={`size-5 transition-transform duration-200 ${openTerm === term.id ? "rotate-180" : ""}`}
                    aria-hidden
                  />
                </button>
              </div>
              {openTerm === term.id ? (
                <p className="mt-5 text-base leading-relaxed">{tx(term.meaning)}</p>
              ) : null}
            </Card>
          ))}
        </div>
      </section>

      <Card className="mt-10">
        <div className="flex items-start justify-between gap-8">
          <div>
            <h2 className="text-xl font-bold">Share this recap with a family member</h2>
            <p className="mt-2 text-base text-muted-foreground">
              They'll see only these counts and the words you learned — never your
              messages, your phone number, or your answers.
            </p>
          </div>
          <button
            type="button"
            role="switch"
            aria-checked={share}
            aria-label="Share this recap with a family member"
            onClick={() => setShare((v) => !v)}
            className={`mt-1 inline-flex h-[40px] w-[72px] shrink-0 items-center rounded-full border-2 transition-colors duration-200 ${share ? "border-primary bg-primary" : "border-border bg-muted"}`}
          >
            <span
              className={`mx-1 size-7 rounded-full bg-card transition-transform duration-200 ${share ? "translate-x-8" : ""}`}
            />
          </button>
        </div>
        {share ? (
          <div className="mt-6">
            <Button variant="secondary">
              <Link2 strokeWidth={2} className="size-5" aria-hidden />
              Copy Share Link
            </Button>
          </div>
        ) : null}
      </Card>
    </div>
  );
}
