from datetime import datetime, timedelta

import pandas as pd


VN_HOLIDAYS = [
    "2026-01-01",
    "2026-02-16", "2026-02-17", "2026-02-18", "2026-02-19", "2026-02-20",
    "2026-04-30",
    "2026-05-01",
    "2026-09-02",
]


def is_holiday(date) -> bool:
    d = pd.Timestamp(date).strftime("%Y-%m-%d")
    return d in VN_HOLIDAYS


def has_blackout_event(ticker: str, date, days_before: int = 3,
                       days_after: int = 3) -> bool:
    try:
        from vnstock import Reference
        ref = Reference()
        events = ref.company(ticker).events()
        if events.empty:
            return False
        if "exright_date" not in events.columns:
            return False
        events["exright_date"] = pd.to_datetime(events["exright_date"],
                                                 errors="coerce")
        date = pd.Timestamp(date)
        close_events = events[
            events["exright_date"].between(
                date - timedelta(days=days_before),
                date + timedelta(days=days_after)
            )
        ]
        return len(close_events) > 0
    except Exception:
        return False


def market_shock(vnindex_return: float, threshold: float = 0.03) -> bool:
    return abs(vnindex_return) > threshold


def can_trade(ticker_y: str, ticker_x: str, date,
              vnindex_return: float = None) -> tuple[bool, str]:
    if is_holiday(date):
        return False, "Market holiday"
    if vnindex_return is not None and market_shock(vnindex_return):
        return False, f"VN-Index shock ({vnindex_return:.1%})"
    if has_blackout_event(ticker_y, date):
        return False, f"{ticker_y} has ex-right event near {pd.Timestamp(date).date()}"
    if has_blackout_event(ticker_x, date):
        return False, f"{ticker_x} has ex-right event near {pd.Timestamp(date).date()}"
    return True, "OK"
