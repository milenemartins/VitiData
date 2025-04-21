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
