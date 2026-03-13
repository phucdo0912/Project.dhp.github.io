# Phân Tích Dữ Liệu Lớn Trong Đầu Tư: Dự Báo Giá Cổ Phiếu Ngành Thép

## 📌 Tổng quan dự án
Dự án này tập trung vào việc phân tích và dự báo biến động giá cổ phiếu của ngành thép tại thị trường Việt Nam. Bằng cách ứng dụng các kỹ thuật phân tích dữ liệu lớn và học máy nâng cao, nghiên cứu cung cấp cái nhìn chuyên sâu giúp nhà đầu tư và các nhà quản lý đưa ra quyết định chính xác hơn trong bối cảnh thị trường biến động.

## 🎯 Mục tiêu và Phạm vi
- **Mục tiêu:** Ứng dụng các mô hình khoa học dữ liệu để dự báo xu hướng giá và hỗ trợ ra quyết định đầu tư.
- **Phạm vi:** Phân tích 5 mã cổ phiếu tiêu biểu ngành thép Việt Nam: **HPG, HSG, NKG, POM, và TVN**.
- **Cơ sở lý thuyết:** Dựa trên Giả thuyết Thị trường Hiệu quả (EMH) và Lý thuyết Bước đi ngẫu nhiên (Random Walk), với giả định thị trường Việt Nam đạt mức độ hiệu quả yếu.

## 📊 Nguồn dữ liệu
Nghiên cứu sử dụng bộ dữ liệu đa tầng kết hợp từ:
- **Dữ liệu tài chính doanh nghiệp:** Giá lịch sử, khối lượng giao dịch, các chỉ số tài chính (ROE, ROA, P/E, P/B).
- **Biến số vĩ mô:** Tăng trưởng GDP, lạm phát (CPI), lãi suất và tỷ giá hối đoái.
- **Yếu tố ngành:** Giá thép thế giới, giá quặng sắt và giá than cốc.

## ⚙️ Phương pháp nghiên cứu (Tiếp cận Hybrid)
Dự án sử dụng kết hợp nhiều mô hình để tối ưu hóa độ chính xác:
- **Thống kê & Học máy:**
  - **SARIMAX:** Xử lý dữ liệu chuỗi thời gian có biến ngoại sinh.
  - **SVR (Support Vector Regression):** Nắm bắt các mối quan hệ phi tuyến.
- **Học sâu (Deep Learning):**
  - **RNN & LSTM:** Nhận diện các phụ thuộc dài hạn trong chuỗi giá.
- **Phân tích rủi ro và Trạng thái thị trường:**
  - **GARCH:** Dự báo biến động (volatility).
  - **Hidden Markov Model (HMM):** Phân loại trạng thái thị trường (Tăng giá, Đi ngang, Giảm giá).

## 🚀 Kết quả chính
- **Hiệu quả mô hình:**
  - **SARIMAX** cho kết quả vượt trội với các mã có thanh khoản cao (HPG, HSG, NKG, POM).
  - **SVR** phù hợp nhất để dự báo cho mã **TVN**.
- **Khả năng dự báo:** Các mô hình đạt độ tin cậy cao nhất trong ngắn hạn (từ 1 đến 3 phiên kế tiếp) và giảm dần độ chính xác khi thời gian dự báo kéo dài.

## 🛠 Cấu trúc dự án
- `data/`: Chứa dữ liệu thô và dữ liệu đã qua xử lý.
- `models/`: Các mã nguồn triển khai SARIMAX, SVR, LSTM và HMM.
- `notebooks/`: Phân tích dữ liệu khám phá (EDA) và kết quả thử nghiệm.
- `reports/`: Báo cáo cuối kỳ chi tiết và tài liệu liên quan.

## 📝 Nhóm tác giả
- **Giảng viên hướng dẫn:** TS. Trần Quang Thắng
- **Sinh viên thực hiện:** Đỗ Hồng Phúc, Nguyễn Phạm Minh Huy, Mọc Đông Nhi, Phạm Hữu Anh Toàn.
- **Lớp - Khóa:** IVP001 - K49, Đại học Kinh tế TP. Hồ Chí Minh (UEH).

## ⚠️ Hạn chế
Mô hình có thể giảm hiệu suất trước các sự kiện "Thiên nga đen" hoặc các thay đổi cấu trúc đột ngột của thị trường. Khuyến nghị nên cập nhật và tái huấn luyện mô hình thường xuyên với dữ liệu thời gian thực.
