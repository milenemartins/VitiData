import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from app.schemas.vinho import ComercioEntrada
from pydantic import ValidationError
from app.state.validados import dados_validados


# Mapeamento de categorias e seus códigos no site
categorias = {
    "vinhosDeMesa": "subopt_01",
    "espumantes": "subopt_02",
    "uvasFrescas": "subopt_03",
    "uvasPassas": "subopt_04",
    "sucoDeUva": "subopt_05"
}

# Anos disponíveis no site
anoAtual = 2024
anoInicial = 1970


def iniciarDriver():
    options = Options()
    options.add_argument("--headless=new")  # novo modo headless
    options.add_argument("--disable-gpu")   # evita bugs no windows
    options.add_argument("--no-sandbox")    # necessário para alguns ambientes
    options.add_argument("--window-size=1920,1080")  # resolução da minha tela
    
    # Tive problemas com certificados no site da Embrapa
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--unsafely-treat-insecure-origin-as-secure=http://vitibrasil.cnpuv.embrapa.br")
    
    driver = webdriver.Chrome(options=options)
    return driver

def definirIntervaloAnos():
    print("\n📌 Escolha o intervalo de anos:")
    print("1 - Último ano (2024)")
    print("2 - Um ano específico")
    print("3 - Últimos 5 anos")
    print("4 - Últimos 10 anos")
    print("5 - Todos os anos (1970 a 2024)")  # para o dataset completo, mas demora beeeeeeem mais
    
    escolha = input("Digite o número da opção desejada: ")
    
    # Processamento da escolha
    if escolha == "1":
        return [anoAtual]
    elif escolha == "2":
        ano = int(input("Digite o ano desejado (ex: 2005): "))
        if ano < anoInicial or ano > anoAtual:
            raise ValueError("Ano fora do intervalo permitido.")
        return [ano]
    elif escolha == "3":
        return list(range(anoAtual - 4, anoAtual + 1))
    elif escolha == "4":
        return list(range(anoAtual - 9, anoAtual + 1))
    elif escolha == "5":
        # Pega todos os anos disponíveis
        return list(range(anoInicial, anoAtual + 1))
    else:
        raise ValueError("Opção inválida.")

def extrairPorCategoriaEAnos(driver, nomeCategoria, subopcao, anos):
    dadosColetados = []  # lista para armazenar os dados
    
    for ano in anos:
        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao={subopcao}"
        print(f"🔄 Coletando: {nomeCategoria} - {ano}")
        
        # Acessar a página
        driver.get(url)
        time.sleep(2)
        
        # Parse do HTML
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        # Localizar a tabela de dados
        tabela = soup.find("table", {"class": "tb_base tb_dados"})
        
        if not tabela:
            print(f"⚠️ Tabela não encontrada para {nomeCategoria} em {ano}")
            continue
        
        # Extrair dados das linhas
        linhas = tabela.find("tbody").find_all("tr")
        for linha in linhas:
            cels = linha.find_all("td")
            if len(cels) >= 3:
                pais = cels[0].text.strip()
                qtd = cels[1].text.strip()
                valor = cels[2].text.strip()
                
                # Adicionar à lista de resultados
                dadosColetados.append([ano, pais, qtd, valor])
    
    return dadosColetados

def salvarCsv(dados, nomeCategoria):
    
    # Criar diretório se não existir
    os.makedirs("dadosImportacao", exist_ok=True)
    nomeArquivo = f"dadosImportacao/{nomeCategoria}.csv"
    
    # Processar os dados antes de salvar
    dadosProcessados = []
    for row in dados:
        ano = int(row[0])
        pais = row[1]
        
        # Tratar a quantidade
        if row[2].strip() == '-' or not row[2].strip():
            quantidade = 0.0
        else:
            # Remover pontos de milhar e converter para float
            quantidade = row[2].replace('.', '')
            quantidade = float(quantidade.replace(',', '.'))
        
        # Tratar o valor
        if row[3].strip() == '-' or not row[3].strip():
            valor = 0.0 
        else:
            # Remover pontos de milhar e converter para float
            valor = row[3].replace('.', '')
            valor = float(valor.replace(',', '.'))
        
        # Adicionar a categoria aos dados
        dadosProcessados.append([ano, pais, nomeCategoria, quantidade, valor])
    
    # Escrever no arquivo
    with open(nomeArquivo, mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow([
            "Ano", 
            "PaisOrigem", 
            "CategoriaProtudo", 
            "QuantidadeKg", 
            "ValorUsd"
        ])
        writer.writerows(dadosProcessados)
    
    print(f"✅ CSV salvo: {nomeArquivo}")
    
    return len(dadosProcessados)

def coletarTudo():
    try:
        # Obter intervalo de anos desejado
        anosSelecionados = definirIntervaloAnos()
    except ValueError as erro:
        print(f"❌ Erro: {erro}")
        return
    
    # Iniciar o navegador
    chrome = iniciarDriver()
    
    # Para cada categoria, extrair dados
    for categoriaNome, codigo in categorias.items():
        # Extrair dados
        resultado = extrairPorCategoriaEAnos(chrome, categoriaNome, codigo, anosSelecionados)
        
        # Salvar resultados se houver dados
        if resultado:
            salvarCsv(resultado, categoriaNome)
        else:
            print(f"⚠️ Nenhum dado encontrado para: {categoriaNome}")
    
    # Fechar navegador
    chrome.quit()
    print("🏁 Finalizado!")
    
if __name__ == "__main__":
    try:
        # Obter intervalo de anos desejado
        anosSelecionados = definirIntervaloAnos()
    except ValueError as erro:
        print(f"❌ Erro: {erro}")
        exit()

    chrome = iniciarDriver()
    validados = []

    for categoriaNome, codigo in categorias.items():
        resultado = extrairPorCategoriaEAnos(chrome, categoriaNome, codigo, anosSelecionados)

        if resultado:
            salvarCsv(resultado, categoriaNome)
            
            
            # Validação Pydantic
            for row in resultado:
                try:
                    ano = int(row[0])
                    pais = row[1]

                    qtd_raw = row[2].strip().lower()
                    if qtd_raw in ["-", "nd", ""]:
                        quantidade = 0.0
                    else:
                        quantidade = float(qtd_raw.replace('.', '').replace(',', '.'))

                    val_raw = row[3].strip().lower()
                    if val_raw in ["-", "nd", ""]:
                        valor = 0.0
                    else:
                        valor = float(val_raw.replace('.', '').replace(',', '.'))

                    registro = {
                        "ano": ano,
                        "categoria": categoriaNome,
                        "pais": pais,
                        "quantidade": quantidade,
                        "valor": valor
                    }

                    item = ComercioEntrada(**registro)
                    validados.append(item)

                except ValidationError as e:
                    print(f"❌ Erro de validação para {categoriaNome} - {row}:\n{e}")

        else:
            print(f"⚠️ Nenhum dado encontrado para: {categoriaNome}")

    chrome.quit()
    print(f"🏁 Finalizado! Total de registros validados: {len(validados)}")

    dados_validados["importacao"] = validados
