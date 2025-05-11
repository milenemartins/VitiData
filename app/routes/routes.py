from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from app.models import WineData
from app import db
from app.scraper import (
    scrape_producao_pages,
    scrape_exportacao,
    scrape_all_processamento,
    scrape_importacao,
    scrape_comercializacao_page
)

ns = Namespace("wines", description="Operações de scraping e consulta de dados de vinho")

# Modelos para Swagger
scrape_model = ns.model("ScrapeRequest", {
    "pagina": fields.String(required=True, description="Categoria da página",
                            enum=["producao","processamento","comercializacao","importacao","exportacao"])
})
scrape_response = ns.model("ScrapeResponse", {
    "status": fields.String(),
    "pagina": fields.String(),
    "total": fields.Integer()
})

wine_model = ns.model("WineData", {
    "id": fields.Integer(),
    "categoria": fields.String(),
    "ano": fields.Integer(),
    "tipo": fields.String(),
    "pais": fields.String(),
    "quantidade": fields.Float(),
    "valor": fields.Float()
})

SCRAPERS = {
    "producao": scrape_producao_pages,
    "exportacao": scrape_exportacao,
    "processamento": scrape_all_processamento,
    "importacao": scrape_importacao,
    "comercializacao": scrape_comercializacao_page
}

@ns.route("/scrape")
class Scrape(Resource):
    @ns.expect(scrape_model, validate=True)
    @ns.response(200, "Dados raspados", scrape_response)
    @ns.response(400, "Categoria inválida")
    @jwt_required()
    def post(self):
        data = request.get_json()
        pagina = data["pagina"]
        if pagina not in SCRAPERS:
            ns.abort(400, "página inválida")
        items = SCRAPERS[pagina]()
        # (sua lógica de salvar no banco aqui)
        return {"status":"ok","pagina":pagina,"total":len(items)}, 200

@ns.route("")
class WineList(Resource):
    @ns.marshal_list_with(wine_model)
    @ns.response(200, "Lista retornada")
    @jwt_required()
    def get(self):
        q = WineData.query
        # (aplique filtros de query params)
        results = q.all()
        return results

@ns.route("/<int:id>")
@ns.param("id", "ID do registro")
class WineDetail(Resource):
    @ns.marshal_with(wine_model)
    @ns.response(200, "Registro encontrado")
    @ns.response(404, "Não encontrado")
    @jwt_required()
    def get(self, id):
        w = WineData.query.get_or_404(id)
        return w