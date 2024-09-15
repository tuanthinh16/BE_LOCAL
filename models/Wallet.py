# models/wallet.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database.db import db
from config.uct7_config import TimeUTC7
from loguru import logger as log
import modules.Base256Encode as endcode256
from modules.Convert import SystemTimeToTimeNumber
from modules.JwtToken import decode_jwt_token

class LOCAL_WALLET(db.Model):
    __tablename__ = 'LOCAL_WALLET'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.BigInteger)
    creator = db.Column(db.String)
    modify_time = db.Column(db.BigInteger, nullable=True)
    modifier = db.Column(db.String, nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('LOCAL_USERS.id'), nullable=False)
    balance = db.Column(db.DECIMAL, default=0.0)
    transaction_id = db.Column(db.Integer, nullable=True)

    def __init__(self, _id=None, username=None, create_time=None, user_id=None, balance=0.0, creator=None, transaction_id=None):
        self.id = _id
        self.username = username
        self.user_id = user_id
        self.balance = balance
        self.creator = creator
        self.transaction_id = transaction_id
        self.create_time = create_time

    def to_dict(self):
        return {
            'id': self.id,
            'create_time': self.create_time,
            'creator': self.creator,
            'modify_time': self.modify_time,
            'modifier': self.modifier,
            'username': self.username,
            'user_id': self.user_id,
            'balance': self.balance,
            'transaction_id': self.transaction_id
        }

class Wallet_Action:
    def __init__(self):
        self.log = log

    def initTable(self):
        # SQLAlchemy tự động tạo bảng nếu không tồn tại khi khởi động ứng dụng
        pass

    def create_wallet(self, username, user_id):
        try:
            create_time = SystemTimeToTimeNumber(TimeUTC7())
            creator = "admin"
            balance = 0.0
            wallet = LOCAL_WALLET(
                create_time=create_time,
                creator=creator,
                username=username,
                user_id=user_id,
                balance=balance
            )
            db.session.add(wallet)
            db.session.commit()
            return wallet.id
        except Exception as e:
            self.log.error(f"Error when creating wallet. Error: {str(e)}")
            return {'error': str(e)}

    def get_all_wallets(self):
        try:
            wallets = LOCAL_WALLET.query.all()
            return [wallet.to_dict() for wallet in wallets]
        except Exception as e:
            self.log.error(f"Error retrieving wallets. Error: {str(e)}")
            return {'error': str(e)}

    def get_wallet_by_id(self, wallet_id):
        try:
            wallet = LOCAL_WALLET.query.get(wallet_id)
            return wallet.to_dict() if wallet else {'error': 'Wallet not found'}
        except Exception as e:
            self.log.error(f"Error retrieving wallet by ID. Error: {str(e)}")
            return {'error': str(e)}
    def get_wallet_by_user_id(self, user_id):
        try:
            # Thực hiện truy vấn SQL để lấy ví theo user_id
            sql = '''
            SELECT * FROM LOCAL_WALLET
            WHERE user_id = :user_id
            '''
            result = db.session.execute(sql, {'user_id': user_id}).fetchone()
            
            if result:
                
                return result
            else:
                return {'error': 'Wallet not found'}
        except Exception as e:
            self.log.error(f"Error retrieving wallet by user ID. Error: {str(e)}")
            return {'error': str(e)}

    def update_wallet(self, wallet_id, username=None, balance=None, fee=None,modifier=None):
        try:
            wallet = LOCAL_WALLET.query.get(wallet_id)
            if wallet:
                if username:
                    wallet.username = username
                if balance is not None:
                    wallet.balance = balance
                if fee:
                    wallet.fee = fee
                wallet.modifier = modifier
                wallet.modify_time = SystemTimeToTimeNumber(TimeUTC7())
                
                db.session.commit()
                return {'success': 'Wallet updated successfully'}
            else:
                return {'error': 'Wallet not found'}
        except Exception as e:
            self.log.error(f"Error updating wallet. Error: {str(e)}")
            return {'error': str(e)}

    def delete_wallet(self, wallet_id):
        try:
            wallet = LOCAL_WALLET.query.get(wallet_id)
            if wallet:
                db.session.delete(wallet)
                db.session.commit()
                return {'success': 'Wallet deleted successfully'}
            else:
                return {'error': 'Wallet not found'}
        except Exception as e:
            self.log.error(f"Error deleting wallet. Error: {str(e)}")
            return {'error': str(e)}

