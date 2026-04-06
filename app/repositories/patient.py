from app.db.models import Patient
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_filters, apply_search, apply_sort
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload


class PatientRepository(BaseRepository[Patient]):
    def __init__(self, db):
        self.db = db
        super().__init__(Patient, db)

    async def get_by_phone(self, phone: str):
        result = await self.db.execute(
            select(Patient).where(Patient.phone == phone)
        )
        return result.unique().scalar_one_or_none()

    async def index(
        self,
        skip: int = 0,
        limit: int = 20,
        search: str = None,
        sort: str = None,
        filters: dict = None,
    ):
        stmt = select(Patient).options(
            selectinload(Patient.gender),
            selectinload(Patient.county),
            selectinload(Patient.sub_county),
        )

        # Auto soft-delete filter
        if hasattr(Patient, "deleted_at"):
            stmt = stmt.where(Patient.deleted_at == None)

        # Dynamic filtering
        if filters:
            stmt = apply_filters(stmt, Patient, filters)

        # Search (only allowed fields)
        if search is not None:
            stmt = apply_search(stmt, Patient, search, ["name", "phone", "location"])

        # Sorting
        if sort is not None:
            stmt = apply_sort(stmt, Patient, sort)

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