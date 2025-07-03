import os
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..services.siscom_client import SiscomClient

ENDPOINT = os.getenv("SISCOM_ENDPOINT")

bp = Blueprint("siscom", __name__, url_prefix="/api/siscom")


@bp.route("/pesquisar_ai", methods=["POST"])
@jwt_required()
def pesquisar_ai():
    data = request.get_json() or {}
    numero = data.get("numero") or data.get("auto_infracao")
    if not numero:
        return jsonify({"msg": "Número do AI não informado"}), 400

    client = SiscomClient(endpoint=ENDPOINT)
    result = client.pesquisar_ai(numero)
    return jsonify(result)


@bp.route("/historico", methods=["POST"])
@jwt_required()
def historico():
    data = request.get_json() or {}
    numero = data.get("numero")
    if not numero:
        return jsonify({"msg": "Número do AI não informado"}), 400

    client = SiscomClient(endpoint=ENDPOINT)
    result = client.historico(numero)
    return jsonify(result)
