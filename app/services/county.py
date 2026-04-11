from app.repositories import CountyRepository
from fastapi import HTTPException, Request


class CountyService:
    def __init__(self, repo: CountyRepository):
        self.repo = repo

    async def index(
            self,
            request: Request,
            search: str = None,
            sort: str = None
    ):
        return await self.repo.index(
            request=request,
            search=search,
            sort=sort
        )

    async def show(self, resource_id: int):
        resource = await self.repo.get(resource_id)

        if not resource:
            raise HTTPException(404, "County not found!")

        return resource
