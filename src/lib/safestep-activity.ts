import { useCallback, useEffect, useState } from "react";

/** Mock, browser-only learning activity used to personalise the Weekly Recap. */
export type ScenarioResult = "first-try" | "learned";

export type Activity = {
  scenarios: Record<string, { result: ScenarioResult; day: number }>;
  viewedTerms: string[];
  checks: number[]; // weekday index (0 = Mon) per message check
};

const KEY = "safestep.activity";
const EVENT = "safestep-activity";
const empty: Activity = { scenarios: {}, viewedTerms: [], checks: [] };

export function todayIndex() {
  return (new Date().getDay() + 6) % 7;
}

function read(): Activity {
  try {
    const raw = window.localStorage.getItem(KEY);
    if (!raw) return empty;
    return { ...empty, ...(JSON.parse(raw) as Partial<Activity>) };
  } catch {
    return empty;
  }
}

function write(next: Activity) {
  window.localStorage.setItem(KEY, JSON.stringify(next));
  window.dispatchEvent(new Event(EVENT));
}

export function recordScenario(id: string, correct: boolean) {
  const a = read();
  if (a.scenarios[id]) return; // keep the first attempt's outcome
  write({
    ...a,
    scenarios: { ...a.scenarios, [id]: { result: correct ? "first-try" : "learned", day: todayIndex() } },
  });
}

export function recordTermView(id: string) {
  const a = read();
  write({ ...a, viewedTerms: [id, ...a.viewedTerms.filter((t) => t !== id)] });
}

export function recordCheck() {
  const a = read();
  write({ ...a, checks: [...a.checks, todayIndex()] });
}

export function useActivity() {
  const [activity, setActivity] = useState<Activity>(empty);
  const refresh = useCallback(() => setActivity(read()), []);
  useEffect(() => {
    refresh();
    window.addEventListener(EVENT, refresh);
    return () => window.removeEventListener(EVENT, refresh);
  }, [refresh]);
  return activity;
}
