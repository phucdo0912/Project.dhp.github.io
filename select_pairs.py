import pandas as pd


def select_pairs(candidates: pd.DataFrame, n: int = 3,
                 existing_pairs: list[dict] = None,
                 p_loosen: float = 0.10) -> list[dict]:
    if candidates.empty:
        print("No cointegrated pairs found!")
        return []
    df = candidates.copy()
    used_tickers = set()
    selected = []
    if existing_pairs:
        for ep in existing_pairs:
            y, x = ep["y"], ep["x"]
            match = df[(df["Y"] == y) & (df["X"] == x)]
            if not match.empty:
                row = match.iloc[0].to_dict()
                row["status"] = "active"
                selected.append(row)
                used_tickers.add(y)
                used_tickers.add(x)
                df = df[~((df["Y"] == y) & (df["X"] == x))]
                print(f"Kept existing pair: {y}/{x}")
    remaining = n - len(selected)
    if remaining <= 0:
        return selected[:n]
    for _, row in df.iterrows():
        if remaining <= 0:
            break
        y, x = row["Y"], row["X"]
        if y in used_tickers or x in used_tickers:
            continue
        row_dict = row.to_dict()
        row_dict["status"] = "active"
        selected.append(row_dict)
        used_tickers.add(y)
        used_tickers.add(x)
        remaining -= 1
    if len(selected) < n:
        print(f"Only found {len(selected)} pairs with p<{candidates['adf_pvalue'].min():.4f}, "
              f"loosening to p<{p_loosen}...")
        df_loose = candidates[candidates["adf_pvalue"] <= p_loosen]
        for _, row in df_loose.iterrows():
            if len(selected) >= n:
                break
            y, x = row["Y"], row["X"]
            if y in used_tickers or x in used_tickers:
                continue
            row_dict = row.to_dict()
            row_dict["status"] = "active"
            selected.append(row_dict)
            used_tickers.add(y)
            used_tickers.add(x)
    print(f"Selected {len(selected)} pairs:")
    for s in selected:
        print(f"  {s['Y']}/{s['X']} - beta={s['beta']:.4f}, "
              f"ADF={s['adf_pvalue']:.4f}, R2={s['r2']:.4f}")
    return selected
