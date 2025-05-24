import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask_jwt_extended import decode_token
from app import db, create_app
from app.auth import Register, Login
from werkzeug.security import check_password_hash

@pytest.fixture
def app():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "password": "testpassword"
    }

def test_register_user(client, user_data):
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    assert response.get_json()["msg"] == "usuário criado"

def test_register_existing_user(client, user_data):
    client.post("/auth/register", json=user_data)
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 409
    data = response.get_json()
    assert data["message"] == "Usuário já existe"

def test_login_valid_credentials(client, user_data):
    client.post("/auth/register", json=user_data)
    response = client.post("/auth/login", json=user_data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert "access_token" in json_data
    decoded = decode_token(json_data["access_token"])
    assert decoded["sub"] == user_data["username"]

def test_login_invalid_credentials(client, user_data):
    client.post("/auth/register", json=user_data)
    response = client.post("/auth/login", json={
        "username": user_data["username"],
        "password": "wrongpass"
    })  # <--- chave fechada aqui corretamente
    assert response.status_code == 401
    data = response.get_json()
    assert data["message"] == "Credenciais inválidas"