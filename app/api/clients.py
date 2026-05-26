from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import ClientCreate, ClientResponse
from app.services.clients_service import (
    ClientsService,
    ClientAlreadyExistsError,
)

router = APIRouter(tags=["clients"])


@router.post("/clientes", response_model=ClientResponse, status_code=201)
def create_client(
    payload: ClientCreate,
    db: Session = Depends(get_db),
) -> ClientResponse:
    service = ClientsService(db)
    try:
        return service.create_client(payload)
    except ClientAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))