import { useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { ArrowLeft } from "lucide-react";
import {
  BadgeMoment,
  Button,
  Card,
  ClickableCard,
  PageHeader,
} from "@/components/safestep/ui";
import { TermGlyph } from "@/components/safestep/icons";
import { scenarios } from "@/lib/safestep-data";

export const Route = createFileRoute("/_app/practice")({
  validateSearch: (search: Record<string, unknown>) => ({
    scenario: typeof search.scenario === "string" ? search.scenario : undefined,
  }),
  head: () => ({
    meta: [
      { title: "Practice a Scenario — SafeStep" },
      {
        name: "description",
        content:
          "Try real-life scam situations in a safe space — no score, no judgement, just practice.",
      },
      { property: "og:title", content: "Practice a Scenario — SafeStep" },
      {
        property: "og:description",
        content: "A safe space to practise what you'd do.",
      },
    ],
  }),
  component: PracticePage,
});

function PracticePage() {
  const { scenario: scenarioParam } = Route.useSearch();
  const [activeId, setActiveId] = useState<string | null>(scenarioParam ?? null);
  const [choice, setChoice] = useState<number | null>(null);
  const [celebrate, setCelebrate] = useState(false);

  const active = scenarios.find((s) => s.id === activeId) ?? null;

  function reset() {
    setActiveId(null);
    setChoice(null);
    setCelebrate(false);
  }

  if (!active) {
    return (
      <div>
        <PageHeader title="Let's practice — this is a safe space to try things out." />
        <div className="grid grid-cols-3 gap-6">
          {scenarios.map((s) => (
            <ClickableCard
              key={s.id}
              onClick={() => setActiveId(s.id)}
              className="flex flex-col gap-4"
            >
              <TermGlyph name={s.icon} className="size-10" />
              <span className="text-xl font-bold leading-snug">{s.title}</span>
              <span className="text-base text-muted-foreground">{s.blurb}</span>
            </ClickableCard>
          ))}
        </div>
      </div>
    );
  }

  const selected = choice !== null ? active.options[choice] : null;

  return (
    <div>
      <button
        type="button"
        onClick={reset}
        className="mb-6 inline-flex items-center gap-2 text-base font-semibold text-primary underline-offset-4 hover:underline"
      >
        <ArrowLeft strokeWidth={2} className="size-5" aria-hidden />
        All scenarios
      </button>

      <PageHeader title={active.title} />

      <div className="card-surface relative rounded-2xl bg-primary-soft p-8">
        <p className="text-xl leading-relaxed">{active.situation}</p>
      </div>

      <div className="mt-8 flex flex-col gap-4">
        {active.options.map((opt, i) => (
          <button
            key={opt.label}
            type="button"
            onClick={() => {
              setChoice(i);
              setCelebrate(false);
            }}
            className={
              choice === i
                ? "min-h-[64px] w-full rounded-2xl border-2 border-primary bg-primary-soft px-8 py-4 text-left text-lg font-semibold transition-all duration-200"
                : "min-h-[64px] w-full rounded-2xl border-2 border-border bg-card px-8 py-4 text-left text-lg font-semibold transition-all duration-200 hover:border-primary hover:shadow-lift"
            }
          >
            <span className="mr-3 font-bold text-primary">{i === 0 ? "A" : "B"}</span>
            {opt.label}
          </button>
        ))}
      </div>

      {selected ? (
        <div className="mt-8">
          <Card
            className={`border-l-8 ${selected.safe ? "border-l-safe" : "border-l-accent"}`}
          >
            <p className="text-lg leading-relaxed">{selected.feedback}</p>
            {!celebrate ? (
              <div className="mt-6">
                <Button onClick={() => setCelebrate(true)}>Continue</Button>
              </div>
            ) : null}
          </Card>
          {celebrate ? (
            <div className="mt-6">
              <BadgeMoment badge={active.badge} />
              <div className="mt-6">
                <Button variant="secondary" onClick={reset}>
                  Try another scenario
                </Button>
              </div>
            </div>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
