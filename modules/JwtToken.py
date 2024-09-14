import jwt
import datetime
import config.app_config as conf
import config.uct7_config as utc7


SECRET_KEY = conf.load_config_from_xml('SECRET_KEY')
def create_jwt_token(payload):
    """
    Tạo JWT token.

    :param payload: Dữ liệu (dictionary) chứa thông tin cần mã hóa trong token.
    :return: JWT token dưới dạng chuỗi.
    """
    try:
        # Thêm thời gian hết hạn cho token (ví dụ: 1 giờ)
        payload['exp'] = utc7.TimeUTC7() + datetime.timedelta(hours=1)
        
        # Mã hóa payload và tạo token
        token = jwt.encode(payload,SECRET_KEY , algorithm='HS256')
        return token
    except Exception as e:
        print(f"Error creating token: {str(e)}")
        return None
def decode_jwt_token(token):
    """
    Xác thực và giải mã JWT token.

    :param token: JWT token dưới dạng chuỗi.
    :return: Dữ liệu đã giải mã (dictionary) hoặc thông báo lỗi.
    """
    try:
        # Giải mã token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}

#
