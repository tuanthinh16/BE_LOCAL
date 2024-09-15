# models/User_Bag.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger
from database.db import db
from config.uct7_config import TimeUTC7
from loguru import logger as log
from modules.Convert import SystemTimeToTimeNumber

class LOCAL_USER_BAG(db.Model):
    __tablename__ = 'LOCAL_USER_BAG'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.BigInteger)
    creator = db.Column(db.String)
    modify_time = db.Column(db.BigInteger, nullable=True)
    modifier = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer)
    item_amount = db.Column(db.String(50), default=0)

    def __init__(self, _id=None, user_id=None, item_id=None, item_amount=None, creator=None):
        self.id = _id
        self.user_id = user_id
        self.item_id = item_id
        self.item_amount = item_amount
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
            'user_id': self.user_id,
            'item_id': self.item_id,
            'item_amount': self.item_amount
        }
# models/User_Bag.py (tiếp tục)
class UserBag_Action:
    def __init__(self):
        self.log = log

    def initTable(self):
        # SQLAlchemy tự động tạo bảng nếu không tồn tại khi khởi động ứng dụng
        pass

    def create_user_bag(self, user_id, item_id, item_amount, creator):
        try:
            create_time = SystemTimeToTimeNumber(TimeUTC7())
            user_bag = LOCAL_USER_BAG(
                create_time=create_time,
                creator=creator,
                user_id=user_id,
                item_id=item_id,
                item_amount=item_amount
            )
            db.session.add(user_bag)
            db.session.commit()
            return user_bag.id
        except Exception as e:
            self.log.error(f"Error when creating user bag. Error: {str(e)}")
            return {'error': str(e)}

    def get_all_user_bags(self):
        try:
            user_bags = LOCAL_USER_BAG.query.all()
            return [user_bag.to_dict() for user_bag in user_bags]
        except Exception as e:
            self.log.error(f"Error retrieving user bags. Error: {str(e)}")
            return {'error': str(e)}

    def get_user_bag_by_id(self, user_bag_id):
        try:
            user_bag = LOCAL_USER_BAG.query.get(user_bag_id)
            return user_bag.to_dict() if user_bag else {'error': 'User bag not found'}
        except Exception as e:
            self.log.error(f"Error retrieving user bag by ID. Error: {str(e)}")
            return {'error': str(e)}

    def get_user_bag_by_user_id(self, user_id):
        try:
            user_bags = LOCAL_USER_BAG.query.filter_by(user_id=user_id).all()
            return [user_bag.to_dict() for user_bag in user_bags] if user_bags else {'error': 'User bags not found'}
        except Exception as e:
            self.log.error(f"Error retrieving user bags by user ID. Error: {str(e)}")
            return {'error': str(e)}

    def update_user_bag(self, user_bag_id, item_id=None, item_amount=None, modifier=None):
        try:
            user_bag = LOCAL_USER_BAG.query.get(user_bag_id)
            if user_bag:
                if item_id:
                    user_bag.item_id = item_id
                if item_amount is not None:
                    user_bag.item_amount = item_amount
                if modifier:
                    user_bag.modifier = modifier
                    user_bag.modify_time = SystemTimeToTimeNumber(TimeUTC7())
                
                db.session.commit()
                return {'success': 'User bag updated successfully'}
            else:
                return {'error': 'User bag not found'}
        except Exception as e:
            self.log.error(f"Error updating user bag. Error: {str(e)}")
            return {'error': str(e)}

    def delete_user_bag(self, user_bag_id):
        try:
            user_bag = LOCAL_USER_BAG.query.get(user_bag_id)
            if user_bag:
                db.session.delete(user_bag)
                db.session.commit()
                return {'success': 'User bag deleted successfully'}
            else:
                return {'error': 'User bag not found'}
        except Exception as e:
            self.log.error(f"Error deleting user bag. Error: {str(e)}")
            return {'error': str(e)}
