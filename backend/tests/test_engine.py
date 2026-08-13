from datetime import date, timedelta

from app.backtests.engine import run_backtest
from app.backtests.models import BacktestRequest, Bar, StrategyKind


def make_bars(closes: list[float]) -> list[Bar]:
    start = date(2026, 1, 1)
    bars = []
    for index, close in enumerate(closes):
        bars.append(
            Bar(
                timestamp=start + timedelta(days=index),
                open=close,
                high=close * 1.01,
                low=close * 0.99,
                close=close,
                volume=1_000_000,
            )
        )
    return bars


def test_sma_cross_uses_next_bar_open_and_produces_trade():
    bars = make_bars([10, 10, 11, 12, 13, 12, 11, 10, 9])
    request = BacktestRequest(
        symbol="RELIANCE",
        strategy=StrategyKind.SMA_CROSS,
        fast_period=2,
        slow_period=3,
        initial_capital=100_000,
        position_size_pct=100,
        slippage_bps=0,
        stop_loss_pct=None,
        take_profit_pct=None,
    )
    result = run_backtest(request, bars)
    assert result.metrics.total_trades == 1
    trade = result.trades[0]
    assert trade.entry_date == bars[3].timestamp
    assert trade.entry_price == bars[3].open
    assert trade.exit_date == bars[7].timestamp
    assert trade.exit_price == bars[7].open
    assert result.metrics.total_costs > 0


def test_stop_loss_is_conservative_when_stop_and_target_both_touch():
    bars = make_bars([10, 10, 11, 12, 13])
    bars[3] = bars[3].model_copy(update={"high": 13.5, "low": 10.5})
    request = BacktestRequest(
        symbol="RELIANCE",
        strategy=StrategyKind.SMA_CROSS,
        fast_period=2,
        slow_period=3,
        initial_capital=100_000,
        position_size_pct=100,
        slippage_bps=0,
        stop_loss_pct=5,
        take_profit_pct=5,
    )
    result = run_backtest(request, bars)
    assert result.trades[0].exit_reason == "stop_loss"


def test_entry_costs_reduce_equity_immediately():
    bars = make_bars([10, 10, 11, 12, 13, 14])
    request = BacktestRequest(
        symbol="RELIANCE",
        strategy=StrategyKind.SMA_CROSS,
        fast_period=2,
        slow_period=3,
        initial_capital=100_000,
        position_size_pct=100,
        slippage_bps=0,
        stop_loss_pct=None,
        take_profit_pct=None,
    )
    result = run_backtest(request, bars)
    assert result.equity_curve[3].equity < request.initial_capital


def test_gap_below_stop_fills_at_gap_open():
    bars = make_bars([10, 10, 11, 12, 10])
    request = BacktestRequest(
        symbol="RELIANCE",
        strategy=StrategyKind.SMA_CROSS,
        fast_period=2,
        slow_period=3,
        initial_capital=100_000,
        position_size_pct=90,
        slippage_bps=0,
        stop_loss_pct=5,
        take_profit_pct=None,
    )
    result = run_backtest(request, bars)
    trade = result.trades[0]
    assert trade.exit_reason == "stop_loss"
    assert trade.exit_date == bars[4].timestamp
    assert trade.exit_price == bars[4].open


def test_gap_above_target_fills_at_gap_open():
    bars = make_bars([10, 10, 11, 12, 14])
    request = BacktestRequest(
        symbol="RELIANCE",
        strategy=StrategyKind.SMA_CROSS,
        fast_period=2,
        slow_period=3,
        initial_capital=100_000,
        position_size_pct=90,
        slippage_bps=0,
        stop_loss_pct=None,
        take_profit_pct=5,
    )
    result = run_backtest(request, bars)
    trade = result.trades[0]
    assert trade.exit_reason == "take_profit"
    assert trade.exit_date == bars[4].timestamp
    assert trade.exit_price == bars[4].open
