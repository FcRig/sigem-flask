from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import User
from ..extensions import db
from ..utils.autoprf import AutoPRFClient

bp = Blueprint('autoprf', __name__, url_prefix='/api/autoprf')

@bp.route('/login', methods=['POST'])
@jwt_required()
def login():
    user = User.query.get_or_404(get_jwt_identity())
    data = request.get_json() or {}
    password = data.get('senha_autoprf') or data.get('password')
    token = data.get('token_autoprf') or data.get('token')
    if not password or not token:
        return jsonify({'msg': 'Credenciais inválidas'}), 400

    client = AutoPRFClient()
    jwt_token = client.login(user.cpf, password, token)

    user.autoprf_session = jwt_token
    db.session.commit()
    return jsonify({'jwt': jwt_token}), 200

@bp.route('/pesquisar_ai', methods=['POST'])
@jwt_required()
def pesquisar_auto_infracao():
    user = User.query.get_or_404(get_jwt_identity())
    
    if not user.autoprf_session:
        return jsonify({'msg': 'Sessão não iniciada'}), 400

    data = request.get_json() or {}
    auto_infracao = data.get('auto_infracao')
    if not auto_infracao:
        return jsonify({'msg': 'Número de Auto de Infração não informado'}), 400

    client = AutoPRFClient(jwt_token=user.autoprf_session)
    client.pesquisa_auto_infracao(auto_infracao)

    return jsonify({'msg': 'Pesquisa realizada com sucesso'})
