# app.py

import sqlite3
from flask import Flask, jsonify, request
from routes.user_routes import user_bp
from models.User import UserAction
from config.Db_config import Config


app = Flask(__name__)

app.register_blueprint(user_bp)

def init_db():
    # create table user
    user_action = UserAction(Config.db_connection)
    user_action.initTable()


with app.app_context():
    init_db()


if __name__ == '__main__':
    app.run(debug=True)
