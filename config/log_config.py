import sys
from loguru import logger
import os

def setup_logging(log_dir="Logs"):
    # Tạo thư mục log nếu chưa tồn tại
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Xóa cấu hình logging hiện tại
    logger.remove()

    # Thêm các handler và cấu hình mới
    logger.add(
        os.path.join(log_dir, "LogSystem.txt"),  # Đường dẫn tới tệp log
        rotation="500 MB",  # Tạo file log mới khi file đạt kích thước 500 MB
        level="DEBUG",  # Mức độ log
        format="{level} : {time:YYYY/MM/DD HH:mm:ss.SSS} - {name} ------ {message} \n",  # Định dạng log
        retention="7 days",  # Giữ các tệp log cũ trong 7 ngày
        compression="zip"  # Nén các tệp log cũ
    )

    # Thêm log ra console
    logger.add(
        sys.stdout,
        level="DEBUG",
        format="{level} - {time:YYYY/MM/DD HH:mm:ss.SSS} - {name} -  {message}"
    )
