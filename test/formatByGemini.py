import os
import sys
import logging
from google.genai import Client
from dotenv import load_dotenv

# Đảm bảo thư mục gốc của project có trong sys.path để import module từ folder utils
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from utils.loggingConfig import setup_global_logging

setup_global_logging()

load_dotenv()
GEMINI_API_KEY = os.getenv("API")
MODEL_NAME = "gemini-2.5-flash" 

client = Client(api_key=GEMINI_API_KEY)

def analyze_article_content(text_content: str) -> str:
    """
    Sử dụng Gemini AI (SDK mới) để trích xuất Features báo chí.
    """
    
    analysis_prompt = f"""
    Bạn là một chuyên gia phân tích dữ liệu báo chí cao cấp. 
    Nhiệm vụ của bạn là trích xuất thông tin từ đoạn văn bản thô dưới đây và chuyển đổi thành định dạng JSON chính xác.

    Nội dung thô cần phân tích:
    ---
    {text_content}
    ---

    Yêu cầu định dạng JSON đầu ra (phải giữ đúng tên key):
    1. "Title": Tiêu đề chính của bài báo.
    2. "BriefDescription": Đoạn sapo hoặc mô tả ngắn gọn nội dung.
    3. "DateOfPublication": Ngày và giờ xuất bản bài viết.
    4. "NewsType": Xác định chủ đề (Ví dụ: Thời sự, Thể thao, Giáo dục, Công nghệ...).
    5. "ArticleFormat": Hình thức trình bày (Ví dụ: Tin ngắn, Phóng sự, Bình luận, Phân tích).
    6. "SourceInformation": Các thông tin về nguồn trích dẫn dữ liệu được nhắc đến trong bài.

    Lưu ý quan trọng: 
    - Nếu thông tin nào không có trong văn bản, hãy để giá trị là null.
    - Chỉ trả về duy nhất khối JSON, không kèm theo lời giải thích nào khác.
    """

    try:
        ai_response = client.models.generate_content(
            model=MODEL_NAME,
            contents=analysis_prompt
        )
        return ai_response.text
    except Exception as error_msg:
        logging.error(f"❌ Lỗi gọi Gemini API: {error_msg}")
        return None

def save_structured_json(json_data: str, output_path: str) -> None:
    """Lưu kết quả JSON sau khi phân tích."""
    if not json_data:
        return
        
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as json_file:
            json_file.write(json_data)
        logging.info(f"✅ Đã lưu kết quả phân tích vào: {output_path}")
    except IOError as io_error:
        logging.error(f"❌ Không thể ghi file JSON: {io_error}")

import json
import re
import logging

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
            return data
        else:
            logging.error("❌ Không tìm thấy cấu trúc JSON trong phản hồi của AI.")
            return None
            
    except json.JSONDecodeError as e:
        logging.error(f"❌ Lỗi định dạng JSON: {e}")
        return None
    except Exception as e:
        logging.error(f"❌ Lỗi xử lý nhiễu: {e}")
        return None

if __name__ == "__main__":
    input_raw_file = "data/raw/dantri_raw_content.txt"
    output_json_file = "data/processed/dantri_structured_data.json"

    if os.path.exists(input_raw_file):
        with open(input_raw_file, "r", encoding="utf-8") as file_in:
            raw_article_text = file_in.read()
        
        # Thực hiện gọi AI
        structured_result = analyze_article_content(raw_article_text)
        cleaned_data = clean_gemini_json(structured_result)
        # Lưu file
        if cleaned_data:
            save_structured_json(json.dumps(cleaned_data), output_json_file)
    else:
        logging.error(f"⚠️ Không tìm thấy file đầu vào tại: {input_raw_file}")