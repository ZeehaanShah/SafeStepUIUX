import { useNavigate } from "@tanstack/react-router";
import { ArrowRight, ChevronLeft, ChevronRight } from "lucide-react";
import { terms } from "@/lib/safestep-data";
import { TermGlyph } from "./icons";
import { Button, Modal, Pill } from "./ui";

export function TermModal({
  index,
  onClose,
  onChangeIndex,
}: {
  index: number | null;
  onClose: () => void;
  onChangeIndex: (i: number) => void;
}) {
  const navigate = useNavigate();
  if (index === null) return null;
  const term = terms[index];

  return (
    <Modal open onClose={onClose} labelledBy="term-title">
      <div className="flex items-center gap-5">
        <TermGlyph name={term.icon} className="size-14" />
        <div>
          <h2 id="term-title" className="text-[28px] font-bold">
            {term.name}
          </h2>
          <div className="mt-2">
            <Pill tone="teal">{term.category}</Pill>
          </div>
        </div>
      </div>

      <div className="mt-8 space-y-7">
        <Section title="What it means:" body={term.meaning} />
        <Section title="A real example:" body={term.example} />
        <Section title="How to stay safe:" body={term.safety} />
      </div>

      <div className="mt-9">
        <Button
          onClick={() =>
            navigate({
              to: "/practice",
              search: term.scenarioId ? { scenario: term.scenarioId } : {},
            })
          }
        >
          Practice this
          <ArrowRight strokeWidth={2} className="size-5" aria-hidden />
        </Button>
      </div>

      <div className="mt-9 flex items-center justify-between border-t border-border pt-6">
        <Button
          variant="ghost"
          onClick={() => onChangeIndex((index - 1 + terms.length) % terms.length)}
        >
          <ChevronLeft strokeWidth={2} className="size-5" aria-hidden />
          Previous word
        </Button>
        <Button variant="ghost" onClick={() => onChangeIndex((index + 1) % terms.length)}>
          Next word
          <ChevronRight strokeWidth={2} className="size-5" aria-hidden />
        </Button>
      </div>
    </Modal>
  );
}

function Section({ title, body }: { title: string; body: string }) {
  return (
    <div>
      <h3 className="text-lg font-bold text-primary">{title}</h3>
      <p className="mt-2 text-base leading-relaxed">{body}</p>
    </div>
  );
}
