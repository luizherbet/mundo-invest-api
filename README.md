# mundo-invest-api

API interna do Mundo Invest para gestão de clientes e integração simulada com Pipefy (GraphQL).

A integração com o Pipefy é **simulada**: a aplicação monta as mutations no formato esperado pela documentação e registra/loga o payload. A persistência e regras de negócio rodam localmente usando SQLite.

## Status

Projeto em construção.

## Stack (prevista)

- Python 3.11+
- FastAPI
- SQLAlchemy (SQLite)
- pytest

## Instalação local

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Executar a API

```bash
uvicorn app.main:app --reload --port 8001
```

- Swagger: http://127.0.0.1:8001/docs
- OpenAPI: http://127.0.0.1:8001/openapi.json

## Banco de dados

SQLite local: arquivo `mundo_invest.db` na raiz (ignorado pelo Git).

As tabelas são criadas via `init_db()` no startup da aplicação.

## Endpoints

### 1) Criar cliente

**POST** `/clientes`

Payload de exemplo (enunciado):

```bash
curl -X POST "http://127.0.0.1:8001/clientes" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_nome": "João Silva",
    "cliente_email": "joao.silva@example.com",
    "tipo_solicitacao": "Atualização cadastral",
    "valor_patrimonio": 250000
  }'
```

### 2) Webhook Pipefy (simulado)

**POST** `/webhooks/pipefy/card-updated`

```bash
curl -X POST "http://127.0.0.1:8001/webhooks/pipefy/card-updated" \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt_123",
    "card_id": "card_456",
    "cliente_email": "joao.silva@example.com",
    "timestamp": "2026-05-18T12:00:00Z"
  }'
```

- **Idempotência**: se o mesmo `event_id` for enviado novamente, a API não reprocessa.

## Testes

```bash
pytest -q
```

Testes cobrem os requisitos do desafio:

- Criação de cliente com payload válido e persistência no banco
- Processamento do webhook aplicando regra de prioridade (>= 200k alta; < 200k normal) e status `"Processado"`
- Bloqueio por `event_id` duplicado (idempotência)

## Onde estão as mutations GraphQL do Pipefy

As mutations e o payload de variáveis ficam em `app/services/pipefy_client.py`:

- `CREATE_CARD_MUTATION` (criação de card)
- `UPDATE_FIELDS_VALUES_MUTATION` (atualização de campos do card)

## Visão de produção (AWS) — sugestão

Uma forma de escalar essa arquitetura na AWS:

- **API Gateway + Lambda** para expor os endpoints HTTP
- **RDS (PostgreSQL)** para dados relacionais do cliente (ou DynamoDB, dependendo do modelo)
- **DynamoDB** (ou tabela no RDS) para idempotência de webhook (`event_id` como chave única)
- **SQS** para desacoplar o webhook do processamento (picos, retries, DLQ)
- **Lambda worker** consumindo fila e executando regras de negócio / integração Pipefy
- **Secrets Manager** para token/credenciais do Pipefy
- **CloudWatch Logs + Alarms** para observabilidade e alertas