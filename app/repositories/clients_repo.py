from sqlalchemy.orm import Session

from app.models import STATUS_AGUARDANDO, Client


class ClientsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> Client | None:
        return self.db.query(Client).filter(Client.email == email).first()

    def create(
        self,
        *,
        nome: str,
        email: str,
        tipo_solicitacao: str,
        valor_patrimonio,
    ) -> Client:
        client = Client(
            nome=nome,
            email=email,
            tipo_solicitacao=tipo_solicitacao,
            valor_patrimonio=valor_patrimonio,
            status=STATUS_AGUARDANDO,
        )
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def update_status_and_prioridade(
        self,
        client: Client,
        *,
        status: str,
        prioridade: str,
    ) -> Client:
        client.status = status
        client.prioridade = prioridade
        self.db.commit()
        self.db.refresh(client)
        return client