from datetime import datetime
from database.db import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    creator = db.Column(db.String(50))
    modify_time = db.Column(db.DateTime, nullable=True)
    modifier = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    fullname = db.Column(db.String(100))
    login_name = db.Column(db.String(50))
    role = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'create_time': self.create_time,
            'creator': self.creator,
            'modify_time': self.modify_time,
            'modifier': self.modifier,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'fullname': self.fullname,
            'login_name': self.login_name,
            'role': self.role
        }
    
    def __init__(self, username=None, email=None, phone=None, fullname=None, login_name=None, role=None, creator=None, modifier=None):
        self.username = username
        self.email = email
        self.phone = phone
        self.fullname = fullname
        self.login_name = login_name
        self.role = role
        self.creator = creator
        self.modifier = modifier
        # `create_time` and `modify_time` are handled automatically by default and on modification
    def is_active(self):
        return True 
