import os
import pytest
from pathlib import Path
from run import clean_project, main

@pytest.fixture
def mock_project_structure(tmp_path):
    root = tmp_path

    # Cria __pycache__ em subdiretórios
    pycache_dir = root / "some_dir" / "__pycache__"
    pycache_dir.mkdir(parents=True)

    # Cria pasta instance
    instance_dir = root / "instance"
    instance_dir.mkdir()

    # Cria arquivos .db na raiz
    db_file = root / "test.db"
    db_file.write_text("fake-db")

    return {
        "root": root,
        "pycache_dir": pycache_dir,
        "instance_dir": instance_dir,
        "db_file": db_file
    }

def test_clean_project_removes_files_and_dirs(mock_project_structure, monkeypatch):
    paths = mock_project_structure
    root = paths["root"]

    # Mocka os.path.dirname(__file__) para retornar o tmp_path
    monkeypatch.setattr(os.path, "dirname", lambda _: str(root))

    # Mocka os.path.abspath para retornar o mesmo valor (evita saída da raiz simulada)
    monkeypatch.setattr(os.path, "abspath", lambda x: x)

    # Executa a função
    clean_project()

    # Verifica se __pycache__ foi removido
    assert not paths["pycache_dir"].exists()

    # Verifica se instance foi removido
    assert not paths["instance_dir"].exists()

    # Verifica se .db foi removido
    assert not paths["db_file"].exists()
