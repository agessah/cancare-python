from app.db.models import SubCounty
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_filters, apply_search, apply_sort
from sqlalchemy import select, func


class SubCountyRepository(BaseRepository[SubCounty]):
    def __init__(self, db):
        self.db = db
        super().__init__(SubCounty, db)

    async def index(
        self,
        skip: int = None,
        limit: int = None,
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