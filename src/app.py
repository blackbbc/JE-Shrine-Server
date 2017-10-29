from flask import Flask, jsonify

import api
from error import APIException
from json_encoder import MongoJSONEncoder

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(api.bp, url_prefix='/api')

from model import db, login_manager
db.init_app(app)
login_manager.init_app(app)
# app.json_encoder = MongoJSONEncoder

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
