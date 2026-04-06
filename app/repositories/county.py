from app.db.models import County
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_search, apply_sort
from sqlalchemy import select, func


class CountyRepository(BaseRepository[County]):
    def __init__(self, db):
        self.db = db
        super().__init__(County, db)

    async def index(
        self,
        skip: int = None,
        limit: int = None,
        search: str = None,
        sort: str = None
    ):
        stmt = select(County)

        # Auto soft-delete filter
        if hasattr(County, "deleted_at"):
            stmt = stmt.where(County.deleted_at is None)

        # Search (only allowed fields)
        if search is not None:
            stmt = apply_search(stmt, County, search, ["name", "town"])

        # Sorting
        if sort is not None:
            stmt = apply_sort(stmt, County, sort)

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





    async def sub_counties(
        self,
        #skip: int = 0,
        #limit: int = 20,
        search: str = None,
        sort: str = None,
        #filters: dict = None,
    ):
        stmt = select(County)

        # Auto soft-delete filter
        if hasattr(County, "active"):
            stmt = stmt.where(County.active == True)

        # Dynamic filtering
        #if filters:
            #stmt = apply_filters(stmt, County, filters)

        # Search (only allowed fields)
        if search is not None:
            stmt = apply_search(stmt, County, search, ["name"])

        # Sorting
        if sort is not None:
            stmt = apply_sort(stmt, County, sort)

        # Count total
        #count_stmt = select(func.count()).select_from(stmt.subquery())
        #total = await self.db.scalar(count_stmt)

        # Pagination
        #stmt = stmt.offset(skip).limit(limit)

        result = await self.db.execute(stmt)

        return result.scalars().all()
