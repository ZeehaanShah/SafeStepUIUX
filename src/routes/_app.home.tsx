import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { ArrowRight, MailSearch, MessageSquareCheck, ShieldCheck } from "lucide-react";
import { Button, Card, ClickableCard, DotTracker } from "@/components/safestep/ui";
import { TermGlyph } from "@/components/safestep/icons";
import { mockUser, terms, weekDots } from "@/lib/safestep-data";

export const Route = createFileRoute("/_app/home")({
  head: () => ({
    meta: [
      { title: "Home — SafeStep" },
      {
        name: "description",
        content:
          "Your SafeStep home: check a message, practise a scenario, and see this week's safe decisions.",
      },
      { property: "og:title", content: "Home — SafeStep" },
      {
        property: "og:description",
        content: "Check a message, practise a scenario, and see your week.",
      },
    ],
  }),
  component: HomePage,
});

function HomePage() {
  const navigate = useNavigate();
  const today = new Date().toLocaleDateString("en-IN", {
    weekday: "long",
    day: "numeric",
    month: "long",
  });

  return (
    <div>
      <header className="mb-10">
        <h1 className="text-[28px] font-bold">Good morning, {mockUser.name}</h1>
        <p className="mt-2 text-base text-muted-foreground">{today}</p>
      </header>

      <Card className="flex items-center justify-between gap-10">
        <div className="flex items-center gap-4">
          <ShieldCheck strokeWidth={1.5} className="size-10 text-primary" aria-hidden />
          <p className="text-2xl font-bold">3 Safe Decisions This Week</p>
        </div>
        <DotTracker days={weekDots} />
      </Card>

      <div className="mt-8 grid grid-cols-2 gap-6">
        <ClickableCard onClick={() => navigate({ to: "/check" })}>
          <MailSearch strokeWidth={1.5} className="size-10 text-primary" aria-hidden />
          <h2 className="mt-5 text-xl font-bold">Check a Message</h2>
          <p className="mt-2 text-base text-muted-foreground">
            Paste anything that felt odd and we'll look at it together.
          </p>
        </ClickableCard>
        <ClickableCard onClick={() => navigate({ to: "/practice" })}>
          <MessageSquareCheck
            strokeWidth={1.5}
            className="size-10 text-primary"
            aria-hidden
          />
          <h2 className="mt-5 text-xl font-bold">Practice a Scenario</h2>
          <p className="mt-2 text-base text-muted-foreground">
            Try a real-life situation in a safe space, with no score.
          </p>
        </ClickableCard>
      </div>

      <section className="mt-12">
        <div className="mb-5 flex items-end justify-between">
          <h2 className="text-xl font-bold">Learn a Word</h2>
          <Link
            to="/words"
            className="inline-flex items-center gap-2 text-base font-semibold text-primary underline-offset-4 hover:underline"
          >
            See all words
            <ArrowRight strokeWidth={2} className="size-5" aria-hidden />
          </Link>
        </div>
        <div className="grid grid-cols-5 gap-4">
          {terms.slice(0, 5).map((term) => (
            <ClickableCard
              key={term.id}
              className="flex flex-col items-center gap-3 p-5 text-center"
              onClick={() => navigate({ to: "/words", search: { term: term.id } })}
            >
              <TermGlyph name={term.icon} className="size-8" />
              <span className="text-base font-semibold leading-snug">{term.name}</span>
            </ClickableCard>
          ))}
        </div>
      </section>

      <Card className="mt-12 flex items-center justify-between gap-8 py-6">
        <div>
          <h2 className="text-xl font-bold">This Week's Recap</h2>
          <p className="mt-1 text-base text-muted-foreground">
            A gentle look back at everything you did this week.
          </p>
        </div>
        <Button variant="secondary" onClick={() => navigate({ to: "/recap" })}>
          View Recap
        </Button>
      </Card>
    </div>
  );
}
