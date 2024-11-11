from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db


class BaseService:
    def __init__(self, db: Annotated[Any, Depends(get_db)]):
        self.db = db

    async def commit(self):
        await self.db.commit()

    async def refresh(self, obj):
        await self.db.refresh(obj)
