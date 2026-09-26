import { useState, type ReactNode } from "react";
import { Link, useNavigate } from "@tanstack/react-router";
import {
  BookOpen,
  CalendarCheck,
  Home,
  LifeBuoy,
  MessageCircleQuestion,
  SearchCheck,
  ShieldCheck,
  UserRound,
} from "lucide-react";
import { Button, Card } from "./ui";

const navItems = [
  { to: "/home", label: "Home", icon: Home },
  { to: "/check", label: "Ask Before You Click", icon: SearchCheck },
  { to: "/words", label: "Learn a Word", icon: BookOpen },
  { to: "/practice", label: "Practice a Scenario", icon: ShieldCheck },
  { to: "/recap", label: "My Weekly Recap", icon: CalendarCheck },
  { to: "/assistant", label: "SafeStep Assistant", icon: MessageCircleQuestion },
  { to: "/account", label: "My Account", icon: UserRound },
] as const;

export function AppShell({ children }: { children: ReactNode }) {
  const [helpOpen, setHelpOpen] = useState(false);
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      <aside className="fixed inset-y-0 left-0 z-30 flex w-[240px] flex-col border-r border-sidebar-border bg-sidebar px-4 py-8">
        <button
          type="button"
          onClick={() => navigate({ to: "/home" })}
          className="mb-10 flex items-center gap-3 px-3 text-left"
        >
          <ShieldCheck strokeWidth={1.5} className="size-9 text-primary" aria-hidden />
          <span className="text-2xl font-bold tracking-tight">SafeStep</span>
        </button>

        <nav className="flex flex-col gap-4">
          {navItems.map(({ to, label, icon: Icon }) => (
            <Link
              key={to}
              to={to}
              className="flex min-h-[56px] items-center gap-3 rounded-xl px-4 py-3 text-base font-medium text-sidebar-foreground transition-colors duration-200 hover:bg-sidebar-accent"
              activeProps={{
                className:
                  "bg-sidebar-accent font-bold text-primary border-l-4 border-l-primary",
              }}
            >
              <Icon strokeWidth={1.5} className="size-6 shrink-0" aria-hidden />
              <span className="leading-snug">{label}</span>
            </Link>
          ))}
        </nav>
      </aside>

      <div className="pl-[240px]">
        <div className="sticky top-0 z-20 flex justify-end bg-background/85 px-10 py-5 backdrop-blur">
          <Button variant="amber" onClick={() => setHelpOpen(true)}>
            <LifeBuoy strokeWidth={1.75} className="size-5" aria-hidden />
            Need Help Now?
          </Button>
        </div>
        <main className="mx-auto w-full max-w-[960px] px-10 pb-24 pt-4">{children}</main>
      </div>

      {helpOpen ? <HelpOverlay onClose={() => setHelpOpen(false)} /> : null}
    </div>
  );
}

const steps = [
  "Hang up the call or don't click anything",
  "Don't share any code, password, or OTP",
  "Call your bank or a trusted family member directly",
];

function HelpOverlay({ onClose }: { onClose: () => void }) {
  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label="Need help now"
      className="fixed inset-0 z-50 overflow-y-auto bg-background px-6 py-16"
    >
      <div className="mx-auto w-full max-w-[600px]">
        <h1 className="text-[32px] font-bold leading-snug">
          If you think this is happening right now, take a breath — here's what to do.
        </h1>
        <div className="mt-10 flex flex-col gap-6">
          {steps.map((step, i) => (
            <Card key={step} className="flex items-center gap-6">
              <span className="flex size-14 shrink-0 items-center justify-center rounded-full bg-primary-soft text-2xl font-bold text-primary">
                {i + 1}
              </span>
              <p className="text-xl font-semibold leading-snug">{step}</p>
            </Card>
          ))}
        </div>
        <div className="mt-12 flex justify-center">
          <Button size="lg" onClick={onClose}>
            I'm okay now, take me back
          </Button>
        </div>
      </div>
    </div>
  );
}
