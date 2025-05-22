import requests
from bs4 import BeautifulSoup
from unicodedata import normalize, combining
import pandas as pd
from app.schemas.vinho import VinhoEntrada
from pydantic import ValidationError
from app.state.validados import dados_validados


def normalizar_string(texto):
    texto_normalizado = normalize('NFKD', texto)
    substituicoes = {
        "º": "", "“": "\"", "”": "\"", "–": "-", "°": ""
    }
    for caractere, novo in substituicoes.items():
        texto_normalizado = texto_normalizado.replace(caractere, novo)
    return ''.join(c for c in texto_normalizado if not combining(c))


def scrape_comercializacao_page():
    print("Iniciando raspagem...\n")
    resultados = []
    base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04&ano={ano}"

    for ano in range(2023, 1999, -1):
        print(f"Raspando dados do ano {ano}...")
        response = requests.get(base_url.format(ano=ano))
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', {'class': 'tb_base tb_dados'})
        if not table:
            print(f"Sem dados disponíveis para o ano {ano}. Pulando...")
            continue

        rows = table.find_all('tr')
        if not rows:
            print(f"Nenhuma linha encontrada para o ano {ano}.")
            continue

        categoria = None
        rows = rows[:-1]

        for i, row in enumerate(rows):
            if i == 0:
                continue

            cols = row.find_all(['th', 'td'])
            dados = [col.get_text(strip=True) for col in cols]

            if len(dados) == 2:
                produto, quantidade = dados

                produto = normalizar_string(produto)

                if produto.isupper():
                    categoria = produto
                    print(f"Categoria encontrada: {categoria}")
                    continue

                if quantidade == "-":
                    quantidade = "0"

                tipo = f"{categoria} {produto}" if categoria else produto

                existe = any(
                    r["ano"] == ano and r["tipo"] == tipo
                    for r in resultados
                )
                if existe:
                    print(f"Registro duplicado: {ano}, {tipo}. Pulando...")
                    continue

                resultados.append({
                    "ano": ano,
                    "tipo": tipo,
                    "quantidade": quantidade
                })

                print(f"Ano: {ano} | Tipo: {tipo} | Quantidade: {quantidade}")

    print(f"\nRaspagem concluída. Total de registros: {len(resultados)}")
    return resultados


# Executa o scraper
dados_producao = scrape_comercializacao_page()

# Validação com Pydantic
validados = []

for item in dados_producao:
    try:
        qtd_raw = item["quantidade"].strip().lower()
        if qtd_raw in ["-", "nd", ""]:
            item["quantidade"] = 0.0
        else:
            item["quantidade"] = float(
                qtd_raw.replace('.', '').replace(',', '.'))

        validado = VinhoEntrada(**item)
        validados.append(validado)
    except ValidationError as e:
        print(f"❌ Erro de validação no registro: {item}\n{e}")


dados_validados["comercializacao"] = validados

# Salvar CSV
df = pd.DataFrame([v.model_dump() for v in validados])
df.to_csv("dadosComercializacao.csv", index=False)
