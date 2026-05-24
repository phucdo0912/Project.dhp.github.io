import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "apt.db"


def get_conn():
    return sqlite3.connect(str(DB_PATH))


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS prices (
            date TEXT, ticker TEXT, close REAL, volume REAL,
            PRIMARY KEY (date, ticker)
        );
        CREATE TABLE IF NOT EXISTS cointegration_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            week TEXT, pair_id TEXT, y TEXT, x TEXT, beta REAL,
            alpha REAL, r2 REAL, adf_pvalue REAL, pp_pvalue REAL,
            spread_mean REAL, spread_std REAL, status TEXT
        );
        CREATE TABLE IF NOT EXISTS signals (
            date TEXT, pair_id TEXT, z_score REAL, signal INTEGER,
            PRIMARY KEY (date, pair_id)
        );
        CREATE TABLE IF NOT EXISTS portfolio_state (
            week TEXT, pair_id TEXT, y TEXT, x TEXT, beta REAL,
            alpha REAL, spread_mean REAL, spread_std REAL,
            in_position INTEGER, current_signal INTEGER,
            entry_z REAL, entry_date TEXT
        );
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pair_id TEXT, direction TEXT,
            entry_date TEXT, exit_date TEXT,
            entry_price REAL, exit_price REAL,
            shares_y REAL, shares_x REAL, pnl REAL,
            note TEXT
        );
    """)
    conn.commit()
    conn.close()


def upsert_prices(df: pd.DataFrame):
    conn = get_conn()
    df_melt = df.reset_index().melt(id_vars=["DATE"], var_name="ticker", value_name="close")
    df_melt = df_melt.dropna(subset=["close"])
    df_melt["volume"] = 0.0
    df_melt["DATE"] = pd.to_datetime(df_melt["DATE"]).dt.strftime("%Y-%m-%d")
    df_melt.to_sql("prices", conn, if_exists="append", index=False, method="multi")
    conn.commit()
    conn.close()


def upsert_volume(df_vol: pd.DataFrame):
    conn = get_conn()
    df_melt = df_vol.reset_index().melt(id_vars=["DATE"], var_name="ticker", value_name="volume")
    df_melt = df_melt.dropna(subset=["volume"])
    df_melt["DATE"] = pd.to_datetime(df_melt["DATE"]).dt.strftime("%Y-%m-%d")
    existing = get_existing_volume_dates()
    df_melt = df_melt[~df_melt["DATE"].isin(existing)]
    if len(df_melt) == 0:
        conn.close()
        return
    temp = pd.read_sql("SELECT date, ticker FROM prices", conn)
    df_melt = df_melt.merge(temp, on=["date", "ticker"], how="inner")
    if len(df_melt) == 0:
        conn.close()
        return
    cur = conn.cursor()
    for _, row in df_melt.iterrows():
        cur.execute("UPDATE prices SET volume = ? WHERE date = ? AND ticker = ?",
                     (row["volume"], row["date"], row["ticker"]))
    conn.commit()
    conn.close()


def get_existing_volume_dates():
    conn = get_conn()
    df = pd.read_sql("SELECT DISTINCT date FROM prices WHERE volume > 0", conn)
    conn.close()
    return set(df["date"].tolist())


def get_prices(tickers=None, start=None, end=None) -> pd.DataFrame:
    conn = get_conn()
    query = "SELECT date, ticker, close FROM prices"
    conditions = []
    if tickers:
        placeholders = ",".join("?" for _ in tickers)
        conditions.append(f"ticker IN ({placeholders})")
    if start:
        conditions.append("date >= ?")
    if end:
        conditions.append("date <= ?")
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    params = []
    if tickers:
        params.extend(tickers)
    if start:
        params.append(start)
    if end:
        params.append(end)
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    if df.empty:
        return df
    df["date"] = pd.to_datetime(df["date"])
    pivot = df.pivot_table(index="date", columns="ticker", values="close", aggfunc="first")
    pivot.index.name = "DATE"
    pivot = pivot.sort_index()
    return pivot


def get_volumes(tickers=None, start=None, end=None) -> pd.DataFrame:
    conn = get_conn()
    query = "SELECT date, ticker, volume FROM prices WHERE volume > 0"
    conditions = []
    if tickers:
        placeholders = ",".join("?" for _ in tickers)
        conditions.append(f"ticker IN ({placeholders})")
    if start:
        conditions.append("date >= ?")
    if end:
        conditions.append("date <= ?")
    if conditions:
        query += " AND " + " AND ".join(conditions)
    params = []
    if tickers:
        params.extend(tickers)
    if start:
        params.append(start)
    if end:
        params.append(end)
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    if df.empty:
        return df
    df["date"] = pd.to_datetime(df["date"])
    pivot = df.pivot_table(index="date", columns="ticker", values="volume", aggfunc="first")
    pivot.index.name = "DATE"
    pivot = pivot.sort_index()
    return pivot


def get_all_tickers() -> list:
    conn = get_conn()
    df = pd.read_sql("SELECT DISTINCT ticker FROM prices", conn)
    conn.close()
    return df["ticker"].tolist()


def save_cointegration_results(week: str, results: list[dict]):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM cointegration_results WHERE week = ?", (week,))
    for r in results:
        cur.execute("""
            INSERT INTO cointegration_results
            (week, pair_id, y, x, beta, alpha, r2, adf_pvalue, pp_pvalue,
             spread_mean, spread_std, status)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (week, r["pair_id"], r["y"], r["x"], r.get("beta"),
              r.get("alpha"), r.get("r2"), r.get("adf_pvalue"),
              r.get("pp_pvalue"), r.get("spread_mean"), r.get("spread_std"),
              r.get("status", "active")))
    conn.commit()
    conn.close()


