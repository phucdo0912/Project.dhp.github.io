# Previous Changes & Updates — apt.md

## v1.0 — 2026-05-13

### Initial Structure
- Framework: Adaptive Pairs Trading cho thị trường Việt Nam
- Data source: vnstock (VCI → KBS → raw API fallback)
- Stock universe: 14 mã HOSE hardcode (VCB, BID, VHM, FPT...)
- Threshold: Entry ±1σ, Exit ±0.5σ (tham khảo từ notebook gốc)

---

## v1.1 — Cập nhật sau test

### Thay đổi
- Stock universe: mở rộng thành **tất cả HOSE** (~685 mã), crawl động
- Threshold: đổi thành **Entry ±1.5σ**, Exit ±0.5σ, Stop-loss ±3σ
- Thêm Liquidity Filter (volume > 500k cp/ngày, giá > 5k VND)
- Chu kỳ: rebalance hàng tuần
- Thêm News/Events Filter
- Pipeline mở rộng từ 4 bước → 10 bước

### Fixes
1. **HOSE filter**: exchange column dùng StringDtype → dùng `str.contains("HOSE")`, không dùng `==` hay `isin()`
2. **Events API**: VCI Company API lỗi `KeyError: 'data'` → thêm try/except graceful degradation
3. **industry data**: `symbols_by_industries()` trả về `industry_code` + `industry_name` (Vietnamese)

### Known Limitations
- VCI `Company.events()` không hoạt động trên vnstock 3.5.0 (cần theo dõi upstream fix tại [github.com/thinh-vu/vnstock](https://github.com/thinh-vu/vnstock))
- Cointegration test mẫu VCB-BID cho p=0.083 (không cointegrated ở 5%)
- Crawl ~400 HOSE tickers tuần tự có thể bị rate-limit (cần batch + delay giữa requests)
- Chưa có transaction cost / slippage trong backtest

---

## v1.2 — Chuyển sang Unified UI (vnstock v4.0)

### Thay đổi
- API cũ `Listing()` → API mới `Reference()` (Unified UI v4.0+)
- API cũ `Company()` → API mới `Reference().company()`
- Yêu cầu `vnstock>=4.0.0`

### Chi tiết migration

| API cũ (v3.x) | API mới (v4.0) |
|---|---|
| `Listing(source="KBS").symbols_by_exchange()` | `Reference().equity.list_by_exchange()` |
| `Listing(source="KBS").all_symbols()` | `Reference().equity.list()` |
| `Listing(source="KBS").symbols_by_industries()` | `Reference().equity.list_by_industry()` |
| `Company(symbol="VCB", source="VCI")` | `Reference().company("VCB")` |

### Đã xóa
- Fallback filter 3-char ticker (không cần, `list_by_exchange()` hoạt động ổn định)
- Source parameter trong ticker discovery (Reference tự động chọn source)

### Updated files
- `apt.md`: Sections 2, 3, 4 (Steps 1, 2, 8), Section 8 (dependencies)

---

## v1.3 — Live Deployment Design (2026-05-17)

### Thay đổi
- Clarify: dùng **log price** trong OLS regression (Step 4)
- Clarify: screening chạy **rolling trên trailing 2 năm**, kiểm tra cặp cũ mỗi tuần
- Thêm **SQLite database schema** để lưu prices, signals, trades
- Module structure mới: `database.py`, `crawl_daily.py`, `dashboard.py`, `run_apt_weekly.py`, `scheduler/`
- Thêm **Section 8 — Deployment**: schedule (Windows Task Scheduler), semi-auto execution, Streamlit dashboard
- Thêm `streamlit` vào dependencies

### Updated files
- `apt.md`: Sections 4, 6, 7, 8 (deployment mới), Section 9 (dependencies cũ)
- `previous_change.md`: This entry

---

## v1.4 — Implementation Complete (2026-05-17)

### New files created

| File | Lines | Chức năng |
|---|---|---|
| `database.py` | 186 | SQLite CRUD: prices, signals, trades, cointegration results, portfolio state |
| `get_hose_tickers.py` | 82 | HOSE ticker discovery (vnstock + VNDirect fallback) + industry map |
| `crawl_daily.py` | 82 | Daily crawl close + volume, batch processing, VCI → KBS fallback |
| `prepare_data.py` | 43 | Forward-fill, liquidity filter (vol>500k), price filter (>5k VND), missing<5% |
| `cointegration.py` | 76 | Engle-Granger: OLS (log price), ADF + Phillips-Perron, R², spread stats |
| `select_pairs.py` | 59 | Greedy 3-pair selection: distinct tickers, keep existing, loosen p-value |
| `trading_strategy.py` | 39 | Signal gen: z-score, Entry ±1.5σ, Exit ±0.5σ, Stop-loss ±3σ |
| `portfolio.py` | 68 | 3-pair equal-weight portfolio, equity curve, Sharpe, Max DD, CAGR |
| `news_filter.py` | 54 | Event filter (ex-right ±3d), VN holidays, VN-Index shock >3% |
| `run_apt_weekly.py` | 90 | Weekly orchestrator: prepare → screen → select → signal → DB |
| `dashboard.py` | 162 | Streamlit dashboard: overview, portfolio, manual trade entry |
| `HUONG_DAN_SU_DUNG.md` | 140 | Usage guide (Vietnamese) |
| `scheduler/schedule_daily.bat` | 5 | Windows Task Scheduler launcher for daily crawl |
| `scheduler/schedule_weekly.bat` | 5 | Windows Task Scheduler launcher for weekly pipeline |

### Key implementation details
- **Database**: SQLite (`data/apt.db`), 5 tables (prices, cointegration_results, signals, portfolio_state, trades)
- **HOSE discovery**: vnstock `Reference().equity.list_by_exchange()` → VNDirect raw API fallback
- **Cointegration**: Giống hệt notebook gốc (OLS + ADF + PP) nhưng đóng gói thành hàm `test_pair()`
- **Pair selection**: Thuật toán greedy — ưu tiên giữ cặp cũ (nếu còn cointegrated), chọn thêm từ candidates
- **Threshold**: Entry ±1.5σ (so với notebook ±1.0σ), thêm Stop-loss ±3σ
- **Dashboard**: 3 tab — Overview (signal + z-score chart), Portfolio (spread charts), Trades (manual form)

### Known Limitations
- `news_filter.py` phụ thuộc vào `Reference().company(ticker).events()` — nếu API vnstock lỗi thì graceful degradation (skip filter)
- Dashboard dùng `st.rerun()` yêu cầu Streamlit ≥ 1.36
- Chưa có transaction cost / slippage trong tính toán P&L
- Crawl HOSE cần batch + delay để tránh rate-limit
