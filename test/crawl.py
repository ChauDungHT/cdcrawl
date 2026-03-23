import logging
import utils.loggingConfig
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time

# --- CONSTANTS ---
DEFAULT_URL = "https://dantri.com.vn"
BRAVE_EXE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
RAW_DATA_DIR = r"D:\cdcrawl\data\raw"
XPATH_ARTICLE_CONTENT = "//h1 | //p | //span | //a"

def fetch_dantri_article(article_url: str = DEFAULT_URL) -> None:
    """Thực hiện kết nối và cào dữ liệu thô từ bài báo."""
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

        # GIAI ĐOẠN 2: Lưu kết quả và ghi log trạng thái (Feature 43) [cite: 43]
        if article_text_list:
            save_raw_content(article_text_list)
            logging.info("Trạng thái: Crawl thành công bài viết.") # Feature 43 [cite: 43]
        else:
            logging.warning("Trạng thái: Thất bại - Không tìm thấy nội dung.") # Feature 43 [cite: 43]

    except Exception as error_msg:
        logging.error(f"Lỗi kỹ thuật khi crawl: {error_msg}") # Feature 43 [cite: 43]
    finally:
        if 'driver' in locals():
            driver.quit()
            logging.info("Đã đóng trình duyệt. Kết thúc phiên làm việc.")

def save_raw_content(article_data: list[str]) -> None:
    """Lưu danh sách nội dung thu thập được vào file .txt theo số thứ tự."""
    # Đảm bảo thư mục tồn tại (Feature 44) [cite: 44]
    if not os.path.exists(RAW_DATA_DIR): 
        os.makedirs(RAW_DATA_DIR)
        logging.info(f"Đã tạo thư mục lưu trữ: {RAW_DATA_DIR}")

    # Đếm số file hiện có để đặt tên file tiếp theo
    existing_file_count = len([f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.txt')])
    new_filename = f"crawl_{existing_file_count + 1}.txt"
    full_file_path = os.path.join(RAW_DATA_DIR, new_filename)

    try:
        with open(full_file_path, "w", encoding="utf-8") as file_out:
            for text_line in article_data:
                file_out.write(text_line + "\n")
        
        # Log lại thời điểm lưu thành công (Feature 44) [cite: 44]
        logging.info(f"Đã lưu dữ liệu thành công vào: {full_file_path}") 
    except IOError as io_error:
        logging.error(f"Không thể ghi file tại {full_file_path}: {io_error}")

if __name__ == "__main__":
    TARGET_ARTICLE_URL = "https://dantri.com.vn/the-gioi/eo-bien-bab-el-mandeb-quan-bai-cua-iran-trong-cuoc-chien-voi-my-israel-20260321230308339.htm"
    fetch_dantri_article(TARGET_ARTICLE_URL)