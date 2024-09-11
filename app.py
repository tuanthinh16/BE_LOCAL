# app.py

from ntpath import join
from posixpath import dirname
import sqlite3
from flask import Flask, jsonify, request
from routes.user_routes import user_bp
from models.User import UserAction
from config.Db_config import Config
from config.log_config import setup_logging
from loguru import logger as log
from dotenv import load_dotenv

app = Flask(__name__)
setup_logging()

log.debug("Server start__BEGIN")
app.register_blueprint(user_bp)
def init_db():
    # create table user
    log.debug("Init Database__Start")
    user_action = UserAction(Config.db_connection)
    user_action.initTable()

with app.app_context():
    init_db()
    log.debug("Init Database__End")


dotenv_path = join(dirname(__file__), '.env') 
load_dotenv(dotenv_path)
log.debug("Server start__END")
if __name__ == '__main__':
    app.run(debug=True)
