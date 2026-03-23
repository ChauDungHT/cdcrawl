# 🛠 Hướng dẫn Lập trình (Style Guide)

Dự án này tập trung vào thu thập dữ liệu (Crawling) và phân tích dữ liệu eSports dựa trên lý thuyết Tập mờ trực giác (IFS). AI cần tuân thủ các quy tắc sau để đảm bảo tính ổn định của hệ thống.

## 1. Môi trường và Thư viện
- **Ngôn ngữ**: Sử dụng Python phiên bản 3.10 để đảm bảo tương thích với các thư viện phân cụm.
- **Thư viện ưu tiên**: 
    - `pandas` cho quản lý dữ liệu bảng.
    - `numpy` cho các phép toán ma trận trong IFS.
    - `scikit-learn` cho tiền xử lý và mô hình hóa.

## 2. Tiêu chuẩn viết Code
- **Hàm (Functions)**: Mọi hàm phải có `docstring` đầy đủ theo định dạng Google hoặc NumPy, giải thích rõ `Args`, `Returns` và `Raises`.
- **Xử lý lỗi**: Đối với các hàm Crawl dữ liệu, bắt buộc sử dụng khối `try-except` để xử lý các lỗi HTTP hoặc lỗi cấu trúc trang web không mong đợi.
- [cite_start]**Tiền xử lý**: Luôn thực hiện chuẩn hóa dữ liệu bằng `StandardScaler` hoặc `MinMaxScaler` (đưa về khoảng [0, 1]) trước khi thực hiện phân cụm hoặc tính toán IFS để đảm bảo các giá trị $\mu, \nu$ hợp lệ[cite: 54].

## 3. Đặc thù Dự án (Data Mining & IFS)
- **Loại bỏ dữ liệu**: Tự động loại bỏ các trường chứa từ khóa "Name" nhưng PHẢI giữ lại các trường "ID" làm khóa định danh.
- [cite_start]**Tính toán IFS**: Khi tính toán hàm thuộc ($\mu$) và không thuộc ($\nu$), phải tuân thủ điều kiện $0 \le \mu_A(x) + \nu_A(x) \le 1$[cite: 54].