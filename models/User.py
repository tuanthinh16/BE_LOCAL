#models/user.py
from datetime import datetime

from flask import jsonify
from database.db import db
import sqlite3
from config.Db_config import Config
from config.uct7_config import TimeUTC7
from loguru import logger as log
from sqlalchemy.orm import relationship
import modules.Base256Encode as endcode256
from models.Wallet import Wallet_Action,LOCAL_WALLET
from modules.Convert import SystemTimeToTimeNumber


class LOCAL_USER(db.Model):
    __tablename__ = 'LOCAL_USERS'
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=TimeUTC7())
    creator = db.Column(db.String(50))
    modify_time = db.Column(db.DateTime, nullable=True)
    modifier = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Integer,default = 1)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    fullname = db.Column(db.String(100))
    login_name = db.Column(db.String(50))
    role_id = db.Column(db.Integer,nullable = True)
    user_identifer = db.Column(db.String(500))
    wallet_id = db.Column(db.Integer,nullable=True)

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
            'role_id': self.role_id,
            'user_identifer':self.user_identifer,
            'wallet_id':self.wallet_id
        }
    
    def __init__(self, username=None, create_time = None,email=None, phone=None, fullname=None, login_name=None, role_id=None, creator=None, modifier=None,user_identifer = None,wallet_id = None,is_active=1):
        self.username = username
        self.email = email
        self.phone = phone
        self.create_time = create_time
        self.fullname = fullname
        self.login_name = login_name
        self.role_id = role_id
        self.creator = creator
        self.modifier = modifier
        self.user_identifer = user_identifer
        self.wallet_id = wallet_id
        self.is_active = is_active



class UserAction:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.conn = sqlite3.connect(self.db_connection,check_same_thread=False)
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
            role_id TEXT,
            is_active INTEGERT DEFAULT 1,
            user_identifer TEXT,
            wallet_id INTEGER
        )
        '''
        cur.execute(sql)
        self.conn.commit()
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
                    user_identifer = row[12],
                    wallet_id=row[13]
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
                    user_identifer = row[12],
                    wallet_id=row[13]
                )
                return jsonify(user.to_dict())
        except Exception as e:
            self.log.error("Error when find user. Error:"+str(e))
            
        return None

    def create(self, username, email, phone, fullname, login_name, role_id, creator):
        try:
            cur = self.conn.cursor()
            
            # Check if email already exists
            check_sql = "SELECT COUNT(*) FROM LOCAL_USERS WHERE email = ? or username = ?"
            cur.execute(check_sql, (email,username,))
            email_exists = cur.fetchone()[0]
            
            if email_exists > 0:
                return {'error': 'Email or Username already exists'}
            
            # SQL query to insert user
            sql = """
            INSERT INTO LOCAL_USERS (create_time, creator, username, email, phone, fullname, login_name, role_id,is_active,user_identifer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?)
            """
            create_time = SystemTimeToTimeNumber(TimeUTC7())
            user_identifer_dict = f"username={username};email={email};role={role_id}"
            user_identifer = endcode256.hash_sha256(user_identifer_dict)
            
            # Parameters to execute
            params = (create_time, creator, username, email, phone, fullname, login_name, role_id,1,user_identifer)
            
            # Execute SQL query with parameters
            cur.execute(sql, params)
            
            # Get the last inserted user ID
            user_id = cur.lastrowid
            
            
            # Commit transactions
            self.conn.commit()
            
            # Close connections
            self.conn.close()
            
            return {'user_id': user_id}

        except Exception as e:
            self.log.error(f"Error when creating user. Error: {str(e)}")
            return {'error': str(e)}

    def update(self, user_id, username=None, email=None, phone=None, fullname=None, login_name=None, role_id=None, modifier=None):
        try:
            cur = self.conn.cursor()
            sql = """
            UPDATE LOCAL_USERS
            SET username = ?, email = ?, phone = ?, fullname = ?, login_name = ?, role_id = ?, modifier = ?, modify_time = ?
            WHERE id = ?
            """
            modify_time = TimeUTC7() if modifier else None
            cur.execute(sql, (username, email, phone, fullname, login_name, role_id, modifier, modify_time, user_id))
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
    def insert_sample_data(self):
        try:
            cur = self.conn.cursor()
            sql = """
            INSERT INTO LOCAL_USERS (create_time, creator, username, email, phone, fullname, login_name, role_id, is_active, user_identifer, wallet_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            create_time = SystemTimeToTimeNumber(TimeUTC7())
            creator = "admin"
            username = "john_doe"
            email = "john.doe@example.com"
            phone = "+1234567890"
            fullname = "John Doe"
            login_name = "johndoe"
            role_id = 1
            user_identifer = endcode256.hash_sha256(f"username={username};email={email};role_id={role_id}")
            cur.execute(sql, (create_time, creator, username, email, phone, fullname, login_name, role_id, 1, user_identifer, None))
            self.conn.commit()
            self.log.info("Sample user data inserted successfully.")
        except Exception as e:
            self.log.error(f"Error inserting sample user data. Error: {str(e)}")
        finally:
            self.conn.close()
            
