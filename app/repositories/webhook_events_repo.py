from datetime import datetime

from sqlalchemy.orm import Session

from app.models import WebhookEvent


class WebhookEventsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def exists_by_event_id(self, event_id: str) -> bool:
        return (
            self.db.query(WebhookEvent)
            .filter(WebhookEvent.event_id == event_id)
            .first()
            is not None
        )

    def create(
        self,
        *,
        event_id: str,
        card_id: str,
        cliente_email: str,
        timestamp: datetime,
    ) -> WebhookEvent:
        event = WebhookEvent(
            event_id=event_id,
            card_id=card_id,
            cliente_email=cliente_email,
            timestamp=timestamp,
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event