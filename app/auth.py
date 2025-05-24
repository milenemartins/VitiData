from flask_restx import Namespace, Resource, fields
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import db
from app.models import User

# namespace para auth
ns = Namespace("auth", description="Autenticação de usuários")

# modelo de entrada (payload) para Swagger
user_model = ns.model("UserLogin", {
    "username": fields.String(required=True, description="Nome do usuário"),
    "password": fields.String(required=True, description="Senha")
})

# rota /auth/register
@ns.route("/register")
class Register(Resource):
    @ns.expect(user_model, validate=True)
    @ns.response(201, "Usuário criado")
    @ns.response(409, "Usuário já existe")
    def post(self):
        data = request.get_json()
        if User.query.filter_by(username=data["username"]).first():
            ns.abort(409, "Usuário já existe")
        user = User(
            username=data["username"],
            password_hash=generate_password_hash(data["password"])
        )
        db.session.add(user)
        db.session.commit()
        return {"msg":"usuário criado"}, 201

# rota /auth/login
@ns.route("/login")
class Login(Resource):
    @ns.expect(user_model, validate=True)
    @ns.response(200, "Login bem-sucedido", model=ns.model("Token", {
        "access_token": fields.String()
    }))
    @ns.response(401, "Credenciais inválidas")
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data["username"]).first()
        if not user or not check_password_hash(user.password_hash, data["password"]):
            ns.abort(401, "Credenciais inválidas")
        token = create_access_token(identity=user.username)
        return {"access_token": token}, 200
