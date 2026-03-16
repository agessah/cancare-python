from typing import List

from app.db.models import County
from app.repositories.county import CountyRepository

class CountyService:
    def __init__(self, repo: CountyRepository):
        self.repo = repo

    async def index(
            self,
            skip: int = None,
            limit: int = None,
            search: str = None,
            sort: str = None
    ):
        return await self.repo.index(
            skip=skip,
            limit=limit,
            search=search,
            sort=sort
        )

    async def show(self, id: int):
        resource = await self.repo.get(id)

        if not resource:
            raise HTTPException(status_code=404, detail="County not found!")

        return resource
