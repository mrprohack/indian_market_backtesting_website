import math

import pytest

from app.backtests.engine import run_backtest
from app.backtests.models import BacktestRequest, StrategyKind
from app.market_data.demo import INSTRUMENTS, get_demo_bars


@pytest.mark.parametrize("symbol", [item["symbol"] for item in INSTRUMENTS])
@pytest.mark.parametrize("strategy", list(StrategyKind))
def test_all_demo_symbols_and_strategies_are_deterministic_and_finite(symbol: str, strategy: StrategyKind):
    request = BacktestRequest(symbol=symbol, strategy=strategy)
    first = run_backtest(request, get_demo_bars(symbol))
    second = run_backtest(request, get_demo_bars(symbol))

    assert first == second
    assert len(first.equity_curve) == 320
    assert first.metrics.total_trades == len(first.trades)
    assert all(trade.quantity > 0 for trade in first.trades)
    assert all(trade.exit_date >= trade.entry_date for trade in first.trades)

    metrics = first.metrics
    numeric_metrics = [
        metrics.final_equity,
        metrics.net_profit,
        metrics.total_return_pct,
        metrics.cagr_pct,
        metrics.max_drawdown_pct,
        metrics.sharpe_ratio,
        metrics.win_rate_pct,
        metrics.profit_factor,
        metrics.average_trade,
        metrics.total_costs,
    ]
    assert all(math.isfinite(value) for value in numeric_metrics)
