import numpy as np
import pandas as pd

from trading_strategy import compute_spread, generate_signals, compute_pnl

N_PAIRS = 3


class Portfolio:
    def __init__(self, capital: float = 1.0):
        self.pairs = []
        self.capital = capital
        self.weights = [1.0 / N_PAIRS] * N_PAIRS
        self.equity = [capital]
        self.dates = []

    def update_pairs(self, pairs: list[dict], prices: pd.DataFrame):
        self.pairs = pairs
        log_prices = np.log(prices.replace(0, np.nan).dropna())
        for p in self.pairs:
            y, x = p["Y"], p["X"]
            if y not in log_prices.columns or x not in log_prices.columns:
                continue
            spread = compute_spread(log_prices[y], log_prices[x],
                                    p["beta"], p["alpha"])
            p["_spread"] = spread

    def daily_update(self, date):
        daily_pnl = 0.0
        for i, p in enumerate(self.pairs):
            if "_spread" not in p or date not in p["_spread"].index:
                continue
            spread = p["_spread"][:date]
            if spread.empty:
                continue
            sig_df, in_pos, sig, entry_z = generate_signals(
                spread, p["spread_mean"], p["spread_std"],
                p.get("_in_position", False),
                p.get("_current_signal", 0),
                p.get("_entry_z"))
            p["_in_position"] = in_pos
            p["_current_signal"] = sig
            p["_entry_z"] = entry_z
            if "_pnl" not in p:
                p["_pnl"] = compute_pnl(spread, sig_df["signal"])
            w = self.weights[i] if i < len(self.weights) else 0
            if date in p["_pnl"].index:
                daily_pnl += w * p["_pnl"][date]
        self.equity.append(self.equity[-1] + daily_pnl)
        self.dates.append(date)

    def get_metrics(self):
        eq = pd.Series(self.equity, index=pd.DatetimeIndex(self.dates))
        returns = eq.pct_change().dropna()
        if len(returns) == 0:
            return {"sharpe": 0, "max_dd": 0, "cagr": 0, "total_pnl": 0}
        total_pnl = eq.iloc[-1] - 1.0
        sharpe = np.sqrt(252) * returns.mean() / returns.std() if returns.std() > 0 else 0
        max_dd = (eq / eq.expanding().max() - 1).min()
        years = max((eq.index[-1] - eq.index[0]).days / 365.25, 1 / 365.25)
        cagr = (eq.iloc[-1] / eq.iloc[0]) ** (1 / years) - 1
        return {
            "sharpe": sharpe,
            "max_dd": max_dd,
            "cagr": cagr,
            "total_pnl": total_pnl,
            "n_trades": sum(1 for p in self.pairs if p.get("_current_signal", 0) != 0),
        }

    def reset(self):
        self.pairs = []
        self.equity = [self.capital]
        self.dates = []
