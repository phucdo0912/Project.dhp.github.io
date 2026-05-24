import pandas as pd
import numpy as np

from database import get_prices, get_volumes, get_all_tickers

MIN_VOLUME = 500_000
MIN_PRICE = 5000
MAX_MISSING_PCT = 5


def prepare(tickers: list = None, start: str = None, end: str = None,
            force_refresh: bool = False) -> tuple[pd.DataFrame, list]:
    prices = get_prices(tickers=tickers, start=start, end=end)
    if prices.empty:
        return prices, []
    if tickers is None:
        tickers = prices.columns.tolist()
    tickers = [t for t in tickers if t in prices.columns]
    prices = prices[tickers]
    prices = prices.ffill().bfill()
    missing_pct = prices.isnull().sum() / len(prices) * 100
    valid_tickers = missing_pct[missing_pct <= MAX_MISSING_PCT].index.tolist()
    prices = prices[valid_tickers]
    prices = prices.dropna(how="all", axis=1)
    if prices.empty:
        return prices, []
    mask = (prices.iloc[-1] >= MIN_PRICE) if len(prices) > 0 else pd.Series(True, index=prices.columns)
    valid_tickers = prices.columns[mask].tolist()
    prices = prices[valid_tickers]
    prices = prices.dropna(how="any")
    if prices.empty:
        return prices, []
    vols = get_volumes(tickers=valid_tickers, start=start, end=end)
    if not vols.empty:
        common_idx = prices.index.intersection(vols.index)
        prices = prices.loc[common_idx]
        vols = vols.loc[common_idx]
        avg_vol = vols.mean()
        liquid = avg_vol[avg_vol > MIN_VOLUME].index.tolist()
        prices = prices[[t for t in liquid if t in prices.columns]]
    final_tickers = prices.columns.tolist()
    print(f"After filtering: {len(final_tickers)} tickers, "
          f"{len(prices)} trading days")
    return prices, final_tickers
