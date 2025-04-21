import requests
from bs4 import BeautifulSoup
from unicodedata import normalize, combining
import time

# Decidi remover acentos e sinais para facilitar anilises futuras


def normalizar_string(texto):
    texto_normalizado = normalize('NFKD', texto)

    substituicoes = {
        "º": "",
        "“": "\"",
        "”": "\"",
        "–": "-",
        "°": ""
    }

    for caractere, novo in substituicoes.items():
        texto_normalizado = texto_normalizado.replace(caractere, novo)

    return ''.join(c for c in texto_normalizado if not combining(c))


def extrair_tabela(soup):
    tabela = soup.find("table", class_="tb_base tb_dados")
    if not tabela:
        return []

    registros = []
    for row in tabela.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) == 2:
            produto = normalizar_string(cols[0].get_text(strip=True))
            quantidade = cols[1].get_text(strip=True)
            registros.append({
                "Produto": produto,
                "Quantidade (L.)": quantidade
            })
    return registros

# Coletando todos os anos para producao ou comercializacao


def scraper_todos_os_anos(opcao):
    dados = []
    for ano in range(1970, 2024):
        print(f"Coletando {opcao} - {ano}")
        try:
            url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opcao}"
            response = requests.get(url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, "html.parser")
            registros = extrair_tabela(soup)
            dados.append({
                "ano": str(ano),
                "total_registros": len(registros),
                "registros": registros
            })
        except Exception as e:
            print(f"Falha {ano}: {e}")
            dados.append({
                "ano": str(ano),
                "total_registros": 0,
                "registros": []
            })
        time.sleep(0.5)
    return dados
