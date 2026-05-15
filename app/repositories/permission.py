from typing import List

from app.db.models.permission import Permission
from app.repositories.base import BaseRepository
from app.utils.query_builder import apply_sort, apply_search

from fastapi import Request
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy import select


class PermissionRepository(BaseRepository[Permission]):
    def __init__(self, db):
        self.db = db
        super().__init__(Permission, db)

    async def index(
        self,
        request: Request,
        search: str = None,
        sort: str = None
    ):
        stmt = select(Permission)

        # Search (only allowed fields)
        if search:
            stmt = apply_search(stmt, Permission, search, ["name"])

        # Sorting
        if sort:
            stmt = apply_sort(stmt, Permission, sort)

        if "page" in request.query_params and "size" in request.query_params:
            data = await paginate(self.db, stmt)
            return data
        else:
            result = await self.db.execute(stmt)
            return {"data": result.scalars().all()}


    async def get_permissions(self, permission_ids: List[int]):
        stmt = select(Permission).where(Permission.id.in_(permission_ids))
        result = await self.db.execute(stmt)
        return result.scalars().all()