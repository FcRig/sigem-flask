import os
import requests
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import User
from ..services.siscom_client import SiscomClient
from ..utils import strip_strings

ENDPOINT = os.getenv("SISCOM_ENDPOINT")

bp = Blueprint("siscom", __name__, url_prefix="/api/siscom")


@bp.route("/login", methods=["POST"])
@jwt_required()
def login():
    user = User.query.get_or_404(get_jwt_identity())
    data = strip_strings(request.get_json() or {})
    password = data.get("senha_siscom") or data.get("password")
    if not password:
        return jsonify({"msg": "Credenciais inválidas"}), 400

    client = SiscomClient()
    try:
        client.login(user.cpf, password)
    except requests.HTTPError:
        return jsonify({"msg": "Erro de autenticação no SISCOM"}), 401
    return jsonify({"msg": "Autenticação SISCOM realizada com sucesso"}), 200


@bp.route("/pesquisar_ai", methods=["POST"])
@jwt_required()
def pesquisar_ai():
    data = strip_strings(request.get_json() or {})
    numero = data.get("numero") or data.get("auto_infracao")
    if not numero:
        return jsonify({"msg": "Número do AI não informado"}), 400

    client = SiscomClient(endpoint=ENDPOINT)
    result = client.pesquisar_ai(numero)
    return jsonify(result)


@bp.route("/historico", methods=["POST"])
@jwt_required()
def historico():
    data = strip_strings(request.get_json() or {})
    numero = data.get("numero")
    if not numero:
        return jsonify({"msg": "Número do AI não informado"}), 400

    client = SiscomClient(endpoint=ENDPOINT)
    result = client.historico(numero)
    return jsonify(result)
