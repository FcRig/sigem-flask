from flask import Blueprint, request, jsonify
from ..utils.scraping_utils import buscar_dados

bp = Blueprint('scraping', __name__, url_prefix='/api/scraping')

@bp.route('/dados', methods=['POST'])
def dados():
    url = request.json.get('url')
    result = buscar_dados(url)
    return jsonify(result)
