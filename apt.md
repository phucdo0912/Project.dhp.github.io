# APT - Adaptive Pairs Trading for Vietnam Stock Market

## 1. Overview

**Chiến lược:** Pairs trading dựa trên cointegration (Engle-Granger), market-neutral, tận dụng mean reversion của spread giữa 2 cổ phiếu đồng liên kết.

**Mục tiêu:** Danh mục 3 cặp (6 cổ phiếu riêng biệt), quản lý theo tuần.

**Thị trường:** HOSE (Sở GDCK TP. Hồ Chí Minh).

---

## 2. Data Sources

### Priority order:
| # | Source | Install | How to use |
|---|---|---|---|
| 1 | `vnstock` (Unified UI) | `pip install vnstock` | `Reference().equity.list_by_exchange()` |
| 2 | `vnstock` (VCI) | `pip install vnstock` | `Quote(symbol, source='VCI')` |
| 3 | `vnstock` (KBS) | `pip install vnstock` | `Quote(symbol, source='KBS')` |
| 4 | VNDirect raw API | `pip install requests` | `https://finfo-api.vndirect.com.vn/v4/stock_prices/` |

### Đầu vào yêu cầu:

**prices.csv** (wide format):
```
DATE, TICKER1, TICKER2, TICKER3, ...
2020-01-02, 20.5, 35.2, ...
```

**constituents.csv** (metadata):
```
Country, Corporation, Ticker, Industry
Vietnam, Vinhomes, VHM, Real Estate
```

---

## 3. Stock Universe — TẤT CẢ MÃ HOSE

Không hardcode danh sách mã. Crawl **động** từ `vnstock` (Unified UI v4.0+):

```python
from vnstock import Reference

ref = Reference()

# Lấy tất cả mã HOSE
df = ref.equity.list_by_exchange()
hose = df[df["exchange"] == "HOSE"]
hose_tickers = hose["symbol"].tolist()

print(f"Total HOSE stocks: {len(hose_tickers)}")
```

> Dự phòng: nếu API vnstock không lấy được HOSE, dùng VNDirect raw API:
> `https://finfo-api.vndirect.com.vn/v4/stock_prices/?q=exchange:hose`

### Liquidity Filter

HOSE có ~685 mã nhưng nhiều mã thanh khoản rất thấp. Cần lọc:

```python
# Sau khi crawl prices xong, loại mã có volume trung bình < threshold
avg_volume = df_volume.mean()
liquid_tickers = avg_volume[avg_volume > 500_000].index.tolist()  # > 500k cp/ngày
```

**Tiêu chuẩn filter:**
- Average daily volume > 500,000 shares (6 tháng gần nhất)
- Missing data < 5%
- Loại mã có giá < 5,000 VND (penny stocks)
- Loại mã vốn hóa quá nhỏ (< 500 tỷ)

### Crawl script (dynamic, all HOSE):

```python
from vnstock import Reference, Quote
import pandas as pd
from itertools import combinations

def get_hose_tickers():
    ref = Reference()
    df = ref.equity.list_by_exchange()
    hose = df[df["exchange"] == "HOSE"]
    return hose["symbol"].tolist()

def get_hose_industries(tickers):
    ref = Reference()
    df = ref.equity.list_by_industry()
    return df[df["symbol"].isin(tickers)]

def crawl_prices(tickers, start, end, source="VCI"):
    df = pd.DataFrame()
    for t in tickers:
        try:
            quote = Quote(symbol=t, source=source)
            hist = quote.history(start=start, end=end, interval="1D")
            col = hist.set_index("time")["close"].rename(t)
            df = pd.concat([df, col], axis=1)
        except:
            try:  # fallback KBS
                quote = Quote(symbol=t, source="KBS")
                hist = quote.history(start=start, end=end, interval="1D")
                col = hist.set_index("time")["close"].rename(t)
                df = pd.concat([df, col], axis=1)
            except:
                print(f"Failed: {t}")
    df.index.name = "DATE"
    return df

# ===== Usage =====
tickers = get_hose_tickers()
print(f"HOSE tickers found: {len(tickers)}")
# prices = crawl_prices(tickers, "2020-01-01", "2025-12-31")
# prices.to_csv("data/prices.csv")

# Build constituents from Reference equity data
industries = get_hose_industries(tickers)
constituents = industries.copy()
constituents["Country"] = "Vietnam"
constituents.to_csv("data/constituents.csv", index=False)
```

---

