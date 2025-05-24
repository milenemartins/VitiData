import pytest
from unittest.mock import patch, MagicMock
from app.scraper.exportacao import scrape_exportacao  # ajuste o import conforme o nome do seu arquivo
from app.schemas.vinho import ComercioEntrada


MOCK_HTML = """
<table class="tb_base tb_dados">
  <tr><th>País</th><th>Quantidade</th><th>Valor</th></tr>
  <tr><td>Brasil</td><td>100</td><td>2000</td></tr>
  <tr><td>Argentina</td><td>-</td><td>1500</td></tr>
  <tr><td>Chile</td><td>300</td><td>-</td></tr>
  <tr><td>Rodapé</td><td>-</td><td>-</td></tr>
</table>
<table class="tb_base tb_header no_print">
  <tr><td><button value="subopt_01">Categoria Teste 1</button></td></tr>
  <tr><td><button value="subopt_02">Categoria Teste 2</button></td></tr>
  <tr><td><button value="subopt_03">Categoria Teste 3</button></td></tr>
  <tr><td><button value="subopt_04">Categoria Teste 4</button></td></tr>
</table>
"""

@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = MOCK_HTML.encode('utf-8')
        mock_get.return_value = mock_response
        yield mock_get

@pytest.fixture
def mock_comercio_entrada():
    with patch("app.schemas.vinho.ComercioEntrada") as mock_model:
        def side_effect(**kwargs):
            mock_instance = MagicMock()
            mock_instance.dict.return_value = kwargs
            return mock_instance
        mock_model.side_effect = side_effect
        yield mock_model

def test_scrape_exportacao_basic(mock_requests_get, mock_comercio_entrada):
    resultados = scrape_exportacao()
    
    print("RESULTADOS:", resultados)
    
    assert isinstance(resultados, list)
    assert len(resultados) > 0

    brasil = next((x for x in resultados if x["pais"] == "Brasil"), None)
    assert brasil is not None
    assert brasil["quantidade"] == 100.0
    assert brasil["valor"] == 2000.0

    argentina = next((x for x in resultados if x["pais"] == "Argentina"), None)
    assert argentina is not None
    assert argentina["quantidade"] == 0.0
    assert argentina["valor"] == 1500.0

    chile = next((x for x in resultados if x["pais"] == "Chile"), None)
    assert chile is not None
    assert chile["quantidade"] == 300.0
    assert chile["valor"] == 0.0