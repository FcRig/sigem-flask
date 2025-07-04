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
