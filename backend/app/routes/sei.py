from flask import Blueprint, jsonify, request
import json
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests

from ..extensions import db

from ..models import User
from ..services.sei_client import SEIClient
from ..utils import strip_strings


bp = Blueprint("sei", __name__, url_prefix="/api/sei")


@bp.route("/login", methods=["POST"])
@jwt_required()
def login():
    user = User.query.get_or_404(get_jwt_identity())

    data = strip_strings(request.get_json() or {})

    usuario = data.get("usuario") or data.get("usuario_sei") or user.usuario_sei
    senha = data.get("senha_sei") or data.get("password")
    token = data.get("token_sei") or data.get("token")

    if not usuario or not senha or not token:
        return jsonify({"msg": "Credenciais inválidas"}), 400

    client = SEIClient()
    try:
        response = client.login(usuario, senha, token)

    except requests.HTTPError:
        return jsonify({"msg": "Erro de autenticação no SEI"}), 401

    user.sei_session = json.dumps(response["cookies"])
    user.sei_home_url = json.dumps(response["url_home"])

    user.sei_home_html = client.home_html
    user.usuario_sei = usuario
    db.session.commit()
    return jsonify({"msg": "Autenticação SEI realizada com sucesso"}), 200


@bp.route("/procurar-processo", methods=["POST"])
@jwt_required()
def procurarprocesso():

    dados = request.get_json()
    processo = dados.get('processo')
    client = SEIClient()
    
    try:
        response = client.search_process(processo)
        return {'response': response}

    except Exception as e:
        print("aaaa")
        print(e)

    return {"a": "su "}


@bp.route("/tipos", methods=["POST"])
@jwt_required()
def tipos_processo():
    """Retorna os tipos de processos disponíveis no SEI."""

    user = User.query.get_or_404(get_jwt_identity())

    if not user.sei_session or not user.sei_home_html:
        return jsonify({"msg": "Sessão não iniciada"}), 400

    session = requests.Session()
    session.cookies = requests.utils.cookiejar_from_dict(json.loads(user.sei_session))
    client = SEIClient(session=session)
    client.home_html = user.sei_home_html
    try:
        tipos = client.list_process_types()
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code in (401, 403):
            user.sei_session = None
            user.sei_home_html = None
            db.session.commit()
            return jsonify({"msg": "Sessão SEI expirada"}), 401
        raise
    except Exception:
        return jsonify({"msg": "Erro ao listar tipos de processo"}), 400

    return jsonify(tipos), 200


@bp.route("/unidades", methods=["POST"])
@jwt_required()
def listar_unidades():
    """Retorna as unidades disponíveis para o usuário."""
    user = User.query.get_or_404(get_jwt_identity())

    if not user.sei_session or not user.sei_home_html:
        return jsonify({"msg": "Sessão não iniciada"}), 400

    session = requests.Session()
    session.cookies = requests.utils.cookiejar_from_dict(json.loads(user.sei_session))
    client = SEIClient(session=session)
    client.home_html = user.sei_home_html
    try:
        unidades = client.list_units()
        user.sei_home_html = client.home_html
        db.session.commit()
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code in (401, 403):
            user.sei_session = None
            user.sei_home_html = None
            db.session.commit()
            return jsonify({"msg": "Sessão SEI expirada"}), 401
        return jsonify({"msg": "Erro ao obter unidades"}), 400

    return jsonify(unidades), 200


@bp.route("/processos", methods=["POST"])
@jwt_required()
def criar_processo():
    """Cria um processo no SEI com as credenciais fornecidas."""
    user = User.query.get_or_404(get_jwt_identity())
    data = strip_strings(request.get_json() or {})

    tipo_nome = data.get("tipo_nome")
    descricao = data.get("descricao")

    if not user.sei_session or not user.sei_home_html or not tipo_nome or not descricao:
        return jsonify({"msg": "Dados incompletos"}), 400

    session = requests.Session()
    session.cookies = requests.utils.cookiejar_from_dict(json.loads(user.sei_session))
    client = SEIClient(session=session)
    client.home_html = user.sei_home_html

    try:
        resp = client.create_process(tipo_nome, descricao)
        resp.raise_for_status()
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code in (401, 403):
            user.sei_session = None
            user.sei_home_html = None
            db.session.commit()
            return jsonify({"msg": "Sessão SEI expirada"}), 401
        return jsonify({"msg": "Erro ao criar processo no SEI"}), 400

    return jsonify({"msg": "Processo criado com sucesso"}), 200
