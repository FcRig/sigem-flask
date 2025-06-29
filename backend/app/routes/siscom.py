import os
import requests
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

ENDPOINT = os.getenv("SISCOM_ENDPOINT", "http://example.com/siscom")

bp = Blueprint("siscom", __name__, url_prefix="/api/siscom")


@bp.route("/pesquisar_ai", methods=["POST"])
@jwt_required()
def pesquisar_ai():
    data = request.get_json() or {}
    numero = data.get("numero") or data.get("auto_infracao")
    if not numero:
        return jsonify({"msg": "Número do AI não informado"}), 400

    response = requests.get(f"{ENDPOINT}/{numero}")
    response.raise_for_status()
    payload = response.json() if response.content else {}

    fields = [
        "numeroAuto",
        "codigoInfracao",
        "descAbreviadaInfracao",
        "placa",
        "renavam",
        "kmInfracao",
        "municipioInfracao",
        "valorInfracao",
    ]
    result = {field: payload.get(field) for field in fields}
    return jsonify(result)
