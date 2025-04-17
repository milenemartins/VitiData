from flask import Flask
from app.routes.routes import bp as routes_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'vitidata_protecao_api_2025'

    app.register_blueprint(routes_bp)

    return app
