#models/user.py
from datetime import datetime
from database.db import db
import sqlite3
from config.Db_config import Config
from LOCAL.Library.AgeCaculator import calculate_age

class LOCAL_USER(db.Model):
    __tablename__ = 'LOCAL_USERS'
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
    is_active = db.Column(db.Short)

    
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



class UserAction:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.conn = sqlite3.connect(self.db_connection)
    def initTable(self):
        cur = self.conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS LOCAL_USERS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            create_time TEXT,
            creator TEXT,
            modify_time TEXT,
            modifier TEXT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            fullname TEXT,
            login_name TEXT,
            role TEXT
        )
        ''')
        self.conn.commit()
        self.conn.close()
    def show_all(self):
        
        cur = self.conn.cursor()
        sql = "SELECT * FROM LOCAL_USERS"
        cur.execute(sql)
        rows = cur.fetchall()
        self.conn.close()
        result = []
        for row in rows:
            user = LOCAL_USER(
                id=row[0],
                create_time=row[1],
                creator=row[2],
                modify_time=row[3],
                modifier=row[4],
                username=row[5],
                email=row[6],
                phone=row[7],
                fullname=row[8],
                login_name=row[9],
                role=row[10]
            )
            result.append(user.to_dict())
        return result

    def get_by_id(self, user_id):
        cur = self.conn.cursor()
        sql = "SELECT * FROM LOCAL_USERS WHERE id = ?"
        cur.execute(sql, (user_id,))
        row = cur.fetchone()
        self.conn.close()
        if row:
            user = LOCAL_USER(
                id=row[0],
                create_time=row[1],
                creator=row[2],
                modify_time=row[3],
                modifier=row[4],
                username=row[5],
                email=row[6],
                phone=row[7],
                fullname=row[8],
                login_name=row[9],
                role=row[10]
            )
            return user.to_dict()
        return None

    def create(self, username, email, phone, fullname, login_name, role, creator):
        cur = self.conn.cursor()
        sql = """
        INSERT INTO LOCAL_USERS (create_time, creator, username, email, phone, fullname, login_name, role)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        create_time = datetime.utcnow()
        cur.execute(sql, (create_time, creator, username, email, phone, fullname, login_name, role))
        self.conn.commit()
        user_id = cur.lastrowid
        self.conn.close()
        return user_id

    def update(self, user_id, username=None, email=None, phone=None, fullname=None, login_name=None, role=None, modifier=None):
        cur = self.conn.cursor()
        sql = """
        UPDATE LOCAL_USERS
        SET username = ?, email = ?, phone = ?, fullname = ?, login_name = ?, role = ?, modifier = ?, modify_time = ?
        WHERE id = ?
        """
        modify_time = datetime.utcnow() if modifier else None
        cur.execute(sql, (username, email, phone, fullname, login_name, role, modifier, modify_time, user_id))
        self.conn.commit()
        self.conn.close()

    def delete(self, user_id):
        cur = self.conn.cursor()
        sql = "DELETE FROM LOCAL_USERS WHERE id = ?"
        cur.execute(sql, (user_id,))
        self.conn.commit()
        self.conn.close()
