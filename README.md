1. Scope: Full detailed plan with all datasets and models
2. Capital: Bank loan + own capital (50-70% borrowed)
3. Risk appetite: Balanced
4. Priority: Integrated value chain (Phương án 1)
5. Focus: Export market analysis
6. Output: Timeline + Gantt chart + Financial model
7. Budget: >500 billion VND
8. Horizon: 5-10 years

Production Data:
- 2024/25 season: 189,360 ha, 12.43M tons cane, 1.266M tons sugar
- 2025/26 forecast: 13.34M tons cane, 1.37M tons sugar
- Productivity: 6.69 tons sugar/ha (highest in ASEAN)
- 25 operational mills, capacity 124,000 tons cane/day
- Average CCS: 10.19%
- Farm gate price: VND 1.2-1.3M/ton (~$48-52/ton)

Export volume stands at roughly 190,000 tons annually with significant destinations being Laos, Thailand, and Italy, though domestic consumption far exceeds production at over 2 million tons per year against a supply of only 1.2 million tons, necessitating roughly 800,000 to 1 million tons in imports to meet demand.
Looking at pricing dynamics, raw sugar from Brazil is trading around $360-460 per ton FOB while Vietnam's exports command $747 per ton, though the domestic market shows considerable pressure with prices ranging from VND 16,200-17,500 per kilogram, which translates to roughly $650-700 per ton and remains the lowest in the region. The industry's cost structure is a critical constraint, with production costs at $50 per ton compared favorably to Australia at $30, Thailand at $30, and Brazil at $16-18, while sugar production generates approximately 696,000 tons of CO2 emissions annually with a conversion rate of 0.55 kg CO2 per kilogram of sugar, and bagasse byproduct utilization reaches 27-30% with molasses at 4-5%.
On the policy side, ASEAN's sugar imports face a 5% tariff under ATIGA with additional anti-dumping measures ranging from 25.73-47.64% on Thai sugar, though smuggled sugar remains a significant problem at an estimated 800,000 tons annually. Key market considerations include potential organic sugar premiums of $100-200 per ton in European and North American markets, ongoing carbon credit mechanisms from bagasse utilization, and growing HFCS competition. Looking at growth trajectories, the sector shows an 8.24% year-over-year increase in the 2025/26 forecast, with CAGR projections of 6.91-8.04% through 2030.

Dataset B — Xuất nhập khẩu đường:
- Volume xuất khẩu theo quốc gia (Lào, Thái Lan, Indonesia, Philippines, Hàn Quốc, Nhật, EU)
- Giá xuất khẩu trung bình theo thị trường ($/ton)
- Lượng nhập khẩu đường (chính ngạch + không chính ngạch) — ước tính ~1 triệu tấn/năm
- Thuế ATIGA 5%, biện pháp phòng vệ thương mại Thái Lan
- Dự báo cung-cầu toàn cầu 2025-2035
Dataset C — Sản xuất trong nước:
- Sản lượng mía (triệu tấn) và diện tích thu hoạch (ha) theo niên vụ
- Sản lượng đường (tấn) theo niên vụ
- Năng suất đường (tấn/ha) — đặc biệt vùng Tây Nguyên, phía Nam
- Giá mua mía tại ruộng (VND/tấn)
- Chi phí sản xuất đường (VND/tấn đường) tại các nhà máy
Dataset D — Tài chính doanh nghiệp đường niêm yết:
- SBT, QNS, LSS, KTS, SLS
- Doanh thu, lợi nhuận gộp, biên lãi gộp (3 năm)
- Tồn kho, công nợ, dòng tiền
- Định giá P/E, P/B, EV/EBITDA
Dataset E — Chính sách & Quy định:
- ATIGA: lịch trình giảm thuế, ngoại lệ, biện pháp phòng vệ
- Thuế chống bán phá giá Thái Lan (25.73-47.64%)
- Quy định xuất khẩu đường, giấy phép, hạn ngạch
- Tiêu chuẩn an toàn thực phẩm thị trường mục tiêu (EU, Hàn Quốc, Nhật Bản)
- Quy định carbon/CBAM

