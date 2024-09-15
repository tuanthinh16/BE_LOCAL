# models/Item.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger
from database.db import db
from config.uct7_config import TimeUTC7
from loguru import logger as log
from modules.Convert import SystemTimeToTimeNumber

class LOCAL_ITEM(db.Model):
    __tablename__ = 'LOCAL_ITEM'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.BigInteger)
    creator = db.Column(db.String)
    modify_time = db.Column(db.BigInteger, nullable=True)
    modifier = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Integer, default=1)
    item_init = db.Column(db.String(50))
    item_type_id = db.Column(db.Integer)
    item_code = db.Column(db.String(100))
    item_name = db.Column(db.String(200))
    item_description = db.Column(db.String(500))
    item_identifier = db.Column(db.String(200))

    def __init__(self, _id=None, item_init=None, item_type_id=None, item_code=None, item_name=None, item_description=None, item_identifier=None, creator=None):
        self.id = _id
        self.item_init = item_init
        self.item_type_id = item_type_id
        self.item_code = item_code
        self.item_name = item_name
        self.item_description = item_description
        self.item_identifier = item_identifier
        self.creator = creator
        self.create_time = SystemTimeToTimeNumber(TimeUTC7())

    def to_dict(self):
        return {
            'id': self.id,
            'create_time': self.create_time,
            'creator': self.creator,
            'modify_time': self.modify_time,
            'modifier': self.modifier,
            'is_active': self.is_active,
            'item_init': self.item_init,
            'item_type_id': self.item_type_id,
            'item_code': self.item_code,
            'item_name': self.item_name,
            'item_description': self.item_description,
            'item_identifier': self.item_identifier
        }
class Item_Action:
    def __init__(self):
        self.log = log

    def initTable(self):
        # SQLAlchemy tự động tạo bảng nếu không tồn tại khi khởi động ứng dụng
        pass

    def create_item(self, item_init, item_type_id, item_code, item_name, item_description, item_identifier, creator):
        try:
            create_time = SystemTimeToTimeNumber(TimeUTC7())
            item = LOCAL_ITEM(
                create_time=create_time,
                creator=creator,
                item_init=item_init,
                item_type_id=item_type_id,
                item_code=item_code,
                item_name=item_name,
                item_description=item_description,
                item_identifier=item_identifier
            )
            db.session.add(item)
            db.session.commit()
            return item.id
        except Exception as e:
            self.log.error(f"Error when creating item. Error: {str(e)}")
            return {'error': str(e)}

    def get_all_items(self):
        try:
            items = LOCAL_ITEM.query.all()
            return [item.to_dict() for item in items]
        except Exception as e:
            self.log.error(f"Error retrieving items. Error: {str(e)}")
            return {'error': str(e)}

    def get_item_by_id(self, item_id):
        try:
            item = LOCAL_ITEM.query.get(item_id)
            return item.to_dict() if item else {'error': 'Item not found'}
        except Exception as e:
            self.log.error(f"Error retrieving item by ID. Error: {str(e)}")
            return {'error': str(e)}

    def update_item(self, item_id, item_init=None, item_type_id=None, item_code=None, item_name=None, item_description=None, item_identifier=None, modifier=None):
        try:
            item = LOCAL_ITEM.query.get(item_id)
            if item:
                if item_init:
                    item.item_init = item_init
                if item_type_id is not None:
                    item.item_type_id = item_type_id
                if item_code:
                    item.item_code = item_code
                if item_name:
                    item.item_name = item_name
                if item_description:
                    item.item_description = item_description
                if item_identifier:
                    item.item_identifier = item_identifier
                
                item.modifier = modifier
                item.modify_time = SystemTimeToTimeNumber(TimeUTC7())
                
                db.session.commit()
                return {'success': 'Item updated successfully'}
            else:
                return {'error': 'Item not found'}
        except Exception as e:
            self.log.error(f"Error updating item. Error: {str(e)}")
            return {'error': str(e)}

    def delete_item(self, item_id):
        try:
            item = LOCAL_ITEM.query.get(item_id)
            if item:
                db.session.delete(item)
                db.session.commit()
                return {'success': 'Item deleted successfully'}
            else:
                return {'error': 'Item not found'}
        except Exception as e:
            self.log.error(f"Error deleting item. Error: {str(e)}")
            return {'error': str(e)}