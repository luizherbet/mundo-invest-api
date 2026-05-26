from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import (
    PRIORIDADE_ALTA,
    PRIORIDADE_NORMAL,
    STATUS_PROCESSADO,
)
from app.repositories.clients_repo import ClientsRepository
from app.repositories.webhook_events_repo import WebhookEventsRepository
from app.schemas import WebhookCardUpdatedRequest, WebhookCardUpdatedResponse
from app.services.pipefy_client import (
    build_update_card_payload,
    simulate_pipefy_request,
)

PATRIMONIO_LIMITE_PRIORIDADE_ALTA = Decimal("200000")


class ClientNotFoundError(Exception):
    """Cliente não encontrado pelo e-mail do webhook."""


class WebhookService:
    def __init__(self, db: Session) -> None:
        self.clients_repo = ClientsRepository(db)
        self.events_repo = WebhookEventsRepository(db)

    def _calcular_prioridade(self, valor_patrimonio) -> str:
        if Decimal(str(valor_patrimonio)) >= PATRIMONIO_LIMITE_PRIORIDADE_ALTA:
            return PRIORIDADE_ALTA
        return PRIORIDADE_NORMAL

    def process_card_updated(
        self, data: WebhookCardUpdatedRequest
    ) -> WebhookCardUpdatedResponse:
        email = str(data.cliente_email)

        if self.events_repo.exists_by_event_id(data.event_id):
            return WebhookCardUpdatedResponse(
                message="evento já processado",
                cliente_email=email,
            )

        client = self.clients_repo.get_by_email(email)
        if not client:
            raise ClientNotFoundError(f"Cliente com e-mail {email} não encontrado.")

        prioridade = self._calcular_prioridade(client.valor_patrimonio)

        self.clients_repo.update_status_and_prioridade(
            client,
            status=STATUS_PROCESSADO,
            prioridade=prioridade,
        )

        payload = build_update_card_payload(
            card_id=data.card_id,
            status=STATUS_PROCESSADO,
            prioridade=prioridade,
        )
        simulate_pipefy_request(payload, operation="updateFieldsValues")

        self.events_repo.create(
            event_id=data.event_id,
            card_id=data.card_id,
            cliente_email=email,
            timestamp=data.timestamp,
        )

        return WebhookCardUpdatedResponse(
            message="evento processado com sucesso",
            status=STATUS_PROCESSADO,
            prioridade=prioridade,
            cliente_email=email,
        )