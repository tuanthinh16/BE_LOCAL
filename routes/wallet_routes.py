#routes/wallet_routes.py
from flask import Blueprint, jsonify, request
from models.Wallet import Wallet_Action
from config.Db_config import Config
from loguru import logger as log
import modules.Base64Encode as encode

wallet_bp = Blueprint('Wallet', __name__)
wallet_action = Wallet_Action()

@wallet_bp.route('/api/Wallet/Get/<int:wallet_id>', methods=['GET'])
def get_wallet(wallet_id=None):
    log.debug("Recive API: /Wallet/Get/" + encode.encode_base64("wallet_id=" + str(wallet_id)))
    if wallet_id:
        wallet = wallet_action.get_wallet_by_id(wallet_id)
        if wallet:
            return jsonify(wallet), 200
    if wallet_id == 0:
        Wallet = wallet_action.show_all()
        return jsonify(Wallet), 200
    log.error("Wallet not found. " + encode.encode_base64("wallet_id=" + str(wallet_id)))
    return jsonify({'message': 'Wallet not found'}), 404

@wallet_bp.route('/api/Wallet/Create', methods=['POST'])
def create_wallet():
    log.debug("Recive API: Create wallet")
    data = request.json
    res = wallet_action.create_wallet(
        username=data.get('username'),
        user_id=data.get('user_id'),
        balance=data.get('balance'),
        creator=data.get('creator')
    )
    if 'wallet_id' in res:
        return jsonify(res), 201
    if 'error' in res:
        return jsonify(res), 500
    else:
        log.error("Error when creating wallet")
        return "error when create wallet", 500

@wallet_bp.route('/api/Wallet/Update/<int:wallet_id>', methods=['POST'])
def update_wallet(wallet_id):
    data = request.json
    log.debug("Recive API: Update wallet data:" + encode.encode_base64(str(data)))
    updated = wallet_action.update_wallet(
        wallet_id,
        username=data.get('username'),
        balance=data.get('balance'),
        modifier=data.get('modifier')
    )
    if updated:
        return jsonify({'message': 'Wallet updated'})
    return jsonify({'message': 'Wallet not found'}), 404

@wallet_bp.route('/api/Wallet/Delete/<int:wallet_id>', methods=['POST'])
def delete_wallet(wallet_id):
    log.debug("Recive API: Delete " + encode.encode_base64("wallet_id=" + str(wallet_id)))
    deleted = wallet_action.delete_wallet(wallet_id)
    if deleted:
        return jsonify({'message': 'Wallet deleted'})
    return jsonify({'message': 'Wallet not found'}), 404
