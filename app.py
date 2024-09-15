# app.py

from ntpath import join
from posixpath import dirname
import sqlite3
from flask import Flask, jsonify, request
from routes.user_routes import user_bp
from routes.wallet_routes import wallet_bp
from routes.transaction_routes import transaction_bp
from routes.role_routes import role_bp
from routes.item_routes import item_bp
from routes.item_type_routes import item_type_bp
from routes.bag_routes import user_bag_bp
from models.User import UserAction
from models.Wallet import Wallet_Action
from models.Role import Role_Action
from models.Transaction import Transaction_Action
from config.Db_config import Config
from config.log_config import setup_logging
from loguru import logger as log
from dotenv import load_dotenv
from database.db import db,init_db
from SQL.Run_Sql import DAO
app = Flask(__name__)
setup_logging()

log.debug("Server start__BEGIN")

app.config.from_object(Config)

# Khởi tạo kết nối cơ sở dữ liệu
init_db(app)
dao = DAO(db_session=db.session)

dotenv_path = join(dirname(__file__), '.env') 
load_dotenv(dotenv_path)


#routes
app.register_blueprint(user_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(wallet_bp)
app.register_blueprint(role_bp)
app.register_blueprint(item_bp)
app.register_blueprint(item_type_bp)
app.register_blueprint(user_bag_bp)
#
def init_db():
    # create table user
   
    log.debug("Init Database__Start")
    db.create_all()

def get_data():
    query = '''SELECT us.* FROM public."LOCAL_USERS" us 
                left join public."LOCAL_WALLET" wl on wl.id = us.wallet_id 
                where wl.id = 8'''
    
    results = dao.get(query)
    print(results)

with app.app_context():
    init_db()
    #get_data()
    log.debug("Init Database__End")
log.debug("Server start__END")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
