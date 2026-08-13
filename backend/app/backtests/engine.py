from __future__ import annotations

import math
from statistics import mean, pstdev

from app.backtests.indicators import ema, rsi, sma
from app.backtests.models import BacktestMetrics, BacktestRequest, BacktestResult, Bar, EquityPoint, StrategyKind, Trade
from app.costs.india import calculate_equity_delivery_costs


def _strategy_state(request: BacktestRequest, closes: list[float]) -> list[bool]:
    if request.strategy == StrategyKind.SMA_CROSS:
        fast = sma(closes, request.fast_period)
        slow = sma(closes, request.slow_period)
        return [bool(f is not None and s is not None and f > s) for f, s in zip(fast, slow)]
    if request.strategy == StrategyKind.EMA_CROSS:
        fast = ema(closes, request.fast_period)
        slow = ema(closes, request.slow_period)
        warmup = request.slow_period - 1
        return [i >= warmup and fast[i] > slow[i] for i in range(len(closes))]

    values = rsi(closes, request.rsi_period)
    active = False
    states: list[bool] = []
    for value in values:
        if value is not None and value < request.rsi_oversold:
            active = True
        elif value is not None and value > request.rsi_exit:
            active = False
        states.append(active)
    return states


def _apply_slippage(price: float, bps: float, side: str) -> float:
    factor = bps / 10_000
    return price * (1 + factor if side == "buy" else 1 - factor)


def _max_drawdown(equity: list[float]) -> float:
    if not equity:
        return 0.0
    peak = equity[0]
    max_dd = 0.0
    for value in equity:
        peak = max(peak, value)
        if peak > 0:
            max_dd = min(max_dd, (value - peak) / peak)
    return abs(max_dd) * 100


def _sharpe(equity: list[float]) -> float:
    returns = [equity[i] / equity[i - 1] - 1 for i in range(1, len(equity)) if equity[i - 1] > 0]
    if len(returns) < 2:
        return 0.0
    sigma = pstdev(returns)
    return 0.0 if sigma == 0 else (mean(returns) / sigma) * math.sqrt(252)


def run_backtest(request: BacktestRequest, bars: list[Bar]) -> BacktestResult:
    min_bars = (request.rsi_period + 2) if request.strategy == StrategyKind.RSI_MEAN_REVERSION else (request.slow_period + 2)
    if len(bars) < min_bars:
        raise ValueError("Not enough bars for the selected strategy")

    closes = [bar.close for bar in bars]
    desired_long = _strategy_state(request, closes)
    cash = request.initial_capital
    shares = 0
    entry_price = 0.0
    entry_date = None
    entry_notional = 0.0
    entry_costs = 0.0
    pending: str | None = None
    trades: list[Trade] = []
    curve: list[EquityPoint] = []

    def close_position(i: int, raw_price: float, reason: str) -> None:
        nonlocal cash, shares, entry_price, entry_date, entry_notional, entry_costs
        exit_price = _apply_slippage(raw_price, request.slippage_bps, "sell")
        sell_value = shares * exit_price
        exit_costs = calculate_equity_delivery_costs(0.0, sell_value).total
        total_costs = entry_costs + exit_costs
        cash += sell_value - exit_costs
        gross = sell_value - entry_notional
        net = gross - total_costs
        trades.append(
            Trade(
                entry_date=entry_date,
                exit_date=bars[i].timestamp,
                entry_price=round(entry_price, 4),
                exit_price=round(exit_price, 4),
                quantity=shares,
                gross_pnl=round(gross, 2),
                costs=round(total_costs, 2),
                net_pnl=round(net, 2),
                return_pct=round((net / entry_notional) * 100, 4) if entry_notional else 0.0,
                exit_reason=reason,
            )
        )
        shares = 0
        entry_price = 0.0
        entry_date = None
        entry_notional = 0.0
        entry_costs = 0.0

    for i, bar in enumerate(bars):
        if pending == "exit" and shares > 0:
            close_position(i, bar.open, "signal")
        elif pending == "entry" and shares == 0:
            fill = _apply_slippage(bar.open, request.slippage_bps, "buy")
            budget = cash * (request.position_size_pct / 100)
            unit_entry_cost = calculate_equity_delivery_costs(fill, 0.0).total
            qty = int(budget // (fill + unit_entry_cost))
            if qty > 0:
                shares = qty
                entry_price = fill
                entry_date = bar.timestamp
                entry_notional = shares * entry_price
                entry_costs = calculate_equity_delivery_costs(entry_notional, 0.0).total
                cash -= entry_notional + entry_costs
        pending = None

        if shares > 0:
            stop_price = entry_price * (1 - request.stop_loss_pct / 100) if request.stop_loss_pct else None
            target_price = entry_price * (1 + request.take_profit_pct / 100) if request.take_profit_pct else None
            stop_hit = stop_price is not None and bar.low <= stop_price
            target_hit = target_price is not None and bar.high >= target_price

            # Gaps are known at the open and therefore take precedence over the
            # unknown intrabar high/low path. If both thresholds are touched
            # later within a bar, assume the stop happened first.
            if stop_price is not None and bar.open <= stop_price:
                close_position(i, bar.open, "stop_loss")
            elif target_price is not None and bar.open >= target_price:
                close_position(i, bar.open, "take_profit")
            elif stop_hit:
                close_position(i, stop_price, "stop_loss")
            elif target_hit:
                close_position(i, target_price, "take_profit")

        if i == len(bars) - 1 and shares > 0:
            close_position(i, bar.close, "end_of_data")

        equity = cash + (shares * bar.close if shares else 0.0)
        curve.append(EquityPoint(date=bar.timestamp, equity=round(equity, 2)))

        if i < len(bars) - 1:
            if shares == 0 and desired_long[i]:
                pending = "entry"
            elif shares > 0 and not desired_long[i]:
                pending = "exit"

    equity_values = [point.equity for point in curve]
    final_equity = equity_values[-1] if equity_values else request.initial_capital
    net_profit = final_equity - request.initial_capital
    total_return = (net_profit / request.initial_capital) * 100
    days = max((bars[-1].timestamp - bars[0].timestamp).days, 1)
    years = days / 365.25
    cagr = ((final_equity / request.initial_capital) ** (1 / years) - 1) * 100 if final_equity > 0 else -100.0
    wins = [trade.net_pnl for trade in trades if trade.net_pnl > 0]
    losses = [trade.net_pnl for trade in trades if trade.net_pnl < 0]
    profit_factor = sum(wins) / abs(sum(losses)) if losses else (999.0 if wins else 0.0)
    metrics = BacktestMetrics(
        initial_capital=round(request.initial_capital, 2),
        final_equity=round(final_equity, 2),
        net_profit=round(net_profit, 2),
        total_return_pct=round(total_return, 2),
        cagr_pct=round(cagr, 2),
        max_drawdown_pct=round(_max_drawdown(equity_values), 2),
        sharpe_ratio=round(_sharpe(equity_values), 2),
        win_rate_pct=round((len(wins) / len(trades) * 100), 2) if trades else 0.0,
        profit_factor=round(profit_factor, 2),
        total_trades=len(trades),
        average_trade=round(sum(t.net_pnl for t in trades) / len(trades), 2) if trades else 0.0,
        total_costs=round(sum(t.costs for t in trades), 2),
    )
    return BacktestResult(symbol=request.symbol, strategy=request.strategy, metrics=metrics, equity_curve=curve, trades=trades)
