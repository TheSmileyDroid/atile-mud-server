from flask import jsonify
from flask_socketio import emit

from atile import app, socketio
from mud.models import User
from mud import users
import helper


@app.route("/teste", methods=["GET"])
@helper.token_required
def teste(user: User):
    if len(user.characters) > 0:
        return jsonify({'message': "Bem vindo {}!".format(user.characters[0].name)})
    return jsonify({'message': "Bem vindo {}!".format(user.email)})

@app.route("/users",methods=["GET"])
def get_users():
    return users.get_users()

@app.route("/users/<id>",methods=["GET"])
def get_user(id):
    return users.get_user(id)

@app.route("/users",methods=["POST"])
def post_user():
    return users.post_user()

@app.route("/users/<int:id>",methods=["PUT"])
@helper.token_required
def update_user(id: int, user: User):
    if user.id == id:
        return users.update_user(id)
    else:
        return jsonify({'message': 'Ação não permitida', 'data':{}}), 401

@app.route("/users/<id>",methods=["DELETE"])
def delete_user(id):
    return users.delete_user(id)

@app.route("/auth", methods=['POST'])
def authenticate():
    return helper.auth()

@socketio.on("connection")
def connection(socket):
    print(socket.id)

@socketio.on('teste')
def test(message):
    emit('teste', {'message': 'Isso é só um teste'})
    print('teste', message['id'])