from typing import List

from app.repositories import UserRepository, RoleRepository
from app.core.security import hash_password
from fastapi import HTTPException, Request


class UserService:
    def __init__(self, repo: UserRepository, role_repo: RoleRepository):
        self.repo = repo
        self.role_repo = role_repo


    async def create(self, payload):
        email_exists = await self.repo.get_by_email(payload.email)

        if email_exists:
            raise HTTPException(status_code=400, detail="Email already exists")

        phone_exists = await self.repo.get_by_phone(payload.phone)

        if phone_exists:
            raise HTTPException(status_code=400, detail="Phone already exists")

        data = payload.model_dump()
        password = data.pop("password")
        role_ids = data.pop("role_ids", [])
        data["password"] = hash_password(password)
        data["active"] = True
        data["roles"] = await self.role_repo.get_roles(role_ids)

        return await self.repo.create(data)


    async def update(self, resource_id, payload):
        resource = await self.repo.get(resource_id)

        if not resource:
            raise HTTPException(404, "User not found")

        data = payload.model_dump(exclude_unset=True)
        password = data.pop("password")
        role_ids = data.pop("role_ids", [])
        data["password"] = hash_password(password)
        data["active"] = True
        data["roles"] = await self.role_repo.get_roles(role_ids)

        return await self.repo.update(resource_id, data)


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
            raise HTTPException(404, "User not found")

        return resource


    async def assign_roles(self, user_id: int, role_ids: List[int]):
        user = await self.repo.get(user_id)

        if not user:
            raise HTTPException(404, "User not found")

        roles = await self.role_repo.get_roles(role_ids)
        if not roles:
            raise HTTPException(404, "No matching roles found")

        return await self.repo.sync_roles(user, roles)