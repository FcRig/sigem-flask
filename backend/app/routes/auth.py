from flask import Blueprint, request, jsonify
from ..models import User
from ..extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/teste', methods=['GET'])
def teste():
    return 'Backend funcionando!'

@bp.route('/register', methods=['POST'])
def register():    
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'Usuário registrado com sucesso.'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    # Accept both "email" and "username" fields to identify the user
    identifier = data.get('email') or data.get('username')
    if not identifier or 'password' not in data:
        return jsonify({'msg': 'Credenciais inválidas.'}), 400

    query_field = 'email' if 'email' in data else 'username'
    user = User.query.filter_by(**{query_field: identifier}).first()

    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token)

    return jsonify({'msg': 'Usuário ou senha inválidos'}), 401

@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(username=user.username, email=user.email)

@bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    user_list = [
        {"id": u.id, "username": u.username, "email": u.email}
        for u in users
    ]
    return jsonify(user_list), 200
