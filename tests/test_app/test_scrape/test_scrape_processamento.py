import pytest
from unittest.mock import patch, Mock
from app.scraper.processamento import scrape_all_processamento
import pandas as pd

def mock_requests_get_func(url, *args, **kwargs):
    import re
    match = re.search(r"ano=(\d+)", url)
    if not match:
        return Mock(status_code=404)

    ano = int(match.group(1))
    quantidade_map = {
        1999: "0,00",
        2000: "1.234,56",
        2001: "789,01",
    }
    quantidade = quantidade_map.get(ano, "0,00")

    html = f"""
    <html>
        <table class="tb_base tb_dados">
          <tr><th>TIPO</th><th>QUANTIDADE</th></tr>
          <tr><td>VINHO</td><td>{quantidade}</td></tr>
        </table>
    </html>
    """

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = html.encode("utf-8")
    return mock_response

@patch("app.scraper.processamento.requests.get")
@patch("pandas.DataFrame.to_csv")
def test_scrape_all_processamento(mock_to_csv, mock_requests_get):
    mock_requests_get.side_effect = mock_requests_get_func

    resultados = scrape_all_processamento(anos=[1999, 2000, 2001])

    assert isinstance(resultados, list)
    assert all(isinstance(item, dict) for item in resultados)

    qtds = [item["quantidade"] for item in resultados]
    assert qtds == [0.0, 1234.56, 789.01]