## 4. Pipeline Workflow

### Step 1: Ticker Discovery
- Use `Reference().equity.list_by_exchange()` → filter `exchange == "HOSE"`
- Lưu danh sách ticker vào `data/hose_tickers.json` để cache

### Step 2: Crawl Data
- Crawl daily close prices via `vnstock.Quote` (VCI → KBS)
- Crawl song song (batch, delay giữa requests để tránh rate-limit)
- Pivot to wide format → save `data/prices.csv`
- Build `data/constituents.csv` từ `Reference().equity.list_by_industry()`

### Step 3: Clean & Filter
- Drop tickers missing >5% data
- Forward-fill còn lại
- Filter to common date range
- **Liquidity filter:** giữ mã có avg volume > 500,000 cp/ngày (6 tháng gần)
- **Price filter:** loại mã < 5,000 VND
- Chốt danh sách ticker cuối cùng (~200-300 mã HOSE thanh khoản)

### Step 4: Cointegration Screening (hàng tuần — Rolling window)
- Window: trailing 2 năm (≈504 trading days), **rolling mỗi tuần**
- Duyệt tất cả tổ hợp cặp từ danh sách HOSE đã lọc (`combinations`)
- Hồi quy OLS: `log(Y) = α + β·log(X) + ε` (dùng log price)
- Kiểm định ADF + Phillips-Perron trên residuals (spread)
- Lọc cặp:
  - ADF p-value < 0.05 AND PP p-value < 0.05
  - Spread std không quá lớn (tránh rủi ro gap)
  - R² ≥ 0.5

### Step 5: Select 3 Pairs
Từ danh sách cặp cointegrated, chọn 3 cặp với các ưu tiên:
1. 6 tickers riêng biệt (không trùng nhau)
2. Đa dạng ngành (tối đa hóa diversification)
3. P-value càng thấp càng tốt
4. Nếu <3 cặp hợp lệ, nới lỏng p-value lên 0.10
5. **Kiểm tra cặp cũ**: nếu cặp hiện tại còn cointegrated → giữ lại

### Step 6: Train (Rolling 2-year window)
- Window: trailing 2 năm (≈504 trading days), rolling — chạy lại sau mỗi lần screening
- Tính spread mean, spread std trên train window
- Thiết lập thresholds:
  - **Entry:** ±1.5σ
  - **Exit:** ±0.5σ
  - **Stop-loss:** ±3σ (thoát lỗ ngay lập tức)
- Cập nhật mỗi tuần (rebalance)

### Step 7: Generate Signals
```python
# Normalized spread
z = (spread - mean) / std

if not in_position:
    if z > 1.5:   # Y expensive, X cheap → SHORT spread (-1)
        signal = -1
    elif z < -1.5: # Y cheap, X expensive → LONG spread (+1)
        signal = 1
else:
    if abs(z) < 0.5:  # reverted → close
        signal = 0
    elif abs(z) > 3.0:  # stop-loss → force close
        signal = 0
```

### Step 8: News & Events Filter
Use `Reference().company()` to filter entries/exits:

```python
from vnstock import Reference

ref = Reference()

def has_blackout_event(ticker, date):
    """Check if ticker has corporate event within ±3 days"""
    try:
        events = ref.company(ticker).events()
        if events.empty:
            return False
        if "exright_date" not in events.columns:
            return False
        events["exright_date"] = pd.to_datetime(events["exright_date"], errors="coerce")
        close_dates = events[events["exright_date"].between(date - pd.Timedelta(days=3), date + pd.Timedelta(days=3))]
        return len(close_dates) > 0
    except Exception:
        return False
```

**Filter rules:**
- Không mở vị thế mới nếu ±3 ngày quanh ex-right date
- Đóng vị thế nếu có tin tức bất lợi (news sentiment negative)
- Không giao dịch vào ngày nghỉ lễ Việt Nam (dùng market-events list từ vnstock)
- Tạm dừng nếu VN-Index biến động >3% trong 1 phiên (market shock)

> **Note:** `ref.company(ticker).events()` dùng data từ VCI/KBS (Unified UI tự động chọn nguồn). Nếu lỗi, filter được skip (graceful degradation).

### Step 9: Portfolio Management
```python
class Portfolio:
    def __init__(self):
        self.pairs = []     # list of 3 active pairs
        self.capital = 1.0  # normalized
        self.weights = [1/3, 1/3, 1/3]  # equal weight
    
    def daily_pnl(self):
        # sum of all pairs' daily P&L
        pass
    
    def weekly_rebalance(self):
        # 1. Re-run cointegration screening
        # 2. Replace broken pairs
        # 3. Update train window
        # 4. Redistribute weights
        pass
```

