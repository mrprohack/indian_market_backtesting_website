from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_instruments_are_available():
    response = client.get("/api/v1/instruments")
    assert response.status_code == 200
    assert any(item["symbol"] == "RELIANCE" for item in response.json())


def test_backtest_endpoint_returns_metrics_and_equity_curve():
    response = client.post(
        "/api/v1/backtests",
        json={
            "symbol": "RELIANCE",
            "strategy": "sma_cross",
            "fast_period": 10,
            "slow_period": 30,
            "initial_capital": 500000,
            "position_size_pct": 90,
            "slippage_bps": 2,
            "stop_loss_pct": 4,
            "take_profit_pct": 10,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "RELIANCE"
    assert "net_profit" in payload["metrics"]
    assert len(payload["equity_curve"]) > 50
