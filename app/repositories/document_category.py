from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DocumentCategory


class DocumentCategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def index(self):
        result = await self.db.execute(select(DocumentCategory))
        return result.unique().scalars().all()