### Step 10: Weekly Rebalance
Mỗi tuần:
1. Lấy trailing 2 năm dữ liệu → chạy cointegration screening (rolling)
2. Nếu cặp cũ còn cointegrated → giữ lại; nếu không → thay thế bằng cặp mới
3. Update spread mean/std trên window 2 năm rolling
4. Generate signals cho tuần tiếp theo
5. Equal weight lại 3 cặp

---

## 5. Thresholds Summary

| Parameter | Value | Note |
|---|---|---|
| Entry long (z-score) | < -1.5 | Spread dưới mean 1.5σ |
| Entry short (z-score) | > 1.5 | Spread trên mean 1.5σ |
| Exit | < 0.5 | Hồi về gần mean |
| Stop-loss | > 3.0 | Cắt lỗ tuyệt đối |
| Train window | 2 years rolling | ~504 trading days |
| Rebalance | Weekly | Every Monday |

## 6. Signal Reference

| Signal | Z-score | Hành động |
|---|---|---|
| LONG ▲ | z < -1.5σ | Y rẻ, X đắt → Mua Y, Bán X |
| SHORT ▼ | z > +1.5σ | Y đắt, X rẻ → Bán Y, Mua X |
| HOLD ◆ | \|z\| < 0.5 | Spread hồi về mean → Đóng vị thế |
| HOLD ◆ | \|z\| > 3.0 | Stop-loss → Cắt lỗ ngay |

**Cách vào lệnh thủ công (semi-auto):**
1. Vào dashboard, tab Overview xem signal
2. Mở sàn giao dịch, vào lệnh theo hướng dẫn
3. Vào dashboard, tab Trades, nhập lệnh đã thực hiện

---

## 7. Examples

### Khởi tạo lần đầu

```bash
# 1. Crawl dữ liệu
python crawl_daily.py

# 2. Chạy weekly pipeline
python run_apt_weekly.py

# 3. Mở dashboard
streamlit run dashboard.py
```

### Đọc output

```
Selected 3 pairs:
  VHM/NVL - beta=1.2345, ADF=0.0012, R2=0.85
  VCB/BID - beta=0.8765, ADF=0.0034, R2=0.79
  FPT/CMG - beta=0.6543, ADF=0.0089, R2=0.72

  VHM/NVL -> HOLD (z=0.32)
  VCB/BID -> SHORT (z=1.82)
  FPT/CMG -> LONG (z=-1.67)
```

→ VCB/BID đang SHORT: z > 1.5σ → Bán VCB, Mua BID.
→ FPT/CMG đang LONG: z < -1.5σ → Mua FPT, Bán CMG.

---

## 8. Code Modules Structure

```
apt/
├── apt.md                         # This file
├── database.py                    # SQLite: create, insert prices, signals, trades
├── get_hose_tickers.py            # Dynamic HOSE ticker discovery
├── crawl_daily.py                 # Daily crawl close + volume → SQLite
├── prepare_data.py                # Clean, forward-fill, liquidity filter
├── cointegration.py               # Engle-Granger (OLS + ADF + PP)
├── select_pairs.py                # Pick 3 diversified pairs
├── trading_strategy.py            # Signal generation + P&L
├── portfolio.py                   # Portfolio aggregation (equal weight)
├── news_filter.py                 # Events/news/market-holiday filter
├── run_apt_weekly.py              # Weekly pipeline (screening → train → signal)
├── dashboard.py                   # Streamlit dashboard
├── data/
│   ├── apt.db                     # SQLite database (prices, signals, trades)
│   ├── hose_tickers.json          # Cached HOSE ticker list
│   ├── prices.csv                 # Wide-format prices (backup)
│   └── constituents.csv           # Company metadata
├── output/
│   ├── apt_report.md              # Performance report
│   └── figs/                      # Charts
└── scheduler/
    ├── schedule_daily.bat         # Windows Task Scheduler: crawl_daily.py
    └── schedule_weekly.bat        # Windows Task Scheduler: run_apt_weekly.py
```

### File structure (summary)

