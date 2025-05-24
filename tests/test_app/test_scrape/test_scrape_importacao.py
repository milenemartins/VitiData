import pytest
from unittest.mock import Mock, patch, call, mock_open, MagicMock, ANY
import os
#import csv
from pathlib import Path
#from selenium.webdriver.chrome.options import Options
from pydantic import ValidationError
from app.schemas.vinho import ComercioEntrada
from app.state.validados import dados_validados




# Funções a serem testadas
from app.scraper.importacao import (
    normalizar_string,
    scrape_importacao,
    categorias
)



HTML_MOCK = """
<table class="tb_base tb_dados">
    <tr><th>País</th><th>Quantidade</th><th>Valor</th></tr>
    <tr><td>Chile</td><td>1.234,56</td><td>7.890,12</td></tr>
    <tr><td>Argentina</td><td>-</td><td>3.210,00</td></tr>
</table>
"""

@pytest.fixture
def mock_requests_get():
    with patch("app.scraper.importacao.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = HTML_MOCK.encode("utf-8")
        mock_get.return_value = mock_response
        yield mock_get

def test_scrape_importacao_basic(mock_requests_get):
    resultado = scrape_importacao()

    assert isinstance(resultado, list)
    assert len(resultado) > 0

    # Confirma que os dados estão validados corretamente
    for registro in resultado:
        assert isinstance(registro, dict)
        assert "ano" in registro
        assert "pais" in registro
        assert "quantidade" in registro
        assert isinstance(registro["quantidade"], float)
        assert "valor" in registro
        assert isinstance(registro["valor"], float)

    # Confirma que os dados foram salvos no estado global
    assert "importacao" in dados_validados
    assert all(isinstance(v, ComercioEntrada) for v in dados_validados["importacao"])
