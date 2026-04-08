from app.repositories import UserRepository
from fastapi import HTTPException


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def show(self, resource_id: int):
        resource = await self.repo.get(resource_id)

        if not resource:
            raise HTTPException(404, "User not found")

        return { "data": resource }