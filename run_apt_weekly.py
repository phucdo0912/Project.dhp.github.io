import sys
from datetime import datetime, timedelta

import pandas as pd
import numpy as np

from database import init_db, get_prices, save_cointegration_results, \
    save_signals, get_active_pairs, get_latest_signal
from get_hose_tickers import get_hose_tickers
from prepare_data import prepare
from cointegration import screen_all
from select_pairs import select_pairs
from trading_strategy import compute_spread, generate_signals
from portfolio import Portfolio
import news_filter


def get_week_label(dt=None) -> str:
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-W%W")


def run():
    print("=" * 60)
    print(f"APT Weekly Pipeline — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    init_db()
    today = datetime.now()
    week = get_week_label(today)
    train_end = today.strftime("%Y-%m-%d")
    train_start = (today - timedelta(days=730)).strftime("%Y-%m-%d")

    tickers = get_hose_tickers()
    print(f"Total HOSE tickers: {len(tickers)}")

    prices, valid_tickers = prepare(tickers=tickers, start=train_start,
                                    end=train_end)
    if prices.empty:
        print("ERROR: No price data available.")
        return
    print(f"Training data: {len(prices)} days, {len(valid_tickers)} tickers")

    existing_pairs = get_active_pairs()
    candidates = screen_all(prices, tickers=valid_tickers,
                            p_threshold=0.05, r2_min=0.5)
    selected = select_pairs(candidates, n=3, existing_pairs=existing_pairs)

    if not selected:
        print("No pairs selected — skipping signal generation.")
        return

    save_cointegration_results(week, selected)

    log_prices = np.log(prices.replace(0, np.nan).dropna())
    last_date = log_prices.index[-1]
    all_signals = []

    for p in selected:
        y, x = p["Y"], p["X"]
        if y not in log_prices.columns or x not in log_prices.columns:
            print(f"  Skipping {y}/{x}: missing price data")
            continue
        spread = compute_spread(log_prices[y], log_prices[x],
                                p["beta"], p["alpha"])
        can_trade_y, reason_y = news_filter.can_trade(y, x, last_date)
        can_trade_x, reason_x = news_filter.can_trade(x, y, last_date)
        blocked = not (can_trade_y and can_trade_x)
        sig_df, _, _, _ = generate_signals(
            spread, p["spread_mean"], p["spread_std"])
        if blocked:
            sig_df["signal"] = 0
            print(f"  {y}/{x}: BLOCKED ({reason_y or reason_x})")
        for dt_idx, row in sig_df.iterrows():
            all_signals.append({
                "date": dt_idx.strftime("%Y-%m-%d"),
                "pair_id": p["pair_id"],
                "z_score": row["z_score"],
                "signal": int(row["signal"]),
            })
        last_sig = sig_df["signal"].iloc[-1]
        sig_label = {1: "LONG", -1: "SHORT", 0: "HOLD"}.get(last_sig, "HOLD")
        print(f"  {y}/{x} → {sig_label} (z={sig_df['z_score'].iloc[-1]:.2f})")

    save_signals(all_signals)
    print(f"Signals saved for {len(all_signals)} date-pair records.")
    print("Weekly pipeline complete.\n")


if __name__ == "__main__":
    run()
