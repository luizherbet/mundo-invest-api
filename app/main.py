from fastapi import FastAPI

from app.api.clients import router as clients_router
from app.api.webhooks import router as webhooks_router
from app.db import init_db

app = FastAPI(title="mundo-invest-api")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


app.include_router(clients_router)
app.include_router(webhooks_router)