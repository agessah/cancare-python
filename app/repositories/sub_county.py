from app.db.models import SubCounty
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_filters, apply_search, apply_sort
from fastapi import Request
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, func


class SubCountyRepository(BaseRepository[SubCounty]):
    def __init__(self, db):
        self.db = db
        super().__init__(SubCounty, db)

    async def index(
        self,
        request: Request,
        search: str = None,
        sort: str = None,
        filters: dict = None
    ):
        stmt = select(SubCounty)

        # Auto soft-delete filter
        if hasattr(SubCounty, "deleted_at"):
            stmt = stmt.where(SubCounty.deleted_at is None)

        # Dynamic filtering
        if filters:
            stmt = apply_filters(stmt, SubCounty, filters)

        # Search (only allowed fields)
        if search is not None:
            stmt = apply_search(stmt, SubCounty, search, ["name"])

        # Sorting
        if sort is not None:
            stmt = apply_sort(stmt, SubCounty, sort)

        if "page" in request.query_params and "size" in request.query_params:
            data = await paginate(self.db, stmt)
            return data
        else:
            result = await self.db.execute(stmt)
            return {"data": result.scalars().all()}