from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from ..services.veiculo_client import VeiculoClient
from ..utils import strip_strings

bp = Blueprint("veiculo", __name__, url_prefix="/api/veiculo")


@bp.route("/placa", methods=["POST"])
@jwt_required()
def consultar_por_placa():
    data = strip_strings(request.get_json() or {})
    placa = data.get("placa")
    if not placa:
        return jsonify({"msg": "Placa não informada"}), 400

    client = VeiculoClient()
    result = client.consultar_placa(placa)
    return jsonify(result)
