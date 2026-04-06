from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.db.models import EncounterAssessment
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_filters, apply_search, apply_sort


class EncounterAssessmentRepository(BaseRepository[EncounterAssessment]):
    def __init__(self, db):
        self.db = db
        super().__init__(EncounterAssessment, db)

    async def index(
        self,
        skip: int = 0,
        limit: int = 20,
        search: str = None,
        sort: str = None,
        filters: dict = None,
    ):
        stmt = select(EncounterAssessment).options(
            selectinload(EncounterAssessment.patient)
        )

        # Auto soft-delete filter
        if hasattr(EncounterAssessment, "deleted_at"):
            stmt = stmt.where(EncounterAssessment.deleted_at == None)

        # Dynamic filtering
        if filters:
            stmt = apply_filters(stmt, EncounterAssessment, filters)

        # Search (only allowed fields)
        if search is not None:
            stmt = apply_search(stmt, EncounterAssessment, search, ["notes"])

        # Sorting
        if sort is not None:
            stmt = apply_sort(stmt, EncounterAssessment, sort)

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