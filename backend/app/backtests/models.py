from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class StrategyKind(str, Enum):
    SMA_CROSS = "sma_cross"
    EMA_CROSS = "ema_cross"
    RSI_MEAN_REVERSION = "rsi_mean_reversion"


class Bar(BaseModel):
    timestamp: date
    open: float
    high: float
    low: float
    close: float
    volume: int = 0


class BacktestRequest(BaseModel):
    symbol: str = "RELIANCE"
    strategy: StrategyKind = StrategyKind.SMA_CROSS
    fast_period: int = Field(default=10, ge=2, le=100)
    slow_period: int = Field(default=30, ge=3, le=250)
    rsi_period: int = Field(default=14, ge=2, le=100)
    rsi_oversold: float = Field(default=30, ge=1, le=49)
    rsi_exit: float = Field(default=55, ge=50, le=99)
    initial_capital: float = Field(default=500_000, gt=1_000)
    position_size_pct: float = Field(default=90, gt=0, le=100)
    slippage_bps: float = Field(default=2, ge=0, le=100)
    stop_loss_pct: float | None = Field(default=4, gt=0, le=50)
    take_profit_pct: float | None = Field(default=10, gt=0, le=200)

    @model_validator(mode="after")
    def validate_periods(self) -> "BacktestRequest":
        if self.strategy in {StrategyKind.SMA_CROSS, StrategyKind.EMA_CROSS} and self.fast_period >= self.slow_period:
            raise ValueError("fast_period must be smaller than slow_period")
        return self


class Trade(BaseModel):
    entry_date: date
    exit_date: date
    entry_price: float
    exit_price: float
    quantity: int
    gross_pnl: float
    costs: float
    net_pnl: float
    return_pct: float
    exit_reason: Literal["signal", "stop_loss", "take_profit", "end_of_data"]


class EquityPoint(BaseModel):
    date: date
    equity: float


class BacktestMetrics(BaseModel):
    initial_capital: float
    final_equity: float
    net_profit: float
    total_return_pct: float
    cagr_pct: float
    max_drawdown_pct: float
    sharpe_ratio: float
    win_rate_pct: float
    profit_factor: float
    total_trades: int
    average_trade: float
    total_costs: float


class BacktestResult(BaseModel):
    symbol: str
    strategy: StrategyKind
    metrics: BacktestMetrics
    equity_curve: list[EquityPoint]
    trades: list[Trade]
    cost_model: str = "zerodha_nse_equity_delivery_2026_08_13"
    data_source: str = "deterministic_demo_provider"
