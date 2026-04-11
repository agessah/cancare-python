from app.db.models import County
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_search, apply_sort
from fastapi import Request
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select


class CountyRepository(BaseRepository[County]):
    def __init__(self, db):
        self.db = db
        super().__init__(County, db)

    async def index(
        self,
        request: Request,
        search: str = None,
        sort: str = None
    ):
        stmt = select(County)

        # Auto soft-delete filter
        if hasattr(County, "deleted_at"):
            stmt = stmt.where(County.deleted_at is None)

        # Search (only allowed fields)
        if search:
            stmt = apply_search(stmt, County, search, ["name", "town"])

        # Sorting
        if sort:
            stmt = apply_sort(stmt, County, sort)

        if "page" in request.query_params and "size" in request.query_params:
            data = await paginate(self.db, stmt)
            return data
        else:
            result = await self.db.execute(stmt)
            return {"data": result.scalars().all()}