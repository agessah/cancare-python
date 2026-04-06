from fastapi import HTTPException

from app.repositories import ReferralRepository


class ReferralService:
    def __init__(self, repo: ReferralRepository):
        self.repo = repo

    async def create(self, payload):
        return await self.repo.create(payload.model_dump())

    async def update(self, resource_id, payload):
        resource = await self.repo.get(resource_id)

        if not resource:
            raise HTTPException(status_code=404, detail="Encounters assessment not found!")

        return await self.repo.update(resource_id, payload.model_dump(exclude_unset=True))

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
            raise HTTPException(status_code=404, detail="Record not found!")

        return resource