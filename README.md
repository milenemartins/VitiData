# 📊 Scraper de Importação de Uvas e Derivados - Embrapa

Este projeto coleta automaticamente os dados da aba **Importação** do site da [Embrapa - Vitibrasil](http://vitibrasil.cnpuv.embrapa.br) para diferentes produtos derivados de uva, como vinhos, espumantes e sucos. Os dados são salvos em arquivos `.csv`, organizados por categoria e ano.

## 🔧 Tecnologias utilizadas

- Python 3.10+
- Selenium
- BeautifulSoup
- Pandas

## 📁 Estrutura do projeto

```
📦 dadosImportacao/
┣ 📄 vinhosDeMesa.csv
┣ 📄 espumantes.csv
...
📄 importacao_embrapa_final_estruturado.ipynb
📄 README.md
```

## 🚀 Como executar

1. Clone este repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o script Python (`.py`) ou utilize o Jupyter Notebook:

```bash
python importacao.py
```

ou abra no Jupyter:

```bash
jupyter notebook importacao_embrapa_final_estruturado.ipynb
```

## ✅ Opções de anos disponíveis

Ao rodar o script, você poderá escolher:

- `1` → Último ano (2024)
- `2` → Um ano específico (ex: 2015)
- `3` → Últimos 5 anos
- `4` → Últimos 10 anos
- `5` → Todos os anos (1970 a 2024)

## 📦 Produtos disponíveis

- Vinhos de Mesa
- Espumantes
- Uvas Frescas
- Uvas Passas
- Suco de Uva

## 📌 Observações

- O site da Embrapa utiliza HTTP e não HTTPS, por isso o navegador é configurado para aceitar conexões inseguras.
- O scraping é realizado com `Selenium` em modo headless.

---
# Scraping de Dados de Processamento da Embrapa

Este projeto realiza o scraping da página da Embrapa com dados de **uvas processadas no Rio Grande do Sul**, disponíveis no site do projeto VitiBrasil: [http://vitibrasil.cnpuv.embrapa.br/](http://vitibrasil.cnpuv.embrapa.br/).

Os dados coletados abrangem os anos de **1970 até o ano atual**, e são extraídos da aba "Processamento" (opção `opt_03` do site).

## 📁 Estrutura do Projeto

```
SCRAPING_PROCESSAMENTO/
├── env/                              # Ambiente virtual (não versionado)
├── dados_processamento_embrapa.csv  # Arquivo gerado com os dados raspados
├── processamento.ipynb              # Notebook com o código de scraping
├── requirements.txt                 # Lista de dependências do projeto
├── .gitignore                       # Arquivos/pastas ignorados pelo Git
└── README.md                        # Documentação do projeto
```

## ▶️ Como Executar

1. Clone o repositório ou baixe os arquivos.

2. Crie e ative o ambiente virtual:

   ```bash
   python -m venv env  # Criar ambiente virtual
   source env/bin/activate        # Ativar no Linux/Mac
   env\Scripts\activate         # Ativar no Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute o notebook `processamento.ipynb` no Jupyter ou no VS Code.

5. O arquivo `dados_processamento_embrapa.csv` será gerado automaticamente com os dados raspados.

## 🛠️ Tecnologias Utilizadas

- Python 3
- Jupyter Notebook
- BeautifulSoup4
- Requests
- Pandas
