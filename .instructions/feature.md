Quy tắc Trích xuất Dữ liệu Bài báo (Scraping Schema)
Bộ quy tắc này định nghĩa các thuộc tính (features) cần thu thập khi thực hiện crawl dữ liệu từ các trang báo điện tử (ví dụ: Dân Trí).

(OK)1. Nhóm Định danh (Identification Features) (OK)
ID bài viết: Mã định danh duy nhất của bài báo trên hệ thống nguồn. -> Có thể lấy từ URL hoặc meta tag.
URL bài viết: Đường dẫn trực tiếp đến bài báo. -> Thu thập từ trình duyệt.
Slug: Chuỗi định danh văn bản trong URL (thường dùng cho SEO). -> Phân tích từ URL.
Nguồn báo: Tên website hoặc đơn vị chủ quản (ví dụ: Dân Trí). -> Cố định là "Dân Trí" hoặc lấy từ meta tag.
Chuyên mục: Phân loại lớn của bài báo (Thời sự, Thể thao,...). -> Thu thập từ breadcrumb hoặc meta tag.
Thẻ tag: Các từ khóa gắn liền với nội dung bài viết. -> Thu thập từ phần tag hoặc meta tag.

(OK)2. Nhóm Nội dung Văn bản (Content Features)
Tiêu đề: Tên chính của bài báo (thường là thẻ H1).
Sapo / Mô tả ngắn: Đoạn tóm tắt đầu bài viết.
Nội dung chi tiết: Toàn bộ văn bản thô của bài viết.

(OK)3. Nhóm Thời gian (Temporal Features) (OK)
Ngày đăng: Ngày xuất bản bài báo.
Giờ đăng: Thời điểm cụ thể bài báo lên sóng.
Ngày cập nhật: Lần cuối cùng bài báo được chỉnh sửa nội dung.
Thời điểm crawl: Mốc thời gian hệ thống thực hiện lấy dữ liệu.
-> Thu thập từ phần thông tin bài viết.

4. Nhóm Tương tác (Engagement Features) (Bổ sung sau)
Số lượt xem: Tổng số lần người dùng truy cập bài viết. 
Số lượt thích: Lượng tương tác "Like" trên trang. 
Số bình luận: Tổng số phản hồi của độc giả dưới bài viết.
Số lượt chia sẻ: Số lần bài báo được chia sẻ lên các nền tảng xã hội.
Reaction khác: Các biểu cảm cảm xúc khác nếu trang web hỗ trợ.

5. Nhóm Cấu trúc HTML & SEO (Technical Structure) (Bổ sung sau)
Thẻ Title & Meta: Bao gồm Title tag, Meta description và Meta keywords phục vụ SEO.
Heading (H1, H2, H3): Cấu trúc phân cấp các tiêu đề trong bài.
Schema Markup: Các cấu trúc dữ liệu có dạng NewsArticle hoặc Article.
Links: Bao gồm Canonical URL, Internal links, External links và tổng số lượng Hyperlinks.

(OK) 6. Nhóm Phân tích Báo chí (Analytical Features)
Loại tin: Chủ đề chính của nội dung (Chính trị, Giáo dục, Công nghệ,...).
Dạng bài: Hình thức trình bày (Tin ngắn, phóng sự, bình luận, phân tích).
Nguồn trích dẫn: Các thông tin về nguồn gốc dữ liệu được nhắc đến trong bài.

7. Nhóm Vận hành Kỹ thuật (Crawl Logs) (Bổ sung sau)
HTTP Status: Mã phản hồi từ máy chủ (ví dụ: 200, 404).
Hiệu suất: Thời gian tải trang và loại Encoding được sử dụng.
Phân loại trang: Xác định là trang bài viết, trang chuyên mục hay trang chủ.
Trạng thái: Kết quả crawl (Thành công/Thất bại), số lần thử lại và ngày lưu vào database.