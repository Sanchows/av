from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import settings


engine = create_async_engine(
    url=f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
    echo=False,
)

async_session = sessionmaker(engine, class_=AsyncSession)  # type: ignore


@asynccontextmanager
async def get_session():
    """Dependency for getting async session"""

    async with async_session() as session:  # type: ignore
        yield session
