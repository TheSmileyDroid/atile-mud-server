from werkzeug.security import generate_password_hash
from atile import app, db
from flask import request, jsonify
from mud.models import (User, user_schema, users_schema,
                        Character, character_schema, characters_schema)

def user_by_email(email):
    try:
        return User.query.filter(User.email == email).one()
    except:
        return None


def get_users():
    users = User.query.all()
    if not users:
        return jsonify({'message': 'Usuários não encontrados', 'data': {}}), 404
    result = users_schema.dump(users)
    return jsonify({'message': 'Usuários encontrados', 'data': result}), 201

def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado', 'data': {}}), 404
    result = user_schema.dump(user)
    return jsonify({'message': 'Usuário encontrado', 'data': result}), 201

def post_user():
    email = request.json['email']
    password = request.json['password']
    pass_hash = generate_password_hash(password)
    user = User(email=email, password=pass_hash.encode("utf-8", "ignore"))
    try:
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({'message': 'Criado com sucesso', 'data': result}), 201
    except Exception as e:
        return jsonify({'message': 'Não foi possível criar o usuário', 'data': {}, 'error': str(e)}), 500

def update_user(id):
    email = request.json['email']
    password = request.json['password']

    user = User.query.get(id)

    if not user:
        return jsonify({'message': 'Usuário não exite'}), 404

    pass_hash = generate_password_hash(password)

    try:
        user.email = email
        user.password = pass_hash
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({'message': 'Atualizado com sucesso', 'data': result}), 201
    except Exception as e:
        return jsonify({'message': 'Não foi possível atualizar o usuário', 'data': {}, 'error': str(e)}), 500

def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({'message': 'Usuário não exite'}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({'message': 'Usuário deletado com sucesso', 'data': result}), 201
    except Exception as e:
        return jsonify({'message': 'Não foi possível deletar o usuário', 'data': {}, 'error': str(e)}), 500