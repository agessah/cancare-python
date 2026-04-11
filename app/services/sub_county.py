from app.repositories import SubCountyRepository
from fastapi import HTTPException, Request


class SubCountyService:
    def __init__(self, repo: SubCountyRepository):
        self.repo = repo

    async def index(
        self,
        request: Request,
        search: str = None,
        sort: str = None,
        filters: dict = None
    ):
        return await self.repo.index(
            request=request,
            search=search,
            sort=sort,
            filters=filters
        )

    async def show(self, resource_id: int):
        resource = await self.repo.get(resource_id)

        if not resource:
            raise HTTPException(404, "Sub-County not found!")

        return resource