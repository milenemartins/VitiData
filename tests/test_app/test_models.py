import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from datetime import datetime
from app import db
from app.models import User, WineData

@pytest.fixture
def novo_usuario():
    return User(username="teste_user", password_hash="hash123")

@pytest.fixture
def novo_vinho():
    return WineData(
        categoria="producao",
        ano=2023,
        tipo="tinto",
        pais="Brasil",
        quantidade=1500.0,
        valor=20000.0,
        created_at=datetime.utcnow()
    )

def test_cria_usuario(novo_usuario):
    assert novo_usuario.username == "teste_user"
    assert novo_usuario.password_hash == "hash123"

def test_cria_vinho(novo_vinho):
    assert novo_vinho.categoria == "producao"
    assert novo_vinho.ano == 2023
    assert novo_vinho.tipo == "tinto"
    assert novo_vinho.pais == "Brasil"
    assert novo_vinho.quantidade == 1500.0
    assert novo_vinho.valor == 20000.0
    assert isinstance(novo_vinho.created_at, datetime)

def test_salva_no_banco(app, novo_usuario, novo_vinho):
    db.session.add(novo_usuario)
    db.session.add(novo_vinho)
    db.session.commit()

    assert User.query.filter_by(username="teste_user").first() is not None
    assert WineData.query.filter_by(categoria="producao").first() is not None