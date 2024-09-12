#models/wallet.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database.db import db
import sqlite3
from config.Db_config import Config
from config.uct7_config import TimeUTC7
from loguru import logger as log
import modules.Base256Encode as endcode256
from modules.Convert import SystemTimeToTimeNumber

class LOCAL_WALLET(db.Model):
    __tablename__ = 'LOCAL_WALLET'
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, default=TimeUTC7())
    creator = Column(String(50))
    modify_time = Column(DateTime, nullable=True)
    modifier = Column(String(50), nullable=True)
    username = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('LOCAL_USERS.id'), nullable=False)
    balance = Column(DECIMAL, default=0.0)
    transaction_id = Column(Integer,nullable=True)

    user = relationship('LOCAL_USER', back_populates='wallets')

    def __init__(self, username=None,create_time = None, user_id=None, balance=0.0, creator=None,transaction_id=None):
        self.username = username
        self.user_id = user_id
        self.balance = balance
        self.creator = creator
        self.transaction_id = transaction_id
        self.create_time = create_time

def set_journal_mode(conn):
    conn.execute('PRAGMA journal_mode=WAL;') 
class Wallet_Action:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.conn = sqlite3.connect(self.db_connection)
        set_journal_mode(self.conn)  # Set journal mode to WAL
        self.conn.isolation_level = None  # Use autocommit mode for simplicity
        self.log  = log
    def initTable(self):
        try:
            cur = self.conn.cursor()
            sql = '''
            CREATE TABLE IF NOT EXISTS LOCAL_WALLET (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                create_time TEXT,
                creator TEXT,
                modify_time TEXT,
                modifier TEXT,
                username TEXT UNIQUE NOT NULL,
                user_id INTEGER,
                balance DECIMAL,
                transaction_id INTEGER
            )
            '''
            cur.execute(sql)
            self.conn.commit()
            self.log.info("LOCAL_WALLET table initialized successfully.")
        except Exception as e:
            self.log.error("Error initializing LOCAL_WALLET table: " + str(e))



    def create_wallet(self, username,user_id):
        try:
            cur = self.conn.cursor()
            sql = """
            INSERT INTO LOCAL_WALLET (create_time, creator, username, user_id, balance)
            VALUES (?, ?, ?, ?, ?)
            """
            # Execute SQL query with the correct number of parameters
            create_time = SystemTimeToTimeNumber(TimeUTC7())
            creator = "admin"
            balance = 0.0
            cur.execute(sql, (create_time, creator, username, user_id, balance))
            
            wallet_id = cur.lastrowid
            
            # Commit the transaction
            self.conn.commit()
            self.conn.close()
            
            return wallet_id
        
        except Exception as e:
            log.error(f"Error when creating wallet. Error: {str(e)}")
            return {'error': str(e)}
        
    def insert_sample_data(self):
        try:
            cur = self.conn.cursor()
            sql = """
            INSERT INTO LOCAL_WALLET (create_time, creator, username, user_id, balance)
            VALUES (?, ?, ?, ?, ?)
            """
            create_time = SystemTimeToTimeNumber(TimeUTC7())
            creator = "admin"
            username = "john_doe"
            user_id = 1  # Assuming user with ID 1 exists
            balance = 1000.0
            cur.execute(sql, (create_time, creator, username, user_id, balance))
            self.conn.commit()
            self.log.info("Sample wallet data inserted successfully.")
        except Exception as e:
            self.log.error(f"Error inserting sample wallet data. Error: {str(e)}")
        finally:
            self.conn.close()
