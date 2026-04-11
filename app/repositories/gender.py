from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Gender


class GenderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def index(self):
        result = await self.db.execute(select(Gender))
        return {"data": result.unique().scalars().all()}