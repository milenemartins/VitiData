# test_wines_app.py

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Namespace, Resource, fields
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import pytest
from unittest.mock import patch

# -------------------------------
# App e configuração
# -------------------------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "test-secret"
app.config["TESTING"] = True

db = SQLAlchemy(app)
jwt = JWTManager(app)
api = Api(app)

# -------------------------------
# Modelo do banco
# -------------------------------
class WineData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50))
    ano = db.Column(db.Integer)
    tipo = db.Column(db.String(50))
    pais = db.Column(db.String(50))
    quantidade = db.Column(db.Float)
    valor = db.Column(db.Float)

# -------------------------------
# Namespace e rotas
# -------------------------------
ns = Namespace("wines", description="Operações com vinhos")

scrape_model = ns.model("ScrapeRequest", {
    "pagina": fields.String(required=True, enum=["producao","processamento","comercializacao","importacao","exportacao"])
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

# Mock SCRAPERS para os testes
SCRAPERS = {
    "producao": lambda: [{"ano": 2022, "tipo": "Tinto", "pais": "Brasil", "quantidade": 1000, "valor": 5000}],
    "exportacao": lambda: [],
    "processamento": lambda: [],
    "importacao": lambda: [],
    "comercializacao": lambda: []
}

@ns.route("/scrape")
class Scrape(Resource):
    @ns.expect(scrape_model)
    @ns.response(200, "Dados raspados", scrape_response)
    @ns.response(400, "Categoria inválida")
    @jwt_required()
    def post(self):
        data = request.get_json()
        pagina = data["pagina"]
        if pagina not in SCRAPERS:
            ns.abort(400, "página inválida")
        items = SCRAPERS[pagina]()
        WineData.query.filter_by(categoria=pagina).delete()
        for itm in items:
            db.session.add(WineData(
                categoria=pagina,
                ano=itm["ano"],
                tipo=itm["tipo"],
                pais=itm["pais"],
                quantidade=itm["quantidade"],
                valor=itm["valor"]
            ))
        db.session.commit()
        return {"status": "ok", "pagina": pagina, "total": len(items)}, 200

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

api.add_namespace(ns, path="/wines")

# -------------------------------
# Fixtures e testes com pytest
# -------------------------------
@pytest.fixture
def client():
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def auth_header():
    with app.app_context():
        token = create_access_token(identity="test_user")
        return {"Authorization": f"Bearer {token}"}

def test_scrape_success(client, auth_header):
    response = client.post("/wines/scrape", json={"pagina": "producao"}, headers=auth_header)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["pagina"] == "producao"
    assert data["total"] == 1

def test_scrape_invalid_category(client, auth_header):
    response = client.post("/wines/scrape", json={"pagina": "invalida"}, headers=auth_header)
    assert response.status_code == 400

def test_get_wine_list_filtered(client, auth_header):
    with app.app_context():
        db.session.add(WineData(categoria="producao", ano=2022, tipo="Tinto", pais="Brasil", quantidade=100, valor=200))
        db.session.commit()
    response = client.get("/wines?pagina=producao&ano=2022&vinho=tinto", headers=auth_header)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["categoria"] == "producao"

def test_get_wine_detail(client, auth_header):
    with app.app_context():
        wine = WineData(categoria="importacao", ano=2021, tipo="Branco", pais="Chile", quantidade=500, valor=1500)
        db.session.add(wine)
        db.session.commit()
        wine_id = wine.id
    response = client.get(f"/wines/{wine_id}", headers=auth_header)
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == wine_id
    assert data["tipo"] == "Branco"

def test_get_wine_detail_not_found(client, auth_header):
    response = client.get("/wines/999", headers=auth_header)
    assert response.status_code == 404
