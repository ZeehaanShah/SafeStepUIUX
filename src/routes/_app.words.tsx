import { useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { Search } from "lucide-react";
import { ClickableCard, PageHeader, Pill } from "@/components/safestep/ui";
import { TermGlyph } from "@/components/safestep/icons";
import { TermModal } from "@/components/safestep/term-modal";
import { termCategories, terms } from "@/lib/safestep-data";

export const Route = createFileRoute("/_app/words")({
  validateSearch: (search: Record<string, unknown>): { term?: string } => {
    const value = search["term"];
    return typeof value === "string" ? { term: value } : {};
  },
  head: () => ({
    meta: [
      { title: "Learn a Word — SafeStep" },
      {
        name: "description",
        content:
          "Plain-language explanations of phishing, vishing, OTP fraud, QR code scams and more.",
      },
      { property: "og:title", content: "Learn a Word — SafeStep" },
      {
        property: "og:description",
        content: "Simple explanations for tricky online-safety terms.",
      },
    ],
  }),
  component: WordsPage,
});

function WordsPage() {
  const { term: termParam } = Route.useSearch();
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState<(typeof termCategories)[number]>("All");
  const [openIndex, setOpenIndex] = useState<number | null>(() => {
    const i = terms.findIndex((t) => t.id === termParam);
    return i >= 0 ? i : null;
  });

  const visible = terms.filter(
    (t) =>
      (category === "All" || t.category === category) &&
      t.name.toLowerCase().includes(query.trim().toLowerCase()),
  );

  return (
    <div>
      <PageHeader
        title="Learn a Word"
        subtitle="Simple explanations for tricky terms — so you always know what you're dealing with."
      />

      <div className="relative">
        <Search
          strokeWidth={1.75}
          className="pointer-events-none absolute left-5 top-1/2 size-6 -translate-y-1/2 text-muted-foreground"
          aria-hidden
        />
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search a word..."
          aria-label="Search a word"
          className="h-[60px] w-full rounded-full border-2 border-input bg-card pl-14 pr-6 text-lg"
        />
      </div>

      <div className="mt-6 flex flex-wrap gap-4">
        {termCategories.map((c) => (
          <Pill key={c} active={category === c} onClick={() => setCategory(c)}>
            {c}
          </Pill>
        ))}
      </div>

      <div className="mt-10 grid grid-cols-3 gap-6">
        {visible.map((term) => (
          <ClickableCard
            key={term.id}
            ariaLabel={`Open ${term.name}`}
            onClick={() => setOpenIndex(terms.findIndex((t) => t.id === term.id))}
            className="flex flex-col gap-4"
          >
            <TermGlyph name={term.icon} className="size-10" />
            <span className="text-xl font-bold leading-snug">{term.name}</span>
            <span>
              <Pill tone="teal">{term.category}</Pill>
            </span>
          </ClickableCard>
        ))}
      </div>

      {visible.length === 0 ? (
        <p className="mt-10 text-lg text-muted-foreground">
          No words match that search yet. Try a shorter word.
        </p>
      ) : null}

      <TermModal
        index={openIndex}
        onClose={() => setOpenIndex(null)}
        onChangeIndex={setOpenIndex}
      />
    </div>
  );
}
