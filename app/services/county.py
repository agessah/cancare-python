from app.repositories import CountyRepository
from fastapi import HTTPException


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

    async def show(self, resource_id: int):
        resource = await self.repo.get(resource_id)

        if not resource:
            raise HTTPException(status_code=404, detail="County not found!")

        return resource
