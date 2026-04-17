from app.db.models import Patient
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_filters, apply_search, apply_sort
from fastapi import Request
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
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
        request: Request,
        search: str = None,
        sort: str = None,
        filters: dict = None
    ):
        stmt = select(Patient).options(
            selectinload(Patient.gender),
            selectinload(Patient.county),
            selectinload(Patient.sub_county),
        )

        # Auto soft-delete filter
        if hasattr(Patient, "deleted_at"):
            stmt = stmt.where(Patient.deleted_at is None)

        # Dynamic filtering
        if filters:
            stmt = apply_filters(stmt, Patient, filters)

        # Search (only allowed fields)
        if search:
            stmt = apply_search(stmt, Patient, search, ["name", "phone", "location"])

        # Sorting
        if sort:
            stmt = apply_sort(stmt, Patient, sort)

        if "page" in request.query_params and "size" in request.query_params:
            data =  await paginate(self.db, stmt)
            return data
        else :
            result = await self.db.execute(stmt)
            return { "data": result.scalars().all() }