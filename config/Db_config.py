# config/config_db.py

class Config:
    SECRET_KEY = 'ThinhVipPro'
    
    # Cấu hình kết nối PostgreSQL
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:thinh1637@103.67.197.243:1521/LOCAL_RS'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
