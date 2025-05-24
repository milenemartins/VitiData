import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask import Flask
from app import db, create_app
from app.models import User, WineData
from datetime import datetime, UTC

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
def novo_usuario():
    return User(username="testeuser", password_hash="hash123")

@pytest.fixture
def novo_vinho():
    return WineData(
        categoria="producao",
        ano=2024,
        tipo="tinto",
        pais="Brasil",
        quantidade=1500.0,
        valor=32000.0,
        created_at=datetime.utcnow()
    )