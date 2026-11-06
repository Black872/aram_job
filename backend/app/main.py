from fastapi import FastAPI
from sqlalchemy import text

from app.api.applications import router as applications_router
from app.core.config import settings
from app.db.session import engine

app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
    description="Self-hosted AI job application tracking and email intelligence.",
)

app.include_router(applications_router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "service": "aram-api", "version": "0.2.0"}


@app.get("/health/ready", tags=["system"])
def readiness():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ready", "database": "connected"}
