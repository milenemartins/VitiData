# 🍇 Tech Challenge — API de Vitivinicultura da Embrapa

## 📌 Visão Geral

Este projeto faz parte do **Tech Challenge** da graduação em Engenharia de Machine Learning. O objetivo é desenvolver uma **API pública em Python** que realize web scraping no site da **Embrapa Uva e Vinho**, extraindo dados sobre vitivinicultura da aba **Produção**, e disponibilizando essas informações por meio de uma API REST.

A API será utilizada futuramente como fonte de dados para alimentar modelos de **Machine Learning**, sendo a primeira etapa de uma pipeline de ingestão e análise de dados.

---

## 🎯 Objetivos

- ✅ Criar uma API RESTful com **Flask**.
- ✅ Realizar scraping dos dados da aba "Produção" do site da Embrapa usando **BeautifulSoup**.
- ✅ Armazenar os dados raspados em um banco de dados local com **SQLAlchemy**.
- ✅ Utilizar **JWT (JSON Web Token)** para proteger rotas da API.
- ✅ Documentar a API com **Flasgger (Swagger UI)**.
- ✅ Realizar deploy local (e futuramente em produção).
- ✅ Criar um plano de arquitetura para ingestão e análise dos dados.

---

## 🔒 Segurança

- Utilização de sistema de **autenticação e login**.
- Geração de **tokens JWT** para acesso aos endpoints protegidos.
- Registro e login disponíveis por meio de rotas públicas.

---

## 📚 Endpoints Principais

### `/api/login` e `/api/register`
- Permite autenticação do usuário e geração de token JWT.

### `/api/vinhos`
- Lista os vinhos extraídos com filtros opcionais (`ano`, `tipo`).
- Protegido por JWT.
- Documentado no Swagger.

### `/api/scrape`
- Dispara a raspagem dos dados da aba **Produção**.
- Processa os dados de todos os anos disponíveis (do ano atual - 2 até 2000).
- Evita duplicações e mantém cache dos anos raspados.

---

## 🛠 Tecnologias Utilizadas

- `Python 3`
- `Flask`
- `SQLAlchemy`
- `BeautifulSoup`
- `Flasgger`
- `JWT (PyJWT)`
- `venv` (ambiente virtual)
- `Postman` (testes)
- `SQLite` (banco de dados local)

---

## 🚀 Plano de Deploy (MVP)

1. Raspagem automatizada dos dados da aba "Produção".
2. API local rodando com `run.py`.
3. Exportação do ambiente com `requirements.txt`.
4. Futuro deploy em plataformas como Render, Railway ou Heroku.
5. Integração com pipeline de ingestão de dados para Machine Learning.

---

## 📂 Estrutura de Pastas

```
/app
    │
    ├── __init__.py         # Configuração do app Flask
    ├── auth.py             # Lógica de autenticação
    ├── models.py           # Definição do banco de dados
    ├── routes.py           # Endpoints da API
    ├── scraper.py          # Lógica de web scraping
├── run.py              # Script de execução da aplicação
```

---

## 📄 Executando a Aplicação Localmente

```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente virtual
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar aplicação
python run.py
```

---

## 🔗 Documentação Swagger

Acesse a documentação automática da API através de:

```
http://localhost:5000/apidocs/
```