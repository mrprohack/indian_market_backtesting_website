"use client";

import type { BacktestRequest, StrategyKind } from "@/lib/types";

const symbols = ["RELIANCE", "INFY", "TCS", "HDFCBANK", "SBIN"];
const strategies: Array<{ id: StrategyKind; label: string }> = [
  { id: "sma_cross", label: "SMA" },
  { id: "ema_cross", label: "EMA" },
  { id: "rsi_mean_reversion", label: "RSI" },
];

export function validateBacktestConfig(value: BacktestRequest): string | null {
  if (Number(value.initial_capital) < 1000) return "Starting capital must be at least ₹1,000.";
  if (Number(value.position_size_pct) < 1 || Number(value.position_size_pct) > 100) return "Allocation must be between 1% and 100%.";
  if (value.strategy !== "rsi_mean_reversion" && Number(value.fast_period) >= Number(value.slow_period)) return "Fast period must be below slow period.";
  return null;
}

type Props = {
  value: BacktestRequest;
  onChange: (next: BacktestRequest) => void;
  onRun: () => void;
  running: boolean;
};

export function StrategyBuilder({ value, onChange, onRun, running }: Props) {
  const error = validateBacktestConfig(value);
  const set = (key: string, next: unknown) => onChange({ ...value, [key]: next });

  return (
    <section className="builder-panel">
      <header className="panel-head">
        <div><span className="eyebrow">Configuration</span><h2>Backtest setup</h2><p>Choose an instrument, signal and portfolio size.</p></div>
        <span className={error ? "status-chip warn" : "status-chip"}>{error ? "Check inputs" : "Ready"}</span>
      </header>

      <div className="config-block">
        <div className="section-title"><span>Market</span><small>Instrument & strategy</small></div>
        <label className="field"><span>Instrument</span><select value={value.symbol} onChange={(e) => set("symbol", e.target.value)}>{symbols.map((symbol) => <option key={symbol}>{symbol}</option>)}</select></label>
        <div className="strategy-choice">{strategies.map((item) => <button key={item.id} type="button" className={value.strategy === item.id ? "selected" : ""} onClick={() => set("strategy", item.id)}><strong>{item.label}</strong><span>{item.id === "rsi_mean_reversion" ? "Mean reversion" : "Trend cross"}</span></button>)}</div>
      </div>

      <div className="config-block">
        <div className="section-title"><span>Signal</span><small>Core parameters</small></div>
        {value.strategy === "rsi_mean_reversion" ? (
          <div className="field-grid three">
            <label className="field"><span>Period</span><input type="number" min="2" value={Number(value.rsi_period)} onChange={(e) => set("rsi_period", Number(e.target.value))} /></label>
            <label className="field"><span>Oversold</span><input type="number" value={Number(value.rsi_oversold)} onChange={(e) => set("rsi_oversold", Number(e.target.value))} /></label>
            <label className="field"><span>Exit</span><input type="number" value={Number(value.rsi_exit)} onChange={(e) => set("rsi_exit", Number(e.target.value))} /></label>
          </div>
        ) : (
          <div className="field-grid two">
            <label className="field"><span>Fast period</span><input type="number" min="2" value={Number(value.fast_period)} onChange={(e) => set("fast_period", Number(e.target.value))} /></label>
            <label className="field"><span>Slow period</span><input type="number" min="3" value={Number(value.slow_period)} onChange={(e) => set("slow_period", Number(e.target.value))} /></label>
          </div>
        )}
      </div>

      <div className="config-block last">
        <div className="section-title"><span>Portfolio</span><small>Capital & allocation</small></div>
        <div className="field-grid two">
          <label className="field"><span>Starting capital</span><input type="number" min="1000" step="10000" value={Number(value.initial_capital)} onChange={(e) => set("initial_capital", Number(e.target.value))} /></label>
          <label className="field"><span>Allocation %</span><input type="number" min="1" max="100" value={Number(value.position_size_pct)} onChange={(e) => set("position_size_pct", Number(e.target.value))} /></label>
        </div>
        {error && <div className="validation-message">{error}</div>}
      </div>

      <footer className="builder-actions"><button className="run-button" type="button" onClick={onRun} disabled={running || Boolean(error)}>{running ? "Running…" : "Run backtest"}</button></footer>
    </section>
  );
}
