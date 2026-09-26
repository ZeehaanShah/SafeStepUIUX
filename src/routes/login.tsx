import { useState } from "react";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { ChevronDown } from "lucide-react";
import { Button } from "@/components/safestep/ui";
import illustration from "@/assets/login-illustration.jpg";

export const Route = createFileRoute("/login")({
  head: () => ({
    meta: [
      { title: "Sign in — SafeStep" },
      {
        name: "description",
        content: "Sign in to SafeStep with your phone number and a one-time code.",
      },
      { property: "og:title", content: "Sign in — SafeStep" },
      {
        property: "og:description",
        content: "Sign in with your phone number and a one-time code.",
      },
    ],
  }),
  component: Login,
});

function Login() {
  const [step, setStep] = useState<"phone" | "otp">("phone");
  const [phone, setPhone] = useState("");
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const [explain, setExplain] = useState(false);
  const navigate = useNavigate();

  return (
    <div className="grid min-h-screen grid-cols-2">
      <div className="flex flex-col items-center justify-center gap-8 bg-primary-soft px-16 py-20">
        <img
          src={illustration}
          alt="An older woman calmly using her phone"
          width={1024}
          height={1024}
          className="w-full max-w-[420px] rounded-2xl"
        />
        <p className="max-w-[420px] text-center text-2xl font-semibold leading-snug text-primary">
          Your friendly guide to staying safe online.
        </p>
      </div>

      <div className="flex items-center justify-center px-16 py-20">
        <div className="w-full max-w-[420px]">
          <h1 className="text-[32px] font-bold">Welcome back</h1>
          <p className="mt-3 text-lg text-muted-foreground">
            We'll send a short code to your phone. No passwords to remember.
          </p>

          {step === "phone" ? (
            <div className="mt-10">
              <label htmlFor="phone" className="text-lg font-semibold">
                Your phone number
              </label>
              <input
                id="phone"
                inputMode="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="98765 43210"
                className="mt-3 h-[60px] w-full rounded-xl border-2 border-input bg-card px-5 text-xl"
              />
              <div className="mt-8">
                <Button onClick={() => setStep("otp")}>Send Code</Button>
              </div>
            </div>
          ) : (
            <div className="mt-10">
              <p className="text-lg font-semibold">Enter the 6-digit code we sent</p>
              <div className="mt-4 flex gap-3">
                {otp.map((digit, i) => (
                  <input
                    key={i}
                    inputMode="numeric"
                    maxLength={1}
                    aria-label={`Code digit ${i + 1}`}
                    value={digit}
                    onChange={(e) => {
                      const next = [...otp];
                      next[i] = e.target.value.slice(-1);
                      setOtp(next);
                    }}
                    className="size-[60px] rounded-xl border-2 border-input bg-card text-center text-2xl font-bold"
                  />
                ))}
              </div>
              <div className="mt-8">
                <Button onClick={() => navigate({ to: "/home" })}>Verify</Button>
              </div>
            </div>
          )}

          <div className="mt-8">
            <button
              type="button"
              onClick={() => setExplain((v) => !v)}
              aria-expanded={explain}
              className="inline-flex items-center gap-2 text-base font-semibold text-primary underline-offset-4 hover:underline"
            >
              What is an OTP?
              <ChevronDown
                strokeWidth={2}
                className={`size-5 transition-transform duration-200 ${explain ? "rotate-180" : ""}`}
                aria-hidden
              />
            </button>
            {explain ? (
              <p className="mt-4 rounded-xl bg-muted p-5 text-base leading-relaxed">
                An OTP is a short code sent to your phone that works only once, and only
                for a few minutes. It proves the phone is yours. Nobody — not your bank,
                not the police, not us on a call — should ever ask you to share it.
              </p>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  );
}
