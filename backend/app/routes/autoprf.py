from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests

from ..models import User
from ..extensions import db
from ..utils import strip_strings
from ..services.autoprf_client import AutoPRFClient

bp = Blueprint('autoprf', __name__, url_prefix='/api/autoprf')

@bp.route('/login', methods=['POST'])
@jwt_required()
def login():
    user = User.query.get_or_404(get_jwt_identity())
    data = strip_strings(request.get_json() or {})
    password = data.get('senha_autoprf') or data.get('password')
    token = data.get('token_autoprf') or data.get('token')
    if not password or not token:
        return jsonify({'msg': 'Credenciais inválidas'}), 400

    client = AutoPRFClient()
    try:
        jwt_token = client.login(user.cpf, password, token)
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code in (401, 403):
            user.autoprf_session = None
            db.session.commit()
            return jsonify({'msg': 'Sessão AutoPRF expirada'}), 401
        raise

    user.autoprf_session = jwt_token
    db.session.commit()
    return jsonify({'jwt': jwt_token}), 200

@bp.route('/pesquisar_ai', methods=['POST'])
@jwt_required()
def pesquisar_auto_infracao():
    user = User.query.get_or_404(get_jwt_identity())
    
    if not user.autoprf_session:
        return jsonify({'msg': 'Sessão não iniciada'}), 400

    data = strip_strings(request.get_json() or {})
    auto_infracao = data.get('auto_infracao')
    if not auto_infracao:
        return jsonify({'msg': 'Número de Auto de Infração não informado'}), 400

    client = AutoPRFClient(jwt_token=user.autoprf_session)
    try:
        result = client.pesquisa_auto_infracao(auto_infracao)
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code in (401, 403):
            user.autoprf_session = None
            db.session.commit()
            return jsonify({'msg': 'Sessão AutoPRF expirada'}), 401
        raise

    return jsonify(result)


@bp.route('/envolvidos/<int:auto_id>', methods=['GET'])
@jwt_required()
def obter_envolvidos(auto_id):
    user = User.query.get_or_404(get_jwt_identity())

    if not user.autoprf_session:
        return jsonify({'msg': 'Sessão não iniciada'}), 400

    client = AutoPRFClient(jwt_token=user.autoprf_session)
    try:
        result = client.get_envolvidos(auto_id)
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code in (401, 403):
            user.autoprf_session = None
            db.session.commit()
            return jsonify({'msg': 'Sessão AutoPRF expirada'}), 401
        raise

    return jsonify(result)


@bp.route('/solicitacao/cancelamento', methods=['POST'])
@jwt_required()
def solicitar_cancelamento():
    user = User.query.get_or_404(get_jwt_identity())

    if not user.autoprf_session:
        return jsonify({'msg': 'Sessão não iniciada'}), 400

    data = strip_strings(request.get_json() or {})
    numero = data.pop('numero', None) or data.pop('numero_ai', None)
    if not numero:
        return jsonify({'msg': 'Número de Auto de Infração não informado'}), 400

    client = AutoPRFClient(jwt_token=user.autoprf_session)
    try:
        result = client.solicitar_cancelamento(numero, data)
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code in (401, 403):
            user.autoprf_session = None
            db.session.commit()
            return jsonify({'msg': 'Sessão AutoPRF expirada'}), 401
        raise

    return jsonify(result)


@bp.route('/historico/<int:id_processo>', methods=['GET'])
@jwt_required()
def historico(id_processo):
    user = User.query.get_or_404(get_jwt_identity())

    if not user.autoprf_session:
        return jsonify({'msg': 'Sessão não iniciada'}), 400

    client = AutoPRFClient(jwt_token=user.autoprf_session)
    try:
        result = client.historico(id_processo)
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code in (401, 403):
            user.autoprf_session = None
            db.session.commit()
            return jsonify({'msg': 'Sessão AutoPRF expirada'}), 401
        raise

    return jsonify(result)


@bp.route('/anexar/<int:id_processo>', methods=['POST'])
@jwt_required()
def anexar(id_processo):
    user = User.query.get_or_404(get_jwt_identity())

    if not user.autoprf_session:
        return jsonify({'msg': 'Sessão não iniciada'}), 400

    file = request.files.get('file')
    if not file:
        return jsonify({'msg': 'Arquivo não enviado'}), 400

    client = AutoPRFClient(jwt_token=user.autoprf_session)
    try:
        result = client.anexar_documento_processo(
            id_processo, file.read(), file.filename
        )
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code in (401, 403):
            user.autoprf_session = None
            db.session.commit()
            return jsonify({'msg': 'Sessão AutoPRF expirada'}), 401
        raise

    return jsonify({'ok': bool(result)})
