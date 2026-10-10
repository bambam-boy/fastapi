from fastapi import FastAPI
from app.core.config import settings

app=FastAPI(
    title=settings.PROJECT_TITLE,
    openapi_url=f"{settings.API_PATH}/openapi.json"
)