| File | Chức năng |
|---|---|
| `database.py` | SQLite — lưu prices, signals, trades |
| `get_hose_tickers.py` | Crawl danh sách mã HOSE |
| `crawl_daily.py` | Crawl giá + volume hàng ngày |
| `prepare_data.py` | Lọc thanh khoản, giá, missing data |
| `cointegration.py` | Kiểm tra đồng liên kết (ADF + PP) |
| `select_pairs.py` | Chọn 3 cặp tối ưu |
| `trading_strategy.py` | Sinh tín hiệu (z-score + threshold) |
| `portfolio.py` | Quản lý danh mục 3 cặp |
| `news_filter.py` | Lọc sự kiện doanh nghiệp, ngày lễ |
| `run_apt_weekly.py` | Pipeline chính chạy hàng tuần |
| `dashboard.py` | Streamlit dashboard |

### Database schema (SQLite — `data/apt.db`)

```sql
-- Daily prices
CREATE TABLE prices (
    date TEXT, ticker TEXT, close REAL, volume REAL,
    PRIMARY KEY (date, ticker)
);

-- Weekly cointegration results
CREATE TABLE cointegration_results (
    week TEXT, pair_id TEXT, y TEXT, x TEXT, beta REAL,
    r2 REAL, adf_pvalue REAL, pp_pvalue REAL, status TEXT  -- active / broken
);

-- Trading signals
CREATE TABLE signals (
    date TEXT, pair_id TEXT, z_score REAL, signal INTEGER,  -- -1, 0, +1
    PRIMARY KEY (date, pair_id)
);

-- Trade log (manual entry via dashboard)
CREATE TABLE trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pair_id TEXT, direction TEXT,  -- LONG / SHORT
    entry_date TEXT, exit_date TEXT,
    entry_price REAL, exit_price REAL, shares REAL, pnl REAL
);
```

---

## 9. Output

### Performance Report (`output/apt_report.md`):

Mỗi cặp:
- Ticker Y, Ticker X, β, R², ADF p-value, PP p-value
- Total P&L, Win rate, Number of trades, Avg duration (days)
- Sharpe ratio, Max drawdown

Portfolio tổng:
- Combined equity curve
- Portfolio Sharpe, Max DD, CAGR
- Correlation giữa các cặp (kiểm soát diversification)

### Figures:
- Spread + signals plot (mỗi cặp)
- P&L cumulative plot (mỗi cặp)
- Portfolio equity curve (3 cặp combined)

---

## 10. Deployment (Live System)

### Schedule

| Task | Thời gian | Tool |
|---|---|---|
| `crawl_daily.py` | Hàng ngày, 15h30 (sau giờ đóng cửa HOSE) | Windows Task Scheduler |
| `run_apt_weekly.py` | Thứ Hai hàng tuần, 08h00 | Windows Task Scheduler |
| `dashboard.py` | On-demand (`streamlit run dashboard.py`) | Manual |

### Execution mode

- **Semi-auto**: Dashboard hiển thị tín hiệu → bạn vào lệnh tay qua sàn giao dịch
- **Trade log**: Nhập lệnh đã thực hiện vào dashboard (manual form)
- **No broker API**: không tự động đặt lệnh

### Dashboard (Streamlit)

Mở browser tại `http://localhost:8501` với 3 tab:

**Overview** — Thông tin 3 cặp đang active:
- Hedge ratio (β), R², ADF p-value, Spread σ
- Z-score hiện tại + tín hiệu (LONG ▲ / SHORT ▼ / HOLD ◆)
- Biểu đồ z-score với các threshold (entry ±1.5σ, exit ±0.5σ, SL ±3σ)

**Portfolio** — Tổng hợp danh mục:
- Biểu đồ spread của cả 3 cặp
- Các metrics chính: equity curve, Sharpe, Max DD, CAGR
- Alert: notification khi signal thay đổi

**Trades** — Nhập lệnh thủ công:
- Form nhập lệnh đã thực hiện (pair, direction, entry/exit price, shares)
- Tự động tính P&L
- Lịch sử giao dịch

## 11. Dependencies

```
vnstock>=4.0.0
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
arch>=6.0      # ADF and PP tests
scipy>=1.10    # stats for OLS
streamlit>=1.28  # Dashboard
```

Install:
```bash
pip install vnstock pandas numpy matplotlib arch scipy streamlit
```
Note:
```bash
Chiến lược được xây dựng mang tính chất tổng quát, KHÔNG PHẢI là cơ sở đầu tư, vui lòng sử dụng kết hợp với các công cụ khác để đưa ra quyết định đầu tư chính xác nhất.
```