import numpy as np
import pandas as pd


ENTRY_THRESHOLD = 1.5
EXIT_THRESHOLD = 0.5
STOP_LOSS = 3.0


def compute_spread(log_prices_y: pd.Series, log_prices_x: pd.Series,
                   beta: float, alpha: float) -> pd.Series:
    return log_prices_y - alpha - beta * log_prices_x


def generate_signals(spread: pd.Series, spread_mean: float, spread_std: float,
                     in_position: bool = False, current_signal: int = 0,
                     entry_z: float = None) -> tuple[pd.DataFrame, bool, int, float]:
    z = (spread - spread_mean) / spread_std
    signals = pd.Series(0, index=spread.index)
    pos = in_position
    sig = current_signal
    entry = entry_z
    for i in range(len(z)):
        z_val = z.iloc[i]
        if not pos:
            if z_val > ENTRY_THRESHOLD:
                sig = -1
                pos = True
                entry = z_val
            elif z_val < -ENTRY_THRESHOLD:
                sig = 1
                pos = True
                entry = z_val
        else:
            if abs(z_val) < EXIT_THRESHOLD:
                sig = 0
                pos = False
                entry = None
            elif abs(z_val) > STOP_LOSS:
                sig = 0
                pos = False
                entry = None
        signals.iloc[i] = sig
    df_signals = pd.DataFrame({
        "z_score": z,
        "signal": signals,
    }, index=spread.index)
    return df_signals, pos, sig, entry


def compute_pnl(spread: pd.Series, signals: pd.Series) -> pd.Series:
    spread_returns = spread.diff().fillna(0)
    strategy_pnl = signals.shift(1).fillna(0) * spread_returns
    return strategy_pnl.cumsum()
