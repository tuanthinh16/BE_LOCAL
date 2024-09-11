#models/wallet.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Decimal, ForeignKey
from sqlalchemy.orm import relationship
from database.db import db
import sqlite3
from config.Db_config import Config
from config.uct7_config import TimeUTC7
from loguru import logger as log
import modules.Base256Encode as endcode256

class LOCAL_WALLET(db.Model):
    __tablename__ = 'LOCAL_WALLET'
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, default=TimeUTC7())
    creator = Column(String(50))
    modify_time = Column(DateTime, nullable=True)
    modifier = Column(String(50), nullable=True)
    username = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('LOCAL_USERS.id'), nullable=False)
    balance = Column(Decimal, default=0.0)
    transaction_id = Column(Integer)

    user = relationship('LOCAL_USER', back_populates='wallets')

    def __init__(self, username=None, user_id=None, balance=0.0, creator=None):
        self.username = username
        self.user_id = user_id
        self.balance = balance
        self.creator = creator
    
class Wallet_Action:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.conn = sqlite3.connect(self.db_connection)
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
                balance DECIMAL
            )
            '''
            cur.execute(sql)
            self.conn.commit()
            self.log.info("LOCAL_WALLET table initialized successfully.")
        except Exception as e:
            self.log.error("Error initializing LOCAL_WALLET table: " + str(e))
        finally:
            self.conn.close()
