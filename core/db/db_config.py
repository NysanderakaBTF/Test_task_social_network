from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

from core.config import config

async_engine = create_async_engine(
    config.DB_URL,
    pool_recycle=3600
)

async_sesison_factory = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sesison_factory() as session:
        yield session


@asynccontextmanager
async def provide_session():
    async with async_sesison_factory() as session:
        try:
            yield session
            await session.commit()
            await session.close()
        except:
            await session.rollback()
            raise

sync_engine = create_engine(config.DB_SYNC_URL)
sync_session = scoped_session(sessionmaker(bind=sync_engine))

Base = declarative_base()




