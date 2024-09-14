# models/Role.py
from sqlalchemy import Column, Integer, String, BigInteger
from database.db import db
from config.uct7_config import TimeUTC7
from loguru import logger as log
from modules.Convert import SystemTimeToTimeNumber

class LOCAL_ROLE(db.Model):
    __tablename__ = 'LOCAL_ROLE'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.BigInteger)  
    creator = db.Column(db.String)
    modify_time = db.Column(db.BigInteger, nullable=True)
    modifier = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Integer, default=1)
    role_code = db.Column(db.String, unique=True, nullable=False)
    role_name = db.Column(db.String)
    role_group_code = db.Column(db.String)

class Role_Action:
    def __init__(self):
        self.log = log

    def initTable(self):
        try:
            db.create_all()
            self.log.info("LOCAL_ROLE table initialized successfully.")
        except Exception as e:
            self.log.error("Error initializing LOCAL_ROLE table: " + str(e))

    def create_role(self, creator, role_code, role_name, role_group_code=None):
        try:
            # Check if role_code already exists
            role_exists = LOCAL_ROLE.query.filter_by(role_code=role_code).first()
            if role_exists:
                return {'error': 'Role code already exists'}
            
            create_time = SystemTimeToTimeNumber(TimeUTC7())
            role = LOCAL_ROLE(
                create_time=create_time,
                creator=creator,
                role_code=role_code,
                role_name=role_name,
                role_group_code=role_group_code
            )
            db.session.add(role)
            db.session.commit()
            self.log.info(f"Role created successfully with ID {role.id}.")
            return role.id
        except Exception as e:
            self.log.error("Error creating role: " + str(e))
            return None

    def update_role(self, role_id, modifier, role_code=None, role_name=None, role_group_code=None, is_active=None):
        try:
            role = LOCAL_ROLE.query.get(role_id)
            if not role:
                self.log.warning(f"Role with ID {role_id} not found.")
                return False
            
            role.modify_time = SystemTimeToTimeNumber(TimeUTC7())
            role.modifier = modifier
            if role_code is not None:
                role.role_code = role_code
            if role_name is not None:
                role.role_name = role_name
            if role_group_code is not None:
                role.role_group_code = role_group_code
            if is_active is not None:
                role.is_active = is_active
            
            db.session.commit()
            self.log.info(f"Role with ID {role_id} updated successfully.")
            return True
        except Exception as e:
            self.log.error("Error updating role: " + str(e))
            return False

    def get_role(self, role_id):
        try:
            role = LOCAL_ROLE.query.get
            role = LOCAL_ROLE.query.get(role_id)
            if role:
                role_dict = {
                    'id': role.id,
                    'create_time': role.create_time,
                    'creator': role.creator,
                    'modify_time': role.modify_time,
                    'modifier': role.modifier,
                    'is_active': role.is_active,
                    'role_code': role.role_code,
                    'role_name': role.role_name,
                    'role_group_code': role.role_group_code
                }
                self.log.info(f"Role with ID {role_id} retrieved successfully.")
                return role_dict
            else:
                self.log.warning(f"Role with ID {role_id} not found.")
                return None
        except Exception as e:
            self.log.error("Error retrieving role: " + str(e))
            return None

    def delete_role(self, role_id):
        try:
            role = LOCAL_ROLE.query.get(role_id)
            if not role:
                self.log.warning(f"Role with ID {role_id} not found.")
                return False
            
            db.session.delete(role)
            db.session.commit()
            self.log.info(f"Role with ID {role_id} deleted successfully.")
            return True
        except Exception as e:
            self.log.error("Error deleting role: " + str(e))
            return False

    def insert_sample_data(self):
        try:
            create_time = SystemTimeToTimeNumber(TimeUTC7())
            role = LOCAL_ROLE(
                create_time=create_time,
                creator="admin",
                role_code="AD",
                role_name="Administrator",
                role_group_code=""
            )
            db.session.add(role)
            db.session.commit()
            self.log.info("Sample role data inserted successfully.")
        except Exception as e:
            self.log.error(f"Error inserting sample role data. Error: {str(e)}")
