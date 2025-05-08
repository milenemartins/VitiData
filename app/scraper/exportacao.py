import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from app.schemas.vinho import ComercioEntrada
from pydantic import ValidationError
from app.state.validados import dados_validados


def scrape_exportacao():

    sub_opc = 1
    resultados = []


    # Loop para acessar outras opções de exportação
    while sub_opc <= 4:
      print("Iniciando raspagem...\n")
      current_year = datetime.datetime.now().year
      sub_opc_str = str(sub_opc)
      base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&subopcao=subopt_0" + sub_opc_str +"&opcao=opt_06"


      # está criando um loop que percorre os anos de 1970 até o ano atual
      for ano in range(1970, current_year + 1):
          print(f"Raspando dados do ano {ano}...")

          # faz uma requisição para a URL que tem o ano formatado dentro dela.
          try:
              response = requests.get(base_url.format(ano=ano))
              response.raise_for_status()

          # Captura qualquer erro de rede e imprime uma mensagem de erro:
          except requests.RequestException as e:
              print(f"Erro ao acessar dados de {ano}: {e}")
              continue

          # Faz o parsing do HTML
          soup = BeautifulSoup(response.content, 'html.parser')

          # Tabela com informações de exportação
          table = soup.find('table', {'class': 'tb_base tb_dados'})

          # Tabela com nome das opções de exportação
          encontrar_opcoes = soup.find_all("table", {"class": "tb_base tb_header no_print"})

          # Caso não encontre a tabela retorna a seguinte mensagem:
          if not table:
              print(f"Sem dados disponíveis para o ano {ano}. Pulando...")
              continue

          # Caso não encontre a linha retorna a seguinte mensagem:
          rows = table.find_all('tr')

          if not rows:
              print(f"Nenhuma linha encontrada para o ano {ano}.")
              continue
          # Removendo o ultimo elemento da lista
          rows = rows[:-1]

          # Variavel para as categorias de exportações
          categoria = None

          # Percorrendo uma lista e pulando o primeiro elemento
          for i, row in enumerate(rows):
              if i == 0:
                  continue

              # Procurando linhas na tabela e extraindo os textos
              cols = row.find_all(['th', 'td'])
              dados = [col.get_text(strip=True) for col in cols]

              # Garantindo que a linha tenha 3 colunas
              if len(dados) == 3:
                  pais, quantidade, valor = dados

                  # Substituindo Valores de quantidade
                  if quantidade == "-":
                      quantidade = "0"

                  # Substituindo Valores de valor
                  if valor == "-":
                      valor = "0"

                  # Capturando nome das opções de exportações
                  for opcao in encontrar_opcoes:
                      nome_opcao = opcao.find("button", {"value": "subopt_0" + sub_opc_str}).text.strip()

                  # add valores em uma lista
                  resultados.append({
                      "ano": ano,
                      "categoria": nome_opcao,
                      "pais": pais,
                      "quantidade": quantidade,
                      "valor": valor
                  })
                  print(f"Ano: {ano} | Categoria: {nome_opcao} | País: {pais} | Quantidade: {quantidade} | Valor(US$): {valor}")
      sub_opc = sub_opc + 1
    print(f"Raspagem concluída. Total de registros: {len(resultados)}")
    return resultados


# ==== Validação separada ====
dados_export = scrape_exportacao()

validados = []

for item in dados_export:
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


dados_validados["exportacao"] = validados

# Salvar CSV
df = pd.DataFrame([v.dict() for v in validados])
df.to_csv("dadosExportacao.csv", index=False)