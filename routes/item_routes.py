# routes/item_routes.py
from flask import Blueprint, jsonify, request
from models.Item import Item_Action
from config.Db_config import Config
from config.log_config import setup_logging
from loguru import logger as log
import modules.Base64Encode as encode
import modules.BaseMd5Encode as md5
import modules.JwtToken as token

item_bp = Blueprint('items', __name__)
item_action = Item_Action()

@item_bp.route('/api/Items/Get/<int:item_id>', methods=['GET'])
@token.token_required
def get_item(item_id=None):
    log.debug("Receive API: /Items/Get/" + encode.encode_base64("item_id=" + str(item_id)))
    if item_id:
        item = item_action.get_item_by_id(item_id)
        if item:
            return jsonify(item)
    if item_id == 0:
        items = item_action.get_all_items()
        return jsonify(items)
    log.error("Item not found. " + encode.encode_base64("item_id=" + str(item_id)))
    return jsonify({'message': 'Item not found'}), 404

@item_bp.route('/api/Items/Create', methods=['POST'])
@token.token_required
def create_item():
    log.debug("Receive API: Create item")
    data = request.json
    res = item_action.create_item(
        item_code=data.get('item_code'),
        item_name=data.get('item_name'),
        item_description=data.get('item_description'),
        item_identifer=data.get('item_identifer'),
        creator=data.get('creator')
    )
    if 'id' in res:
        return jsonify(res), 201
    if 'error' in res:
        return jsonify(res), 500
    else:
        log.error("Error when creating item")
        return "Error when creating item", 500

@item_bp.route('/api/Items/Update/<int:item_id>', methods=['POST'])
@token.token_required
def update_item(item_id):
    data = request.json
    log.debug("Receive API: Update item data:" + encode.encode_base64(data))
    updated = item_action.update_item(
        item_id,
        item_code=data.get('item_code'),
        item_name=data.get('item_name'),
        item_description=data.get('item_description'),
        item_identifer=data.get('item_identifer'),
        modifier=data.get('modifier')
    )
    return jsonify(updated)

@item_bp.route('/api/Items/Delete/<int:item_id>', methods=['POST'])
@token.token_required
def delete_item(item_id):
    log.debug("Receive API: Delete " + encode.encode_base64("item_id=" + str(item_id)))
    deleted = item_action.delete_item(item_id)
    if deleted:
        return jsonify({'message': 'Item deleted'}), 200
    return jsonify({'message': 'Item not found'}), 404
