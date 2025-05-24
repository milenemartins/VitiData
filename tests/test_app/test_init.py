import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_app_creation(app):
    assert app is not None
    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == 'sqlite:///:memory:'
    assert app.config["JWT_SECRET_KEY"] == "test-secret-key"

def test_health_check_route(client):
    response = client.get("/swagger.json")
    assert response.status_code == 200
    assert response.is_json
    
def test_swagger_json_available(client):
    response = client.get("/swagger.json")
    assert response.status_code == 200
    assert response.is_json
    
def test_routes_registered(app):
    routes = [str(rule) for rule in app.url_map.iter_rules()]
    assert "/auth/login" in routes
    assert "/wines" in routes
    assert "/swagger.json" in routes