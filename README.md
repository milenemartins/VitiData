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