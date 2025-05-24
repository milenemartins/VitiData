import pytest
from unittest.mock import patch, MagicMock
from app.scraper import scrape_producao_pages
from app.schemas.vinho import VinhoEntrada
import pandas as pd
from app.scraper.producao import scrape_producao_pages  # ajuste para seu módulo real
from app.state.validados import dados_validados


HTML_MOCK = """
<html>
  <body>
    <table class="tb_base tb_dados">
      <tr><th>Produto</th><th>Quantidade</th></tr>
      <tr><td>VINHO DE MESA</td><td></td></tr>
      <tr><td>Suco</td><td>1.000</td></tr>
      <tr><td>Vinho Tinto</td><td>500</td></tr>
      <tr><td>Última linha ignorada</td><td>0</td></tr>
    </table>
  </body>
</html>
"""

@patch("app.scraper.producao.requests.get")
@patch("pandas.DataFrame.to_csv")  # Patch global do método to_csv do pandas
def test_scrape_producao_pages(mock_to_csv, mock_get):
    mock_response = MagicMock()
    mock_response.content = HTML_MOCK.encode("utf-8")
    mock_get.return_value = mock_response

    resultado = scrape_producao_pages()

    assert isinstance(resultado, list)
    assert len(resultado) > 0

    # Verifica os campos do primeiro item
    primeiro = resultado[0]
    assert "ano" in primeiro
    assert "tipo" in primeiro
    assert "quantidade" in primeiro

    # Valida contra o schema
    VinhoEntrada(**primeiro)

    # Verifica que os dados foram salvos no dicionário compartilhado
    assert "producao" in dados_validados
    assert isinstance(dados_validados["producao"], list)

    # Certifica-se que o arquivo CSV *não* foi salvo de fato
    mock_to_csv.assert_called_once()