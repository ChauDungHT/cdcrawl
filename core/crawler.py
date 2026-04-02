import sys
from pathlib import Path
# Thêm thư mục gốc của dự án vào sys.path
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

import logging
import utils.loggingConfig
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import sys
import time
from pathlib import Path
import json

# Thêm đường dẫn gốc dự án vào sys.path để import packages
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# --- CONSTANTS ---
DEFAULT_URL = "https://dantri.com.vn"
BRAVE_EXE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
RAW_DATA_DIR = r"E:\cd\cdcrawl\data\raw"
BACKUP_DATA_DIR = r"E:\cd\cdcrawl\data\backup"
XPATH_ARTICLE_CONTENT = "//h1 | //p | //span"

def fetch_dantri_article(article_url: str = DEFAULT_URL) -> str:
    """Thực hiện kết nối và cào dữ liệu thô từ bài báo, trả về chuỗi văn bản thô."""
    chrome_options = Options()
    chrome_options.binary_location = BRAVE_EXE_PATH

    # Các tham số tối ưu (Features kỹ thuật khi crawl) [cite: 37]
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    start_time = time.time() # Tính thời gian tải trang (Feature 39) [cite: 39]

    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        logging.info(f"Bắt đầu crawl URL: {article_url}") # Feature 3 (URL bài viết) [cite: 3]
        driver.get(article_url)
        
        # Chờ trang tải đầy đủ
        driver.implicitly_wait(10)
        load_time = round(time.time() - start_time, 2)
        logging.info(f"Thời gian tải trang: {load_time}s") # Feature 39 [cite: 39]

        # GIAI ĐOẠN 1: Thu thập nội dung (Lấy đủ thẻ cho Feature 9 & 11) [cite: 9, 11]
        content_elements = driver.find_elements(By.XPATH, XPATH_ARTICLE_CONTENT)
        
        article_text_list = []
        for el in content_elements:
            try:
                text_value = el.text.strip()
                if text_value: 
                    article_text_list.append(text_value)
            except Exception:
                continue

        raw_text = "\n".join(article_text_list)

        # GIAI ĐOẠN 2: Lưu kết quả và ghi log trạng thái (Feature 43) [cite: 43]
        if raw_text:
            name = save_raw_content(article_text_list, article_url)
            logging.info("Trạng thái: Crawl thành công bài viết.") # Feature 43 [cite: 43]
            return raw_text, name
        else:
            logging.warning("Trạng thái: Thất bại - Không tìm thấy nội dung.") # Feature 43 [cite: 43]
            return ""

    except Exception as error_msg:
        logging.error(f"Lỗi kỹ thuật khi crawl: {error_msg}") # Feature 43 [cite: 43]
        return ""
    finally:
        if 'driver' in locals():
            driver.quit()
            logging.info("Đã đóng trình duyệt. Kết thúc phiên làm việc.")

def save_raw_content(article_data: list[str], url: str) -> str:
    """Lưu danh sách nội dung thu thập được vào file .txt theo số thứ tự, kèm URL và backup."""
    # Đảm bảo thư mục RAW tồn tại (Feature 44) [cite: 44]
    if not os.path.exists(RAW_DATA_DIR): 
        os.makedirs(RAW_DATA_DIR)
        logging.info(f"Đã tạo thư mục lưu trữ: {RAW_DATA_DIR}")

    # Đếm số file hiện có để đặt tên file tiếp theo
    existing_file_count = len([f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.txt')])
    new_filename = f"crawl_{existing_file_count + 1}.txt"
    full_file_path = os.path.join(RAW_DATA_DIR, new_filename)

    # Chuẩn bị nội dung file
    file_content = f"URL: {url}\n\n"
    for text_line in article_data:
        file_content += text_line + "\n"

    # Lưu file vào RAW_DATA_DIR
    try:
        with open(full_file_path, "w", encoding="utf-8") as file_out:
            file_out.write(file_content)
        logging.info(f"Đã lưu dữ liệu thành công vào: {full_file_path}") 
    except IOError as io_error:
        logging.error(f"Không thể ghi file tại {full_file_path}: {io_error}")
        return full_file_path

    # Đảm bảo thư mục BACKUP tồn tại
    if not os.path.exists(BACKUP_DATA_DIR):
        os.makedirs(BACKUP_DATA_DIR)
        logging.info(f"Đã tạo thư mục backup: {BACKUP_DATA_DIR}")

    # Lưu file backup
    backup_file_path = os.path.join(BACKUP_DATA_DIR, new_filename)
    try:
        with open(backup_file_path, "w", encoding="utf-8") as backup_file:
            backup_file.write(file_content)
        logging.info(f"Đã lưu file backup thành công vào: {backup_file_path}")
    except IOError as io_error:
        logging.error(f"Không thể ghi file backup tại {backup_file_path}: {io_error}")

    return full_file_path

def clear_url_data():
    """Dọn dẹp thư mục url sau khi xử lý xong."""
    url_dir = Path(r"E:\cd\cdcrawl\data\url")
    for file in url_dir.glob("*.json"):
        file.unlink()
    logging.info("Đã dọn dẹp thư mục url.")

def batch_crawl():
    """Quét thư mục url và cào dữ liệu từ tất cả file JSON."""
    url_dir = Path(r"E:\cd\cdcrawl\data\url")
    for json_file in url_dir.glob("*.json"):
        logging.info(f"Đang xử lý file: {json_file.name}")
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for item in data:
                url = item['url']
                logging.info(f"Đang cào URL: {url}")
                try:
                    fetch_dantri_article(url)
                except Exception as e:
                    logging.error(f"Lỗi khi cào {url}: {e}")
                    continue
        except Exception as e:
            logging.error(f"Lỗi khi xử lý file {json_file}: {e}")
    clear_url_data()

if __name__ == "__main__":
    batch_crawl()