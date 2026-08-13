export type StrategyKind = "sma_cross" | "ema_cross" | "rsi_mean_reversion";

export type BacktestRequest = {
  symbol: string;
  strategy: StrategyKind;
  fast_period: number;
  slow_period: number;
  rsi_period: number;
  rsi_oversold: number;
  rsi_exit: number;
  initial_capital: number;
  position_size_pct: number;
  slippage_bps: number;
  stop_loss_pct: number | null;
  take_profit_pct: number | null;
};

export type Trade = {
  entry_date: string;
  exit_date: string;
  quantity: number;
  net_pnl: number;
  exit_reason: string;
};

export type BacktestResult = {
  symbol: string;
  strategy: string;
  metrics: Record<string, number>;
  equity_curve: Array<{ date: string; equity: number }>;
  trades: Trade[];
  cost_model: string;
  data_source: string;
};
