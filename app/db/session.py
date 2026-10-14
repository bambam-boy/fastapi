from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from app.core.config import settings


engine=create_async_engine(settings.SQLALCHEMY_URL_ASYNC)
asyncsession=async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False,
    class_=AsyncSession)


async def get_session():
    async with asyncsession() as session:
        yield session