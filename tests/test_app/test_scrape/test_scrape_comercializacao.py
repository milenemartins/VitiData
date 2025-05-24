import pytest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from app.schemas.vinho import VinhoEntrada
from app.scraper.comercializacao import scrape_comercializacao_page


HTML_MOCK = """
<html>
  <body>
    <table class="tb_base tb_dados">
      <tr><th>Produto</th><th>Quantidade</th></tr>
      <tr><td>VINHO DE MESA</td><td></td></tr>
      <tr><td>Tinto</td><td>1.234.567,89</td></tr>
      <tr><td>Branco</td><td>987.654,32</td></tr>
    </table>
  </body>
</html>
"""


@patch("app.scraper.comercializacao.requests.get")
def test_scrape_comercializacao_page(mock_get):
    mock_response = Mock()
    mock_response.content = HTML_MOCK
    mock_get.return_value = mock_response

    resultados = scrape_comercializacao_page(anos=[2023])

    print("\nRESULTADOS RASPADOS NO TESTE:")
    for r in resultados:
        print(r)

    assert isinstance(resultados, list)
    assert len(resultados) > 0

    item = resultados[0]
    assert item["ano"] == 2023
    assert item["tipo"] == "VINHO DE MESA Tinto"
    assert item["quantidade"] == "1.234.567,89"


def test_valida_vinho_entrada():
    dados = {
        "ano": 2023,
        "tipo": "TINTO SECO",
        "quantidade": "1.234,56"
    }
    dados["quantidade"] = float(dados["quantidade"].replace('.', '').replace(',', '.'))
    vinho = VinhoEntrada(**dados)
    
    assert vinho.ano == 2023
    assert vinho.tipo == "TINTO SECO"
    assert vinho.quantidade == 1234.56