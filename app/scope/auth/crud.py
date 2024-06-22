from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import AsyncDatabaseManager, get_async_db_session



async def get_user_by_id(db: AsyncSession, id: int):
    pass
