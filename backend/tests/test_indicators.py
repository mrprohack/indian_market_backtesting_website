from app.backtests.indicators import ema, rsi, sma


def test_sma_returns_none_until_window_is_ready():
    assert sma([1, 2, 3, 4], 3) == [None, None, 2.0, 3.0]


def test_ema_is_seeded_from_first_value():
    values = ema([10, 12, 14], 3)
    assert values[0] == 10
    assert values[1] == 11
    assert values[2] == 12.5


def test_rsi_reaches_100_for_only_gains_after_warmup():
    values = rsi([1, 2, 3, 4, 5, 6], 3)
    assert values[:3] == [None, None, None]
    assert values[3:] == [100.0, 100.0, 100.0]
