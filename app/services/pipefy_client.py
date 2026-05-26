import json
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

# IDs de exemplo — em produção viriam de variáveis de ambiente
PIPE_ID = "123456"
FIELD_CLIENTE_NOME = "cliente_nome"
FIELD_CLIENTE_EMAIL = "cliente_email"
FIELD_VALOR_PATRIMONIO = "valor_patrimonio"
FIELD_STATUS_CLIENTE = "status_cliente"
FIELD_PRIORIDADE = "prioridade"

CREATE_CARD_MUTATION = """
mutation CreateCard(
  $pipeId: ID!
  $clienteNome: String!
  $clienteEmail: String!
  $valorPatrimonio: String!
) {
  createCard(input: {
    pipe_id: $pipeId
    fields_attributes: [
      { field_id: "cliente_nome", field_value: $clienteNome }
      { field_id: "cliente_email", field_value: $clienteEmail }
      { field_id: "valor_patrimonio", field_value: $valorPatrimonio }
    ]
  }) {
    card {
      id
    }
  }
}
"""

UPDATE_FIELDS_VALUES_MUTATION = """
mutation UpdateFieldsValues($nodeId: ID!, $values: [NodeFieldValueInput!]!) {
  updateFieldsValues(input: { nodeId: $nodeId, values: $values }) {
    success
    userErrors {
      field
      message
    }
  }
}
"""


def build_create_card_payload(
    *,
    cliente_nome: str,
    cliente_email: str,
    valor_patrimonio: Decimal | float | int,
    pipe_id: str = PIPE_ID,
) -> dict:
    """Monta mutation + variables para createCard (doc Pipefy)."""
    variables = {
        "pipeId": pipe_id,
        "clienteNome": cliente_nome,
        "clienteEmail": cliente_email,
        "valorPatrimonio": str(valor_patrimonio),
    }
    return {
        "query": CREATE_CARD_MUTATION.strip(),
        "variables": variables,
    }


def build_update_card_payload(
    *,
    card_id: str,
    status: str,
    prioridade: str,
) -> dict:
    """Monta mutation + variables para updateFieldsValues (doc Pipefy)."""
    variables = {
        "nodeId": card_id,
        "values": [
            {"fieldId": FIELD_STATUS_CLIENTE, "value": status},
            {"fieldId": FIELD_PRIORIDADE, "value": prioridade},
        ],
    }
    return {
        "query": UPDATE_FIELDS_VALUES_MUTATION.strip(),
        "variables": variables,
    }


def simulate_pipefy_request(payload: dict, operation: str) -> None:
    """
    Simula envio ao Pipefy: não chama API real.
    Persistência fica no banco local; aqui só loga o payload GraphQL.
    """
    logger.info(
        "[Pipefy simulado] operação=%s payload=%s",
        operation,
        json.dumps(payload, ensure_ascii=False),
    )