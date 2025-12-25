from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
import logging

from ..models import User
from ..extensions import db
from ..utils import strip_strings
from ..services.autoprf_client import AutoPRFClient

bp = Blueprint('autoprf', __name__, url_prefix='/api/autoprf')

logger = logging.getLogger(__name__)


def _clear_autoprf_session(user, reason, status_code=None):
    user.autoprf_session = None
    db.session.commit()
    status = status_code if status_code is not None else "unknown"
    logger.warning(
        "AutoPRF session cleared (%s) for user_id=%s status=%s",
        reason,
        user.id,
        status,
    )

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
        print("JWT Token:", jwt_token)  # Debugging line
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code in (401, 403):
            _clear_autoprf_session(user, "login", e.response.status_code)
            return jsonify({'msg': 'Sessão AutoPRF expirada'}), 401
        raise

    user.autoprf_session = jwt_token
    db.session.commit()
    logger.info(
        "AutoPRF session stored for user_id=%s token_len=%s",
        user.id,
        len(jwt_token) if jwt_token else 0,
    )
    return jsonify({'jwt': jwt_token}), 200

@bp.route('/pesquisar_ai', methods=['POST'])
@jwt_required()
def pesquisar_auto_infracao():
    user = User.query.get_or_404(get_jwt_identity())   
    print("User AutoPRF Session:", user.autoprf_session)  # Debugging line 
    
    if not user.autoprf_session:
        return jsonify({'msg': 'Sessão não iniciada'}), 400

    data = strip_strings(request.get_json() or {})
    auto_infracao = data.get('auto_infracao')
    print("Auto Infracao:", auto_infracao)  # Debugging line
    if not auto_infracao:
        return jsonify({'msg': 'Número de Auto de Infração não informado'}), 400

    client = AutoPRFClient(jwt_token=user.autoprf_session)
    try:
        result = client.pesquisa_auto_infracao(auto_infracao)
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code in (401, 403):
            _clear_autoprf_session(user, "pesquisar_ai", e.response.status_code)
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
            _clear_autoprf_session(user, "envolvidos", e.response.status_code)
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
            _clear_autoprf_session(user, "solicitacao_cancelamento", e.response.status_code)
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
            _clear_autoprf_session(user, "historico", e.response.status_code)
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
            _clear_autoprf_session(user, "anexar", e.response.status_code)
            return jsonify({'msg': 'Sessão AutoPRF expirada'}), 401
        raise

    return jsonify({'ok': bool(result)})
