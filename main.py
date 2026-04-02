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

from core.finder import ArticleFinder
from core.crawler import batch_crawl
from core.formater import batch_format

def main():
    """
    Luồng chính: Finder -> Crawler -> Formater
    
    Bước 1: Finder - Tìm kiếm và thu thập URLs
    Bước 2: Crawler - Cào dữ liệu thô từ các URLs
    Bước 3: Formater - Phân tích và định dạng dữ liệu bằng Gemini AI
    """
    logging.info('=== BẮT ĐẦU CHƯƠNG TRÌNH CHÍNH ===')
    try:
        # === BƯỚC 1: FINDER ===
        logging.info('Bước 1: Tìm kiếm các bài báo và lưu URLs...')
        finder = ArticleFinder()
        finder.fetch_urls_by_count()
        logging.info('Hoàn thành bước 1: Finder')

        # === BƯỚC 2: CRAWLER ===
        logging.info('Bước 2: Cào dữ liệu thô từ các URLs...')
        batch_crawl()
        logging.info('Hoàn thành bước 2: Crawler')

        # === BƯỚC 3: FORMATER ===
        logging.info('Bước 3: Phân tích và định dạng dữ liệu bằng Gemini AI...')
        batch_format()
        logging.info('Hoàn thành bước 3: Formater')

        logging.info('=== HOÀN THÀNH TOÀN BỘ QUY TRÌNH ===')
        print("✓ Quy trình xử lý dữ liệu hoàn tất thành công!")

    except Exception as e:
        logging.error(f'Lỗi trong quá trình thực thi: {e}')
        print(f"✗ Lỗi: {e}")

if __name__ == "__main__":
    main()