from mangum import Mangum
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import Select
from auth.models import User

from core.config import settings
from core.database import (
    AsyncDatabaseManager,
    AsyncSession,
    init_database,
    get_async_db_session,
)


@asynccontextmanager
async def async_db_lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    try:
        await init_database()
        yield
    except Exception as exc:
        raise exc
    finally:
        if AsyncDatabaseManager._engine is not None:
            # Close the DB connection
            await AsyncDatabaseManager.close()


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME, lifespan=async_db_lifespan)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
handler = Mangum(app=app, lifespan="auto")

@app.get("/")
async def basci(db: AsyncSession = Depends(get_async_db_session)):
    saved = await db.execute(Select(User))
    return saved
