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
    password = data.get('senha_autoprf')
    token = data.get('token_autoprf')
    if not password or not token:
        return jsonify({'msg': 'Credenciais inválidas'}), 400

    client = AutoPRFClient()
    session_token = client.login(user.cpf, password, token)

    user.autoprf_session = session_token
    db.session.commit()
    return jsonify({'session': session_token}), 200
