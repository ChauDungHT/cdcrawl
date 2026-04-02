from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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

def fetch_dantri_article(article_url: str = DEFAULT_URL) -> None:
    """Thực hiện kết nối và cào dữ liệu thô từ bài báo."""
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
        explicit_wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/nav")))

        try:
            hidden_button = explicit_wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/nav/ol/li[18]/svg[1]")))
            hidden_button.click()
            time.sleep(0.5)
        except Exception:
            pass  
        
        parent_elements = driver.find_elements(By.XPATH, "/html/body/nav/nav/div/ol/li/a")

        for parent in parent_elements:
            try:
                parent_name = parent.get_attribute("textContent")
                if not parent_name:
                    continue
                child_elements = parent.find_elements(By.XPATH, "../ol/li/a")
                child_names = [child.get_attribute("textContent") for child in child_elements if child.get_attribute("textContent")]
                print(f"Parent: {parent_name}, Children: {child_names}")
            except (StaleElementReferenceException, TimeoutException) as err:
                print(f"Lỗi khi xử lý parent [{parent_name}]: {err}")
            continue

    finally:
        driver.quit()

if __name__ == "__main__":
    fetch_dantri_article()