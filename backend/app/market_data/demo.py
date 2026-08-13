from __future__ import annotations

import random
from datetime import date, timedelta

from app.backtests.models import Bar

INSTRUMENTS = [
    {"symbol": "RELIANCE", "name": "Reliance Industries", "exchange": "NSE", "type": "equity"},
    {"symbol": "INFY", "name": "Infosys", "exchange": "NSE", "type": "equity"},
    {"symbol": "TCS", "name": "Tata Consultancy Services", "exchange": "NSE", "type": "equity"},
    {"symbol": "HDFCBANK", "name": "HDFC Bank", "exchange": "NSE", "type": "equity"},
    {"symbol": "SBIN", "name": "State Bank of India", "exchange": "NSE", "type": "equity"},
]

BASE_PRICES = {"RELIANCE": 1450, "INFY": 1575, "TCS": 3350, "HDFCBANK": 1980, "SBIN": 825}


def get_demo_bars(symbol: str, count: int = 320) -> list[Bar]:
    if symbol not in BASE_PRICES:
        raise KeyError(symbol)
    rng = random.Random(f"backtest-demo:{symbol}:2026")
    day = date(2025, 4, 1)
    price = float(BASE_PRICES[symbol])
    bars: list[Bar] = []
    while len(bars) < count:
        if day.weekday() < 5:
            drift = 0.00035 + 0.0018 * __import__("math").sin(len(bars) / 18)
            shock = rng.gauss(0, 0.011)
            open_price = price * (1 + rng.gauss(0, 0.003))
            close = max(10.0, open_price * (1 + drift + shock))
            high = max(open_price, close) * (1 + rng.uniform(0.001, 0.012))
            low = min(open_price, close) * (1 - rng.uniform(0.001, 0.012))
            bars.append(
                Bar(
                    timestamp=day,
                    open=round(open_price, 2),
                    high=round(high, 2),
                    low=round(low, 2),
                    close=round(close, 2),
                    volume=rng.randint(700_000, 4_500_000),
                )
            )
            price = close
        day += timedelta(days=1)
    return bars
