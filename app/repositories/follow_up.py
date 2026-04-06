from app.db.models import FollowUp
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_filters, apply_sort
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload


class FollowUpRepository(BaseRepository[FollowUp]):
    def __init__(self, db):
        self.db = db
        super().__init__(FollowUp, db)

    async def index(
        self,
        skip: int = None,
        limit: int = None,
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
        if sort is not None:
            stmt = apply_sort(stmt, FollowUp, sort)

        total = 0
        if skip is not None and limit is not None:
            # Count total
            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = await self.db.scalar(count_stmt)

            # Pagination
            stmt = stmt.offset(skip).limit(limit)

        result = await self.db.execute(stmt)

        if skip is not None and limit is not None:
            return {
                "total": total,
                "items": result.scalars().all()
            }

        return result.unique().scalars().all()