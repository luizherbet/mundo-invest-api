from sqlalchemy.orm import Session

from app.models import Client
from app.repositories.clients_repo import ClientsRepository
from app.schemas import ClientCreate, ClientResponse
from app.services.pipefy_client import (
    build_create_card_payload,
    simulate_pipefy_request,
)


class ClientAlreadyExistsError(Exception):
    """E-mail já cadastrado."""


class ClientsService:
    def __init__(self, db: Session) -> None:
        self.repo = ClientsRepository(db)

    def create_client(self, data: ClientCreate) -> ClientResponse:
        email = str(data.cliente_email)

        if self.repo.get_by_email(email):
            raise ClientAlreadyExistsError(f"Cliente com e-mail {email} já existe.")

        client = self.repo.create(
            nome=data.cliente_nome,
            email=email,
            tipo_solicitacao=data.tipo_solicitacao,
            valor_patrimonio=data.valor_patrimonio,
        )

        payload = build_create_card_payload(
            cliente_nome=data.cliente_nome,
            cliente_email=email,
            valor_patrimonio=data.valor_patrimonio,
        )
        simulate_pipefy_request(payload, operation="createCard")

        return ClientResponse.from_client(client)