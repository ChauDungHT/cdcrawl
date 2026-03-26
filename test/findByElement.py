from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

# Giả định các biến này đã được bạn định nghĩa trong test.crawl
# Nếu chưa có, bạn hãy thay đường dẫn thực tế vào đây
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

        # Bước 1: Khởi tạo và Tải trang (Page Loading)
        driver.get(article_url)
        explicit_wait = wait(driver, 15)
        explicit_wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        explicit_wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/nav")))

        # Bước 2: Tương tác mở rộng Menu (Action)
        try:
            hidden_button = explicit_wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/nav/ol/li[18]/svg[1]")))
            hidden_button.click()
            time.sleep(0.5)
        except Exception:
            pass  # bỏ qua nếu không tìm thấy nút

        # Bước 3: Định vị và Trích xuất phần tử Cha (Parent Nodes)
        parent_elements = driver.find_elements(By.XPATH, "/html/body/nav/nav/div/ol/li")

        # Bước 4: Duyệt vòng lặp và Bóc tách dữ liệu Con (Iterate & Extract)
        for parent in parent_elements:
            try:
                # Trích xuất Tên thẻ Cha
                parent_name = parent.find_element(By.XPATH, "./a").text.strip()

                # Trích xuất Thẻ Con
                child_elements = parent.find_elements(By.XPATH, ".//ol/li")

                # Trích xuất Tên thẻ Con
                child_names = []
                for child in child_elements:
                    try:
                        child_name = child.find_element(By.XPATH, "./a").text.strip()
                        child_names.append(child_name)
                    except Exception:
                        continue  # bỏ qua nếu không tìm thấy ./a

                # Bước 5: Định dạng Đầu ra (Console Output)
                if not child_names:
                    print(f"Phần tử [{parent_name}] không có phần tử con.")
                else:
                    print(f"Phần tử [{parent_name}] gồm: {', '.join(child_names)}")

            except (StaleElementReferenceException, TimeoutException) as err:
                print(f"Lỗi khi xử lý parent: {err}")
                continue

        print("Done!")

    finally:
        driver.quit()

# Chạy thử
if __name__ == "__main__":
    fetch_dantri_article()