import time
from datetime import datetime, timedelta

import pandas as pd

from database import init_db, upsert_prices, upsert_volume
from get_hose_tickers import get_hose_tickers

BATCH_SIZE = 50
DELAY_BETWEEN_BATCHES = 2


def crawl_daily_prices(tickers: list, start: str = None, end: str = None,
                       source: str = "VCI") -> pd.DataFrame:
    from vnstock import Quote
    if end is None:
        end = datetime.now().strftime("%Y-%m-%d")
    if start is None:
        start = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    all_close = {}
    all_volume = {}
    failed = []
    total = len(tickers)

    for i in range(0, total, BATCH_SIZE):
        batch = tickers[i:i + BATCH_SIZE]
        print(f"Crawling batch {i // BATCH_SIZE + 1}/{(total - 1) // BATCH_SIZE + 1} "
              f"({len(batch)} tickers)...")

        for t in batch:
            try:
                quote = Quote(symbol=t, source=source)
                hist = quote.history(start=start, end=end, interval="1D")
                if hist.empty:
                    continue
                if "time" not in hist.columns:
                    continue
                hist = hist.set_index("time")
                if "close" in hist.columns:
                    all_close[t] = hist["close"]
                if "volume" in hist.columns:
                    all_volume[t] = hist["volume"]
            except Exception:
                try:
                    quote = Quote(symbol=t, source="KBS")
                    hist = quote.history(start=start, end=end, interval="1D")
                    if hist.empty:
                        continue
                    if "time" not in hist.columns:
                        continue
                    hist = hist.set_index("time")
                    if "close" in hist.columns:
                        all_close[t] = hist["close"]
                    if "volume" in hist.columns:
                        all_volume[t] = hist["volume"]
                except Exception as e:
                    failed.append(t)
                    print(f"  Failed {t}: {e}")

        if i + BATCH_SIZE < total:
            time.sleep(DELAY_BETWEEN_BATCHES)

    df_close = pd.DataFrame(all_close)
    df_close.index.name = "DATE"
    df_close.index = pd.to_datetime(df_close.index)

    df_vol = pd.DataFrame(all_volume)
    df_vol.index.name = "DATE"
    df_vol.index = pd.to_datetime(df_vol.index)

    if failed:
        print(f"Failed tickers ({len(failed)}): {failed}")

    return df_close, df_vol


def run():
    print("=" * 50)
    print(f"APT Daily Crawl — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    init_db()
    tickers = get_hose_tickers()
    print(f"Tickers to crawl: {len(tickers)}")
    df_close, df_vol = crawl_daily_prices(tickers)
    if df_close.empty:
        print("No new price data fetched.")
        return
    print(f"Prices: {df_close.shape[0]} days x {df_close.shape[1]} tickers")
    upsert_prices(df_close)
    if not df_vol.empty:
        upsert_volume(df_vol)
    print("Crawl complete.")


if __name__ == "__main__":
    run()
