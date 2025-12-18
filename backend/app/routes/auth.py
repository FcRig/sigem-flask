from flask import Blueprint, request, jsonify
from ..models import User
from ..extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..utils import strip_strings

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/teste', methods=['GET'])
def teste():
    return 'Backend funcionando!'

@bp.route('/register', methods=['POST'])
def register():
    data = strip_strings(request.get_json())
    if not data.get('cpf'):
        return jsonify({'msg': 'CPF é obrigatório'}), 400
    username = data.get('username')
    email = data.get('email')
    cpf = data.get('cpf')

    if User.query.filter((User.email == email) | (User.username == username) | (User.cpf == cpf)).first():
        return jsonify({'msg': 'Usuário já existe'}), 400
    user = User(
        username=username,
        email=email,
        administrador=data.get('administrador', False),
        cpf=cpf
    )
    user.set_password(data['password'])
    if data.get('usuario_sei'):
        user.usuario_sei = data['usuario_sei']
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'Usuário registrado com sucesso.'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = strip_strings(request.get_json())
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token)
    return jsonify({'msg': 'Email ou senha inválidos'}), 401

@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return (
        jsonify(
            id=user.id,
            username=user.username,
            email=user.email,
            administrador=user.administrador,
            cpf=user.cpf,
        ),
        200,
    )

@bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    user_list = [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "administrador": u.administrador,
            "cpf": u.cpf,
        }
        for u in users
    ]
    return jsonify(user_list), 200


@bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    current_user = User.query.get(get_jwt_identity())
    if not current_user or not current_user.administrador:
        return jsonify({'msg': 'Acesso não autorizado'}), 403

    data = strip_strings(request.get_json() or {})
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    administrador = data.get('administrador', False)
    cpf = data.get('cpf')
    usuario_sei = data.get('usuario_sei')

    if not username or not email or not password or not cpf:
        return jsonify({'msg': 'Dados inválidos'}), 400

    if User.query.filter((User.email == email) | (User.username == username) | (User.cpf == cpf)).first():
        return jsonify({'msg': 'Usuário já existe'}), 400

    user = User(username=username, email=email, administrador=administrador, cpf=cpf)
    user.set_password(password)
    if usuario_sei:
        user.usuario_sei = usuario_sei
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'Usuário criado com sucesso.'}), 201


@bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return (
        jsonify(
            id=user.id,
            username=user.username,
            email=user.email,
            administrador=user.administrador,
            cpf=user.cpf,
        ),
        200,
    )


@bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = strip_strings(request.get_json() or {})
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'administrador' in data:
        user.administrador = data['administrador']
    if 'cpf' in data:
        user.cpf = data['cpf']
    if data.get('password'):
        user.set_password(data['password'])    
    if data.get('usuario_sei'):
        user.usuario_sei = data['usuario_sei']   
    db.session.commit()
    return jsonify({'msg': 'Usuário atualizado com sucesso.'}), 200


@bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'Usuário removido com sucesso.'}), 200
