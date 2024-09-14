#routes/transaction_routes.py
from flask import Blueprint, jsonify, request
from models.Transaction import Transaction_Action
from config.Db_config import Config
from loguru import logger as log
import modules.Base64Encode as encode

transaction_bp = Blueprint('Transaction', __name__)
transaction_action = Transaction_Action()

@transaction_bp.route('/api/Transaction/Get/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id=None):
    log.debug("Recive API: /Transaction/Get/" + encode.encode_base64("transaction_id=" + str(transaction_id)))
    if transaction_id:
        transaction = transaction_action.get_transaction(transaction_id)
        if transaction:
            return jsonify(transaction), 200
    log.error("Transaction not found. " + encode.encode_base64("transaction_id=" + str(transaction_id)))
    return jsonify({'message': 'Transaction not found'}), 404

@transaction_bp.route('/api/Transaction/Create', methods=['POST'])
def create_transaction():
    log.debug("Recive API: Create transaction")
    data = request.json
    res = transaction_action.create_transaction(
        request_user_id=data.get('request_user_id'),
        amount=data.get('amount'),
        recive_user_id=data.get('recive_user_id'),
        creator=data.get('creator'),
        fee=data.get('fee')
    )
    if res:
        return {"message":res},201
    else:
        log.error("Error when creating transaction")
        return "error when create transaction", 500

@transaction_bp.route('/api/Transaction/Update/<int:transaction_id>', methods=['POST'])
def update_transaction(transaction_id):
    data = request.json
    log.debug("Recive API: Update transaction data:" + encode.encode_base64(str(data)))
    updated = transaction_action.update_transaction(
        transaction_id,
        bill_id=data.get('bill_id'),
        is_pause=data.get('is_pause')
    )
    if updated:
        return jsonify({'message': 'Transaction updated'})
    return jsonify({'message': 'Transaction not found'}), 404

@transaction_bp.route('/api/Transaction/Delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    log.debug("Recive API: Delete " + encode.encode_base64("transaction_id=" + str(transaction_id)))
    deleted = transaction_action.delete_transaction(transaction_id)
    if deleted:
        return jsonify({'message': 'Transaction deleted'})
    return jsonify({'message': 'Transaction not found'}), 404
