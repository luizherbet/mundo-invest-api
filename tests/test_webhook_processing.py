from app.models import (
    PRIORIDADE_ALTA,
    PRIORIDADE_NORMAL,
    STATUS_PROCESSADO,
    Client,
    WebhookEvent,
)


def _create_client(client, *, email: str, valor_patrimonio: int):
  return client.post(
      "/clientes",
      json={
          "cliente_nome": "Cliente Teste",
          "cliente_email": email,
          "tipo_solicitacao": "Atualização cadastral",
          "valor_patrimonio": valor_patrimonio,
      },
  )


def _send_webhook(client, *, event_id: str, email: str):
    return client.post(
        "/webhooks/pipefy/card-updated",
        json={
            "event_id": event_id,
            "card_id": "card_456",
            "cliente_email": email,
            "timestamp": "2026-05-18T12:00:00Z",
        },
    )


def test_webhook_sets_prioridade_alta_when_patrimonio_gte_200k(client, db_session):
    email = "alta@example.com"
    _create_client(client, email=email, valor_patrimonio=250000)

    response = _send_webhook(client, event_id="evt_alta", email=email)

    assert response.status_code == 200
    data = response.json()
    assert data["prioridade"] == PRIORIDADE_ALTA
    assert data["status"] == STATUS_PROCESSADO

    saved = db_session.query(Client).filter(Client.email == email).first()
    assert saved.prioridade == PRIORIDADE_ALTA
    assert saved.status == STATUS_PROCESSADO


def test_webhook_sets_prioridade_normal_when_patrimonio_lt_200k(client, db_session):
    email = "normal@example.com"
    _create_client(client, email=email, valor_patrimonio=150000)

    response = _send_webhook(client, event_id="evt_normal", email=email)

    assert response.status_code == 200
    data = response.json()
    assert data["prioridade"] == PRIORIDADE_NORMAL
    assert data["status"] == STATUS_PROCESSADO

    saved = db_session.query(Client).filter(Client.email == email).first()
    assert saved.prioridade == PRIORIDADE_NORMAL
    assert saved.status == STATUS_PROCESSADO


def test_webhook_blocks_duplicate_event_id(client, db_session):
    email = "dup@example.com"
    _create_client(client, email=email, valor_patrimonio=250000)

    first = _send_webhook(client, event_id="evt_dup", email=email)
    second = _send_webhook(client, event_id="evt_dup", email=email)

    assert first.status_code == 200
    assert first.json()["message"] == "evento processado com sucesso"

    assert second.status_code == 200
    assert second.json()["message"] == "evento já processado"

    events = db_session.query(WebhookEvent).filter(WebhookEvent.event_id == "evt_dup").all()
    assert len(events) == 1