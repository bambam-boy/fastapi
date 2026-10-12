from fastapi import FastAPI
from app.core.config import settings
from app.api.api_router import router

app=FastAPI(
    title=settings.PROJECT_TITLE,
    openapi_url=f"{settings.API_PATH}/openapi.json"
)


app.include_router(router,prefix=settings.API_PATH)


