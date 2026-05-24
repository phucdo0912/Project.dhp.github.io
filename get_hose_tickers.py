import json
import time
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
CACHE_FILE = DATA_DIR / "hose_tickers.json"
CONSTITUENTS_FILE = DATA_DIR / "constituents.csv"


def get_hose_tickers(use_cache=True) -> list:
    if use_cache and CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            return json.load(f)
    try:
        from vnstock import Reference
        ref = Reference()
        df = ref.equity.list_by_exchange()
        hose = df[df["exchange"].str.contains("HOSE", na=False)]
        tickers = sorted(hose["symbol"].unique().tolist())
    except Exception as e:
        print(f"vnstock Reference API failed: {e}")
        print("Trying VNDirect fallback...")
        tickers = _fallback_hose_tickers()
    if not tickers:
        print("WARNING: No HOSE tickers found!")
        return []
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(tickers, f)
    print(f"Found {len(tickers)} HOSE tickers, cached to {CACHE_FILE}")
    return tickers


def _fallback_hose_tickers():
    import requests
    url = "https://finfo-api.vndirect.com.vn/v4/stock_prices/"
    params = {"q": "exchange:hose", "size": 1}
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    total = resp.json().get("total", {}).get("value", 0)
    params["size"] = min(total, 2000)
    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    tickers = sorted(set(item["code"] for item in data if item.get("code")))
    return tickers


def get_industry_map(tickers: list = None) -> pd.DataFrame:
    try:
        from vnstock import Reference
        ref = Reference()
        df = ref.equity.list_by_industry()
        if tickers:
            df = df[df["symbol"].isin(tickers)]
        df["Country"] = "Vietnam"
        df.to_csv(CONSTITUENTS_FILE, index=False)
        return df
    except Exception as e:
        print(f"Could not fetch industry data: {e}")
        return pd.DataFrame()


def refresh_cache():
    CACHE_FILE.unlink(missing_ok=True)
    tickers = get_hose_tickers(use_cache=False)
    get_industry_map(tickers)
    return tickers


if __name__ == "__main__":
    tickers = refresh_cache()
    print(f"Total HOSE tickers: {len(tickers)}")
