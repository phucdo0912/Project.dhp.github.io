# Phân Tích Dữ Liệu Sản Phẩm Amazon (Amazon Products Analysis)

## 📌 Tổng quan dự án
File Notebook này thực hiện quy trình phân tích dữ liệu toàn diện trên tập dữ liệu sản phẩm của Amazon. Mục tiêu chính là làm sạch, biến đổi và trích xuất các thông tin giá trị từ thuộc tính sản phẩm để hỗ trợ việc đánh giá hiệu năng kinh doanh và hành vi người dùng.

## ⚙️ Các thao tác xử lý chính

* **Khởi tạo môi trường và thiết lập tham số hệ thống:** Cấu hình các thư viện phân tích cốt lõi (`Pandas`, `NumPy`) và các công cụ trực quan hóa dữ liệu (`Matplotlib`, `Seaborn`), đồng thời tối ưu hóa các tùy chọn hiển thị để kiểm soát luồng dữ liệu lớn một cách hiệu quả.
* **Khám phá dữ liệu sơ bộ (Exploratory Data Analysis - EDA):** Thực hiện truy vấn cấu trúc tập dữ liệu nhằm xác định các thuộc tính định danh, phân loại kiểu dữ liệu và đánh giá tổng quan về phân phối của các biến số chính trong danh mục sản phẩm.
* **Kiểm định chất lượng và tính toàn vẹn của dữ liệu:** Phân tích mật độ các giá trị khuyết thiếu (null values) và kiểm tra tính duy nhất của dữ liệu để xác định các bản ghi trùng lặp, đảm bảo tính chính xác cho các bước phân tích tiếp theo.
* **Tiền xử lý và Chuẩn hóa dữ liệu (Data Cleaning & Normalization):**
    * **Tái cấu trúc dữ liệu số:** Chuyển đổi các trường dữ liệu như giá cả và tỷ lệ chiết khấu từ định dạng văn bản (chứa ký tự đặc biệt như ₹, %) sang định dạng số thực.
    * **Xử lý dữ liệu phân cấp:** Phân tách và chuẩn hóa các cột dữ liệu phức tạp như danh mục sản phẩm (category) để phục vụ phân tích đa chiều.
* **Kỹ thuật đặc trưng nâng cao (Feature Engineering):** Thiết lập mô hình tính toán chỉ số sức mạnh sản phẩm (`product_score`) thông qua hàm logarit, kết hợp giữa điểm đánh giá định tính (rating), tỷ lệ ưu đãi và quy mô tương tác của người dùng (rating count).
* **Phân tích thứ hạng và Đánh giá hiệu năng:** Áp dụng các thuật toán sắp xếp và bộ lọc đa tiêu chí để chiết xuất nhóm sản phẩm có hiệu quả kinh doanh và mức độ ưu tiên cao nhất, từ đó đưa ra các nhận định chiến lược về sản phẩm.

## 🛠 Công nghệ sử dụng
- **Ngôn ngữ:** Python
- **Thư viện:** Pandas, NumPy, Matplotlib, Seaborn
- **Môi trường:** Jupyter Notebook

## 📊 Kết quả đạt được
- Làm sạch và chuẩn hóa thành công tập dữ liệu với hơn 1,400 bản ghi.
- Xây dựng được thang đo đánh giá sản phẩm tiềm năng dựa trên dữ liệu thực tế.
- Trực quan hóa mối tương quan giữa giá trị giảm giá và phản hồi của người dùng.
