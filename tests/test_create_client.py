from app.models import STATUS_AGUARDANDO, Client


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