def save_signals(signals: list[dict]):
    conn = get_conn()
    cur = conn.cursor()
    for s in signals:
        cur.execute("""
            INSERT OR REPLACE INTO signals (date, pair_id, z_score, signal)
            VALUES (?,?,?,?)
        """, (s["date"], s["pair_id"], s["z_score"], s["signal"]))
    conn.commit()
    conn.close()


def get_latest_cointegration(week: str = None) -> pd.DataFrame:
    conn = get_conn()
    if week:
        df = pd.read_sql("SELECT * FROM cointegration_results WHERE week = ?", conn, params=(week,))
    else:
        df = pd.read_sql("""
            SELECT * FROM cointegration_results
            WHERE week = (SELECT MAX(week) FROM cointegration_results)
        """, conn)
    conn.close()
    return df


def get_active_pairs() -> list[dict]:
    conn = get_conn()
    df = pd.read_sql("""
        SELECT * FROM cointegration_results
        WHERE week = (SELECT MAX(week) FROM cointegration_results)
          AND status = 'active'
    """, conn)
    conn.close()
    return df.to_dict("records")


def get_latest_signal(pair_id: str = None) -> pd.DataFrame:
    conn = get_conn()
    query = "SELECT * FROM signals"
    params = []
    if pair_id:
        query += " WHERE pair_id = ?"
        params.append(pair_id)
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
    return df


def save_trade(trade: dict):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO trades (pair_id, direction, entry_date, exit_date,
                            entry_price, exit_price, shares_y, shares_x, pnl, note)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (trade["pair_id"], trade["direction"], trade.get("entry_date"),
          trade.get("exit_date"), trade.get("entry_price"),
          trade.get("exit_price"), trade.get("shares_y"),
          trade.get("shares_x"), trade.get("pnl"), trade.get("note")))
    conn.commit()
    conn.close()


def get_trades(pair_id: str = None) -> pd.DataFrame:
    conn = get_conn()
    query = "SELECT * FROM trades"
    params = []
    if pair_id:
        query += " WHERE pair_id = ?"
        params.append(pair_id)
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df
