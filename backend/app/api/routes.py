from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.backtests.engine import run_backtest
from app.backtests.models import BacktestRequest, BacktestResult
from app.market_data.demo import INSTRUMENTS, get_demo_bars

router = APIRouter(prefix="/api/v1")


@router.get("/instruments")
def instruments() -> list[dict[str, str]]:
    return INSTRUMENTS


@router.get("/strategies/templates")
def strategy_templates() -> list[dict[str, str]]:
    return [
        {"id": "sma_cross", "name": "SMA Trend Cross", "description": "Fast/slow moving-average trend strategy."},
        {"id": "ema_cross", "name": "EMA Momentum Cross", "description": "Faster trend response using exponential averages."},
        {"id": "rsi_mean_reversion", "name": "RSI Mean Reversion", "description": "Buy oversold conditions and exit on recovery."},
    ]


@router.post("/backtests", response_model=BacktestResult)
def create_backtest(request: BacktestRequest) -> BacktestResult:
    try:
        bars = get_demo_bars(request.symbol)
        return run_backtest(request, bars)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown demo symbol: {request.symbol}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
