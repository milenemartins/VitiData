import requests
from bs4 import BeautifulSoup
from unicodedata import normalize, combining
import time


def normalizar_string(texto):
    texto_normalizado = normalize('NFKD', texto)

    # Substituições específicas
    substituicoes = {
        "º": "",          # remove símbolos no geral
        "“": "\"",
        "”": "\"",
        "–": "-",
        "°": ""
    }

    for caractere, novo in substituicoes.items():
        texto_normalizado = texto_normalizado.replace(caractere, novo)

    # Removendo acentos facilitando analises posteriores
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


def scrape_por_ano(ano="2023", opcao="opt_04"):
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opcao}"
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    registros = extrair_tabela(soup)
    return {
        "ano": ano,
        "total_registros": len(registros),
        "registros": registros
    }


def scrape_todos_os_anos(opcao="opt_04"):
    dados = []
    for ano in range(1970, 2024):
        print(f"Coletando {opcao} - {ano}")
        try:
            resultado = scrape_por_ano(str(ano), opcao)
        except Exception as e:
            print(f"Falha em {ano}: {e}")
            resultado = {"ano": str(ano), "registros": [],
                         "total_registros": 0}
        dados.append(resultado)
        time.sleep(0.5)
    return dados
