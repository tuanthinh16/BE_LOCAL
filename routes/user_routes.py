#routes/user_routes.py
from flask import Blueprint
from flask import Flask, jsonify, request
from models.User import UserAction
from config.Db_config import Config


user_bp = Blueprint('users', __name__)
user_action = UserAction(Config.db_connection)

@user_bp.route('/Users/Get/<int:user_id>', methods=['GET'])
def get_user(user_id=None):
    if user_id:
        user = user_action.get_by_id(user_id)
        if user:
            return jsonify(user)
    else:
        users = user_action.show_all()
        return jsonify(users)
        
    return jsonify({'message': 'User not found'}), 404

@user_bp.route('/Users', methods=['POST'])
def create_user():
    data = request.json
    user_id = user_action.create(
        username=data.get('username'),
        email=data.get('email'),
        phone=data.get('phone'),
        fullname=data.get('fullname'),
        login_name=data.get('login_name'),
        role=data.get('role'),
        creator=data.get('creator')
    )
    return jsonify({'user_id': user_id}), 201

@user_bp.route('/Users/Update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    data = request.json
    updated = user_action.update(
        user_id,
        username=data.get('username'),
        email=data.get('email'),
        phone=data.get('phone'),
        fullname=data.get('fullname'),
        login_name=data.get('login_name'),
        role=data.get('role'),
        modifier=data.get('modifier')
    )
    if updated:
        return jsonify({'message': 'User updated'})
    return jsonify({'message': 'User not found'}), 404

@user_bp.route('/Users/Delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    deleted = user_action.delete(user_id)
    if deleted:
        return jsonify({'message': 'User deleted'})
    return jsonify({'message': 'User not found'}), 404
