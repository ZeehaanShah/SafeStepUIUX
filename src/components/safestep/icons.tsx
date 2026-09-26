import {
  AlertTriangle,
  BadgeCheck,
  CreditCard,
  Lock,
  Mail,
  Phone,
  QrCode,
  Smile,
  Video,
  Anchor,
} from "lucide-react";

type Props = { name: string; className?: string };

/**
 * Composite line-art icons: a base outlined Lucide icon plus a small badge glyph,
 * so each glossary term has its own recognisable mark.
 */
export function TermGlyph({ name, className = "size-8" }: Props) {
  const base = "text-primary";
  const badge =
    "absolute -bottom-1 -right-1 size-4 rounded-full bg-card text-accent-foreground";

  const map: Record<string, { Base: typeof Mail; Badge?: typeof Anchor; badgeTone?: string }> = {
    "mail-hook": { Base: Mail, Badge: Anchor },
    "phone-mail": { Base: Phone, Badge: Mail },
    "phone-warning": { Base: Phone, Badge: AlertTriangle, badgeTone: "text-risk" },
    "face-question": { Base: Smile, Badge: AlertTriangle, badgeTone: "text-risk" },
    "lock-dots": { Base: Lock, Badge: BadgeCheck },
    "video-badge": { Base: Video, Badge: BadgeCheck },
    "qr-warning": { Base: QrCode, Badge: AlertTriangle, badgeTone: "text-risk" },
    "card-warning": { Base: CreditCard, Badge: AlertTriangle, badgeTone: "text-risk" },
  };

  const entry = map[name] ?? { Base: Mail };
  const { Base, Badge, badgeTone } = entry;

  return (
    <span className="relative inline-flex shrink-0">
      <Base strokeWidth={1.5} className={`${base} ${className}`} aria-hidden />
      {Badge ? (
        <Badge
          strokeWidth={2}
          className={`${badge} ${badgeTone ?? "text-accent"} p-[1px]`}
          aria-hidden
        />
      ) : null}
    </span>
  );
}
