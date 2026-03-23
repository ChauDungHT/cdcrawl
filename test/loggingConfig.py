import logging
import os

# --- THIẾT LẬP LOGGING TOÀN CỤC ---
def setup_global_logging():
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    root_logger = logging.getLogger() # Đây là logger gốc (toàn cục)
    root_logger.setLevel(logging.INFO)

    # Nếu đã có handlers (tránh việc tạo trùng lặp khi chạy nhiều lần)
    if not root_logger.handlers:
        # Handler ghi vào file log.txt
        file_handler = logging.FileHandler('log.txt', mode='a', encoding='utf-8')
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)

        # Handler in ra màn hình
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        root_logger.addHandler(console_handler)

# Chạy thiết lập ngay khi load file
setup_global_logging()