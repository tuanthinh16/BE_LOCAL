# app.py

from flask import Flask, jsonify, request
from config.Db_config import Config
from database.db import db
from models import User
from datetime import datetime
from routes.user_routes import user_bp

# Tạo ứng dụng Flask
app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(user_bp)

# Khởi tạo cơ sở dữ liệu
db.init_app(app)

# push context manually to app
with app.app_context():
    db.create_all()
    
app.secret_key = 'super secret string'
if __name__ == '__main__':
    app.run(debug=True)
