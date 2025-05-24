import requests
from bs4 import BeautifulSoup
from unicodedata import normalize, combining
import pandas as pd
from app.schemas.vinho import ComercioEntrada
from pydantic import ValidationError
from app.state.validados import dados_validados

# Mapeamento das categorias e seus códigos
categorias = {
    "vinhosDeMesa": "subopt_01",
    "espumantes": "subopt_02",
    "uvasFrescas": "subopt_03",
    "uvasPassas": "subopt_04",
    "sucoDeUva": "subopt_05"
}

def normalizar_string(texto):
    texto_normalizado = normalize('NFKD', texto)
    substituicoes = {
        "º": "", "“": "\"", "”": "\"", "–": "-", "°": ""
    }
    for caractere, novo in substituicoes.items():
        texto_normalizado = texto_normalizado.replace(caractere, novo)
    return ''.join(c for c in texto_normalizado if not combining(c))

def scrape_importacao():
    print("Iniciando raspagem de dados de importação...\n")
    resultados = []

    base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao={subopcao}"

    for categoria, subopcao in categorias.items():
        print(f"\n🔹 Categoria: {categoria}")

        for ano in range(2024, 1998, -1):
            print(f"Raspando dados do ano {ano}...")

            url = base_url.format(ano=ano, subopcao=subopcao)
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"❌ Erro ao acessar {url}: {e}")
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            tabela = soup.find("table", {"class": "tb_base tb_dados"})

            if not tabela:
                print(f"⚠️ Sem dados para {categoria} no ano {ano}. Pulando...")
                continue

            linhas = tabela.find_all("tr")
            if not linhas:
                print(f"⚠️ Nenhuma linha encontrada para {categoria} no ano {ano}. Pulando...")
                continue

            for linha in linhas[1:]:  # Ignorar cabeçalho
                colunas = linha.find_all("td")
                if len(colunas) < 3:
                    continue

                pais = normalizar_string(colunas[0].get_text(strip=True))
                quantidade = colunas[1].get_text(strip=True)
                valor = colunas[2].get_text(strip=True)

                resultados.append({
                    "ano": ano,
                    "categoria": categoria,
                    "pais": pais,
                    "quantidade": quantidade,
                    "valor": valor
                })

                print(f"Ano: {ano} | Categoria: {categoria} | País: {pais} | Quantidade: {quantidade} | Valor: {valor}")

    print(f"\nRaspagem concluída. Total de registros coletados: {len(resultados)}")

    # Validação e transformação
    validados = []

    for item in resultados:
        try:
            qtd_raw = item["quantidade"].strip().lower()
            if qtd_raw in ["-", "nd", ""]:
                item["quantidade"] = 0.0
            else:
                item["quantidade"] = float(qtd_raw.replace('.', '').replace(',', '.'))

            val_raw = item["valor"].strip().lower()
            if val_raw in ["-", "nd", ""]:
                item["valor"] = 0.0
            else:
                item["valor"] = float(val_raw.replace('.', '').replace(',', '.'))

            validado = ComercioEntrada(**item)
            validados.append(validado)
        except ValidationError as e:
            print(f"❌ Erro de validação no registro: {item}\n{e}")

    dados_validados["importacao"] = validados

    # Exportar para CSV
    df = pd.DataFrame([v.model_dump() for v in validados])
    df.to_csv("dadosImportacao.csv", index=False)

    print(f"✅ Arquivo CSV salvo: dadosImportacao.csv")
    print(f"✅ Total de registros validados: {len(validados)}")

    return [v.model_dump() for v in validados]

# Execução direta
if __name__ == "__main__":
    scrape_importacao()
