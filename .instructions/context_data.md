# Style Guide - Dan Tri News Crawler (Python 3.14)

Tài liệu này quy định các tiêu chuẩn lập trình để đảm bảo mã nguồn dự án crawl dữ liệu từ báo Dân Trí luôn nhất quán, dễ bảo trì và tận dụng tối đa hiệu suất của Python 3.14.

---

## 1. Tiêu chuẩn chung (General Standards)
* **PEP 8:** Tuân thủ tuyệt đối quy tắc đặt tên và trình bày code.
* **Độ dài dòng:** Tối đa **100 ký tự** để phù hợp với màn hình hiện đại.
* **Ngôn ngữ:** * Code (Biến, Hàm, Class): **Tiếng Anh**.
    * Comments/Docstrings: **Tiếng Việt** (để mô tả logic nghiệp vụ crawl báo chí).
* **Định dạng:** Sử dụng `black` để tự động format code trước khi commit.

---

## 2. Đặc trưng Python 3.14+
* **Type Hinting (Bắt buộc):** Sử dụng cú pháp Type Hinting mới nhất.
    * Ví dụ: `list[str] | None` thay vì `Optional[List[str]]`.
* **Pattern Matching:** Sử dụng `match-case` để phân loại cấu trúc HTML (ví dụ: bài viết dạng Ảnh, Video, hoặc Infographic).
* **F-strings:** Tận dụng hiệu suất của f-strings để tạo URL và log message.

---

## 3. Quy định đặt tên (Naming Conventions)

| Thành phần | Định dạng | Ví dụ |
| :--- | :--- | :--- |
| **Module / File** | `snake_case` | `dantri_parser.py`, `database_helper.py` |
| **Class** | `PascalCase` | `DantriCrawler`, `ArticleCleaner` |
| **Function / Method** | `snake_case` | `fetch_article()`, `get_author_info()` |
| **Variable** | `snake_case` | `article_url`, `retry_count` |
| **Constants** | `UPPER_CASE` | `BASE_URL = "https://dantri.com.vn"`, `MAX_RETRIES = 5` |
| **Selectors** | `PREFIX_` | `CSS_TITLE_SELECTOR`, `XPATH_CONTENT` |

---

## 4. Kiến trúc Crawler & Quy trình xử lý dữ liệu

Dự án tuân thủ quy trình xử lý dữ liệu theo 3 bước tuần tự để đảm bảo tính toàn vẹn của nội dung từ báo Dân Trí:

### 4.1. Giai đoạn 1: Thu thập nội dung thô (Raw Crawling)
* **Phạm vi:** Trích xuất toàn bộ nội dung nằm trong các thẻ hiển thị văn bản, chủ yếu là thẻ `<p>` (đoạn văn) và thẻ `<a>` (liên kết/neo văn bản).
* **Yêu cầu:** Không lọc bỏ dữ liệu ở bước này, lấy tất cả các node văn bản có khả năng chứa thông tin hữu ích.
* **Công cụ:** Ưu tiên sử dụng các thư viện parse HTML mạnh mẽ như `BeautifulSoup` hoặc `lxml`.

### 4.2. Giai đoạn 2: Lọc và Kết xuất (Filtering to TXT)
* **Xử lý:** Loại bỏ các thành phần rác (quảng cáo, script, menu điều hướng) không nằm trong các thẻ mục tiêu.
* **Lưu trữ:** Dữ liệu sau khi lọc được ghi vào file `.txt` trung gian. 
* **Cấu trúc file .txt:** Mỗi thành phần nội dung (tiêu đề, đoạn văn, link) phải được phân tách rõ ràng (ví dụ: mỗi thẻ một dòng hoặc phân cách bằng ký tự đặc biệt) để phục vụ bước format.

### 4.3. Giai đoạn 3: Chuẩn hóa định dạng (Final Formatting)
* **Mục tiêu:** Đọc từ file `.txt` và chuyển đổi sang định dạng mẫu cuối cùng (JSON, CSV hoặc Markdown tùy theo yêu cầu đề tài).
* **Quy tắc:**
    * Làm sạch khoảng trắng thừa.
    * Chuẩn hóa bảng mã tiếng Việt.
    * Gắn nhãn (labeling) cho các thành phần dữ liệu (ví dụ: Đề mục, Nội dung chính, Tác giả).

---

## 5. Ví dụ Code chuẩn (Template)

```python
import logging
from typing import Any

# Khai báo Selector riêng biệt
SELECTORS = {
    "title": "h1.title-page",
    "body": ".singular-content",
}

class ArticleParser:
    """Lớp xử lý bóc tách dữ liệu từ HTML báo Dân Trí."""

    def __init__(self, html_content: str):
        self.html = html_content

    def extract_data(self) -> dict[str, Any] | None:
        """Trích xuất tiêu đề và nội dung bài viết."""
        try:
            # Giả lập logic bóc tách
            title = self._get_element(SELECTORS["title"])
            if not title:
                raise ValueError("Không tìm thấy tiêu đề bài viết")
                
            return {
                "title": title.strip(),
                "source": "Dân Trí"
            }
        except Exception as e:
            logging.error(f"Lỗi khi parse HTML: {e}")
            return None

    def _get_element(self, selector: str) -> str | None:
        # Logic sử dụng BeautifulSoup hoặc Selectolax
        ...