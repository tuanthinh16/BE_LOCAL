#models/user.py
from datetime import datetime
from database.db import db
import sqlite3
from config.Db_config import Config
from config.uct7_config import TimeUTC7
from loguru import logger as log
from sqlalchemy.orm import relationship
import modules.Base256Encode as endcode256
import models.Wallet


class LOCAL_USER(db.Model):
    __tablename__ = 'LOCAL_USERS'
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=TimeUTC7())
    creator = db.Column(db.String(50))
    modify_time = db.Column(db.DateTime, nullable=True)
    modifier = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    fullname = db.Column(db.String(100))
    login_name = db.Column(db.String(50))
    role = db.Column(db.String(20))
    is_active = db.Column(db.Integer)
    user_identifer = db.Column(db.String(100))
    wallet_id = db.Column(db.Integer)

    wallets = relationship('LOCAL_WALLET', back_populates='user')

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
            'role': self.role,
            'user_identifer':self.user_identifer,
            'wallet_id':self.wallet_id
        }
    
    def __init__(self, username=None, email=None, phone=None, fullname=None, login_name=None, role=None, creator=None, modifier=None,user_identifer = None,wallet_id = None):
        self.username = username
        self.email = email
        self.phone = phone
        self.fullname = fullname
        self.login_name = login_name
        self.role = role
        self.creator = creator
        self.modifier = modifier
        self.user_identifer = user_identifer
        self.wallet_id = wallet_id
        # `create_time` and `modify_time` are handled automatically by default and on modification
    def is_active(self):
        return True 



class UserAction:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.conn = sqlite3.connect(self.db_connection)
        self.log  = log
    def initTable(self):
        cur = self.conn.cursor()
        sql = '''
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
            role TEXT,
            is_active INTEGERT,
            user_identifer TEXT
        )
        '''
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
    def show_all(self):
        result = []
        try:
            cur = self.conn.cursor()
            sql = "SELECT * FROM LOCAL_USERS"
            cur.execute(sql)
            rows = cur.fetchall()
            self.conn.close()
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
                    role=row[10],
                    user_identifer = row[12]
                )
                result.append(user.to_dict())
        except Exception as e:
            self.log.error("Error when get all user. Error: "+str(e))
            
        return result

    def get_by_id(self, user_id):
        try:
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
                    role=row[10],
                    user_identifer = row[12]
                )
                return user.to_dict()
        except Exception as e:
            self.log.error("Error when find user. Error:"+str(e))
            
        return None

    def create(self, username, email, phone, fullname, login_name, role, creator):
        try:
            cur = self.conn.cursor()
            sql = """
            INSERT INTO LOCAL_USERS (create_time, creator, username, email, phone, fullname, login_name, role,is_active,user_identifer,wallet_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?,?)
            """
            create_time = TimeUTC7()
            user_identifer = endcode256.hash_sha256({'username':username,'email':email,'role':role})
            cur.execute(sql, (create_time, creator, username, email, phone, fullname, login_name, role,1,user_identifer,None))
            wallet = models.Wallet.LOCAL_WALLET(username=username, user_id=user_id, balance=0.0, creator=creator)
            db.session.add(wallet)
            db.session.commit()
            self.conn.commit()
            user_id = cur.lastrowid
            self.conn.close()
        except Exception as e:
            self.log.error("Error when create user. Error: "+str(e))
            
        return user_id

    def update(self, user_id, username=None, email=None, phone=None, fullname=None, login_name=None, role=None, modifier=None):
        try:
            cur = self.conn.cursor()
            sql = """
            UPDATE LOCAL_USERS
            SET username = ?, email = ?, phone = ?, fullname = ?, login_name = ?, role = ?, modifier = ?, modify_time = ?
            WHERE id = ?
            """
            modify_time = TimeUTC7() if modifier else None
            cur.execute(sql, (username, email, phone, fullname, login_name, role, modifier, modify_time, user_id))
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            self.log.error("Error when update user. Error: "+str(e))
            

    def delete(self, user_id):
        try:
            cur = self.conn.cursor()
            sql = "DELETE FROM LOCAL_USERS WHERE id = ?"
            cur.execute(sql, (user_id,))
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            self.log.error("Error when delete user. Error: "+str(e))
            
