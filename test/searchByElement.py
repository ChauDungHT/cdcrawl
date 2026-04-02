

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

BRAVE_EXE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" 
DEFAULT_URL = "https://dantri.com.vn/"
XPATH_ARTICLE_CONTENT = "//h1 | //p | //span | //a"
XPATH_PARENT = "/html/body/nav/ol/li"
#key_word = input("Nhập vào từ khóa muốn tìm kiếm: ")
#count = int(input("Nhập vào số lượng kết quả muốn lấy: "))

def search_dantri_article(article_url: str = DEFAULT_URL, key_word: str = None) -> None:
    """Thực hiện kết nối và tìm kiếm bài báo."""
    if key_word is None:
        key_word = input("Nhập vào từ khóa muốn tìm kiếm: ")
    
    chrome_options = Options()
    chrome_options.binary_location = BRAVE_EXE_PATH

    # Các tham số tối ưu (Features kỹ thuật khi crawl)
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    start_time = time.time()

    try:
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(article_url)
        explicit_wait = wait(driver, 15)
        explicit_wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        explicit_wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/header")))

        # Tìm và click nút search (click vào button cha của svg)
        try:
            search_button = explicit_wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/header/div/div[4]/div[1]/button")))
            search_button.click()
            time.sleep(0.5)
        except Exception as err:
            print(f"Không thể tìm thấy nút search: {err}")
            pass

        # Nhập từ khóa và thực hiện tìm kiếm
        try:
            search_input = explicit_wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text' or @placeholder='Tìm kiếm']")))
            search_input.send_keys(key_word)
            time.sleep(0.5)
            search_input.send_keys(Keys.ENTER)
            time.sleep(2)
            # Lấy tất cả article trong div[4]
            result_elements = driver.find_elements(By.XPATH, "/html/body/main/div[1]/div[1]/div[4]/article")
            for result in result_elements:
                try:
                    parent_name = result.get_attribute("textContent")
                    if not parent_name:
                        continue
                    title_element = result.find_element(By.XPATH, "./div[2]/h3/a")
                    title = title_element.get_attribute("textContent").strip()
                    print(f"Title: {title}")
                except (StaleElementReferenceException, TimeoutException) as err:
                    print(f"Lỗi khi xử lý parent [{parent_name}]: {err}")
                continue
        except Exception as err:
            print(f"Không thể thực hiện tìm kiếm: {err}")

    finally:
        driver.quit()

if __name__ == "__main__":
    search_dantri_article()
