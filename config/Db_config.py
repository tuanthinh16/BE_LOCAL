# config/config_db.py

class Config:
    SECRET_KEY = 'ThinhVipPro'
    
    # Cấu hình kết nối PostgreSQL
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:thinh1637@localhost:1521/LOCAL_RS'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
