from typing import List

from app.db.models import SubCounty
from app.repositories.sub_county import SubCountyRepository

class SubCountyService:
    def __init__(self, repo: SubCountyRepository):
        self.repo = repo

    async def index(
        self,
        skip: int = None,
        limit: int = None,
        search: str = None,
        sort: str = None,
        filters: dict = None
    ):
        return await self.repo.index(
            skip=skip,
            limit=limit,
            search=search,
            sort=sort,
            filters=filters
        )

    async def show(self, id: int):
        resource = await self.repo.get(id)

        if not resource:
            raise HTTPException(status_code=404, detail="Sub-County not found!")

        return resource
