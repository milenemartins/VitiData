# VitiData API

## Visão Geral do Projeto

O **VitiData API** é uma aplicação desenvolvida como parte de um Tech Challenge da Embrapa. Seu objetivo é:

1. **Raspagem (web scraping)** dos dados de vitivinicultura nas cinco abas principais do site da Embrapa:

   * Produção
   * Processamento
   * Comercialização
   * Importação
   * Exportação
2. **API REST** em Python (Flask) para:

   * Acionar os scrapers de cada módulo
   * Persistir os dados em um banco SQL via SQLAlchemy
   * Consultar registros já coletados
3. **Autenticação** de usuários via JWT para proteger as rotas de scraping e consulta.
4. **Documentação automática** com Swagger UI, gerada pelo Flask‑RESTX.
5. **Script de limpeza** para remover caches e bancos antigos antes de iniciar a aplicação.

Os dados coletados ficam armazenados num banco SQLite (por padrão) e podem alimentar futuramente modelos de Machine Learning.

---

## Funcionalidades Principais

* **/auth/register** (POST): registra novo usuário.
* **/auth/login** (POST): faz login e retorna token JWT.
* **/wines/scrape** (POST): dispara a raspagem de uma das categorias (`producao`, `processamento`, `comercializacao`, `importacao`, `exportacao`).
* **/wines** (GET): lista registros, com filtros opcionais por `pagina`, `ano` e `vinho`.
* **/wines/{id}** (GET): detalha um registro específico.
* **/apidocs**: interface Swagger interativa para explorar todos os endpoints.
* **run.py --clean**: comando para apagar diretórios `__pycache__`, a pasta `instance/` e arquivos `.db` antes de iniciar a API.

---

## Estrutura de Pastas

```text
VitiData/
├── app/
│   ├── __init__.py        # App factory, init de DB, JWT e Swagger
│   ├── auth.py            # Namespace de autenticação (Flask-RESTX)
│   ├── models.py          # Models User e WineData (SQLAlchemy)
│   ├── routes/            # Namespace de scraping e consulta
│   │   └── routes.py
│   ├── scraper/           # Módulos de scraping por categoria
│   └── state/             # Estado em memória (validados)
├── run.py                 # Entry point e script de limpeza
│── config.py          # Configurações via .env
├── requirements.txt       # Dependências
└── README.md              # Documentação do projeto
```

---

## Instalação e Execução

1. **Clone** o repositório e entre na pasta:

   ```bash
   git clone <URL-do-repo>
   cd VitiData
   ```
2. **Virtualenv** e dependências:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate    # Windows
   pip install -r requirements.txt
   ```
3. **Variáveis de ambiente** (`.env` na raiz):

   ```ini
   SECRET_KEY=<chave-flask>
   JWT_SECRET_KEY=<chave-jwt>
   DATABASE_URL=sqlite:///app.db  # ou sua URI SQL
   ```
4. **Limpar caches** (opcional):

   ```bash
   python run.py --clean
   ```
5. **Rodar a API**:

   ```bash
   python run.py        # modo debug
   # ou
   flask run
   ```
6. **Acesse**:

   * **API Base:** `http://localhost:5000`
   * **Swagger UI:** `http://localhost:5000/apidocs/`

---

## Testes com Postman

1. Crie um **Environment** `Local API` com:

   * `base_url = http://localhost:5000`
   * `token = ` (vazio inicialmente)
2. Coleção **VitiData API** com requests:

   * **Register**: POST `{{base_url}}/auth/register`
   * **Login**: POST `{{base_url}}/auth/login` (salvar `{{token}}` via script de teste)
   * **Scrape Produção**: POST `{{base_url}}/wines/scrape` (body `{ "pagina":"producao" }`)
   * **List Wines**: GET `{{base_url}}/wines`
   * **Get Wine by ID**: GET `{{base_url}}/wines/{{id}}`
3. Use header `Authorization: Bearer {{token}}` nas rotas protegidas.
