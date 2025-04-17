from flask import Blueprint, jsonify
from app.services.scraper_generico_requests import scrape_todos_os_anos  

bp = Blueprint('routes', __name__)

@bp.route('/producao', methods=['GET'])
def producao_todos_anos():
    return jsonify(scrape_todos_os_anos("opt_02"))

@bp.route('/comercializacao', methods=['GET'])
def comercializacao_todos_anos():
    return jsonify(scrape_todos_os_anos("opt_04"))

