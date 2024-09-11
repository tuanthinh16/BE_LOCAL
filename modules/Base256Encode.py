import hashlib
from loguru import logger

def hash_sha256(value):
    # Chuyển đổi giá trị thành bytes
    value_bytes = str(value).encode('utf-8')
    # Tạo đối tượng hash SHA-256 và tính toán hash
    sha256_hash = hashlib.sha256(value_bytes).hexdigest()
    return sha256_hash