from __future__ import annotations

from pydantic import BaseModel


class CostBreakdown(BaseModel):
    brokerage: float
    stt: float
    transaction_charges: float
    sebi_charges: float
    stamp_duty: float
    gst: float
    total: float


NSE_TRANSACTION_RATE = 0.0000307
STT_DELIVERY_RATE = 0.001
SEBI_RATE = 10 / 10_000_000
STAMP_BUY_RATE = 0.00015
GST_RATE = 0.18


def calculate_equity_delivery_costs(buy_value: float, sell_value: float) -> CostBreakdown:
    buy_value = max(float(buy_value), 0.0)
    sell_value = max(float(sell_value), 0.0)
    turnover = buy_value + sell_value
    brokerage = 0.0
    stt = turnover * STT_DELIVERY_RATE
    transaction_charges = turnover * NSE_TRANSACTION_RATE
    sebi_charges = turnover * SEBI_RATE
    stamp_duty = buy_value * STAMP_BUY_RATE
    gst = (brokerage + transaction_charges + sebi_charges) * GST_RATE
    total = brokerage + stt + transaction_charges + sebi_charges + stamp_duty + gst
    return CostBreakdown(
        brokerage=brokerage,
        stt=stt,
        transaction_charges=transaction_charges,
        sebi_charges=sebi_charges,
        stamp_duty=stamp_duty,
        gst=gst,
        total=total,
    )
