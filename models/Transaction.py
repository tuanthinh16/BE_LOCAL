

#models/Transaction.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database.db import db
import sqlite3
from config.Db_config import Config
from config.uct7_config import TimeUTC7
from loguru import logger as log
import modules.Base256Encode as endcode256
import modules.Base256Encode as hash
from modules.Convert import SystemTimeToTimeNumber
from models.User import UserAction


class LOCAL_TRANSACTION(db.Model):
    __tablename__ = 'LOCAL_TRANSACTION'
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(String(50), default=SystemTimeToTimeNumber(TimeUTC7()))
    creator = Column(String(50))
    modify_time = Column(String(20), nullable=True)
    modifier = Column(String(50), nullable=True)
    execute_time = Column(String(20),nullable=False)
    request_user_id = Column(Integer,nullable=False)
    amount = Column(DECIMAL,default=0)
    fee = Column(DECIMAL,default=0.0000)
    recive_user_id = Column(Integer,nullable=False)
    pre_hash = Column(String(500),nullable=False)
    current_hash = Column(String(500),nullable=False)
    is_pause = Column(Integer,nullable=True)
    bill_id = Column(Integer)

class Transaction_Action:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.conn = sqlite3.connect(self.db_connection)
        self.log = log

    def InitTable(self):
        """
        Initialize the LOCAL_TRANSACTION table if it doesn't exist.
        """
        try:
            cur = self.conn.cursor()
            sql = '''
            CREATE TABLE IF NOT EXISTS LOCAL_TRANSACTION (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                create_time TEXT,
                creator TEXT,
                modify_time TEXT,
                modifier TEXT,
                execute_time TEXT NOT NULL,
                request_user_id INTEGER NOT NULL,
                amount DECIMAL DEFAULT 0,
                fee DECIMAL DEFAULT 0.0000,
                recive_user_id INTEGER NOT NULL,
                pre_hash TEXT NOT NULL,
                current_hash TEXT NOT NULL,
                is_pause INTEGER,
                bill_id INTEGER
            )
            '''
            cur.execute(sql)
            self.conn.commit()
            self.log.info("LOCAL_TRANSACTION table initialized successfully.")
        except Exception as e:
            self.log.error("Error initializing LOCAL_TRANSACTION table: " + str(e))

    def create_transaction(self, creator, execute_time, request_user_id, amount, fee, recive_user_id, pre_hash, current_hash, is_pause=None, bill_id=None):
        """
        Create a new transaction record in the LOCAL_TRANSACTION table.
        
        :param creator: Creator of the transaction
        :param execute_time: Time of the transaction execution
        :param request_user_id: ID of the user requesting the transaction
        :param amount: Amount of the transaction
        :param fee: Fee of the transaction
        :param recive_user_id: ID of the user receiving the transaction
        :param pre_hash: Previous hash
        :param current_hash: Current hash
        :param is_pause: Optional status of the transaction (paused or not)
        :param bill_id: Optional bill ID
        :return: The ID of the created transaction
        """
        try:
            cur = self.conn.cursor()
            create_time = SystemTimeToTimeNumber(datetime.datetime.now())
            sql = '''
            INSERT INTO LOCAL_TRANSACTION (create_time, creator, execute_time, request_user_id, amount, fee, recive_user_id, pre_hash, current_hash, is_pause, bill_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            cur.execute(sql, (create_time, creator, execute_time, request_user_id, amount, fee, recive_user_id, pre_hash, current_hash, is_pause, bill_id))
            self.conn.commit()
            transaction_id = cur.lastrowid
            self.log.info(f"Transaction created successfully with ID {transaction_id}.")
            return transaction_id
        except Exception as e:
            self.log.error("Error creating transaction: " + str(e))
            return None
        finally:
            self.conn.close()

    def update_transaction(self, transaction_id, modifier, execute_time=None, amount=None, fee=None, recive_user_id=None, pre_hash=None, current_hash=None, is_pause=None, bill_id=None):
        """
        Update an existing transaction record in the LOCAL_TRANSACTION table.
        
        :param transaction_id: ID of the transaction to update
        :param modifier: Modifier of the transaction
        :param execute_time: New execution time (optional)
        :param amount: New amount (optional)
        :param fee: New fee (optional)
        :param recive_user_id: New receiving user ID (optional)
        :param pre_hash: New previous hash (optional)
        :param current_hash: New current hash (optional)
        :param is_pause: New pause status (optional)
        :param bill_id: New bill ID (optional)
        :return: True if the update was successful, False otherwise
        """
        try:
            cur = self.conn.cursor()
            modify_time = SystemTimeToTimeNumber(datetime.datetime.now())
            sql = '''
            UPDATE LOCAL_TRANSACTION
            SET modify_time = ?, modifier = ?,
                execute_time = COALESCE(?, execute_time),
                amount = COALESCE(?, amount),
                fee = COALESCE(?, fee),
                recive_user_id = COALESCE(?, recive_user_id),
                pre_hash = COALESCE(?, pre_hash),
                current_hash = COALESCE(?, current_hash),
                is_pause = COALESCE(?, is_pause),
                bill_id = COALESCE(?, bill_id)
            WHERE id = ?
            '''
            cur.execute(sql, (modify_time, modifier, execute_time, amount, fee, recive_user_id, pre_hash, current_hash, is_pause, bill_id, transaction_id))
            self.conn.commit()
            if cur.rowcount > 0:
                self.log.info(f"Transaction with ID {transaction_id} updated successfully.")
                return True
            else:
                self.log.warning(f"Transaction with ID {transaction_id} not found.")
                return False
        except Exception as e:
            self.log.error("Error updating transaction: " + str(e))
            return False
        finally:
            self.conn.close()

    def get_transaction(self, transaction_id):
        """
        Retrieve a transaction record from the LOCAL_TRANSACTION table.
        
        :param transaction_id: ID of the transaction to retrieve
        :return: A dictionary with transaction details or None if not found
        """
        try:
            cur = self.conn.cursor()
            sql = '''
            SELECT * FROM LOCAL_TRANSACTION
            WHERE id = ?
            '''
            cur.execute(sql, (transaction_id,))
            row = cur.fetchone()
            if row:
                transaction = {
                    'id': row[0],
                    'create_time': row[1],
                    'creator': row[2],
                    'modify_time': row[3],
                    'modifier': row[4],
                    'execute_time': row[5],
                    'request_user_id': row[6],
                    'amount': row[7],
                    'fee': row[8],
                    'recive_user_id': row[9],
                    'pre_hash': row[10],
                    'current_hash': row[11],
                    'is_pause': row[12],
                    'bill_id': row[13]
                }
                self.log.info(f"Transaction with ID {transaction_id} retrieved successfully.")
                return transaction
            else:
                self.log.warning(f"Transaction with ID {transaction_id} not found.")
                return None
        except Exception as e:
            self.log.error("Error retrieving transaction: " + str(e))
            return None
        finally:
            self.conn.close()

    def delete_transaction(self, transaction_id):
        """
        Delete a transaction record from the LOCAL_TRANSACTION table.
        
        :param transaction_id: ID of the transaction to delete
        :return: Message indicating the result of the deletion attempt
        """
        try:
            cur = self.conn.cursor()
            
            # Retrieve the transaction details first
            sql_select = '''
            SELECT is_pause, bill_id FROM LOCAL_TRANSACTION
            WHERE id = ?
            '''
            cur.execute(sql_select, (transaction_id,))
            row = cur.fetchone()
            
            if row:
                is_pause, bill_id = row
                
                # Check if is_pause is 1 and bill_id is not null
                if is_pause == 1 and bill_id is not None:
                    self.log.warning(f"Transaction with ID {transaction_id} cannot be deleted because it is completed.")
                    return "Giao dịch đã hoàn tất"
                
                # Proceed with deletion
                sql_delete = '''
                DELETE FROM LOCAL_TRANSACTION
                WHERE id = ?
                '''
                cur.execute(sql_delete, (transaction_id,))
                self.conn.commit()
                
                if cur.rowcount > 0:
                    self.log.info(f"Transaction with ID {transaction_id} deleted successfully.")
                    return "Transaction deleted successfully"
                else:
                    self.log.warning(f"Transaction with ID {transaction_id} not found.")
                    return "Transaction not found"
            else:
                self.log.warning(f"Transaction with ID {transaction_id} not found.")
                return "Transaction not found"
        except Exception as e:
            self.log.error("Error deleting transaction: " + str(e))
            return "Error occurred while deleting transaction"
        finally:
            self.conn.close()


    def insert_sample_data(self):
        try:
            cur = self.conn.cursor()
            sql = """
            INSERT INTO LOCAL_TRANSACTION (create_time, creator, modify_time, modifier, execute_time, request_user_id, amount, fee, recive_user_id, pre_hash, current_hash, is_pause, bill_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            create_time = SystemTimeToTimeNumber(TimeUTC7())
            execute_time = create_time
            amount = 100.0
            fee = 0.0001
            request_user_id = 1  # Assuming user with ID 1 exists
            user_action = UserAction(self.db_connection)
            #user = user_action.get_by_id(request_user_id)
            recive_user_id = 2  # Assuming user with ID 1 exists
            pre_hash = hash.hash_sha256("CREATE LOCAL TEST DATA")
            current_hash = hash.hash_sha256(f"username=john_doe;amount={amount};fee={fee};revice_userid={recive_user_id}")
            cur.execute(sql, (create_time, "admin", None, None, execute_time, request_user_id, amount, fee, recive_user_id, pre_hash, current_hash, 0, None))
            self.conn.commit()
            self.log.info("Sample transaction data inserted successfully.")
        except Exception as e:
            self.log.error(f"Error inserting sample transaction data. Error: {str(e)}")
        finally:
            self.conn.close()