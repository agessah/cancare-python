from app.repositories import SubCountyRepository
from fastapi import HTTPException


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

    async def show(self, resource_id: int):
        resource = await self.repo.get(resource_id)

        if not resource:
            raise HTTPException(status_code=404, detail="Sub-County not found!")

        return resource
