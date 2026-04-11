from app.db.models import FollowUp
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_filters, apply_sort

from fastapi import Request
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload


class FollowUpRepository(BaseRepository[FollowUp]):
    def __init__(self, db):
        self.db = db
        super().__init__(FollowUp, db)

    async def index(
        self,
        request: Request,
        search: str = None,
        sort: str = None,
        filters: dict = None
    ):
        stmt = select(FollowUp).options(
            selectinload(FollowUp.referral),
            selectinload(FollowUp.status),
        )

        # Auto soft-delete filter
        if hasattr(FollowUp, "deleted_at"):
            stmt = stmt.where(FollowUp.deleted_at == None)

        # Dynamic filtering
        if filters:
            stmt = apply_filters(stmt, FollowUp, filters)

        # Search (only allowed fields)
        #stmt = apply_search(stmt, Referral, search, ["name"])

        # Sorting
        if sort:
            stmt = apply_sort(stmt, FollowUp, sort)

        if "page" in request.query_params and "size" in request.query_params:
            data = await paginate(self.db, stmt)
            return data
        else:
            result = await self.db.execute(stmt)
            return {"data": result.scalars().all()}