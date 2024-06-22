import logging
import contextlib
from typing import Any, AsyncIterator

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    create_async_engine,
)

from core.config import settings


@as_declarative()
class Base:
    """
    Base class for all SQLAlchemy models in this application.

    This class provides the following features:

    * Automatic table name generation based
        on the class name (lowercase with an 's' suffix).

    * Standardized metadata management using a shared DeclarativeMeta class.

    Do not instantiate this class directly; use child classes instead.
    """

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generates the table name for a child class based on its name.

        Returns:
            str: The table name with lowercase name and 's' suffix.
        """
        return f"{cls.__name__.lower()}s"

    def dict(self, exclude_none=True):
        return {
            key: value
            for key, value in self.__dict__.items()
            if value is not None and key not in ('_sa_instance_state')
        }

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_sa_instance_state']
        # del state['password']  # Exclude password for safety
        return state


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = sessionmaker(
            autocommit=False, bind=self._engine, class_=AsyncSession)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception as exc:
                await connection.rollback()
                raise exc

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception as exc:
            await session.rollback()
            raise exc
        finally:
            await session.close()


AsyncDatabaseManager = DatabaseSessionManager(
    host=str(settings.DATABASE_URI),
    engine_kwargs={"echo": settings.DATABASE_ECHO,
                   # "poolclass": NullPool})
                   "pool_size": 5})


async def get_async_db_session() -> AsyncSession:
    async with AsyncDatabaseManager.session() as session:
        yield session


async def init_database():
    """
    Creates database tables if they don't exist.

    This should be called within a lifespan event for optimal timing.
    """
    async with AsyncDatabaseManager._engine.begin() as session:
        session: AsyncSession
        await session.run_sync(Base.metadata.create_all)
        logging.info("Database tables created successfully!")
