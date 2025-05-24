from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app import db
from app.models import WineData
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
        # persiste no banco
        WineData.query.filter_by(categoria=pagina).delete()
        for itm in items:
            w = WineData(
                categoria=pagina,
                ano=itm.get("ano"),
                tipo=itm.get("tipo"),
                pais=itm.get("pais"),
                quantidade=itm.get("quantidade"),
                valor=itm.get("valor")
            )
            db.session.add(w)
        db.session.commit()
        return {"status":"ok","pagina":pagina,"total":len(items)}, 200

@ns.route("")
class WineList(Resource):
    @ns.marshal_list_with(wine_model)
    @jwt_required()
    def get(self):
        q = WineData.query
        pagina = request.args.get("pagina")
        ano = request.args.get("ano", type=int)
        vinho = request.args.get("vinho")
        if pagina:
            q = q.filter_by(categoria=pagina)
        if ano:
            q = q.filter_by(ano=ano)
        if vinho:
            q = q.filter(WineData.tipo.ilike(f"%{vinho}%"))
        return q.all()

@ns.route("/<int:id>")
@ns.param("id", "ID do registro")
class WineDetail(Resource):
    @ns.marshal_with(wine_model)
    @ns.response(404, "Não encontrado")
    @jwt_required()
    def get(self, id):
        return WineData.query.get_or_404(id)