from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import FollowUpStatus


class FollowUpStatusRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def index(self):
        result = await self.db.execute(select(FollowUpStatus))
        return {"data": result.unique().scalars().all()}