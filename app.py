# app.py

from ntpath import join
from posixpath import dirname
import sqlite3
from flask import Flask, jsonify, request
from routes.user_routes import user_bp
from routes.wallet_routes import wallet_bp
from routes.transaction_routes import transaction_bp
from routes.role_routes import role_bp
from models.User import UserAction
from models.Wallet import Wallet_Action
from models.Role import Role_Action
from models.Transaction import Transaction_Action
from config.Db_config import Config
from config.log_config import setup_logging
from loguru import logger as log
from dotenv import load_dotenv
from database.db import db,init_db

app = Flask(__name__)
setup_logging()

log.debug("Server start__BEGIN")

app.config.from_object(Config)

# Khởi tạo kết nối cơ sở dữ liệu
init_db(app)

dotenv_path = join(dirname(__file__), '.env') 
load_dotenv(dotenv_path)


#routes
app.register_blueprint(user_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(wallet_bp)
app.register_blueprint(role_bp)
#
def init_db():
    # create table user
    db.create_all()
    log.debug("Init Database__Start")
    user_action = UserAction()
    user_action.initTable()
    wallet_action = Wallet_Action()
    wallet_action.initTable()
    role_action = Role_Action()
    role_action.initTable()
    trans_acton = Transaction_Action()
    trans_acton.initTable()

    #add sample data
    # user_action.insert_sample_data()
    # wallet_action.insert_sample_data()
    # role_action.insert_sample_data()
    # trans_acton.insert_sample_data()


with app.app_context():
    init_db()
    log.debug("Init Database__End")
log.debug("Server start__END")

if __name__ == '__main__':
    app.run(debug=True)
