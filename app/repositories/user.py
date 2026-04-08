from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self, db):
        self.db = db
        super().__init__(User, db)

    @staticmethod
    async def get_by_id(db: AsyncSession, resource_id: int) -> User | None:
        result = await db.execute(select(User).where(User.id == resource_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_phone(db: AsyncSession, phone: str) -> User | None:
        result = await db.execute(select(User).where(User.phone == phone))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_token(db: AsyncSession, token: str) -> User | None:
        result = await db.execute(select(User).where(User.token == token))
        return result.scalar_one_or_none()

    @staticmethod
    async def commit(db: AsyncSession):
        await db.commit()
