#routes/role_routes.py
from flask import Blueprint, jsonify, request
from models.Role import Role_Action
from config.Db_config import Config
from loguru import logger as log
import modules.Base64Encode as encode

role_bp = Blueprint('Role', __name__)
role_action = Role_Action()

@role_bp.route('/api/Role/Get/<int:role_id>', methods=['GET'])
def get_role(role_id=None):
    log.debug("Recive API: /Role/Get/" + encode.encode_base64("role_id=" + str(role_id)))
    if role_id:
        role = role_action.get_role(role_id)
        if role:
            return jsonify(role), 200
    log.error("Role not found. " + encode.encode_base64("role_id=" + str(role_id)))
    return jsonify({'message': 'Role not found'}), 404

@role_bp.route('/api/Role/Create', methods=['POST'])
def create_role():
    log.debug("Recive API: Create role")
    data = request.json
    res = role_action.create_role(
        role_name=data.get('role_name'),
        description=data.get('description'),
        creator=data.get('creator')
    )
    if 'role_id' in res:
        return jsonify(res), 201
    if 'error' in res:
        return jsonify(res), 500
    else:
        log.error("Error when creating role")
        return "error when create role", 500

@role_bp.route('/api/Role/Update/<int:role_id>', methods=['POST'])
def update_role(role_id):
    data = request.json
    log.debug("Recive API: Update role data:" + encode.encode_base64(str(data)))
    updated = role_action.update_role(
        role_id,
        role_name=data.get('role_name'),
        description=data.get('description'),
        modifier=data.get('modifier')
    )
    if updated:
        return jsonify({'message': 'Role updated'})
    return jsonify({'message': 'Role not found'}), 404

@role_bp.route('/api/Role/Delete/<int:role_id>', methods=['POST'])
def delete_role(role_id):
    log.debug("Recive API: Delete " + encode.encode_base64("role_id=" + str(role_id)))
    deleted = role_action.delete_role(role_id)
    if deleted:
        return jsonify({'message': 'Role deleted'})
    return jsonify({'message': 'Role not found'}), 404
