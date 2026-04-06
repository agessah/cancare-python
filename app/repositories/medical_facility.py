from app.db.models import MedicalFacility
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_filters, apply_search, apply_sort
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload


class MedicalFacilityRepository(BaseRepository[MedicalFacility]):
    def __init__(self, db):
        self.db = db
        super().__init__(MedicalFacility, db)

    async def index(
        self,
        skip: int = None,
        limit: int = None,
        search: str = None,
        sort: str = None,
        filters: dict = None
    ):
        stmt = select(MedicalFacility).options(
            selectinload(MedicalFacility.county),
            selectinload(MedicalFacility.sub_county),
        )

        # Auto soft-delete filter
        if hasattr(MedicalFacility, "deleted_at"):
            stmt = stmt.where(MedicalFacility.deleted_at == None)

        # Dynamic filtering
        if filters:
            stmt = apply_filters(stmt, MedicalFacility, filters)

        # Search (only allowed fields)
        if search is not None:
            stmt = apply_search(stmt, MedicalFacility, search, ["name"])

        # Sorting
        if sort is not None:
            stmt = apply_sort(stmt, MedicalFacility, sort)

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