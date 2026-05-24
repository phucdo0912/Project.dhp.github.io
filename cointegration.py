import numpy as np
import pandas as pd
from arch.unitroot import ADF, PhillipsPerron
from itertools import combinations


def test_pair(Y: np.ndarray, X: np.ndarray) -> dict:
    X_with_const = np.column_stack([np.ones_like(X), X])
    coeffs = np.linalg.lstsq(X_with_const, Y, rcond=None)[0]
    alpha, beta = float(coeffs[0]), float(coeffs[1])
    fitted = X_with_const @ coeffs
    resid = Y - fitted
    ss_res = float(np.dot(resid, resid))
    y_centered = Y - Y.mean()
    ss_tot = float(np.dot(y_centered, y_centered))
    r2 = np.nan if ss_tot == 0.0 else 1.0 - ss_res / ss_tot
    try:
        adf_pvalue = float(ADF(resid).pvalue)
    except Exception:
        adf_pvalue = np.nan
    try:
        pp_pvalue = float(PhillipsPerron(resid).pvalue)
    except Exception:
        pp_pvalue = np.nan
    spread_mean = float(resid.mean())
    spread_std = float(resid.std())
    return {
        "alpha": alpha, "beta": beta, "r2": r2,
        "adf_pvalue": adf_pvalue, "pp_pvalue": pp_pvalue,
        "spread_mean": spread_mean, "spread_std": spread_std,
        "resid": resid,
    }


def screen_all(prices: pd.DataFrame, tickers: list = None,
               p_threshold: float = 0.05, r2_min: float = 0.5,
               max_spread_std: float = None) -> pd.DataFrame:
    if tickers is None:
        tickers = prices.columns.tolist()
    tickers = [t for t in tickers if t in prices.columns]
    log_prices = np.log(prices[tickers].replace(0, np.nan).dropna())
    results = []
    total_pairs = len(list(combinations(tickers, 2)))
    print(f"Screening {total_pairs} pairs...")
    for idx, (Y, X) in enumerate(combinations(tickers, 2)):
        if (idx + 1) % 1000 == 0:
            print(f"  Progress: {idx + 1}/{total_pairs}")
        sY = log_prices[Y].to_numpy()
        sX = log_prices[X].to_numpy()
        result = test_pair(sY, sX)
        if np.isnan(result["adf_pvalue"]) or np.isnan(result["pp_pvalue"]):
            continue
        if result["adf_pvalue"] > p_threshold or result["pp_pvalue"] > p_threshold:
            continue
        if result["r2"] < r2_min:
            continue
        if max_spread_std and result["spread_std"] > max_spread_std:
            continue
        results.append({
            "Y": Y, "X": X,
            "alpha": result["alpha"], "beta": result["beta"],
            "r2": result["r2"],
            "adf_pvalue": result["adf_pvalue"],
            "pp_pvalue": result["pp_pvalue"],
            "spread_mean": result["spread_mean"],
            "spread_std": result["spread_std"],
            "pair_id": f"{Y}_{X}",
        })
    df = pd.DataFrame(results)
    if not df.empty:
        df = df.sort_values("adf_pvalue")
    print(f"Found {len(df)} cointegrated pairs (p<{p_threshold}, R²≥{r2_min})")
    return df
