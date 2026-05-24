import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

from database import get_active_pairs, get_latest_signal, get_trades, \
    save_trade, get_prices
from trading_strategy import compute_spread, ENTRY_THRESHOLD, EXIT_THRESHOLD, STOP_LOSS
import numpy as np

st.set_page_config(page_title="APT Dashboard", layout="wide")
st.title("APT — Adaptive Pairs Trading Dashboard")
st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

tab_overview, tab_portfolio, tab_trades = st.tabs(
    ["Overview", "Portfolio", "Trades"])

active_pairs = get_active_pairs()
signals = get_latest_signal()

with tab_overview:
    st.header("Active Pairs & Signals")
    if not active_pairs:
        st.info("No active pairs. Run the weekly pipeline first.")
    else:
        cols = st.columns(len(active_pairs))
        for i, p in enumerate(active_pairs):
            with cols[i]:
                pair_signals = signals[signals["pair_id"] == p["pair_id"]] \
                    if not signals.empty else pd.DataFrame()
                last_sig = pair_signals.iloc[-1] if not pair_signals.empty else None
                z = last_sig["z_score"] if last_sig is not None else None
                sig = last_sig["signal"] if last_sig is not None else 0
                sig_label = {1: "LONG ▲", -1: "SHORT ▼", 0: "HOLD ◆"}.get(sig, "HOLD")
                sig_color = {1: "green", -1: "red", 0: "gray"}.get(sig, "gray")
                st.subheader(f"{p['y']} / {p['x']}")
                st.metric("β (Hedge Ratio)", f"{p['beta']:.4f}")
                st.metric("R²", f"{p['r2']:.4f}")
                st.metric("ADF p-value", f"{p['adf_pvalue']:.4f}")
                st.metric("Spread σ", f"{p['spread_std']:.4f}")
                if z is not None:
                    st.metric("Z-Score", f"{z:.2f}")
                st.markdown(
                    f"<h3 style='color:{sig_color};'>Signal: {sig_label}</h3>",
                    unsafe_allow_html=True)
                if pair_signals.empty:
                    continue
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=pair_signals["date"], y=pair_signals["z_score"],
                    mode="lines", name="Z-Score",
                    line=dict(color="cyan")))
                fig.add_hline(y=ENTRY_THRESHOLD, line_dash="dash",
                              line_color="red",
                              annotation_text="Entry +1.5σ")
                fig.add_hline(y=-ENTRY_THRESHOLD, line_dash="dash",
                              line_color="red",
                              annotation_text="Entry -1.5σ")
                fig.add_hline(y=EXIT_THRESHOLD, line_dash="dot",
                              line_color="green",
                              annotation_text="Exit +0.5σ")
                fig.add_hline(y=-EXIT_THRESHOLD, line_dash="dot",
                              line_color="green",
                              annotation_text="Exit -0.5σ")
                fig.add_hline(y=STOP_LOSS, line_dash="dash",
                              line_color="orange",
                              annotation_text="SL +3σ")
                fig.add_hline(y=-STOP_LOSS, line_dash="dash",
                              line_color="orange",
                              annotation_text="SL -3σ")
                fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig, use_container_width=True)

with tab_portfolio:
    st.header("Portfolio Performance")
    if not active_pairs:
        st.info("No active pairs.")
    else:
        prices = get_prices()
        if not prices.empty:
            log_prices = np.log(prices.replace(0, np.nan).dropna())
            fig = go.Figure()
            for p in active_pairs:
                y, x = p["y"], p["x"]
                if y not in log_prices.columns or x not in log_prices.columns:
                    continue
                spread = compute_spread(log_prices[y], log_prices[x],
                                        p["beta"], p["alpha"])
                fig.add_trace(go.Scatter(
                    x=spread.index, y=spread.values,
                    mode="lines", name=f"{y}/{x} spread"))
            fig.update_layout(title="Spread Series (All Pairs)",
                              height=400)
            st.plotly_chart(fig, use_container_width=True)
        metrics_cols = st.columns(4)
        with metrics_cols[0]:
            st.metric("Active Pairs", len(active_pairs))
        with metrics_cols[1]:
            st.metric("Entry Threshold", f"±{ENTRY_THRESHOLD}σ")
        with metrics_cols[2]:
            st.metric("Exit Threshold", f"±{EXIT_THRESHOLD}σ")
        with metrics_cols[3]:
            st.metric("Stop-Loss", f"±{STOP_LOSS}σ")

with tab_trades:
    st.header("Trade Log")
    trade_history = get_trades()
    if trade_history.empty:
        st.info("No trades recorded yet.")
    else:
        st.dataframe(trade_history, use_container_width=True)
    st.subheader("Record New Trade")
    with st.form("trade_form"):
        pair_options = [f"{p['y']}/{p['x']}" for p in active_pairs] \
            if active_pairs else ["No pairs"]
        col1, col2 = st.columns(2)
        with col1:
            pair_id = st.selectbox("Pair", pair_options)
            direction = st.selectbox("Direction", ["LONG", "SHORT"])
            entry_date = st.date_input("Entry Date")
            entry_price = st.number_input("Entry Price", min_value=0.0,
                                          format="%.2f")
        with col2:
            exit_date = st.date_input("Exit Date", value=None)
            exit_price = st.number_input("Exit Price (if closed)",
                                         min_value=0.0, format="%.2f")
            shares_y = st.number_input("Shares Y", min_value=0, format="%d")
            shares_x = st.number_input("Shares X", min_value=0, format="%d")
        note = st.text_input("Note")
        submitted = st.form_submit_button("Save Trade")
        if submitted:
            pnl = (exit_price - entry_price) * shares_y if exit_price > 0 else 0
            trade = {
                "pair_id": pair_id,
                "direction": direction,
                "entry_date": entry_date.isoformat(),
                "exit_date": exit_date.isoformat() if exit_date else None,
                "entry_price": entry_price,
                "exit_price": exit_price if exit_price > 0 else None,
                "shares_y": shares_y,
                "shares_x": shares_x,
                "pnl": pnl,
                "note": note,
            }
            save_trade(trade)
            st.success(f"Trade saved! P&L: {pnl:.2f}")
            st.rerun()
