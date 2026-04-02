import os
import sys
import logging
from google.genai import Client
from dotenv import load_dotenv
from pathlib import Path

# Đảm bảo thư mục gốc của project có trong sys.path để import module từ folder utils
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

INPUT_RAW_FOLDER = os.path.join(ROOT_DIR, "data", "raw")
OUTPUT_PROCESSED_FOLDER = os.path.join(ROOT_DIR, "data", "processed")
BACKUP_PROCESSED_FOLDER = os.path.join(ROOT_DIR, "data", "backup", "processed")

from utils.loggingConfig import setup_global_logging
setup_global_logging()

load_dotenv()
GEMINI_API_KEY = os.getenv("API")
MODEL_NAME = "gemini-2.5-flash" 

client = Client(api_key=GEMINI_API_KEY)

def analyze_article_content(text_content: str, url: str = "") -> str:
    """
    Sử dụng Gemini AI (SDK mới) để trích xuất Features báo chí.
    """
    
    analysis_prompt = f"""
    Bạn là một chuyên gia phân tích dữ liệu báo chí cao cấp, có khả năng bóc tách cấu trúc URL và nội dung văn bản một cách chính xác.
    Nhiệm vụ của bạn là trích xuất thông tin từ URL và đoạn văn bản thô dưới đây để chuyển đổi thành định dạng JSON.

    URL bài viết: {url}

    Nội dung thô cần phân tích:
    ---
    {text_content}
    ---

    HƯỚNG DẪN TRÍCH XUẤT ĐẶC BIỆT:
    1. ID bài viết: Tìm mã số định danh trong URL hoặc trong nội dung văn bản (thường là dãy số cuối URL).
    2. Slug: Là chuỗi định danh không dấu, ngăn cách bằng dấu gạch ngang nằm trong URL.
    3. NewsType: Phân tích từ các thư mục (folders) trên URL.
    4. Tags: Tìm các từ khóa ở cuối bài viết hoặc các cụm từ quan trọng được lặp lại.

    YÊU CẦU ĐỊNH DẠNG JSON (Phải giữ đúng tên key):
    {{
        "ArticleID": "Mã định danh duy nhất của bài báo",
        "URL": "{url}",
        "Slug": "Chuỗi định danh văn bản trong URL",
        "Source": "Tên website hoặc đơn vị chủ quản (ví dụ: Dân Trí)",
        "Title": "Tiêu đề chính của bài báo",
        "BriefDescription": "Đoạn sapo hoặc mô tả ngắn gọn nội dung",
        "Category": "Phân loại lớn của bài báo (Thời sự, Thể thao, Kinh doanh...)",
        "NewsType": "Chủ đề cụ thể lấy từ URL (Chính trị, Giáo dục, Công nghệ...)",
        "ArticleFormat": "Dạng bài (Tin ngắn, Phóng sự, Bình luận, Phân tích...)",
        "Tags": ["Mảng", "Các", "Từ", "Khóa"],
        "DateOfPublication": "Ngày và giờ xuất bản (định dạng YYYY-MM-DD HH:mm)",
        "SourceInformation": "Các thông tin về nguồn gốc dữ liệu/trích dẫn được nhắc đến trong bài",
        "ContentSummary": "Tóm tắt nội dung chính (nếu cần)"
    }}

    Lưu ý quan trọng: 
    - Nếu thông tin nào không thể xác định, hãy để giá trị là null.
    - Phải đảm bảo tính nhất quán của dữ liệu.
    - Chỉ trả về duy nhất khối JSON, không kèm theo lời giải thích nào khác.
    """

    try:
        ai_response = client.models.generate_content(
            model=MODEL_NAME,
            contents=analysis_prompt
        )
        return ai_response.text
    except Exception as error_msg:
        logging.error(f"Lỗi gọi Gemini API: {error_msg}")
        return None



import json
import re

def clean_gemini_json(raw_response: str):
    """
    Loại bỏ các ký tự nhiễu, Markdown và trích xuất đúng định dạng JSON.
    """
    if not raw_response:
        return None

    try:
        json_match = re.search(r"\{.*\}", raw_response, re.DOTALL)
        if json_match:
            clean_str = json_match.group(0)
            data = json.loads(clean_str)
            
            # Trả về chuỗi JSON có xuống dòng, thụt lề 4 khoảng trắng, hỗ trợ tiếng Việt
            return json.dumps(data, indent=4, ensure_ascii=False)
        else:
            logging.error("Không tìm thấy cấu trúc JSON trong phản hồi của AI.")
            return None
    except json.JSONDecodeError as e:
        logging.error(f"Lỗi định dạng JSON: {e}")
        return None
    except Exception as e:
        logging.error(f"Lỗi xử lý nhiễu: {e}")
        return None
    

def save_processed_content(cleaned_data: str, output_folder: str = OUTPUT_PROCESSED_FOLDER) -> None:
    # Đếm số file hiện có để đặt tên file tiếp theo
    #existing_file_count = len([f for f in os.listdir(output_folder) if f.endswith('.json')])
    cleaned = json.loads(cleaned_data)
    article_id = cleaned.get("ArticleID")

    if article_id:
        # Loại bỏ các ký tự không hợp lệ cho tên file (nếu ID lấy từ URL có chứa / hoặc ?)
        safe_id = str(article_id).strip().replace("/", "_")
        new_filename = f"processed_{safe_id}.json"
    else:
        new_filename = "processed_unknown.json"
    full_file_path = os.path.join(output_folder, new_filename)
    try:
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
        with open(full_file_path, "w", encoding="utf-8") as json_file:
            json_file.write(cleaned_data)
        # Log lại thời điểm lưu thành công (Feature 43 & 44)
        logging.info(f"Đã lưu dữ liệu thành công vào: {full_file_path}")
    except IOError as io_error:
        logging.error(f"Không thể ghi file tại {full_file_path}: {io_error}")

def batch_format():
    raw_dir = Path(INPUT_RAW_FOLDER)
    if not raw_dir.exists():
        logging.warning(f"Thư mục {INPUT_RAW_FOLDER} không tồn tại.")
        return

    processed_dir = Path(OUTPUT_PROCESSED_FOLDER)
    processed_dir.mkdir(parents=True, exist_ok=True)

    for file_path in raw_dir.glob("*.txt"):
        logging.info(f"Đang xử lý file: {file_path.name}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            raw_response = analyze_article_content(text_content)
            cleaned_data = clean_gemini_json(raw_response)
            if cleaned_data:
                save_processed_content(cleaned_data)
        except Exception as e:
            logging.error(f"Lỗi xử lý file {file_path}: {e}")
    
    # Dọn dẹp folder raw sau khi format
    cleanup_raw_data()

def cleanup_raw_data():
    """Xóa các file raw đã xử lý khỏi thư mục raw."""
    raw_dir = Path(INPUT_RAW_FOLDER)
    
    if not raw_dir.exists():
        logging.warning(f"Thư mục {INPUT_RAW_FOLDER} không tồn tại.")
        return
    
    # Xóa các file raw
    deleted_count = 0
    for file_path in raw_dir.glob("*.txt"):
        try:
            file_path.unlink()
            deleted_count += 1
            logging.info(f"Đã xóa file: {file_path.name}")
        except Exception as e:
            logging.error(f"Lỗi khi xóa file {file_path.name}: {e}")
    
    logging.info(f"Hoàn thành dọn dẹp: Đã xóa {deleted_count} file raw.")

if __name__ == "__main__":
    batch_format()
