from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import WebhookCardUpdatedRequest, WebhookCardUpdatedResponse
from app.services.webhook_service import ClientNotFoundError, WebhookService

router = APIRouter(prefix="/webhooks/pipefy", tags=["webhooks"])


@router.post("/card-updated", response_model=WebhookCardUpdatedResponse)
def card_updated(
    payload: WebhookCardUpdatedRequest,
    db: Session = Depends(get_db),
) -> WebhookCardUpdatedResponse:
    service = WebhookService(db)
    try:
        return service.process_card_updated(payload)
    except ClientNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))