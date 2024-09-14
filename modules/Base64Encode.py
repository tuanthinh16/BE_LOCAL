import base64


def encode_base64(value):
    # Chuyển đổi giá trị thành bytes và mã hóa Base64
    return base64.b64encode(str(value).encode('utf-8')).decode('utf-8')

