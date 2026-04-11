from app.db.models import MedicalFacility
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_filters, apply_search, apply_sort
from fastapi import Request
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class MedicalFacilityRepository(BaseRepository[MedicalFacility]):
    def __init__(self, db):
        self.db = db
        super().__init__(MedicalFacility, db)

    async def index(
        self,
        request: Request,
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

        if "page" in request.query_params and "size" in request.query_params:
            data = await paginate(self.db, stmt)
            return data
        else:
            result = await self.db.execute(stmt)
            return {"data": result.scalars().all()}