# routes/user_bag_routes.py
from flask import Blueprint, jsonify, request
from models.User_Bag import UserBag_Action
from config.Db_config import Config
from config.log_config import setup_logging
from loguru import logger as log
import modules.Base64Encode as encode
import modules.BaseMd5Encode as md5
import modules.JwtToken as token

user_bag_bp = Blueprint('user_bags', __name__)
user_bag_action = UserBag_Action()

@user_bag_bp.route('/api/UserBags/Get/<int:user_bag_id>', methods=['GET'])
@token.token_required
def get_user_bag(user_bag_id=None):
    log.debug("Receive API: /UserBags/Get/" + encode.encode_base64("user_bag_id=" + str(user_bag_id)))
    if user_bag_id:
        user_bag = user_bag_action.get_user_bag_by_id(user_bag_id)
        if user_bag:
            return jsonify(user_bag)
    if user_bag_id == 0:
        user_bags = user_bag_action.get_all_user_bags()
        return jsonify(user_bags)
    log.error("User bag not found. " + encode.encode_base64("user_bag_id=" + str(user_bag_id)))
    return jsonify({'message': 'User bag not found'}), 404

@user_bag_bp.route('/api/UserBags/GetByUserId/<int:user_id>', methods=['GET'])
@token.token_required
def get_user_bag_by_user_id(user_id):
    log.debug("Receive API: /UserBags/GetByUserId/" + encode.encode_base64("user_id=" + str(user_id)))
    user_bags = user_bag_action.get_user_bag_by_user_id(user_id)
    if user_bags:
        return jsonify(user_bags)
    log.error("User bags not found for user_id. " + encode.encode_base64("user_id=" + str(user_id)))
    return jsonify({'message': 'User bags not found'}), 404

@user_bag_bp.route('/api/UserBags/Create', methods=['POST'])
@token.token_required
def create_user_bag():
    log.debug("Receive API: Create user bag")
    data = request.json
    res = user_bag_action.create_user_bag(
        user_id=data.get('user_id'),
        item_id=data.get('item_id'),
        item_amount=data.get('item_amount'),
        creator=data.get('creator')
    )
    if 'id' in res:
        return jsonify(res), 201
    if 'error' in res:
        return jsonify(res), 500
    else:
        log.error("Error when creating user bag")
        return "Error when creating user bag", 500

@user_bag_bp.route('/api/UserBags/Update/<int:user_bag_id>', methods=['POST'])
@token.token_required
def update_user_bag(user_bag_id):
    data = request.json
    log.debug("Receive API: Update user bag data:" + encode.encode_base64(data))
    updated = user_bag_action.update_user_bag(
        user_bag_id,
        item_id=data.get('item_id'),
        item_amount=data.get('item_amount'),
        modifier=data.get('modifier')
    )
    return jsonify(updated)

@user_bag_bp.route('/api/UserBags/Delete/<int:user_bag_id>', methods=['POST'])
@token.token_required
def delete_user_bag(user_bag_id):
    log.debug("Receive API: Delete " + encode.encode_base64("user_bag_id=" + str(user_bag_id)))
    deleted = user_bag_action.delete_user_bag(user_bag_id)
    if deleted:
        return jsonify({'message': 'User bag deleted'}), 200
    return jsonify({'message': 'User bag not found'}), 404
