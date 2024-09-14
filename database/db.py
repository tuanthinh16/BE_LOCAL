# database/db.py

from flask_sqlalchemy import SQLAlchemy

# Tạo đối tượng SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
