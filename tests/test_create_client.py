from app.models import STATUS_AGUARDANDO, Client
from app.services.pipefy_client import (
    CREATE_CARD_MUTATION,
    PIPE_ID,
    build_create_card_payload,
)


def test_create_client_valid_payload_saves_to_database(client, db_session):
    payload = {
        "cliente_nome": "João Silva",
        "cliente_email": "joao.silva@example.com",
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": 250000,
    }

    response = client.post("/clientes", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["cliente_email"] == payload["cliente_email"]
    assert data["status"] == STATUS_AGUARDANDO

    saved = db_session.query(Client).filter(Client.email == payload["cliente_email"]).first()
    assert saved is not None
    assert saved.nome == payload["cliente_nome"]
    assert saved.status == STATUS_AGUARDANDO


def test_build_create_card_payload_matches_pipefy_create_card_shape():
    payload = build_create_card_payload(
        cliente_nome="João Silva",
        cliente_email="joao.silva@example.com",
        valor_patrimonio=250000,
    )

    assert payload["query"] == CREATE_CARD_MUTATION.strip()
    assert "createCard(input:" in payload["query"]
    assert "pipe_id: $pipeId" in payload["query"]
    assert 'field_id: "cliente_nome", field_value: $clienteNome' in payload["query"]
    assert 'field_id: "cliente_email", field_value: $clienteEmail' in payload["query"]
    assert 'field_id: "valor_patrimonio", field_value: $valorPatrimonio' in payload["query"]
    assert payload["variables"] == {
        "pipeId": PIPE_ID,
        "clienteNome": "João Silva",
        "clienteEmail": "joao.silva@example.com",
        "valorPatrimonio": "250000",
    }
