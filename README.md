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
| 1 | `vnstock` (VCI) | `pip install vnstock` | `Quote(symbol, source='VCI')` |
| 2 | `vnstock` (KBS) | `pip install vnstock` | `Quote(symbol, source='KBS')` |
| 3 | VNDirect raw API | `pip install requests` | `https://finfo-api.vndirect.com.vn/v4/stock_prices/` |

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

Không hardcode danh sách mã. Crawl **động** từ `vnstock`:

```python
from vnstock import Listing

# Lấy tất cả mã HOSE
listing = Listing(source="KBS")
all_listed = listing.symbols_by_exchange()

# Lưu ý: exchange column dùng StringDtype, nên str.contains() mới work
# Không dùng == "HOSE" hoặc isin() vì dtype không tương thích
hose = all_listed[all_listed["exchange"].fillna("").str.contains("HOSE", na=False)]
hose = hose[hose["type"] == "stock"]  # type là chữ thường
hose_tickers = hose["symbol"].tolist()

print(f"Total HOSE stocks: {len(hose_tickers)}")
```

> Dự phòng: nếu API vnstock không lấy được HOSE, dùng VNDirect raw API:
> `https://finfo-api.vndirect.com.vn/v4/stock_prices/?q=exchange:hose`

### Liquidity Filter

HOSE có ~400 mã nhưng nhiều mã thanh khoản rất thấp. Cần lọc:

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
from vnstock import Quote, Listing
import pandas as pd
from itertools import combinations

def get_hose_tickers(source="KBS"):
    listing = Listing(source=source)
    try:
        df = listing.symbols_by_exchange()
        mask = df["exchange"].fillna("").str.contains("HOSE", na=False)
        mask &= df["type"] == "stock"
        return df[mask]["symbol"].tolist()
    except:
        symbols = listing.all_symbols()["symbol"].tolist()
        return [s for s in symbols if len(s) == 3 and s.isalpha()]

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

# Build constituents from listing (industry data)
# symbols_by_industries trả về: symbol, industry_code, industry_name
listing_industries = Listing(source="KBS")
industries = listing_industries.symbols_by_industries()
constituents = industries[industries["symbol"].isin(tickers)].copy()
constituents["Country"] = "Vietnam"

# Thêm công ty info từ Company.overview() nếu cần
# company = Company(symbol="VCB", source="VCI")
# ov = company.overview()  # chứa organ_name, industry, v.v.

constituents.to_csv("data/constituents.csv", index=False)
```

---

## 4. Pipeline Workflow

### Step 1: Ticker Discovery
- Use `Listing(source="KBS").symbols_by_exchange()` → filter `exchange.str.contains("HOSE")` + `type == "stock"`
- Fallback: lọc ticker 3 ký tự alphabet từ `all_symbols()`
- Lưu danh sách ticker vào `data/hose_tickers.json` để cache

### Step 2: Crawl Data
- Crawl daily close prices via `vnstock` (VCI → KBS)
- Crawl song song (batch, delay giữa requests để tránh rate-limit)
- Pivot to wide format → save `data/prices.csv`
- Build `data/constituents.csv` từ `Listing().symbols_by_industries()`

### Step 3: Clean & Filter
- Drop tickers missing >5% data
- Forward-fill còn lại
- Filter to common date range
- **Liquidity filter:** giữ mã có avg volume > 500,000 cp/ngày (6 tháng gần)
- **Price filter:** loại mã < 5,000 VND
- Chốt danh sách ticker cuối cùng (~200-300 mã HOSE thanh khoản)

### Step 4: Cointegration Screening (hàng tuần)
- Duyệt tất cả tổ hợp cặp từ danh sách HOSE đã lọc (`combinations`)
- Hồi quy OLS: `log(Y) = α + β·log(X) + ε`
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

### Step 6: Train (Rolling 2-year window)
- Window: trailing 2 năm (≈504 trading days)
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
Use `vnstock` Company data to filter entries/exits:

```python
from vnstock import Company

def has_blackout_event(ticker, date, source="VCI"):
    """Check if ticker has corporate event within ±3 days"""
    try:
        company = Company(symbol=ticker, source=source)
        events = company.events()
        if events.empty:
            return False
        if "exright_date" not in events.columns:
            return False
        events["exright_date"] = pd.to_datetime(events["exright_date"], errors="coerce")
        close_dates = events[events["exright_date"].between(date - pd.Timedelta(days=3), date + pd.Timedelta(days=3))]
        return len(close_dates) > 0
    except Exception:
        # Events API might be temporarily unavailable; skip filter
        return False
```

**Filter rules:**
- Không mở vị thế mới nếu ±3 ngày quanh ex-right date
- Đóng vị thế nếu có tin tức bất lợi (news sentiment negative)
- Không giao dịch vào ngày nghỉ lễ Việt Nam (dùng market-events list từ vnstock)
  - Tạm dừng nếu VN-Index biến động >3% trong 1 phiên (market shock)

> **Note:** VCI Company.events() API có thể không hoạt động do thay đổi từ nhà cung cấp (vnstock v3.5.0). Nếu lỗi, events filter được skip tự động (graceful degradation). Theo dõi issue trên [github.com/thinh-vu/vnstock](https://github.com/thinh-vu/vnstock) để cập nhật.

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
1. Quét lại cointegration với dữ liệu mới nhất
2. Nếu cặp cũ không còn cointegrated → thay thế bằng cặp mới
3. Update spread mean/std trên window 2 năm rolling
4. Equal weight lại 3 cặp

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

---

## 6. Code Modules Structure

```
apt/
├── apt.md                         # This skill file
├── get_hose_tickers.py            # Dynamic HOSE ticker discovery
├── crawl_vn_data.py               # Multi-source crawl + liquidity filter
├── prepare_data.py                # Pivot, clean, save CSV
├── cointegration.py               # Engle-Granger (ADF + PP)
├── select_pairs.py                # Pick 3 diversified pairs
├── trading_strategy.py            # Signal generation + P&L
├── portfolio.py                   # Portfolio aggregation (equal weight)
├── news_filter.py                 # Events/news/market-holiday filter
├── run_apt.py                     # Main pipeline (weekly cron)
├── data/
│   ├── hose_tickers.json          # Cached HOSE ticker list
│   ├── prices.csv                 # Wide-format prices
│   └── constituents.csv           # Company metadata
└── output/
    ├── apt_report.md              # Performance report
    └── figs/                      # Charts
```

---

## 7. Output

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

## 8. Dependencies

```
vnstock>=3.5.0
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
arch>=6.0      # ADF and PP tests
scipy>=1.10    # stats for OLS
```

Install:
```bash
pip install vnstock pandas numpy matplotlib arch scipy
```
