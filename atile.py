import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)
socketio = SocketIO(app, cors_allowed_origins="*")
migrate = Migrate(app, db)

from mud import models

db.create_all()

import routes

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
