#routes/user_routes.py
from flask import Blueprint
from flask import Flask, jsonify, request
from models.User import UserAction
from config.Db_config import Config
from config.log_config import setup_logging
from loguru import logger as log
import modules.Base64Encode as encode

user_bp = Blueprint('users', __name__)
user_action = UserAction(Config.db_connection)

@user_bp.route('/Users/Get/<int:user_id>', methods=['GET'])
def get_user(user_id=None):
    log.debug("Recive API: /User/Get/"+encode.encode_base64("user_id="+str(user_id)))
    if user_id:
        user = user_action.get_by_id(user_id)
        if user:
            return jsonify(user)
    if user_id == 0:
        users = user_action.show_all()
        return jsonify(users)
    log.error("User not found. "+encode.encode_base64("user_id="+str(user_id)))
    return jsonify({'message': 'User not found'}), 404

@user_bp.route('/Users/Create', methods=['POST'])
def create_user():
    log.debug("Recive API: Create user")
    data = request.json
    res = user_action.create(
        username=data.get('username'),
        email=data.get('email'),
        phone=data.get('phone'),
        fullname=data.get('fullname'),
        login_name=data.get('login_name'),
        role=data.get('role'),
        creator=data.get('creator')
    )
    if 'user_id' in res:
        return jsonify(res), 201
    if 'error' in res:
        return jsonify(res), 500
    else:
        log.error("Error when creating user")
        return "error when create user", 500

@user_bp.route('/Users/Update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    
    data = request.json
    log.debug("Recive API: Update user data:"+encode.encode_base64(data))
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
    log.debug("Recive API: Delete "+encode.encode_base64("user_id="+str(user_id)))
    deleted = user_action.delete(user_id)
    if deleted:
        return jsonify({'message': 'User deleted'})
    return jsonify({'message': 'User not found'}), 404
