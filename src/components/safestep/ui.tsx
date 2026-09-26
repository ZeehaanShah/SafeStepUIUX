import type { ButtonHTMLAttributes, ReactNode } from "react";
import { cn } from "@/lib/utils";
import { AlertTriangle, PartyPopper, X } from "lucide-react";

/* ---------------- Button ---------------- */

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "ghost" | "amber" | "muted";
  size?: "md" | "lg";
};

export function Button({
  variant = "primary",
  size = "md",
  className,
  ...props
}: ButtonProps) {
  return (
    <button
      {...props}
      className={cn(
        "inline-flex items-center justify-center gap-3 rounded-full font-semibold transition-all duration-200 disabled:pointer-events-none disabled:opacity-50",
        size === "lg" ? "min-h-[60px] px-10 text-xl" : "min-h-[48px] px-8 text-base",
        variant === "primary" &&
          "bg-primary text-primary-foreground shadow-soft hover:-translate-y-[1px] hover:bg-primary/90 hover:shadow-lift",
        variant === "secondary" &&
          "border-2 border-primary bg-card text-primary hover:bg-primary-soft hover:shadow-soft",
        variant === "amber" &&
          "border-2 border-accent bg-card text-accent-foreground hover:bg-accent-soft hover:shadow-soft",
        variant === "ghost" && "text-primary underline-offset-4 hover:underline",
        variant === "muted" &&
          "border border-border bg-card text-muted-foreground hover:bg-muted",
        className,
      )}
    />
  );
}

/* ---------------- Card ---------------- */

export function Card({
  className,
  children,
}: {
  className?: string;
  children: ReactNode;
}) {
  return <div className={cn("card-surface p-8", className)}>{children}</div>;
}

export function ClickableCard({
  className,
  children,
  onClick,
  ariaLabel,
}: {
  className?: string;
  children: ReactNode;
  onClick: () => void;
  ariaLabel?: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={ariaLabel}
      className={cn("card-interactive p-7", className)}
    >
      {children}
    </button>
  );
}

/* ---------------- Pill (filter / tag) ---------------- */

export function Pill({
  children,
  active,
  onClick,
  tone = "neutral",
}: {
  children: ReactNode;
  active?: boolean;
  onClick?: () => void;
  tone?: "neutral" | "teal";
}) {
  const base =
    "inline-flex items-center rounded-full px-5 py-2 text-sm font-semibold transition-colors duration-200";
  if (!onClick) {
    return (
      <span
        className={cn(
          base,
          tone === "teal"
            ? "bg-primary-soft text-primary"
            : "bg-muted text-muted-foreground",
        )}
      >
        {children}
      </span>
    );
  }
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        base,
        "min-h-[48px] px-6 text-base",
        active
          ? "bg-primary text-primary-foreground"
          : "border-2 border-border bg-card text-foreground hover:border-primary hover:bg-primary-soft",
      )}
    >
      {children}
    </button>
  );
}

/* ---------------- Page header ---------------- */

export function PageHeader({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <header className="mb-10">
      <h1 className="text-[32px] font-bold tracking-tight">{title}</h1>
      {subtitle ? (
        <p className="mt-3 max-w-2xl text-lg text-muted-foreground">{subtitle}</p>
      ) : null}
    </header>
  );
}

/* ---------------- Dot tracker ---------------- */

export function DotTracker({
  days,
  labels,
}: {
  days: boolean[];
  labels?: string[];
}) {
  return (
    <div className="flex gap-5">
      {days.map((filled, i) => (
        <div key={i} className="flex flex-col items-center gap-2">
          <span
            className={cn(
              "size-6 rounded-full border-2",
              filled ? "border-primary bg-primary" : "border-border bg-transparent",
            )}
          />
          {labels ? (
            <span className="text-sm text-muted-foreground">{labels[i]}</span>
          ) : null}
        </div>
      ))}
    </div>
  );
}

/* ---------------- Result card ---------------- */

export function ResultCard({
  safe,
  verdict,
  flags,
  action,
  footer,
}: {
  safe: boolean;
  verdict: string;
  flags: string[];
  action: string;
  footer?: ReactNode;
}) {
  return (
    <div
      className={cn(
        "card-surface overflow-hidden border-l-8 p-8",
        safe ? "border-l-safe" : "border-l-risk",
      )}
    >
      <p className={cn("text-2xl font-bold", safe ? "text-safe" : "text-risk")}>
        {verdict}
      </p>
      <ul className="mt-6 space-y-4">
        {flags.map((flag) => (
          <li key={flag} className="flex items-start gap-3 text-base">
            <AlertTriangle
              strokeWidth={1.75}
              className={cn("mt-1 size-5 shrink-0", safe ? "text-safe" : "text-risk")}
              aria-hidden
            />
            <span>{flag}</span>
          </li>
        ))}
      </ul>
      <p className="mt-6 rounded-xl bg-muted p-5 text-base font-bold">{action}</p>
      {footer ? <div className="mt-6">{footer}</div> : null}
    </div>
  );
}

/* ---------------- Risk meter ---------------- */

export function RiskMeter({ value }: { value: number }) {
  const pct = Math.min(100, Math.max(0, value));
  return (
    <div className="w-full">
      <div className="relative h-4 w-full rounded-full bg-gradient-to-r from-safe via-accent to-risk">
        <span
          className="absolute top-1/2 size-7 -translate-x-1/2 -translate-y-1/2 rounded-full border-4 border-card bg-foreground shadow-soft"
          style={{ left: `${pct}%` }}
          aria-hidden
        />
      </div>
      <div className="mt-3 flex justify-between text-sm font-semibold">
        <span className="text-safe">Safe</span>
        <span className="text-risk">Risky</span>
      </div>
    </div>
  );
}

/* ---------------- Badge moment ---------------- */

export function BadgeMoment({ badge }: { badge: string }) {
  return (
    <div className="card-surface flex items-center gap-5 border-l-8 border-l-accent bg-accent-soft p-7">
      <PartyPopper strokeWidth={1.5} className="size-10 text-accent-foreground" aria-hidden />
      <div>
        <p className="text-xl font-bold">You earned the “{badge}” badge</p>
        <p className="text-base text-muted-foreground">
          You're doing great — one more safe decision under your belt.
        </p>
      </div>
    </div>
  );
}

/* ---------------- Modal ---------------- */

export function Modal({
  open,
  onClose,
  labelledBy,
  children,
  width = "600px",
}: {
  open: boolean;
  onClose: () => void;
  labelledBy?: string;
  children: ReactNode;
  width?: string;
}) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-foreground/45 p-10 backdrop-blur-[2px]">
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby={labelledBy}
        className="card-surface relative my-auto w-full p-10"
        style={{ maxWidth: width }}
      >
        <button
          type="button"
          onClick={onClose}
          aria-label="Close"
          className="absolute right-6 top-6 inline-flex size-12 items-center justify-center rounded-full border-2 border-border bg-card transition-colors duration-200 hover:border-primary hover:bg-primary-soft"
        >
          <X strokeWidth={2} className="size-6" aria-hidden />
        </button>
        {children}
      </div>
    </div>
  );
}
