from app.db.models import User
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_filters, apply_search, apply_sort
from fastapi import Request
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

class UserRepository(BaseRepository[User]):
    def __init__(self, db):
        self.db = db
        super().__init__(User, db)


    async def get_by_email(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.unique().scalar_one_or_none()


    async def get_by_phone(self, phone: str):
        result = await self.db.execute(select(User).where(User.phone == phone))
        return result.unique().scalar_one_or_none()

    async def get_by_username(self, value: str):
        result = await self.db.execute(select(User).where(or_(User.email == value, User.phone == value)))
        return result.unique().scalar_one_or_none()


    async def get_by_token(self, token: str) -> User | None:
        result = await self.db.execute(select(User).where(User.token == token))
        return result.unique().scalar_one_or_none()


    async def index(
        self,
        request: Request,
        search: str = None,
        sort: str = None,
        filters: dict = None
    ):
        stmt = select(User).options(
            selectinload(User.roles),
        )

        # Auto soft-delete filter
        if hasattr(User, "deleted_at"):
            stmt = stmt.where(User.deleted_at == None)

        # Dynamic filtering
        if filters:
            stmt = apply_filters(stmt, User, filters)

        # Search (only allowed fields)
        if search:
            stmt = apply_search(stmt, User, search, ["name", "phone"])

        # Sorting
        if sort:
            stmt = apply_sort(stmt, User, sort)

        if "page" in request.query_params and "size" in request.query_params:
            data =  await paginate(self.db, stmt)
            return data
        else :
            result = await self.db.execute(stmt)
            return { "data": result.scalars().all() }