# Dân Trí News Crawler

## Mô tả dự án

Dự án này là một công cụ thu thập dữ liệu (crawler) tự động dành cho trang web báo Dân Trí (dantri.com.vn). Nó sử dụng Selenium WebDriver để truy cập và trích xuất nội dung bài viết, sau đó lưu trữ dữ liệu thô vào file văn bản để phục vụ phân tích và xử lý tiếp theo.

### Tính năng chính
- Thu thập nội dung thô từ các bài viết trên Dân Trí.
- Sử dụng trình duyệt Brave hoặc Chrome trong chế độ headless để tránh phát hiện tự động.
- Lưu trữ dữ liệu vào file `.txt` với định dạng dễ đọc.
- Hỗ trợ logging chi tiết để theo dõi quá trình crawl.

### Công nghệ sử dụng
- **Ngôn ngữ**: Python 3.14
- **Thư viện chính**:
  - Selenium: Để điều khiển trình duyệt và tương tác với trang web.
  - WebDriver Manager: Quản lý tự động ChromeDriver.
  - Logging: Ghi log các sự kiện trong quá trình crawl.
- **Công cụ bổ sung**: BeautifulSoup (đề xuất cho parsing HTML trong tương lai).

### Quy trình xử lý dữ liệu
Dự án tuân thủ quy trình 3 giai đoạn:
1. **Thu thập nội dung thô**: Trích xuất văn bản từ thẻ `<p>` và `<a>`.
2. **Lọc và lưu trữ**: Loại bỏ dữ liệu rác và ghi vào file `.txt`.
3. **Chuẩn hóa định dạng**: Chuyển đổi sang JSON hoặc định dạng khác nếu cần.

### Yêu cầu hệ thống
- Python 3.14+
- Trình duyệt Brave hoặc Chrome đã cài đặt.
- Các thư viện trong `requirement.txt`.

### Cài đặt
1. Clone repository này.
2. Tạo virtual environment: `python -m venv venv`
3. Kích hoạt venv: `venv\Scripts\activate` (Windows)
4. Cài đặt dependencies: `pip install -r requirement.txt`
5. Đổi tên file `.env.example` thành `.env` và điền API key cho Gemini (GEMINI_API_KEY).
6. Tạo thư mục `data` và các thư mục con `raw` và `processed`: `mkdir -p data/raw data/processed`
7. Chạy chương trình chính: `python main.py` và nhập URL bài báo Dân Trí khi được yêu cầu.

### Sử dụng
Chạy chương trình chính:
```bash
python main.py
```
Chương trình sẽ yêu cầu nhập URL bài báo Dân Trí, sau đó crawl dữ liệu thô, phân tích bằng Gemini AI và lưu kết quả JSON vào `data/processed/`.

### Hướng dẫn lập trình
- Tuân thủ Style Guide trong `.instructions/style_guide.md`.
- Sử dụng Type Hinting và Pattern Matching của Python 3.14.
- Thực hiện kiểm thử theo `testing_guide.md`.