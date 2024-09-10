# routes/user_routes.py

from flask import Blueprint
from flask import Flask, jsonify, request
from config.Db_config import Config
from database.db import db
from models import User
from datetime import datetime
user_bp = Blueprint('users', __name__)

# @user_bp.route('/users', methods=['GET'])
# def get_users():
#     return {'message': 'Hello from users route'}



# API lấy danh sách người dùng
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# API lấy thông tin người dùng theo id
@user_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

# API thêm người dùng
@user_bp.route('/users', methods=['GET'])
def create_user():
    data = request.json
    new_user = User(
        username=data.get('username'),
        email=data.get('email'),
        phone=data.get('phone'),
        fullname=data.get('fullname'),
        login_name=data.get('login_name'),
        role=data.get('role'),
        creator=data.get('creator')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# API cập nhật người dùng
@user_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.modify_time = datetime.utcnow()
    user.modifier = data.get('modifier')
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.fullname = data.get('fullname', user.fullname)
    user.login_name = data.get('login_name', user.login_name)
    user.role = data.get('role', user.role)
    db.session.commit()
    return jsonify(user.to_dict())

# API xóa người dùng
@user_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
