
#models/Role.py
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

class LOCAL_ROLE(db.Model):
    __tablename__ = 'LOCAL_ROLE'
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, default=SystemTimeToTimeNumber(TimeUTC7()))
    creator = Column(String(50))
    modify_time = Column(DateTime, nullable=True)
    modifier = Column(String(50), nullable=True)
    is_active = Column(Integer,default=1)
    role_code = Column(String(50))
    role_name = Column(String(50))
    role_group_code = Column(String(50),nullable = True)

class Role_Action:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.conn = sqlite3.connect(self.db_connection)
        self.log = log

    def initTable(self):
        """
        Initialize the LOCAL_ROLE table if it doesn't exist.
        """
        try:
            cur = self.conn.cursor()
            sql = '''
            CREATE TABLE IF NOT EXISTS LOCAL_ROLE (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                create_time INTEGER,
                creator TEXT,
                modify_time INTEGER,
                modifier TEXT,
                is_active INTEGER DEFAULT 1,
                role_code TEXT UNIQUE NOT NULL,
                role_name TEXT,
                role_group_code TEXT
            )
            '''
            cur.execute(sql)
            self.conn.commit()
            self.log.info("LOCAL_ROLE table initialized successfully.")
        except Exception as e:
            self.log.error("Error initializing LOCAL_ROLE table: " + str(e))

    def create_role(self, creator, role_code, role_name, role_group_code=None):
        """
        Create a new role record in the LOCAL_ROLE table.
        
        :param creator: Creator of the role
        :param role_code: Code of the role
        :param role_name: Name of the role
        :param role_group_code: Optional group code of the role
        :return: The ID of the created role
        """
        try:
            cur = self.conn.cursor()
            # Check if email already exists
            check_sql = "SELECT COUNT(*) FROM LOCAL_ROLE WHERE role_code = "
            cur.execute(check_sql, (role_code,))
            email_exists = cur.fetchone()[0]
            
            if email_exists > 0:
                return {'error': 'Email or Username already exists'}
            create_time = SystemTimeToTimeNumber(datetime.datetime.now())
            sql = '''
            INSERT INTO LOCAL_ROLE (create_time, creator, role_code, role_name, role_group_code)
            VALUES (?, ?, ?, ?, ?)
            '''
            cur.execute(sql, (create_time, creator, role_code, role_name, role_group_code))
            self.conn.commit()
            role_id = cur.lastrowid
            self.log.info(f"Role created successfully with ID {role_id}.")
            return role_id
        except Exception as e:
            self.log.error("Error creating role: " + str(e))
            return None
        finally:
            self.conn.close()

    def update_role(self, role_id, modifier, role_code=None, role_name=None, role_group_code=None, is_active=None):
        """
        Update an existing role record in the LOCAL_ROLE table.
        
        :param role_id: ID of the role to update
        :param modifier: Modifier of the role
        :param role_code: New role code (optional)
        :param role_name: New role name (optional)
        :param role_group_code: New role group code (optional)
        :param is_active: New status of the role (optional)
        :return: True if the update was successful, False otherwise
        """
        try:
            cur = self.conn.cursor()
            modify_time = SystemTimeToTimeNumber(datetime.datetime.now())
            sql = '''
            UPDATE LOCAL_ROLE
            SET modify_time = ?, modifier = ?,
                role_code = COALESCE(?, role_code),
                role_name = COALESCE(?, role_name),
                role_group_code = COALESCE(?, role_group_code),
                is_active = COALESCE(?, is_active)
            WHERE id = ?
            '''
            cur.execute(sql, (modify_time, modifier, role_code, role_name, role_group_code, is_active, role_id))
            self.conn.commit()
            if cur.rowcount > 0:
                self.log.info(f"Role with ID {role_id} updated successfully.")
                return True
            else:
                self.log.warning(f"Role with ID {role_id} not found.")
                return False
        except Exception as e:
            self.log.error("Error updating role: " + str(e))
            return False
        finally:
            self.conn.close()

    def get_role(self, role_id):
        """
        Retrieve a role record from the LOCAL_ROLE table.
        
        :param role_id: ID of the role to retrieve
        :return: A dictionary with role details or None if not found
        """
        try:
            cur = self.conn.cursor()
            sql = '''
            SELECT * FROM LOCAL_ROLE
            WHERE id = ?
            '''
            cur.execute(sql, (role_id,))
            row = cur.fetchone()
            if row:
                role = {
                    'id': row[0],
                    'create_time': row[1],
                    'creator': row[2],
                    'modify_time': row[3],
                    'modifier': row[4],
                    'is_active': row[5],
                    'role_code': row[6],
                    'role_name': row[7],
                    'role_group_code': row[8]
                }
                self.log.info(f"Role with ID {role_id} retrieved successfully.")
                return role
            else:
                self.log.warning(f"Role with ID {role_id} not found.")
                return None
        except Exception as e:
            self.log.error("Error retrieving role: " + str(e))
            return None
        finally:
            self.conn.close()

    def delete_role(self, role_id):
        """
        Delete a role record from the LOCAL_ROLE table.
        
        :param role_id: ID of the role to delete
        :return: True if the deletion was successful, False otherwise
        """
        try:
            cur = self.conn.cursor()
            sql = '''
            DELETE FROM LOCAL_ROLE
            WHERE id = ?
            '''
            cur.execute(sql, (role_id,))
            self.conn.commit()
            if cur.rowcount > 0:
                self.log.info(f"Role with ID {role_id} deleted successfully.")
                return True
            else:
                self.log.warning(f"Role with ID {role_id} not found.")
                return False
        except Exception as e:
            self.log.error("Error deleting role: " + str(e))
            return False
        finally:
            self.conn.close()
    def insert_sample_data(self):
        try:
            cur = self.conn.cursor()
            sql = """
            INSERT INTO LOCAL_ROLE (create_time, creator, modify_time, modifier, is_active, role_code, role_name, role_group_code)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            create_time = SystemTimeToTimeNumber(TimeUTC7())
            creator = "admin"
            role_code = "AD"
            role_name = "Administrator"
            role_group_code = ""
            cur.execute(sql, (create_time, creator, None, None, 1, role_code, role_name, role_group_code))
            self.conn.commit()
            self.log.info("Sample role data inserted successfully.")
        except Exception as e:
            self.log.error(f"Error inserting sample role data. Error: {str(e)}")
        finally:
            self.conn.close()