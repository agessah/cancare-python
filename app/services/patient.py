from app.repositories import PatientRepository
from fastapi import HTTPException, Request


class PatientService:
    def __init__(self, repo: PatientRepository):
        self.repo = repo


    async def create(self, payload):
        # Check duplicate phone
        exists = await self.repo.get_by_phone(payload.phone)

        if exists:
            raise HTTPException(status_code=400, detail="Phone already exists")

        return await self.repo.create(payload.model_dump())


    async def update(self, resource_id, payload):
        resource = await self.repo.get(resource_id)

        if not resource:
            raise HTTPException(404, "Patient not found")

        return await self.repo.update(resource_id, payload.model_dump(exclude_unset=True))


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
            raise HTTPException(status_code=404, detail="Patient not found")

        return resource