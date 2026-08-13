# BharatBacktest

A simple-to-advanced Indian-market backtesting workspace. This first working release focuses on the part that must be trustworthy before adding more features: deterministic strategy execution, India-specific costs, clear analytics, and a polished strategy builder.

## What works now

- Visual strategy configuration for SMA cross, EMA cross and RSI mean reversion.
- Deterministic seeded demo data for RELIANCE, INFY, TCS, HDFCBANK and SBIN.
- Signal-on-close / next-bar-open execution to prevent lookahead.
- Stop-loss, take-profit, position sizing and adverse slippage.
- Versioned NSE equity-delivery fee model (brokerage, STT, exchange transaction charge, SEBI charge, stamp duty, GST).
- Net profit, total return, CAGR, drawdown, Sharpe, win rate, profit factor, costs, equity curve and trade ledger.
- FastAPI OpenAPI docs at `/docs`.
- Responsive Next.js workbench, Docker Compose and CI.

> The included market data is intentionally synthetic and deterministic. It lets the product and engine run without redistributing licensed historical exchange data. Do not use demo results for investment decisions.

## Run locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest -q
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

Open `http://localhost:3000`. The API is at `http://localhost:8000` and interactive API docs are at `http://localhost:8000/docs`.

### Docker

```bash
docker compose up --build
```

## Cost model

The MVP default is tagged `zerodha_nse_equity_delivery_2026_08_13`. Rates were captured from Zerodha's published charges page on 2026-08-13: https://zerodha.com/charges/ . The rate table is code, not a timeless truth; production data should select a broker and an effective-date schedule. DP charges are not yet modeled because they require account/day/scrip-level handling rather than a simple per-fill percentage.

## Repository map

```text
frontend/                  Next.js strategy workbench
backend/app/backtests/     indicators, models and execution engine
backend/app/costs/         versioned India trading-cost model
backend/app/market_data/   deterministic provider boundary
backend/tests/             engine, costs, indicators and API tests
docs/superpowers/          product spec and implementation plan
.github/workflows/         clean CI verification
```

## Next roadmap

1. Licensed/provider-backed historical NSE cash data with corporate actions and exchange calendars.
2. Saved strategies/backtests, PostgreSQL metadata and Parquet/DuckDB market storage.
3. Futures with historical lot sizes, expiry/roll and margin assumptions.
4. Options Lab with point-in-time chains, multi-leg strategies and portfolio exits.
5. Optimization, walk-forward/out-of-sample and Monte Carlo robustness.
6. Sandboxed Python strategies and custom indicators.
7. Broker-linked paper/live execution behind a risk gateway.
