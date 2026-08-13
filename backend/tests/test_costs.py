from app.costs.india import calculate_equity_delivery_costs


def test_equity_delivery_costs_match_published_rate_formula():
    costs = calculate_equity_delivery_costs(buy_value=100_000, sell_value=110_000)
    assert costs.brokerage == 0
    assert round(costs.stt, 2) == 210.00
    assert round(costs.transaction_charges, 2) == 6.45
    assert round(costs.sebi_charges, 2) == 0.21
    assert round(costs.stamp_duty, 2) == 15.00
    assert round(costs.gst, 2) == 1.20
    assert round(costs.total, 2) == 232.86
