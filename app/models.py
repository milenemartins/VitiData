from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class WineData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(20), nullable=False)  # ex: producao, importacao…
    ano = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(100))
    pais = db.Column(db.String(100))
    quantidade = db.Column(db.Float, nullable=False)
    valor = db.Column(db.Float)  # nem todos os scrapers têm valor
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