Bước 2: Nguồn dữ liệu
| Nguồn | Loại | URL/Tài liệu |
|---|---|---|
| Tổng cục Thống kê Việt Nam (GSO) | Số liệu vĩ mô, sản xuất nông nghiệp | gso.gov.vn |
| Bộ Công Thương — Vụ Thị trường trong nước | Sản lượng đường, giá cả | moc.gov.vn |
| Hiệp hội Mía đường Việt Nam (VSSA) | Báo cáo ngành, số liệu sản xuất | vienmiaduong.vn |
| Tổng cục Hải quan | Dữ liệu xuất nhập khẩu | hanoicustoms.gov.vn |
| UN Comtrade | Dữ liệu xuất khẩu đường theo quốc gia | comtrade.un.org |
| ITC Trade Map | Thị trường xuất khẩu, giá, đối thủ | trademap.org |
| FAO — Food Outlook | Cung-cầu đường toàn cầu | fao.org/faostat |
| USDA — Sugar: World Markets and Trade | Dự báo sản xuất, tiêu thụ toàn cầu | fas.usda.gov |
| World Bank / IMF | GDP, CPI, tỷ giá dự báo | worldbank.org |
| Báo cáo niên yết doanh nghiệp (SBT, QNS...) | Báo cáo tài chính chi tiết | cafef.vn, vietstock.vn |
| IndexBox / Ken Research / 6Wresearch | Báo cáo ngành đường Việt Nam | indexbox.io, kenresearch.com |
| VCCI, VnEconomy | Tin tức ngành, phân tích chính sách | vcci.com.vn |
Bước 3: Quy trình thu thập
Giai đoạn 1 (Tháng 1-2):
- Tải toàn bộ dữ liệu sản xuất từ GSO và VSSA (2015-2025)
- Truy xuất dữ liệu xuất nhập khẩu từ UN Comtrade và ITC (2015-2025)
- Thu thập báo cáo tài chính 5 doanh nghiệp đường niêm yết (3 năm)
- Thu thập báo cáo ngành từ IndexBox, Ken Research, USDA
Giai đoạn 2 (Tháng 3):
- Tổng hợp dữ liệu vào file Excel/CSV tập trung
- Phân loại theo Dataset A→E
- Kiểm tra missing data, outliers
---
PHẦN II: PHÂN TÍCH THỊ TRƯỜNG XUẤT KHẨU
2.1. Tổng quan thị trường đường thế giới
Sản lượng toàn cầu 2024:
- Brazil: 44.7MMT (lớn nhất, chiếm ~20% sản lượng)
- Ấn Độ: ~32MMT
- Trung Quốc: ~11MMT
- Thái Lan: ~10.3MMT
- Việt Nam: ~1.26MMT
Xuất khẩu toàn cầu 2024:
- Brazil: ~28MMT ($18.6B, giá $486/ton)
- Thái Lan: ~8MMT ($2.36B, giá $580/ton)
- Ấn Độ: ~1.5MMT ($379M, giá $619/ton)
- Việt Nam: ~190.000 tấn ($67M)
Giá thế giới (2024-2025):
- Giá thô NY#11 (2024): trung bình 22.05 ¢/lb → ~$486/ton
- Giá thô NY#11 (2025 dự báo): 14.97 ¢/lb → ~$330/ton (giảm 32%)
- Dự báo 2025-2026: $440-460/ton (14.2-14.9 ¢/lb)
- Đường tinh luyện ICUMSA 45 FOB Santos: $420-460/ton
- Giá xuất khẩu đường Việt Nam trung bình 2024: $747/ton
Dự báo cung-cầu toàn cầu (USDA, Krungsri):
- Tăng trưởng sản xuất 2025-2026: +0.5-1.5% CAGR
- Tăng trưởng tiêu thụ: +0.5-1.5% CAGR
- Nguồn cung có xu hướng vượt cầu → áp lực giảm giá trung hạn
2.2. Thị trường xuất khẩu mục tiêu — Phân tích chi tiết từng thị trường
---
THỊ TRƯỜNG 1: HÀN QUỐC — ƯU TIÊN CAO NHẤT ★★★★★
Tổng quan:
- Dân số: 51.7M, thu nhập cao, ngành F&B phát triển mạnh
- Nhập khẩu đường: ~300.000-350.000 tấn/năm
- Đối tác cung cấp chính: Thái Lan, Australia, Brazil
Lợi thế cho Việt Nam:
- Hiệp định EVFTA: thuế suất ưu đãi, giảm dần về 0% theo lộ trình
- Khoảng cách địa lý gần, chi phí vận chuyển thấp hơn Brazil
- Hàn Quốc nhập khẩu từ Thái Lan giá $600-650/ton — Việt Nam có thể cạnh tranh
Hạn chế:
- Cạnh tranh gay gắt với Thái Lan ( FTA ASEAN-Hàn Quốc, thuế 0%)
- Yêu cầu chất lượng cao: ICUMSA < 45, tiêu chuẩn an toàn thực phẩm nghiêm ngặt
- Nhà nhập khẩu Hàn Quốc ưa chuộng nguồn cung ổn định dài hạn
Giá tham chiếu:
- Giá nhập khẩu Hàn Quốc từ Thái Lan: ~$580-620/ton CIF
- Premium cho đường chất lượng cao (organic, fair trade): +$50-150/ton
- Mục tiêu giá xuất khẩu từ Việt Nam: $550-650/ton FOB
Chiến lược thâm nhập:
1. Đăng ký chứng nhận KFDA (Korea Food and Drug Administration)
2. Tham gia hội chợ thực phẩm Seoul Food Expo hàng năm
3. Xây dựng kênh phân phối qua các nhà nhập khẩu lớn (Lotte, CJ, Nongsim)
4. Ưu tiên sản phẩm: đường tinh luyện ICUMSA 45, đường hữu cơ
---
THỊ TRƯỜNG 2: NHẬT BẢN — ƯU TIÊN CAO ★★★★★
Tổng quan:
- Dân số: 125M, thu nhập rất cao
- Nhập khẩu đường: ~600.000 tấn/năm
- Đối tác cung cấp chính: Brazil, Thái Lan, Australia
Lợi thế cho Việt Nam:
- CPTPP: thuế suất giảm dần, cơ hội cạnh tranh với Brazil
- Người tiêu dùng sẵn sàng trả giá cao cho sản phẩm chất lượng, hữu cơ
- Tiềm năng premium cao: đường organic/tự nhiên Việt Nam
Hạn chế:
- Tiêu chuẩn an toàn thực phẩm (JAS) rất nghiêm ngặt
- Chu kỳ phê duyệt nhập khẩu dài, quy định phức tạp
- Cạnh tranh gay gắt với Australia (quốc gia CPTPP, chất lượng cao)
Giá tham chiếu:
- Giá nhập khẩu Nhật Bản từ Brazil: ~$550-650/ton CIF
- Premium cho đường organic/tự nhiên: +$100-250/ton
- Mục tiêu giá xuất khẩu từ Việt Nam: $600-750/ton FOB
Chiến lược thâm nhập:
1. Đăng ký chứng nhận JAS (Japanese Agricultural Standards) cho đường hữu cơ
2. Tham gia Foodex Japan — hội chợ thực phẩm lớn nhất Nhật Bản
3. Hợp tác với các tập đoàn thực phẩm lớn (Ajinomoto, Kirin, Suntory)
4. Sản phẩm: đường organic, đường tinh luyện đặc biệt
---
THỊ TRƯỜNG 3: PHILIPPINES — ƯU TIÊN CAO ★★★★☆
Tổng quan:
- Dân số: 115M, thu nhập trung bình thấp
- Nhập khẩu đường: ~500.000-600.000 tấn/năm
- Đối tác cung cấp chính: Thailand, Thái Lan, Việt Nam
Lợi thế cho Việt Nam:
- Việt Nam đã là nhà cung cấp lớn thứ 3 cho Philippines (sau Thái Lan và Indonesia)
- Lợi thế địa lý, chi phí vận chuyển thấp
- ASEAN: thuế ATIGA 0-5%, không có rào cản lớn
Hạn chế:
- Philippines có ngành đường nội địa bảo hộ (quota nội địa cao)
- Cạnh tranh giá mạnh từ Thái Lan
- Biến động chính sách nội địa ảnh hưởng đến nhập khẩu
Giá tham chiếu:
- Giá nhập khẩu Philippines: ~$500-600/ton CIF
- Mục tiêu giá xuất khẩu từ Việt Nam: $480-550/ton FOB
Chiến lược thâm nhập:
1. Đa dạng hóa sản phẩm (đường thô cho công nghiệp, đường tinh luyện cho tiêu dùng)
2. Xây dựng quan hệ với các nhà máy thực phẩm lớn (San Miguel, Universal Robina)
3. Tham gia hội chợ thực phẩm Philippines
---
THỊ TRƯỜNG 4: INDONESIA — ƯU TIÊN TRUNG BÌNH ★★★★☆
Tổng quan:
- Dân số: 275M, thu nhập trung bình
- Nhập khẩu đường: ~3-4 triệu tấn/năm (rất lớn)
- Đối tác cung cấp chính: Brazil, Thái Lan, Australia
Lợi thế cho Việt Nam:
- Việt Nam đã bắt đầu xuất khẩu đường sang Indonesia gần đây
- Tăng trưởng nhanh (CAGR 2825% theo dữ liệu 2020-2023)
- ASEAN: thuế ATIGA, lợi thế địa lý
Hạn chế:
- Yêu cầu chất lượng khá cao
- Cạnh tranh gay gắt với Brazil và Thái Lan
- Quy định nhập khẩu phức tạp
Giá tham chiếu:
- Giá nhập khẩu từ Brazil: ~$480-550/ton CIF
- Mục tiêu giá xuất khẩu từ Việt Nam: $460-520/ton FOB
---
THỊ TRƯỜNG 5: CHÂU ÂU (EU) — ƯU TIÊN TRUNG BÌNH ★★★★☆
Tổng quan:
- Nhập khẩu đường EU: ~2-3 triệu tấn/năm (chủ yếu đường thô cho ethanol và đường tinh luyện)
- Yêu cầu khắt khe về sustainability (EUDR, CBAM)
Lợi thế cho Việt Nam:
- EVFTA: thuế suất giảm dần, cơ hội tăng trưởng
- Premium cao cho đường organic, fair trade, sustainable
- Thị trường tiềm năng 450 triệu dân
Hạn chế:
- CBAM sắp áp dụng cho carbon-intensive products
- Quy định EUDR về traceability (không mua từ đất có deforestation)
- Tiêu chuẩn bãi bỏ fructose syrup cao
- Cạnh tranh từ Brazil, Thái Lan, Australia (các nước có FTA với EU)
Giá tham chiếu:
- Đường thô FOB: $450-520/ton
- Đường organic premium: $800-1.200/ton
- Mục tiêu giá xuất khẩu từ Việt Nam: $500-900/ton FOB (tùy phân khúc)
Chiến lược thâm nhập:
1. Đăng ký chứng nhận EU Organic, Fair Trade, Rainforest Alliance
2. Đáp ứng EUDR: truy xuất nguồn gốc đến từng hecta
3. Tập trung vào phân khúc organic sugar và fair trade sugar
4. Tham gia BioFach (hội chợ organic lớn nhất thế giới) — Nuremberg
---
THỊ TRƯỜNG 6: TRUNG QUỐC — ƯU TIÊN THẤP ★★★☆☆
Tổng quan:
- Nhập khẩu đường: ~4-5 triệu tấn/năm
- Đối tác chính: Brazil (~70%), Úc, Myanmar
Lợi thế cho Việt Nam:
- Vùng nguyên liệu Tây Nguyên/Bắc Việt gần biên giới phía Bắc
- RCEP: thuế ưu đãi, cơ hội tiếp cận thị trường lớn
- Biên giới đường bộ thuận lợi cho xuất khẩu biên giới
Hạn chế:
- Cạnh tranh cực kỳ gay gắt từ Brazil (chi phí thấp hơn rất nhiều)
- Tiêu chuẩn chất lượng cao, quy định nhập khẩu phức tạp
- Giá xuất khẩu sang Trung Quốc thường thấp nhất
- Gần biên giới → dễ có đường nhập lậu ngược lại
Giá tham chiếu:
- Giá nhập khẩu từ Brazil: ~$450-500/ton CIF
- Mục tiêu giá xuất khẩu từ Việt Nam: $420-480/ton FOB
---
THỊ TRƯỜNG 7: MỸ — ƯU TIÊN THẤP ★★★☆☆
Tổng quan:
- Nhập khẩu đường: ~3-4 triệu tấn/năm
- Đối tác chính: Brazil, Mexico, Guatemala
Lợi thế cho Việt Nam:
- CPTPP: cơ hội tiếp cận thị trường lớn
- Premium rất cao cho sản phẩm organic, fair trade
- Ai đã có: quota nhập khẩu, phân bổ quota cho Việt Nam
Hạn chế:
- Mỹ áp dụng quota nhập khẩu — Việt Nam khó đạt quota lớn
- Cạnh tranh gay gắt từ Mexico, Brazil, Guatemala
- Tiêu chuẩn FDA rất nghiêm ngặt
- Rủi ro địa chính trị
Giá tham chiếu:
- Giá nhập khẩu Mỹ từ Mexico: ~$600-700/ton CIF (quota)
- Premium organic: +$200-400/ton
- Mục tiêu giá xuất khẩu từ Việt Nam: $600-850/ton FOB
---
2.3. Ma trận ưu tiên thị trường
| Thị trường | Ưu tiên | FTA | Thuế ưu đãi | Premium tiềm năng | Rủi ro chính | Mục giá FOB mục tiêu |
|---|---|---|---|---|---|---|
| Hàn Quốc | ★★★★★ | EVFTA | Giảm dần | +$50-150/ton | Cạnh tranh Thái Lan | $550-650/ton |
| Nhật Bản | ★★★★★ | CPTPP | Giảm dần | +$100-250/ton | Tiêu chuẩn JAS cao | $600-750/ton |
| Philippines | ★★★★☆ | ATIGA | 0-5% | Trung bình | Bảo hộ nội địa | $480-550/ton |
| Indonesia | ★★★★☆ | ATIGA | 0-5% | Trung bình | Cạnh tranh Brazil | $460-520/ton |
| EU | ★★★★☆ | EVFTA | Giảm dần | +$150-450/ton | CBAM, EUDR | $500-900/ton |
| Trung Quốc | ★★★☆☆ | RCEP | Ưu đãi | Thấp | Cạnh tranh Brazil | $420-480/ton |
| Mỹ | ★★★☆☆ | CPTPP | Quota | +$200-400/ton | Quota hạn chế | $600-850/ton |
---
2.4. Kênh phân phối và logistics xuất khẩu
Cảng xuất khẩu chính của Việt Nam:
- Cảng Hải Phòng (miền Bắc): phục vụ Hàn Quốc, Nhật Bản, Trung Quốc
- Cảng Cái Lân (Quảng Ninh): xuất khẩu Bắc Âu, Hàn Quốc
- Cảng Đà Nẵng: phục vụ Nhật Bản, Hàn Quốc, Đài Loan
- Cảng Sài Gòn (TP.HCM): phục vụ ASEAN, Trung Đông, châu Phi
Chi phí logistics ước tính (FOB vs CIF):
- Vận chuyển nội địa (nhà máy → cảng): $15-25/ton
- Container 20ft (18-22 tấn đường): phí cảng $100-200/container
- Freight đường biển Hải Phòng → Busan (Hàn Quốc): $30-50/ton
- Freight Hải Phòng → Yokohama (Nhật): $50-80/ton
- Freight Sài Gòn → Jakarta (Indonesia): $40-60/ton
---
PHẦN III: MÔ HÌNH TÀI CHÍNH (DCF)
3.1. Giả định cơ bản
Cơ cấu vốn:
- Tổng vốn đầu tư: 600 tỷ VND (~$24M)
- Vốn tự có: 180 tỷ VND (30%)
- Vay ngân hàng: 420 tỷ VND (70%)
- Lãi suất vay: 8.5%/năm (trung bình)
- WACC: ước tính ~9.5-10.5%/năm
Hoạt động sản xuất:
- Công suất nhà máy: 3.000 tấn mía/ngày × 120 ngày vụ = 360.000 tấn mía/năm
- Tỷ lệ chuyển đổi: 8 tấn mía → 1 tấn đường (hiệu suất ~12.5% với CCS 10.19%)
- Sản lượng đường: ~45.000 tấn đường/năm (vùng nguyên liệu 5.000 ha × 70 tấn/ha = 350.000 tấn mía)
- Tỷ lệ liên kết nông dân: 80% (4.000 ha liên kết, 1.000 ha tự trồng)
Giá bán:
- Giá bán nội địa trung bình: VND 18.500/kg = $740/ton (tỷ giá 25.000 VND/USD)
- Giá bán xuất khẩu trung bình (phối hợp nhiều thị trường): $620/ton FOB
- Premium đường hữu cơ (từ năm thứ 4): +$150-250/ton
Chi phí sản xuất:
- Chi phí mua mía: VND 1.25M/tấn = $50/ton × 8 tấn = $400/ton đường
- Chi phí chế biến (khấu hao, nhân công, năng lượng): ~$120/ton đường
- Chi phí logistics & đóng gói: $25/ton
- Chi phí quản lý & bán hàng: $35/ton
- Tổng chi phí: ~$580/ton đường
Doanh thu dự kiến:
- Nội địa (40% sản lượng): 18.000 tấn × $740/ton = $13.32M = ~333 tỷ VND
- Xuất khẩu (60% sản lượng): 27.000 tấn × $620/ton = $16.74M = ~418.5 tỷ VND
- Tổng doanh thu: ~751.5 tỷ VND/năm
Lợi nhuận gộp:
- Chi phí sản xuất đường: 45.000 tấn × $580 = $26.1M = ~652.5 tỷ VND
- Lợi nhuận gộp: 751.5 - 652.5 = ~99 tỷ VND (Biên lãi gộp ~13.2%)
3.2. Dự báo dòng tiền 10 năm (Kịch bản cơ bản)
| Năm | Doanh thu (tỷ VND) | EBITDA Margin | EBITDA | Chi phí lãi vay | Khấu hao | EBIT | Thuế (20%) | NOPAT | FCF |
|---|---|---|---|---|---|---|---|---|---|
| Năm 1 | 100 | 8% | 8.0 | 35.7 | 25 | -52.7 | 0 | -52.7 | -77.7 |
| Năm 2 | 300 | 10% | 30.0 | 35.7 | 25 | -30.7 | 0 | -30.7 | -55.7 |
| Năm 3 | 500 | 12% | 60.0 | 35.7 | 25 | -0.7 | 0 | -0.7 | -25.7 |
| Năm 4 | 650 | 13% | 84.5 | 30.0 | 25 | 29.5 | 5.9 | 23.6 | -1.4 |
| Năm 5 | 752 | 14% | 105.3 | 25.0 | 25 | 55.3 | 11.1 | 44.2 | 19.2 |
| Năm 6 | 800 | 14% | 112.0 | 20.0 | 25 | 67.0 | 13.4 | 53.6 | 28.6 |
| Năm 7 | 850 | 14.5% | 123.3 | 15.0 | 25 | 83.3 | 16.7 | 66.6 | 41.6 |
| Năm 8 | 900 | 15% | 135.0 | 10.0 | 25 | 100.0 | 20.0 | 80.0 | 55.0 |
| Năm 9 | 950 | 15% | 142.5 | 5.0 | 25 | 112.5 | 22.5 | 90.0 | 65.0 |
| Năm 10 | 1.000 | 15% | 150.0 | 0 | 25 | 125.0 | 25.0 | 100.0 | 75.0 |
Giả định:
- Năm 1-3: Xây dựng nhà máy, vùng nguyên liệu, sản lượng thấp dần
- Năm 4+: Vận hành ổn định, tăng trưởng doanh thu 5%/năm
- Lãi suất vay giảm dần theo trả nợ gốc
- Thuế thu nhập doanh nghiệp: 20%
- Khấu hao tài sản cố định: 25 tỷ VND/năm (vòng đời 20 năm)
3.3. Phân tích NPV và IRR
Các giả định quan trọng:
- WACC: 10%
- Tốc độ tăng trưởng dài hạn (Terminal): 3%
- Thời gian dự án: 10 năm
- Giá trị còn lại (Terminal Value) = FCF cuối × (1+g) / (WACC - g)
Kịch bản Cơ bản (Base Case):
- NPV (10 năm, WACC 10%): Ước tính ~50-80 tỷ VND (dương)
- IRR: Ước tính ~14-16%
- Thời gian hoàn vốn: ~7-8 năm
Kịch bản Lạc quan (Upside):
- Giá đường xuất khẩu cao hơn (+15%), sản lượng tăng 20%
- NPV: ~120-150 tỷ VND
- IRR: ~18-22%
- Thời gian hoàn vốn: ~5-6 năm
Kịch bản Bi quan (Downside):
- Giá đường nội địa tiếp tục giảm, đường nhập lậu không kiểm soát
- NPV: ~-20-30 tỷ VND (rủi ro thua lỗ)
- IRR: ~5-7%
- Thời gian hoàn vốn: >10 năm hoặc không hoàn vốn
Điểm hòa vốn (Break-even):
- Sản lượng hòa vốn: ~38.000 tấn đường/năm (84% công suất)
- Giá hòa vốn: ~$560/ton (tổng chi phí + lãi vay)
3.4. Độ nhạy (Sensitivity Analysis)
| Biến số | -20% NPV | Base | +20% NPV |
|---|---|---|---|
| Giá bán đường | -150 tỷ | +65 tỷ | +280 tỷ |
| Sản lượng mía | -100 tỷ | +65 tỷ | +230 tỷ |
| Chi phí mía | +90 tỷ | +65 tỷ | +40 tỷ |
| WACC (+/-2%) | +120 tỷ | +65 tỷ | +20 tỷ |
---
PHẦN IV: TIMELINE VÀ GANTT CHART
Giai đoạn I — Chuẩn bị & Nghiên cứu (Tháng 1-6, Năm 1)
| Tháng | Hoạt động | Ngân sách (tỷ VND) | Trách nhiệm |
|---|---|---|---|
| Tháng 1-2 | Thu thập Dataset A-E (Desk Research toàn diện) | 2 | Đội ngũ nghiên cứu |
| Tháng 2-3 | Due diligence 3-5 nhà máy đường tiềm năng | 3 | Bộ phận đầu tư |
| Tháng 3-4 | Đàm phán sơ bộ với nhà máy/đối tác | 1 | Ban lãnh đạo |
| Tháng 4-5 | Phân tích pháp lý, thuế, quy định xuất khẩu | 2 | Tư vấn pháp lý |
| Tháng 5-6 | Hoàn thiện Deal structure, ký MOU | 2 | Ban lãnh đạo |
Tổng ngân sách Giai đoạn I: ~10 tỷ VND
Giai đoạn II — Thiết lập vùng nguyên liệu & Nhà máy (Tháng 7-18, Năm 1-2)
| Tháng | Hoạt động | Ngân sách (tỷ VND) | Trách nhiệm |
|---|---|---|---|
| Tháng 7-9 | Ký hợp đồng liên kết vùng nguyên liệu (3.000 ha) | 5 | Bộ phận nông nghiệp |
| Tháng 8-12 | Đầu tư nâng cấp/cải tạo nhà máy đường | 150 | Bộ phận kỹ thuật |
| Tháng 10-15 | Mua/sản xuất giống mía chất lượng cao (KK3) | 15 | Bộ phận nông nghiệp |
| Tháng 12-18 | Xây dựng hệ thống logistics, kho bãi | 30 | Bộ phận logistics |
| Tháng 15-18 | Xây dựng hệ thống truy xuất nguồn gốc | 10 | Bộ phận IT/QC |
Tổng ngân sách Giai đoạn II: ~210 tỷ VND
Giai đoạn III — Vận hành thử & Chứng nhận (Tháng 19-30, Năm 2-3)
| Tháng | Hoạt động | Ngân sách (tỷ VND) | Trách nhiệm |
|---|---|---|---|
| Tháng 19-21 | Vận hành thử nhà máy (trial production) | 20 | Bộ phận sản xuất |
| Tháng 20-24 | Xin cấp phép xuất khẩu, đăng ký chứng nhận | 5 | Bộ phận pháp lý |
| Tháng 22-27 | Đăng ký HACCP, ISO 22000, Kosher, Halal | 8 | Bộ phận QC |
| Tháng 25-30 | Trial export — xuất khẩu thử sang Hàn Quốc/Nhật | 15 | Bộ phận thương mại |
Tổng ngân sách Giai đoạn III: ~48 tỷ VND
Giai đoạn IV — Mở rộng & Đa dạng hóa (Năm 3-5)
| Tháng | Hoạt động | Ngân sách (tỷ VND) | Trách nhiệm |
|---|---|---|---|
| Năm 3 | Mở rộng vùng nguyên liệu lên 5.000 ha | 80 | Bộ phận nông nghiệp |
| Năm 3-4 | Đăng ký JAS (Nhật), KFDA (Hàn Quốc), EU Organic | 20 | Bộ phận QC |
| Năm 3-4 | Mở rộng kho bãi tại cảng Hải Phòng | 40 | Bộ phận logistics |
| Năm 4 | Trial export EU — BioFach Nuremberg | 15 | Bộ phận thương mại |
| Năm 5 | Mở rộng sang thị trường Indonesia, Philippines | 30 | Bộ phận thương mại |
Tổng ngân sách Giai đoạn IV: ~185 tỷ VND
Giai đoạn V — Tăng trưởng bền vững (Năm 5-10)
| Tháng | Hoạt động | Ngân sách (tỷ VND) | Trách nhiệm |
|---|---|---|---|
| Năm 5-6 | Mở rộng nhà máy thứ 2 hoặc M&A nhà máy nhỏ | 200 | Ban lãnh đạo |
| Năm 5-7 | Phát triển dự án carbon credit từ bã mía | 30 | Bộ phận CSR/Môi trường |
| Năm 6-8 | Xây dựng thương hiệu "Vietnam Organic Sugar" | 40 | Bộ phận marketing |
| Năm 7-10 | Đầu tư dây chuyền ethanol/bio-fuel | 150 | Ban lãnh đạo |
| Năm 8-10 | Mở rộng vùng nguyên liệu nước ngoài (Lào/Campuchia) | 100 | Ban lãnh đạo |
Tổng ngân sách Giai đoạn V: ~520 tỷ VND
---
Tổng hợp ngân sách theo giai đoạn
| Giai đoạn | Thời gian | Ngân sách (tỷ VND) | % Tổng |
|---|---|---|---|
| Giai đoạn I: Chuẩn bị | Năm 1 (Tháng 1-6) | 10 | 1.5% |
| Giai đoạn II: Thiết lập | Năm 1-2 (Tháng 7-18) | 210 | 31% |
| Giai đoạn III: Vận hành thử | Năm 2-3 (Tháng 19-30) | 48 | 7% |
| Giai đoạn IV: Mở rộng | Năm 3-5 | 185 | 27% |
| Giai đoạn V: Tăng trưởng | Năm 5-10 | 520 | 33.5% |
| TỔNG | 10 năm | ~973 tỷ VND | 100% |
---
PHẦN V: ĐÁNH GIÁ RỦI RO
5.1. Ma trận rủi ro
| Rủi ro | Xác suất | Mức độ | Tác động | Biện pháp giảm thiểu |
|---|---|---|---|---|
| Đường nhập lậu không kiểm soát | Cao | Nghiêm trọng | Giá đường nội địa giảm, mất thị trường | Vận động chính sách, đa dạng hóa xuất khẩu |
| Giá đường thế giới giảm mạnh | Trung bình | Lớn | Doanh thu giảm, khó trả nợ | Hedge giá, hợp đồng dài hạn với khách hàng |
| Thời tiết bất lợi (La Niña) | Trung bình | Lớn | Mía mất mùa, công suất giảm | Bảo hiểm mùa màng, đa dạng vùng trồng |
| Rủi ro pháp lý (ATIGA, thuế) | Trung bình | Trung bình | Chi phí tăng, cạnh tranh khó hơn | Theo dõi sát chính sách, lobby ngành |
| HFCS thay thế mạnh hơn dự kiến | Trung bình | Lớn | Nhu cầu nội địa giảm | Tập trung xuất khẩu, sản phẩm cao cấp |
| Cạnh tranh từ Thái Lan/Brazil | Cao | Lớn | Khó giành thị phần xuất khẩu | Định vị phân khúc organic, sustainable |
| Rủi ro tín dụng (vay ngân hàng) | Thấp | Rất lớn | Dòng tiền bị thắt, khó trả nợ | Quản lý dòng tiền chặt chẽ, duy trì reserve |
| CBAM EU tăng chi phí tuân thủ | Trung bình | Trung bình | Chi phí logistics tăng | Đầu tư carbon credit, giảm phát thải sớm |
---
