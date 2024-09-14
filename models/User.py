
# models/user.py
from flask_sqlalchemy import SQLAlchemy
from config.uct7_config import TimeUTC7
from loguru import logger as log
import modules.Base256Encode as endcode256
from modules.Convert import SystemTimeToTimeNumber
from modules.LocalData import get_token_login,get_login_name
from models.Wallet import LOCAL_WALLET,Wallet_Action
from models.Transaction import LOCAL_TRANSACTION,Transaction_Action
import  modules.BaseMd5Encode as md5
# Đảm bảo rằng `db` đã được import từ database/db.py
from database.db import db
import modules.JwtToken as token

class LOCAL_USER(db.Model):
    __tablename__ = 'LOCAL_USERS'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.BigInteger)
    creator = db.Column(db.String)
    modify_time = db.Column(db.BigInteger, nullable=True)
    modifier = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Integer, default=1)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    fullname = db.Column(db.String(100))
    login_name = db.Column(db.String(50))
    role_id = db.Column(db.Integer, nullable=True)
    user_identifer = db.Column(db.String(500))
    wallet_id = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String(200))

    def to_dict(self):
        return {
            'id': self.id,
            'create_time': self.create_time,
            'creator': self.creator,
            'modify_time': self.modify_time,
            'modifier': self.modifier,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'fullname': self.fullname,
            'login_name': self.login_name,
            'role_id': self.role_id,
            'user_identifer': self.user_identifer,
            'wallet_id': self.wallet_id
        }

    def __init__(self, id=None, username=None, create_time=None, email=None, phone=None, fullname=None, login_name=None, role_id=None, creator=None, modifier=None, user_identifer=None, wallet_id=None, is_active=1,password=None):
        self.id = id
        self.username = username
        self.email = email
        self.phone = phone
        self.create_time = create_time
        self.fullname = fullname
        self.login_name = login_name
        self.role_id = role_id
        self.creator = creator
        self.modifier = modifier
        self.user_identifer = user_identifer
        self.wallet_id = wallet_id
        self.is_active = is_active
        self.password = password

class UserAction:
    def __init__(self):
        self.log = log

    def initTable(self):
        # Không cần thiết phải thực hiện điều này với SQLAlchemy vì SQLAlchemy tự động tạo bảng khi cần
        pass

    def show_all(self):
        try:
            users = LOCAL_USER.query.all()
            return [user.to_dict() for user in users]
        except Exception as e:
            self.log.error("Error when get all user. Error: " + str(e))
            return []

    def get_by_id(self, user_id):
        try:
            user = LOCAL_USER.query.get(user_id)
            return user.to_dict() if user else None
        except Exception as e:
            self.log.error("Error when find user. Error: " + str(e))
            return None

    def create(self, username, email, phone, fullname, login_name, role_id, creator,password):
        try:
            # Check if email or username already exists
            user_exists = LOCAL_USER.query.filter((LOCAL_USER.email == email) | (LOCAL_USER.username == username)).first()
            if user_exists:
                return {'error': 'Email or Username already exists'}
            
            create_time = SystemTimeToTimeNumber(TimeUTC7())
            user_identifer_dict = f"username={username};email={email};role={role_id}"
            user_identifer = endcode256.hash_sha256(user_identifer_dict)
            
            new_user = LOCAL_USER(
                create_time=create_time,
                creator=creator,
                username=username,
                email=email,
                phone=phone,
                fullname=fullname,
                login_name=login_name,
                role_id=role_id,
                is_active=1,
                user_identifer=user_identifer,
                password = password
            )
            db.session.add(new_user)
            db.session.commit()
            wallet = Wallet_Action()
            wallet.create_wallet(new_user.username,new_user.id)
            db.session.commit()
            wl = LOCAL_WALLET.query.filter(LOCAL_WALLET.username == new_user.username).first()
            if wl:
                new_user.wallet_id = wl.id
                db.session.commit()
            return {'user_id': new_user.id}
        except Exception as e:
            self.log.error(f"Error when creating user. Error: {str(e)}")
            return {'error': str(e)}

    def update(self, user_id, email=None, phone=None, fullname=None, login_name = None,role_id=None, wallet_id = None,modifier=None):
        try:
            user = LOCAL_USER.query.get(user_id)
            if user:

                if email:
                    user.email = email
                if phone:
                    user.phone = phone
                if fullname:
                    user.fullname = fullname
                if login_name:
                    user.login_name = login_name
                user.role_id = role_id
                user.modifier = get_login_name()
                user.modify_time = SystemTimeToTimeNumber(TimeUTC7())
                
                db.session.commit()
                return {"message": "Successfully"}, 200
            else:
                return {"message": "User not found"}, 404
        except Exception as e:
            self.log.error("Error when update user. Error: " + str(e))
            return {"message": "Error"}, 500
    
    def delete(self, user_id):
        try:
            user = LOCAL_USER.query.get(user_id)
            if user:
                if user.wallet_id:
                    wallet = LOCAL_WALLET.query.get(user.wallet_id)
                    if wallet:
                        db.session.delete(wallet)
                        tran = LOCAL_TRANSACTION.query(wallet.transaction_id)
                        if tran:
                            tran.is_active = 1
                            tran.modify_message = f"Delete Wallet & User (user_id = {user_id},wallet_id  {wallet.id})"
                db.session.delete(user)
                db.session.commit()
                return {"message": "Successfully"}, 200
            else:
                return {"message": "User not found"}, 404
        except Exception as e:
            self.log.error("Error when delete user. Error: " + str(e))
            return {"message": "Error"}, 500
    def login(self,username,password):
        try:
            user = LOCAL_USER.query.filter(LOCAL_USER.username == username).first()
            if user:
                if user.password == md5.base_md5_endcode(password):
                    
                    _token = token.create_jwt_token({'username':username,'role_id':user.role_id})
                    if _token :
                        return {"username":username,"token":_token}
                    else:
                        return {"Error":"Error when generate token"}
                else:
                    return {"Error":"Wrong password"}
            else:
                return {"Error":"User not found"}
        except Exception as e:
            self.log.error("Error when login. Error: " + str(e))
            return {"message": "Error"}
    def get_user_by_username(self, username):
        try:
            # Thực hiện truy vấn SQL để lấy ví theo user_id
            sql = '''
            SELECT * FROM LOCAL_USERS
            WHERE username = :username
            '''
            result = db.session.execute(sql, {'username': username}).fetchone()
            
            if result:
                # Chuyển đổi kết quả thành dictionary (hoặc theo cấu trúc bạn cần)
                user = dict(result)
                return user
            else:
                return {'error': 'User not found'}
        except Exception as e:
            self.log.error(f"Error retrieving User by username. Error: {str(e)}")
            return {'error': str(e)}
