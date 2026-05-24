# Hướng dẫn sử dụng APT — Adaptive Pairs Trading

## 1. Cài đặt

```bash
cd pair_trading
pip install vnstock pandas numpy matplotlib arch scipy streamlit
```

## 2. Luồng hoạt động

### Hàng ngày (sau 15h00 — giờ đóng cửa HOSE)

```bash
python crawl_daily.py
```

Crawl dữ liệu giá đóng cửa + volume từ vnstock (VCI → KBS) cho tất cả mã HOSE.
Dữ liệu được lưu vào `data/apt.db`.

> Thiết lập tự động: Windows Task Scheduler chạy `scheduler\schedule_daily.bat`.

### Hàng tuần (thứ Hai 08h00)

```bash
python run_apt_weekly.py
```

Pipeline tự động:
1. Lọc ticker (liquidity > 500k, giá > 5k VND, missing < 5%)
2. Chạy cointegration screening trên trailing 2 năm
3. Kiểm tra cặp cũ — nếu còn cointegrated thì giữ lại
4. Chọn 3 cặp mới (6 tickers riêng biệt, ưu tiên p-value thấp)
5. Tính spread mean/std, generate signals (LONG/SHORT/HOLD)
6. Kiểm tra news filter (ex-right date, holiday, VN-Index shock)
7. Lưu kết quả vào database

> Thiết lập tự động: Windows Task Scheduler chạy `scheduler\schedule_weekly.bat`.

### Dashboard (on-demand)

```bash
streamlit run dashboard.py
```

Mở browser tại `http://localhost:8501` với 3 tab:

**Overview** — Thông tin 3 cặp đang active:
- Hedge ratio (β), R², ADF p-value, Spread σ
- Z-score hiện tại + tín hiệu (LONG ▲ / SHORT ▼ / HOLD ◆)
- Biểu đồ z-score với các threshold (entry ±1.5σ, exit ±0.5σ, SL ±3σ)

**Portfolio** — Tổng hợp danh mục:
- Biểu đồ spread của cả 3 cặp
- Các metrics chính (active pairs, thresholds)

**Trades** — Nhập lệnh thủ công:
- Form nhập lệnh đã thực hiện (pair, direction, entry/exit price, shares)
- Tự động tính P&L
- Lịch sử giao dịch

## 3. Cách đọc tín hiệu

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

## 4. Ví dụ

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

## 5. Cấu trúc file

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

## 6. Thiết lập Windows Task Scheduler

### Daily crawl
1. Mở Task Scheduler → Create Basic Task
2. Name: `APT Daily Crawl`
3. Trigger: Daily, 15:30
4. Action: Start a program → Browse → chọn `scheduler\schedule_daily.bat`

### Weekly pipeline
1. Mở Task Scheduler → Create Basic Task
2. Name: `APT Weekly Pipeline`
3. Trigger: Weekly, Monday, 08:00
4. Action: Start a program → Browse → chọn `scheduler\schedule_weekly.bat`

> Log output được ghi vào `output/crawl_daily.log` và `output/apt_weekly.log`.
