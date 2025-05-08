import requests
from bs4 import BeautifulSoup
from unicodedata import normalize, combining
import time
from pydantic import ValidationError
from app.schemas.vinho import ComercializacaoItem
from app.state.validados import dados_validados
import pandas as pd


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
                "produto": produto,
                "quantidade_litros": quantidade
            })
    return registros

def scrape_comercializacao_page():
    dados = []
    for ano in range(1970, 2024):
        print(f"Coletando comercialização - {ano}")
        try:
            url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_04"
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
    print(f"\nRaspagem finalizada. Total de anos: {len(dados)}")
    return dados


# ==== Validação ====

dados = scrape_comercializacao_page()

validados = []

for ano_bloco in dados:
    ano = ano_bloco["ano"]
    for registro in ano_bloco["registros"]:
        try:
            # Converte string para float antes da validação
            qtd_raw = registro["quantidade_litros"].strip().lower()
            if qtd_raw in ["-", "nd", ""]:
                registro["quantidade_litros"] = 0.0
            else:
                registro["quantidade_litros"] = float(qtd_raw.replace('.', '').replace(',', '.'))

            item = ComercializacaoItem(**registro)
            validados.append(item)
        except ValidationError as e:
            print(f"❌ Erro no ano {ano} com registro {registro}:\n{e}")    

dados_validados["comercializacao"] = validados

# Salvar CSV
df = pd.json_normalize(validados)
df.to_csv("dadosComercializacao.csv", index=False)
