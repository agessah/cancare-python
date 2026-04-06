from app.db.models.referral import Referral
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_filters, apply_sort
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload


class ReferralRepository(BaseRepository[Referral]):
    def __init__(self, db):
        self.db = db
        super().__init__(Referral, db)

    async def index(
        self,
        skip: int = None,
        limit: int = None,
        search: str = None,
        sort: str = None,
        filters: dict = None
    ):
        stmt = select(Referral).options(
            selectinload(Referral.patient),
            selectinload(Referral.urgency_level),
            selectinload(Referral.medical_facility)
        )

        # Auto soft-delete filter
        if hasattr(Referral, "deleted_at"):
            stmt = stmt.where(Referral.deleted_at == None)

        # Dynamic filtering
        if filters:
            stmt = apply_filters(stmt, Referral, filters)

        # Search (only allowed fields)
        #stmt = apply_search(stmt, Referral, search, ["name"])

        # Sorting
        if sort is not None:
            stmt = apply_sort(stmt, Referral, sort)

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