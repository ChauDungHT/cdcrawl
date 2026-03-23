import os
from google.genai import Client
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API")

client = Client(api_key=api_key)

try:
    # 1. Liệt kê các model có sẵn (Cú pháp mới: client.models.list)
    print("Danh sách các Model khả dụng cho tài khoản của bạn:")
    for model in client.models.list():
        print(f"  > {model.name}")

except Exception as e:
    print(f"Lỗi: Có vấn đề xảy ra. Chi tiết: {e}")