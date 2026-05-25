from datetime import datetime

from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

STATUS_AGUARDANDO = "Aguardando Análise"
STATUS_PROCESSADO = "Processado"

PRIORIDADE_ALTA = "prioridade_alta"
PRIORIDADE_NORMAL = "prioridade_normal"


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    tipo_solicitacao: Mapped[str] = mapped_column(String(255), nullable=False)
    valor_patrimonio: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=STATUS_AGUARDANDO
    )
    prioridade: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    card_id: Mapped[str] = mapped_column(String(255), nullable=False)
    cliente_email: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )