# routes/item_type_routes.py
from flask import Blueprint, jsonify, request
from models.Item_Type import ItemType_Action
from config.Db_config import Config
from config.log_config import setup_logging
from loguru import logger as log
import modules.Base64Encode as encode
import modules.JwtToken as token

item_type_bp = Blueprint('item_types', __name__)
item_type_action = ItemType_Action()

@item_type_bp.route('/api/ItemTypes/Get/<int:item_type_id>', methods=['GET'])
@token.token_required
def get_item_type(item_type_id=None):
    log.debug("Receive API: /ItemTypes/Get/" + encode.encode_base64("item_type_id=" + str(item_type_id)))
    if item_type_id:
        item_type = item_type_action.get_item_type_by_id(item_type_id)
        if item_type:
            return jsonify(item_type)
    if item_type_id == 0:
        item_types = item_type_action.get_all_item_types()
        return jsonify(item_types)
    log.error("Item type not found. " + encode.encode_base64("item_type_id=" + str(item_type_id)))
    return jsonify({'message': 'Item type not found'}), 404

@item_type_bp.route('/api/ItemTypes/Create', methods=['POST'])
@token.token_required
def create_item_type():
    log.debug("Receive API: Create item type")
    data = request.json
    res = item_type_action.create_item_type(
        item_type_code=data.get('item_type_code'),
        item_type_name=data.get('item_type_name'),
        creator=data.get('creator')
    )
    if 'id' in res:
        return jsonify(res), 201
    if 'error' in res:
        return jsonify(res), 500
    else:
        log.error("Error when creating item type")
        return "Error when creating item type", 500

@item_type_bp.route('/api/ItemTypes/Update/<int:item_type_id>', methods=['POST'])
@token.token_required
def update_item_type(item_type_id):
    data = request.json
    log.debug("Receive API: Update item type data:" + encode.encode_base64(data))
    updated = item_type_action.update_item_type(
        item_type_id,
        item_type_code=data.get('item_type_code'),
        item_type_name=data.get('item_type_name'),
        modifier=data.get('modifier')
    )
    return jsonify(updated)

@item_type_bp.route('/api/ItemTypes/Delete/<int:item_type_id>', methods=['POST'])
@token.token_required
def delete_item_type(item_type_id):
    log.debug("Receive API: Delete " + encode.encode_base64("item_type_id=" + str(item_type_id)))
    deleted = item_type_action.delete_item_type(item_type_id)
    if deleted:
        return jsonify({'message': 'Item type deleted'}), 200
    return jsonify({'message': 'Item type not found'}), 404
