# models/Transaction.py
from sqlalchemy import Column, Integer, String, BigInteger, DECIMAL
from sqlalchemy.orm import relationship
from database.db import db
from config.uct7_config import TimeUTC7
from loguru import logger as log
import modules.Base256Encode as hash
from modules.Convert import SystemTimeToTimeNumber

class LOCAL_TRANSACTION(db.Model):
    __tablename__ = 'LOCAL_TRANSACTION'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.BigInteger)  
    creator = db.Column(db.String)
    modify_time = db.Column(db.BigInteger, nullable=True)
    modifier = db.Column(db.String, nullable=True)
    modify_message = db.Column(String(500),nullable=True)
    is_active = db.Column(Integer,nullable = True)
    execute_time = db.Column(db.BigInteger, nullable=False)
    request_user_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.DECIMAL, default=0)
    fee = db.Column(db.String(50), default='0.0000')
    recive_user_id = db.Column(db.Integer, nullable=False)
    pre_hash = db.Column(db.String(500), nullable=False)
    current_hash = db.Column(db.String(500), nullable=False)
    is_pause = db.Column(db.Integer, nullable=True)
    bill_id = db.Column(db.Integer)

class Transaction_Action:
    def __init__(self):
        self.log = log

    def initTable(self):
        try:
            db.create_all()
            self.log.info("LOCAL_TRANSACTION table initialized successfully.")
        except Exception as e:
            self.log.error("Error initializing LOCAL_TRANSACTION table: " + str(e))

    def create_transaction(self, creator, request_user_id, amount, fee, recive_user_id):
        try:
            create_time = SystemTimeToTimeNumber(TimeUTC7())
            last_record = LOCAL_TRANSACTION.query.order_by(LOCAL_TRANSACTION.create_time.desc()).first()
            if last_record:
                pre_hash = last_record.current_hash
            else:
                pre_hash = hash.hash_sha256("request_user_id=0;amount=100;fee=0.002;recvie_user_id=0")
            
            current_hash = hash.hash_sha256(f"request_user_id={recive_user_id};amount={amount};fee={fee};recvie_user_id={recive_user_id}")  
            transaction = LOCAL_TRANSACTION(
                create_time=create_time,
                creator=creator,
                request_user_id=request_user_id,
                amount=amount,
                fee=fee,
                recive_user_id=recive_user_id,
                pre_hash=pre_hash,
                current_hash=current_hash
            )
            db.session.add(transaction)
            db.session.commit()
            self.log.info(f"Transaction created successfully with ID {transaction.id}.")
            return transaction.id
        except Exception as e:
            self.log.error("Error creating transaction: " + str(e))
            return None

    def update_transaction(self, transaction_id, bill_id=None, is_pause=None):
        try:
            transaction = LOCAL_TRANSACTION.query.get(transaction_id)
            if not transaction:
                self.log.warning(f"Transaction with ID {transaction_id} not found.")
                return False
            
            transaction.modify_time = SystemTimeToTimeNumber(TimeUTC7())
            transaction.modifier = "admin_be"
            if bill_id is not None:
                transaction.bill_id = bill_id
            if is_pause is not None:
                transaction.is_pause = is_pause
            
            db.session.commit()
            self.log.info(f"Transaction with ID {transaction_id} updated successfully.")
            return True
        except Exception as e:
            self.log.error("Error updating transaction: " + str(e))
            return False

    def get_transaction(self, transaction_id):
        try:
            transaction = LOCAL_TRANSACTION.query.get(transaction_id)
            if transaction:
                transaction_dict = {
                    'id': transaction.id,
                    'create_time': transaction.create_time,
                    'creator': transaction.creator,
                    'modify_time': transaction.modify_time,
                    'modifier': transaction.modifier,
                    'execute_time': transaction.execute_time,
                    'request_user_id': transaction.request_user_id,
                    'amount': transaction.amount,
                    'fee': transaction.fee,
                    'recive_user_id': transaction.recive_user_id,
                    'pre_hash': transaction.pre_hash,
                    'current_hash': transaction.current_hash,
                    'is_pause': transaction.is_pause,
                    'bill_id': transaction.bill_id
                }
                self.log.info(f"Transaction with ID {transaction_id} retrieved successfully.")
                return transaction_dict
            else:
                self.log.warning(f"Transaction with ID {transaction_id} not found.")
                return None
        except Exception as e:
            self.log.error("Error retrieving transaction: " + str(e))
            return None

    def delete_transaction(self, transaction_id):
        try:
            transaction = LOCAL_TRANSACTION.query.get(transaction_id)
            if not transaction:
                self.log.warning(f"Transaction with ID {transaction_id} not found.")
                return "Transaction not found"
            
            if transaction.is_pause == 1 and transaction.bill_id is not None:
                self.log.warning(f"Transaction with ID {transaction_id} cannot be deleted because it is completed.")
                return "Giao dịch đã hoàn tất"

            db.session.delete(transaction)
            db.session.commit()
            self.log.info(f"Transaction with ID {transaction_id} deleted successfully.")
            return "Transaction deleted successfully"
        except Exception as e:
            self.log.error("Error deleting transaction: " + str(e))
            return "Error occurred while deleting transaction"

