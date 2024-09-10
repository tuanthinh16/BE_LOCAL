# config.py

import os

class Config:
    # Cấu hình chung cho Flask và SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
