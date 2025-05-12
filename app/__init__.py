from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restx import Api
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    api = Api(
        app,
        version="1.0",
        title="VitiData API",
        description="API para raspagem e consulta de dados de vitivinicultura da Embrapa",
        doc="/apidocs"
    )

    from app.auth import ns as auth_ns
    api.add_namespace(auth_ns, path="/auth")

    from app.routes.routes import ns as wines_ns
    api.add_namespace(wines_ns)
    
    with app.app_context():
        db.create_all()

    return app