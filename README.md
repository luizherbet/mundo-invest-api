# mundo-invest-api

API interna do Mundo Invest para gestão de clientes e integração simulada com Pipefy.

## Status

Projeto em construção.

## Stack (prevista)

- Python 3.11+
- FastAPI
- SQLAlchemy (SQLite)
- pytest

## Próximos passos

- Configurar dependências (`requirements.txt`)
- Implementar endpoints `POST /clientes` e `POST /webhooks/pipefy/card-updated`
- Testes automatizados

## Instalação local

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Banco de dados

SQLite local: arquivo `mundo_invest.db` na raiz (ignorado pelo Git).

As tabelas são criadas via `init_db()` na inicialização da API (commit futuro).