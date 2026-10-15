from fastapi import FastAPI
from app.core.config import settings
from app.api.api_router import router
from redis_fastapi import FastAPIRedis


app=FastAPI(
    title=settings.PROJECT_TITLE,
    openapi_url=f"{settings.API_PATH}/openapi.json"
)

FastAPIRedis(app).lifespan().caching().rate_limiting()

app.include_router(router,prefix=settings.API_PATH)


