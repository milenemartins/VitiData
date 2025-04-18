import requests
from bs4 import BeautifulSoup
from .models import Vinho
from . import db
import datetime

# Lista de anos já raspados
years_scraped = []

def scrape_all_pages():
    """Realiza raspagem de dados da página da Embrapa de 3 anos atrás até 2000."""
    current_year = datetime.datetime.now().year
    start_year = current_year - 2
    base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02&ano={ano}"

    total_registros = 0  # Inicializa o contador de registros

    for ano in range(start_year, 1999, -1):  # Vai até 2000
        if ano in years_scraped:
            print(f"Ano {ano} já foi raspado, pulando...")
            continue  # Pula se já raspou esse ano

        print(f"Raspando dados do ano {ano}...")

        # Monta a URL com o parâmetro opcao=opt_02 fixo
        response = requests.get(base_url.format(ano=ano))
        soup = BeautifulSoup(response.content, 'html.parser')

        # Verifica se existe a tabela de produção
        table = soup.find('table', {'class': 'tb_base tb_dados'})
        if not table:
            print(f"Sem dados para o ano {ano}. Encerrando.")
            break

        rows = table.find_all('tr')

        if not rows:
            print(f"Nenhuma linha encontrada para {ano}.")
            continue

        categoria = None  # Categoria atual, começamos com None

        # Exclui a última linha (que é o total geral)
        rows = rows[:-1]

        for i, row in enumerate(rows):
            # Ignora a linha de cabeçalho (primeira linha)
            if i == 0:
                continue

            # Captura todas as colunas (th ou td)
            cols = row.find_all(['th', 'td'])
            dados = [col.get_text(strip=True) for col in cols]

            # Se a linha tem 2 colunas, processa
            if len(dados) == 2:
                produto, quantidade = dados

                # Se o produto está em maiúsculas, é uma linha de total (categoria)
                if produto.isupper():
                    categoria = produto  # Define a categoria
                    print(f"Categoria encontrada: {categoria}")
                    continue  # Pula para a próxima linha (não salva os totais)

                # Trata os valores "-" como 0
                if quantidade == "-":
                    quantidade = "0"

                # Combina o nome da categoria com o subtipo
                tipo = f"{categoria} {produto}" if categoria else produto

                # Verifica se o vinho já existe (para evitar duplicação)
                existing_vinho = Vinho.query.filter_by(ano=ano, tipo=tipo).first()
                if existing_vinho:
                    print(f"Vinho de {ano} e tipo '{tipo}' já existe no banco. Pulando...")
                    continue  # Pula se já existe

                # Adiciona o registro no banco
                vinho = Vinho(ano=ano, tipo=tipo, quantidade=quantidade)
                db.session.add(vinho)

        db.session.commit()  # Efetiva as inserções no banco
        print(f"Ano {ano}: {len(rows)} registros processados.")

        # Atualiza o contador total de registros
        total_registros += len(rows)
        years_scraped.append(ano)  # Cacheia o ano raspado

    # Exibe o total de registros inseridos
    print(f"Total de registros inseridos: {total_registros}")
    return Vinho.query.all()
