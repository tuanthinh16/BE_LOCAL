# models/Item_Type.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger
from database.db import db
from config.uct7_config import TimeUTC7
from loguru import logger as log
from modules.Convert import SystemTimeToTimeNumber

class LOCAL_ITEM_TYPE(db.Model):
    __tablename__ = 'LOCAL_ITEM_TYPE'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.BigInteger)
    creator = db.Column(db.String)
    modify_time = db.Column(db.BigInteger, nullable=True)
    modifier = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Integer, default=1)
    item_type_code = db.Column(db.String(50))
    item_type_name = db.Column(db.String(250))

    def __init__(self, _id=None, item_type_code=None, item_type_name=None, creator=None):
        self.id = _id
        self.item_type_code = item_type_code
        self.item_type_name = item_type_name
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
            'item_type_code': self.item_type_code,
            'item_type_name': self.item_type_name
        }
# models/Item_Type.py (tiếp tục)
class ItemType_Action:
    def __init__(self):
        self.log = log

    def initTable(self):
        # SQLAlchemy tự động tạo bảng nếu không tồn tại khi khởi động ứng dụng
        pass

    def create_item_type(self, item_type_code, item_type_name, creator):
        try:
            create_time = SystemTimeToTimeNumber(TimeUTC7())
            item_type = LOCAL_ITEM_TYPE(
                create_time=create_time,
                creator=creator,
                item_type_code=item_type_code,
                item_type_name=item_type_name
            )
            db.session.add(item_type)
            db.session.commit()
            return item_type.id
        except Exception as e:
            self.log.error(f"Error when creating item type. Error: {str(e)}")
            return {'error': str(e)}

    def get_all_item_types(self):
        try:
            item_types = LOCAL_ITEM_TYPE.query.all()
            return [item_type.to_dict() for item_type in item_types]
        except Exception as e:
            self.log.error(f"Error retrieving item types. Error: {str(e)}")
            return {'error': str(e)}

    def get_item_type_by_id(self, item_type_id):
        try:
            item_type = LOCAL_ITEM_TYPE.query.get(item_type_id)
            return item_type.to_dict() if item_type else {'error': 'Item type not found'}
        except Exception as e:
            self.log.error(f"Error retrieving item type by ID. Error: {str(e)}")
            return {'error': str(e)}

    def update_item_type(self, item_type_id, item_type_code=None, item_type_name=None, modifier=None):
        try:
            item_type = LOCAL_ITEM_TYPE.query.get(item_type_id)
            if item_type:
                if item_type_code:
                    item_type.item_type_code = item_type_code
                if item_type_name:
                    item_type.item_type_name = item_type_name
                if modifier:
                    item_type.modifier = modifier
                    item_type.modify_time = SystemTimeToTimeNumber(TimeUTC7())
                
                db.session.commit()
                return {'success': 'Item type updated successfully'}
            else:
                return {'error': 'Item type not found'}
        except Exception as e:
            self.log.error(f"Error updating item type. Error: {str(e)}")
            return {'error': str(e)}

    def delete_item_type(self, item_type_id):
        try:
            item_type = LOCAL_ITEM_TYPE.query.get(item_type_id)
            if item_type:
                db.session.delete(item_type)
                db.session.commit()
                return {'success': 'Item type deleted successfully'}
            else:
                return {'error': 'Item type not found'}
        except Exception as e:
            self.log.error(f"Error deleting item type. Error: {str(e)}")
            return {'error': str(e)}
