# --- THIẾT LẬP LOGGING CHO searchByElement.py ---
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    handlers=[
                        logging.FileHandler('log.txt', mode='a', encoding='utf-8'),
                        logging.StreamHandler()
                    ])

# Ghi log khi bắt đầu tìm kiếm bài báo
logging.info('Bắt đầu tìm kiếm bài báo tại %s', 'https://dantri.com.vn/')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementClickInterceptedException
import os
import json
from datetime import datetime

BRAVE_EXE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" 
DEFAULT_URL = "https://dantri.com.vn/"
XPATH_ARTICLE_CONTENT = "//h1 | //p | //span | //a"
XPATH_PARENT = "/html/body/nav/ol/li"

class ArticleFinder:
    ITEMS_PER_PAGE = 10

    @staticmethod
    def generate_file_path(base_dir=r"E:\cd\cdcrawl\data\url"):
        """
        Tạo đường dẫn file đầy đủ dựa trên thời gian hiện tại.
        Đảm bảo thư mục tồn tại trước khi trả về đường dẫn.
        """
        # 1. Kiểm tra và tạo thư mục nếu chưa có
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            print(f"Created directory: {base_dir}")

        # 2. Tạo tên file: YYYYMMDD_HHMMSS.json
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{timestamp}.json"
        
        # 3. Kết hợp thành đường dẫn tuyệt đối
        return os.path.join(base_dir, file_name)

    def fetch_urls_by_count(self):
        key_word = input("Nhập vào từ khóa muốn tìm kiếm: ")
        count = int(input("Nhập vào số lượng bài báo muốn tìm kiếm: "))
        pages_to_click = (count - 1) // self.ITEMS_PER_PAGE

        chrome_options = Options()
        chrome_options.binary_location = BRAVE_EXE_PATH

        # Các tham số tối ưu (Features kỹ thuật khi crawl)
        chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(options=chrome_options)

        try:
            driver.get(DEFAULT_URL)
            explicit_wait = wait(driver, 15)
            explicit_wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            explicit_wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/header")))

            # Tìm và click nút search (click vào button cha của svg)
            try:
                search_button = explicit_wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/header/div/div[4]/div[1]/button")))
                search_button.click()
                time.sleep(0.5)
            except Exception as err:
                logging.error(f"Không thể tìm thấy nút search: {err}")
                return

            # Nhập từ khóa và thực hiện tìm kiếm
            try:
                search_input = explicit_wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text' or @placeholder='Tìm kiếm']")))
                search_input.send_keys(key_word)
                time.sleep(0.5)
                search_input.send_keys(Keys.ENTER)
                time.sleep(2)
            except Exception as err:
                logging.error(f"Không thể thực hiện tìm kiếm: {err}")
                return

            # Pagination loop
            scraped_data = []
            current_page = 0
            while len(scraped_data) < count and current_page <= pages_to_click:
                # Lấy tất cả article trong div[4]
                result_elements = driver.find_elements(By.XPATH, "/html/body/main/div[1]/div[1]/div[4]/article")
                for result in result_elements:
                    if len(scraped_data) >= count:
                        break
                    try:
                        title_element = result.find_element(By.XPATH, "./div[2]/h3/a")
                        title = title_element.get_attribute("textContent").strip()
                        url = title_element.get_attribute("href")
                        scraped_data.append({"title": title, "url": url})
                    except (StaleElementReferenceException, TimeoutException) as err:
                        logging.error(f"Lỗi khi xử lý parent [{result}]: {err}")
                        continue

                if len(scraped_data) < count:
                    # Click nút chuyển trang
                    try:
                        next_button = explicit_wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/div[1]/div[5]/li[7]")))
                        next_button.click()
                        time.sleep(1)
                        current_page += 1
                    except (ElementClickInterceptedException, Exception) as e:
                        logging.error(f"Không thể click nút chuyển trang: {e}")
                        break

            if scraped_data:
                target_path = self.generate_file_path()
                
                try:
                    with open(target_path, 'w', encoding='utf-8') as f:
                        json.dump(scraped_data, f, ensure_ascii=False, indent=4)
                        logging.info(f"Đã lưu kết quả tìm kiếm vào: {target_path}")
                except Exception as e:
                    logging.error(f"Failed to write file: {e}")
        finally:
            driver.quit()

if __name__ == "__main__":
    finder = ArticleFinder()
    finder.fetch_urls_by_count()
