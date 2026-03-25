import os
import sys
import logging
from utils.loggingConfig import setup_global_logging

# Thiết lập logging toàn cục
setup_global_logging()

# Đảm bảo thư mục gốc của project có trong sys.path để import module từ folder core và utils
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.crawler import fetch_dantri_article
from core.formater import analyze_article_content, clean_gemini_json, save_processed_content

def main():
    """Luồng chính: Nhận URL -> Crawl dữ liệu thô -> Phân tích bằng Gemini -> Lưu kết quả JSON."""
    logging.info('Bắt đầu chương trình chính.')
    try:
        # Bước 1: Nhận input URL từ người dùng
        url = input("Nhập URL bài báo Dân Trí: ").strip()
        if not url:
            print("URL không hợp lệ. Thoát chương trình.")
            return

        # Bước 2: Gọi crawl để lấy dữ liệu thô
        logging.info("Đang crawl dữ liệu từ URL...")
        raw_text, name = fetch_dantri_article(url)
        if not raw_text or not name:
            logging.error("Không thể crawl dữ liệu. Thoát chương trình.")
            return

        # Bước 3: Chạy phân tích bằng Gemini
        logging.info("Đang phân tích dữ liệu bằng Gemini AI...")
        structured_result = analyze_article_content(raw_text, url)
        if not structured_result:
            logging.error("Lỗi khi phân tích dữ liệu. Thoát chương trình.")
            return

        cleaned_data = clean_gemini_json(structured_result)
        if not cleaned_data:
            logging.error("Không thể làm sạch dữ liệu JSON. Thoát chương trình.")
            return

        # Bước 4: Lưu kết quả JSON
        save_processed_content(cleaned_data)

    except Exception as e:
        print(f"Lỗi trong quá trình thực thi: {e}")

if __name__ == "__main__":
    main()