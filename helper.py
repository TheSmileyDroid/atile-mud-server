from datetime import datetime, timedelta
from threading import current_thread
from atile import app
import jwt
from werkzeug.security import check_password_hash
from flask import request, jsonify
from functools import wraps
from mud.users import user_by_email
from mud import user_id_dict

def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Não foi possível verificar', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401
    
    user = user_by_email(auth.username)
    if not user:
        return jsonify({'message': 'Email não encontrado', 'data': {}}), 401
    
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'username': user.email, 'exp': datetime.now() + timedelta(hours=12)},
                            app.config['SECRET_KEY'])
        return jsonify({'message': 'Validação feita com sucesso', 'token': token,
                        'exp': datetime.now() + timedelta(hours=12)})
    
    return jsonify({'message': 'Não foi possível verificar', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

def socket_auth(id, email, password):
    if not email or not password:
        return
    user = user_by_email(email)
    if not user:
        return {'message': 'Email não encontrado', 'error': True}
    if check_password_hash(user.password, password):
        user_id_dict[id] = user
        return {'message': 'Login completo', 'error': False}
    return {'message': 'Senha incorreta', 'error': True}
                

def token_required(f):
    wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Está faltando o token', 'data': {}}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user = user_by_email(data['username'])
        except:
            return jsonify({'message': 'Token inválido ou expirado', 'data': {}}), 401
        return f(user=user, *args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

    