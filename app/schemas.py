from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# --- POST /clientes ---

class ClientCreate(BaseModel):
    """Payload de entrada do enunciado."""

    cliente_nome: str = Field(..., min_length=1, max_length=255)
    cliente_email: EmailStr
    tipo_solicitacao: str = Field(..., min_length=1, max_length=255)
    valor_patrimonio: Decimal = Field(..., gt=0)


class ClientResponse(BaseModel):
    """Resposta após criar ou consultar cliente."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_nome: str
    cliente_email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: Decimal
    status: str
    prioridade: str | None = None

    @classmethod
    def from_client(cls, client) -> "ClientResponse":
        """Converte o model SQLAlchemy (nome/email) para o JSON da API."""
        return cls(
            id=client.id,
            cliente_nome=client.nome,
            cliente_email=client.email,
            tipo_solicitacao=client.tipo_solicitacao,
            valor_patrimonio=client.valor_patrimonio,
            status=client.status,
            prioridade=client.prioridade,
        )


# --- POST /webhooks/pipefy/card-updated ---

class WebhookCardUpdatedRequest(BaseModel):
    """Payload do webhook simulado."""

    event_id: str = Field(..., min_length=1, max_length=255)
    card_id: str = Field(..., min_length=1, max_length=255)
    cliente_email: EmailStr
    timestamp: datetime


class WebhookCardUpdatedResponse(BaseModel):
    """Resposta do processamento do webhook."""

    message: str
    status: str | None = None
    prioridade: str | None = None
    cliente_email: EmailStr | None = None