import type { BacktestRequest, BacktestResult } from "./types";

export async function createBacktest(payload: BacktestRequest): Promise<BacktestResult> {
  const response = await fetch("api/v1/backtests", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Backtest failed" }));
    throw new Error(error.detail ?? "Backtest failed");
  }
  return response.json() as Promise<BacktestResult>;
}
