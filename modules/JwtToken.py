# token.py
from functools import wraps
from flask import jsonify, request
import jwt
import datetime

import pytz
import config.app_config as conf
import config.uct7_config as utc7
from loguru import logger as log

# Load the secret key from the configuration
SECRET_KEY = conf.load_config_from_xml('SECRET_KEY')
token = ''
# Function to create JWT token
def create_jwt_token(payload, expiration_hours=1):
    """
    Tạo JWT token với thời gian hết hạn.
    
    :param payload: Dữ liệu chứa thông tin cần mã hóa.
    :param expiration_hours: Thời gian sống của token tính theo giờ (mặc định 1 giờ).
    :return: JWT token dưới dạng chuỗi.
    """
    try:
        # Thêm thời gian hết hạn cho token
        payload['exp'] = utc7.TimeUTC7() + datetime.timedelta(hours=expiration_hours)
        # Mã hóa và tạo token
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token
    except Exception as e:
        log.error(f"Error creating token: {str(e)}")
        return None

# Function to decode JWT token
def decode_jwt_token(token):
    """
    Xác thực và giải mã JWT token.
    
    :param token: JWT token dưới dạng chuỗi.
    :return: Dữ liệu đã giải mã hoặc lỗi.
    """
    try:
        # Giải mã token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}

# Decorator to verify token
from functools import wraps
from flask import jsonify, request
import jwt
import datetime
from loguru import logger as log
from config.uct7_config import TimeUTC7

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        log.info(f"Authorization header: {auth_header}")
        
        if auth_header and auth_header.startswith('Bearer '):
            # Extract the token after 'Bearer '
            token = auth_header.split(' ')[1]
        else:
            return jsonify({'message': 'Token is missing or invalid!'}), 401
        
        # Decode the token
        try:
            data = decode_jwt_token(token)
            if 'error' in data:
                return jsonify({'message': data['error']}), 401

            # Check token expiration
            exp = data.get('exp')
            if exp:
                #log.debug(exp)
                current_time = TimeUTC7()  # Get the current UTC7 time
                token_expiration_time = datetime.datetime.utcfromtimestamp(exp).replace(tzinfo=pytz.UTC)

                # Compare the expiration time with the current time
                if token_expiration_time < current_time:
                    log.warning("Token has expired")
                    return jsonify({'message': 'Token has expired, please log in again to get a new token.'}), 401
                
                # Optionally: Warn if the token is about to expire soon (e.g., less than 5 minutes remaining)
                time_remaining = token_expiration_time - current_time
                if time_remaining.total_seconds() < 300:
                    log.warning(f"Token is about to expire in {time_remaining.total_seconds()} seconds.")

        except jwt.ExpiredSignatureError:
            log.error("Token has expired")
            return jsonify({'message': 'Token has expired, please log in again to get a new token.'}), 401
        except jwt.InvalidTokenError:
            log.error("Invalid token")
            return jsonify({'message': 'Token is invalid!'}), 401
        except Exception as e:
            log.error(f"Error decoding token: {str(e)}")
            return jsonify({'message': 'Token is invalid!'}), 401
        
        # Proceed with the request if token is valid
        return f(*args, **kwargs)
    token = decorated
    return decorated

def get_token():
    """
    Lấy token từ tiêu đề Authorization của request.
    
    :return: Token hoặc lỗi nếu không có token.
    """
    auth_header = request.headers.get('Authorization')
    
    if auth_header and auth_header.startswith('Bearer '):
        # Extract the token after 'Bearer '
        token = auth_header.split(' ')[1]
        return token
    else:
        log.warning("Token is missing or invalid in Authorization header.")
        return jsonify({'message': 'Token is missing or invalid!'}), 401