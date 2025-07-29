from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests

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
        client.login(usuario, senha, token)
    except requests.HTTPError:
        return jsonify({"msg": "Erro de autenticação no SEI"}), 401
    return jsonify({"msg": "Autenticação SEI realizada com sucesso"}), 200


@bp.route("/tipos", methods=["POST"])
@jwt_required()
def tipos_processo():
    """Retorna os tipos de processos disponíveis no SEI."""
    user = User.query.get_or_404(get_jwt_identity())
    data = strip_strings(request.get_json() or {})
    usuario = data.get("usuario") or data.get("usuario_sei") or user.usuario_sei
    senha = data.get("senha_sei") or data.get("password")
    token = data.get("token_sei") or data.get("token")
    if not usuario or not senha or not token:
        return jsonify({"msg": "Credenciais inválidas"}), 400

    client = SEIClient()
    try:
        client.login(usuario, senha, token)
        tipos = client.list_process_types()
    except requests.HTTPError:
        return jsonify({"msg": "Erro de autenticação no SEI"}), 401
    except Exception:
        return jsonify({"msg": "Erro ao listar tipos de processo"}), 400

    return jsonify(tipos), 200


@bp.route("/processos", methods=["POST"])
@jwt_required()
def criar_processo():
    """Cria um processo no SEI com as credenciais fornecidas."""
    user = User.query.get_or_404(get_jwt_identity())
    data = strip_strings(request.get_json() or {})

    usuario = data.get("usuario") or data.get("usuario_sei") or user.usuario_sei
    senha = data.get("senha_sei") or data.get("password")
    token = data.get("token_sei") or data.get("token")
    tipo_id = data.get("tipo_id")
    tipo_nome = data.get("tipo_nome")
    descricao = data.get("descricao")

    if not usuario or not senha or not token or not tipo_id or not tipo_nome or not descricao:
        return jsonify({"msg": "Dados incompletos"}), 400

    client = SEIClient()
    try:
        client.login(usuario, senha, token)
        resp = client.create_process(tipo_id, tipo_nome, descricao)
        resp.raise_for_status()
    except requests.HTTPError:
        return jsonify({"msg": "Erro ao criar processo no SEI"}), 400

    return jsonify({"msg": "Processo criado com sucesso"}), 200
