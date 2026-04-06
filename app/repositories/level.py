from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Level


class LevelRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def index(self):
        result = await self.db.execute(select(Level))
        return result.unique().scalars().all()