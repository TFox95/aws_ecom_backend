import logging
from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Select
from scope.auth.models import User

from core.config import settings
from core.database import (
    AsyncSession,
    get_async_db_session,
)


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

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


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Log the exception
    logging.error(f"Unhandled exception: {exc}")

    # Return a generic error response
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal Server Error"},
    )


@app.get("/")
async def basci(db: AsyncSession = Depends(get_async_db_session)):
    saved = await db.execute(Select(User))
    return saved
