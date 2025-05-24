import os
import pytest
from config import Config  # substitua 'your_module' pelo nome do arquivo que contém a classe Config (sem .py)

@pytest.fixture(autouse=True)
def clear_env():
    # Limpa as variáveis de ambiente antes de cada teste
    keys = ["SECRET_KEY", "JWT_SECRET_KEY", "DATABASE_URL"]
    original_env = {key: os.environ.get(key) for key in keys}
    for key in keys:
        if key in os.environ:
            del os.environ[key]
    yield
    # Restaura as variáveis de ambiente após o teste
    for key, value in original_env.items():
        if value is not None:
            os.environ[key] = value
        elif key in os.environ:
            del os.environ[key]

def test_config_default_database_uri():
    # Quando DATABASE_URL não está setado, usa SQLite padrão
    config = Config()
    assert config.SECRET_KEY is None
    assert config.JWT_SECRET_KEY is None
    assert config.SQLALCHEMY_DATABASE_URI.startswith("sqlite:///")
    assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False

def test_config_env_variables_set(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "mysecret")
    monkeypatch.setenv("JWT_SECRET_KEY", "jwtsecret")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost/dbname")

    config = Config()

    assert config.SECRET_KEY == "mysecret"
    assert config.JWT_SECRET_KEY == "jwtsecret"
    assert config.SQLALCHEMY_DATABASE_URI == "postgresql://user:pass@localhost/dbname"
    assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False