from flask import Blueprint, request, jsonify
from app.schemas.vinho import VinhoEntrada
from pydantic import ValidationError
from app.state.validados import dados_validados


bp = Blueprint("routes", __name__)

@bp.route("/vinhos", methods=["POST"])
def receber_vinho():
    payload = request.json
    try:
        vinho = VinhoEntrada(**payload)
        return jsonify({"status": "ok", "data": vinho.dict()})
    except ValidationError as e:
        return jsonify({"status": "erro", "detalhes": e.errors()}), 400


@bp.route("/dados-validos", methods=["GET"])
def get_dados_validados():
    retorno = {}
    for chave, lista in dados_validados.items():
        retorno[chave] = [item.dict() for item in lista]
    return jsonify(retorno)